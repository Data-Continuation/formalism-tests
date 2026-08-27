#!/usr/bin/env python3
"""Run and capture FI continuity interoperability canonical proof in repository-owned GitHub Actions."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST="tools/tasks/fi_transition_continuity_interop_tasks.json"
REPORT=ROOT/"reports/fi_transition_continuity_interop_report.json"
VERIFICATION=ROOT/"reports/fi_transition_continuity_interop_artifact_verification.json"
GATE=ROOT/"reports/fi_transition_continuity_interop_canonical_evidence_gate.json"
EVIDENCE=ROOT/"receipts/fi_transition_continuity_interop_canonical_execution_evidence.json"
EXPECTED=ROOT/"tests/fixtures/fi_transition_continuity_interop_expected_outcomes.json"
BASELINE=ROOT/"tests/fixtures/fi_transition_continuity_interop_artifact_baseline.json"
HANDOFF=ROOT/"docs/formalisms/FI_TRANSITION_CONTINUITY_INTEROP_MIRROR_HANDOFF.md"
AUTHORITY="CONTINUITY_INTEROPERABILITY_ONLY"
TASKS=("fi_transition_continuity_interop_tests","verify_fi_transition_continuity_interop_artifacts","check_fi_transition_continuity_interop_canonical_evidence_gate")

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canonical(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def cmd(t): return [sys.executable,"tools/run_declared_tasks.py",MANIFEST,"--task-id",t]
def cmd_text(t): return f"python tools/run_declared_tasks.py {MANIFEST} --task-id {t}"
def run(t):
    if subprocess.run(cmd(t),cwd=ROOT).returncode: raise SystemExit(f"FI canonical task failed: {t}")
def env():
    if os.getenv("GITHUB_ACTIONS")!="true" or os.getenv("GITHUB_REF")!="refs/heads/main": raise SystemExit("canonical capture requires GitHub Actions main")
    s=os.getenv("GITHUB_SHA",""); r=os.getenv("GITHUB_RUN_ID","")
    if len(s)!=40 or any(c not in "0123456789abcdef" for c in s) or not r.isdigit(): raise SystemExit("invalid canonical run identity")
    return s,r
def expected_gate_bytes():
    p={"authority_posture":AUTHORITY,"errors":[],"mode":"CANONICAL_EVIDENCE_PRESENT","promotion_eligible":True,"schema":"stegverse.fi-transition-continuity-interop.canonical-evidence-gate-result.v1","status":"PASS"}
    return (json.dumps(p,indent=2,sort_keys=True)+"\n").encode()
def append_handoff(s,r,h):
    text=HANDOFF.read_text(); marker="## Canonical GitHub Actions execution observed"
    block=f"""\n{marker}\n\n```text
status: VERIFIED_CANONICAL_RUN
commit_sha: {s}
execution_surface: GITHUB_ACTIONS
run_id: {r}
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/{r}
task_results: 3/3 PASS
report_sha256: {h['report_sha256']}
artifact_verification_sha256: {h['artifact_verification_sha256']}
canonical_evidence_gate_sha256: {h['canonical_evidence_gate_sha256']}
artifact_equivalence: report=true expected_outcomes=true canonical_evidence_gate=true
authority_posture: {AUTHORITY}
```\n\nThis is bounded continuity-interoperability proof evidence only. It establishes neither cross-domain support nor universal-law, production, publication, certification, release, or execution authority.\n"""
    if marker in text: text=text.split(marker,1)[0].rstrip()+"\n"+block
    else: text=text.rstrip()+"\n"+block
    HANDOFF.write_text(text.rstrip()+"\n")
def main():
    s,r=env()
    run(TASKS[0])
    report=json.loads(REPORT.read_text()); baseline=json.loads(BASELINE.read_text()); expected=json.loads(EXPECTED.read_text())
    if report.get("status")!="PASS" or report.get("passed")!=4 or report.get("failed")!=0: raise SystemExit("FI report did not preserve 4/4 PASS")
    if canonical(report)!=baseline.get("canonical_report_sha256"): raise SystemExit("FI canonical report hash mismatch")
    if report.get("suite_id")!=expected.get("suite_id"): raise SystemExit("FI expected-outcome suite mismatch")
    run(TASKS[1])
    v=json.loads(VERIFICATION.read_text())
    if v.get("valid") is not True: raise SystemExit("FI artifact verification did not PASS")
    gate_bytes=expected_gate_bytes()
    hashes={"report_sha256":sha256(REPORT),"artifact_verification_sha256":sha256(VERIFICATION),"canonical_evidence_gate_sha256":hashlib.sha256(gate_bytes).hexdigest()}
    ev={"schema":"stegverse.fi-transition-continuity-interop.canonical-execution-evidence.v1","suite_id":"fi-transition-continuity-interoperability-v0.1","repository":"Data-Continuation/formalism-tests","issue":4,"status":"VERIFIED_CANONICAL_RUN","authority_posture":AUTHORITY,"commit_sha":s,"execution_surface":"GITHUB_ACTIONS","commands":[cmd_text(t) for t in TASKS],"task_results":{t:"PASS" for t in TASKS},"artifact_hashes":hashes,"artifact_equivalence":{"report":True,"expected_outcomes":True,"canonical_evidence_gate":True}}
    EVIDENCE.write_text(json.dumps(ev,indent=2)+"\n")
    run(TASKS[2])
    if GATE.read_bytes()!=gate_bytes: raise SystemExit("FI canonical gate output differs from pre-bound deterministic PASS output")
    append_handoff(s,r,hashes)
    print("FI CONTINUITY INTEROP CANONICAL CI CAPTURE: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
