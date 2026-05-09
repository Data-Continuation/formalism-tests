"""
Seed classifier for the StegVerse AI Block formalism.

This is intentionally minimal:
- no external dependencies
- deterministic classification
- explicit fail-closed hard gates
"""

from dataclasses import dataclass
from typing import Dict, Iterable


FAIL_CLOSED = "FAIL-CLOSED"


@dataclass(frozen=True)
class Transition:
    description: str
    target_intended: str = ""
    target_selected: str = ""
    target_committed: str = ""
    authority_delegated: float = 1.0
    authority_executed: float = 0.0
    context_sufficiency: float = 1.0
    context_min: float = 0.5
    receipt_sufficiency: float = 1.0
    receipt_min: float = 0.5


SEED_BURDENS: Dict[str, float] = {
    "AI-INF-P2-I": 0.20,
    "AI-GEN-P3-R": 0.32,
    "AI-DEC-P4-G": 0.46,
    "AI-GEN:CFG-P5-G/R": 0.58,
    "AI-GEN:WORKFLOW-P5-G/R": 0.66,
    "AI-TOOL:GITHUB-P5-R": 0.70,
    "AI-TOOL:EMAIL-P6-Q": 0.72,
    "AI-AGENT:DEP-P6-V/H": 0.84,
    "AI-RANK:PERS-P7-Q": 0.86,
    "AI-CRED-P5-G/H": 0.88,
    "AI-FIN-P7-Q/H": 0.90,
    "AI-REC:POLICY-P5-G": 0.92,
    "AI-PERS-P7-Q/R": 0.94,
    "AI-MEM-P8-G/R": 0.94,
    "AI-LIFE-P7-L/H": 0.96,
}


def classify_transition(description: str) -> str:
    """Classify an AI-mediated transition into a seed transition element."""
    text = description.lower()

    if any(term in text for term in ["memory", "remember", "forget"]):
        return "AI-MEM-P8-G/R"
    if any(term in text for term in ["policy", "governance rule", "admissibility rule"]):
        return "AI-REC:POLICY-P5-G"
    if any(term in text for term in ["life", "medical", "injury", "treatment", "survival"]):
        return "AI-LIFE-P7-L/H"
    if any(term in text for term in ["person", "people", "candidate", "applicant", "opportunity", "rank"]):
        return "AI-RANK:PERS-P7-Q"
    if any(term in text for term in ["financial", "payment", "transfer funds", "wallet", "settlement"]):
        return "AI-FIN-P7-Q/H"
    if any(term in text for term in ["credential", "secret", "token", "key", "password"]):
        return "AI-CRED-P5-G/H"
    if any(term in text for term in ["deploy", "deployment", "production"]):
        return "AI-AGENT:DEP-P6-V/H"
    if any(term in text for term in ["github", "commit", "mutate file", "write file"]):
        return "AI-TOOL:GITHUB-P5-R"
    if any(term in text for term in ["send email", "email through a tool"]):
        return "AI-TOOL:EMAIL-P6-Q"
    if any(term in text for term in ["workflow", "github actions", "action yaml"]):
        return "AI-GEN:WORKFLOW-P5-G/R"
    if any(term in text for term in ["config", "configuration"]):
        return "AI-GEN:CFG-P5-G/R"
    if any(term in text for term in ["decide", "select action", "choose action"]):
        return "AI-DEC-P4-G"
    if any(term in text for term in ["draft", "markdown", "generate artifact", "write document"]):
        return "AI-GEN-P3-R"
    if any(term in text for term in ["summarize", "classify", "infer", "extract"]):
        return "AI-INF-P2-I"

    return "AI-INF-P2-I"


def burden_for(code: str) -> float:
    return SEED_BURDENS[code]


def compute_icc(
    inference_role: float,
    tool_binding: float,
    authority_scope: float,
    externalization: float,
    persistence: float,
    recursion: float,
    icc_max: float = 32.0,
) -> float:
    """Compute normalized Inference-Consequence Coupling."""
    raw = (
        inference_role
        * (1 + tool_binding)
        * (1 + authority_scope)
        * (1 + externalization)
        * (1 + persistence)
        * (1 + recursion)
    )
    return min(max(raw / icc_max, 0.0), 1.0)


def compute_d_ai(
    agency: float,
    tool_access: float,
    authority: float,
    persistence: float,
    recursion: float,
    externalization: float,
    governance: float,
    control: float,
    trust: float,
    receipt: float,
    recoverability: float,
) -> float:
    """Compute artificial consequence-determinacy pressure."""
    denominator = governance * control * trust * receipt * recoverability
    if denominator <= 0:
        return float("inf")
    return (
        agency
        * tool_access
        * authority
        * persistence
        * recursion
        * externalization
    ) / denominator


def hard_gate(transition: Transition) -> str:
    """Return ALLOW if hard gates pass, otherwise FAIL-CLOSED."""
    targets = [
        transition.target_intended,
        transition.target_selected,
        transition.target_committed,
    ]
    if any(targets) and len(set(targets)) != 1:
        return FAIL_CLOSED

    if transition.authority_executed > transition.authority_delegated:
        return FAIL_CLOSED

    if transition.context_sufficiency < transition.context_min:
        return FAIL_CLOSED

    if transition.receipt_sufficiency < transition.receipt_min:
        return FAIL_CLOSED

    return "ALLOW"


def is_monotonic(codes: Iterable[str]) -> bool:
    values = [burden_for(code) for code in codes]
    return all(left < right for left, right in zip(values, values[1:]))
