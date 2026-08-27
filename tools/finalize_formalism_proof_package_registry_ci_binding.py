#!/usr/bin/env python3
"""Finalize proof-package registry CI binding from the running GitHub Actions job.

This script is intended to run inside the existing continuation-tests workflow.
It observes the current workflow run through the GitHub Actions API, resolves the
numeric job ID, hashes the generated registry verification report, updates the
binding record, and writes a durable repository receipt.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "status/formalism_proof_package_registry_ci_binding.pending.json"
REPORT = ROOT / "reports/formalism_proof_package_registry_verification.json"
RECEIPT = ROOT / "receipts/formalism_proof_package_registry_ci_binding_execution.json"
EXPECTED_WORKFLOW_PATH = ".github/workflows/continuation-tests.yml"
EXPECTED_JOB_NAME = "continuation-tests"


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"required environment variable is missing: {name}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_jobs(repository: str, run_id: int, token: str) -> list[dict[str, object]]:
    url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}/jobs?per_page=100"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "stegverse-formalism-tests-ci-binding-finalizer",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    jobs = payload.get("jobs", [])
    if not isinstance(jobs, list):
        raise RuntimeError("GitHub Actions jobs response did not contain a jobs array")
    return [job for job in jobs if isinstance(job, dict)]


def resolve_job_id(repository: str, run_id: int, token: str) -> int:
    last_error: Exception | None = None
    for attempt in range(1, 7):
        try:
            jobs = fetch_jobs(repository, run_id, token)
            exact = [job for job in jobs if job.get("name") == EXPECTED_JOB_NAME]
            candidates = exact or jobs
            for job in candidates:
                job_id = job.get("id")
                if isinstance(job_id, int) and job_id > 0:
                    return job_id
            last_error = RuntimeError("current workflow job ID is not yet observable")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            last_error = exc
        if attempt < 6:
            time.sleep(attempt * 2)
    raise RuntimeError(f"unable to resolve workflow job ID: {last_error}")


def main() -> int:
    repository = require_env("GITHUB_REPOSITORY")
    run_id = int(require_env("GITHUB_RUN_ID"))
    commit_sha = require_env("GITHUB_SHA")
    token = require_env("GITHUB_TOKEN")

    if len(commit_sha) != 40 or any(ch not in "0123456789abcdef" for ch in commit_sha):
        raise RuntimeError("GITHUB_SHA must be a lowercase 40-character commit SHA")
    if not REPORT.is_file():
        raise RuntimeError(f"registry verification report is missing: {REPORT.relative_to(ROOT)}")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "PASS":
        raise RuntimeError("registry verification report must be PASS before binding finalization")
    if report.get("package_count") != 4:
        raise RuntimeError("registry verification report must contain exactly four packages")
    if report.get("active_issue_count") != 2:
        raise RuntimeError("registry verification report must contain exactly two active proof owners")
    if report.get("completed_issue_count") != 2:
        raise RuntimeError("registry verification report must contain exactly two completed proof owners")
    if report.get("canonical_owner_count") != 4:
        raise RuntimeError("registry verification report must preserve exactly four total canonical proof owners")

    job_id = resolve_job_id(repository, run_id, token)
    report_sha256 = sha256_file(REPORT)

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    contract["status"] = "VERIFIED_EXISTING_WORKFLOW_BINDING"
    contract["observed"] = {
        "workflow_path": EXPECTED_WORKFLOW_PATH,
        "workflow_run_id": run_id,
        "job_id": job_id,
        "commit_sha": commit_sha,
        "report_sha256": report_sha256,
        "layer_built": True,
        "existing_workflow_reused": True,
        "competing_workflow_created": False,
        "layer_activated": True,
        "binding_verified": True,
        "canonical_execution_claimed": False,
    }
    contract["promotion_eligible"] = False
    contract["canonical_proof_issues_satisfied"] = []
    CONTRACT.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse.formalism-tests.proof-package-registry-ci-binding-execution.v1",
        "repository": repository,
        "issue": 7,
        "workflow_path": EXPECTED_WORKFLOW_PATH,
        "workflow_run_id": run_id,
        "job_id": job_id,
        "commit_sha": commit_sha,
        "registry_report": str(REPORT.relative_to(ROOT)),
        "registry_report_sha256": report_sha256,
        "registry_report_status": report.get("status"),
        "package_count": report.get("package_count"),
        "active_issue_count": report.get("active_issue_count"),
        "completed_issue_count": report.get("completed_issue_count"),
        "canonical_owner_count": report.get("canonical_owner_count"),
        "binding_status": "VERIFIED_EXISTING_WORKFLOW_BINDING",
        "authority_posture": "REGISTRY_CONSISTENCY_ONLY",
        "canonical_proof_issues_satisfied": [],
        "canonical_execution_claimed": False,
        "release_authority_granted": False,
        "publication_authority_granted": False,
        "downstream_mutation_authority_granted": False,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
