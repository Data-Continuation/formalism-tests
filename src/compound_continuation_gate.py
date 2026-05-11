#!/usr/bin/env python3
"""
Stage 3 compound continuation gate.

This script generates executable proof artifacts for:

- Local-Composite Non-Equivalence
- Commit-Time Sufficiency
- Inference-Window Collapse
- Recoverability Floor
- Replay Non-Reversal

Inputs:
    tests/compound_cases.json

Outputs:
    reports/compound_receipts.jsonl
    reports/compound_continuation_report.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


INPUT_PATH = Path("tests/compound_cases.json")
RECEIPTS_PATH = Path("reports/compound_receipts.jsonl")
REPORT_PATH = Path("reports/compound_continuation_report.md")

INF_WINDOW_MIN = 0.05


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
        raise ValueError("tests/compound_cases.json must contain a cases list")
    return cases


def decide(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id = text(case.get("case_id"), "case_id")
    theorem = text(case.get("theorem"), "theorem")
    data_id = text(case.get("data_id"), "data_id")
    role = text(case.get("role"), "role")
    transition = text(case.get("transition"), "transition")

    local_decisions = case.get("local_decisions")
    if not isinstance(local_decisions, list) or not all(isinstance(x, str) for x in local_decisions):
        raise ValueError(f"{case_id}: local_decisions must be a string list")

    basis_complete = bool_value(case.get("basis_complete"), "basis_complete")
    legitimacy_capacity = score(case.get("legitimacy_capacity"), "legitimacy_capacity")
    consequence_mass = score(case.get("consequence_mass"), "consequence_mass")
    inference_window_width = score(case.get("inference_window_width"), "inference_window_width")
    recoverability_floor = score(case.get("recoverability_floor"), "recoverability_floor")
    recoverability_score = score(case.get("recoverability_score"), "recoverability_score")
    replay_intent = text(case.get("replay_intent"), "replay_intent")
    replay_matches_receipt = bool_value(case.get("replay_matches_receipt"), "replay_matches_receipt")
    attempts_reversal = bool_value(case.get("attempts_reversal"), "attempts_reversal")

    pre_commit_state_hash = text(case.get("pre_commit_state_hash"), "pre_commit_state_hash")
    commit_state_hash = text(case.get("commit_state_hash"), "commit_state_hash")

    basis: List[str] = []
    decision = "ALLOW"

    if not basis_complete:
        decision = "FAIL_CLOSED"
        basis.append("missing required compound continuation basis")

    elif any(item.upper() == "FAIL_CLOSED" for item in local_decisions):
        decision = "FAIL_CLOSED"
        basis.append("at least one local continuation component failed closed")

    elif consequence_mass > legitimacy_capacity:
        decision = "FAIL_CLOSED"
        basis.append("composite consequence mass exceeds legitimacy capacity")

    elif pre_commit_state_hash != commit_state_hash:
        decision = "FAIL_CLOSED"
        basis.append("commit-time state drift detected")

    elif inference_window_width < INF_WINDOW_MIN:
        decision = "FAIL_CLOSED"
        basis.append("inference window collapsed below continuation threshold")

    elif recoverability_score < recoverability_floor:
        decision = "FAIL_CLOSED"
        basis.append("recoverability score below required floor")

    elif replay_intent == "reverse" or attempts_reversal:
        decision = "FAIL_CLOSED"
        basis.append("replay may reconstruct receipt state but may not reverse consequence")

    elif not replay_matches_receipt:
        decision = "FAIL_CLOSED"
        basis.append("replay does not match receipt state")

    else:
        basis.append("compound continuation remains within capacity and recoverability bounds")

    expected_decision = text(case.get("expected_decision"), "expected_decision")
    expected_basis_contains = text(case.get("expected_basis_contains"), "expected_basis_contains")

    matched_expected_decision = decision == expected_decision
    matched_expected_basis = any(expected_basis_contains in item for item in basis)

    return {
        "receipt_id": f"stage3-{case_id}",
        "case_id": case_id,
        "theorem": theorem,
        "data_id": data_id,
        "role": role,
        "transition": transition,
        "local_decisions": local_decisions,
        "decision": decision,
        "basis": basis,
        "matched_expected_decision": matched_expected_decision,
        "matched_expected_basis": matched_expected_basis,
        "metrics": {
            "legitimacy_capacity": legitimacy_capacity,
            "consequence_mass": consequence_mass,
            "inference_window_width": inference_window_width,
            "recoverability_floor": recoverability_floor,
            "recoverability_score": recoverability_score,
        },
        "state": {
            "pre_commit_state_hash": pre_commit_state_hash,
            "commit_state_hash": commit_state_hash,
        },
        "replay": {
            "replay_intent": replay_intent,
            "replay_matches_receipt": replay_matches_receipt,
            "attempts_reversal": attempts_reversal,
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


def theorem_status(receipts: List[Dict[str, Any]]) -> Dict[str, str]:
    status: Dict[str, str] = {}
    for receipt in receipts:
        theorem = receipt["theorem"]
        if receipt["matched_expected_decision"] and receipt["matched_expected_basis"]:
            status[theorem] = "Covered"
        else:
            status[theorem] = "Mismatch"
    return status


def markdown_table_row(values: List[Any]) -> str:
    return "| " + " | ".join(str(value) for value in values) + " |"


def write_report(receipts: List[Dict[str, Any]]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    counts = count_by_decision(receipts)
    statuses = theorem_status(receipts)
    success = all(
        receipt["matched_expected_decision"] and receipt["matched_expected_basis"]
        for receipt in receipts
    )

    lines: List[str] = [
        "# Stage 3 Compound Continuation Test Report",
        "",
        "## Public proof claims",
        "",
        "```text",
        "local allow + local allow does not imply composite allow",
        "pre-commit allow does not imply commit-time allow after state drift",
        "replay can reconstruct consequence state but cannot reverse consequence",
        "recoverability and inference-window floors are admissibility conditions",
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
        lines.append(markdown_table_row([decision, counts[decision]]))

    lines.extend([
        "",
        "## Theorem mapping",
        "",
        "| Theorem | Status |",
        "|---|---|",
    ])

    for theorem in sorted(statuses):
        lines.append(markdown_table_row([theorem, statuses[theorem]]))

    lines.extend([
        "",
        "## Receipts",
        "",
        "| Receipt | Theorem | Role | Transition | Decision | Basis |",
        "|---|---|---|---|---|---|",
    ])

    for receipt in receipts:
        lines.append(markdown_table_row([
            receipt["receipt_id"],
            receipt["theorem"],
            receipt["role"],
            receipt["transition"],
            receipt["decision"],
            "; ".join(receipt["basis"]),
        ]))

    lines.extend([
        "",
        "## Interpretation",
        "",
        "Stage 3 extends continuation testing beyond role comparison into compound and temporal admissibility.",
        "",
        "The new receipt set demonstrates that local admissibility does not compose automatically into global admissibility. A transition may fail closed because the composite consequence mass exceeds legitimacy capacity, because state drift occurred at commit time, because the inference window collapsed, because recoverability fell below the required floor, or because replay was incorrectly treated as reversal.",
        "",
        "This supports the next formal move from data-role continuation toward system-coherent boundary dynamics and coupled admissibility fields.",
        "",
    ])

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
        "stage": "stage_3_compound_continuation",
        "receipt_count": len(receipts),
        "success": success,
        "receipts_path": str(RECEIPTS_PATH),
        "report_path": str(REPORT_PATH),
    }, indent=2, sort_keys=True))

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
