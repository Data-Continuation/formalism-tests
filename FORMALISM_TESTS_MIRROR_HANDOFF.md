# Formalism Tests Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `Data-Continuation/formalism-tests` until superseded.

Incoming sessions must preserve active issue ownership, distinguish connector-materialized reproduction from canonical execution, and avoid promoting documentation or external-framework results into StegVerse execution authority.

## Repository authority boundary

```text
Data-Continuation/formalism-tests
  -> executable fixtures, deterministic expected outcomes, artifact verification, and proof receipts

StegVerse-Labs/admissibility-wiki
  -> vocabulary, bounded public explanation, and proof references only

StegVerse-Labs/Site
  -> downstream display only after verified public activation

GCAT-BCAT-Engine/Publisher
  -> downstream publication/indexing only after governed propagation review

StegVerse-002/stegguardian-wiki
  -> bounded interpretation only after proof receipts are indexed
```

No fixture, report, connector reproduction, workflow result, public page, or external-framework verdict independently grants execution, release, certification, publication, or admissibility authority.

## Denial-reachability package

Installed:

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

Verified bounded result:

```text
status: PASS
case_count: 5
passed_count: 5
failed_count: 0
connector reproduction: PASS
byte equivalence to committed baseline: true
authority posture: REPRODUCTION_EVIDENCE_ONLY
canonical execution: pending
```

Canonical completion remains separate and must be supported by repository-checkout, existing CI, or GitHub Actions evidence.

## FI continuity interoperability package

Installed:

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

Verified bounded cases:

```text
CONTINUOUS_IDENTIFIABLE_TRANSITION -> INTEROPERABLE
BROKEN_ORDERED_EVIDENCE_CHAIN -> FAIL_CLOSED
UNRELATED_REPLACEMENT_WITH_SAME_LABEL -> FAIL_CLOSED
NO_DETECTABLE_DIFFERENCE -> NOT_A_TRANSITION
```

Boundary:

```text
same label != same identity
ordered evidence continuity is required
no detectable difference != transition
continuity interoperability != cross-domain validation
continuity interoperability != execution authority
reproduction pass != canonical execution
```

Canonical-run ownership remains with issue #4.

## Morrison Runtime commit-time scope package

The repository contains a bounded comparative suite for the public Resurrection Tech clarification that ordinary Runtime Governance performs a second pre-execution decision, while full fresh-state reconstruction and evidence binding are separately configurable high-assurance capabilities.

Installed:

```text
tests/fixtures/morrison_runtime_commit_time_scope_cases.json
tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json
tests/fixtures/morrison_runtime_commit_time_scope_artifact_baseline.json
tools/run_morrison_runtime_commit_time_scope.py
tools/verify_morrison_runtime_commit_time_scope_artifacts.py
tools/check_morrison_runtime_canonical_evidence_gate.py
tools/tasks/morrison_runtime_commit_time_scope_tasks.json
reports/morrison_runtime_commit_time_scope_report.json
receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl
receipts/morrison_runtime_connector_materialized_reproduction.json
schemas/morrison_runtime_canonical_execution_evidence.schema.json
receipts/morrison_runtime_canonical_execution_evidence.pending.json
receipts/morrison_runtime_commit_time_scope_downstream_activation_contract.json
```

Bounded deterministic result:

```text
status: PASS
case_count: 7
passed_count: 7
failed_count: 0
expected-outcome equivalence: true
committed report semantic equivalence: true
committed receipt semantic equivalence: true
authority posture: EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY
canonical repository checkout: false
GitHub Actions run: false
canonical execution claimed: false
promotion eligible: false
external framework validation claimed: false
```

Verified cases:

```text
MRG-CT-001 contradictory live evidence: ALLOW -> DENY
MRG-CT-002 corrective live evidence: BLOCK -> ALLOW
MRG-CT-003 missing required evidence: FAIL_CLOSED
MRG-CT-004 unknown evidence coverage: FAIL_CLOSED
MRG-CT-005 stale cached binding: FAIL_CLOSED
MRG-CT-006 unmodeled material parameter: FAIL_CLOSED
MRG-CT-007 complete commit-boundary reconstruction: ALLOW preserved
```

The connector-materialized reproduction is bounded reproduction evidence only. It is not a native Morrison execution, repository checkout, GitHub Actions run, certification, endorsement, production validation, or StegVerse execution-authority determination.

## Morrison canonical evidence contract alignment

The canonical-evidence checker and pending record are aligned with the committed JSON Schema and declared-task manifest.

```text
schema contract:
  artifact_hashes.report_sha256
  artifact_hashes.receipts_sha256
  artifact_hashes.verification_sha256
  artifact_equivalence.report
  artifact_equivalence.receipts
  artifact_equivalence.expected_outcomes

canonical evidence task results:
  morrison_runtime_commit_time_scope_tests -> PASS
  verify_morrison_runtime_commit_time_scope_artifacts -> PASS

post-install gate task:
  check_morrison_runtime_canonical_evidence_gate -> PASS
```

The checker no longer accepts the former schema-incompatible flat fields or `promotion_eligible` inside the canonical evidence record. Promotion eligibility is derived only in the gate result after a schema-compatible canonical record passes validation.

Alignment commits:

```text
e5d1707c4ec4000cbf15d24758a779cd2882051e
5cf992b281e0f4dce47ef54b12baeb9ce342e389
```

This correction is a deterministic contract repair only. It does not claim that canonical execution occurred.

## Morrison canonical evidence gate

Issue #5 owns canonical closure.

Required commands:

```bash
python tools/run_declared_tasks.py tools/tasks/morrison_runtime_commit_time_scope_tasks.json --task-id morrison_runtime_commit_time_scope_tests
python tools/run_declared_tasks.py tools/tasks/morrison_runtime_commit_time_scope_tasks.json --task-id verify_morrison_runtime_commit_time_scope_artifacts
python tools/run_declared_tasks.py tools/tasks/morrison_runtime_commit_time_scope_tasks.json --task-id check_morrison_runtime_canonical_evidence_gate
```

Promotion to `VERIFIED_CANONICAL_RUN` requires durable evidence identifying the commit, approved canonical execution surface, commands, task results, exact artifact equivalence, and required SHA-256 values. Until that contract is satisfied:

```text
canonical evidence status: PENDING_CANONICAL_EXECUTION
promotion eligible: false
downstream activation: prohibited
handoff promotion: prohibited
```

## Current active ownership

```text
issue #4
  -> canonical FI continuity interoperability execution and durable equivalence evidence

issue #5
  -> canonical Morrison commit-time scope execution and evidence-gate satisfaction

admissibility-wiki issue #39
  -> bounded downstream compatibility-report promotion only after issue #5 closure
```

Do not duplicate these issue-owned workloads.

## Next parallel-safe work

Parallel work may proceed only when it does not claim canonical execution or duplicate issue #4 or #5. Safe examples include:

```text
verify committed references and schema consistency
repair exact deterministic contract defects
preserve fail-closed downstream activation contracts
prepare bounded documentation references that remain unpublished and non-authoritative
inspect repository-owned workflow evidence when exposed
```

Do not infer progress from elapsed time, connector access, branch existence, or external-framework claims.

## Downstream restrictions

```text
StegVerse-Labs/Site
  -> read docs/SITE_MIRROR_HANDOFF.md before any mutation
  -> mirror only after admissibility-wiki validation and public-route verification

GCAT-BCAT-Engine/Publisher
  -> propagate only after verified wiki artifact and canonical-run receipt exist

StegVerse-002/stegguardian-wiki
  -> preserve refusal-capability and proof-boundary language

Admissible-Existence/Fundamental-Invariants-of-Reality
  -> do not treat continuity interoperability as cross-domain validation
```

## Release posture

No release or tag is authorized until required canonical executions, artifact equivalence, durable evidence, downstream validation, and repository release criteria are confirmed.

When release-qualified, queue propagation-status review for:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Archive posture

This handoff preserves the installed denial-reachability, FI continuity, and Morrison commit-time scope packages; bounded reproduction results; canonical evidence contract alignment; active issue ownership; canonical evidence gates; authority boundaries; downstream restrictions; and next parallel-safe work. The complete thread is ready for archiving without additional conversation context.
