from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "stegverse001_bounded_autonomy_cases.json"
REPORT = ROOT / "reports" / "stage35_stegverse001_bounded_autonomy_report.json"
RECEIPTS = ROOT / "reports" / "stage35_stegverse001_bounded_autonomy_receipts.jsonl"

VOCAB = {"ALLOW","ALLOW_WITH_SIGNOFF","DENY","FAIL_CLOSED","REDIRECT","ESCALATE"}

def canon_hash(obj: Any) -> str:
    data=json.dumps(obj,sort_keys=True,separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(data).hexdigest()

def decide(lease: dict, case: dict) -> tuple[str,str]:
    mode=case["mode"]
    if mode=="DISCOVERY":
        return "REDIRECT","CANDIDATE_TASK_REQUIRES_ADMISSION"

    if case["lease_state"]!="ACTIVE":
        return "FAIL_CLOSED","LEASE_NOT_ACTIVE"
    if case["current_step"] >= lease["max_consequential_steps"]:
        return "FAIL_CLOSED","STEP_CEILING_EXCEEDED"
    if not case["denial_reachable"]:
        return "FAIL_CLOSED","DENIAL_NOT_REACHABLE"
    if not case["receipt_available"]:
        return "FAIL_CLOSED","RECEIPT_REQUIRED"

    tc=case["transition_class"]
    if tc in lease["forbidden_transition_classes"]:
        return "DENY","FORBIDDEN_TRANSITION_CLASS"
    if mode=="REPAIR":
        if not lease.get("repair_replanning_allowed",False):
            return "DENY","REPAIR_NOT_AUTHORIZED"
        if case["repair_widens_authority"]:
            return "DENY","REPAIR_AUTHORITY_WIDENING_FORBIDDEN"
        return "REDIRECT","NEAREST_ADMISSIBLE_REPAIR_SEARCH"

    if not case["authority_basis_present"]:
        return "DENY","AUTHORITY_BASIS_MISSING"
    if tc not in lease["allowed_transition_classes"]:
        return "DENY","TRANSITION_CLASS_NOT_ALLOWED"
    if tc in lease.get("review_trigger_transition_classes",[]) and not case["review_signoff"]:
        return "ALLOW_WITH_SIGNOFF","REVIEW_TRIGGER"

    return "ALLOW","LEASE_AND_COMMIT_BOUNDARY_SATISFIED"

def main() -> int:
    payload=json.loads(FIXTURE.read_text())
    lease=payload["lease"]
    results=[]
    all_pass=True
    for case in payload["cases"]:
        decision,reason=decide(lease,case)
        ok=decision==case["expected_decision"] and reason==case["expected_reason"] and decision in VOCAB
        if case.get("output_correct") and not case.get("authority_basis_present"):
            ok = ok and decision != "ALLOW"
        row={
            "case_id":case["id"],
            "name":case["name"],
            "decision":decision,
            "reason":reason,
            "expected_decision":case["expected_decision"],
            "expected_reason":case["expected_reason"],
            "output_correct":case.get("output_correct",False),
            "authorized_success": bool(decision=="ALLOW" and case.get("authority_basis_present")),
            "pass":ok,
        }
        row["receipt_hash"]=canon_hash(row)
        results.append(row)
        all_pass = all_pass and ok

    report={
        "schema":"stegverse.stage35.stegverse001-bounded-autonomy-report/v1",
        "stage":35,
        "goal_id":"STEGVERSE001-BOUNDED-AUTONOMY-001",
        "entity_id":"StegVerse-001",
        "entity_alias":"Beta_Orionis",
        "autonomy_posture":"BOUNDED_NON_SOVEREIGN",
        "lease_hash":canon_hash(lease),
        "case_count":len(results),
        "passed_count":sum(1 for r in results if r["pass"]),
        "failed_count":sum(1 for r in results if not r["pass"]),
        "results":results,
        "invariants":{
            "discovery_grants_execution_authority":False,
            "plan_selection_grants_execution_authority":False,
            "correct_output_proves_authorized_execution":False,
            "repair_may_widen_authority":False,
            "denial_must_remain_reachable":True,
            "receipts_required":True,
            "self_accreditation_allowed":False,
            "sovereign_authority_granted":False,
        },
        "success":all_pass,
        "authority_effect":"FORMALISM_TEST_EVIDENCE_ONLY",
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    with RECEIPTS.open("w",encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if all_pass else 1

if __name__=="__main__":
    raise SystemExit(main())
