#!/usr/bin/env python3
"""
Stage 5 system-coherent boundary transition gate.

This gate adds executable proof cases for:

- system-coherence failure
- purpose-convergence failure
- degraded-authority recoverability
- governed boundary reset
- governed boundary evolution
- multi-body coupling stress

Input:
    tests/boundary_transition_cases.json

Outputs:
    reports/boundary_transition_receipts.jsonl
    reports/boundary_transition_report.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


INPUT_PATH = Path("tests/boundary_transition_cases.json")
RECEIPTS_PATH = Path("reports/boundary_transition_receipts.jsonl")
REPORT_PATH = Path("reports/boundary_transition_report.md")

CONTRACT_FLOORS = {
    "boundary_integrity": 0.50,
    "recoverability": 0.50,
    "purpose_convergence": 0.35,
    "system_coherence": 0.45,
    "degraded_authority_recoverability": 0.40,
    "multi_body_coupling_risk": 0.80,
    "uncertainty": 0.70,
}


REQUIRED_FIELDS = [
    "case_id",
    "transition_id",
    "transition_name",
    "transition_family",
    "theorem_basis",
    "boundary_behavior",
    "multi_body_coupling_class",
    "boundary_integrity",
    "recoverability",
    "purpose_convergence",
    "system_coherence",
    "degraded_authority_recoverability",
    "boundary_evolution_available",
    "boundary_reset_available",
    "multi_body_coupling_risk",
    "uncertainty",
    "expected_decision",
    "expected_basis_contains",
]


def score(value: Any, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if result < 0.0 or result > 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return result


def text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def bool_value(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be boolean")
    return value


def load_cases() -> List[Dict[str, Any]]:
    payload = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise ValueError("tests/boundary_transition_cases.json must contain a cases list")
    return cases


def missing_fields(case: Dict[str, Any]) -> List[str]:
    return [field for field in REQUIRED_FIELDS if field not in case]


def decide(case: Dict[str, Any]) -> Dict[str, Any]:
    missing = missing_fields(case)

    case_id = text(case.get("case_id"), "case_id")
    transition_id = text(case.get("transition_id"), "transition_id")
    transition_name = text(case.get("transition_name"), "transition_name")
    transition_family = text(case.get("transition_family"), "transition_family")
    theorem_basis = text(case.get("theorem_basis"), "theorem_basis")
    boundary_behavior = text(case.get("boundary_behavior"), "boundary_behavior")
    multi_body_coupling_class = text(case.get("multi_body_coupling_class"), "multi_body_coupling_class")

    boundary_integrity = score(case.get("boundary_integrity"), "boundary_integrity")
    recoverability = score(case.get("recoverability"), "recoverability")
    purpose_convergence = score(case.get("purpose_convergence"), "purpose_convergence")
    system_coherence = score(case.get("system_coherence"), "system_coherence")
    degraded_authority_recoverability = score(
        case.get("degraded_authority_recoverability"),
        "degraded_authority_recoverability",
    )
    multi_body_coupling_risk = score(case.get("multi_body_coupling_risk"), "multi_body_coupling_risk")
    uncertainty = score(case.get("uncertainty"), "uncertainty")

    boundary_evolution_available = bool_value(
        case.get("boundary_evolution_available"),
        "boundary_evolution_available",
    )
    boundary_reset_available = bool_value(
        case.get("boundary_reset_available"),
        "boundary_reset_available",
    )

    basis: List[str] = []
    decision = "ALLOW"

    if missing:
        decision = "FAIL_CLOSED"
        basis.append("boundary transition class is missing required admissibility contract fields")

    elif uncertainty >= CONTRACT_FLOORS["uncertainty"]:
        decision = "FAIL_CLOSED"
        basis.append("uncertainty exceeds boundary-class tolerance")

    elif boundary_integrity < CONTRACT_FLOORS["boundary_integrity"] and recoverability < CONTRACT_FLOORS["recoverability"]:
        decision = "FAIL_CLOSED"
        basis.append("boundary integrity and recoverability below boundary-class floors")

    elif degraded_authority_recoverability < CONTRACT_FLOORS["degraded_authority_recoverability"]:
        decision = "FAIL_CLOSED"
        basis.append("degraded-authority recoverability below boundary-class floor")

    elif multi_body_coupling_risk > CONTRACT_FLOORS["multi_body_coupling_risk"]:
        decision = "FAIL_CLOSED"
        basis.append("multi-body coupling risk exceeds boundary-class tolerance")

    elif purpose_convergence < CONTRACT_FLOORS["purpose_convergence"] and boundary_reset_available:
        decision = "RESET_BOUNDARY"
        if boundary_behavior == "reset_recoverable_non_convergence":
            basis.append("recoverable non-convergence detected and reset path is available")
        else:
            basis.append("purpose convergence below boundary-class floor and reset path is available")

    elif system_coherence < CONTRACT_FLOORS["system_coherence"] and boundary_evolution_available:
        decision = "EVOLVE_BOUNDARY"
        if boundary_behavior == "bounded_boundary_evolution":
            basis.append("bounded boundary evolution is available")
        else:
            basis.append("system coherence below boundary-class floor")

    elif (
        boundary_integrity >= 0.60
        and recoverability >= 0.60
        and purpose_convergence >= 0.60
        and system_coherence >= 0.60
        and degraded_authority_recoverability >= 0.60
        and multi_body_coupling_risk <= 0.60
        and uncertainty < 0.50
    ):
        decision = "ALLOW"
        basis.append("boundary class admissibility contract satisfied")

    else:
        decision = "FAIL_CLOSED"
        basis.append("boundary transition does not satisfy allow, reset, or evolution conditions")

    expected_decision = text(case.get("expected_decision"), "expected_decision")
    expected_basis_contains = text(case.get("expected_basis_contains"), "expected_basis_contains")

    matched_expected_decision = decision == expected_decision
    matched_expected_basis = any(expected_basis_contains in item for item in basis)

    return {
        "receipt_id": f"stage5-{case_id}",
        "case_id": case_id,
        "transition_id": transition_id,
        "transition_name": transition_name,
        "transition_family": transition_family,
        "theorem_basis": theorem_basis,
        "decision": decision,
        "basis": basis,
        "matched_expected_decision": matched_expected_decision,
        "matched_expected_basis": matched_expected_basis,
        "boundary_contract": {
            "boundary_behavior": boundary_behavior,
            "multi_body_coupling_class": multi_body_coupling_class,
            "boundary_integrity": boundary_integrity,
            "recoverability": recoverability,
            "purpose_convergence": purpose_convergence,
            "system_coherence": system_coherence,
            "degraded_authority_recoverability": degraded_authority_recoverability,
            "boundary_evolution_available": boundary_evolution_available,
            "boundary_reset_available": boundary_reset_available,
            "multi_body_coupling_risk": multi_body_coupling_risk,
            "uncertainty": uncertainty,
        },
    }


def write_receipts(receipts: List[Dict[str, Any]]) -> None:
    RECEIPTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RECEIPTS_PATH.open("w", encoding="utf-8") as handle:
        for receipt in receipts:
            handle.write(json.dumps(receipt, sort_keys=True) + "\n")


def count_by_decision(receipts: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for receipt in receipts:
        decision = receipt["decision"]
        counts[decision] = counts.get(decision, 0) + 1
    return counts


def row(values: List[Any]) -> str:
    return "| " + " | ".join(str(value) for value in values) + " |"


def write_report(receipts: List[Dict[str, Any]]) -> None:
    success = all(
        receipt["matched_expected_decision"] and receipt["matched_expected_basis"]
        for receipt in receipts
    )
    counts = count_by_decision(receipts)

    lines = [
        "# Stage 5 System-Coherent Boundary Transition Classes Report",
        "",
        "## Public proof claims",
        "",
        "```text",
        "a boundary is admissible only while it remains coherent with the recoverable convergence of the entity-system it governs",
        "a boundary that prevents harm by preventing meaningful convergence has ceased to be coherent to the system",
        "boundary reset and boundary evolution are admissible transition outcomes when governed by recoverability and coherence",
        "```",
        "",
        "## Verification status",
        "",
        f"Success: `{str(success).lower()}`",
        "",
        "## Decision summary",
        "",
        "| Decision | Count |",
        "|---|---:|",
    ]

    for decision in sorted(counts):
        lines.append(row([decision, counts[decision]]))

    lines.extend([
        "",
        "## Boundary transition receipts",
        "",
        "| Receipt | Transition ID | Theorem basis | Coupling class | Decision | Basis |",
        "|---|---|---|---|---|---|",
    ])

    for receipt in receipts:
        contract = receipt["boundary_contract"]
        lines.append(row([
            receipt["receipt_id"],
            receipt["transition_id"],
            receipt["theorem_basis"],
            contract["multi_body_coupling_class"],
            receipt["decision"],
            "; ".join(receipt["basis"]),
        ]))

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Stage 5 adds system-coherent boundary dynamics to the transition table proof surface.",
        "",
        "The new receipt set demonstrates that a boundary can fail because it loses system coherence, blocks purpose convergence, fails under degraded authority, or creates excessive multi-body coupling risk.",
        "",
        "The receipt set also verifies two non-binary admissibility outcomes: RESET_BOUNDARY and EVOLVE_BOUNDARY.",
        "",
        "This moves the transition table from consequence-class verification into boundary-dynamics verification.",
        "",
    ])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    receipts = [decide(case) for case in load_cases()]
    write_receipts(receipts)
    write_report(receipts)

    success = all(
        receipt["matched_expected_decision"] and receipt["matched_expected_basis"]
        for receipt in receipts
    )

    print(json.dumps({
        "stage": "stage_5_system_coherent_boundary_transition_classes",
        "receipt_count": len(receipts),
        "success": success,
        "receipts_path": str(RECEIPTS_PATH),
        "report_path": str(REPORT_PATH),
    }, indent=2, sort_keys=True))

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
