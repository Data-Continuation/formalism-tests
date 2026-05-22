#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REPORTS = Path("reports")
RECEIPTS = Path("receipts")
WORK = Path(".tmp/core-lite-discovery")
REMOTE_REPORT = REPORTS / "core_lite_remote_discovery_report.json"
RECEIPT = RECEIPTS / "core_lite_remote_discovery_receipts.jsonl"


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    repo = os.environ.get("CORE_LITE_REPO", "Data-Continuation/core-lite")
    branch = os.environ.get("CORE_LITE_BRANCH", "main")
    token = os.environ.get("CORE_LITE_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    clone_dir = WORK / "repo"

    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True, exist_ok=True)

    if repo.startswith("http://") or repo.startswith("https://"):
        url = repo
        safe_repo_name = repo.rsplit("/", 1)[-1].replace(".git", "")
    else:
        safe_repo_name = repo
        if token:
            url = f"https://x-access-token:{token}@github.com/{repo}.git"
        else:
            url = f"https://github.com/{repo}.git"

    clone = run(["git", "clone", "--depth", "1", "--branch", branch, url, str(clone_dir)])
    if clone.returncode != 0:
        report = {
            "schema": "stegverse_core_lite_remote_discovery_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "repo": safe_repo_name,
            "branch": branch,
            "error": "clone_failed",
            "stderr": clone.stderr[-4000:],
            "stdout": clone.stdout[-4000:]
        }
        REMOTE_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    discovery_script = Path("tools/discover_core_lite_state.py")
    if not discovery_script.exists():
        report = {
            "schema": "stegverse_core_lite_remote_discovery_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "repo": safe_repo_name,
            "branch": branch,
            "error": "missing_discovery_script",
            "required": "tools/discover_core_lite_state.py"
        }
        REMOTE_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    env = dict(os.environ)
    env["CORE_LITE_ROOT"] = str(clone_dir.resolve())

    proc = subprocess.run(
        [sys.executable, str(discovery_script)],
        text=True,
        capture_output=True,
        env=env
    )

    success = proc.returncode == 0
    report = {
        "schema": "stegverse_core_lite_remote_discovery_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "repo": safe_repo_name,
        "branch": branch,
        "clone_dir": str(clone_dir),
        "discovery_script": str(discovery_script),
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "expected_outputs": [
            "reports/core_lite_discovery_report.json",
            "reports/core_lite_discovered_state.json",
            "reports/core_lite_discovery_gap_report.md",
            "reports/core_lite_state_diff.json",
            "reports/core_lite_install_plan_candidate.json",
            "receipts/core_lite_discovery_receipts.jsonl"
        ]
    }
    REMOTE_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_core_lite_remote_discovery_receipt.v1",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_REMOTE_DISCOVERY_REPORT" if success else "FAIL_CLOSED_REMOTE_DISCOVERY",
        "basis": "Remote core-lite repository was cloned into temporary workspace and discovery was run without installation.",
        "repo": safe_repo_name,
        "branch": branch,
        "success": success,
        "install_authority": False,
        "production_authority": False,
        "report": str(REMOTE_REPORT)
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
