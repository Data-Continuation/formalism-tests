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
state: PENDING_CANONICAL_EXECUTION
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

## Next transition

Bind a canonical capture runner into the existing `continuation-tests.yml` workflow, observe the hosted run, preserve any first-attempt failure as historical evidence, repair only directly observed deterministic defects, and close issue #3 only after the full canonical contract passes.

## Archive posture

```text
archive_state: NOT_READY_WHILE_CANONICAL_EXECUTION_PENDING
manual_user_task: none
```
