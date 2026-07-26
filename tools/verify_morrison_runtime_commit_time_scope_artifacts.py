#!/usr/bin/env python3
"""Verify Morrison Runtime commit-time scope report and receipts against baseline."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_artifact_baseline.json"
REPORT = ROOT / "reports/morrison_runtime_commit_time_scope_report.json"
RECEIPTS = ROOT / "receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl"
VERIFICATION = ROOT / "reports/morrison_runtime_commit_time_scope_artifact_verification.json"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    baseline = json.loads(BASELINE.read_text())
    report = json.loads(REPORT.read_text())
    receipts = [json.loads(line) for line in RECEIPTS.read_text().splitlines() if line.strip()]
    errors: list[str] = []

    if report.get("suite_id") != baseline["suite_id"]:
        fail(errors, "suite_id mismatch")
    if report.get("status") != baseline["required_status"]:
        fail(errors, "report status mismatch")
    if report.get("case_count") != baseline["required_case_count"]:
        fail(errors, "case_count mismatch")
    if report.get("passed_count") != baseline["required_passed_count"]:
        fail(errors, "passed_count mismatch")
    if report.get("failed_count") != baseline["required_failed_count"]:
        fail(errors, "failed_count mismatch")
    if report.get("authority_posture") != baseline["required_authority_posture"]:
        fail(errors, "authority_posture mismatch")

    observed = {item["case_id"]: item["observed_stegverse_result"] for item in report.get("results", [])}
    if observed != baseline["required_case_results"]:
        fail(errors, "case result map mismatch")
    if any(not item.get("pass", False) for item in report.get("results", [])):
        fail(errors, "one or more report cases failed")

    if len(receipts) != baseline["required_receipt_count"]:
        fail(errors, "receipt count mismatch")
    receipt_map = {item["case_id"]: item["commit_time_result"] for item in receipts}
    if receipt_map != baseline["required_case_results"]:
        fail(errors, "receipt result map mismatch")
    for receipt in receipts:
        if receipt.get("suite_id") != baseline["suite_id"]:
            fail(errors, f"receipt suite mismatch: {receipt.get('case_id')}")
        if receipt.get("authority_posture") != baseline["required_authority_posture"]:
            fail(errors, f"receipt authority mismatch: {receipt.get('case_id')}")
        if receipt.get("pass") is not True:
            fail(errors, f"receipt pass false: {receipt.get('case_id')}")

    verification = {
        "schema": "stegverse.morrison-runtime.commit-time-scope.artifact-verification.v1",
        "suite_id": baseline["suite_id"],
        "status": "PASS" if not errors else "FAIL",
        "verified_report": str(REPORT.relative_to(ROOT)),
        "verified_receipts": str(RECEIPTS.relative_to(ROOT)),
        "case_count": report.get("case_count"),
        "receipt_count": len(receipts),
        "authority_posture": baseline["required_authority_posture"],
        "errors": errors,
    }
    VERIFICATION.parent.mkdir(parents=True, exist_ok=True)
    VERIFICATION.write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps(verification, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
