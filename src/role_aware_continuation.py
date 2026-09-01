from __future__ import annotations

from typing import Any, Dict, Iterable

from outcome_vocabulary import CANONICAL_OUTCOMES, project_to_root_gate, project_to_transition_table

INITIAL_ROLES = {
    "context", "informational_note", "evidence", "recommendation", "instruction",
    "authorization_basis", "command", "policy_basis", "identity_claim", "custody_basis",
    "transaction_basis", "physical_control_signal",
}

REQUIRED_ROLE_ESCALATION_BLOCKS = (
    "role_change_declared",
    "transition_class_declared",
    "authority_current",
    "evidence_fresh",
    "scope_valid",
    "trust_basis_current",
    "risk_basis_current",
    "receipt_required",
    "fail_closed_if_missing",
)

TRUE_STATES = {True, "true", "pass", "passed", "current", "valid", "present", "yes"}
UNKNOWN_STATES = {None, "unknown", "unset", "missing"}
STALE_STATES = {"stale", "expired", "outdated"}

def _state(value: Any) -> str:
    if value in TRUE_STATES:
        return "PASS"
    if value in STALE_STATES:
        return "STALE"
    if value in UNKNOWN_STATES:
        return "UNKNOWN"
    if value is False or str(value).strip().lower() in {"false", "fail", "failed", "invalid", "absent", "no"}:
        return "FAIL"
    return "UNKNOWN"

def evaluate_role_blocks(block_results: Dict[str, Any]) -> Dict[str, str]:
    return {name: _state(block_results.get(name)) for name in REQUIRED_ROLE_ESCALATION_BLOCKS}

def decide_continuation(
    *,
    role: str,
    transition_class: str,
    consequence_mass: float,
    legitimacy_capacity: float,
    block_results: Dict[str, Any],
    signoff_required: bool = False,
    redirect_available: bool = False,
    escalation_available: bool = False,
) -> Dict[str, Any]:
    role = str(role or "").strip()
    transition_class = str(transition_class or "").strip()
    evaluated = evaluate_role_blocks(block_results)
    basis = []

    if not role or role not in INITIAL_ROLES:
        decision = "FAIL_CLOSED"
        basis.append("role is missing or unknown")
    elif not transition_class:
        decision = "FAIL_CLOSED"
        basis.append("transition class is missing")
    elif any(v in {"UNKNOWN", "STALE"} for v in evaluated.values()):
        decision = "FAIL_CLOSED"
        basis.append("required role-escalation basis is missing, unknown, or stale")
    elif any(v == "FAIL" for v in evaluated.values()):
        if redirect_available:
            decision = "REDIRECT"
            basis.append("required role-escalation block failed and a governed redirect exists")
        elif escalation_available:
            decision = "ESCALATE"
            basis.append("required role-escalation block failed and governed escalation is required")
        else:
            decision = "DENY"
            basis.append("required role-escalation block failed")
    elif consequence_mass > legitimacy_capacity:
        if escalation_available:
            decision = "ESCALATE"
            basis.append("consequence mass exceeds current legitimacy capacity")
        else:
            decision = "DENY"
            basis.append("consequence mass exceeds legitimacy capacity")
    elif signoff_required:
        decision = "ALLOW_WITH_SIGNOFF"
        basis.append("all required blocks pass but explicit signoff remains required")
    else:
        decision = "ALLOW"
        basis.append("role, transition class, capacity, and required blocks resolve at commit")

    assert decision in CANONICAL_OUTCOMES
    return {
        "role": role,
        "transition_class": transition_class,
        "consequence_mass": float(consequence_mass),
        "legitimacy_capacity": float(legitimacy_capacity),
        "capacity_gap": float(legitimacy_capacity) - float(consequence_mass),
        "required_blocks": list(REQUIRED_ROLE_ESCALATION_BLOCKS),
        "block_results": evaluated,
        "decision": decision,
        "projections": {
            "root_gate": project_to_root_gate(decision),
            "transition_table": project_to_transition_table(decision),
        },
        "basis": basis,
    }
