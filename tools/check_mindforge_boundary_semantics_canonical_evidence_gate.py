#!/usr/bin/env python3
"""Fail-closed gate for MindForge canonical execution evidence."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PENDING=ROOT/"receipts/mindforge_boundary_semantics_canonical_execution_evidence.pending.json"
CANONICAL=ROOT/"receipts/mindforge_boundary_semantics_canonical_execution_evidence.json"
VERIFY=ROOT/"reports/mindforge_boundary_semantics_artifact_verification.json"
REPORT=ROOT/"reports/mindforge_boundary_semantics_report.json"
RECEIPTS=ROOT/"receipts/mindforge_boundary_semantics_execution_receipts.jsonl"
EXPECTED=ROOT/"tests/fixtures/mindforge_boundary_semantics_expected_outcomes.json"
OUTPUT=ROOT/"reports/mindforge_boundary_semantics_canonical_evidence_gate.json"
AUTHORITY="ARCHITECTURAL_BOUNDARY_SEMANTICS_ONLY"
SHA40=re.compile(r"^[0-9a-f]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")
TASKS=[
 "mindforge_boundary_semantics_tests",
 "verify_mindforge_boundary_semantics_artifacts",
 "check_mindforge_boundary_semantics_canonical_evidence_gate",
]
COMMANDS=[
 "python tools/run_declared_tasks.py tools/tasks/mindforge_boundary_semantics_tasks.json --task-id "+t
 for t in TASKS
]
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def main():
    errors=[]
    mode="CANONICAL_EVIDENCE_PRESENT" if CANONICAL.exists() else "PENDING_FAIL_CLOSED"
    if mode=="PENDING_FAIL_CLOSED":
        p=load(PENDING)
        if p.get("status")!="PENDING_CANONICAL_EXECUTION": errors.append("pending status mismatch")
        if p.get("authority_posture")!=AUTHORITY: errors.append("pending authority mismatch")
        if p.get("required_commands")!=COMMANDS: errors.append("pending commands mismatch")
        if p.get("promotion_prohibited_until_complete") is not True: errors.append("pending must prohibit promotion")
    else:
        c=load(CANONICAL)
        if c.get("schema")!="stegverse.mindforge-boundary-semantics.canonical-execution-evidence.v1": errors.append("canonical schema mismatch")
        if c.get("suite_id")!="mindforge-boundary-semantics-v1": errors.append("canonical suite mismatch")
        if c.get("repository")!="Data-Continuation/formalism-tests": errors.append("canonical repository mismatch")
        if not SHA40.fullmatch(str(c.get("commit_sha",""))): errors.append("canonical commit invalid")
        if c.get("execution_surface")!="GITHUB_ACTIONS": errors.append("canonical execution surface invalid")
        if not isinstance(c.get("run_id"),int) or c["run_id"]<1: errors.append("canonical run_id invalid")
        if c.get("commands")!=COMMANDS: errors.append("canonical commands mismatch")
        tr=c.get("task_results",{})
        if set(tr)!=set(TASKS) or any(tr.get(t)!="PASS" for t in TASKS): errors.append("canonical task results must all PASS")
        if c.get("status")!="VERIFIED_CANONICAL_RUN": errors.append("canonical status mismatch")
        if c.get("authority_posture")!=AUTHORITY: errors.append("canonical authority mismatch")
        v=load(VERIFY)
        if v.get("status")!="PASS": errors.append("artifact verification not PASS")
        eq=c.get("artifact_equivalence",{})
        for key in ("report_receipt_equivalence","expected_outcome_equivalence","no_execution_invoked"):
            if eq.get(key) is not True or v.get(key) is not True: errors.append(f"equivalence {key} not true")
        hashes=c.get("artifact_hashes",{})
        expected_hashes={
          "report_sha256":sha256(REPORT),
          "receipts_sha256":sha256(RECEIPTS),
          "expected_outcomes_sha256":sha256(EXPECTED),
          "artifact_verification_sha256":sha256(VERIFY),
        }
        if set(hashes)!=set(expected_hashes): errors.append("canonical hash fields mismatch")
        for k,val in expected_hashes.items():
            if not SHA64.fullmatch(str(hashes.get(k,""))) or hashes.get(k)!=val:
                errors.append(f"canonical hash mismatch: {k}")
    result={
      "schema":"stegverse.mindforge-boundary-semantics.canonical-evidence-gate-result.v1",
      "mode":mode,
      "status":"PASS" if not errors else "FAIL",
      "promotion_eligible":mode=="CANONICAL_EVIDENCE_PRESENT" and not errors,
      "authority_posture":AUTHORITY,
      "errors":errors,
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
