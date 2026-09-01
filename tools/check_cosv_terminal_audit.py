#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
idx=json.loads((ROOT/"data/cosv/task-vector-index.json").read_text())
registry=json.loads((ROOT/"data/formalism_proof_package_registry.json").read_text())
mindforge=json.loads((ROOT/"receipts/mindforge_boundary_semantics_canonical_execution_evidence.json").read_text())
handoff=(ROOT/"FORMALISM_TESTS_MIRROR_HANDOFF.md").read_text()

assert registry["active_issue_ownership"]==[]
assert len(registry["completed_issue_ownership"])==4
assert all(p["canonical_state"]=="VERIFIED_CANONICAL_RUN" for p in registry["packages"])
assert mindforge["status"]=="VERIFIED_CANONICAL_RUN"
assert mindforge["run_id"]==33463237601
assert all(v=="PASS" for v in mindforge["task_results"].values())
assert mindforge["artifact_equivalence"]["no_execution_invoked"] is True
assert "current structured active machine tasks: 0" in handoff\nassert "issue #8: CLOSED by repository-owned workflow" in handoff

assert idx["tasks"]==[]
cov=idx["coverage"]
assert cov["current_structured_active_tasks_audited"]==0
assert cov["current_structured_active_tasks_projected"]==0
assert cov["current_structured_active_task_gap"]==0
assert cov["repository_active_task_surface_audit_complete"] is True
assert cov["repository_no_active_task_surface_candidate"] is True
assert idx["authority_effect"]=="NONE"
print("FORMALISM_TESTS_COSV_TERMINAL_PASS active_tasks=0 no_active_task_surface_candidate=true")
