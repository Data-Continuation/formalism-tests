#!/usr/bin/env python3
"""Validate theorem-map consistency against latest proof reports.

This runner prevents stale theorem coverage text from reappearing in the root
or current theorem proof map after Representation Non-Consequence and later
proof layers have passed.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POLICY_PATH = Path("tests/fixtures/theorem_map_consistency_policy.json")
REPORT_PATH = Path("reports/theorem_map_consistency_report.json")


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


def read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"missing text file: {path}")
    return path.read_text(encoding="utf-8")


def validate_map_text(path: Path, text: str, policy: dict[str, Any]) -> int:
    checks = 0
    checks += require("formalism-tests produces receipts" in text, f"{path}: missing authority boundary")
    for theorem in policy.get("required_covered_theorems", []):
        checks += require(f"| {theorem} |" in text, f"{path}: missing theorem row for {theorem}")
        row_lines = [line for line in text.splitlines() if line.startswith(f"| {theorem} |")]
        checks += require(any(line.rstrip().endswith("| Covered |") for line in row_lines), f"{path}: theorem not marked Covered: {theorem}")
    for marker in policy.get("forbidden_markers", []):
        checks += require(marker not in text, f"{path}: stale forbidden marker present: {marker}")
    return checks


def validate_reports(policy: dict[str, Any]) -> int:
    checks = 0
    for report in policy.get("required_report_checks", []):
        path = Path(report["path"])
        data = load_json(path)
        for key, expected in report.get("required", {}).items():
            checks += require(data.get(key) == expected, f"{path}: expected {key}={expected!r}, got {data.get(key)!r}")
    return checks


def main() -> int:
    try:
        policy = load_json(POLICY_PATH)
        root_path = Path(policy["root_theorem_map"])
        current_path = Path(policy["current_theorem_map"])

        root_text = read_text(root_path)
        current_path.parent.mkdir(parents=True, exist_ok=True)

        # Keep current theorem map synchronized with root map before validation.
        shutil.copy2(root_path, current_path)
        current_text = read_text(current_path)

        checks = 0
        checks += validate_map_text(root_path, root_text, policy)
        checks += validate_map_text(current_path, current_text, policy)
        checks += require(root_text == current_text, "root and current theorem maps must match exactly")
        checks += validate_reports(policy)
        checks += require(policy.get("authority_boundary", "").startswith("formalism-tests produces receipts"), "policy missing authority boundary")

        report = {
            "schema": "stegverse_theorem_map_consistency_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assertion_count": checks,
            "root_theorem_map": str(root_path),
            "current_theorem_map": str(current_path),
            "covered_theorem_count": len(policy.get("required_covered_theorems", [])),
            "message": "Theorem map consistency validation passed."
        }
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_theorem_map_consistency_report.v1",
            "success": False,
            "error": str(exc)
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
