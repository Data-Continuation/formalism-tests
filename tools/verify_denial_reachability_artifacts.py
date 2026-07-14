#!/usr/bin/env python3
"""Verify committed denial-reachability proof artifacts and hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/denial_reachability_cases.json"
EXPECTED = ROOT / "tests/fixtures/denial_reachability_expected_outcomes.json"
BASELINE = ROOT / "tests/fixtures/denial_reachability_artifact_baseline.json"
REPORT = ROOT / "reports/denial_reachability_report.json"
RECEIPTS = ROOT / "receipts/denial_reachability_execution_receipts.jsonl"
STATUS = ROOT / "reports/denial_reachability_artifact_verification.json"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    for path in (FIXTURES, EXPECTED, BASELINE, REPORT, RECEIPTS):
        if not path.is_file():
            fail(f"missing artifact: {path.relative_to(ROOT)}")

    fixtures_document = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected_document = json.loads(EXPECTED.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    if report.get("status") != "PASS":
        fail("proof report status is not PASS")
    if report.get("failed_count") != 0 or report.get("passed_count") != 5:
        fail("proof report counts are not 5 passed / 0 failed")

    fixture_canonical_hash = canonical_hash(fixtures_document)
    expected_canonical_hash = canonical_hash(expected_document)
    if report.get("fixtures_sha256") != fixture_canonical_hash:
        fail("fixture canonical hash does not match committed fixture document")
    if report.get("expected_outcomes_sha256") != expected_canonical_hash:
        fail("expected-outcomes canonical hash does not match committed document")
    if baseline.get("proof_report_canonical_sha256") != report.get("report_sha256"):
        fail("proof report canonical hash does not match artifact baseline")

    generated_hashes = {
        "reports/denial_reachability_report.json": file_sha256(REPORT),
        "receipts/denial_reachability_execution_receipts.jsonl": file_sha256(RECEIPTS),
    }
    expected_generated_hashes = baseline.get("generated_file_sha256", {})
    if generated_hashes != expected_generated_hashes:
        fail("generated report or receipt bytes differ from artifact baseline")

    receipts = [
        json.loads(line)
        for line in RECEIPTS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(receipts) != 5:
        fail("expected exactly five execution-control receipts")

    report_cases = {item["case_id"]: item for item in report.get("results", [])}
    receipt_cases = {item["case_id"]: item for item in receipts}
    if set(report_cases) != set(receipt_cases):
        fail("report and receipt case sets differ")

    receipt_contract_fields = (
        "decision",
        "failure_class",
        "consequence_bound",
        "denial_controlled_execution",
        "execution_prevented",
        "fixture_sha256",
    )
    for case_id, result in report_cases.items():
        receipt = receipt_cases[case_id]
        if receipt.get("formalism_id") != report.get("formalism_id"):
            fail(f"formalism mismatch for {case_id}")
        if receipt.get("report_sha256") != report.get("report_sha256"):
            fail(f"report reference mismatch for {case_id}")
        for field in receipt_contract_fields:
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
        "fixtures_canonical_sha256": fixture_canonical_hash,
        "expected_outcomes_canonical_sha256": expected_canonical_hash,
        "fixtures_file_sha256": file_sha256(FIXTURES),
        "expected_outcomes_file_sha256": file_sha256(EXPECTED),
        "report_file_sha256": generated_hashes["reports/denial_reachability_report.json"],
        "receipts_file_sha256": generated_hashes["receipts/denial_reachability_execution_receipts.jsonl"],
        "artifact_baseline_file_sha256": file_sha256(BASELINE),
        "byte_equivalence_to_baseline": True,
        "receipt_contract_fields": list(receipt_contract_fields),
        "late_refusal_non_prevention_preserved": True,
        "canonical_execution_evidence": "PENDING_EXTERNAL_DECLARED_TASK_RUN",
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: denial-reachability artifacts match canonical and byte baselines")


if __name__ == "__main__":
    main()
