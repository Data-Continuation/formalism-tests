#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
INPUT_PATH=Path('tests/transition_table_cases.json')
RECEIPTS_PATH=Path('reports/transition_table_receipts.jsonl')
REPORT_PATH=Path('reports/transition_table_report.md')
REQUIRED_CONTRACT_FIELDS=['transition_id','transition_name','transition_family','theorem_basis','role','consequence_mass','legitimacy_capacity_required','recoverability_floor','recoverability_score','inference_window_minimum','inference_window_width','commit_time_state_required','pre_commit_state_hash','commit_state_hash','replay_semantics','boundary_behavior','multi_body_coupling_class','allowed_outcomes']
def score(value:Any,name:str)->float:
    if not isinstance(value,(int,float)): raise ValueError(f'{name} must be numeric')
    result=float(value)
    if result<0.0 or result>1.0: raise ValueError(f'{name} must be between 0 and 1')
    return result
def text(value:Any,name:str)->str:
    if not isinstance(value,str) or not value.strip(): raise ValueError(f'{name} must be a non-empty string')
    return value
def bool_value(value:Any,name:str)->bool:
    if not isinstance(value,bool): raise ValueError(f'{name} must be boolean')
    return value
def load_cases()->List[Dict[str,Any]]:
    payload=json.loads(INPUT_PATH.read_text(encoding='utf-8'))
    cases=payload.get('cases')
    if not isinstance(cases,list): raise ValueError('tests/transition_table_cases.json must contain a cases list')
    return cases
def validate_contract(case:Dict[str,Any])->List[str]: return [f for f in REQUIRED_CONTRACT_FIELDS if f not in case]
def decide(case:Dict[str,Any])->Dict[str,Any]:
    case_id=text(case.get('case_id'),'case_id'); missing=validate_contract(case)
    transition_id=text(case.get('transition_id'),'transition_id'); transition_name=text(case.get('transition_name'),'transition_name')
    transition_family=text(case.get('transition_family'),'transition_family'); theorem_basis=text(case.get('theorem_basis'),'theorem_basis'); role=text(case.get('role'),'role')
    consequence_mass=score(case.get('consequence_mass'),'consequence_mass'); legitimacy_capacity_required=score(case.get('legitimacy_capacity_required'),'legitimacy_capacity_required')
    recoverability_floor=score(case.get('recoverability_floor'),'recoverability_floor'); recoverability_score=score(case.get('recoverability_score'),'recoverability_score')
    inference_window_minimum=score(case.get('inference_window_minimum'),'inference_window_minimum'); inference_window_width=score(case.get('inference_window_width'),'inference_window_width')
    commit_time_state_required=bool_value(case.get('commit_time_state_required'),'commit_time_state_required')
    pre_commit_state_hash=text(case.get('pre_commit_state_hash'),'pre_commit_state_hash'); commit_state_hash=text(case.get('commit_state_hash'),'commit_state_hash')
    replay_semantics=text(case.get('replay_semantics'),'replay_semantics'); boundary_behavior=text(case.get('boundary_behavior'),'boundary_behavior')
    multi_body_coupling_class=text(case.get('multi_body_coupling_class'),'multi_body_coupling_class')
    allowed_outcomes=case.get('allowed_outcomes')
    if not isinstance(allowed_outcomes,list) or not all(isinstance(x,str) for x in allowed_outcomes): raise ValueError(f'{case_id}: allowed_outcomes must be a string list')
    basis=[]; decision='ALLOW'
    if missing: decision='FAIL_CLOSED'; basis.append('transition class is missing required admissibility contract fields')
    elif consequence_mass>legitimacy_capacity_required: decision='FAIL_CLOSED'; basis.append('composite consequence mass exceeds legitimacy capacity')
    elif commit_time_state_required and pre_commit_state_hash!=commit_state_hash: decision='FAIL_CLOSED'; basis.append('commit-time state drift detected')
    elif inference_window_width<inference_window_minimum: decision='FAIL_CLOSED'; basis.append('inference window collapsed below transition-class minimum')
    elif recoverability_score<recoverability_floor: decision='FAIL_CLOSED'; basis.append('recoverability score below transition-class floor')
    elif replay_semantics=='reverse_attempt': decision='FAIL_CLOSED'; basis.append('transition-class replay semantics prohibit reversal')
    else: basis.append('transition class admissibility contract satisfied')
    if decision not in allowed_outcomes: decision='FAIL_CLOSED'; basis.append('computed outcome is not allowed by transition class')
    expected_decision=text(case.get('expected_decision'),'expected_decision'); expected_basis_contains=text(case.get('expected_basis_contains'),'expected_basis_contains')
    return {'receipt_id':f'stage4-{case_id}','case_id':case_id,'transition_id':transition_id,'transition_name':transition_name,'transition_family':transition_family,'theorem_basis':theorem_basis,'role':role,'decision':decision,'basis':basis,'matched_expected_decision':decision==expected_decision,'matched_expected_basis':any(expected_basis_contains in item for item in basis),'admissibility_contract':{'consequence_mass':consequence_mass,'legitimacy_capacity_required':legitimacy_capacity_required,'recoverability_floor':recoverability_floor,'recoverability_score':recoverability_score,'inference_window_minimum':inference_window_minimum,'inference_window_width':inference_window_width,'commit_time_state_required':commit_time_state_required,'replay_semantics':replay_semantics,'boundary_behavior':boundary_behavior,'multi_body_coupling_class':multi_body_coupling_class,'allowed_outcomes':allowed_outcomes},'state':{'pre_commit_state_hash':pre_commit_state_hash,'commit_state_hash':commit_state_hash}}
def write_receipts(receipts):
    RECEIPTS_PATH.parent.mkdir(parents=True,exist_ok=True)
    with RECEIPTS_PATH.open('w',encoding='utf-8') as h:
        for receipt in receipts: h.write(json.dumps(receipt,sort_keys=True)+'\n')
def count_by_decision(receipts):
    counts={}
    for receipt in receipts: counts[receipt['decision']]=counts.get(receipt['decision'],0)+1
    return counts
def row(values): return '| '+' | '.join(str(v) for v in values)+' |'
def write_report(receipts):
    REPORT_PATH.parent.mkdir(parents=True,exist_ok=True)
    success=all(r['matched_expected_decision'] and r['matched_expected_basis'] for r in receipts); counts=count_by_decision(receipts)
    lines=['# Stage 4 Transition Table Integration Report','','## Public proof claim','','```text','A transition class is valid only if its admissibility contract specifies the conditions under which the transition may bind consequence.','```','','## Verification status','',f'Success: `{str(success).lower()}`','','## Decision summary','','| Decision | Count |','|---|---:|']
    for decision in sorted(counts): lines.append(row([decision,counts[decision]]))
    lines+=['','## Transition class receipts','','| Receipt | Transition ID | Family | Theorem basis | Coupling class | Decision | Basis |','|---|---|---|---|---|---|---|']
    for receipt in receipts:
        contract=receipt['admissibility_contract']; lines.append(row([receipt['receipt_id'],receipt['transition_id'],receipt['transition_family'],receipt['theorem_basis'],contract['multi_body_coupling_class'],receipt['decision'],'; '.join(receipt['basis'])]))
    lines+=['','## Interpretation','','Stage 4 turns Stage 3 continuation proofs into executable transition-table classes.','','The transition table is no longer only descriptive. Each transition class now carries an admissibility contract containing consequence mass, required legitimacy capacity, recoverability floor, inference-window minimum, commit-time state requirements, replay semantics, boundary behavior, coupling class, and allowed outcomes.','','This supports the construction of a transition periodic table in which each transition type is a governed consequence-binding class rather than a label.','']
    REPORT_PATH.write_text('\n'.join(lines),encoding='utf-8')
def main():
    receipts=[decide(c) for c in load_cases()]; write_receipts(receipts); write_report(receipts)
    success=all(r['matched_expected_decision'] and r['matched_expected_basis'] for r in receipts)
    print(json.dumps({'stage':'stage_4_transition_table_integration','receipt_count':len(receipts),'success':success,'receipts_path':str(RECEIPTS_PATH),'report_path':str(REPORT_PATH)},indent=2,sort_keys=True))
    return 0 if success else 1
if __name__=='__main__': raise SystemExit(main())
