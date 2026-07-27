#!/usr/bin/env python3
"""Verify optimization-target report and receipts against the committed baseline."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests/fixtures/optimization_target_commit_boundary_artifact_baseline.json"
REPORT = ROOT / "reports/optimization_target_commit_boundary_report.json"
RECEIPTS = ROOT / "receipts/optimization_target_commit_boundary_execution_receipts.jsonl"
OUTPUT = ROOT / "reports/optimization_target_commit_boundary_artifact_verification.json"


def main() -> int:
    errors: list[str] = []
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    receipts = [json.loads(line) for line in RECEIPTS.read_text(encoding="utf-8").splitlines() if line.strip()]

    checks = {
        "suite_id": baseline["suite_id"],
        "status": baseline["required_status"],
        "case_count": baseline["required_case_count"],
        "passed_count": baseline["required_passed_count"],
        "failed_count": baseline["required_failed_count"],
        "authority_posture": baseline["required_authority_posture"],
    }
    for field, expected in checks.items():
        if report.get(field) != expected:
            errors.append(f"report.{field} must equal {expected!r}")

    observed = {item.get("case_id"): item.get("observed_result") for item in report.get("results", [])}
    if observed != baseline["required_case_results"]:
        errors.append("report case-result map mismatch")
    if any(item.get("pass") is not True for item in report.get("results", [])):
        errors.append("one or more report cases did not pass")

    if len(receipts) != baseline["required_receipt_count"]:
        errors.append("receipt count mismatch")
    receipt_map = {item.get("case_id"): item.get("commit_time_result") for item in receipts}
    if receipt_map != baseline["required_case_results"]:
        errors.append("receipt result map mismatch")
    for receipt in receipts:
        case_id = receipt.get("case_id")
        if receipt.get("suite_id") != baseline["suite_id"]:
            errors.append(f"receipt suite mismatch: {case_id}")
        if receipt.get("authority_posture") != baseline["required_authority_posture"]:
            errors.append(f"receipt authority mismatch: {case_id}")
        if receipt.get("pass") is not True:
            errors.append(f"receipt pass false: {case_id}")

    result = {
        "schema": "stegverse.optimization-target.commit-boundary.artifact-verification.v1",
        "suite_id": baseline["suite_id"],
        "status": "PASS" if not errors else "FAIL",
        "verified_report": str(REPORT.relative_to(ROOT)),
        "verified_receipts": str(RECEIPTS.relative_to(ROOT)),
        "case_count": report.get("case_count"),
        "receipt_count": len(receipts),
        "authority_posture": baseline["required_authority_posture"],
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
