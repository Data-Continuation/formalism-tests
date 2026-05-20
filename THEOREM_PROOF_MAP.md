# Theorem Proof Map

## Purpose

This file maps DCF theorem candidates to executable proof artifacts.

## Current artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
tests/expected_outcomes.json
src/validate_expected_outcomes.py
tests/compound_cases.json
src/compound_continuation_gate.py
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
tools/tasks/formalism_tests_tasks.json
tools/rules/runtime_artifact_rules.json
tools/apply_runtime_artifact_rules.py
tools/run_declared_tasks.py
tests/fixtures/representation_non_consequence_cases.json
tools/run_representation_non_consequence_tests.py
reports/representation_non_consequence_receipts.jsonl
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
```

## Current workflow evidence

The declared-task workflow can now run:

```text
archive_runtime_artifacts
continuation_gate
compound_continuation_gate
transition_table_gate
boundary_transition_gate
stage6_unified_gate_tests
transition_table_public_surface_tests
representation_non_consequence_tests
```

## Mapping

| Theorem | Current evidence | Status |
|---|---|---|
| Representation Non-Consequence | Direct representation-only receipts show `NO_CONSEQUENCE` until a datum is bound to a consequence-bearing role, transition, and continuation path. | Covered |
| Role Non-Transfer | Same patient-risk datum produces ALLOW, ALLOW_WITH_SIGNOFF, and FAIL_CLOSED across roles. | Covered |
| Continuation Capacity | Insufficient capacity cases fail closed. | Covered |
| Fail-Closed Basis Requirement | Missing required block basis fails closed. | Covered |
| Local-Composite Non-Equivalence | Stage 3 compound-local-001: local ALLOW + local ALLOW fails closed because composite consequence mass exceeds legitimacy capacity. | Covered |
| Commit-Time Sufficiency | Stage 3 drift-commit-001: pre-commit state differs from commit state, producing FAIL_CLOSED due to commit-time state drift. | Covered |
| Replay Non-Reversal | Stage 3 replay-non-reversal-001: replay may reconstruct receipt state but may not reverse consequence. | Covered |
| Inference-Window Collapse | Stage 3 inference-collapse-001: inference window collapsed below continuation threshold, producing FAIL_CLOSED. | Covered |
| Recoverability Floor | Stage 3 recoverability-floor-001: recoverability score below required floor, producing FAIL_CLOSED. | Covered |
| Role-Transition Dependence | Covered by role comparison and same-data continuation decisions. | Covered |
| Compound Continuation Positive Control | Stage 3 compound-allow-001: compound continuation remains within capacity and recoverability bounds, producing ALLOW. | Covered |
| Stage 6 Unified Gate | Stage 6 runner validates 10 candidates and 320 assertions through the existing declared-task workflow. | Covered |
| Transition Table Public Surface | Public surface runner validates 10 transition classes, 16 elements, 12 unlocked Level 5 elements, single-source status, and mobile contract. | Covered |

## Stage 2 proof surface

```text
same data ≠ same continuation admissibility
```

## Stage 3 proof surface

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

## Representation Non-Consequence proof surface

```text
representation alone has no consequence-bearing status
representation becomes consequence-bearing only when bound to role + transition + continuation path
```

## Current interpretation

The proof surface now separates:

```text
representation
role binding
transition binding
continuation path
consequence authority
commit-time admissibility
```

This closes the earlier direct-proof gap for Representation Non-Consequence.
