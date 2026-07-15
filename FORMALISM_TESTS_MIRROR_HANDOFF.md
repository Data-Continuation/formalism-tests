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
```

Canonical commands:

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id verify_denial_reachability_artifacts
python tools/run_declared_tasks.py tools/tasks/fi_transition_continuity_interop_tasks.json --task-id fi_transition_continuity_interop_tests
```

## Verified proof cases

```text
REACHABLE_DENY
  decision: DENY
  execution_prevented: true
  denial_controlled_execution: true

UNREACHABLE_DENY
  decision: FAIL_CLOSED
  failure_class: INHERITED_AUTHORIZATION
  execution_prevented: true
  denial_controlled_execution: false

COSMETIC_GATING
  decision: FAIL_CLOSED
  failure_class: COSMETIC_GATING
  execution_prevented: true
  denial_controlled_execution: false

LATE_REFUSAL
  decision: FAIL_CLOSED
  failure_class: LATE_REFUSAL
  execution_prevented: false
  denial_controlled_execution: false

SPLIT_BOUNDARY_INSUFFICIENCY
  decision: FAIL_CLOSED
  failure_class: SPLIT_BOUNDARY_INSUFFICIENCY
  execution_prevented: true
  denial_controlled_execution: false
```

## Verification result

```text
status: PASS
case_count: 5
passed_count: 5
failed_count: 0
report_sha256: 8c2c460e3d7ae790a4f5fc347e44f9e91615db8b1913ee98c893e3071a5fb284
generated_report_file_sha256: f5a07da05497bdd8d85bd60e43ceb5d043eac656bad2f873a6d9aee2d65f95be
generated_receipts_file_sha256: 9f1c0dc5463dc7396addf7a62147b8beb33f818b67add8f41bc069c96cef2953
```

The artifact verifier checks canonical fixture and expected-outcome hashes, report status and counts, report/receipt case equality, receipt contract fields, formalism and report references, late-refusal non-prevention, and generated report/receipt byte-equivalence to the committed artifact baseline.

## Discovered verifier blocker and correction

The first declared verification run exposed a contract defect:

```text
proof report stored canonical JSON hashes
verifier compared raw file-byte hashes
result: verifier could never pass even when the proof was correct
```

Corrected by:

```text
c37ea88e0af6fb6b3a3a5b31d425d2c7ed2a4783
  -> compare canonical document hashes

a9eb029ab09c085d4d91c1ee825216cc3e4a1c4c
  -> add deterministic generated-artifact byte baseline

1f4474fc6cbba0e1bbce272300a9d2adc3c92a54
  -> enforce report and receipt byte-equivalence to baseline
```

## Connector-materialized reproduction

Both denial-reachability declared tasks were executed successfully against a snapshot materialized from the committed GitHub sources through the connector.

Durable receipt:

```text
receipts/denial_reachability_connector_snapshot_run.json
```

Result:

```text
denial_reachability_commit_boundary_tests: PASS
verify_denial_reachability_artifacts: PASS
byte_equivalence_to_baseline: true
late_refusal_non_prevention_preserved: true
authority_posture: REPRODUCTION_EVIDENCE_ONLY
```

This is not represented as GitHub Actions or repository-checkout evidence. It materially narrows the remaining validation gap but does not replace the required repository or existing-CI run.

## FI continuity interoperability slice

The repository now contains a continuity-specific interoperability surface for `Admissible-Existence/FI` claim `FI-TRANSITION-001`.

Installed surfaces:

```text
tests/fixtures/fi_transition_continuity_interop_cases.json
tests/fixtures/fi_transition_continuity_interop_expected_outcomes.json
tools/run_fi_transition_continuity_interop.py
tools/tasks/fi_transition_continuity_interop_tasks.json
```

The test boundary is deliberately narrow:

```text
same label != same identity
ordered evidence continuity is required
no detectable difference != transition
continuity interoperability != cross-domain support
continuity interoperability != execution authority
continuity interoperability != universal law
```

Expected cases:

```text
CONTINUOUS_IDENTIFIABLE_TRANSITION -> INTEROPERABLE
BROKEN_ORDERED_EVIDENCE_CHAIN -> FAIL_CLOSED
UNRELATED_REPLACEMENT_WITH_SAME_LABEL -> FAIL_CLOSED
NO_DETECTABLE_DIFFERENCE -> NOT_A_TRANSITION
```

Execution evidence for this new declared task remains pending. Its installation does not alter the active denial-reachability canonical-run obligation.

## Authority boundary

```text
Data-Continuation/formalism-tests owns executable proof and test authority.
Admissible-Existence/FI owns candidate invariant definitions and local claim contracts.
Admissible-Existence/Fundamental-Invariants-of-Reality will own cross-domain falsification after creation.
StegVerse-Labs/admissibility-wiki owns vocabulary, public explanation, and proof references only.
StegVerse-Labs/Site and GCAT-BCAT-Engine/Publisher are downstream mirrors and must not infer proof from documentation alone.
```

## Completed downstream integration

```text
StegVerse-Labs/admissibility-wiki
  -> denial-reachability public formalism installed
  -> proof-reference receipt installed
  -> executable proof status and report hash recorded
  -> NON_EXECUTION_AUTHORITY boundary preserved
```

## Active goal

Obtain canonical declared-task execution evidence without creating a new workflow solely for this task.

Completion requires:

```text
run both denial-reachability declared tasks in a repository checkout or existing CI execution surface
confirm generated report and receipt bytes match the committed baseline
commit reports/denial_reachability_artifact_verification.json
attach workflow, run, commit, or other durable canonical execution evidence
replace PENDING_EXTERNAL_DECLARED_TASK_RUN with VERIFIED_CANONICAL_RUN
```

Supplemental FI interoperability completion requires:

```text
run fi_transition_continuity_interop_tests through the declared-task runner
commit reports/fi_transition_continuity_interop_report.json
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
  -> interpret denial reachability only after proof receipt is indexed and refusal-capability language preserves the proof boundary

Admissible-Existence/Fundamental-Invariants-of-Reality
  -> do not treat continuity interoperability as cross-domain validation
```

## Archive posture

This handoff preserves the completed proof, verifier correction, deterministic byte baseline, connector-materialized reproduction evidence, FI continuity interoperability installation, authority boundaries, active canonical-run requirement, completion events, and downstream restrictions so the complete thread can be archived without additional context.
