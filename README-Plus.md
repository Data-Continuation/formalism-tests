# formalism-tests

## Repository Purpose

formalism-tests is the executable proof and validation repository for the StegVerse transition formalism.

This repository is the proof authority for transition-table and admissibility work. It contains fixtures, declared tasks, headless validators, reports, receipts, theorem maps, runtime-artifact handling, current-report preservation rules, and reconciliation tests.

Authority boundary:

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Current Status

| Area | Status | Summary |
|---|---|---|
| Stage 2 Data Continuation | Verified | Same data can produce different continuation decisions depending on role and consequence path. |
| Stage 3 Compound Continuation | Verified | Compound, temporal, replay, inference-window, and recoverability constraints are tested. |
| Stage 6 Unified Gate | Verified | 10 candidates and 320 assertions validate the unified AE gate. |
| Stage 7 Element Dependency Closure | Verified | 13 elements and 105 assertions validate dependency closure. |
| Stage 8 AI Domain Transition Classes | Verified | 8 AI-domain candidates and 64 assertions validate AI governance, derivation, verification, quorum, hidden authority, closure, and scope behavior. |
| Stage 9 Multi-Body Coupling Closure | Verified | 10 candidates and 80 assertions validate all 9 declared multi-body coupling classes. |
| Representation Non-Consequence | Covered | Representation alone is not consequence-bearing until bound to role, transition, and continuation path. |
| Transition Table Public Surface | Verified | Public proof-surface contract validates transition classes, elements, mobile behavior, and status source. |
| Site Mirror Integrity | Verified | Site mirror fixture snapshots match the proof surface. |
| Current Report Preservation | Verified | Latest proof outputs are preserved under stable reports/current paths. |
| Theorem Map Consistency | Verified | Root and current theorem maps agree with successful proof reports. |
| Stage 9 Reconciliation | Verified | Documentation, theorem map, policies, and declared-task state are reconciled through Stage 9. |

## Current Stage Picture

```text
Stage 1 - Initial continuation model / seed cases
Stage 2 - Same-data role dependence: PASS
Stage 3 - Compound and temporal continuation: PASS
Stage 4 - Transition classes as admissibility contracts: PASS
Stage 5 - System-coherent boundary transition classes: PASS
Stage 6 - Admissible Existence Unified Gate: PASS
Stage 7 - Element Dependency Closure: PASS
Stage 8 - AI Domain Transition Classes: PASS
Stage 9 - Multi-Body Coupling Closure: PASS
Stage 10 - Canonical Transition Table Release: NEXT
```

## Declared Task Chain

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

Manifest:

```text
tools/tasks/formalism_tests_tasks.json
```

Runner:

```text
tools/run_declared_tasks.py
```

## How to Run Tests

Use GitHub Actions:

```text
Actions
-> Data Continuation Tests
-> Run workflow
```

Set:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
```

To run one task:

```text
task_id = stage9_reconciliation_tests
```

## Stage 7 - Element Dependency Closure

Validated task:

```text
element_dependency_closure_tests
```

Runner:

```text
tools/run_element_dependency_closure_tests.py
```

Expected outputs:

```text
reports/element_dependency_closure_report.json
reports/element_dependency_closure_receipts.jsonl
```

Verified result:

```text
elements: 13
assertions: 105
passed: 105
failed: 0
result: PASS
```

## Stage 8 - AI Domain Transition Classes

Validated task:

```text
stage8_ai_domain_tests
```

Runner:

```text
tools/run_stage8_ai_domain_tests.py
```

Expected outputs:

```text
reports/stage8_ai_domain_report.json
reports/stage8_ai_domain_receipts.jsonl
```

Verified result:

```text
candidates: 8
assertions: 64
result: PASS
```

Stage 8 validates:

```text
AI governance agent
AI derivation agent
AI verification agent
AI quorum gate
AI_BLOCK scope enforcement
dependency closure failure
hidden authority failure
scope violation failure
```

After Stage 8, AI entities may propose candidates within AI_BLOCK scope when dependency closure and quorum requirements are satisfied.

## Stage 9 - Multi-Body Coupling Closure

Validated task:

```text
stage9_multi_body_coupling_tests
```

Runner:

```text
tools/run_stage9_multi_body_coupling_tests.py
```

Expected outputs:

```text
reports/stage9_multi_body_coupling_report.json
reports/stage9_multi_body_coupling_receipts.jsonl
```

Verified result:

```text
candidates: 10
assertions: 80
coupling_classes_declared: 9
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

Stage 9 validates that admissibility cannot be evaluated in isolation when entities are coupled.

## Stage 9 Reconciliation

Validated task:

```text
stage9_reconciliation_tests
```

Runner:

```text
tools/run_stage9_reconciliation_tests.py
```

Expected output:

```text
reports/stage9_reconciliation_report.json
```

This validates that:

```text
README.md includes Stage 7, Stage 8, and Stage 9
THEOREM_PROOF_MAP.md includes Stage 7, Stage 8, and Stage 9
current-report preservation policy includes Stage 7, Stage 8, and Stage 9
theorem-map consistency policy requires Stage 9
declared-task manifest includes Stage 9 and reconciliation tasks
```

## Next Validation Target

The next recommended validation layer is:

```text
Stage 10 - Canonical Transition Table Release
```

Purpose:

```text
Produce a versioned canonical transition table release with hash, manifest, replay packet, current-report snapshot, dependency closure proof, AI-domain proof, multi-body coupling proof, and Site mirror target.
```

Expected task:

```text
stage10_canonical_release_tests
```

Expected output:

```text
reports/stage10_canonical_release_report.json
```

## Current Bottom Line

formalism-tests has moved from isolated theorem tests into a validated proof operating surface.

It now validates:

```text
data representation
-> role binding
-> transition binding
-> continuation path
-> compound admissibility
-> transition class
-> boundary coherence
-> Stage 6 unified gate
-> element dependency closure
-> AI-domain transition classes
-> multi-body coupling closure
-> public Transition Table proof surface
-> Site mirror integrity
-> current-report preservation
-> theorem-map consistency
```

The next step is a canonical Stage 10 release of the Transition Table.
