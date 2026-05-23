#!/usr/bin/env python3
from __future__ import annotations

import ast
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPO = "Data-Continuation/core-lite"
DEFAULT_BRANCH = "main"
DEFAULT_WORK_DIR = Path(tempfile.gettempdir()) / "stegverse-001-cge-contractual-inclusion"

REPORT_DIR = Path("reports/current/stegverse-001-cge-contractual-inclusion")
RECEIPT_DIR = Path("receipts/current/stegverse-001-cge-contractual-inclusion")
DIST_DIR = Path("dist/current/stegverse-001-cge-contractual-inclusion")

REPORT_JSON = REPORT_DIR / "candidate_report.json"
REPORT_MD = REPORT_DIR / "candidate_report.md"
CANDIDATE_MANIFEST = DIST_DIR / "candidate_manifest.json"
PATCH_FILE = DIST_DIR / "core_lite_cge_contractual_inclusion.patch"
CANDIDATE_CGE = DIST_DIR / "core_lite/cge.py"
RECEIPTS = RECEIPT_DIR / "receipts.jsonl"

REQUIRED_EXPORT = "generate_cge_fingerprint"
PRESERVE_EXPORTS = {"CGEDecision", "precheck_manifest", "classify_sandbox_result"}


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_dict(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class ReceiptChain:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.previous_hash = self._last_hash()

    def _last_hash(self) -> str | None:
        if not self.path.exists():
            return None
        last = None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                last = json.loads(line).get("receipt_hash")
            except json.JSONDecodeError:
                continue
        return last

    def record(self, event_type: str, decision: str, basis: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        receipt = {
            "schema": "stegverse_001_cge_contractual_inclusion_receipt.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "actor": "StegVerse-001",
            "event_type": event_type,
            "decision": decision,
            "basis": basis,
            "previous_receipt_hash": self.previous_hash,
            "metadata": metadata or {},
        }
        receipt["receipt_hash"] = hash_dict(receipt)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(receipt) + "\n")
        self.previous_hash = receipt["receipt_hash"]
        return receipt


def clone_target(receipts: ReceiptChain) -> tuple[Path | None, dict[str, Any]]:
    local = os.environ.get("CORE_LITE_LOCAL_PATH", "").strip()
    repo = os.environ.get("CORE_LITE_REPO", DEFAULT_REPO).strip() or DEFAULT_REPO
    branch = os.environ.get("CORE_LITE_BRANCH", DEFAULT_BRANCH).strip() or DEFAULT_BRANCH
    token = os.environ.get("CORE_LITE_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""

    if local:
        local_path = Path(local)
        meta = {"mode": "local", "repo": repo, "branch": branch, "root": local_path.as_posix(), "success": local_path.exists()}
        receipts.record("target_repo_selected", "LOCAL_PATH_SELECTED" if meta["success"] else "FAIL_CLOSED", "Selected local core-lite target for candidate generation.", meta)
        return (local_path if local_path.exists() else None), meta

    work_dir = Path(os.environ.get("CORE_LITE_WORK_DIR", str(DEFAULT_WORK_DIR)))
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    clone_dir = work_dir / "core-lite"

    if repo.startswith(("http://", "https://")):
        url = repo
        safe_repo = repo
    else:
        safe_repo = repo
        url = f"https://x-access-token:{token}@github.com/{repo}.git" if token else f"https://github.com/{repo}.git"

    proc = subprocess.run(["git", "clone", "--depth", "1", "--branch", branch, url, str(clone_dir)], text=True, capture_output=True)
    meta = {
        "mode": "clone",
        "repo": safe_repo,
        "branch": branch,
        "root": clone_dir.as_posix(),
        "runtime_work_dir": work_dir.as_posix(),
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "runtime_committed_path": False,
    }
    receipts.record("target_repo_cloned", "CLONED" if proc.returncode == 0 else "FAIL_CLOSED", "Cloned core-lite into runtime temp space for candidate generation.", meta)
    return (clone_dir if proc.returncode == 0 else None), meta


def parse_exports(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    exports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            exports.add(node.name)
    return exports


def append_generate_cge_fingerprint(source: str) -> str:
    if REQUIRED_EXPORT in parse_exports(source):
        return source

    block = '''
def generate_cge_fingerprint(*args: Any, **kwargs: Any) -> dict[str, Any]:
    # Additive compatibility surface for core-lite CLI.
    import hashlib
    import json
    from datetime import datetime, timezone

    def _safe(value: Any) -> Any:
        try:
            json.dumps(value, sort_keys=True, default=str)
            return value
        except TypeError:
            return repr(value)

    payload = {
        "schema": "stegverse_core_lite_cge_fingerprint_input.v1",
        "args": [_safe(value) for value in args],
        "kwargs": {str(key): _safe(value) for key, value in sorted(kwargs.items())},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    input_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    return {
        "schema": "stegverse_core_lite_cge_fingerprint.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision_scope": "initialization_contractual_inclusion",
        "input_hash": input_hash,
        "available_cge_surfaces": [
            "CGEDecision",
            "precheck_manifest",
            "classify_sandbox_result",
        ],
        "install_authority": False,
        "production_authority": False,
        "node_status": False,
        "finco_eligibility": False,
    }
'''
    suffix = "\n" if source.endswith("\n") else "\n\n"
    return source + suffix + block


def write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# StegVerse-001 CGE Contractual Inclusion Candidate Report",
        "",
        "## Status",
        "",
        "```text",
        f"actor: {report['actor']}",
        f"transition: {report['transition']}",
        f"decision: {report['decision']}",
        f"success: {str(report['success']).lower()}",
        "```",
        "",
        "## Candidate",
        "",
        "```text",
        "target: core_lite/cge.py",
        "required_export: generate_cge_fingerprint",
        "preserve_existing_exports: true",
        "mutation_to_core_lite_performed: false",
        "```",
        "",
        "## Outputs",
        "",
        "```text",
        f"candidate_file: {report['outputs']['candidate_file']}",
        f"patch_file: {report['outputs']['patch_file']}",
        f"candidate_manifest: {report['outputs']['candidate_manifest']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "No push to core-lite.",
        "No workflow changes.",
        "No incoming bundle submission.",
        "No production.",
        "Candidate only.",
        "Return report and receipt.",
        "STOP.",
        "```",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    receipts = ReceiptChain(RECEIPTS)
    receipts.record("candidate_builder_started", "RECEIVED", "StegVerse-001 started CGE contractual inclusion candidate builder.", {"target": "core_lite/cge.py", "required_export": REQUIRED_EXPORT})

    repo_root, access = clone_target(receipts)
    if repo_root is None:
        failure = {"schema": "stegverse_001_cge_contractual_inclusion_candidate_report.v1", "generated_at": datetime.now(timezone.utc).isoformat(), "success": False, "decision": "FAIL_CLOSED", "basis": "Could not access core-lite target.", "target_access": access}
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    source_path = repo_root / "core_lite" / "cge.py"
    if not source_path.exists():
        failure = {"schema": "stegverse_001_cge_contractual_inclusion_candidate_report.v1", "generated_at": datetime.now(timezone.utc).isoformat(), "success": False, "decision": "FAIL_CLOSED", "basis": "core_lite/cge.py not found in target repo.", "target_access": access}
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    original = source_path.read_text(encoding="utf-8")
    original_exports = parse_exports(original)
    missing_preserved = sorted(PRESERVE_EXPORTS - original_exports)

    if missing_preserved:
        decision = "FAIL_CLOSED"
        basis = "Existing CGE surfaces required for preservation are missing."
        candidate = original
    else:
        candidate = append_generate_cge_fingerprint(original)
        decision = "CANDIDATE_PREPARED"
        basis = "Prepared additive contractual inclusion candidate for generate_cge_fingerprint."

    CANDIDATE_CGE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_CGE.write_text(candidate, encoding="utf-8")

    diff = "".join(difflib.unified_diff(original.splitlines(keepends=True), candidate.splitlines(keepends=True), fromfile="core_lite/cge.py", tofile="core_lite/cge.py"))
    PATCH_FILE.write_text(diff, encoding="utf-8")

    candidate_exports = parse_exports(candidate)
    manifest = {
        "schema": "stegverse_001_cge_contractual_inclusion_candidate_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "actor": "StegVerse-001",
        "transition": "CONTRACTUAL_INCLUSION_CANDIDATE",
        "target_repo": access.get("repo", DEFAULT_REPO),
        "target_path": "core_lite/cge.py",
        "required_export": REQUIRED_EXPORT,
        "preserve_exports": sorted(PRESERVE_EXPORTS),
        "original_sha256": sha256_text(original),
        "candidate_sha256": sha256_text(candidate),
        "patch_sha256": sha256_text(diff),
        "mutation_to_target_performed": False,
        "workflow_change_authority": False,
        "push_authority": False,
        "incoming_submission_authority": False,
        "stop_condition": "Candidate prepared. Report and receipt returned. STOP.",
    }
    CANDIDATE_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = {
        "schema": "stegverse_001_cge_contractual_inclusion_candidate_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": decision == "CANDIDATE_PREPARED",
        "actor": "StegVerse-001",
        "transition": "Core-Lite CGE Contractual Inclusion Candidate",
        "decision": decision,
        "basis": basis,
        "target_access": access,
        "target_path": "core_lite/cge.py",
        "required_export": REQUIRED_EXPORT,
        "original_exports": sorted(original_exports),
        "candidate_exports": sorted(candidate_exports),
        "preserved_exports": sorted(PRESERVE_EXPORTS),
        "missing_preserved_exports": missing_preserved,
        "added_export_present": REQUIRED_EXPORT in candidate_exports,
        "mutation_to_target_performed": False,
        "outputs": {
            "candidate_file": CANDIDATE_CGE.as_posix(),
            "patch_file": PATCH_FILE.as_posix(),
            "candidate_manifest": CANDIDATE_MANIFEST.as_posix(),
        },
        "boundary": [
            "formalism-tests is the command backdrop.",
            "core-lite is the remote target.",
            "This task prepares a candidate only.",
            "This task does not patch, push, submit incoming bundles, or change workflows.",
            "STOP after report, candidate, patch, manifest, and receipt.",
        ],
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report)
    receipts.record("candidate_prepared", decision, basis, {"report": REPORT_JSON.as_posix(), "candidate_manifest": CANDIDATE_MANIFEST.as_posix(), "patch": PATCH_FILE.as_posix(), "candidate_file": CANDIDATE_CGE.as_posix(), "added_export_present": REQUIRED_EXPORT in candidate_exports})
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
