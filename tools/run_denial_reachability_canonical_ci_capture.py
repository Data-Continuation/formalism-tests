#!/usr/bin/env python3
"""Run and capture denial-reachability canonical proof in repository-owned GitHub Actions."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST="tools/tasks/denial_reachability_tasks.json"
REPORT=ROOT/"reports/denial_reachability_report.json"
RECEIPTS=ROOT/"receipts/denial_reachability_execution_receipts.jsonl"
VERIFICATION=ROOT/"reports/denial_reachability_artifact_verification.json"
GATE=ROOT/"reports/denial_reachability_canonical_evidence_gate.json"
GATE_SOURCE=ROOT/"tools/check_denial_reachability_canonical_evidence_gate.py"
EVIDENCE=ROOT/"receipts/denial_reachability_canonical_execution_evidence.json"
EXPECTED=ROOT/"tests/fixtures/denial_reachability_expected_outcomes.json"
BASELINE=ROOT/"tests/fixtures/denial_reachability_artifact_baseline.json"
HANDOFF=ROOT/"docs/formalisms/DENIAL_REACHABILITY_MIRROR_HANDOFF.md"
AUTHORITY="REPRODUCTION_EVIDENCE_ONLY"
TASKS=("denial_reachability_commit_boundary_tests","verify_denial_reachability_artifacts","check_denial_reachability_canonical_evidence_gate")

def sha256(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(t): return [sys.executable,"tools/run_declared_tasks.py",MANIFEST,"--task-id",t]
def cmd_text(t): return f"python tools/run_declared_tasks.py {MANIFEST} --task-id {t}"
def run(t):
    if subprocess.run(cmd(t),cwd=ROOT).returncode: raise SystemExit(f"denial canonical task failed: {t}")
def env():
    if os.getenv("GITHUB_ACTIONS")!="true" or os.getenv("GITHUB_REF")!="refs/heads/main": raise SystemExit("canonical capture requires GitHub Actions main")
    s=os.getenv("GITHUB_SHA",""); r=os.getenv("GITHUB_RUN_ID","")
    if len(s)!=40 or any(c not in "0123456789abcdef" for c in s) or not r.isdigit(): raise SystemExit("invalid canonical run identity")
    return s,r
def append_handoff(s,r,h):
    text=HANDOFF.read_text()
    marker="## Canonical GitHub Actions execution observed"
    block=f"""\n{marker}\n\n```text
status: VERIFIED_CANONICAL_RUN
commit_sha: {s}
execution_surface: GITHUB_ACTIONS
run_id: {r}
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/{r}
task_results: 3/3 PASS
report_sha256: {h['report_sha256']}
receipts_sha256: {h['receipts_sha256']}
artifact_verification_sha256: {h['artifact_verification_sha256']}
canonical_evidence_gate_sha256: {h['canonical_evidence_gate_sha256']}
artifact_equivalence: report=true receipts=true expected_outcomes=true canonical_evidence_gate=true
authority_posture: {AUTHORITY}
```\n\nThis is bounded repository-owned canonical proof evidence only. It grants no execution, publication, certification, release, financial, sovereign, or downstream mutation authority.\n"""
    if marker in text: text=text.split(marker,1)[0].rstrip()+"\n"+block
    else: text=text.rstrip()+"\n"+block
    HANDOFF.write_text(text.rstrip()+"\n")
def main():
    s,r=env()
    committed_report=REPORT.read_bytes(); committed_receipts=RECEIPTS.read_bytes()
    run(TASKS[0])
    if REPORT.read_bytes()!=committed_report: raise SystemExit("generated denial report is not byte-equivalent to committed baseline output")
    if RECEIPTS.read_bytes()!=committed_receipts: raise SystemExit("generated denial receipts are not byte-equivalent to committed baseline output")
    run(TASKS[1])
    v=json.loads(VERIFICATION.read_text())
    if v.get("status")!="PASS" or v.get("byte_equivalence_to_baseline") is not True: raise SystemExit("denial artifact verification did not PASS")
    baseline=json.loads(BASELINE.read_text()); expected=json.loads(EXPECTED.read_text())
    if json.loads(REPORT.read_text()).get("report_sha256")!=baseline.get("proof_report_canonical_sha256"): raise SystemExit("denial canonical report hash mismatch")
    if not isinstance(expected.get("expected"),dict) or len(expected["expected"])!=5: raise SystemExit("denial expected outcome set invalid")
    hashes={"report_sha256":sha256(REPORT),"receipts_sha256":sha256(RECEIPTS),"artifact_verification_sha256":sha256(VERIFICATION),"canonical_evidence_gate_sha256":sha256(GATE_SOURCE)}
    ev={"schema":"stegverse.denial-reachability.canonical-execution-evidence.v1","suite_id":"denial-reachability-v0.1","repository":"Data-Continuation/formalism-tests","commit_sha":s,"execution_surface":"GITHUB_ACTIONS","commands":[cmd_text(t) for t in TASKS],"task_results":{t:"PASS" for t in TASKS},"artifact_hashes":hashes,"artifact_equivalence":{"report":True,"receipts":True,"expected_outcomes":True,"canonical_evidence_gate":True},"status":"VERIFIED_CANONICAL_RUN","authority_posture":AUTHORITY}
    EVIDENCE.write_text(json.dumps(ev,indent=2)+"\n")
    run(TASKS[2])
    g=json.loads(GATE.read_text())
    if g.get("status")!="PASS" or g.get("promotion_eligible") is not True: raise SystemExit("denial canonical gate did not PASS")
    append_handoff(s,r,hashes)
    print("DENIAL REACHABILITY CANONICAL CI CAPTURE: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
