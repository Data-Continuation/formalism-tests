#!/usr/bin/env python3
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage13_active_work_entity_release_delta_cases.json")
REPORT = Path("reports/stage13_active_work_entity_release_delta_report.json")
RECEIPTS = Path("reports/stage13_active_work_entity_release_delta_receipts.jsonl")


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1


def decide(c):
    if c.get("entity_status") != "active":
        return "FAIL_CLOSED", "work-entity is not active"
    if c.get("entity_id") != "StegVerse-001":
        return "FAIL_CLOSED", "unexpected work-entity"
    if c.get("self_promotion_attempted"):
        return "FAIL_CLOSED", "active work-entity may not self-promote"
    if c.get("canonical_upgrade_authority") != "formalism-tests":
        return "FAIL_CLOSED", "canonical upgrade authority must remain formalism-tests"
    if c.get("site_claims_authority"):
        return "FAIL_CLOSED", "Site cannot become proof or release authority"
    if not c.get("source_release_hash_present"):
        return "FAIL_CLOSED", "source release hash missing"
    if c.get("queued_candidate_state") != "accepted_queue_entry":
        return "FAIL_CLOSED", "candidate is not an accepted queue entry"
    if c.get("review_state") != "accepted":
        return "FAIL_CLOSED", "candidate review is not accepted"
    if c.get("dependency_closure") != "closed":
        return "FAIL_CLOSED", "dependency closure is not closed"
    if not c.get("receipt_chain_valid"):
        return "FAIL_CLOSED", "receipt chain invalid"
    if not c.get("delta_manifest_present"):
        return "FAIL_CLOSED", "delta manifest missing"
    if not c.get("delta_manifest_hash_valid"):
        return "FAIL_CLOSED", "delta manifest hash invalid"
    if not c.get("replay_packet_present"):
        return "FAIL_CLOSED", "replay packet missing"
    if not c.get("lineage_continuity_valid"):
        return "FAIL_CLOSED", "release lineage continuity invalid"
    if c.get("requested_action") == "record_canonical_upgrade_delta":
        if c.get("ledger_record_required") and c.get("ledger_record_emitted"):
            return "LEDGER_CANONICAL_UPGRADE", "canonical upgrade delta ledger entry recorded"
        return "FAIL_CLOSED", "canonical upgrade ledger record missing"
    if c.get("requested_action") != "propose_release_candidate_delta":
        return "FAIL_CLOSED", "requested action is not an allowed Stage 13 delta action"
    return "ALLOW_RELEASE_CANDIDATE_DELTA", "active governed work-entity may propose release-candidate delta under formalism-tests authority"


def main():
    try:
        data = json.loads(FIXTURE.read_text())
        checks = 0
        receipts = []
        counts = {}
        cases = data["cases"]
        entity = data["work_entity"]

        checks += req(data.get("stage") == "Stage 13", "stage must be Stage 13")
        checks += req(data.get("source_release_id") == "transition-table-v1-rc1", "source release must be transition-table-v1-rc1")
        checks += req(data.get("target_release_id") == "transition-table-v1-rc2", "target release must be transition-table-v1-rc2")
        checks += req(entity.get("entity_status") == "active", "work-entity must be active")
        checks += req(entity.get("canonical_authority") is False, "work-entity must not be canonical authority")
        checks += req(entity.get("self_promotion_allowed") is False, "self-promotion must not be allowed")
        checks += req("formalism-tests" in data.get("authority_boundary", ""), "authority boundary must preserve formalism-tests authority")

        allowed_actions = set(entity.get("allowed_actions", []))
        checks += req("propose_release_candidate_delta" in allowed_actions, "Stage 13 delta action must be allowed")

        for control in data["required_controls"]:
            checks += req(isinstance(control, str) and control, "invalid required control")

        for c in cases:
            checks += req(c.get("candidate_id"), f"{c.get('case_id')}: missing candidate_id")
            checks += req(c.get("expected_decision"), f"{c.get('case_id')}: missing expected_decision")
            checks += req(c.get("source_release_id") == data["source_release_id"], f"{c.get('case_id')}: source release mismatch")
            checks += req(c.get("target_release_id") == data["target_release_id"], f"{c.get('case_id')}: target release mismatch")
            decision, basis = decide(c)
            checks += req(decision == c["expected_decision"], f"{c['case_id']}: expected {c['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage13_active_work_entity_release_delta_receipt.v1",
                "case_id": c["case_id"],
                "candidate_id": c["candidate_id"],
                "entity_id": c["entity_id"],
                "entity_alias": c.get("entity_alias"),
                "entity_status": c.get("entity_status"),
                "source_release_id": c["source_release_id"],
                "target_release_id": c["target_release_id"],
                "decision": decision,
                "basis": basis,
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required in ["ALLOW_RELEASE_CANDIDATE_DELTA", "FAIL_CLOSED", "LEDGER_CANONICAL_UPGRADE"]:
            checks += req(required in counts, f"missing decision coverage {required}")

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts))

        report = {
            "schema": "stegverse_stage13_active_work_entity_release_delta_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 13",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(cases),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "source_release_id": data["source_release_id"],
            "target_release_id": data["target_release_id"],
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "message": "Stage 13 active work-entity release-candidate delta validation passed.",
            "report": str(REPORT),
            "receipts": str(RECEIPTS)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as e:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage13_active_work_entity_release_delta_report.v1",
            "success": False,
            "error": str(e)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
