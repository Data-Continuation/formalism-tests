#!/usr/bin/env python3
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage11_candidate_expansion_cases.json")
REPORT = Path("reports/stage11_candidate_expansion_governance_report.json")
RECEIPTS = Path("reports/stage11_candidate_expansion_governance_receipts.jsonl")

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def decide(c):
    if c.get("workflow_mutation_requested") and not c.get("human_or_core_review"):
        return "FAIL_CLOSED", "workflow mutation requires explicit review"
    if c.get("hidden_authority_claim"):
        return "FAIL_CLOSED", "hidden authority claim is not admissible"
    if c.get("site_claims_proof_authority"):
        return "FAIL_CLOSED", "Site mirror cannot become proof authority"
    if c.get("receipt_required") and not c.get("receipt_emitted"):
        return "FAIL_CLOSED", "required receipt missing"
    if c.get("dependency_closure") != "closed":
        return "FAIL_CLOSED", "dependency closure is not closed"
    if c.get("canonical_promotion_requested"):
        if c.get("promotion_authority") != "formalism-tests":
            return "FAIL_CLOSED", "canonical promotion requires formalism-tests authority"
        if c.get("review_state") != "accepted":
            return "FAIL_CLOSED", "canonical promotion requires accepted review state"
        return "ALLOW_RELEASE_QUEUE", "accepted candidate may enter release queue"
    if c.get("review_state") == "rejected":
        if c.get("ledger_record_required") and c.get("ledger_record_emitted"):
            return "LEDGER_REJECTION", "rejected candidate recorded in ledger"
        return "FAIL_CLOSED", "rejection missing ledger record"
    if c.get("review_state") == "superseded":
        if c.get("lineage_required") and c.get("lineage_record_emitted") and c.get("superseded_by"):
            return "LEDGER_SUPERSESSION", "supersession lineage recorded"
        return "FAIL_CLOSED", "supersession missing lineage"
    if c.get("candidate_scope") == "sandbox_only":
        return "ALLOW_SANDBOX", "candidate may remain inside sandbox scope"
    return "FAIL_CLOSED", "unrecognized candidate expansion path"

def main():
    try:
        data = json.loads(FIXTURE.read_text())
        checks = 0
        receipts = []
        counts = {}
        cases = data["cases"]
        checks += req(data["stage"] == "Stage 11", "stage must be Stage 11")
        checks += req(len(cases) == 10, "expected 10 cases")
        for control in data["required_controls"]:
            checks += req(isinstance(control, str) and control, "invalid control")
        for c in cases:
            checks += req(c.get("entity_id") == "StegVerse-001", "wrong entity")
            checks += req(c.get("candidate_id"), "missing candidate_id")
            checks += req(c.get("expected_decision"), "missing expected decision")
            decision, basis = decide(c)
            checks += req(decision == c["expected_decision"], f"{c['case_id']}: expected {c['expected_decision']}, got {decision}")
            receipt = {
                "schema": "stegverse_stage11_candidate_expansion_receipt.v1",
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
        for required in ["ALLOW_SANDBOX","ALLOW_RELEASE_QUEUE","FAIL_CLOSED","LEDGER_REJECTION","LEDGER_SUPERSESSION"]:
            checks += req(required in counts, f"missing decision coverage {required}")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts))
        report = {
            "schema": "stegverse_stage11_candidate_expansion_governance_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 11",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(cases),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "report": str(REPORT),
            "receipts": str(RECEIPTS),
            "message": "Stage 11 candidate expansion governance validation passed."
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as e:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {"schema": "stegverse_stage11_candidate_expansion_governance_report.v1", "success": False, "error": str(e)}
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
