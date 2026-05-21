#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


POLICY_PATH = Path("tests/fixtures/stage9_reconciliation_policy.json")
REPORT_PATH = Path("reports/stage9_reconciliation_report.json")
TASK_MANIFEST_PATH = Path("tools/tasks/formalism_tests_tasks.json")


def load_json(path: Path):
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


def resolve_report(entry, policy):
    live = Path(entry["path"])
    if live.exists():
        return live

    fixture_dir = Path(policy.get("fixture_report_dir", "tests/fixtures/stage9_reconciliation_reports"))
    fixture = fixture_dir / entry["fixture"]
    if fixture.exists():
        return fixture

    raise AssertionError(f"missing report: {live}")


def validate_markdown(policy):
    checks = 0

    for item in policy.get("required_markdown", []):
        path = Path(item["path"])
        checks += require(path.exists(), f"missing markdown file: {path}")

        text = path.read_text(encoding="utf-8")

        for marker in item.get("markers", []):
            checks += require(marker in text, f"{path}: missing marker {marker}")

        for group in item.get("marker_groups", []):
            missing = [marker for marker in group if marker not in text]
            checks += require(not missing, f"{path}: missing marker group terms {missing}")

        checks += require("Partially covered theorem group" not in text, f"{path}: stale partial theorem group present")
        checks += require("Representation Non-Consequence remains partially covered" not in text, f"{path}: stale Representation language present")

    return checks


def validate_reports(policy):
    checks = 0
    sources = []

    for entry in policy.get("required_reports", []):
        path = resolve_report(entry, policy)
        data = load_json(path)
        sources.append(str(path))

        for key, expected in entry.get("required", {}).items():
            checks += require(data.get(key) == expected, f"{path}: expected {key}={expected!r}, got {data.get(key)!r}")

    return checks, sources


def validate_tasks(policy):
    checks = 0
    manifest = load_json(TASK_MANIFEST_PATH)
    task_ids = {task.get("task_id") for task in manifest.get("tasks", [])}

    for task_id in policy.get("required_tasks", []):
        checks += require(task_id in task_ids, f"declared task missing: {task_id}")

    return checks


def validate_policy_files():
    checks = 0

    current_policy_path = Path("tests/fixtures/current_report_preservation_policy.json")
    if current_policy_path.exists():
        current_policy = json.dumps(load_json(current_policy_path))
        for marker in ["stage8_ai_domain_report.json", "stage9_multi_body_coupling_report.json", "element_dependency_closure_report.json"]:
            checks += require(marker in current_policy, f"current preservation policy missing {marker}")

    theorem_policy_path = Path("tests/fixtures/theorem_map_consistency_policy.json")
    if theorem_policy_path.exists():
        theorem_policy = json.dumps(load_json(theorem_policy_path))
        for marker in ["Stage 7", "Stage 8", "Stage 9"]:
            checks += require(marker in theorem_policy, f"theorem consistency policy missing {marker}")

    return checks


def main() -> int:
    try:
        policy = load_json(POLICY_PATH)

        checks = 0
        checks += validate_markdown(policy)

        report_checks, report_sources = validate_reports(policy)
        checks += report_checks

        checks += validate_tasks(policy)
        checks += validate_policy_files()
        checks += require(policy.get("authority_boundary", "").startswith("formalism-tests produces receipts"), "authority boundary missing")

        report = {
            "schema": "stegverse_stage9_reconciliation_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assertion_count": checks,
            "report_sources": report_sources,
            "reconciled_stages": ["Stage 7", "Stage 8", "Stage 9"],
            "next_stage": "Stage 10 - Canonical Transition Table Release",
            "message": "Stage 9 reconciliation validation passed."
        }

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage9_reconciliation_report.v1",
            "success": False,
            "error": str(exc)
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
