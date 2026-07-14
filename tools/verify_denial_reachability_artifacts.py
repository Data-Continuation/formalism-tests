#!/usr/bin/env python3
"""Verify committed denial-reachability proof artifacts and hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/denial_reachability_cases.json"
EXPECTED = ROOT / "tests/fixtures/denial_reachability_expected_outcomes.json"
REPORT = ROOT / "reports/denial_reachability_report.json"
RECEIPTS = ROOT / "receipts/denial_reachability_execution_receipts.jsonl"
STATUS = ROOT / "reports/denial_reachability_artifact_verification.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    for path in (FIXTURES, EXPECTED, REPORT, RECEIPTS):
        if not path.is_file():
            fail(f"missing artifact: {path.relative_to(ROOT)}")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "PASS":
        fail("proof report status is not PASS")
    if report.get("failed_count") != 0 or report.get("passed_count") != 5:
        fail("proof report counts are not 5 passed / 0 failed")

    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)
    if report.get("fixtures_sha256") != fixture_hash:
        fail("fixture hash does not match committed fixture bytes")
    if report.get("expected_outcomes_sha256") != expected_hash:
        fail("expected-outcomes hash does not match committed bytes")

    receipts = [json.loads(line) for line in RECEIPTS.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(receipts) != 5:
        fail("expected exactly five execution-control receipts")

    report_cases = {item["case_id"]: item for item in report.get("results", [])}
    receipt_cases = {item["case_id"]: item for item in receipts}
    if set(report_cases) != set(receipt_cases):
        fail("report and receipt case sets differ")

    for case_id, result in report_cases.items():
        receipt = receipt_cases[case_id]
        for field in (
            "decision",
            "failure_class",
            "consequence_bound",
            "denial_before_binding",
            "denial_controlled_execution",
            "execution_prevented",
            "fixture_sha256",
        ):
            if receipt.get(field) != result.get(field):
                fail(f"receipt mismatch for {case_id}: {field}")

    late = report_cases.get("LATE_REFUSAL", {})
    if late.get("execution_prevented") is not False or late.get("consequence_bound") is not True:
        fail("late-refusal evidence must preserve post-binding non-prevention")

    status = {
        "schema": "stegverse.denial_reachability.artifact_verification.v1",
        "status": "PASS",
        "proof_report_status": report["status"],
        "case_count": len(report_cases),
        "receipt_count": len(receipts),
        "fixtures_sha256": fixture_hash,
        "expected_outcomes_sha256": expected_hash,
        "report_file_sha256": sha256(REPORT),
        "receipts_file_sha256": sha256(RECEIPTS),
        "late_refusal_non_prevention_preserved": True,
        "canonical_execution_evidence": "PENDING_EXTERNAL_DECLARED_TASK_RUN"
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: denial-reachability committed artifacts are internally consistent")


if __name__ == "__main__":
    main()
