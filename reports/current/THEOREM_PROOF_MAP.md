# Theorem Proof Map

## Purpose

This file maps DCF theorem candidates to executable proof artifacts.

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Current Workflow Evidence

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
site_mirror_integrity_tests
current_report_preservation_tests
theorem_map_consistency_tests
```

## Current Artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
reports/transition_table_receipts.jsonl
reports/boundary_transition_receipts.jsonl
reports/representation_non_consequence_receipts.jsonl
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
reports/transition_table_public_surface_report.json
reports/site_mirror_integrity_report.json
reports/current_report_preservation_report.json
reports/current/
tests/fixtures/representation_non_consequence_cases.json
tests/fixtures/site/
tests/fixtures/site_mirror/
tests/fixtures/current_report_preservation_policy.json
tools/run_stage6_unified_gate_tests.py
tools/run_transition_table_public_surface_tests.py
tools/run_representation_non_consequence_tests.py
tools/run_site_mirror_integrity_tests.py
tools/run_current_report_preservation_tests.py
tools/run_theorem_map_consistency_tests.py
tools/tasks/formalism_tests_tasks.json
tools/run_declared_tasks.py
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
| Transition Table Public Surface | Public surface runner validates 10 transition classes, 16 elements, 12+ unlocked Level 5 elements, single-source status, and mobile contract. | Covered |
| Site Mirror Integrity | Site mirror runner validates Stage 6 status, public result alignment, Representation Non-Consequence coverage, element pages, mobile contract, and duplicate receipt handling. | Covered |
| Current Report Preservation | Current-report runner preserves latest successful reports under `reports/current/` while runtime artifact archiving remains available. | Covered |
| Theorem Map Consistency | Theorem-map runner verifies root and current theorem maps agree with latest successful proof reports. | Covered |

## Stage 2 Proof Surface

```text
same data ≠ same continuation admissibility
```

Stage 2 demonstrates that a datum can be safe as an informational note, conditional as a clinician recommendation, and inadmissible as autonomous actuation.

## Stage 3 Proof Surface

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

## Representation Non-Consequence Proof Surface

```text
representation alone has no consequence-bearing status
representation becomes consequence-bearing only when bound to role + transition + continuation path
```

Representation Non-Consequence is now directly covered.

## Stage 6 Unified Gate Proof Surface

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

Verified result:

```text
candidate_count: 10
assertion_count: 320
ALLOW: 3
FAIL_CLOSED: 5
RESET_BOUNDARY: 1
EVOLVE_BOUNDARY: 1
```

## Transition Table Public Surface

Verified result:

```text
transition_class_count: 10
element_count: 16
unlocked_level_5_count: 12+
single_status_source: data/formalism-tests/transition-proof-surface.json
```

## Site Mirror Integrity

Verified result:

```text
current_stage: Stage 6
representation_non_consequence_status: Covered
single_status_source: data/formalism-tests/transition-proof-surface.json
```

## Current Report Preservation

The latest successful proof outputs should be preserved under:

```text
reports/current/
```

Runtime archival may continue moving older or generated artifacts into:

```text
legacy/runtime-artifacts/<timestamp>/
```

The preservation rule is:

```text
archive old runtime outputs
preserve current proof outputs
do not let public proof evidence become hard to locate
```

## Duplicate Receipt Handling

Canonical:

```text
reports/transition_table_receipts.jsonl
```

Noncanonical duplicate:

```text
reports/transition_table_receipts 2.jsonl
```

## Current Interpretation

The proof surface now separates:

```text
representation
role binding
transition binding
continuation path
consequence authority
commit-time admissibility
replay/reconstruction
recoverable convergence
system-coherent boundary evolution
public mirror integrity
current-report preservation
theorem-map consistency
```

The Transition Table is now a validated public map of admissible transition classes, theorem coverage, and consequence-bearing state movement.
