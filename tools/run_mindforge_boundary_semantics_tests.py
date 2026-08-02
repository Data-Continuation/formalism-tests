#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAIL_EVIDENCE = {
    "hash_mismatch",
    "missing_history",
    "policy_ambiguous",
    "delegation_partially_revoked",
}


def evaluate(case):
    if case.get("candidate_authorizing") is not False:
        return "FAIL_CLOSED", False, "candidate_authority_violation"
    if case.get("evidence") in FAIL_EVIDENCE:
        return "FAIL_CLOSED", False, case["evidence"]
    if case.get("trusted_time") is not True:
        return "FAIL_CLOSED", False, "trusted_time_unavailable"
    if case.get("target_identity") != "clear":
        return "FAIL_CLOSED", False, "target_identity_ambiguous"
    if case.get("action_semantics") != "stable":
        return "FAIL_CLOSED", False, "action_semantic_drift"
    if case.get("recovery_path") is not True:
        return "FAIL_CLOSED", False, "recovery_path_unavailable"
    if case.get("standing") == "DENY":
        return "DENY", False, "standing_rejects_transition"
    if case.get("standing") == "ALLOW":
        return "ALLOW", False, "standing_allows_candidate_only"
    return "FAIL_CLOSED", False, "standing_unreconstructable"


def main():
    cases = json.loads(
        (ROOT / "tests/fixtures/mindforge_boundary_semantics_cases.json").read_text()
    )["cases"]
    expected = json.loads(
        (ROOT / "tests/fixtures/mindforge_boundary_semantics_expected_outcomes.json").read_text()
    )["expected_outcomes"]

    rows = []
    failures = []
    for case in cases:
        result, executed, reason = evaluate(case)
        row = {
            "case_id": case["id"],
            "result": result,
            "expected": expected[case["id"]],
            "execution_invoked": executed,
            "reason": reason,
        }
        rows.append(row)
        if result != expected[case["id"]] or executed is not False:
            failures.append(row)

    report = {
        "schema_version": "1.0.0",
        "suite": "mindforge_boundary_semantics",
        "status": "PASS" if not failures else "FAIL",
        "case_count": len(rows),
        "passed_count": len(rows) - len(failures),
        "failed_count": len(failures),
        "allow_executes_transition": False,
        "authority_posture": "ARCHITECTURAL_BOUNDARY_SEMANTICS_ONLY",
        "results": rows,
    }

    report_path = ROOT / "reports/mindforge_boundary_semantics_report.json"
    receipt_path = ROOT / "receipts/mindforge_boundary_semantics_execution_receipts.jsonl"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    receipt_path.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
    )
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
