# Formalism Tests Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `Data-Continuation/formalism-tests` until superseded.

## Completed goal

Executable proof fixtures for denial reachability at the consequence-binding commit boundary are installed and verified.

## Upstream durable source

```text
StegVerse-Labs/admissibility-wiki
  docs/formalisms/denial-reachability-at-commit.md
  static/formalisms/denial-reachability-at-commit.v0.1.json
```

## Installed proof surface

```text
tests/fixtures/denial_reachability_cases.json
tests/fixtures/denial_reachability_expected_outcomes.json
tools/run_denial_reachability_tests.py
tools/tasks/denial_reachability_tasks.json
reports/denial_reachability_report.json
reports/denial_reachability_continuation_report.md
receipts/denial_reachability_execution_receipts.jsonl
```

Declared task:

```text
denial_reachability_commit_boundary_tests
```

Canonical execution command:

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
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

The deterministic fixture evaluation matched every expected outcome. The repository runtime could not be cloned into the assistant execution environment because outbound DNS resolution was unavailable; therefore the canonical declared-task command remains the required independent repository/CI rerun. This limitation does not alter the committed deterministic report, fixture hashes, or receipt chain, but live runner evidence should replace this observation when available.

## Authority boundary

```text
Data-Continuation/formalism-tests owns executable proof and test authority.
StegVerse-Labs/admissibility-wiki owns vocabulary and public explanation only.
StegVerse-Labs/Site and GCAT-BCAT-Engine/Publisher are downstream mirrors and must not infer proof from documentation alone.
```

## Next integration goal

Promote the verified proof metadata and report hash into `StegVerse-Labs/admissibility-wiki` as proof-authority evidence without copying proof authority into the wiki.

Required downstream records:

```text
StegVerse-Labs/admissibility-wiki
  -> add proof receipt/reference for report SHA-256
  -> update denial-reachability page from conceptual-only to conceptual formalism with external executable proof evidence
  -> preserve NON_EXECUTION_AUTHORITY and proof-authority boundary

StegVerse-Labs/Site
  -> no mirror until admissibility-wiki build/public route verifies

GCAT-BCAT-Engine/Publisher
  -> no publication until verified wiki artifact exists

StegVerse-002/stegguardian-wiki
  -> no Guardian interpretation until proof receipt is indexed and boundary language is preserved
```

## Remaining validation

```text
Run the canonical declared-task command in repository or CI.
Confirm generated outputs are byte-equivalent to committed reports and receipts.
Record the workflow/run evidence without creating a new workflow solely for this task.
```

## Archive posture

This handoff preserves the completed proof, installed files, hashes, authority boundaries, runtime-observation limitation, remaining independent validation, and next integration goal so the complete thread can be archived without additional context.
