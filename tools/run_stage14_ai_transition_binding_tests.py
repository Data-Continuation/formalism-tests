#!/usr/bin/env python3
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage14_ai_transition_binding_cases.json")
REPORT = Path("reports/stage14_ai_transition_binding_report.json")
RECEIPTS = Path("reports/stage14_ai_transition_binding_receipts.jsonl")


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1


def decide(case, required_classes):
    policy = case.get("policy_scope", {})
    applicable = set(case.get("applicable_ai_governance_transition_classes", []))
    required = set(required_classes)

    if case.get("entity_id") != "StegVerse-001":
        return "FAIL_CLOSED", "wrong governed work-entity"
    if case.get("entity_status") != "active":
        return "FAIL_CLOSED", "work-entity is not active"
    if not case.get("transition_table_bound"):
        return "FAIL_CLOSED", "work-entity is not bound to the Transition Table"
    if case.get("binding_authority") != "formalism-tests":
        return "FAIL_CLOSED", "binding authority must be formalism-tests"
    if case.get("entity_claims_canonical_authority"):
        return "FAIL_CLOSED", "active work-entity cannot claim canonical authority"
    if case.get("site_claims_authority"):
        return "FAIL_CLOSED", "Site cannot become binding or proof authority"
    if case.get("review_state") != "accepted":
        return "FAIL_CLOSED", "review is not accepted"
    if case.get("dependency_closure") != "closed":
        return "FAIL_CLOSED", "dependency closure is not closed"
    if case.get("receipt_required") and not case.get("receipt_emitted"):
        return "FAIL_CLOSED", "required receipt missing"
    if case.get("applicability_mode") != "all_applicable_ai_governance_transitions":
        return "FAIL_CLOSED", "AI work-entity must be governed by all applicable AI-governance transitions"
    missing = sorted(required - applicable)
    if missing:
        return "FAIL_CLOSED", "missing applicable AI-governance transition classes: " + ", ".join(missing)
    if case.get("unrecognized_transition_classes"):
        return "FAIL_CLOSED", "unrecognized transition classes are denied by policy"
    if not policy.get("policy_source"):
        return "FAIL_CLOSED", "policy source missing"
    if not policy.get("policy_version"):
        return "FAIL_CLOSED", "policy version missing"
    if policy.get("decision") != "ALLOW":
        return "FAIL_CLOSED", "policy scope did not allow binding"
    if policy.get("authority_scope") != "bounded_work_entity":
        return "FAIL_CLOSED", "policy authority scope is not bounded_work_entity"
    if policy.get("transition_scope") != "ai_governance_applicable_transitions":
        return "FAIL_CLOSED", "policy transition scope is not ai_governance_applicable_transitions"
    if not case.get("release_queue_lineage_valid"):
        return "FAIL_CLOSED", "release queue lineage invalid"
    if case.get("binding_action") == "record_binding_entry":
        if case.get("ledger_record_required") and case.get("ledger_record_emitted"):
            return "LEDGER_ENTITY_BINDING", "active work-entity Transition Table binding ledger entry recorded"
        return "FAIL_CLOSED", "binding ledger record missing"
    return "ALLOW_TRANSITION_TABLE_BINDING", "active work-entity is bound to all applicable AI-governance transitions under declared policy scope"


def main():
    try:
        data = json.loads(FIXTURE.read_text())
        checks = 0
        receipts = []
        counts = {}
        cases = data["cases"]
        required_classes = data["required_ai_governance_transition_classes"]

        checks += req(data.get("stage") == "Stage 14", "stage must be Stage 14")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "wrong work entity")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")
        checks += req(data.get("binding_target", {}).get("binding_mode") == "all_applicable_ai_governance_transitions", "binding mode must require all applicable AI transitions")
        checks += req(len(required_classes) >= 10, "expected broad AI-governance transition coverage")
        checks += req(len(cases) >= 10, "expected at least 10 cases")

        for control in data["required_policy_controls"]:
            checks += req(isinstance(control, str) and control, "invalid policy control")

        for case in cases:
            checks += req(case.get("case_id"), "missing case_id")
            checks += req(case.get("candidate_id"), f"{case.get('case_id')}: missing candidate_id")
            checks += req(case.get("expected_decision"), f"{case.get('case_id')}: missing expected_decision")
            checks += req(case.get("transition_table_release") == data["binding_target"]["transition_table_release"], f"{case['case_id']}: wrong transition table release")
            decision, basis = decide(case, required_classes)
            checks += req(decision == case["expected_decision"], f"{case['case_id']}: expected {case['expected_decision']}, got {decision}: {basis}")
            receipt = {
                "schema": "stegverse_stage14_ai_transition_binding_receipt.v1",
                "stage": data["stage"],
                "case_id": case["case_id"],
                "candidate_id": case["candidate_id"],
                "entity_id": case["entity_id"],
                "entity_status": case["entity_status"],
                "transition_table_release": case["transition_table_release"],
                "decision": decision,
                "basis": basis,
                "binding_authority": case.get("binding_authority"),
                "policy_scope": case.get("policy_scope"),
                "applicable_ai_governance_transition_classes": case.get("applicable_ai_governance_transition_classes", []),
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required in ["ALLOW_TRANSITION_TABLE_BINDING", "FAIL_CLOSED", "LEDGER_ENTITY_BINDING"]:
            checks += req(required in counts, f"missing decision coverage {required}")

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts))
        report = {
            "schema": "stegverse_stage14_ai_transition_binding_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": data["stage"],
            "theorem_basis": data["theorem_basis"],
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "assertion_count": checks,
            "case_count": len(cases),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "message": "Stage 14 active AI work-entity Transition Table binding validation passed.",
            "report": str(REPORT),
            "receipts": str(RECEIPTS),
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {"schema": "stegverse_stage14_ai_transition_binding_report.v1", "success": False, "error": str(exc)}
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
