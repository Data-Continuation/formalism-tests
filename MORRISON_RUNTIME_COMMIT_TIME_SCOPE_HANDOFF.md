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

## 2026-08-26 repository-owned canonical CI activation

The existing `continuation-tests.yml` workflow is now the canonical execution surface for issue #5. It runs `tools/run_morrison_runtime_canonical_ci_capture.py` on non-PR `main` execution, which runs all three declared Morrison tasks, verifies deterministic output equivalence, creates the schema-bound canonical execution evidence, verifies the canonical gate hash, appends the hosted observation here, commits generated evidence through the repository-owned evidence step, and closes issue #5 only after `VERIFIED_CANONICAL_RUN` exists.

Implementation commits:

```text
524426b45683b2eab4b0d50749e03a3f118ff3f9
  add repository-owned Morrison canonical CI capture

5f6e26bb39520f31aee56d3cb5b9353a3dfbdcba
  bind capture, evidence upload, durable commit, and issue closure to continuation-tests.yml
```

First hosted attempt `33014851827` proved the first declared Morrison task PASS with all 7/7 cases, then correctly failed its stronger byte-equivalence gate because the committed report used a compact JSON formatting form while the deterministic generator emits canonical pretty JSON. This was an artifact-byte representation mismatch, not a semantic test failure.

Commit `7bca1de68bf6cb160a2a447e74744a335cde68d4` canonicalizes the committed report to the generator's deterministic byte format without changing any semantic field, case result, authority posture, or evidence claim. A successor repository-owned run is required before canonical execution may be promoted.

## Current state

```text
proof_package_structure: COMPLETE
connector_materialized_reproduction: RECORDED
canonical_repository_or_ci_execution: VERIFIED_CANONICAL_RUN
canonical_run_id: 33014956712
canonical_run_commit: daca16578387c45cde616b82ba517d11314e1ef2
durable_evidence_commit: 42ac1a25cf4427290f0b239c8e069253c87f86ba
artifact_equivalence_promotion: VERIFIED
authority_posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
```

Connector-materialized reproduction is evidence of deterministic reconstruction from committed sources. It is not a canonical repository checkout, GitHub Actions run, certification, endorsement, or execution-authority grant.

## Canonical-run owner

```text
issue: Data-Continuation/formalism-tests#5
title: Run canonical Morrison commit-time scope tasks and verify artifact equivalence
state: closed_completed
```

Issue #5 completed the repository-owned CI execution, exact report and receipt equivalence, verification regeneration, durable run evidence, and final upstream handoff promotion. Downstream responsibility is now exclusively `StegVerse-Labs/admissibility-wiki#39`.

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

## Canonical GitHub Actions execution observed

```text
status: VERIFIED_CANONICAL_RUN
commit_sha: 9aad3e55354657b33d1c6abe1500186c24d15aec
execution_surface: GITHUB_ACTIONS
run_id: 33633233140
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/33633233140
task_results:
  morrison_runtime_commit_time_scope_tests: PASS
  verify_morrison_runtime_commit_time_scope_artifacts: PASS
  check_morrison_runtime_canonical_evidence_gate: PASS
report_sha256: 47fe6f349b2a5f181c2653db8e874e7cd862287e69aa3ba80f762f4019079dd1
receipts_sha256: 0993a3c118de08ea9a4bdb1aac93cad3363893c1bf0b573edc057dc247d73ce2
verification_sha256: 7f067bf605d363850ead0acb6851ccc5d16aa3b90d07b96a35becf06f11fd3da
canonical_evidence_gate_sha256: e670e3487487db345fcd584526109cacad81d763b04415f6c1584b5da196eddf
report_equivalence: true
receipts_equivalence: true
expected_outcomes_equivalence: true
canonical_evidence_gate_equivalence: true
authority_posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
downstream_owner: StegVerse-Labs/admissibility-wiki#39
```

This is repository-owned canonical execution evidence for the bounded comparative proof package. It is not Morrison certification, endorsement, production validation, StegVerse execution authority, release authority, or downstream mutation authority. Downstream promotion remains separately gated by the admissibility-wiki canonical/public-route contracts.
