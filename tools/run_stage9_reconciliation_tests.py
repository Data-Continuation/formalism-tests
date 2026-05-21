#!/usr/bin/env python3
import json, sys
from datetime import datetime, timezone
from pathlib import Path

POLICY = Path("tests/fixtures/stage9_reconciliation_policy.json")
REPORT = Path("reports/stage9_reconciliation_report.json")
TASKS = Path("tools/tasks/formalism_tests_tasks.json")

def load(path):
    if not path.exists():
        raise AssertionError(f"missing JSON file: {path}")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def resolve(entry, policy):
    live = Path(entry["path"])
    if live.exists():
        return live
    fixture = Path(policy["fixture_report_dir"]) / entry["fixture"]
    if fixture.exists():
        return fixture
    raise AssertionError(f"missing report: {live}")

def main():
    try:
        policy = load(POLICY)
        checks = 0
        sources = []
        for item in policy["required_markdown"]:
            path = Path(item["path"])
            checks += req(path.exists(), f"missing markdown file: {path}")
            text = path.read_text()
            for group in item["marker_groups"]:
                missing = [m for m in group if m not in text]
                checks += req(not missing, f"{path}: missing marker group terms {missing}")
            checks += req("Partially covered theorem group" not in text, f"{path}: stale partial theorem group present")
            checks += req("Representation Non-Consequence remains partially covered" not in text, f"{path}: stale Representation language present")
        for entry in policy["required_reports"]:
            path = resolve(entry, policy)
            data = load(path)
            sources.append(str(path))
            for key, expected in entry["required"].items():
                checks += req(data.get(key) == expected, f"{path}: expected {key}={expected!r}, got {data.get(key)!r}")
        ids = {t.get("task_id") for t in load(TASKS).get("tasks", [])}
        for task in policy["required_tasks"]:
            checks += req(task in ids, f"declared task missing: {task}")
        report = {
            "schema": "stegverse_stage9_reconciliation_report.v2",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assertion_count": checks,
            "report_sources": sources,
            "reconciled_stages": ["Stage 7", "Stage 8", "Stage 9", "Stage 10"],
            "next_stage": "Stage 10 - Canonical Transition Table Release",
            "message": "Stage 9 and Stage 10 documentation reconciliation validation passed."
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as e:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {"schema": "stegverse_stage9_reconciliation_report.v2", "success": False, "error": str(e)}
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
