#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


OUT_DIR = Path("dist/current/core-lite-discovery")
REPORT_PATH = Path("reports/core_lite_discovery_artifact_routing_report.json")
RECEIPT_PATH = Path("receipts/core_lite_discovery_artifact_routing_receipts.jsonl")
INDEX_PATH = OUT_DIR / "CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md"
ZIP_PATH = Path("dist/current/core-lite-discovery-artifacts.zip")

EXPECTED = [
    "reports/core_lite_remote_discovery_report.json",
    "reports/core_lite_discovery_report.json",
    "reports/core_lite_discovered_state.json",
    "reports/core_lite_discovery_gap_report.md",
    "reports/core_lite_state_diff.json",
    "reports/core_lite_install_plan_candidate.json",
    "receipts/core_lite_remote_discovery_receipts.jsonl",
    "receipts/core_lite_discovery_receipts.jsonl",
    "receipts/core_lite_remote_discovery_bundle_receipts.jsonl",
]


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def copy_expected() -> List[Dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: List[Dict[str, Any]] = []

    for source_text in EXPECTED:
        source = Path(source_text)
        target = OUT_DIR / source.name
        exists = source.exists() and source.is_file()

        entry: Dict[str, Any] = {
            "source": source_text,
            "target": target.as_posix(),
            "exists": exists,
            "copied": False,
            "sha256": None,
        }

        if exists:
            shutil.copy2(source, target)
            entry["copied"] = True
            entry["sha256"] = sha256_file(target)

        entries.append(entry)

    return entries


def write_index(entries: List[Dict[str, Any]]) -> None:
    lines = [
        "# Core-Lite Discovery Artifact Index",
        "",
        "## Purpose",
        "",
        "This folder collects the current core-lite discovery outputs in one place so the owner does not need to search through historical runtime artifact folders.",
        "",
        "## Boundary",
        "",
        "```text",
        "Discovery observes.",
        "Discovery does not install.",
        "Install plans are candidates, not authority.",
        "```",
        "",
        "## Files",
        "",
        "| File | Present | Source |",
        "|---|---:|---|",
    ]

    for entry in entries:
        present = "yes" if entry["copied"] else "no"
        lines.append(f"| `{Path(entry['target']).name}` | {present} | `{entry['source']}` |")

    lines.extend([
        "",
        "## Next Review Files",
        "",
        "Read these first:",
        "",
        "```text",
        "core_lite_discovery_gap_report.md",
        "core_lite_state_diff.json",
        "core_lite_install_plan_candidate.json",
        "```",
    ])

    INDEX_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_zip() -> str:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT_DIR.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(OUT_DIR.parent).as_posix())

    return sha256_file(ZIP_PATH) or ""


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

    entries = copy_expected()
    write_index(entries)
    zip_hash = write_zip()

    missing = [entry["source"] for entry in entries if not entry["copied"]]

    report = {
        "schema": "stegverse_core_lite_discovery_artifact_routing_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": len(missing) == 0,
        "out_dir": OUT_DIR.as_posix(),
        "zip": ZIP_PATH.as_posix(),
        "zip_sha256": zip_hash,
        "missing": missing,
        "entries": entries,
        "note": "This task collects current discovery outputs into one folder and zip for review."
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_core_lite_discovery_artifact_routing_receipt.v1",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_DISCOVERY_ARTIFACT_ROUTING" if len(missing) == 0 else "REQUIRE_DISCOVERY_ARTIFACT_REVIEW",
        "basis": "Core-lite discovery outputs were routed into a single current review folder and zip.",
        "success": report["success"],
        "zip": ZIP_PATH.as_posix(),
        "zip_sha256": zip_hash,
        "missing_count": len(missing)
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
