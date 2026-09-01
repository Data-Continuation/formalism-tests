#!/usr/bin/env python3
"""Capture MindForge boundary semantics as repository-owned canonical evidence on main."""
from __future__ import annotations
import hashlib,json,os,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST="tools/tasks/mindforge_boundary_semantics_tasks.json"
REPORT=ROOT/"reports/mindforge_boundary_semantics_report.json"
RECEIPTS=ROOT/"receipts/mindforge_boundary_semantics_execution_receipts.jsonl"
EXPECTED=ROOT/"tests/fixtures/mindforge_boundary_semantics_expected_outcomes.json"
VERIFY=ROOT/"reports/mindforge_boundary_semantics_artifact_verification.json"
GATE=ROOT/"reports/mindforge_boundary_semantics_canonical_evidence_gate.json"
EVIDENCE=ROOT/"receipts/mindforge_boundary_semantics_canonical_execution_evidence.json"
HANDOFF=ROOT/"docs/formalisms/MINDFORGE_BOUNDARY_SEMANTICS_MIRROR_HANDOFF.md"
AUTHORITY="ARCHITECTURAL_BOUNDARY_SEMANTICS_ONLY"
TASKS=[
 "mindforge_boundary_semantics_tests",
 "verify_mindforge_boundary_semantics_artifacts",
 "check_mindforge_boundary_semantics_canonical_evidence_gate",
]
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def command(t): return [sys.executable,"tools/run_declared_tasks.py",MANIFEST,"--task-id",t]
def command_text(t): return f"python tools/run_declared_tasks.py {MANIFEST} --task-id {t}"
def run(t):
    cp=subprocess.run(command(t),cwd=ROOT)
    if cp.returncode: raise SystemExit(f"MindForge canonical task failed: {t}")
def canonical_env():
    if os.getenv("GITHUB_ACTIONS")!="true" or os.getenv("GITHUB_REF")!="refs/heads/main":
        raise SystemExit("MindForge canonical capture requires GitHub Actions on main")
    sha=os.getenv("GITHUB_SHA","")
    run_id=os.getenv("GITHUB_RUN_ID","")
    if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha):
        raise SystemExit("invalid GITHUB_SHA")
    if not run_id.isdigit():
        raise SystemExit("invalid GITHUB_RUN_ID")
    return sha,int(run_id)
def update_handoff(commit_sha,run_id,evidence):
    text=HANDOFF.read_text()
    marker="## Canonical repository-owned execution evidence"
    block=f"""\n{marker}\n\n```text
status: VERIFIED_CANONICAL_RUN
commit_sha: {commit_sha}
run_id: {run_id}
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/{run_id}
execution_surface: GITHUB_ACTIONS
task_results: 3/3 PASS
report_sha256: {evidence['artifact_hashes']['report_sha256']}
receipts_sha256: {evidence['artifact_hashes']['receipts_sha256']}
expected_outcomes_sha256: {evidence['artifact_hashes']['expected_outcomes_sha256']}
artifact_verification_sha256: {evidence['artifact_hashes']['artifact_verification_sha256']}
report_receipt_equivalence: true
expected_outcome_equivalence: true
no_execution_invoked: true
authority_posture: {AUTHORITY}
```

This satisfies the repository-local canonical-execution portion of issue #8. It does not create
MindForge specification authority, implementation certification, execution authority, release
authority, publication authority, or admissibility authority. Downstream reference transfer remains
bounded to immutable evidence references.
"""
    if marker in text:
        text=text.split(marker,1)[0].rstrip()+"\n"+block
    else:
        text=text.rstrip()+"\n"+block
    HANDOFF.write_text(text.rstrip()+"\n")
def main():
    commit_sha,run_id=canonical_env()
    run(TASKS[0])
    run(TASKS[1])
    v=json.loads(VERIFY.read_text())
    if v.get("status")!="PASS": raise SystemExit("MindForge artifact verification not PASS")
    hashes={
      "report_sha256":sha256(REPORT),
      "receipts_sha256":sha256(RECEIPTS),
      "expected_outcomes_sha256":sha256(EXPECTED),
      "artifact_verification_sha256":sha256(VERIFY),
    }
    evidence={
      "schema":"stegverse.mindforge-boundary-semantics.canonical-execution-evidence.v1",
      "suite_id":"mindforge-boundary-semantics-v1",
      "repository":"Data-Continuation/formalism-tests",
      "commit_sha":commit_sha,
      "execution_surface":"GITHUB_ACTIONS",
      "run_id":run_id,
      "commands":[command_text(t) for t in TASKS],
      "task_results":{t:"PASS" for t in TASKS},
      "artifact_hashes":hashes,
      "artifact_equivalence":{
        "report_receipt_equivalence":True,
        "expected_outcome_equivalence":True,
        "no_execution_invoked":True,
      },
      "status":"VERIFIED_CANONICAL_RUN",
      "authority_posture":AUTHORITY,
    }
    EVIDENCE.write_text(json.dumps(evidence,indent=2)+"\n")
    run(TASKS[2])
    gate=json.loads(GATE.read_text())
    if gate.get("status")!="PASS" or gate.get("promotion_eligible") is not True:
        raise SystemExit("MindForge canonical evidence gate did not PASS")
    update_handoff(commit_sha,run_id,evidence)
    print("MINDFORGE CANONICAL CI CAPTURE: PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
