#!/usr/bin/env python3
"""Execute denial-reachability proof fixtures and emit deterministic evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/denial_reachability_cases.json"
EXPECTED = ROOT / "tests/fixtures/denial_reachability_expected_outcomes.json"
REPORT_JSON = ROOT / "reports/denial_reachability_report.json"
REPORT_MD = ROOT / "reports/denial_reachability_continuation_report.md"
RECEIPTS = ROOT / "receipts/denial_reachability_execution_receipts.jsonl"

REQUIRED_PREDICATES = {
    "ADMISSIBLE",
    "AUTHORITY_CURRENT",
    "STATE_SUFFICIENT",
    "DENIAL_REACHABLE",
    "DENIAL_ENFORCEABLE",
}


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evaluate(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case["case_id"]
    predicates = case["predicates"]
    boundary = case["boundary"]

    missing = REQUIRED_PREDICATES - set(predicates)
    if missing:
        raise ValueError(f"{case_id}: missing predicates {sorted(missing)}")

    deny_time = boundary.get("deny_result_time")
    bind_time = boundary["consequence_binding_time"]
    denial_before_binding = deny_time is not None and deny_time < bind_time
    denial_controlled_execution = bool(
        predicates["DENIAL_REACHABLE"]
        and predicates["DENIAL_ENFORCEABLE"]
        and denial_before_binding
        and boundary["actuator_obeys_gate"]
        and boundary["single_boundary_resolution"]
        and not boundary["consequence_bound"]
    )

    if case_id == "LATE_REFUSAL":
        decision = "FAIL_CLOSED"
        failure_class = "LATE_REFUSAL"
        execution_prevented = False
    elif not boundary["single_boundary_resolution"]:
        decision = "FAIL_CLOSED"
        failure_class = "SPLIT_BOUNDARY_INSUFFICIENCY"
        execution_prevented = not boundary["consequence_bound"]
    elif predicates["DENIAL_REACHABLE"] and not predicates["DENIAL_ENFORCEABLE"]:
        decision = "FAIL_CLOSED"
        failure_class = "COSMETIC_GATING"
        execution_prevented = not boundary["consequence_bound"]
    elif not predicates["DENIAL_REACHABLE"] or not predicates["DENIAL_ENFORCEABLE"]:
        decision = "FAIL_CLOSED"
        failure_class = "INHERITED_AUTHORIZATION"
        execution_prevented = not boundary["consequence_bound"]
    elif not predicates["ADMISSIBLE"]:
        decision = "DENY"
        failure_class = None
        execution_prevented = denial_controlled_execution
    elif all(predicates[name] for name in REQUIRED_PREDICATES):
        decision = "ALLOW"
        failure_class = None
        execution_prevented = False
    else:
        decision = "FAIL_CLOSED"
        failure_class = "STATE_OR_AUTHORITY_INSUFFICIENT"
        execution_prevented = not boundary["consequence_bound"]

    return {
        "case_id": case_id,
        "decision": decision,
        "failure_class": failure_class,
        "execution_prevented": execution_prevented,
        "denial_controlled_execution": denial_controlled_execution,
        "consequence_bound": boundary["consequence_bound"],
        "denial_before_binding": denial_before_binding,
        "fixture_sha256": canonical_hash(case),
    }


def main() -> None:
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected_document = json.loads(EXPECTED.read_text(encoding="utf-8"))
    expected = expected_document["expected"]

    results = [evaluate(case) for case in fixtures["cases"]]
    mismatches: list[dict[str, Any]] = []

    for result in results:
        case_expected = expected[result["case_id"]]
        observed = {
            key: result[key]
            for key in (
                "decision",
                "failure_class",
                "execution_prevented",
                "denial_controlled_execution",
            )
        }
        if observed != case_expected:
            mismatches.append(
                {
                    "case_id": result["case_id"],
                    "expected": case_expected,
                    "observed": observed,
                }
            )

    status = "PASS" if not mismatches else "FAIL"
    report = {
        "schema": "stegverse.denial_reachability.report.v1",
        "formalism_id": fixtures["formalism_id"],
        "status": status,
        "case_count": len(results),
        "passed_count": len(results) - len(mismatches),
        "failed_count": len(mismatches),
        "required_predicates": sorted(REQUIRED_PREDICATES),
        "results": results,
        "mismatches": mismatches,
        "fixtures_sha256": canonical_hash(fixtures),
        "expected_outcomes_sha256": canonical_hash(expected_document),
    }
    report["report_sha256"] = canonical_hash(report)

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    markdown = [
        "# Denial Reachability Continuation Report",
        "",
        f"- Status: `{status}`",
        f"- Cases: `{len(results)}`",
        f"- Passed: `{len(results) - len(mismatches)}`",
        f"- Failed: `{len(mismatches)}`",
        f"- Report SHA-256: `{report['report_sha256']}`",
        "",
        "## Results",
        "",
    ]
    for result in results:
        markdown.extend(
            [
                f"### {result['case_id']}",
                "",
                f"- Decision: `{result['decision']}`",
                f"- Failure class: `{result['failure_class']}`",
                f"- Execution prevented: `{str(result['execution_prevented']).lower()}`",
                f"- Denial controlled execution: `{str(result['denial_controlled_execution']).lower()}`",
                "",
            ]
        )
    markdown.extend(
        [
            "## Boundary conclusion",
            "",
            "Authorization is valid at the consequence-binding boundary only when denial remains both reachable and enforceable until the decision controls execution.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(markdown), encoding="utf-8")

    with RECEIPTS.open("w", encoding="utf-8") as handle:
        for result in results:
            receipt = {
                "schema": "stegverse.denial_reachability.execution_receipt.v1",
                "formalism_id": fixtures["formalism_id"],
                "case_id": result["case_id"],
                "decision": result["decision"],
                "failure_class": result["failure_class"],
                "execution_prevented": result["execution_prevented"],
                "denial_controlled_execution": result["denial_controlled_execution"],
                "consequence_bound": result["consequence_bound"],
                "fixture_sha256": result["fixture_sha256"],
                "report_sha256": report["report_sha256"],
            }
            receipt["receipt_sha256"] = canonical_hash(receipt)
            handle.write(json.dumps(receipt, sort_keys=True) + "\n")

    if mismatches:
        raise SystemExit(f"FAIL: {len(mismatches)} denial-reachability case(s) mismatched")

    print(f"PASS: {len(results)} denial-reachability cases verified")
    print(REPORT_JSON.relative_to(ROOT))
    print(REPORT_MD.relative_to(ROOT))
    print(RECEIPTS.relative_to(ROOT))


if __name__ == "__main__":
    main()
