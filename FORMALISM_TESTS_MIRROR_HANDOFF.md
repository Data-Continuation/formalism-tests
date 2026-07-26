# Formalism Tests Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `Data-Continuation/formalism-tests` until superseded.

## Completed goal

Executable proof fixtures for denial reachability at the consequence-binding commit boundary are installed and verified against committed expected outcomes.

## Installed proof surface

```text
tests/fixtures/denial_reachability_cases.json
tests/fixtures/denial_reachability_expected_outcomes.json
tests/fixtures/denial_reachability_artifact_baseline.json
tools/run_denial_reachability_tests.py
tools/verify_denial_reachability_artifacts.py
tools/tasks/denial_reachability_tasks.json
reports/denial_reachability_report.json
reports/denial_reachability_continuation_report.md
receipts/denial_reachability_execution_receipts.jsonl
receipts/denial_reachability_connector_snapshot_run.json
```

## Declared tasks

```text
denial_reachability_commit_boundary_tests
verify_denial_reachability_artifacts
fi_transition_continuity_interop_tests
verify_fi_transition_continuity_interop_artifacts
```

Canonical commands:

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id verify_denial_reachability_artifacts
python tools/run_declared_tasks.py tools/tasks/fi_transition_continuity_interop_tasks.json --task-id fi_transition_continuity_interop_tests
python tools/run_declared_tasks.py tools/tasks/fi_transition_continuity_interop_tasks.json --task-id verify_fi_transition_continuity_interop_artifacts
```

## Verified denial-reachability result

```text
status: PASS
case_count: 5
passed_count: 5
failed_count: 0
report_sha256: 8c2c460e3d7ae790a4f5fc347e44f9e91615db8b1913ee98c893e3071a5fb284
generated_report_file_sha256: f5a07da05497bdd8d85bd60e43ceb5d043eac656bad2f873a6d9aee2d65f95be
generated_receipts_file_sha256: 9f1c0dc5463dc7396addf7a62147b8beb33f818b67add8f41bc069c96cef2953
```

The denial-reachability artifact verifier checks canonical fixture and expected-outcome hashes, report status and counts, report/receipt case equality, receipt contract fields, formalism and report references, late-refusal non-prevention, and generated report/receipt byte-equivalence to the committed artifact baseline.

## Connector-materialized denial-reachability reproduction

Both denial-reachability declared tasks were executed successfully against a snapshot materialized from committed GitHub sources through the connector.

```text
receipt: receipts/denial_reachability_connector_snapshot_run.json
denial_reachability_commit_boundary_tests: PASS
verify_denial_reachability_artifacts: PASS
byte_equivalence_to_baseline: true
late_refusal_non_prevention_preserved: true
authority_posture: REPRODUCTION_EVIDENCE_ONLY
```

This is not GitHub Actions or repository-checkout evidence and does not replace the required canonical run.

## FI continuity interoperability slice

The repository contains a continuity-specific interoperability surface for `Admissible-Existence/FI` claim `FI-TRANSITION-001`.

Installed surfaces:

```text
tests/fixtures/fi_transition_continuity_interop_cases.json
tests/fixtures/fi_transition_continuity_interop_expected_outcomes.json
tests/fixtures/fi_transition_continuity_interop_artifact_baseline.json
tools/run_fi_transition_continuity_interop.py
tools/verify_fi_transition_continuity_interop_artifacts.py
tools/tasks/fi_transition_continuity_interop_tasks.json
reports/fi_transition_continuity_interop_report.json
receipts/fi_transition_continuity_interop_connector_snapshot_run.json
```

Verified reproduction result:

```text
status: PASS
case_count: 4
passed_count: 4
failed_count: 0
authority_posture: CONTINUITY_INTEROPERABILITY_ONLY
execution_surface: connector_materialized_committed_sources
canonical_repository_checkout: false
github_actions_run: false
```

Verified cases:

```text
CONTINUOUS_IDENTIFIABLE_TRANSITION -> INTEROPERABLE
BROKEN_ORDERED_EVIDENCE_CHAIN -> FAIL_CLOSED
UNRELATED_REPLACEMENT_WITH_SAME_LABEL -> FAIL_CLOSED
NO_DETECTABLE_DIFFERENCE -> NOT_A_TRANSITION
```

Canonical report baseline:

```text
canonical_report_sha256: 6b3b42c93ef8f118e984deb25b8075dbf5f3e9cbb6fd91f66dc772882f4cf170
hash_type: canonical JSON document hash
```

The FI artifact verifier requires report hash equality, suite identity/version equality, `PASS`, zero failures, and preservation of `CONTINUITY_INTEROPERABILITY_ONLY`.

The boundary remains:

```text
same label != same identity
ordered evidence continuity is required
no detectable difference != transition
continuity interoperability != cross-domain support
continuity interoperability != execution authority
continuity interoperability != universal law
reproduction pass != canonical execution
```

## Durable canonical-run ownership

```text
issue: Data-Continuation/formalism-tests #4
title: Run canonical FI continuity interoperability tasks and verify report equivalence
state: open
```

Issue #4 owns the repository-checkout or existing-CI run, exact report-equivalence verification, durable execution evidence, and completion conditions for the FI interoperability slice.

## Active Morrison Runtime commit-time scope goal

The repository now owns executable comparative fixtures for the public Resurrection Tech clarification that normal Runtime Governance performs a second pre-execution decision, while full fresh-state reconstruction and evidence binding are separately configurable high-assurance capabilities.

Installed initial surfaces:

```text
tests/fixtures/morrison_runtime_commit_time_scope_cases.json
tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json
tools/run_morrison_runtime_commit_time_scope.py
```

Required cases:

```text
MRG-CT-001 ALLOW_TO_BLOCK_CONTRADICTORY_EVIDENCE
MRG-CT-002 BLOCK_TO_ALLOW_CORRECTIVE_EVIDENCE
MRG-CT-003 MISSING_REQUIRED_EVIDENCE_FAIL_CLOSED
MRG-CT-004 UNKNOWN_EVIDENCE_COVERAGE_FAIL_CLOSED
MRG-CT-005 STALE_CACHED_BINDING_FAIL_CLOSED
MRG-CT-006 PREVIOUSLY_UNMODELED_PARAMETER_FAIL_CLOSED
MRG-CT-007 COMPLETE_COMMIT_BOUNDARY_RECONSTRUCTION_ALLOW
```

Remaining installation:

```text
tools/verify_morrison_runtime_commit_time_scope_artifacts.py
tools/tasks/morrison_runtime_commit_time_scope_tasks.json
reports/morrison_runtime_commit_time_scope_report.json
receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl
committed artifact baseline and connector-materialized reproduction receipt
```

Completion requires deterministic fixture execution, expected-result equality, report and receipt generation, artifact verification, and durable canonical execution evidence. Native Morrison results remain external evidence only and do not become StegVerse execution authority.

## Authority boundary

```text
Data-Continuation/formalism-tests owns executable proof and test authority.
Admissible-Existence/FI owns candidate invariant definitions and local claim contracts.
Admissible-Existence/Fundamental-Invariants-of-Reality will own cross-domain falsification after creation.
StegVerse-Labs/admissibility-wiki owns vocabulary, public explanation, and proof references only.
StegVerse-Labs/Site and GCAT-BCAT-Engine/Publisher are downstream mirrors and must not infer proof from documentation alone.
```

## Active goals

Denial-reachability canonical completion still requires:

```text
run both denial-reachability declared tasks in a repository checkout or existing CI execution surface
confirm generated report and receipt bytes match the committed baseline
commit reports/denial_reachability_artifact_verification.json
attach durable canonical execution evidence
replace PENDING_EXTERNAL_DECLARED_TASK_RUN with VERIFIED_CANONICAL_RUN
```

FI interoperability canonical completion requires:

```text
execute issue #4
run fi_transition_continuity_interop_tests through the declared-task runner
run verify_fi_transition_continuity_interop_artifacts through the declared-task runner
confirm canonical report hash 6b3b42c93ef8f118e984deb25b8075dbf5f3e9cbb6fd91f66dc772882f4cf170
attach repository-checkout, CI, workflow, or commit evidence
preserve authority_posture: CONTINUITY_INTEROPERABILITY_ONLY
```

## Downstream restrictions

```text
StegVerse-Labs/Site
  -> check docs/SITE_MIRROR_HANDOFF.md before mutation
  -> mirror only after admissibility-wiki build and public route verify

GCAT-BCAT-Engine/Publisher
  -> publish only after verified wiki artifact and canonical-run receipt exist

StegVerse-002/stegguardian-wiki
  -> interpret denial reachability and Morrison scope only after proof receipts are indexed and refusal-capability language preserves the proof boundary

Admissible-Existence/Fundamental-Invariants-of-Reality
  -> do not treat continuity interoperability as cross-domain validation
```

## Archive posture

This handoff preserves the completed proofs, deterministic baselines, connector-materialized reproduction evidence, FI continuity interoperability implementation, active Morrison commit-time scope fixtures, authority boundaries, canonical-run obligations, completion events, and downstream restrictions so the complete thread can be archived without additional context.
