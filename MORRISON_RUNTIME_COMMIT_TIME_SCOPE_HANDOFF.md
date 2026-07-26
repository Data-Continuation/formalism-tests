# Morrison Runtime Commit-Time Scope Handoff

## Current source of truth

This file is the goal-specific continuation source of truth for the Morrison Runtime commit-time scope proof package in `Data-Continuation/formalism-tests`.

## Goal

Establish executable, deterministic comparative evidence for the distinction between:

1. a second pre-execution governance decision under configured constraints; and
2. full fresh-state reconstruction with evidence binding at the consequence-binding commit boundary.

The first does not by itself prove the second.

## Installed proof surface

```text
tests/fixtures/morrison_runtime_commit_time_scope_cases.json
tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json
tests/fixtures/morrison_runtime_commit_time_scope_artifact_baseline.json
tools/run_morrison_runtime_commit_time_scope.py
tools/verify_morrison_runtime_commit_time_scope_artifacts.py
tools/tasks/morrison_runtime_commit_time_scope_tasks.json
reports/morrison_runtime_commit_time_scope_report.json
reports/morrison_runtime_commit_time_scope_artifact_verification.json
reports/morrison_runtime_commit_time_scope_continuation_report.md
receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl
receipts/morrison_runtime_commit_time_scope_connector_snapshot_run.json
receipts/morrison_runtime_commit_time_scope_canonical_run_request.json
receipts/morrison_runtime_commit_time_scope_downstream_activation_contract.json
receipts/morrison_runtime_commit_time_scope_orchestration_status.json
```

## Declared tasks

```bash
python tools/run_declared_tasks.py tools/tasks/morrison_runtime_commit_time_scope_tasks.json --task-id morrison_runtime_commit_time_scope_tests
python tools/run_declared_tasks.py tools/tasks/morrison_runtime_commit_time_scope_tasks.json --task-id verify_morrison_runtime_commit_time_scope_artifacts
```

## Required cases

```text
MRG-CT-001 ALLOW_TO_BLOCK_CONTRADICTORY_EVIDENCE -> DENY
MRG-CT-002 BLOCK_TO_ALLOW_CORRECTIVE_EVIDENCE -> ALLOW
MRG-CT-003 MISSING_REQUIRED_EVIDENCE_FAIL_CLOSED -> FAIL_CLOSED
MRG-CT-004 UNKNOWN_EVIDENCE_COVERAGE_FAIL_CLOSED -> FAIL_CLOSED
MRG-CT-005 STALE_CACHED_BINDING_FAIL_CLOSED -> FAIL_CLOSED
MRG-CT-006 PREVIOUSLY_UNMODELED_PARAMETER_FAIL_CLOSED -> FAIL_CLOSED
MRG-CT-007 COMPLETE_COMMIT_BOUNDARY_RECONSTRUCTION_ALLOW -> ALLOW
```

## Current state

```text
proof_package_structure: COMPLETE
connector_materialized_reproduction: RECORDED
canonical_repository_or_ci_execution: PENDING
artifact_equivalence_promotion: BLOCKED_PENDING_CANONICAL_EXECUTION
authority_posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
```

Connector-materialized reproduction is evidence of deterministic reconstruction from committed sources. It is not a canonical repository checkout, GitHub Actions run, certification, endorsement, or execution-authority grant.

## Canonical-run owner

```text
issue: Data-Continuation/formalism-tests#5
title: Run canonical Morrison commit-time scope tasks and verify artifact equivalence
state: open
```

Issue #5 owns the repository-checkout or existing-CI execution, exact report and receipt equivalence, verification regeneration, durable run evidence, and final handoff promotion.

## Completion conditions

```text
- both declared tasks pass in a repository checkout or existing CI surface
- generated report equals the committed deterministic baseline
- generated receipt set equals the committed receipt baseline
- artifact verification is regenerated as PASS
- durable evidence identifies commit, execution surface, commands, results, and hashes
- authority_posture remains EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
- no Morrison verdict becomes StegVerse execution authority
```

## Downstream activation

After canonical evidence exists, activation may proceed only through:

```text
StegVerse-Labs/admissibility-wiki#39
```

The wiki may then bind the proof package as verified bounded comparative evidence, run its canonical validation chain, verify the public route, and review current destination handoffs.

Direct propagation to Site, Publisher, or stegguardian-wiki remains prohibited until the wiki promotion is complete and each destination handoff grants the relevant scope.

## Fail-closed rule

Any missing canonical execution evidence, artifact mismatch, unknown source provenance, failed verifier, or authority-posture drift blocks promotion.

## Archive posture

This file preserves the proof surface, declared commands, case contract, current standing, issue ownership, completion conditions, downstream gate, and authority boundary so continuation does not depend on prior chat context.