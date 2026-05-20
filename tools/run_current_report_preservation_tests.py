#!/usr/bin/env python3
"""Preserve current proof reports under stable reports/current paths.

This runner copies latest successful proof reports into reports/current and
validates that the current proof surface remains discoverable even when
runtime artifacts are later archived into legacy/runtime-artifacts.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POLICY_PATH = Path("tests/fixtures/current_report_preservation_policy.json")
REPORT_PATH = Path("reports/current_report_preservation_report.json")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"missing JSON file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data


def require(condition: bool, message: str) -> int:
    if not condition:
        raise AssertionError(message)
    return 1


def validate_source(entry: dict[str, Any]) -> int:
    checks = 0
    source = Path(entry["source"])
    current = Path(entry["current"])
    kind = entry.get("kind")

    checks += require(source.exists(), f"missing source report: {source}")
    current.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, current)
    checks += require(current.exists(), f"current report was not created: {current}")

    if kind == "json_report":
        data = load_json(current)
        for key, expected in entry.get("required_json", {}).items():
            checks += require(data.get(key) == expected, f"{current}: expected {key}={expected!r}, got {data.get(key)!r}")
    elif kind == "markdown_report":
        text = current.read_text(encoding="utf-8")
        for marker in entry.get("required_markers", []):
            checks += require(marker in text, f"{current}: missing marker {marker!r}")
    else:
        raise AssertionError(f"{source}: unsupported report kind {kind!r}")

    return checks


def main() -> int:
    try:
        policy = load_json(POLICY_PATH)
        checks = 0
        preserved = []

        for entry in policy.get("required_sources", []):
            checks += validate_source(entry)
            preserved.append(entry["current"])

        for duplicate in policy.get("noncanonical_duplicates", []):
            checks += require(duplicate not in preserved, f"noncanonical duplicate preserved as current: {duplicate}")

        for canonical in policy.get("canonical_receipts", []):
            checks += require(not canonical.endswith(" 2.jsonl"), f"canonical receipt cannot be duplicate: {canonical}")

        checks += require(policy.get("authority_boundary", "").startswith("formalism-tests produces receipts"), "authority boundary missing")

        report = {
            "schema": "stegverse_current_report_preservation_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assertion_count": checks,
            "preserved_count": len(preserved),
            "current_dir": policy.get("current_dir"),
            "preserved_reports": preserved,
            "noncanonical_duplicates": policy.get("noncanonical_duplicates", []),
            "canonical_receipts": policy.get("canonical_receipts", []),
            "message": "Current proof reports preserved under stable reports/current paths."
        }

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_current_report_preservation_report.v1",
            "success": False,
            "error": str(exc)
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
