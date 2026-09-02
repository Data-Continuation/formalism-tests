# Denial Reachability Mirror Handoff

## Source of truth

This file is the goal-specific continuation source of truth for the denial-reachability canonical proof package in `Data-Continuation/formalism-tests`. Repository-wide ownership remains subordinate to `FORMALISM_TESTS_MIRROR_HANDOFF.md` and the machine-readable proof-package registry.

## Goal

Complete issue #3 through the existing repository-owned CI surface without creating a duplicate workflow, while preserving the distinction between denial-reachability proof evidence and execution authority.

## Installed proof package

```text
tests/fixtures/denial_reachability_cases.json
tests/fixtures/denial_reachability_expected_outcomes.json
tests/fixtures/denial_reachability_artifact_baseline.json
tools/run_denial_reachability_tests.py
tools/verify_denial_reachability_artifacts.py
tools/check_denial_reachability_canonical_evidence_gate.py
tools/tasks/denial_reachability_tasks.json
reports/denial_reachability_report.json
receipts/denial_reachability_execution_receipts.jsonl
schemas/denial_reachability_canonical_execution_evidence.schema.json
receipts/denial_reachability_canonical_execution_evidence.pending.json
```

## Canonical owner

```text
repository: Data-Continuation/formalism-tests
issue: #3
state: VERIFIED_CANONICAL_RUN
approved existing CI: .github/workflows/continuation-tests.yml
duplicate workflow allowed: false
authority_posture: REPRODUCTION_EVIDENCE_ONLY
```

## Required machine execution

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id verify_denial_reachability_artifacts
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id check_denial_reachability_canonical_evidence_gate
```

Completion requires all three tasks PASS in one approved repository-owned execution; exact report and receipt byte equivalence to the committed deterministic baseline; a PASS artifact-verification report; four SHA-256 bindings for report, receipts, artifact verification, and committed canonical-evidence checker source; four equivalence assertions; schema-shaped `VERIFIED_CANONICAL_RUN` evidence; and issue #3 closure only after the durable evidence exists.

## Boundary

```text
reachable denial != cosmetic refusal
late refusal != prevented execution
reproduction evidence != canonical execution
canonical execution != downstream authority
canonical PASS != release
```

No result here grants execution, publication, certification, release, financial, sovereign, or downstream mutation authority.

## Repository-owned CI activation installed

Capture runner: `tools/run_denial_reachability_canonical_ci_capture.py` (`74188299448635cea882bf34dd82ddbeceaf9d3c`).
Existing workflow binding: `75e4689cb8444c867f67cb4345a53eac3379fa8c`.

The source integration is installed; hosted canonical execution remains pending until a workflow run completes the three-task/evidence contract.

## Next transition

Bind a canonical capture runner into the existing `continuation-tests.yml` workflow, observe the hosted run, preserve any first-attempt failure as historical evidence, repair only directly observed deterministic defects, and close issue #3 only after the full canonical contract passes.

## Archive posture

```text
archive_state: CANONICAL_SCOPE_COMPLETE_DOWNSTREAM_REVIEW_PENDING
manual_user_task: none
```

## Canonical GitHub Actions execution observed

```text
status: VERIFIED_CANONICAL_RUN
commit_sha: 88f9731525347612edf48a73002b883a82530f23
execution_surface: GITHUB_ACTIONS
run_id: 33651133645
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/33651133645
task_results: 3/3 PASS
report_sha256: f5a07da05497bdd8d85bd60e43ceb5d043eac656bad2f873a6d9aee2d65f95be
receipts_sha256: 9f1c0dc5463dc7396addf7a62147b8beb33f818b67add8f41bc069c96cef2953
artifact_verification_sha256: a6ae45547ce523e2455bf8bcc88cd5c4a7072e8bd49e98b055139fac5b7518bd
canonical_evidence_gate_sha256: 2fd95c240ac8cafba2a4082ac0eaa81a2b557bef3efb45e11daa9480c993af09
artifact_equivalence: report=true receipts=true expected_outcomes=true canonical_evidence_gate=true
authority_posture: REPRODUCTION_EVIDENCE_ONLY
```

This is bounded repository-owned canonical proof evidence only. It grants no execution, publication, certification, release, financial, sovereign, or downstream mutation authority.
