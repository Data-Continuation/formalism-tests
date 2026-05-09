"""
Executable tests for the StegVerse AI Block seed classifier.

Run:
    python test_ai_block_classifier.py
"""

from ai_block_classifier import (
    FAIL_CLOSED,
    Transition,
    burden_for,
    classify_transition,
    compute_d_ai,
    compute_icc,
    hard_gate,
    is_monotonic,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def assert_true(value, label):
    if not value:
        raise AssertionError(label)


def test_classification():
    cases = {
        "summarize a document": "AI-INF-P2-I",
        "draft markdown": "AI-GEN-P3-R",
        "generate workflow file": "AI-GEN:WORKFLOW-P5-G/R",
        "send email through a tool": "AI-TOOL:EMAIL-P6-Q",
        "mutate GitHub file": "AI-TOOL:GITHUB-P5-R",
        "deploy generated code": "AI-AGENT:DEP-P6-V/H",
        "alter policy rules": "AI-REC:POLICY-P5-G",
        "rank people for opportunity": "AI-RANK:PERS-P7-Q",
        "modify memory": "AI-MEM-P8-G/R",
    }

    for description, expected in cases.items():
        assert_equal(
            classify_transition(description),
            expected,
            f"classify {description}",
        )


def test_monotonic_burden():
    sequence = [
        "AI-INF-P2-I",
        "AI-GEN-P3-R",
        "AI-DEC-P4-G",
        "AI-TOOL:GITHUB-P5-R",
        "AI-AGENT:DEP-P6-V/H",
        "AI-REC:POLICY-P5-G",
    ]
    assert_true(is_monotonic(sequence), "burden should rise monotonically")


def test_modifiers_raise_burden():
    base = burden_for("AI-GEN-P3-R")
    for code in [
        "AI-RANK:PERS-P7-Q",
        "AI-LIFE-P7-L/H",
        "AI-FIN-P7-Q/H",
        "AI-CRED-P5-G/H",
        "AI-REC:POLICY-P5-G",
    ]:
        assert_true(burden_for(code) > base, f"{code} should exceed base generation burden")


def test_hard_gate_target_binding():
    result = hard_gate(
        Transition(
            description="write file",
            target_intended="repo-a/file.md",
            target_selected="repo-b/file.md",
            target_committed="repo-b/file.md",
        )
    )
    assert_equal(result, FAIL_CLOSED, "target mismatch must fail closed")


def test_hard_gate_authority():
    result = hard_gate(
        Transition(
            description="execute tool",
            authority_delegated=0.4,
            authority_executed=0.7,
        )
    )
    assert_equal(result, FAIL_CLOSED, "authority overflow must fail closed")


def test_hard_gate_context():
    result = hard_gate(
        Transition(
            description="mutate GitHub file",
            context_sufficiency=0.2,
            context_min=0.6,
        )
    )
    assert_equal(result, FAIL_CLOSED, "missing context must fail closed")


def test_hard_gate_receipt():
    result = hard_gate(
        Transition(
            description="send email",
            receipt_sufficiency=0.2,
            receipt_min=0.8,
        )
    )
    assert_equal(result, FAIL_CLOSED, "insufficient receipt must fail closed")


def test_icc_range_and_growth():
    low = compute_icc(
        inference_role=0.2,
        tool_binding=0.0,
        authority_scope=0.0,
        externalization=0.0,
        persistence=0.0,
        recursion=0.0,
    )
    high = compute_icc(
        inference_role=1.0,
        tool_binding=1.0,
        authority_scope=1.0,
        externalization=1.0,
        persistence=1.0,
        recursion=1.0,
    )
    assert_true(0.0 <= low <= 1.0, "low ICC should be normalized")
    assert_true(0.0 <= high <= 1.0, "high ICC should be normalized")
    assert_true(high > low, "ICC should rise with coupling factors")


def test_d_ai_governance_reduces_determinacy():
    weak_governance = compute_d_ai(
        agency=1.0,
        tool_access=1.0,
        authority=1.0,
        persistence=1.0,
        recursion=1.0,
        externalization=1.0,
        governance=0.2,
        control=0.2,
        trust=0.2,
        receipt=0.2,
        recoverability=0.2,
    )
    strong_governance = compute_d_ai(
        agency=1.0,
        tool_access=1.0,
        authority=1.0,
        persistence=1.0,
        recursion=1.0,
        externalization=1.0,
        governance=0.9,
        control=0.9,
        trust=0.9,
        receipt=0.9,
        recoverability=0.9,
    )
    assert_true(
        weak_governance > strong_governance,
        "stronger governance terms should reduce D_AI",
    )


def run_all():
    test_classification()
    test_monotonic_burden()
    test_modifiers_raise_burden()
    test_hard_gate_target_binding()
    test_hard_gate_authority()
    test_hard_gate_context()
    test_hard_gate_receipt()
    test_icc_range_and_growth()
    test_d_ai_governance_reduces_determinacy()
    print("PASS: AI Block formalism seed tests")


if __name__ == "__main__":
    run_all()
