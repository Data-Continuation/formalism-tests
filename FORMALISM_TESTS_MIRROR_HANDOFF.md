# Formalism Tests Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `Data-Continuation/formalism-tests` until superseded.

## Completed goal

Executable proof fixtures for denial reachability at the consequence-binding commit boundary are installed and verified against committed expected outcomes.

## Installed proof surface

```text
tests/fixtures/denial_reachability_cases.json
tests/fixtures/denial_reachability_expected_outcomes.json
tools/run_denial_reachability_tests.py
tools/verify_denial_reachability_artifacts.py
tools/tasks/denial_reachability_tasks.json
reports/denial_reachability_report.json
reports/denial_reachability_continuation_report.md
receipts/denial_reachability_execution_receipts.jsonl
```

## Declared tasks

```text
denial_reachability_commit_boundary_tests
verify_denial_reachability_artifacts
```

Canonical commands:

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id verify_denial_reachability_artifacts
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
```

The artifact verifier now checks:

```text
committed fixture and expected-outcome hashes
report PASS and 5/0 counts
report/receipt case-set equality
receipt contract fields against report results
formalism and report-hash references
late-refusal post-binding non-prevention
```

The verifier writes:

```text
reports/denial_reachability_artifact_verification.json
```

with `canonical_execution_evidence: PENDING_EXTERNAL_DECLARED_TASK_RUN` until an actual repository or CI execution record is attached.

## Authority boundary

```text
Data-Continuation/formalism-tests owns executable proof and test authority.
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
run both declared tasks in repository or an existing CI execution surface
confirm generated report and receipt bytes match committed artifacts
commit reports/denial_reachability_artifact_verification.json
attach workflow, run, commit, or other durable execution evidence
replace PENDING_EXTERNAL_DECLARED_TASK_RUN with VERIFIED_CANONICAL_RUN
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
```

## Archive posture

This handoff preserves the completed proof, integrity-verification task, installed files, hashes, authority boundaries, active canonical-run requirement, completion event, and downstream restrictions so the complete thread can be archived without additional context.
