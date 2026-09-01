from __future__ import annotations

CANONICAL_OUTCOMES = (
    "ALLOW",
    "ALLOW_WITH_SIGNOFF",
    "DENY",
    "FAIL_CLOSED",
    "REDIRECT",
    "ESCALATE",
)

ROOT_GATE_OUTCOMES = ("ALLOW", "DENY", "FAIL_CLOSED")
TRANSITION_TABLE_OUTCOMES = ("ALLOW", "DENY", "FAIL_CLOSED", "QUARANTINE", "REPAIR")

def validate_canonical_outcome(outcome: str) -> str:
    if outcome not in CANONICAL_OUTCOMES:
        raise ValueError(f"unknown canonical continuation outcome: {outcome}")
    return outcome

def project_to_root_gate(outcome: str) -> str:
    outcome = validate_canonical_outcome(outcome)
    return {
        "ALLOW": "ALLOW",
        "ALLOW_WITH_SIGNOFF": "FAIL_CLOSED",
        "DENY": "DENY",
        "FAIL_CLOSED": "FAIL_CLOSED",
        "REDIRECT": "FAIL_CLOSED",
        "ESCALATE": "FAIL_CLOSED",
    }[outcome]

def project_to_transition_table(outcome: str) -> str:
    outcome = validate_canonical_outcome(outcome)
    return {
        "ALLOW": "ALLOW",
        "ALLOW_WITH_SIGNOFF": "QUARANTINE",
        "DENY": "DENY",
        "FAIL_CLOSED": "FAIL_CLOSED",
        "REDIRECT": "REPAIR",
        "ESCALATE": "QUARANTINE",
    }[outcome]
