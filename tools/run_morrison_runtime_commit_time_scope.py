#!/usr/bin/env python3
"""Evaluate Morrison Runtime commit-time scope fixtures deterministically."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_cases.json"
EXPECTED = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json"
REPORT = ROOT / "reports/morrison_runtime_commit_time_scope_report.json"
RECEIPTS = ROOT / "receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl"
SUITE_ID = "morrison-runtime-commit-time-scope-v0.1"
AUTHORITY_POSTURE = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"


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


def displacement(initial: str, observed: str, inputs: dict) -> str:
    if initial == "ALLOW" and observed == "DENY":
        return "ALLOW_TO_DENY"
    if initial == "BLOCK" and observed == "ALLOW":
        return "BLOCK_TO_ALLOW"
    if initial == "ALLOW" and observed == "FAIL_CLOSED":
        return "ALLOW_TO_FAIL_CLOSED"
    if initial == "ALLOW" and observed == "ALLOW" and inputs.get("all_material_parameters_reconstructed", False):
        return "ALLOW_PRESERVED_AFTER_FULL_RECONSTRUCTION"
    return f"{initial}_TO_{observed}"


def main() -> int:
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))["expected"]
    results = []
    receipts = []
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
        receipts.append({
            "schema": "stegverse.morrison-runtime.commit-time-scope.receipt.v1",
            "suite_id": SUITE_ID,
            "case_id": case["case_id"],
            "initial_runtime_result": case["initial_runtime_result"],
            "commit_time_result": observed,
            "displacement": displacement(case["initial_runtime_result"], observed, case["commit_time_inputs"]),
            "authority_posture": AUTHORITY_POSTURE,
            "pass": ok,
        })

    report = {
        "schema": "stegverse.morrison-runtime.commit-time-scope.report.v1",
        "suite_id": SUITE_ID,
        "status": "PASS" if passed == len(results) else "FAIL",
        "case_count": len(results),
        "passed_count": passed,
        "failed_count": len(results) - passed,
        "authority_posture": AUTHORITY_POSTURE,
        "results": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    RECEIPTS.write_text(
        "".join(json.dumps(receipt, separators=(",", ":")) + "\n" for receipt in receipts),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
