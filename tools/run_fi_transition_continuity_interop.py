#!/usr/bin/env python3
"""Run continuity-specific interoperability checks for FI-TRANSITION-001."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "fixtures" / "fi_transition_continuity_interop_cases.json"
EXPECTED = ROOT / "tests" / "fixtures" / "fi_transition_continuity_interop_expected_outcomes.json"
REPORT = ROOT / "reports" / "fi_transition_continuity_interop_report.json"


def decide(case: dict) -> str:
    if case["predecessor_state"] == case["successor_state"] or not case["difference_detected"]:
        return "NOT_A_TRANSITION"
    if not case["subject_identity_preserved"]:
        return "FAIL_CLOSED"
    if not case["ordered_evidence_chain_present"]:
        return "FAIL_CLOSED"
    if float(case["continuity_score"]) < float(case["continuity_min"]):
        return "FAIL_CLOSED"
    return "INTEROPERABLE"


def main() -> int:
    cases_doc = json.loads(CASES.read_text(encoding="utf-8"))
    expected_doc = json.loads(EXPECTED.read_text(encoding="utf-8"))
    expected = expected_doc["expected"]

    results = []
    failures = 0
    for case in cases_doc["cases"]:
        actual = decide(case)
        wanted = expected[case["case_id"]]
        passed = actual == wanted == case["expected"]
        failures += 0 if passed else 1
        results.append({
            "case_id": case["case_id"],
            "expected": wanted,
            "actual": actual,
            "passed": passed,
        })

    report = {
        "suite_id": cases_doc["suite_id"],
        "suite_version": cases_doc["suite_version"],
        "status": "PASS" if failures == 0 else "FAIL",
        "total": len(results),
        "passed": len(results) - failures,
        "failed": failures,
        "authority_posture": "CONTINUITY_INTEROPERABILITY_ONLY",
        "results": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
