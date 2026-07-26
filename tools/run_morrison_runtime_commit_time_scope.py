#!/usr/bin/env python3
"""Evaluate Morrison Runtime commit-time scope fixtures deterministically."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_cases.json"
EXPECTED = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json"
REPORT = ROOT / "reports/morrison_runtime_commit_time_scope_report.json"


def evaluate(inputs: dict) -> str:
    if not inputs.get("authority_current", False):
        return "DENY"
    if not inputs.get("required_evidence_complete", False):
        return "FAIL_CLOSED"
    if not inputs.get("coverage_known", False):
        return "FAIL_CLOSED"
    if not inputs.get("freshness_valid", False):
        return "FAIL_CLOSED"
    if inputs.get("unmodeled_material_parameter_present", False):
        return "FAIL_CLOSED"
    if inputs.get("contradictory_evidence_present", False):
        return "DENY"
    if not inputs.get("policy_allows", False):
        return "DENY"
    return "ALLOW"


def main() -> int:
    fixtures = json.loads(FIXTURES.read_text())
    expected = json.loads(EXPECTED.read_text())["expected"]
    results = []
    passed = 0

    for case in fixtures["cases"]:
        observed = evaluate(case["commit_time_inputs"])
        wanted = expected[case["case_id"]]
        ok = observed == wanted == case["expected_stegverse_result"]
        passed += int(ok)
        results.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "initial_runtime_result": case["initial_runtime_result"],
            "observed_stegverse_result": observed,
            "expected_stegverse_result": wanted,
            "pass": ok,
        })

    report = {
        "schema": "stegverse.morrison-runtime.commit-time-scope.report.v1",
        "suite_id": expected and "morrison-runtime-commit-time-scope-v0.1",
        "status": "PASS" if passed == len(results) else "FAIL",
        "case_count": len(results),
        "passed_count": passed,
        "failed_count": len(results) - passed,
        "authority_posture": "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY",
        "results": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
