# Theorem Proof Map

## Purpose

This file maps DCF theorem candidates and transition-stage proof layers to executable proof artifacts.

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Current Workflow Evidence

```text
archive_runtime_artifacts
continuation_gate
compound_continuation_gate
transition_table_gate
boundary_transition_gate
stage6_unified_gate_tests
element_dependency_closure_tests
stage8_ai_domain_tests
stage9_multi_body_coupling_tests
transition_table_public_surface_tests
representation_non_consequence_tests
site_mirror_integrity_tests
current_report_preservation_tests
theorem_map_consistency_tests
stage9_reconciliation_tests
```

## Mapping

| Theorem / Proof Layer | Current evidence | Status |
|---|---|---|
| Representation Non-Consequence | Direct representation-only receipts show NO_CONSEQUENCE until a datum is bound to a consequence-bearing role, transition, and continuation path. | Covered |
| Role Non-Transfer | Same patient-risk datum produces ALLOW, ALLOW_WITH_SIGNOFF, and FAIL_CLOSED across roles. | Covered |
| Continuation Capacity | Insufficient capacity cases fail closed. | Covered |
| Fail-Closed Basis Requirement | Missing required block basis fails closed. | Covered |
| Local-Composite Non-Equivalence | Stage 3 compound-local-001 proves local ALLOW plus local ALLOW may fail closed when composite consequence mass exceeds legitimacy capacity. | Covered |
| Commit-Time Sufficiency | Stage 3 drift-commit-001 proves pre-commit state is not sufficient after commit-time drift. | Covered |
| Replay Non-Reversal | Stage 3 replay-non-reversal-001 proves replay reconstructs receipt state but does not reverse consequence. | Covered |
| Inference-Window Collapse | Stage 3 inference-collapse-001 proves collapsed inference window fails closed. | Covered |
| Recoverability Floor | Stage 3 recoverability-floor-001 proves recoverability below floor fails closed. | Covered |
| Role-Transition Dependence | Covered by role comparison and same-data continuation decisions. | Covered |
| Compound Continuation Positive Control | Stage 3 compound-allow-001 proves compound continuation can ALLOW when capacity and recoverability bounds hold. | Covered |
| Stage 6 Unified Gate | Stage 6 validates 10 candidates and 320 assertions. | Covered |
| Stage 7 Element Dependency Closure | Stage 7 validates 13 elements and 105 assertions. | Covered |
| Stage 8 AI Domain Transition Classes | Stage 8 validates 8 AI-domain candidates and 64 assertions. | Covered |
| Stage 9 Multi-Body Coupling Closure | Stage 9 validates 10 candidates, 80 assertions, and all 9 declared multi-body coupling classes. | Covered |
| Transition Table Public Surface | Public surface runner validates transition classes, elements, single-source status, and mobile contract. | Covered |
| Site Mirror Integrity | Site mirror runner validates public mirror alignment with formalism-tests proof authority. | Covered |
| Current Report Preservation | Current-report runner preserves successful reports under reports/current. | Covered |
| Theorem Map Consistency | Theorem-map runner verifies root and current theorem maps agree with proof reports. | Covered |
| Stage 9 Reconciliation | Stage 9 reconciliation runner verifies documentation, theorem map, policies, and declared-task state are reconciled through Stage 9. | Covered |

## Stage 2 Proof Surface

```text
same data != same continuation admissibility
```

## Stage 3 Proof Surface

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

## Stage 6 Unified Gate Proof Surface

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

## Stage 7 Element Dependency Closure Proof Surface

```text
elements: 13
assertions: 105
passed: 105
failed: 0
result: PASS
```

## Stage 8 AI Domain Transition Class Proof Surface

```text
candidates: 8
assertions: 64
result: PASS
```

## Stage 9 Multi-Body Coupling Closure Proof Surface

```text
candidates: 10
assertions: 80
coupling_classes_tested: 9
result: PASS
```

Tested coupling classes:

```text
authority-transfer
coherence-coupled
distributed-node
irreversible-consequence
isolated
multi-agent-cascade
paired-boundary
shared-resource
trust-field
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
dependency closure
AI-domain participation
multi-body coupling closure
public mirror integrity
current-report preservation
theorem-map consistency
stage reconciliation
```

The next proof layer is Stage 10 - Canonical Transition Table Release.
