# formalism-tests

## Repository Purpose

formalism-tests is the executable proof and validation repository for the StegVerse transition formalism.

Authority boundary:

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

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
Stage 10 - Canonical Transition Table Release: RELEASE_CANDIDATE
```

## Active Declared Tasks

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
stage9_reconciliation_tests
stage10_canonical_release_tests
transition_table_public_surface_tests
representation_non_consequence_tests
site_mirror_integrity_tests
current_report_preservation_tests
theorem_map_consistency_tests
```

## Run

```text
Actions
-> Data Continuation Tests
-> Run workflow
```

Stage 9:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = stage9_reconciliation_tests
```

Stage 10:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = stage10_canonical_release_tests
```

## Stage 9 Reconciliation

Runner:

```text
tools/run_stage9_reconciliation_tests.py
```

Report:

```text
reports/stage9_reconciliation_report.json
```

It validates that README.md, THEOREM_PROOF_MAP.md, docs/, policies, and the active task manifest are reconciled through Stage 10.

## Stage 10 Canonical Transition Table Release

Runner:

```text
tools/run_stage10_canonical_release_tests.py
```

Report:

```text
reports/stage10_canonical_release_report.json
```

Artifacts:

```text
dist/transition-table-v1-rc1/canonical_transition_table_release.json
dist/transition-table-v1-rc1/canonical_transition_table_release.sha256
dist/transition-table-v1-rc1/replay_packet.json
dist/transition-table-v1-rc1/release_receipt.json
```

Release candidate:

```text
release_id: transition-table-v1-rc1
canonical_status: release_candidate
canonical_element_count: 13
coupling_class_count: 9
next_release_state: transition-table-v1
```

## Documentation

```text
docs/STAGE_10_CANONICAL_RELEASE.md
docs/TRANSITION_TABLE_STATUS.md
docs/VALIDATION_ROADMAP.md
```

## Current Bottom Line

formalism-tests now validates:

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
-> public proof surface
-> Site mirror integrity
-> current-report preservation
-> theorem-map consistency
-> canonical release-candidate generation
```
