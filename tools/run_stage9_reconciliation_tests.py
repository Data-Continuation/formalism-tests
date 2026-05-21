#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path

POLICY_PATH = Path("tests/fixtures/stage9_reconciliation_policy.json")
REPORT_PATH = Path("reports/stage9_reconciliation_report.json")
TASK_MANIFEST_PATH = Path("tools/tasks/formalism_tests_tasks.json")

def load_json(path: Path):
    if not path.exists():
        raise AssertionError(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def require(condition: bool, message: str) -> int:
    if not condition:
        raise AssertionError(message)
    return 1

def resolve_report(entry, policy):
    live = Path(entry["path"])
    if live.exists():
        return live
    fixture = Path(policy.get("fixture_report_dir", "tests/fixtures/stage9_reconciliation_reports")) / entry["fixture"]
    if fixture.exists():
        return fixture
    raise AssertionError(f"missing report: {live}")

def main() -> int:
    try:
        policy = load_json(POLICY_PATH)
        checks = 0
        sources = []
        for item in policy["required_markdown"]:
            path = Path(item["path"])
            checks += require(path.exists(), f"missing markdown file: {path}")
            text = path.read_text(encoding="utf-8")
            for marker in item["markers"]:
                checks += require(marker in text, f"{path}: missing marker {marker}")
            checks += require("Partially covered theorem group" not in text, f"{path}: stale partial theorem group present")
        for entry in policy["required_reports"]:
            path = resolve_report(entry, policy)
            data = load_json(path)
            sources.append(str(path))
            for key, expected in entry["required"].items():
                checks += require(data.get(key) == expected, f"{path}: expected {key}={expected!r}")
        tasks = {t.get("task_id") for t in load_json(TASK_MANIFEST_PATH).get("tasks", [])}
        for task_id in policy["required_tasks"]:
            checks += require(task_id in tasks, f"declared task missing: {task_id}")
        current_policy = json.dumps(load_json(Path("tests/fixtures/current_report_preservation_policy.json")))
        for marker in ["element_dependency_closure_report.json", "stage8_ai_domain_report.json", "stage9_multi_body_coupling_report.json"]:
            checks += require(marker in current_policy, f"current preservation policy missing {marker}")
        theorem_policy = json.dumps(load_json(Path("tests/fixtures/theorem_map_consistency_policy.json")))
        for marker in ["Stage 7 Element Dependency Closure", "Stage 8 AI Domain Transition Classes", "Stage 9 Multi-Body Coupling Closure"]:
            checks += require(marker in theorem_policy, f"theorem consistency policy missing {marker}")
        report = {
            "schema": "stegverse_stage9_reconciliation_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assertion_count": checks,
            "report_sources": sources,
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
        report = {"schema": "stegverse_stage9_reconciliation_report.v1", "success": False, "error": str(exc)}
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
