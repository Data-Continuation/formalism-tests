#!/usr/bin/env python3
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
FIXTURE=Path("tests/fixtures/stage15_active_work_entity_test_execution_cases.json")
REPORT=Path("reports/stage15_active_work_entity_test_execution_report.json")
RECEIPTS=Path("reports/stage15_active_work_entity_test_execution_receipts.jsonl")
EXPECTED_RUNNER="tools/run_declared_tasks.py"; EXPECTED_MANIFEST="tools/tasks/formalism_tests_tasks.json"; EXPECTED_AUTHORITY="formalism-tests"
def canon(o): return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def digest(o): return hashlib.sha256(canon(o).encode()).hexdigest()
def req(ok,msg):
    if not ok: raise AssertionError(msg)
    return 1
def decide(c):
    if c.get("entity_id")!="StegVerse-001": return "FAIL_CLOSED","unknown work-entity"
    if not c.get("entity_active"): return "FAIL_CLOSED","work-entity is not active"
    if not c.get("transition_table_bound"): return "FAIL_CLOSED","work-entity is not bound to the Transition Table"
    if not c.get("policy_scope_valid"): return "FAIL_CLOSED","declared policy scope is not valid"
    if not c.get("governed_by_all_applicable_ai_transitions"): return "FAIL_CLOSED","not governed by all applicable AI-governance transitions"
    if c.get("execution_authority")!=EXPECTED_AUTHORITY: return "FAIL_CLOSED","test execution authority must remain formalism-tests"
    if c.get("runner")!=EXPECTED_RUNNER: return "FAIL_CLOSED","next-stage execution must use the declared-task runner"
    if c.get("manifest_path")!=EXPECTED_MANIFEST: return "FAIL_CLOSED","next-stage execution must use the declared task manifest"
    if not c.get("target_task_declared"): return "FAIL_CLOSED","target task_id is not declared in the manifest"
    if c.get("receipt_required") and not c.get("receipt_emitted"): return "FAIL_CLOSED","required execution receipt missing"
    if c.get("report_required") and not c.get("report_emitted"): return "FAIL_CLOSED","required execution report missing"
    if c.get("canonical_mutation_requested"): return "FAIL_CLOSED","test execution may not mutate canonical release artifacts"
    if c.get("site_claims_authority"): return "FAIL_CLOSED","Site cannot become test, proof, or release authority"
    if c.get("execution_action")=="record_test_execution":
        if c.get("ledger_record_required") and c.get("ledger_record_emitted"): return "LEDGER_TEST_EXECUTION","active work-entity test execution ledger entry recorded"
        return "FAIL_CLOSED","test execution ledger record missing"
    if c.get("execution_action")=="run_declared_task": return "ALLOW_TEST_EXECUTION","active work-entity may run declared next-stage tests under formalism-tests authority"
    return "FAIL_CLOSED","unknown execution action"
def main():
    try:
        data=json.loads(FIXTURE.read_text()); checks=0; receipts=[]; counts={}; cases=data["cases"]
        checks+=req(data.get("stage")=="Stage 15","stage must be Stage 15")
        checks+=req(data.get("work_entity",{}).get("entity_id")=="StegVerse-001","work entity must be StegVerse-001")
        checks+=req(data.get("work_entity",{}).get("active") is True,"work entity must be active")
        checks+=req(data.get("work_entity",{}).get("transition_table_bound") is True,"work entity must be transition-table-bound")
        checks+=req(data.get("declared_runner")==EXPECTED_RUNNER,"declared runner mismatch")
        checks+=req(data.get("declared_manifest")==EXPECTED_MANIFEST,"declared manifest mismatch")
        checks+=req(len(cases)>=10,"expected at least 10 cases")
        for control in ["active_work_entity_required","transition_table_binding_required","ai_governance_transition_scope_required","declared_policy_scope_required","formalism_tests_execution_authority_required","declared_task_runner_required","declared_manifest_required","declared_task_id_required","no_canonical_mutation_during_test_execution","site_mirror_not_authority"]:
            checks+=req(control in data.get("required_controls",[]),f"missing required control: {control}")
        for transition in ["active_work_entity_execution","transition_table_binding","policy_scope_evolution"]:
            checks+=req(transition in data.get("applicable_ai_governance_transitions",[]),f"missing applicable AI governance transition: {transition}")
        for c in cases:
            cid=c.get("case_id","<missing>"); checks+=req(c.get("target_stage"),f"{cid}: missing target_stage"); checks+=req(c.get("target_task_id"),f"{cid}: missing target_task_id"); checks+=req(c.get("expected_decision"),f"{cid}: missing expected_decision")
            decision,basis=decide(c); checks+=req(decision==c["expected_decision"],f"{cid}: expected {c['expected_decision']}, got {decision}")
            r={"schema":"stegverse_stage15_active_work_entity_test_execution_receipt.v1","case_id":cid,"entity_id":c["entity_id"],"target_stage":c["target_stage"],"target_task_id":c["target_task_id"],"decision":decision,"basis":basis,"authority_boundary":data["authority_boundary"]}; r["receipt_hash"]=digest(r); receipts.append(r); counts[decision]=counts.get(decision,0)+1
        for d in ["ALLOW_TEST_EXECUTION","FAIL_CLOSED","LEDGER_TEST_EXECUTION"]: checks+=req(d in counts,f"missing decision coverage {d}")
        REPORT.parent.mkdir(parents=True,exist_ok=True); RECEIPTS.parent.mkdir(parents=True,exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in receipts))
        report={"schema":"stegverse_stage15_active_work_entity_test_execution_report.v1","success":True,"generated_at":datetime.now(timezone.utc).isoformat(),"stage":"Stage 15","theorem_basis":data["theorem_basis"],"assertion_count":checks,"case_count":len(cases),"receipt_count":len(receipts),"decision_counts":counts,"work_entity":"StegVerse-001 / Beta_Orionis","message":"Stage 15 active work-entity next-stage test execution validation passed.","report":str(REPORT),"receipts":str(RECEIPTS)}
        REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); print(json.dumps(report,indent=2,sort_keys=True)); return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True,exist_ok=True); report={"schema":"stegverse_stage15_active_work_entity_test_execution_report.v1","success":False,"error":str(exc)}; REPORT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n"); print(json.dumps(report,indent=2,sort_keys=True)); return 1
if __name__=="__main__": sys.exit(main())
