#!/usr/bin/env python3
"""Stage 6 Unified Gate test runner.

This runner intentionally uses only the Python standard library so it can run
inside the existing Data Continuation Tests workflow without installing pytest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_PATH = Path("tests/fixtures/stage6_candidates.json")


def fail(message: str) -> None:
    raise AssertionError(message)


def approx_equal(left: float, right: float, tolerance: float = 1e-9) -> bool:
    return abs(left - right) <= tolerance


def load_candidates() -> list[dict[str, Any]]:
    if not FIXTURE_PATH.exists():
        fail(f"missing fixture: {FIXTURE_PATH}")

    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        fail("fixture root must be an object")

    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        fail("fixture must contain a candidates list")

    if len(candidates) != 10:
        fail(f"expected 10 Stage 6 candidates, found {len(candidates)}")

    return candidates


def candidate_decision(candidate: dict[str, Any]) -> str:
    return (
        candidate.get("expected_decision")
        or candidate.get("candidate_expected_outcome")
        or candidate.get("verified_decision")
        or ""
    )


def family_outcomes(candidate: dict[str, Any]) -> list[str]:
    outcomes = candidate.get("family_allowed_outcomes")
    if outcomes is None:
        outcomes = candidate.get("allowed_outcomes")
    if not isinstance(outcomes, list):
        fail(f"{candidate.get('transition_id')}: allowed/family outcomes must be a list")
    return outcomes


def recompute_core_decision(candidate: dict[str, Any]) -> str:
    iw = candidate.get("iw_containment", {})
    re_bound = candidate.get("re_bound", {})

    if iw.get("contained") is not True:
        return "FAIL_CLOSED"
    if re_bound.get("within_bound") is not True:
        return "FAIL_CLOSED"

    block = candidate.get("ai_block")
    if isinstance(block, dict) and block.get("scope_respected") is False:
        return "FAIL_CLOSED"

    finco = candidate.get("finco_chain")
    if isinstance(finco, dict):
        if finco.get("chain_intact") is False:
            return "FAIL_CLOSED"
        if finco.get("recoverability_delta", 1.0) < finco.get("recoverability_minimum", 0.0):
            return "FAIL_CLOSED"
        if finco.get("creates_entitlement") is True:
            return "FAIL_CLOSED"

    recoverability_score = candidate.get("recoverability_score")
    recoverability_floor = candidate.get("recoverability_floor")
    if recoverability_score is not None and recoverability_floor is not None:
        if recoverability_score < recoverability_floor:
            return "FAIL_CLOSED"

    if candidate.get("convergence_failure") is True:
        if candidate.get("recoverability_score", 0.0) >= candidate.get("recoverability_floor", 1.0):
            return "RESET_BOUNDARY"
        return "FAIL_CLOSED"

    if candidate.get("coherence_failure") is True or candidate.get("purpose_convergence_test") == "fail":
        if (
            candidate.get("recoverability_score", 0.0) >= candidate.get("recoverability_floor", 1.0)
            and candidate.get("convergence_score", 0.0) >= candidate.get("convergence_minimum", 1.0)
        ):
            return "EVOLVE_BOUNDARY"
        return "FAIL_CLOSED"

    return "ALLOW"


def run_candidate_checks(candidate: dict[str, Any]) -> int:
    transition_id = candidate.get("transition_id", "<missing transition_id>")
    checks = 0

    if not transition_id or transition_id == "<missing transition_id>":
        fail("candidate missing transition_id")
    checks += 1

    for key in [
        "transition_name",
        "transition_family",
        "theorem_basis",
        "role",
        "periodic_table_coordinates",
        "iw_containment",
        "re_bound",
        "component_gate_results",
        "basis",
    ]:
        if key not in candidate:
            fail(f"{transition_id}: missing required key {key}")
        checks += 1

    decision = candidate_decision(candidate)
    if decision not in {"ALLOW", "FAIL_CLOSED", "RESET_BOUNDARY", "EVOLVE_BOUNDARY", "DENY", "ALLOW_WITH_SIGNOFF"}:
        fail(f"{transition_id}: invalid expected decision {decision!r}")
    checks += 1

    outcomes = family_outcomes(candidate)
    if decision not in outcomes:
        fail(f"{transition_id}: expected decision {decision} not in allowed outcomes {outcomes}")
    checks += 1

    iw = candidate["iw_containment"]
    window = iw.get("inference_window")
    a_total = iw.get("a_total")
    if not (isinstance(window, list) and len(window) == 2):
        fail(f"{transition_id}: inference_window must be a two-value list")
    if not (isinstance(a_total, list) and len(a_total) == 2):
        fail(f"{transition_id}: a_total must be a two-value list")
    checks += 2

    width = window[1] - window[0]
    if "iw_width" in iw and not approx_equal(width, float(iw["iw_width"])):
        fail(f"{transition_id}: iw_width mismatch")
    checks += 1

    contained_math = window[0] >= a_total[0] and window[1] <= a_total[1]
    if contained_math != bool(iw.get("contained")):
        fail(f"{transition_id}: IW containment flag does not match interval math")
    checks += 1

    if not contained_math and "breach_margin" in iw:
        breach_margin = max(a_total[0] - window[0], 0.0) + max(window[1] - a_total[1], 0.0)
        if not approx_equal(breach_margin, float(iw["breach_margin"])):
            fail(f"{transition_id}: breach_margin mismatch")
    checks += 1

    if contained_math and decision == "FAIL_CLOSED":
        # Allowed when some other required gate fails.
        has_other_failure = (
            candidate["re_bound"].get("within_bound") is False
            or candidate.get("recoverability_score", 1.0) < candidate.get("recoverability_floor", 0.0)
            or (isinstance(candidate.get("ai_block"), dict) and candidate["ai_block"].get("scope_respected") is False)
            or (isinstance(candidate.get("finco_chain"), dict) and candidate["finco_chain"].get("chain_intact") is False)
        )
        if not has_other_failure:
            fail(f"{transition_id}: contained IW with FAIL_CLOSED requires another gate failure")
    checks += 1

    re_bound = candidate["re_bound"]
    if re_bound.get("within_bound") != (re_bound.get("re_score") <= re_bound.get("re_max")):
        fail(f"{transition_id}: RE within_bound flag does not match score/max math")
    checks += 1

    if re_bound.get("within_bound") is False and "breach_amount" in re_bound:
        breach_amount = re_bound["re_score"] - re_bound["re_max"]
        if not approx_equal(breach_amount, float(re_bound["breach_amount"])):
            fail(f"{transition_id}: RE breach_amount mismatch")
    checks += 1

    recomputed = recompute_core_decision(candidate)
    if recomputed != decision:
        fail(f"{transition_id}: recomputed decision {recomputed} != expected decision {decision}")
    checks += 1

    if decision == "ALLOW":
        if iw.get("contained") is not True or re_bound.get("within_bound") is not True:
            fail(f"{transition_id}: ALLOW requires IW contained and RE within bound")
    checks += 1

    if decision == "RESET_BOUNDARY":
        if candidate.get("convergence_failure") is not True:
            fail(f"{transition_id}: RESET_BOUNDARY requires convergence_failure")
        if candidate.get("recoverability_score", 0.0) < candidate.get("recoverability_floor", 1.0):
            fail(f"{transition_id}: RESET_BOUNDARY requires recoverability above floor")
    checks += 2

    if decision == "EVOLVE_BOUNDARY":
        if candidate.get("coherence_failure") is not True and candidate.get("purpose_convergence_test") != "fail":
            fail(f"{transition_id}: EVOLVE_BOUNDARY requires coherence or purpose-convergence failure")
        if candidate.get("recoverability_score", 0.0) < candidate.get("recoverability_floor", 1.0):
            fail(f"{transition_id}: EVOLVE_BOUNDARY requires recoverability above floor")
    checks += 2

    components = candidate["component_gate_results"]
    if not isinstance(components, dict):
        fail(f"{transition_id}: component_gate_results must be an object")
    for component in ["AE", "BC", "CHF", "DC", "DaCo", "Triad"]:
        if component not in components:
            fail(f"{transition_id}: missing component gate {component}")
        checks += 1

    return checks


def main() -> int:
    try:
        candidates = load_candidates()
        total_checks = 0
        decision_counts: dict[str, int] = {}

        for candidate in candidates:
            total_checks += run_candidate_checks(candidate)
            decision = candidate_decision(candidate)
            decision_counts[decision] = decision_counts.get(decision, 0) + 1

        report = {
            "schema": "stegverse_stage6_unified_gate_test_report.v1",
            "success": True,
            "fixture": str(FIXTURE_PATH),
            "candidate_count": len(candidates),
            "assertion_count": total_checks,
            "decision_counts": decision_counts,
            "message": f"Stage 6 unified gate checks passed for {len(candidates)} candidates.",
        }

        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        report = {
            "schema": "stegverse_stage6_unified_gate_test_report.v1",
            "success": False,
            "fixture": str(FIXTURE_PATH),
            "error": str(exc),
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
