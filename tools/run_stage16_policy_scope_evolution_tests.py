#!/usr/bin/env python3
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage16_policy_scope_evolution_cases.json")
REPORT = Path("reports/stage16_policy_scope_evolution_report.json")
RECEIPTS = Path("reports/stage16_policy_scope_evolution_receipts.jsonl")

EXPECTED_AUTHORITY = "formalism-tests"

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def decide(case):
    if case.get("entity_id") != "StegVerse-001":
        return "FAIL_CLOSED", "unknown work-entity"
    if case.get("entity_status") != "active":
        return "FAIL_CLOSED", "work-entity is not active"
    if not case.get("transition_table_bound"):
        return "FAIL_CLOSED", "work-entity is not bound to the Transition Table"
    if case.get("policy_evolution_authority") != EXPECTED_AUTHORITY:
        return "FAIL_CLOSED", "policy evolution authority must remain formalism-tests"
    if not case.get("policy_version_incremented"):
        return "FAIL_CLOSED", "policy version was not incremented"
    if not case.get("transition_class_discovered"):
        return "FAIL_CLOSED", "new transition class was not discovered"
    if not case.get("applicability_evaluated"):
        return "FAIL_CLOSED", "transition applicability was not evaluated"
    if case.get("receipt_required") and not case.get("receipt_emitted"):
        return "FAIL_CLOSED", "required policy evolution receipt missing"

    applicability = case.get("applicability_decision")
    if applicability == "applicable":
        if not case.get("bound_to_entity"):
            return "FAIL_CLOSED", "applicable AI-governance transition was not bound to the entity"
    elif applicability == "not_applicable":
        if not case.get("not_applicable_basis"):
            return "FAIL_CLOSED", "not-applicable transition lacks explicit basis"
    elif applicability == "requires_review":
        return "REQUIRE_APPLICABILITY_REVIEW", "transition applicability requires review before binding"
    else:
        return "FAIL_CLOSED", "unknown applicability decision"

    if case.get("ledger_record_required"):
        if case.get("ledger_record_emitted"):
            return "LEDGER_POLICY_SCOPE_UPDATE", "policy scope update ledger entry recorded"
        return "FAIL_CLOSED", "policy scope ledger record missing"

    return "ALLOW_POLICY_SCOPE_EVOLUTION", "policy scope evolution is admissible"

def main():
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        checks = 0
        receipts = []
        counts = {}
        cases = data["cases"]

        checks += req(data.get("stage") == "Stage 16", "stage must be Stage 16")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")
        checks += req(data.get("work_entity", {}).get("transition_table_bound") is True, "work entity must be transition-table-bound")
        checks += req(data.get("source_policy_version") != data.get("target_policy_version"), "policy version must evolve")
        checks += req(len(cases) >= 10, "expected at least 10 cases")

        for control in [
            "active_work_entity_required",
            "transition_table_binding_required",
            "new_transition_class_discovery_required",
            "applicability_evaluation_required",
            "applicable_transition_binding_required",
            "not_applicable_basis_required",
            "policy_version_increment_required",
            "formalism_tests_policy_authority_required",
            "unknown_applicability_fail_closed",
        ]:
            checks += req(control in data.get("required_controls", []), f"missing required control: {control}")

        for transition in [
            "active_work_entity_execution",
            "transition_table_binding",
            "policy_scope_evolution",
        ]:
            checks += req(transition in data.get("known_ai_governance_transition_classes", []), f"missing known transition: {transition}")

        for case in cases:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("candidate_id"), f"{case_id}: missing candidate_id")
            checks += req(case.get("new_transition_class"), f"{case_id}: missing new_transition_class")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage16_policy_scope_evolution_receipt.v1",
                "case_id": case_id,
                "candidate_id": case["candidate_id"],
                "entity_id": case["entity_id"],
                "source_policy_version": case["source_policy_version"],
                "target_policy_version": case["target_policy_version"],
                "new_transition_class": case["new_transition_class"],
                "applicability_decision": case["applicability_decision"],
                "decision": decision,
                "basis": basis,
                "authority_boundary": data["authority_boundary"],
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in [
            "ALLOW_POLICY_SCOPE_EVOLUTION",
            "FAIL_CLOSED",
            "LEDGER_POLICY_SCOPE_UPDATE",
            "REQUIRE_APPLICABILITY_REVIEW",
        ]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage16_policy_scope_evolution_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 16",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(cases),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "source_policy_version": data["source_policy_version"],
            "target_policy_version": data["target_policy_version"],
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "message": "Stage 16 AI policy scope evolution and transition applicability reconciliation passed.",
            "report": str(REPORT),
            "receipts": str(RECEIPTS),
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage16_policy_scope_evolution_report.v1",
            "success": False,
            "error": str(exc),
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
