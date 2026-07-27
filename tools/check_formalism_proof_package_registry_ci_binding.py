#!/usr/bin/env python3
"""Validate the proof-package registry CI-binding contract fail-closed."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "status/formalism_proof_package_registry_ci_binding.pending.json"
OUTPUT = ROOT / "reports/formalism_proof_package_registry_ci_binding_verification.json"

EXPECTED_COMMAND = [
    "python",
    "tools/run_declared_tasks.py",
    "tools/tasks/formalism_proof_package_registry_tasks.json",
    "--task-id",
    "check_formalism_proof_package_registry",
]


def main() -> int:
    errors: list[str] = []
    record = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if record.get("schema") != "stegverse.formalism-tests.proof-package-registry-ci-binding.v1":
        errors.append("schema mismatch")
    if record.get("repository") != "Data-Continuation/formalism-tests":
        errors.append("repository mismatch")
    if record.get("issue") != 7:
        errors.append("issue must equal 7")
    if record.get("task_id") != "check_formalism_proof_package_registry":
        errors.append("task_id mismatch")
    if record.get("required_command") != EXPECTED_COMMAND:
        errors.append("required command mismatch")
    if record.get("expected_output") != "reports/formalism_proof_package_registry_verification.json":
        errors.append("expected output mismatch")
    if record.get("authority_posture") != "REGISTRY_CONSISTENCY_ONLY":
        errors.append("authority posture mismatch")
    if record.get("promotion_eligible") is not False:
        errors.append("promotion_eligible must remain false until verified")
    if record.get("canonical_proof_issues_satisfied") != []:
        errors.append("CI binding cannot satisfy canonical proof issues")

    requirements = record.get("binding_requirements", {})
    for key in (
        "inspect_existing_workflow_first",
        "reuse_existing_workflow",
        "competing_workflow_prohibited",
        "durable_workflow_evidence_required",
    ):
        if requirements.get(key) is not True:
            errors.append(f"{key} must be true")
    if requirements.get("report_status_required") != "PASS":
        errors.append("report_status_required must be PASS")
    if requirements.get("expected_package_count") != 4:
        errors.append("expected_package_count must be 4")
    if requirements.get("expected_active_owner_count") != 4:
        errors.append("expected_active_owner_count must be 4")

    observed = record.get("observed", {})
    verified = observed.get("binding_verified") is True
    if record.get("status") == "PENDING_EXISTING_WORKFLOW_BINDING":
        if verified:
            errors.append("pending status cannot claim verified binding")
        if observed.get("canonical_execution_claimed") is not False:
            errors.append("canonical_execution_claimed must remain false")
    elif record.get("status") == "VERIFIED_EXISTING_WORKFLOW_BINDING":
        if not verified:
            errors.append("verified status requires binding_verified=true")
        workflow_path = observed.get("workflow_path")
        commit_sha = observed.get("commit_sha")
        report_sha = observed.get("report_sha256")
        if not isinstance(workflow_path, str) or not workflow_path.startswith(".github/workflows/"):
            errors.append("verified binding requires an existing workflow path")
        if not isinstance(commit_sha, str) or re.fullmatch(r"[0-9a-f]{40}", commit_sha) is None:
            errors.append("verified binding requires a 40-character commit SHA")
        if not isinstance(report_sha, str) or re.fullmatch(r"[0-9a-f]{64}", report_sha) is None:
            errors.append("verified binding requires a report SHA-256")
    else:
        errors.append("invalid status")

    result = {
        "schema": "stegverse.formalism-tests.proof-package-registry-ci-binding-verification.v1",
        "status": "PASS" if not errors else "FAIL",
        "binding_status": record.get("status"),
        "binding_verified": verified,
        "promotion_eligible": False,
        "canonical_proof_issues_satisfied": [],
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
