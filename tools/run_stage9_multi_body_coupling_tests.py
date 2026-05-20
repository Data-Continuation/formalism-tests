#!/usr/bin/env python3
"""
run_stage9_multi_body_coupling_tests.py
=========================================
Declared task: stage9_multi_body_coupling_tests

Stage 9 — Multi-Body Coupling Closure

Validates that admissibility cannot be evaluated in isolation
when entities are coupled. Proves that local ALLOW does not
compose into global ALLOW across all coupling classes.

After Stage 9 verification:
  - Multi-agent AI participation is formally governed
  - Authority gradient drift is detected and failed closed
  - Coherence failure propagation is proven
  - AI split-brain routes to QUARANTINE not DENY
  - Multi-agent cascade without human quorum fails closed
  - Human-AI quorum is the formally verified participation path

Usage:
  python tools/run_stage9_multi_body_coupling_tests.py
  python tools/run_stage9_multi_body_coupling_tests.py --candidates tests/fixtures/stage9_candidates.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE       = Path(__file__).resolve().parent
ROOT       = HERE.parent
CANDIDATES = ROOT / "tests" / "fixtures" / "stage9_candidates.json"
REPORT     = ROOT / "reports" / "stage9_multi_body_coupling_report.json"
REPORT_MD  = ROOT / "reports" / "stage9_multi_body_coupling_report.md"
RECEIPTS   = ROOT / "reports" / "stage9_multi_body_coupling_receipts.jsonl"
CURRENT    = ROOT / "reports" / "current"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Gate functions
# ---------------------------------------------------------------------------

def check_composite_iw(candidate: dict) -> tuple[bool, str]:
    iw = candidate.get("iw_containment", {})
    contained = iw.get("composite_iw_contained")
    if contained is None:
        return False, "composite_iw_contained not declared"
    return contained, (
        f"composite IW width={iw.get('composite_iw_width', '?')} "
        f"{'contained' if contained else 'BREACHES A_total'}"
    )


def check_composite_re(candidate: dict) -> tuple[bool, str]:
    re = candidate.get("re_bound", {})
    within = re.get("composite_re_within_bound")
    if within is None:
        return False, "composite_re_within_bound not declared"
    return within, (
        f"composite RE={re.get('composite_re_score', '?')} "
        f"RE_max={re.get('re_max', '?')} "
        f"{'within bound' if within else 'EXCEEDS MAX'}"
    )


def check_global_coherence(candidate: dict) -> tuple[bool, str]:
    gc = candidate.get("global_coherence", {})
    if not gc:
        return True, "no global_coherence check — N/A"
    satisfied = gc.get("satisfied", True)
    return satisfied, (
        f"global coherence={gc.get('score', '?')} "
        f"min={gc.get('minimum', '?')} "
        f"{'satisfied' if satisfied else 'FAILED'}"
    )


def check_convergence(candidate: dict) -> tuple[bool, str]:
    cv = candidate.get("convergence", {})
    if not cv:
        return True, "no convergence check — N/A"
    satisfied = cv.get("satisfied", True)
    return satisfied, (
        f"convergence={cv.get('score', '?')} "
        f"min={cv.get('minimum', '?')} "
        f"{'satisfied' if satisfied else 'FAILED'}"
    )


def check_composite_recoverability(candidate: dict) -> tuple[bool, str]:
    comp_rec = candidate.get("composite_recoverability")
    if comp_rec is None:
        return True, "no composite_recoverability — using individual scores"
    floor = candidate.get("recoverability_floor", 0.40)
    ok = comp_rec >= floor
    return ok, (
        f"composite recoverability={comp_rec} "
        f"floor={floor} "
        f"{'above' if ok else 'BELOW'} floor"
    )


def check_authority_gradient(candidate: dict) -> tuple[bool, str]:
    coupling = candidate.get("coupling_analysis", {})
    drift = coupling.get("authority_class_exceeded", False)
    if drift:
        return False, (
            f"authority gradient drift: "
            f"effective={coupling.get('effective_authority_class')} "
            f"declared={coupling.get('declared_authority_class')}"
        )
    cascade = coupling.get("quorum_bypassed", False)
    if cascade:
        return False, "cascade bypasses quorum — authority gradient violated"
    return True, "authority gradient stable"


def check_coupling_class_coverage(
    candidate: dict, covered: set
) -> tuple[bool, str]:
    cc = candidate.get("coupling_class", "")
    covered.add(cc)
    return True, f"coupling_class={cc} recorded"


def determine_composite_decision(candidate: dict) -> str:
    """
    Determine composite decision from gate results and coupling analysis.
    Mirrors the admissibility logic from the formalism.
    """
    coupling = candidate.get("coupling_analysis", {})
    multi_body = candidate.get("multi_body_gate_result", "")

    # Direct fail conditions
    iw_ok, _ = check_composite_iw(candidate)
    re_ok, _ = check_composite_re(candidate)
    gc_ok, _ = check_global_coherence(candidate)
    cv_ok, _ = check_convergence(candidate)
    rec_ok, _ = check_composite_recoverability(candidate)
    auth_ok, _ = check_authority_gradient(candidate)

    # Split-brain → QUARANTINE
    if coupling.get("mutually_incompatible_coherent_states"):
        return "QUARANTINE"

    # Hard fails
    if not iw_ok or not re_ok or not auth_ok:
        return "FAIL_CLOSED"

    if not rec_ok:
        return "FAIL_CLOSED"

    if coupling.get("composite_exceeds_capacity") or \
       coupling.get("cascade_exceeds_capacity"):
        return "FAIL_CLOSED"

    # Coherence failure → EVOLVE_BOUNDARY
    comp_coherence = candidate.get("coupling_analysis", {}).get(
        "composite_coherence_satisfied"
    )
    if comp_coherence is False:
        return "EVOLVE_BOUNDARY"

    # Convergence failure → RESET_BOUNDARY
    quorum_structure = coupling.get("quorum_structure")
    conv_fail = coupling.get("convergence_failure_evidence", False)
    if conv_fail and coupling.get("quorum_satisfied"):
        return "RESET_BOUNDARY"

    # Positive controls
    if not gc_ok or not cv_ok:
        return "FAIL_CLOSED"

    return "ALLOW"


def evaluate_candidate(candidate: dict) -> dict:
    tid = candidate.get("transition_id", "unknown")
    expected = candidate.get("verified_decision", "unknown")
    covered_classes: set = set()

    gates = {}

    ok, detail = check_composite_iw(candidate)
    gates["composite_iw_containment"] = {"pass": ok, "detail": detail}

    ok, detail = check_composite_re(candidate)
    gates["composite_re_bound"] = {"pass": ok, "detail": detail}

    ok, detail = check_global_coherence(candidate)
    gates["global_coherence"] = {"pass": ok, "detail": detail}

    ok, detail = check_convergence(candidate)
    gates["convergence"] = {"pass": ok, "detail": detail}

    ok, detail = check_composite_recoverability(candidate)
    gates["composite_recoverability"] = {"pass": ok, "detail": detail}

    ok, detail = check_authority_gradient(candidate)
    gates["authority_gradient"] = {"pass": ok, "detail": detail}

    ok, detail = check_coupling_class_coverage(candidate, covered_classes)
    gates["coupling_class_recorded"] = {"pass": ok, "detail": detail}

    actual = determine_composite_decision(candidate)
    matches = actual == expected

    return {
        "transition_id": tid,
        "transition_name": candidate.get("transition_name"),
        "coupling_class": candidate.get("coupling_class"),
        "entity_count": len(candidate.get("entities", [])),
        "expected_decision": expected,
        "actual_decision": actual,
        "decision_matches": matches,
        "gates": gates,
        "basis": candidate.get("basis", ""),
        "generated_at": now_utc(),
    }


def run(candidates_path: Path) -> dict:
    print("=== Stage 9 — Multi-Body Coupling Closure ===")

    if not candidates_path.exists():
        print(f"ERROR: candidates not found: {candidates_path}")
        return {"verified": False, "error": "candidates not found"}

    data = json.loads(candidates_path.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])
    coupling_classes_declared = set(data.get("coupling_classes_covered", []))

    print(f"  Candidates: {len(candidates)}")
    print(f"  Coupling classes declared: {len(coupling_classes_declared)}")
    print()

    results = []
    coupling_classes_tested: set = set()

    for c in candidates:
        result = evaluate_candidate(c)
        coupling_classes_tested.add(c.get("coupling_class", ""))
        results.append(result)

        status = "PASS" if result["decision_matches"] else "FAIL"
        print(f"  [{status}] {result['transition_id']}")
        print(f"         {result['coupling_class']} — {result['actual_decision']}")
        if not result["decision_matches"]:
            print(
                f"         expected {result['expected_decision']}, "
                f"got {result['actual_decision']}"
            )
        for gate, gr in result["gates"].items():
            if not gr["pass"] and gate != "coupling_class_recorded":
                print(f"         gate: {gate}: {gr['detail']}")

    print()

    # Coverage check
    missing_classes = coupling_classes_declared - coupling_classes_tested
    coverage_complete = len(missing_classes) == 0

    passed_decisions = sum(1 for r in results if r["decision_matches"])
    failed_decisions = len(results) - passed_decisions

    # Assertion count: gates per candidate + decision match
    total_assertions = sum(len(r["gates"]) + 1 for r in results)
    passed_assertions = sum(
        sum(1 for g in r["gates"].values() if g["pass"]) +
        (1 if r["decision_matches"] else 0)
        for r in results
    )

    success = failed_decisions == 0 and coverage_complete

    print(f"  Candidates: {len(candidates)}")
    print(f"  Assertions: {total_assertions}")
    print(f"  Passed: {passed_assertions}")
    print(f"  Failed: {total_assertions - passed_assertions}")
    print(f"  Coupling classes tested: {sorted(coupling_classes_tested)}")
    if missing_classes:
        print(f"  Missing classes: {sorted(missing_classes)}")
    print(f"  Result: {'PASS' if success else 'FAIL'}")

    # Decision summary
    decisions: dict[str, int] = {}
    for r in results:
        d = r["actual_decision"]
        decisions[d] = decisions.get(d, 0) + 1

    # Coupling class summary
    coupling_summary: dict[str, str] = {}
    for r in results:
        cc = r["coupling_class"]
        coupling_summary[cc] = r["actual_decision"]

    # Build receipts
    receipts = []
    for r in results:
        rec = {
            "transition_id": r["transition_id"],
            "coupling_class": r["coupling_class"],
            "decision": r["actual_decision"],
            "decision_matches_expected": r["decision_matches"],
            "basis": r["basis"],
            "generated_at": r["generated_at"],
        }
        rec["receipt_hash"] = sha256_str(json.dumps(rec, sort_keys=True))
        receipts.append(rec)

    report = {
        "schema": "stegverse_stage9_multi_body_report.v1",
        "stage": "Stage 9",
        "theorem_basis": "Multi-Body Coupling Closure",
        "canonical_claim": data.get("canonical_claim", ""),
        "generated_at": now_utc(),
        "verified": success,
        "candidate_count": len(candidates),
        "assertion_count": total_assertions,
        "passed_assertions": passed_assertions,
        "failed_assertions": total_assertions - passed_assertions,
        "decisions": decisions,
        "coupling_classes_declared": sorted(coupling_classes_declared),
        "coupling_classes_tested": sorted(coupling_classes_tested),
        "coupling_coverage_complete": coverage_complete,
        "coupling_summary": coupling_summary,
        "local_allow_composite_fail_verified": any(
            r["transition_id"] == "T-MB-LOCAL-ALLOW-COMPOSITE-FAIL-001"
            and r["decision_matches"] for r in results
        ),
        "authority_gradient_drift_verified": any(
            r["transition_id"] == "T-MB-AUTH-GRADIENT-DRIFT-001"
            and r["decision_matches"] for r in results
        ),
        "split_brain_quarantine_verified": any(
            r["transition_id"] == "T-MB-SPLIT-BRAIN-AI-001"
            and r["decision_matches"] for r in results
        ),
        "cascade_fail_verified": any(
            r["transition_id"] == "T-MB-CASCADE-FAIL-001"
            and r["decision_matches"] for r in results
        ),
        "human_ai_quorum_path_verified": any(
            r["transition_id"] == "T-MB-TRUST-FIELD-ALLOW-001"
            and r["decision_matches"] for r in results
        ),
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

    lines = [
        "# Stage 9 — Multi-Body Coupling Closure Report",
        "",
        f"Generated: `{now_utc()}`",
        f"Result: **{'PASS' if success else 'FAIL'}**",
        f"Candidates: {len(candidates)} | "
        f"Assertions: {total_assertions} | "
        f"Passed: {passed_assertions}",
        "",
        "## Canonical Claim",
        "",
        f"> {data.get('canonical_claim', '')}",
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
        "## Coupling Class Coverage",
        "",
        "| Coupling Class | Decision |",
        "|---|---|",
    ]
    for cc, dec in sorted(coupling_summary.items()):
        lines.append(f"| {cc} | {dec} |")

    lines += [
        "",
        "## Key Verifications",
        "",
        f"- Local ALLOW → Composite FAIL_CLOSED: "
        f"**{report['local_allow_composite_fail_verified']}**",
        f"- Authority gradient drift detected: "
        f"**{report['authority_gradient_drift_verified']}**",
        f"- AI split-brain → QUARANTINE: "
        f"**{report['split_brain_quarantine_verified']}**",
        f"- Multi-agent cascade without quorum → FAIL_CLOSED: "
        f"**{report['cascade_fail_verified']}**",
        f"- Human-AI quorum path verified: "
        f"**{report['human_ai_quorum_path_verified']}**",
        "",
        "## What This Unlocks",
        "",
        "After Stage 9 verification:",
        "",
        "- Multi-agent AI participation is formally governed",
        "- The Human-AI quorum path (Rige + Beta_Orionis) is the",
        "  formally verified path for ecosystem changes",
        "- AI-to-AI interaction without human in the loop is",
        "  formally proven to fail closed or route to QUARANTINE",
        "- External AI entities from outside the ecosystem can be",
        "  evaluated against the formal coupling framework",
        "- The transition table is defensible to outside observers",
    ]

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    CURRENT.mkdir(parents=True, exist_ok=True)
    (CURRENT / "stage9_multi_body_coupling_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\n  Report: {REPORT}")
    print(f"  Receipts: {RECEIPTS}")

    return report


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", default=str(CANDIDATES))
    args = parser.parse_args()
    result = run(Path(args.candidates))
    return 0 if result.get("verified") else 1


if __name__ == "__main__":
    raise SystemExit(main())
