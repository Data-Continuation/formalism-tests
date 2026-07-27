#!/usr/bin/env python3
"""Evaluate optimization-target commit-boundary fixtures deterministically."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/fixtures/optimization_target_commit_boundary_cases.json"
EXPECTED = ROOT / "tests/fixtures/optimization_target_commit_boundary_expected_outcomes.json"
REPORT = ROOT / "reports/optimization_target_commit_boundary_report.json"
RECEIPTS = ROOT / "receipts/optimization_target_commit_boundary_execution_receipts.jsonl"
AUTHORITY = "FORMALISM_TEST_EVIDENCE_ONLY"


def evaluate(inputs: dict) -> str:
    if not inputs.get("target_declared", False):
        return "FAIL_CLOSED"
    if not inputs.get("target_current", False):
        return "FAIL_CLOSED"
    if not inputs.get("mutation_authorized", False):
        return "FAIL_CLOSED"
    if not inputs.get("policy_consistent", False):
        return "FAIL_CLOSED"
    if not inputs.get("deny_reachable", False):
        return "FAIL_CLOSED"
    return "ALLOW"


def main() -> int:
    suite = json.loads(CASES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))["expected"]
    results = []
    receipts = []

    for case in suite["cases"]:
        observed = evaluate(case["inputs"])
        wanted = expected[case["case_id"]]
        passed = observed == wanted == case["expected_result"]
        results.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "observed_result": observed,
            "expected_result": wanted,
            "pass": passed,
        })
        receipts.append({
            "schema": "stegverse.optimization-target.commit-boundary.receipt.v1",
            "suite_id": suite["suite_id"],
            "case_id": case["case_id"],
            "commit_time_result": observed,
            "authority_posture": AUTHORITY,
            "pass": passed,
        })

    passed_count = sum(1 for item in results if item["pass"])
    report = {
        "schema": "stegverse.optimization-target.commit-boundary.report.v1",
        "suite_id": suite["suite_id"],
        "status": "PASS" if passed_count == len(results) else "FAIL",
        "case_count": len(results),
        "passed_count": passed_count,
        "failed_count": len(results) - passed_count,
        "authority_posture": AUTHORITY,
        "results": results,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    RECEIPTS.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in receipts), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
