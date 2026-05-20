#!/usr/bin/env python3
"""Direct Representation Non-Consequence proof runner.

This standard-library runner validates that representation-only states are
not consequence-bearing until bound to a transition role and continuation path.
It emits receipts and reports for the existing declared-task workflow.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CASES_PATH = Path("tests/fixtures/representation_non_consequence_cases.json")
RECEIPTS_PATH = Path("reports/representation_non_consequence_receipts.jsonl")
REPORT_JSON_PATH = Path("reports/representation_non_consequence_report.json")
REPORT_MD_PATH = Path("reports/representation_non_consequence_report.md")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_cases() -> dict[str, Any]:
    if not CASES_PATH.exists():
        raise AssertionError(f"missing fixture: {CASES_PATH}")
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError("fixture root must be an object")
    if not isinstance(data.get("cases"), list):
        raise AssertionError("fixture must contain cases list")
    return data


def evaluate(case: dict[str, Any]) -> tuple[str, list[str]]:
    consequence_binding = bool(case.get("consequence_binding"))
    role = case.get("role")
    transition = case.get("transition")
    continuation_path = case.get("continuation_path")

    if not consequence_binding:
        if transition is not None or continuation_path is not None:
            return "FAIL_CLOSED", ["non-consequence case cannot carry transition or continuation path"]
        return "NO_CONSEQUENCE", ["representation is not bound to a consequence-bearing transition"]

    if not role or not transition or not continuation_path:
        return "FAIL_CLOSED", ["consequence-bearing case missing role, transition, or continuation path"]

    if case.get("signoff_required") is True:
        if case.get("authority_present") is True and case.get("capacity_sufficient") is True:
            return "ALLOW_WITH_SIGNOFF", ["same representation is conditional when bound to signoff-required role"]
        return "FAIL_CLOSED", ["signoff-required representation lacks authority or capacity"]

    if case.get("authority_required") is True:
        if case.get("authority_present") is not True:
            return "FAIL_CLOSED", ["consequence-bearing representation lacks authority"]
        if case.get("capacity_sufficient") is not True:
            return "FAIL_CLOSED", ["consequence-bearing representation lacks sufficient capacity"]

    return "ALLOW", ["representation is consequence-bearing only after role and transition binding"]


def make_receipt(case: dict[str, Any], outcome: str, reasons: list[str], matched_expected: bool) -> dict[str, Any]:
    receipt = {
        "schema": "stegverse_representation_non_consequence_receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "theorem": "Representation Non-Consequence",
        "case_id": case.get("case_id"),
        "datum_id": case.get("datum_id"),
        "content_class": case.get("content_class"),
        "representation_state": case.get("representation_state"),
        "role": case.get("role"),
        "transition": case.get("transition"),
        "continuation_path": case.get("continuation_path"),
        "consequence_binding": case.get("consequence_binding"),
        "expected_decision": case.get("expected_decision"),
        "outcome": outcome,
        "matched_expected": matched_expected,
        "reasons": reasons,
        "basis": case.get("basis"),
    }
    receipt["receipt_hash"] = sha256(receipt)
    return receipt


def write_markdown(report: dict[str, Any], receipts: list[dict[str, Any]]) -> None:
    counts = report["decision_counts"]
    rows = "\n".join(
        f"| {r['case_id']} | {r['representation_state']} | {r.get('role') or 'none'} | {r.get('transition') or 'none'} | {r['outcome']} | {r['basis']} |"
        for r in receipts
    )
    counts_rows = "\n".join(f"| {decision} | {count} |" for decision, count in sorted(counts.items()))

    text = f"""# Representation Non-Consequence Test Report

## Public proof claim

```text
Representation alone has no consequence-bearing status until it is bound to a transition role and continuation path.
```

## Verification status

Success: `{str(report['success']).lower()}`

## Summary

| Decision | Count |
|---|---:|
{counts_rows}

## Receipts

| Case | Representation State | Role | Transition | Decision | Basis |
|---|---|---|---|---|---|
{rows}

## Interpretation

This report directly closes the earlier gap where Representation Non-Consequence was only indirectly supported by same-data role dependence.

The receipt set verifies that a represented datum, by itself, is not a continuation event and does not carry consequence authority. The same content becomes admissibility-relevant only when it is bound to a role, transition, and continuation path.

Therefore governance cannot attach to representation alone. It must attach to representation-as-bound-to-transition.
"""
    REPORT_MD_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        data = load_cases()
        receipts: list[dict[str, Any]] = []
        failures: list[str] = []
        decision_counts: dict[str, int] = {}
        assertion_count = 0

        for case in data["cases"]:
            case_id = case.get("case_id")
            if not case_id:
                raise AssertionError("case missing case_id")
            assertion_count += 1

            outcome, reasons = evaluate(case)
            expected = case.get("expected_decision")
            matched_expected = outcome == expected
            assertion_count += 1

            if not matched_expected:
                failures.append(f"{case_id}: expected {expected}, got {outcome}")

            decision_counts[outcome] = decision_counts.get(outcome, 0) + 1
            receipts.append(make_receipt(case, outcome, reasons, matched_expected))

        assertion_count += 1 if decision_counts.get("NO_CONSEQUENCE", 0) >= 3 else 0
        if decision_counts.get("NO_CONSEQUENCE", 0) < 3:
            failures.append("expected at least three NO_CONSEQUENCE cases")

        assertion_count += 1 if decision_counts.get("ALLOW", 0) >= 1 else 0
        if decision_counts.get("ALLOW", 0) < 1:
            failures.append("expected at least one ALLOW case")

        assertion_count += 1 if decision_counts.get("ALLOW_WITH_SIGNOFF", 0) >= 1 else 0
        if decision_counts.get("ALLOW_WITH_SIGNOFF", 0) < 1:
            failures.append("expected at least one ALLOW_WITH_SIGNOFF case")

        assertion_count += 1 if decision_counts.get("FAIL_CLOSED", 0) >= 2 else 0
        if decision_counts.get("FAIL_CLOSED", 0) < 2:
            failures.append("expected at least two FAIL_CLOSED cases")

        REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS_PATH.write_text(
            "".join(json.dumps(receipt, sort_keys=True) + "\n" for receipt in receipts),
            encoding="utf-8"
        )

        report = {
            "schema": "stegverse_representation_non_consequence_report.v1",
            "success": not failures,
            "theorem": data.get("theorem"),
            "claim": data.get("claim"),
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "assertion_count": assertion_count,
            "decision_counts": decision_counts,
            "failures": failures,
            "receipts_path": str(RECEIPTS_PATH),
            "report_markdown_path": str(REPORT_MD_PATH),
            "message": "Representation Non-Consequence direct proof passed." if not failures else "Representation Non-Consequence proof failed."
        }

        REPORT_JSON_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_markdown(report, receipts)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if not failures else 1

    except Exception as exc:
        REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_representation_non_consequence_report.v1",
            "success": False,
            "error": str(exc),
        }
        REPORT_JSON_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
