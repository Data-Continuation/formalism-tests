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

# Required for the next decision step.
REQUIRED = [
    "reports/core_lite_discovery_gap_report.md",
    "reports/core_lite_state_diff.json",
    "reports/core_lite_install_plan_candidate.json",
]

# Useful context. Missing optional files should warn, not fail the routing task.
OPTIONAL = [
    "reports/core_lite_remote_discovery_report.json",
    "reports/core_lite_discovery_report.json",
    "reports/core_lite_discovered_state.json",
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
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def copy_one(source_text: str, required: bool) -> Dict[str, Any]:
    source = Path(source_text)
    target = OUT_DIR / source.name
    exists = source.exists() and source.is_file()

    entry: Dict[str, Any] = {
        "source": source_text,
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


def copy_artifacts() -> List[Dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: List[Dict[str, Any]] = []

    for source_text in REQUIRED:
        entries.append(copy_one(source_text, required=True))

    for source_text in OPTIONAL:
        entries.append(copy_one(source_text, required=False))

    return entries


def write_index(entries: List[Dict[str, Any]], missing_required: List[str], missing_optional: List[str]) -> None:
    lines = [
        "# Core-Lite Discovery Artifact Index",
        "",
        "## Purpose",
        "",
        "This folder collects the current core-lite discovery outputs in one place so the owner does not need to search through historical runtime artifact folders.",
        "",
        "## Routing Status",
        "",
        "```text",
        f"required_missing: {len(missing_required)}",
        f"optional_missing: {len(missing_optional)}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "Discovery observes.",
        "Discovery does not install.",
        "Install plans are candidates, not authority.",
        "Historical artifacts are for audit.",
        "dist/current/ is for action.",
        "```",
        "",
        "## Files",
        "",
        "| File | Required | Present | Source |",
        "|---|---:|---:|---|",
    ]

    for entry in entries:
        present = "yes" if entry["copied"] else "no"
        required = "yes" if entry["required"] else "no"
        lines.append(f"| `{Path(entry['target']).name}` | {required} | {present} | `{entry['source']}` |")

    lines.extend([
        "",
        "## Review These First",
        "",
        "```text",
        "core_lite_discovery_gap_report.md",
        "core_lite_state_diff.json",
        "core_lite_install_plan_candidate.json",
        "```",
    ])

    if missing_required:
        lines.extend(["", "## Missing Required Files", ""])
        for item in missing_required:
            lines.append(f"- `{item}`")

    if missing_optional:
        lines.extend(["", "## Missing Optional Files", ""])
        for item in missing_optional:
            lines.append(f"- `{item}`")

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

    entries = copy_artifacts()
    missing_required = [entry["source"] for entry in entries if entry["required"] and not entry["copied"]]
    missing_optional = [entry["source"] for entry in entries if not entry["required"] and not entry["copied"]]

    write_index(entries, missing_required, missing_optional)
    zip_hash = write_zip()

    success = len(missing_required) == 0

    report = {
        "schema": "stegverse_core_lite_discovery_artifact_routing_report.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "out_dir": OUT_DIR.as_posix(),
        "zip": ZIP_PATH.as_posix(),
        "zip_sha256": zip_hash,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
        "entries": entries,
        "note": "Required current review artifacts must exist. Optional context artifacts warn but do not fail routing."
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_core_lite_discovery_artifact_routing_receipt.v2",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_DISCOVERY_ARTIFACT_ROUTING" if success else "REQUIRE_DISCOVERY_ARTIFACT_REVIEW",
        "basis": "Core-lite discovery outputs were routed into a single current review folder and zip.",
        "success": success,
        "zip": ZIP_PATH.as_posix(),
        "zip_sha256": zip_hash,
        "missing_required_count": len(missing_required),
        "missing_optional_count": len(missing_optional)
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
