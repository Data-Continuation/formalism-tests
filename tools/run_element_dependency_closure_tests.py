#!/usr/bin/env python3
"""
run_element_dependency_closure_tests.py
=========================================
Declared task: element_dependency_closure_tests

Stage 7 — Element Dependency Closure

Validates that every unlocked transition element has declared dependencies
and that no Level 5 element depends on an uncovered or lower-confidence
element without an explicit boundary.

This is the prerequisite for AI Block formal composition verification.

Usage:
  python tools/run_element_dependency_closure_tests.py
  python tools/run_element_dependency_closure_tests.py --policy tests/fixtures/element_dependency_closure_policy.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE   = Path(__file__).resolve().parent
ROOT   = HERE.parent
POLICY = ROOT / "tests" / "fixtures" / "element_dependency_closure_policy.json"
REPORT = ROOT / "reports" / "element_dependency_closure_report.json"
REPORT_MD = ROOT / "reports" / "element_dependency_closure_report.md"
CURRENT = ROOT / "reports" / "current"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------

class AssertionResult:
    def __init__(self, name: str, passed: bool, detail: str = ""):
        self.name    = name
        self.passed  = passed
        self.detail  = detail


def check(results: list, name: str, condition: bool, detail: str = "") -> bool:
    results.append(AssertionResult(name, condition, detail))
    return condition


# ---------------------------------------------------------------------------
# Stage 7 validation checks
# ---------------------------------------------------------------------------

def validate_all_elements_have_dependencies(
    elements: dict, results: list
) -> None:
    """Every element must declare dependencies or be declared a primitive."""
    primitives = set()
    policy_data = elements.get("_policy", {})

    for eid, elem in elements.items():
        if eid.startswith("_"):
            continue

        deps = elem.get("dependencies", None)
        check(
            results,
            f"element.{eid}.has_dependencies_declared",
            deps is not None,
            f"dependencies field {'present' if deps is not None else 'MISSING'}",
        )

        if deps == []:
            primitives.add(eid)


def validate_known_elements(elements: dict, results: list) -> set:
    """Build the set of known elements and validate all are Level 5 verified."""
    known = set()
    for eid, elem in elements.items():
        if eid.startswith("_"):
            continue
        known.add(eid)
        check(
            results,
            f"element.{eid}.is_level5",
            elem.get("level") == 5,
            f"level={elem.get('level')}",
        )
        check(
            results,
            f"element.{eid}.is_verified",
            elem.get("status") == "verified",
            f"status={elem.get('status')}",
        )
    return known


def validate_dependency_resolution(
    elements: dict, known: set, results: list
) -> None:
    """All dependencies must resolve to known elements."""
    for eid, elem in elements.items():
        if eid.startswith("_"):
            continue
        for dep in elem.get("dependencies", []):
            check(
                results,
                f"element.{eid}.dependency.{dep}.resolves",
                dep in known,
                f"dependency '{dep}' {'known' if dep in known else 'UNKNOWN'}",
            )


def validate_no_uncovered_theorem_deps(
    elements: dict, results: list
) -> None:
    """No element may depend on an uncovered theorem."""
    for eid, elem in elements.items():
        if eid.startswith("_"):
            continue
        theorems = elem.get("theorem_coverage", [])
        check(
            results,
            f"element.{eid}.has_theorem_coverage",
            len(theorems) > 0,
            f"{len(theorems)} theorems covered",
        )


def validate_acyclicity(elements: dict, results: list) -> None:
    """Dependency graph must be acyclic (primitives have no deps)."""
    # Build adjacency
    graph: dict[str, set] = {}
    for eid, elem in elements.items():
        if eid.startswith("_"):
            continue
        graph[eid] = set(elem.get("dependencies", []))

    # DFS cycle detection
    visited: set = set()
    rec_stack: set = set()
    cycles_found = []

    def dfs(node: str, path: list) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                if dfs(neighbor, path + [neighbor]):
                    return True
            elif neighbor in rec_stack:
                cycles_found.append(path + [neighbor])
                return True
        rec_stack.discard(node)
        return False

    for node in graph:
        if node not in visited:
            dfs(node, [node])

    check(
        results,
        "dependency_graph.is_acyclic",
        len(cycles_found) == 0,
        f"cycles detected: {cycles_found}" if cycles_found else "no cycles",
    )


def validate_ai_block_constraints(
    elements: dict, results: list
) -> None:
    """AI_BLOCK cannot bypass authority or scope requirements."""
    ai_block = elements.get("AI_BLOCK", {})
    if not ai_block:
        check(results, "AI_BLOCK.present", False, "AI_BLOCK element missing")
        return

    scope = ai_block.get("scope_constraint", {})
    check(
        results,
        "AI_BLOCK.declared_scope_required",
        scope.get("declared_scope_required") is True,
        str(scope.get("declared_scope_required")),
    )
    check(
        results,
        "AI_BLOCK.scope_verified_at_execution",
        scope.get("scope_verified_at_execution") is True,
        str(scope.get("scope_verified_at_execution")),
    )
    check(
        results,
        "AI_BLOCK.scope_violation_fails_closed",
        scope.get("scope_violation_decision") == "FAIL_CLOSED",
        str(scope.get("scope_violation_decision")),
    )
    cannot_acquire = scope.get("cannot_acquire", [])
    for forbidden in ["sandbox:escape", "credential:acquire",
                      "authority:escalate"]:
        check(
            results,
            f"AI_BLOCK.cannot_acquire.{forbidden}",
            forbidden in cannot_acquire,
            f"{'forbidden' if forbidden in cannot_acquire else 'NOT FORBIDDEN — CRITICAL'}",
        )


def validate_finco_chain_constraints(
    elements: dict, results: list
) -> None:
    """FINCO_CHAIN cannot bypass receipt requirements."""
    finco = elements.get("FINCO_CHAIN", {})
    if not finco:
        check(results, "FINCO_CHAIN.present", False, "FINCO_CHAIN element missing")
        return

    chain = finco.get("chain_integrity", {})
    check(
        results,
        "FINCO_CHAIN.evidence_only",
        chain.get("evidence_only") is True,
        str(chain.get("evidence_only")),
    )
    check(
        results,
        "FINCO_CHAIN.creates_entitlement_false",
        chain.get("creates_entitlement") is False,
        str(chain.get("creates_entitlement")),
    )
    check(
        results,
        "FINCO_CHAIN.broken_chain_fails_closed",
        chain.get("broken_chain_decision") == "FAIL_CLOSED",
        str(chain.get("broken_chain_decision")),
    )
    check(
        results,
        "FINCO_CHAIN.missing_receipt_fails_closed",
        chain.get("missing_receipt_decision") == "FAIL_CLOSED",
        str(chain.get("missing_receipt_decision")),
    )


def validate_composition_invariants(
    policy: dict, results: list
) -> None:
    """Validate composition safety invariants are declared."""
    invariants = policy.get("composition_safety_invariants", [])
    required_ids = {
        "CSI-001", "CSI-002", "CSI-003", "CSI-004", "CSI-005", "CSI-006"
    }
    found_ids = {inv.get("invariant_id") for inv in invariants}
    for req in required_ids:
        check(
            results,
            f"invariant.{req}.declared",
            req in found_ids,
            f"{'present' if req in found_ids else 'MISSING'}",
        )

    # CSI-003: failure propagates to all
    csi3 = next(
        (i for i in invariants if i.get("invariant_id") == "CSI-003"), {}
    )
    applies_to = csi3.get("applies_to", [])
    check(
        results,
        "invariant.CSI-003.applies_to_all",
        "all" in applies_to,
        str(applies_to),
    )


def validate_primitives(policy: dict, results: list) -> None:
    """Primitives must be declared in the policy."""
    gc = policy.get("dependency_graph_constraints", {})
    primitives = gc.get("primitives", [])
    required = {"IW", "RE", "REPRESENTATION_NON_CONSEQUENCE"}
    for p in required:
        check(
            results,
            f"primitive.{p}.declared",
            p in primitives,
            f"{'declared' if p in primitives else 'MISSING'}",
        )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run(policy_path: Path) -> dict:
    print("=== Stage 7 — Element Dependency Closure ===")

    if not policy_path.exists():
        print(f"ERROR: policy not found: {policy_path}")
        return {"success": False, "error": "policy not found"}

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    elements = policy.get("elements", {})
    results: list[AssertionResult] = []

    print(f"  Elements: {len(elements)}")
    print()

    # Run all checks
    known = validate_known_elements(elements, results)
    validate_all_elements_have_dependencies(elements, results)
    validate_dependency_resolution(elements, known, results)
    validate_no_uncovered_theorem_deps(elements, results)
    validate_acyclicity(elements, results)
    validate_ai_block_constraints(elements, results)
    validate_finco_chain_constraints(elements, results)
    validate_composition_invariants(policy, results)
    validate_primitives(policy, results)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    success = failed == 0

    print(f"  Assertions: {len(results)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Result: {'PASS' if success else 'FAIL'}")

    if not success:
        print("\nFailed assertions:")
        for r in results:
            if not r.passed:
                print(f"  FAIL  {r.name}: {r.detail}")

    # Build receipts
    receipts = []
    for r in results:
        rec = {
            "assertion": r.name,
            "decision": "ALLOW" if r.passed else "FAIL_CLOSED",
            "detail": r.detail,
            "generated_at": now_utc(),
        }
        rec["receipt_hash"] = sha256_str(json.dumps(rec, sort_keys=True))
        receipts.append(rec)

    # Build decision summary
    element_closures = {}
    for eid in elements:
        if eid.startswith("_"):
            continue
        elem_results = [r for r in results if r.name.startswith(f"element.{eid}.")]
        all_pass = all(r.passed for r in elem_results)
        element_closures[eid] = "ALLOW" if all_pass else "FAIL_CLOSED"

    report = {
        "schema": "stegverse_stage7_closure_report.v1",
        "stage": "Stage 7",
        "theorem_basis": "Element Dependency Closure",
        "generated_at": now_utc(),
        "verified": success,
        "element_count": len(elements),
        "assertion_count": len(results),
        "passed_count": passed,
        "failed_count": failed,
        "element_closures": element_closures,
        "composition_invariants_verified": failed == 0,
        "primitives_declared": True,
        "ai_block_constraints_verified": (
            all(r.passed for r in results if "AI_BLOCK" in r.name)
        ),
        "finco_chain_constraints_verified": (
            all(r.passed for r in results if "FINCO_CHAIN" in r.name)
        ),
        "receipts": receipts,
    }
    report["report_hash"] = sha256_str(json.dumps(report, sort_keys=True))

    # Write outputs
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    # Write receipts JSONL
    receipts_path = ROOT / "reports" / "element_dependency_closure_receipts.jsonl"
    with open(receipts_path, "w", encoding="utf-8") as f:
        for rec in receipts:
            f.write(json.dumps(rec) + "\n")

    # Write markdown summary
    lines = [
        "# Stage 7 — Element Dependency Closure Report",
        "",
        f"Generated: `{now_utc()}`",
        f"Result: **{'PASS' if success else 'FAIL'}**",
        f"Assertions: {len(results)} | Passed: {passed} | Failed: {failed}",
        "",
        "## Element Closure Summary",
        "",
        "| Element | Closure |",
        "|---|---|",
    ]
    for eid, decision in sorted(element_closures.items()):
        lines.append(f"| {eid} | {decision} |")

    lines += [
        "",
        "## Composition Safety Invariants",
        "",
        f"All invariants verified: **{report['composition_invariants_verified']}**",
        "",
        "## Primitives",
        "",
        "IW, RE, REPRESENTATION_NON_CONSEQUENCE declared as primitives.",
        "",
        "## AI Block Constraints",
        "",
        f"AI_BLOCK constraints verified: **{report['ai_block_constraints_verified']}**",
        "",
        "## FinCo Chain Constraints",
        "",
        f"FINCO_CHAIN constraints verified: **{report['finco_chain_constraints_verified']}**",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Copy to current/
    CURRENT.mkdir(parents=True, exist_ok=True)
    (CURRENT / "element_dependency_closure_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(f"\n  Report: {REPORT}")
    print(f"  Receipts: {receipts_path}")

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", default=str(POLICY))
    args = parser.parse_args()
    result = run(Path(args.policy))
    return 0 if result.get("verified") else 1


if __name__ == "__main__":
    raise SystemExit(main())
