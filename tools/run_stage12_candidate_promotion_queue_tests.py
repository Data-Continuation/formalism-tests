#!/usr/bin/env python3
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage12_candidate_promotion_queue_cases.json")
REPORT = Path("reports/stage12_candidate_promotion_queue_report.json")
RECEIPTS = Path("reports/stage12_candidate_promotion_queue_receipts.jsonl")

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def decide(c):
    if c.get("dependency_closure") != "closed":
        return "FAIL_CLOSED", "dependency closure is not closed"
    if c.get("review_state") != "accepted":
        return "FAIL_CLOSED", "candidate review is not accepted"
    if c.get("receipt_required") and not c.get("receipt_emitted"):
        return "FAIL_CLOSED", "required receipt missing"
    if c.get("promotion_authority") != "formalism-tests":
        return "FAIL_CLOSED", "promotion authority must be formalism-tests"
    if c.get("site_claims_authority"):
        return "FAIL_CLOSED", "Site cannot become proof or release authority"
    if not c.get("release_manifest_present"):
        return "FAIL_CLOSED", "release manifest missing"
    if not c.get("release_manifest_hash_valid"):
        return "FAIL_CLOSED", "release manifest hash invalid"
    if c.get("candidate_state") == "superseded" and not c.get("supersession_lineage_valid"):
        return "FAIL_CLOSED", "supersession lineage invalid"
    if c.get("release_queue_action") == "record_queue_entry":
        if c.get("ledger_record_required") and c.get("ledger_record_emitted"):
            return "LEDGER_QUEUE_ENTRY", "release queue entry recorded"
        return "FAIL_CLOSED", "queue ledger record missing"
    return "ALLOW_QUEUE_ENTRY", "candidate may enter governed release queue"

def main():
    try:
        data = json.loads(FIXTURE.read_text())
        checks = 0
        receipts = []
        counts = {}
        cases = data["cases"]

        checks += req(data.get("stage") == "Stage 12", "stage must be Stage 12")
        checks += req(len(cases) >= 10, "expected at least 10 cases")
        checks += req("formalism-tests authority" in data.get("authority_boundary", ""), "authority boundary missing formalism-tests authority")

        for control in data["required_controls"]:
            checks += req(isinstance(control, str) and control, "invalid required control")

        for c in cases:
            checks += req(c.get("entity_id") == "StegVerse-001", f"{c.get('case_id')}: wrong entity")
            checks += req(c.get("candidate_id"), f"{c.get('case_id')}: missing candidate_id")
            checks += req(c.get("expected_decision"), f"{c.get('case_id')}: missing expected_decision")
            decision, basis = decide(c)
            checks += req(decision == c["expected_decision"], f"{c['case_id']}: expected {c['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage12_candidate_promotion_queue_receipt.v1",
                "case_id": c["case_id"],
                "candidate_id": c["candidate_id"],
                "entity_id": c["entity_id"],
                "decision": decision,
                "basis": basis,
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required in ["ALLOW_QUEUE_ENTRY", "FAIL_CLOSED", "LEDGER_QUEUE_ENTRY"]:
            checks += req(required in counts, f"missing decision coverage {required}")

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts))

        report = {
            "schema": "stegverse_stage12_candidate_promotion_queue_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 12",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(cases),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "message": "Stage 12 governed candidate promotion and release queue validation passed.",
            "report": str(REPORT),
            "receipts": str(RECEIPTS)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as e:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {"schema": "stegverse_stage12_candidate_promotion_queue_report.v1", "success": False, "error": str(e)}
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
