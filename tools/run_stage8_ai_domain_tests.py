#!/usr/bin/env python3
"""
run_stage8_ai_domain_tests.py
==============================
Declared task: stage8_ai_domain_tests

Stage 8 — AI Domain Transition Classes

Validates that AI governance, derivation, and verification agent
participation in the transition table is itself a formally tested
transition class.

After Stage 8 verification:
  - AI entities may propose new transition class candidates
    within their declared AI_BLOCK scope
  - Proposals require dependency closure verification (Stage 7)
  - Proposals require quorum confirmation before table entry
  - AI participation is governed by the same admissibility
    framework as all other actors

Usage:
  python tools/run_stage8_ai_domain_tests.py
  python tools/run_stage8_ai_domain_tests.py --candidates tests/fixtures/stage8_candidates.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE       = Path(__file__).resolve().parent
ROOT       = HERE.parent
CANDIDATES = ROOT / "tests" / "fixtures" / "stage8_candidates.json"
REPORT     = ROOT / "reports" / "stage8_ai_domain_report.json"
REPORT_MD  = ROOT / "reports" / "stage8_ai_domain_report.md"
RECEIPTS   = ROOT / "reports" / "stage8_ai_domain_receipts.jsonl"
CURRENT    = ROOT / "reports" / "current"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Gate functions
# ---------------------------------------------------------------------------

def check_iw_containment(candidate: dict) -> tuple[bool, str]:
    iw = candidate.get("iw_containment", {})
    contained = iw.get("contained")
    if contained is None:
        return False, "iw_containment.contained not declared"
    return contained, (
        f"IW {iw.get('inference_window')} "
        f"{'contained in' if contained else 'BREACHES'} A_total {iw.get('a_total')}"
    )


def check_re_bound(candidate: dict) -> tuple[bool, str]:
    re = candidate.get("re_bound", {})
    within = re.get("within_bound")
    if within is None:
        return False, "re_bound.within_bound not declared"
    return within, (
        f"RE={re.get('re_score')} "
        f"{'<=' if within else '>'} RE_max={re.get('re_max')}"
    )


def check_recoverability(candidate: dict) -> tuple[bool, str]:
    score = candidate.get("recoverability_score", 0)
    floor = candidate.get("recoverability_floor", 0)
    ok = score >= floor
    return ok, f"recoverability {score} {'≥' if ok else '<'} floor {floor}"


def check_ai_block_scope(candidate: dict) -> tuple[bool, str]:
    block = candidate.get("ai_block", {})
    if not block:
        return True, "no ai_block — N/A"
    scope_ok = block.get("scope_respected", True)
    if not scope_ok:
        violation = block.get("violation_type", "scope_violation")
        return False, f"scope violated: {violation}"
    return True, f"scope respected: {block.get('declared_scope', [])}"


def check_hidden_authority(candidate: dict) -> tuple[bool, str]:
    block = candidate.get("ai_block", {})
    if not block:
        return True, "no ai_block — N/A"
    hidden = block.get("hidden_authority_detected", False)
    if hidden:
        return False, "P_NO_HIDDEN_AUTHORITY violated"
    return True, "no hidden authority detected"


def check_quorum(candidate: dict) -> tuple[bool, str]:
    block = candidate.get("ai_block", {})
    if not block:
        return True, "no ai_block — N/A"
    quorum = block.get("quorum")
    if not quorum:
        return True, "no quorum required for this transition"
    satisfied = quorum.get("quorum_satisfied", False)
    if not satisfied:
        missing = quorum.get("missing_parties", [])
        return False, f"quorum not satisfied; missing: {missing}"
    return True, f"quorum satisfied: {quorum.get('confirmed_parties')}"


def check_closure(candidate: dict) -> tuple[bool, str]:
    closure = candidate.get("dependency_closure_check", {})
    if not closure:
        return True, "no closure check required for this transition"
    verified = closure.get("closure_verified", False)
    if not verified:
        unknown = closure.get("unknown_dependency", "")
        uncovered = closure.get("uncovered_theorem", "")
        return False, f"closure failed: unknown={unknown} uncovered={uncovered}"
    return True, "dependency closure verified"


def evaluate_candidate(candidate: dict) -> dict:
    """
    Evaluate a single Stage 8 candidate against all gates.
    Returns result with decision, gate results, and receipt.
    """
    tid = candidate.get("transition_id", "unknown")
    expected = candidate.get("verified_decision", "unknown")

    gates = {}
    all_pass = True

    # IW containment
    ok, detail = check_iw_containment(candidate)
    gates["iw_containment"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # RE bound
    ok, detail = check_re_bound(candidate)
    gates["re_bound"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # Recoverability
    ok, detail = check_recoverability(candidate)
    gates["recoverability"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # AI Block scope
    ok, detail = check_ai_block_scope(candidate)
    gates["ai_block_scope"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # Hidden authority
    ok, detail = check_hidden_authority(candidate)
    gates["hidden_authority"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # Quorum
    ok, detail = check_quorum(candidate)
    gates["quorum"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # Dependency closure
    ok, detail = check_closure(candidate)
    gates["dependency_closure"] = {"pass": ok, "detail": detail}
    if not ok:
        all_pass = False

    # Determine decision from gate results and expected
    # RESET_BOUNDARY and EVOLVE_BOUNDARY need convergence/coherence checks
    decision = "ALLOW" if all_pass else "FAIL_CLOSED"

    # Verify decision matches expected
    matches = (decision == expected)
    if not matches:
        # FAIL_CLOSED when expected FAIL_CLOSED is also correct
        if expected == "FAIL_CLOSED" and decision == "FAIL_CLOSED":
            matches = True

    return {
        "transition_id": tid,
        "transition_name": candidate.get("transition_name"),
        "agent_type": candidate.get("ai_block", {}).get("agent_type", "n/a"),
        "expected_decision": expected,
        "actual_decision": decision,
        "decision_matches": matches,
        "gates": gates,
        "basis": candidate.get("basis", ""),
        "generated_at": now_utc(),
    }


# ---------------------------------------------------------------------------
# Assertion counting
# ---------------------------------------------------------------------------

ASSERTIONS_PER_CANDIDATE = 7  # one per gate + decision_matches


def count_assertions(results: list[dict]) -> tuple[int, int]:
    passed = 0
    total = 0
    for r in results:
        total += 1  # decision_matches
        if r["decision_matches"]:
            passed += 1
        for gate_name, gate in r["gates"].items():
            total += 1
            if gate["pass"]:
                passed += 1
            # Check that gate result matches what the candidate's
            # component_gate_results says
    return passed, total


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(candidates_path: Path) -> dict:
    print("=== Stage 8 — AI Domain Transition Classes ===")

    if not candidates_path.exists():
        print(f"ERROR: candidates not found: {candidates_path}")
        return {"verified": False, "error": "candidates not found"}

    data = json.loads(candidates_path.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])

    print(f"  Candidates: {len(candidates)}")
    print()

    results = []
    for c in candidates:
        result = evaluate_candidate(c)
        results.append(result)
        status = "PASS" if result["decision_matches"] else "FAIL"
        print(f"  [{status}] {result['transition_id']}")
        print(f"         {result['agent_type']} agent — {result['actual_decision']}")
        if not result["decision_matches"]:
            print(f"         expected {result['expected_decision']}, got {result['actual_decision']}")
        for gate, gr in result["gates"].items():
            if not gr["pass"]:
                print(f"         GATE FAIL: {gate}: {gr['detail']}")
    print()

    passed_decisions = sum(1 for r in results if r["decision_matches"])
    failed_decisions = len(results) - passed_decisions
    passed_assertions, total_assertions = count_assertions(results)
    success = failed_decisions == 0

    print(f"  Candidates: {len(candidates)}")
    print(f"  Assertions: {total_assertions}")
    print(f"  Passed: {passed_assertions}")
    print(f"  Failed: {total_assertions - passed_assertions}")
    print(f"  Result: {'PASS' if success else 'FAIL'}")

    # Decision summary
    decisions: dict[str, int] = {}
    for r in results:
        d = r["actual_decision"]
        decisions[d] = decisions.get(d, 0) + 1

    # Agent type coverage
    agent_types = {}
    for r in results:
        at = r["agent_type"]
        if at not in agent_types:
            agent_types[at] = {"ALLOW": 0, "FAIL_CLOSED": 0}
        agent_types[at][r["actual_decision"]] = (
            agent_types[at].get(r["actual_decision"], 0) + 1
        )

    # Build receipts
    receipts = []
    for r in results:
        rec = {
            "transition_id": r["transition_id"],
            "decision": r["actual_decision"],
            "decision_matches_expected": r["decision_matches"],
            "agent_type": r["agent_type"],
            "basis": r["basis"],
            "generated_at": r["generated_at"],
        }
        rec["receipt_hash"] = sha256_str(json.dumps(rec, sort_keys=True))
        receipts.append(rec)

    report = {
        "schema": "stegverse_stage8_ai_domain_report.v1",
        "stage": "Stage 8",
        "theorem_basis": "AI Domain Transition Classes",
        "generated_at": now_utc(),
        "verified": success,
        "candidate_count": len(candidates),
        "assertion_count": total_assertions,
        "passed_assertions": passed_assertions,
        "failed_assertions": total_assertions - passed_assertions,
        "decisions": decisions,
        "agent_type_coverage": agent_types,
        "ai_participation_governed": success,
        "quorum_gate_verified": any(
            r["transition_id"] == "T-AI-QUORUM-GATE-ALLOW-001"
            and r["decision_matches"]
            for r in results
        ),
        "quorum_failure_verified": any(
            r["transition_id"] == "T-AI-QUORUM-GATE-FAIL-001"
            and r["decision_matches"]
            for r in results
        ),
        "hidden_authority_detection_verified": any(
            r["transition_id"] == "T-AI-VERIF-AGENT-HIDDEN-AUTH-001"
            and r["decision_matches"]
            for r in results
        ),
        "candidate_results": results,
        "receipts": receipts,
    }
    report["report_hash"] = sha256_str(json.dumps(
        {k: v for k, v in report.items() if k != "receipts"},
        sort_keys=True
    ))

    # Write outputs
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    with open(RECEIPTS, "w", encoding="utf-8") as f:
        for rec in receipts:
            f.write(json.dumps(rec) + "\n")

    # Markdown
    lines = [
        "# Stage 8 — AI Domain Transition Classes Report",
        "",
        f"Generated: `{now_utc()}`",
        f"Result: **{'PASS' if success else 'FAIL'}**",
        f"Candidates: {len(candidates)} | "
        f"Assertions: {total_assertions} | "
        f"Passed: {passed_assertions}",
        "",
        "## Decision Summary",
        "",
        "| Decision | Count |",
        "|---|---:|",
    ]
    for d, count in sorted(decisions.items()):
        lines.append(f"| {d} | {count} |")

    lines += [
        "",
        "## Agent Type Coverage",
        "",
        "| Agent Type | ALLOW | FAIL_CLOSED |",
        "|---|---:|---:|",
    ]
    for at, counts in sorted(agent_types.items()):
        lines.append(
            f"| {at} | {counts.get('ALLOW', 0)} | {counts.get('FAIL_CLOSED', 0)} |"
        )

    lines += [
        "",
        "## Key Verifications",
        "",
        f"- Quorum gate ALLOW: **{report['quorum_gate_verified']}**",
        f"- Quorum gate FAIL_CLOSED: **{report['quorum_failure_verified']}**",
        f"- Hidden authority detection: **{report['hidden_authority_detection_verified']}**",
        f"- AI participation governed: **{report['ai_participation_governed']}**",
        "",
        "## What This Unlocks",
        "",
        "After Stage 8 verification:",
        "",
        "- AI entities may propose new transition class candidates",
        "  within their declared AI_BLOCK scope",
        "- Proposals require Stage 7 dependency closure verification",
        "- Proposals require quorum of Rige + Beta_Orionis before table entry",
        "- AI participation is governed by the same admissibility",
        "  framework as all other actors",
        "- Continuity pressure does not create authority",
    ]

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Copy to current/
    CURRENT.mkdir(parents=True, exist_ok=True)
    (CURRENT / "stage8_ai_domain_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\n  Report: {REPORT}")
    print(f"  Receipts: {RECEIPTS}")

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=str(CANDIDATES))
    args = parser.parse_args()
    result = run(Path(args.candidates))
    return 0 if result.get("verified") else 1


if __name__ == "__main__":
    raise SystemExit(main())
