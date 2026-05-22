#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPORTS = Path("reports")
RECEIPTS = Path("receipts")
DIST_CURRENT = Path("dist/current/core-lite-discovery")
ZIP_PATH = Path("dist/current/core-lite-discovery-artifacts.zip")
REPORT_PATH = REPORTS / "core_lite_discovery_current_packet_report.json"
RECEIPT_PATH = RECEIPTS / "core_lite_discovery_current_packet_receipts.jsonl"

REMOTE_SCRIPT = Path("tools/discover_core_lite_remote_state.py")
ROUTE_SCRIPT = Path("tools/route_core_lite_discovery_artifacts.py")

REQUIRED_FINAL = [
    "dist/current/core-lite-discovery/CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md",
    "dist/current/core-lite-discovery/core_lite_discovery_gap_report.md",
    "dist/current/core-lite-discovery/core_lite_state_diff.json",
    "dist/current/core-lite-discovery/core_lite_install_plan_candidate.json",
    "dist/current/core-lite-discovery-artifacts.zip",
]


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def digest(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def run_python(script: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script)], text=True, capture_output=True)


def fail_report(reason: str, missing: list[str]) -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "stegverse_core_lite_discovery_current_packet_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "error": reason,
        "missing": missing
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    DIST_CURRENT.mkdir(parents=True, exist_ok=True)

    missing_scripts = [str(p) for p in [REMOTE_SCRIPT, ROUTE_SCRIPT] if not p.exists()]
    if missing_scripts:
        return fail_report("missing_required_scripts", missing_scripts)

    started_at = datetime.now(timezone.utc).isoformat()
    discovery = run_python(REMOTE_SCRIPT)

    route = None
    if discovery.returncode == 0:
        route = run_python(ROUTE_SCRIPT)

    final_outputs = {path: Path(path).exists() for path in REQUIRED_FINAL}
    missing_final = [path for path, exists in final_outputs.items() if not exists]
    success = discovery.returncode == 0 and route is not None and route.returncode == 0 and not missing_final

    report = {
        "schema": "stegverse_core_lite_discovery_current_packet_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "started_at": started_at,
        "success": success,
        "repo": os.environ.get("CORE_LITE_REPO", "Data-Continuation/core-lite"),
        "branch": os.environ.get("CORE_LITE_BRANCH", "main"),
        "steps": {
            "remote_discovery": {
                "script": str(REMOTE_SCRIPT),
                "returncode": discovery.returncode,
                "stdout_tail": discovery.stdout[-4000:],
                "stderr_tail": discovery.stderr[-4000:]
            },
            "artifact_routing": {
                "script": str(ROUTE_SCRIPT),
                "returncode": None if route is None else route.returncode,
                "stdout_tail": "" if route is None else route.stdout[-4000:],
                "stderr_tail": "" if route is None else route.stderr[-4000:]
            }
        },
        "required_final_outputs": final_outputs,
        "missing_final_outputs": missing_final,
        "current_review_dir": str(DIST_CURRENT),
        "current_review_zip": str(ZIP_PATH),
        "current_review_zip_sha256": sha256_file(ZIP_PATH),
        "boundary": [
            "Discovery observes.",
            "Discovery does not install.",
            "Artifact routing collects current evidence.",
            "dist/current/ is for action.",
            "Historical artifacts are for audit."
        ]
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_core_lite_discovery_current_packet_receipt.v1",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_CURRENT_DISCOVERY_PACKET" if success else "FAIL_CLOSED_CURRENT_DISCOVERY_PACKET",
        "basis": "Core-lite discovery and current artifact routing were run in the same workflow checkout.",
        "success": success,
        "current_review_dir": str(DIST_CURRENT),
        "current_review_zip": str(ZIP_PATH),
        "current_review_zip_sha256": report["current_review_zip_sha256"],
        "install_authority": False,
        "production_authority": False
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
