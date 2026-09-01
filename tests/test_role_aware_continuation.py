from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from outcome_vocabulary import (
    CANONICAL_OUTCOMES,
    project_to_root_gate,
    project_to_transition_table,
)
from role_aware_continuation import (
    REQUIRED_ROLE_ESCALATION_BLOCKS,
    decide_continuation,
)

def passing_blocks():
    return {name: True for name in REQUIRED_ROLE_ESCALATION_BLOCKS}

def test_projection_contract_is_total_and_fail_closed():
    assert set(CANONICAL_OUTCOMES) == {
        "ALLOW", "ALLOW_WITH_SIGNOFF", "DENY", "FAIL_CLOSED", "REDIRECT", "ESCALATE"
    }
    assert project_to_root_gate("ALLOW_WITH_SIGNOFF") == "FAIL_CLOSED"
    assert project_to_root_gate("REDIRECT") == "FAIL_CLOSED"
    assert project_to_transition_table("REDIRECT") == "REPAIR"
    assert project_to_transition_table("ESCALATE") == "QUARANTINE"

def test_role_is_a_real_decision_input():
    result = decide_continuation(
        role="not-a-declared-role",
        transition_class="T-TEST",
        consequence_mass=0.1,
        legitimacy_capacity=0.9,
        block_results=passing_blocks(),
    )
    assert result["decision"] == "FAIL_CLOSED"
    assert "role is missing or unknown" in result["basis"]

def test_missing_unknown_or_stale_block_fails_closed():
    blocks = passing_blocks()
    blocks["authority_current"] = "stale"
    result = decide_continuation(
        role="evidence",
        transition_class="T-TEST",
        consequence_mass=0.1,
        legitimacy_capacity=0.9,
        block_results=blocks,
    )
    assert result["decision"] == "FAIL_CLOSED"

def test_failed_block_can_redirect():
    blocks = passing_blocks()
    blocks["scope_valid"] = False
    result = decide_continuation(
        role="evidence",
        transition_class="T-TEST",
        consequence_mass=0.1,
        legitimacy_capacity=0.9,
        block_results=blocks,
        redirect_available=True,
    )
    assert result["decision"] == "REDIRECT"
    assert result["projections"]["transition_table"] == "REPAIR"

def test_capacity_gap_can_escalate():
    result = decide_continuation(
        role="authorization_basis",
        transition_class="T-AUTH",
        consequence_mass=0.95,
        legitimacy_capacity=0.4,
        block_results=passing_blocks(),
        escalation_available=True,
    )
    assert result["decision"] == "ESCALATE"

def test_signoff_is_distinct_from_allow():
    result = decide_continuation(
        role="instruction",
        transition_class="T-INSTRUCTION",
        consequence_mass=0.2,
        legitimacy_capacity=0.8,
        block_results=passing_blocks(),
        signoff_required=True,
    )
    assert result["decision"] == "ALLOW_WITH_SIGNOFF"
    assert result["projections"]["root_gate"] == "FAIL_CLOSED"


def main():
    test_projection_contract_is_total_and_fail_closed()
    test_role_is_a_real_decision_input()
    test_missing_unknown_or_stale_block_fails_closed()
    test_failed_block_can_redirect()
    test_capacity_gap_can_escalate()
    test_signoff_is_distinct_from_allow()
    print("ROLE_AWARE_CONTINUATION_PASS cases=6")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
