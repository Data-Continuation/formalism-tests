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
DEFAULT_WORK_DIR = Path(tempfile.gettempdir()) / "stegverse-001-cli-dependency-contract"

REPORT_DIR = Path("reports/current/stegverse-001-cli-dependency-contract")
RECEIPT_DIR = Path("receipts/current/stegverse-001-cli-dependency-contract")
DIST_DIR = Path("dist/current/stegverse-001-cli-dependency-contract")

REPORT_JSON = REPORT_DIR / "candidate_report.json"
REPORT_MD = REPORT_DIR / "candidate_report.md"
CANDIDATE_MANIFEST = DIST_DIR / "candidate_manifest.json"
PATCH_FILE = DIST_DIR / "cli_dependency_contractual_inclusion.patch"
CANDIDATE_INGEST = DIST_DIR / "core_lite/ingest.py"
CANDIDATE_RECEIPTS = DIST_DIR / "core_lite/receipts.py"
RECEIPTS = RECEIPT_DIR / "receipts.jsonl"

INGEST_REQUIRED = {"ingest_incoming", "load_core_policy"}
RECEIPTS_REQUIRED = {"append_receipt"}
INGEST_PRESERVE = {"run_ingestion", "load_manifest", "write_markdown_report"}
RECEIPTS_PRESERVE = {"ReceiptRecorder"}


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
            "schema": "stegverse_001_cli_dependency_contract_receipt.v1",
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


LOAD_CORE_POLICY_BLOCK = '''
def load_core_policy(repo_root: Path | str = ".") -> dict[str, Any]:
    root = Path(repo_root)
    policy_candidates = [
        root / "core_lite_policy.json",
        root / ".stegverse" / "core_lite_policy.json",
        root / "policy" / "core_lite_policy.json",
    ]
    for candidate in policy_candidates:
        if candidate.exists() and candidate.is_file():
            try:
                return json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {
                    "schema": "stegverse_core_lite_policy.v1",
                    "policy_loaded": False,
                    "policy_error": "invalid_json",
                    "policy_path": candidate.as_posix(),
                    "install_authority": False,
                    "production_authority": False,
                }
    return {
        "schema": "stegverse_core_lite_policy.v1",
        "policy_loaded": False,
        "policy_path": None,
        "install_authority": False,
        "production_authority": False,
        "node_status": False,
        "finco_eligibility": False,
    }
'''

INGEST_INCOMING_BLOCK = '''
def ingest_incoming(repo_root: Path | str = ".", *, task_id: str = "", skip_tasks: bool = False) -> dict[str, Any]:
    root = Path(repo_root)
    incoming = root / "incoming"

    if not incoming.exists():
        report = {
            "schema": "stegverse_core_lite_ingest_incoming_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": True,
            "decision": "NO_INCOMING_DIRECTORY",
            "repo_root": root.as_posix(),
            "incoming": incoming.as_posix(),
            "task_id": task_id,
            "skip_tasks": skip_tasks,
            "install_authority": False,
            "production_authority": False,
        }
        (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
        return report

    bundles = sorted([path for path in incoming.iterdir() if path.is_file()])
    if not bundles:
        report = {
            "schema": "stegverse_core_lite_ingest_incoming_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": True,
            "decision": "NO_INCOMING_BUNDLES",
            "repo_root": root.as_posix(),
            "incoming": incoming.as_posix(),
            "task_id": task_id,
            "skip_tasks": skip_tasks,
            "install_authority": False,
            "production_authority": False,
        }
        (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
        return report

    results = [run_ingestion(bundle, repo_root=root) for bundle in bundles]
    report = {
        "schema": "stegverse_core_lite_ingest_incoming_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": all(bool(item.get("success")) for item in results),
        "decision": "INGESTION_ATTEMPTED",
        "repo_root": root.as_posix(),
        "incoming": incoming.as_posix(),
        "bundle_count": len(bundles),
        "task_id": task_id,
        "skip_tasks": skip_tasks,
        "results": results,
        "install_authority": False,
        "production_authority": False,
    }
    (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
    return report
'''

APPEND_RECEIPT_BLOCK = '''
def append_receipt(repo_root: Path | str = ".", receipt: dict[str, Any] | None = None, **metadata: Any) -> dict[str, Any]:
    root = Path(repo_root)
    recorder = ReceiptRecorder(root / ".stegverse" / "receipts" / "core_lite_receipts.jsonl")
    payload = receipt if receipt is not None else {}
    if not isinstance(payload, dict):
        payload = {"value": repr(payload)}
    if metadata:
        payload = {**payload, **metadata}
    return recorder.record(
        event_type=str(payload.get("event_type", "core_lite_cli_receipt")),
        decision=str(payload.get("decision", "RECORDED")),
        basis=str(payload.get("basis", "Core-Lite CLI receipt recorded.")),
        metadata=payload,
    )
'''


def append_ingest_contract(source: str) -> str:
    exports = parse_exports(source)
    additions = []
    if "load_core_policy" not in exports:
        additions.append(LOAD_CORE_POLICY_BLOCK)
    if "ingest_incoming" not in exports:
        additions.append(INGEST_INCOMING_BLOCK)
    if not additions:
        return source
    suffix = "\n" if source.endswith("\n") else "\n\n"
    return source + suffix + "\n".join(additions).lstrip()


def append_receipts_contract(source: str) -> str:
    if "append_receipt" in parse_exports(source):
        return source
    suffix = "\n" if source.endswith("\n") else "\n\n"
    return source + suffix + APPEND_RECEIPT_BLOCK.lstrip()


def write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# StegVerse-001 CLI Dependency Contractual Inclusion Candidate Report",
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
        "## Candidate Targets",
        "",
        "```text",
        "core_lite/ingest.py:",
        "  add ingest_incoming",
        "  add load_core_policy",
        "",
        "core_lite/receipts.py:",
        "  add append_receipt",
        "```",
        "",
        "## Outputs",
        "",
        "```text",
        f"candidate_ingest: {report['outputs']['candidate_ingest']}",
        f"candidate_receipts: {report['outputs']['candidate_receipts']}",
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
    receipts.record(
        "candidate_builder_started",
        "RECEIVED",
        "StegVerse-001 started CLI dependency contractual inclusion candidate builder.",
        {
            "targets": ["core_lite/ingest.py", "core_lite/receipts.py"],
            "required_exports": {
                "core_lite/ingest.py": sorted(INGEST_REQUIRED),
                "core_lite/receipts.py": sorted(RECEIPTS_REQUIRED),
            },
        },
    )

    repo_root, access = clone_target(receipts)
    if repo_root is None:
        failure = {
            "schema": "stegverse_001_cli_dependency_contract_candidate_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "decision": "FAIL_CLOSED",
            "basis": "Could not access core-lite target.",
            "target_access": access,
        }
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    ingest_path = repo_root / "core_lite" / "ingest.py"
    receipts_path = repo_root / "core_lite" / "receipts.py"
    if not ingest_path.exists() or not receipts_path.exists():
        missing = [p.as_posix() for p in [ingest_path, receipts_path] if not p.exists()]
        failure = {
            "schema": "stegverse_001_cli_dependency_contract_candidate_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "decision": "FAIL_CLOSED",
            "basis": "Required target files are missing.",
            "target_access": access,
            "missing_files": missing,
        }
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    ingest_original = ingest_path.read_text(encoding="utf-8")
    receipts_original = receipts_path.read_text(encoding="utf-8")

    ingest_original_exports = parse_exports(ingest_original)
    receipts_original_exports = parse_exports(receipts_original)

    missing_preserved = {
        "core_lite/ingest.py": sorted(INGEST_PRESERVE - ingest_original_exports),
        "core_lite/receipts.py": sorted(RECEIPTS_PRESERVE - receipts_original_exports),
    }
    missing_preserved = {key: value for key, value in missing_preserved.items() if value}

    if missing_preserved:
        ingest_candidate = ingest_original
        receipts_candidate = receipts_original
        decision = "FAIL_CLOSED"
        basis = "Existing surfaces required for preservation are missing."
    else:
        ingest_candidate = append_ingest_contract(ingest_original)
        receipts_candidate = append_receipts_contract(receipts_original)
        decision = "CANDIDATE_PREPARED"
        basis = "Prepared additive CLI dependency contractual inclusion candidate."

    CANDIDATE_INGEST.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_INGEST.write_text(ingest_candidate, encoding="utf-8")
    CANDIDATE_RECEIPTS.write_text(receipts_candidate, encoding="utf-8")

    diff_ingest = "".join(difflib.unified_diff(ingest_original.splitlines(keepends=True), ingest_candidate.splitlines(keepends=True), fromfile="core_lite/ingest.py", tofile="core_lite/ingest.py"))
    diff_receipts = "".join(difflib.unified_diff(receipts_original.splitlines(keepends=True), receipts_candidate.splitlines(keepends=True), fromfile="core_lite/receipts.py", tofile="core_lite/receipts.py"))
    combined_patch = diff_ingest + ("\n" if diff_ingest and diff_receipts else "") + diff_receipts
    PATCH_FILE.write_text(combined_patch, encoding="utf-8")

    ingest_candidate_exports = parse_exports(ingest_candidate)
    receipts_candidate_exports = parse_exports(receipts_candidate)

    manifest = {
        "schema": "stegverse_001_cli_dependency_contract_candidate_manifest.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "actor": "StegVerse-001",
        "transition": "CLI_DEPENDENCY_CONTRACTUAL_INCLUSION_CANDIDATE",
        "target_repo": access.get("repo", DEFAULT_REPO),
        "targets": {
            "core_lite/ingest.py": {
                "required_exports": sorted(INGEST_REQUIRED),
                "preserve_exports": sorted(INGEST_PRESERVE),
                "original_sha256": sha256_text(ingest_original),
                "candidate_sha256": sha256_text(ingest_candidate),
            },
            "core_lite/receipts.py": {
                "required_exports": sorted(RECEIPTS_REQUIRED),
                "preserve_exports": sorted(RECEIPTS_PRESERVE),
                "original_sha256": sha256_text(receipts_original),
                "candidate_sha256": sha256_text(receipts_candidate),
            },
        },
        "patch_sha256": sha256_text(combined_patch),
        "mutation_to_target_performed": False,
        "workflow_change_authority": False,
        "push_authority": False,
        "incoming_submission_authority": False,
        "stop_condition": "Candidate prepared. Report and receipt returned. STOP.",
    }
    CANDIDATE_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = {
        "schema": "stegverse_001_cli_dependency_contract_candidate_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": decision == "CANDIDATE_PREPARED",
        "actor": "StegVerse-001",
        "transition": "Core-Lite CLI Dependency Contractual Inclusion Candidate",
        "decision": decision,
        "basis": basis,
        "target_access": access,
        "targets": {
            "core_lite/ingest.py": {
                "required_exports": sorted(INGEST_REQUIRED),
                "original_exports": sorted(ingest_original_exports),
                "candidate_exports": sorted(ingest_candidate_exports),
                "added_exports_present": sorted(INGEST_REQUIRED & ingest_candidate_exports),
                "missing_required_exports": sorted(INGEST_REQUIRED - ingest_candidate_exports),
            },
            "core_lite/receipts.py": {
                "required_exports": sorted(RECEIPTS_REQUIRED),
                "original_exports": sorted(receipts_original_exports),
                "candidate_exports": sorted(receipts_candidate_exports),
                "added_exports_present": sorted(RECEIPTS_REQUIRED & receipts_candidate_exports),
                "missing_required_exports": sorted(RECEIPTS_REQUIRED - receipts_candidate_exports),
            },
        },
        "missing_preserved_exports": missing_preserved,
        "mutation_to_target_performed": False,
        "outputs": {
            "candidate_ingest": CANDIDATE_INGEST.as_posix(),
            "candidate_receipts": CANDIDATE_RECEIPTS.as_posix(),
            "patch_file": PATCH_FILE.as_posix(),
            "candidate_manifest": CANDIDATE_MANIFEST.as_posix(),
        },
        "boundary": [
            "formalism-tests is the command backdrop.",
            "core-lite is the remote target.",
            "This task prepares candidates only.",
            "This task does not patch, push, submit incoming bundles, or change workflows.",
            "STOP after report, candidates, patch, manifest, and receipt.",
        ],
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report)

    receipts.record(
        "candidate_prepared",
        decision,
        basis,
        {
            "report": REPORT_JSON.as_posix(),
            "candidate_manifest": CANDIDATE_MANIFEST.as_posix(),
            "patch": PATCH_FILE.as_posix(),
            "candidate_ingest": CANDIDATE_INGEST.as_posix(),
            "candidate_receipts": CANDIDATE_RECEIPTS.as_posix(),
            "targets": report["targets"],
        },
    )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
