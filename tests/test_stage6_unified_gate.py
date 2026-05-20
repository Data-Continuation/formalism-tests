"""Stage 6 complete candidate tests for the Admissible Existence Unified Gate.

Repo placement:
    tests/test_stage6_unified_gate.py

Fixture placement:
    tests/fixtures/stage6_candidates.json

Core-lite rule:
    This file adds no workflows and does not require workflow changes.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "stage6_candidates.json"
TERMINAL_FAIL_DECISION = "FAIL_CLOSED"
VALID_DECISIONS = {"ALLOW", "FAIL_CLOSED", "RESET_BOUNDARY", "EVOLVE_BOUNDARY"}
EXPECTED_CANDIDATE_IDS = {
    "T-AE-UNIFIED-ALLOW-001",
    "T-AE-UNIFIED-IW-BREACH-001",
    "T-AE-UNIFIED-RE-BREACH-001",
    "T-AE-UNIFIED-DUAL-BREACH-001",
    "T-AE-UNIFIED-RESET-001",
    "T-AE-UNIFIED-EVOLVE-001",
    "T-AE-UNIFIED-AI-BLOCK-ALLOW-001",
    "T-AE-UNIFIED-AI-BLOCK-ESCAPE-001",
    "T-AE-UNIFIED-FINCO-CHAIN-001",
    "T-AE-UNIFIED-FINCO-CHAIN-BREAK-001",
}


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture(scope="module")
def fixture() -> dict[str, Any]:
    return load_fixture()


@pytest.fixture(scope="module")
def candidates(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return fixture["candidates"]


def candidate_ids(candidates: list[dict[str, Any]]) -> list[str]:
    return [candidate["transition_id"] for candidate in candidates]


def candidates_by_id(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {candidate["transition_id"]: candidate for candidate in candidates}


def is_iw_contained(candidate: dict[str, Any]) -> bool:
    iw = candidate["iw_containment"]
    iw_min, iw_max = iw["inference_window"]
    a_min, a_max = iw["a_total"]
    return a_min <= iw_min and iw_max <= a_max


def is_re_within_bound(candidate: dict[str, Any]) -> bool:
    re_bound = candidate["re_bound"]
    return re_bound["re_score"] <= re_bound["re_max"]


def ai_block_fails(candidate: dict[str, Any]) -> bool:
    block = candidate.get("ai_block")
    if not block:
        return False
    return (
        block.get("scope_violation") is True
        or block.get("scope_respected") is not True
        or block.get("all_elements_validated") is not True
    )


def finco_chain_fails(candidate: dict[str, Any]) -> bool:
    chain = candidate.get("finco_chain")
    if not chain:
        return False

    required_true = (
        "consent_receipt_valid",
        "access_receipt_valid",
        "use_receipt_valid",
        "compensation_rule_defined",
        "revocation_rule_defined",
        "evidence_only",
        "chain_intact",
    )
    if any(chain.get(key) is not True for key in required_true):
        return True
    if chain.get("creates_entitlement") is True:
        return True
    return chain.get("recoverability_delta", 0.0) < chain.get("recoverability_minimum", 0.0)


def compute_stage6_decision(candidate: dict[str, Any]) -> str:
    if not is_iw_contained(candidate):
        return TERMINAL_FAIL_DECISION
    if not is_re_within_bound(candidate):
        return TERMINAL_FAIL_DECISION
    if candidate.get("recoverability_score", 0.0) < candidate.get("recoverability_floor", 0.0):
        return TERMINAL_FAIL_DECISION
    if ai_block_fails(candidate):
        return TERMINAL_FAIL_DECISION
    if finco_chain_fails(candidate):
        return TERMINAL_FAIL_DECISION
    if candidate.get("convergence_failure") is True:
        return "RESET_BOUNDARY"
    if candidate.get("coherence_failure") is True:
        return "EVOLVE_BOUNDARY"
    return "ALLOW"


def assert_close(actual: float, expected: float) -> None:
    assert math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-9)


# ---------------------------------------------------------------------------
# Fixture-level contract tests.
# ---------------------------------------------------------------------------


def test_fixture_schema_identity(fixture: dict[str, Any]) -> None:
    assert fixture["schema"] in {"stegverse_stage6_candidates.v1", "stegverse_stage6_candidates.v1.1"}
    assert fixture["stage"] == "Stage 6"
    assert fixture["theorem_basis"] == "Admissible Existence Unified Gate"
    assert fixture["gate_formula"] == "ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max"


def test_fixture_component_coverage(fixture: dict[str, Any]) -> None:
    assert fixture["components_covered"] == ["AE", "BC", "CHF", "DC", "DaCo", "Triad"]
    assert fixture["new_decisions"] == ["RESET_BOUNDARY", "EVOLVE_BOUNDARY"]


def test_fixture_contains_completed_stage6_candidate_set(candidates: list[dict[str, Any]]) -> None:
    assert set(candidate_ids(candidates)) == EXPECTED_CANDIDATE_IDS
    assert len(candidates) == len(EXPECTED_CANDIDATE_IDS)


def test_candidate_ids_are_unique(candidates: list[dict[str, Any]]) -> None:
    ids = candidate_ids(candidates)
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_candidate_has_required_stage6_fields(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    required_fields = {
        "transition_id",
        "transition_name",
        "transition_family",
        "theorem_basis",
        "role",
        "periodic_table_coordinates",
        "iw_containment",
        "re_bound",
        "consequence_mass",
        "legitimacy_capacity_required",
        "recoverability_floor",
        "recoverability_score",
        "commit_time_state_required",
        "replay_semantics",
        "boundary_behavior",
        "multi_body_coupling_class",
        "component_gate_results",
        "basis",
        "family_allowed_outcomes",
        "candidate_expected_outcome",
        "expected_decision",
        "validated_decision",
        "validation_status",
    }
    assert required_fields.issubset(candidate.keys())


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_candidate_result_fields_are_fixture_expectations_not_validator_output(
    transition_id: str, candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert candidate["expected_decision"] in VALID_DECISIONS
    assert candidate["candidate_expected_outcome"] == candidate["expected_decision"]
    assert candidate["expected_decision"] in set(candidate["family_allowed_outcomes"])
    assert candidate["validated_decision"] is None
    assert candidate["validation_status"] is None


# ---------------------------------------------------------------------------
# Per-candidate gate-decision tests.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("transition_id", "expected_decision"),
    [
        ("T-AE-UNIFIED-ALLOW-001", "ALLOW"),
        ("T-AE-UNIFIED-IW-BREACH-001", "FAIL_CLOSED"),
        ("T-AE-UNIFIED-RE-BREACH-001", "FAIL_CLOSED"),
        ("T-AE-UNIFIED-DUAL-BREACH-001", "FAIL_CLOSED"),
        ("T-AE-UNIFIED-RESET-001", "RESET_BOUNDARY"),
        ("T-AE-UNIFIED-EVOLVE-001", "EVOLVE_BOUNDARY"),
        ("T-AE-UNIFIED-AI-BLOCK-ALLOW-001", "ALLOW"),
        ("T-AE-UNIFIED-AI-BLOCK-ESCAPE-001", "FAIL_CLOSED"),
        ("T-AE-UNIFIED-FINCO-CHAIN-001", "ALLOW"),
        ("T-AE-UNIFIED-FINCO-CHAIN-BREAK-001", "FAIL_CLOSED"),
    ],
)
def test_candidate_expected_decision_matches_computed_stage6_decision(
    transition_id: str, expected_decision: str, candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert candidate["expected_decision"] == expected_decision
    assert compute_stage6_decision(candidate) == expected_decision


# ---------------------------------------------------------------------------
# IW containment, IW width, and IW breach-margin tests.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_iw_containment_flag_matches_computed_containment(
    transition_id: str, candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert candidate["iw_containment"]["contained"] is is_iw_contained(candidate)


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_iw_width_matches_inference_window_bounds(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    iw = candidates_by_id(candidates)[transition_id]["iw_containment"]
    iw_min, iw_max = iw["inference_window"]
    assert_close(iw["iw_width"], iw_max - iw_min)


@pytest.mark.parametrize(
    ("transition_id", "expected_breach_margin"),
    [
        ("T-AE-UNIFIED-IW-BREACH-001", 0.40),
        ("T-AE-UNIFIED-DUAL-BREACH-001", 0.80),
        ("T-AE-UNIFIED-AI-BLOCK-ESCAPE-001", 0.60),
    ],
)
def test_iw_breach_margin_matches_excess_over_a_total(
    transition_id: str, expected_breach_margin: float, candidates: list[dict[str, Any]]
) -> None:
    iw = candidates_by_id(candidates)[transition_id]["iw_containment"]
    _, iw_max = iw["inference_window"]
    _, a_max = iw["a_total"]
    assert_close(iw["breach_margin"], iw_max - a_max)
    assert_close(iw["breach_margin"], expected_breach_margin)


# ---------------------------------------------------------------------------
# Reverse-entropy bound tests.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_re_bound_flag_matches_computed_bound(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert candidate["re_bound"]["within_bound"] is is_re_within_bound(candidate)


@pytest.mark.parametrize(
    ("transition_id", "expected_breach_amount"),
    [
        ("T-AE-UNIFIED-RE-BREACH-001", 0.23),
        ("T-AE-UNIFIED-DUAL-BREACH-001", 0.41),
        ("T-AE-UNIFIED-AI-BLOCK-ESCAPE-001", 0.32),
    ],
)
def test_re_breach_amount_matches_excess_over_re_max(
    transition_id: str, expected_breach_amount: float, candidates: list[dict[str, Any]]
) -> None:
    re_bound = candidates_by_id(candidates)[transition_id]["re_bound"]
    assert_close(re_bound["breach_amount"], re_bound["re_score"] - re_bound["re_max"])
    assert_close(re_bound["breach_amount"], expected_breach_amount)


# ---------------------------------------------------------------------------
# Decision-routing tests.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "transition_id",
    [
        "T-AE-UNIFIED-IW-BREACH-001",
        "T-AE-UNIFIED-DUAL-BREACH-001",
        "T-AE-UNIFIED-AI-BLOCK-ESCAPE-001",
    ],
)
def test_iw_failure_routes_to_fail_closed(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert is_iw_contained(candidate) is False
    assert compute_stage6_decision(candidate) == "FAIL_CLOSED"


@pytest.mark.parametrize(
    "transition_id",
    [
        "T-AE-UNIFIED-RE-BREACH-001",
        "T-AE-UNIFIED-DUAL-BREACH-001",
        "T-AE-UNIFIED-AI-BLOCK-ESCAPE-001",
    ],
)
def test_re_failure_routes_to_fail_closed(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    assert is_re_within_bound(candidate) is False
    assert compute_stage6_decision(candidate) == "FAIL_CLOSED"


def test_reset_boundary_requires_contained_iw_bounded_re_recoverability_and_non_convergence(
    candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-RESET-001"]
    assert is_iw_contained(candidate) is True
    assert is_re_within_bound(candidate) is True
    assert candidate["recoverability_score"] >= candidate["recoverability_floor"]
    assert candidate["convergence_failure"] is True
    assert candidate["convergence_score"] < candidate["convergence_minimum"]
    assert compute_stage6_decision(candidate) == "RESET_BOUNDARY"


def test_evolve_boundary_requires_contained_iw_bounded_re_recoverability_convergence_and_coherence_failure(
    candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-EVOLVE-001"]
    assert is_iw_contained(candidate) is True
    assert is_re_within_bound(candidate) is True
    assert candidate["recoverability_score"] >= candidate["recoverability_floor"]
    assert candidate["convergence_failure"] is False
    assert candidate["convergence_score"] >= candidate["convergence_minimum"]
    assert candidate["coherence_failure"] is True
    assert candidate["coherence_score"] < candidate["coherence_minimum"]
    assert candidate["purpose_convergence_test"] == "fail"
    assert compute_stage6_decision(candidate) == "EVOLVE_BOUNDARY"


# ---------------------------------------------------------------------------
# Domain-specific contract tests.
# ---------------------------------------------------------------------------


def test_ai_block_allow_requires_validated_elements_and_respected_scope(candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-AI-BLOCK-ALLOW-001"]
    block = candidate["ai_block"]
    assert block["all_elements_validated"] is True
    assert block["scope_respected"] is True
    assert "attempted_scope" not in block
    assert ai_block_fails(candidate) is False
    assert compute_stage6_decision(candidate) == "ALLOW"


def test_ai_block_escape_fails_for_unauthorized_capability_acquisition(candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-AI-BLOCK-ESCAPE-001"]
    block = candidate["ai_block"]
    assert block["scope_violation"] is True
    assert block["scope_respected"] is False
    assert block["violation_type"] == "unauthorized_capability_acquisition"
    assert "workflow:create" in block["attempted_scope"]
    assert "credential:acquire" in block["attempted_scope"]
    assert "sandbox:escape" in block["attempted_scope"]
    assert ai_block_fails(candidate) is True
    assert compute_stage6_decision(candidate) == "FAIL_CLOSED"


def test_finco_chain_allow_requires_intact_evidence_only_non_entitlement_chain(
    candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-FINCO-CHAIN-001"]
    chain = candidate["finco_chain"]
    assert chain["consent_receipt_valid"] is True
    assert chain["access_receipt_valid"] is True
    assert chain["use_receipt_valid"] is True
    assert chain["compensation_rule_defined"] is True
    assert chain["revocation_rule_defined"] is True
    assert chain["evidence_only"] is True
    assert chain["creates_entitlement"] is False
    assert chain["chain_intact"] is True
    assert chain["recoverability_delta"] >= chain["recoverability_minimum"]
    assert finco_chain_fails(candidate) is False
    assert compute_stage6_decision(candidate) == "ALLOW"


def test_finco_chain_break_fails_for_missing_consent_compensation_and_unauthorized_entitlement(
    candidates: list[dict[str, Any]]
) -> None:
    candidate = candidates_by_id(candidates)["T-AE-UNIFIED-FINCO-CHAIN-BREAK-001"]
    chain = candidate["finco_chain"]
    assert chain["consent_receipt_valid"] is False
    assert chain["access_receipt_valid"] is False
    assert chain["compensation_rule_defined"] is False
    assert chain["revocation_rule_defined"] is False
    assert chain["evidence_only"] is False
    assert chain["creates_entitlement"] is True
    assert chain["chain_intact"] is False
    assert chain["recoverability_delta"] < chain["recoverability_minimum"]
    assert finco_chain_fails(candidate) is True
    assert compute_stage6_decision(candidate) == "FAIL_CLOSED"


# ---------------------------------------------------------------------------
# Component gate consistency tests.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("transition_id", sorted(EXPECTED_CANDIDATE_IDS))
def test_component_gate_results_only_use_valid_decisions(transition_id: str, candidates: list[dict[str, Any]]) -> None:
    candidate = candidates_by_id(candidates)[transition_id]
    for component, decision in candidate["component_gate_results"].items():
        assert component in {"AE", "BC", "CHF", "DC", "DaCo", "Triad"}
        assert decision in VALID_DECISIONS


@pytest.mark.parametrize(
    "transition_id",
    [
        "T-AE-UNIFIED-DUAL-BREACH-001",
        "T-AE-UNIFIED-AI-BLOCK-ESCAPE-001",
    ],
)
def test_total_component_failure_cases_have_only_fail_closed_component_results(
    transition_id: str, candidates: list[dict[str, Any]]
) -> None:
    component_results = candidates_by_id(candidates)[transition_id]["component_gate_results"]
    assert set(component_results.values()) == {"FAIL_CLOSED"}
