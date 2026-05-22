#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPORTS = Path("reports")
RECEIPTS = Path("receipts")
DIST_CURRENT = Path("dist/current/core-lite-discovery")
DIST_ZIP = Path("dist/current/core-lite-discovery-artifacts.zip")

REMOTE_SCRIPT = Path("tools/discover_core_lite_remote_state.py")

CURRENT_INDEX = REPORTS / "current_core_lite_discovery_artifact_index.md"
CURRENT_GAP = REPORTS / "current_core_lite_discovery_gap_report.md"
CURRENT_DIFF = REPORTS / "current_core_lite_state_diff.json"
CURRENT_PLAN = REPORTS / "current_core_lite_install_plan_candidate.json"
CURRENT_MANIFEST = REPORTS / "current_core_lite_discovery_packet_manifest.json"
CURRENT_RECEIPTS = RECEIPTS / "current_core_lite_discovery_receipts.jsonl"
CURRENT_REPORT = REPORTS / "current_core_lite_discovery_packet_report.json"

SOURCE_REQUIRED = {
    "reports/core_lite_discovery_gap_report.md": CURRENT_GAP,
    "reports/core_lite_state_diff.json": CURRENT_DIFF,
    "reports/core_lite_install_plan_candidate.json": CURRENT_PLAN,
}

SOURCE_OPTIONAL = {
    "reports/core_lite_remote_discovery_report.json": REPORTS / "current_core_lite_remote_discovery_report.json",
    "reports/core_lite_discovery_report.json": REPORTS / "current_core_lite_discovery_report.json",
    "reports/core_lite_discovered_state.json": REPORTS / "current_core_lite_discovered_state.json",
    "receipts/core_lite_remote_discovery_receipts.jsonl": RECEIPTS / "current_core_lite_remote_discovery_receipts.jsonl",
    "receipts/core_lite_discovery_receipts.jsonl": RECEIPTS / "current_core_lite_discovery_base_receipts.jsonl",
}


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def digest(obj: dict) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def copy_file(source: Path, target: Path, required: bool) -> dict:
    exists = source.exists() and source.is_file()
    entry = {
        "source": source.as_posix(),
        "target": target.as_posix(),
        "required": required,
        "exists": exists,
        "copied": False,
        "sha256": None,
    }
    if exists:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        entry["copied"] = True
        entry["sha256"] = sha256_file(target)
    return entry


def write_current_index(entries: list[dict], missing_required: list[str], missing_optional: list[str]) -> None:
    lines = [
        "# Current Core-Lite Discovery Artifact Index",
        "",
        "## Purpose",
        "",
        "This is the current action surface for core-lite discovery.",
        "",
        "It exists under `reports/` so the stable dispatcher can persist it without requiring workflow changes.",
        "",
        "## Boundary",
        "",
        "```text",
        "Discovery observes.",
        "Discovery does not install.",
        "Reports/current_* is for action.",
        "dist/current/ is optional packet/cache surface.",
        "Historical runtime artifacts are for audit.",
        "```",
        "",
        "## Status",
        "",
        "```text",
        f"missing_required: {len(missing_required)}",
        f"missing_optional: {len(missing_optional)}",
        "```",
        "",
        "## Review These First",
        "",
        "```text",
        "reports/current_core_lite_discovery_gap_report.md",
        "reports/current_core_lite_state_diff.json",
        "reports/current_core_lite_install_plan_candidate.json",
        "reports/current_core_lite_discovery_packet_manifest.json",
        "```",
        "",
        "## Files",
        "",
        "| File | Required | Present | Source |",
        "|---|---:|---:|---|",
    ]
    for entry in entries:
        name = Path(entry["target"]).name
        required = "yes" if entry["required"] else "no"
        present = "yes" if entry["copied"] else "no"
        lines.append(f"| `{name}` | {required} | {present} | `{entry['source']}` |")

    if missing_required:
        lines.extend(["", "## Missing Required", ""])
        for item in missing_required:
            lines.append(f"- `{item}`")

    if missing_optional:
        lines.extend(["", "## Missing Optional", ""])
        for item in missing_optional:
            lines.append(f"- `{item}`")

    CURRENT_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_dist_packet(entries: list[dict]) -> str | None:
    DIST_CURRENT.mkdir(parents=True, exist_ok=True)

    # Copy the current action files into dist/current as a convenience packet.
    packet_files = [
        CURRENT_INDEX,
        CURRENT_GAP,
        CURRENT_DIFF,
        CURRENT_PLAN,
        CURRENT_MANIFEST,
        CURRENT_REPORT,
        CURRENT_RECEIPTS,
    ]

    for path in packet_files:
        if path.exists() and path.is_file():
            shutil.copy2(path, DIST_CURRENT / path.name)

    DIST_ZIP.parent.mkdir(parents=True, exist_ok=True)
    if DIST_ZIP.exists():
        DIST_ZIP.unlink()

    with zipfile.ZipFile(DIST_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(DIST_CURRENT.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(DIST_CURRENT.parent).as_posix())

    return sha256_file(DIST_ZIP)


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)

    if not REMOTE_SCRIPT.exists():
        report = {
            "schema": "stegverse_current_core_lite_discovery_packet_report.v4",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "error": "missing_remote_discovery_script",
            "missing": str(REMOTE_SCRIPT),
        }
        CURRENT_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    started_at = datetime.now(timezone.utc).isoformat()
    discovery = subprocess.run([sys.executable, str(REMOTE_SCRIPT)], text=True, capture_output=True)

    entries = []

    if discovery.returncode == 0:
        for source_text, target in SOURCE_REQUIRED.items():
            entries.append(copy_file(Path(source_text), target, required=True))
        for source_text, target in SOURCE_OPTIONAL.items():
            entries.append(copy_file(Path(source_text), target, required=False))

    missing_required = [e["source"] for e in entries if e["required"] and not e["copied"]]
    missing_optional = [e["source"] for e in entries if not e["required"] and not e["copied"]]

    success = discovery.returncode == 0 and not missing_required

    manifest = {
        "schema": "stegverse_current_core_lite_discovery_packet_manifest.v4",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "repo": os.environ.get("CORE_LITE_REPO", "Data-Continuation/core-lite"),
        "branch": os.environ.get("CORE_LITE_BRANCH", "main"),
        "action_surface": "reports/current_*",
        "optional_packet_surface": "dist/current/core-lite-discovery/",
        "required_files": [
            CURRENT_GAP.as_posix(),
            CURRENT_DIFF.as_posix(),
            CURRENT_PLAN.as_posix(),
        ],
        "missing_required": missing_required,
        "missing_optional": missing_optional,
        "entries": entries,
        "boundary": [
            "Discovery observes.",
            "Discovery does not install.",
            "reports/current_* is for action.",
            "dist/current/ is optional packet/cache surface.",
            "Historical runtime artifacts are for audit."
        ]
    }
    CURRENT_MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    write_current_index(entries, missing_required, missing_optional)
    zip_hash = write_dist_packet(entries)

    report = {
        "schema": "stegverse_current_core_lite_discovery_packet_report.v4",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "started_at": started_at,
        "success": success,
        "repo": manifest["repo"],
        "branch": manifest["branch"],
        "discovery_returncode": discovery.returncode,
        "discovery_stdout_tail": discovery.stdout[-4000:],
        "discovery_stderr_tail": discovery.stderr[-4000:],
        "current_action_files": {
            "index": CURRENT_INDEX.as_posix(),
            "gap_report": CURRENT_GAP.as_posix(),
            "state_diff": CURRENT_DIFF.as_posix(),
            "install_plan": CURRENT_PLAN.as_posix(),
            "manifest": CURRENT_MANIFEST.as_posix(),
        },
        "dist_packet": DIST_CURRENT.as_posix(),
        "dist_zip": DIST_ZIP.as_posix(),
        "dist_zip_sha256": zip_hash,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
    }
    CURRENT_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_current_core_lite_discovery_receipt.v4",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_CURRENT_DISCOVERY_ACTION_SURFACE" if success else "FAIL_CLOSED_CURRENT_DISCOVERY_ACTION_SURFACE",
        "basis": "Core-lite discovery outputs were routed to reports/current_* for dispatcher-compatible action review.",
        "success": success,
        "install_authority": False,
        "production_authority": False,
        "current_manifest": CURRENT_MANIFEST.as_posix(),
        "current_report": CURRENT_REPORT.as_posix(),
        "dist_zip_sha256": zip_hash,
    }
    receipt["receipt_hash"] = digest(receipt)
    CURRENT_RECEIPTS.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
