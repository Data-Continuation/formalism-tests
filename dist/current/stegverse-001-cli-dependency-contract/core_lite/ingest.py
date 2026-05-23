from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_ingestion(bundle: Path, repo_root: Path | str = ".") -> dict[str, Any]:
    return {"success": True, "bundle": str(bundle)}


def write_markdown_report(report: dict[str, Any]) -> None:
    return None

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
        (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
        (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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
    (root / "core_lite_ingest_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report
