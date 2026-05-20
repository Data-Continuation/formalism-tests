# formalism-tests

## Repository Purpose

`formalism-tests` is the executable validation repository for the StegVerse transition-theorem proof surface.

This repository is not a presentation site. It is the proof and receipt authority for the transition formalism work. It contains fixtures, declared tasks, headless validators, reports, receipts, theorem maps, and runtime-artifact routing rules that validate whether proposed transition concepts are actually executable under the StegVerse admissibility model.

The public Site repository may mirror selected results from this repository, but the authority boundary is:

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```

## Current Status

The repository has advanced through the following verified layers:

| Layer | Status | Summary |
|---|---|---|
| Stage 2 | Verified | Same data can produce different continuation decisions depending on role and consequence path. |
| Stage 3 | Verified | Compound, temporal, replay, inference-window, and recoverability failures are independently tested. |
| Stage 4 | Verified | Transition classes are treated as admissibility contracts, not labels. |
| Stage 5 | Verified | Boundary transition classes validate system coherence, convergence, and recoverability constraints. |
| Stage 6 | Verified | The Admissible Existence Unified Gate validates 10 candidates and 320 assertions. |
| Transition Table Public Surface | Verified | The public proof surface validates 10 transition classes, 16 elements, 12 Level 5 unlocked elements, and 297 assertions. |
| Representation Non-Consequence | Verified | Direct receipts now prove representation alone has no consequence-bearing status until bound to role, transition, and continuation path. |

## Core Claim

The current proof surface supports the following central claim:

```text
Admissibility is not local boundary compliance.
Admissibility is recoverable convergence across coherent, evolving, coupled boundary fields.
```

This repository validates that claim by testing the difference between:

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
```

## Current Verified Results

### Stage 2 — Same-Data Role Dependence

Public proof claim:

```text
same data ≠ same continuation admissibility
```

The same datum can be safe as an informational note, conditional as a clinician recommendation, and inadmissible as autonomous actuation.

Current report:

```text
reports/continuation_report.md
```

Current receipt file:

```text
reports/sample_receipts.jsonl
```

Decision summary:

| Decision | Count |
|---|---:|
| ALLOW | 3 |
| ALLOW_WITH_SIGNOFF | 1 |
| FAIL_CLOSED | 4 |

Theorem coverage:

| Theorem | Status |
|---|---|
| Role Non-Transfer | Covered |
| Continuation Capacity | Covered |
| Fail-Closed Basis Requirement | Covered |
| Role-Transition Dependence | Covered |

## Stage 3 — Compound and Temporal Admissibility

Public proof claims:

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

Current report:

```text
reports/compound_continuation_report.md
```

Current receipt file:

```text
reports/compound_receipts.jsonl
```

Decision summary:

| Decision | Count |
|---|---:|
| ALLOW | 1 |
| FAIL_CLOSED | 5 |

Theorem coverage:

| Theorem | Status |
|---|---|
| Local-Composite Non-Equivalence | Covered |
| Commit-Time Sufficiency | Covered |
| Replay Non-Reversal | Covered |
| Inference-Window Collapse | Covered |
| Recoverability Floor | Covered |
| Compound Continuation Positive Control | Covered |

## Stage 4 — Transition Classes as Admissibility Contracts

Public proof claim:

```text
a transition type is not only a label; it is an admissibility contract
```

Stage 4 verifies that transition classes must include explicit admissibility properties, including:

```text
transition_id
transition_name
transition_family
theorem_basis
role
periodic_table_coordinates
consequence_mass
legitimacy_capacity_required
recoverability_floor
recoverability_score
inference_window_width
inference_window_minimum
commit_time_state_required
replay_semantics
boundary_behavior
multi_body_coupling_class
expected decision
basis
```

Current receipt file:

```text
reports/transition_table_receipts.jsonl
```

Important cleanup note:

```text
reports/transition_table_receipts 2.jsonl
```

has been identified as a duplicate of:

```text
reports/transition_table_receipts.jsonl
```

The canonical file to preserve is:

```text
reports/transition_table_receipts.jsonl
```

## Stage 5 — Boundary Transition Classes

Stage 5 validates system-coherent boundary transition behavior.

This layer extends transition validation from local continuation into coupled boundary fields, including:

```text
boundary load-capacity failure
consequence horizon absorption breach
purpose-convergence failure
distributed local-pass/global-fail
split-brain coherence failure
governed boundary reset
governed boundary evolution
```

Current receipt file:

```text
reports/boundary_transition_receipts.jsonl
```

## Stage 6 — Admissible Existence Unified Gate

Stage 6 integrates the prior layers into the unified admissibility gate.

Gate formula:

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

Components covered:

```text
AE
BC
CHF
DC
DaCo
Triad
```

Validated task:

```text
stage6_unified_gate_tests
```

Runner:

```text
tools/run_stage6_unified_gate_tests.py
```

Fixture:

```text
tests/fixtures/stage6_candidates.json
```

Verified result:

| Metric | Value |
|---|---:|
| Candidate count | 10 |
| Assertion count | 320 |
| Success | true |

Decision summary:

| Decision | Count |
|---|---:|
| ALLOW | 3 |
| FAIL_CLOSED | 5 |
| RESET_BOUNDARY | 1 |
| EVOLVE_BOUNDARY | 1 |

Stage 6 validates:

```text
IW containment
RE bound
dual IW/RE breach
recoverable non-convergence
governed boundary reset
governed boundary evolution
AI Block scope control
FinCo receipt-chain integrity
fail-closed behavior
```

## Transition Table Public Surface Validation

The Transition Table has now been validated as a public proof surface, not merely as an internal math fixture.

Validated task:

```text
transition_table_public_surface_tests
```

Runner:

```text
tools/run_transition_table_public_surface_tests.py
```

Report:

```text
reports/transition_table_public_surface_report.json
```

Verified result:

| Metric | Value |
|---|---:|
| Success | true |
| Assertion count | 297 |
| Current stage | Stage 6 |
| Transition class count | 10 |
| Element count | 16 |
| Level 5 unlocked elements | 12 |
| Single status source | `data/formalism-tests/transition-proof-surface.json` |

This validates:

```text
single-source public status
Stage 6 verified status
Stage 6 declared-task result
Transition Discovery map coverage
element detail-page coverage
transition class coverage
RESET_BOUNDARY and EVOLVE_BOUNDARY presence
mobile presentation contract
public Site proof-surface contract
```

## Representation Non-Consequence

Representation Non-Consequence is now directly covered.

Theorem claim:

```text
Representation alone has no consequence-bearing status until it is bound to a transition role and continuation path.
```

Validated task:

```text
representation_non_consequence_tests
```

Runner:

```text
tools/run_representation_non_consequence_tests.py
```

Fixture:

```text
tests/fixtures/representation_non_consequence_cases.json
```

Reports:

```text
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
```

Receipts:

```text
reports/representation_non_consequence_receipts.jsonl
```

Verified result:

| Metric | Value |
|---|---:|
| Success | true |
| Case count | 7 |
| Receipt count | 7 |
| Assertion count | 18 |

Decision summary:

| Decision | Count |
|---|---:|
| NO_CONSEQUENCE | 3 |
| ALLOW | 1 |
| ALLOW_WITH_SIGNOFF | 1 |
| FAIL_CLOSED | 2 |

This closes the previous theorem gap.

Previous status:

```text
Representation Non-Consequence: Partially covered
```

Current status:

```text
Representation Non-Consequence: Covered
```

## Theorem Coverage

Current theorem coverage:

| Theorem | Status |
|---|---|
| Representation Non-Consequence | Covered |
| Role Non-Transfer | Covered |
| Continuation Capacity | Covered |
| Fail-Closed Basis Requirement | Covered |
| Local-Composite Non-Equivalence | Covered |
| Commit-Time Sufficiency | Covered |
| Replay Non-Reversal | Covered |
| Inference-Window Collapse | Covered |
| Recoverability Floor | Covered |
| Role-Transition Dependence | Covered |
| Compound Continuation Positive Control | Covered |
| Stage 6 Unified Gate | Covered |
| Transition Table Public Surface | Covered |

## Declared Task Model

This repository uses a declared-task model.

The existing workflow runs:

```text
tools/run_declared_tasks.py
```

The workflow should remain stable. New validation should be added as declared tasks and headless Python runners, not as new workflow files.

Declared task manifest:

```text
tools/tasks/formalism_tests_tasks.json
```

Current important tasks:

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

## How to Run Tests Through the Existing Workflow

Open GitHub Actions for the repository.

Select:

```text
Data Continuation Tests
```

Click:

```text
Run workflow
```

Use:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
```

To run all enabled tasks, leave `task_id` blank.

To run one task, set `task_id` to one of:

```text
stage6_unified_gate_tests
transition_table_public_surface_tests
representation_non_consequence_tests
```

## Local Headless Runs

Run Stage 6:

```bash
python tools/run_stage6_unified_gate_tests.py
```

Run Transition Table public-surface validation:

```bash
python tools/run_transition_table_public_surface_tests.py
```

Run Representation Non-Consequence validation:

```bash
python tools/run_representation_non_consequence_tests.py
```

Run through the declared-task runner:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id representation_non_consequence_tests
```

## Runtime Artifact Routing

Runtime artifacts may be moved into:

```text
legacy/runtime-artifacts/<timestamp>/
```

This is expected when the runtime artifact routing task executes.

However, current proof reports should be intentionally preserved when they form part of the public proof surface.

Recommended stable reports to preserve:

```text
reports/continuation_report.md
reports/compound_continuation_report.md
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
reports/representation_non_consequence_receipts.jsonl
reports/transition_table_public_surface_report.json
reports/transition_table_receipts.jsonl
reports/sample_receipts.jsonl
```

Duplicate artifact to avoid preserving:

```text
reports/transition_table_receipts 2.jsonl
```

## Site Relationship

`StegVerse-Labs/Site` is the public presentation surface.

It should mirror public proof data from this repository, especially:

```text
data/formalism-tests/transition-proof-surface.json
data/formalism-tests/transition-discovery-map.json
data/formalism-tests/transition-table-classes.json
```

The Site should not generate receipts.

The correct relationship is:

```text
formalism-tests proves.
Site mirrors public proof data.
HTML pages render mirrored JSON.
```

## Transition Table Public Presentation Model

The current Site-facing public model is:

```text
Transition Proof Surface
  → current Stage 6 status from one shared source

Transition Discovery
  → 0–5 color-coded element map

Transition Element Pages
  → one page per transition element

Transition Table Classes
  → desktop table
  → mobile expandable periodic-style cards

Stage 6 Unified Gate
  → public validation result
  → 10 candidates
  → 320 assertions
  → PASS
```

## Unlocked Transition Elements

Current mapped elements:

| Level | Count | Meaning |
|---:|---:|---|
| 5 | 12 | Unified |
| 4 | 3 | Integrated |
| 2 | 1 | Partitioned |

Level 5 unlocked elements:

```text
AE
BC
CHF
DC
DaCo
Triad
IW
RE
RESET_BOUNDARY
EVOLVE_BOUNDARY
AI_BLOCK
FINCO_CHAIN
```

## Repository Structure

Expected structure:

```text
formalism-tests/
  README.md
  THEOREM_PROOF_MAP.md
  tools/
    run_declared_tasks.py
    run_stage6_unified_gate_tests.py
    run_transition_table_public_surface_tests.py
    run_representation_non_consequence_tests.py
    tasks/
      formalism_tests_tasks.json
    rules/
      runtime_artifact_rules.json
      apply_runtime_artifact_rules.py
  tests/
    fixtures/
      stage6_candidates.json
      representation_non_consequence_cases.json
      site/
        transition-proof-surface.json
        transition-discovery-map.json
        transition-table-classes.json
        site-public-surface-contract.json
  reports/
    continuation_report.md
    compound_continuation_report.md
    representation_non_consequence_report.json
    representation_non_consequence_report.md
    representation_non_consequence_receipts.jsonl
    transition_table_public_surface_report.json
    transition_table_receipts.jsonl
    sample_receipts.jsonl
  legacy/
    runtime-artifacts/
      <timestamp>/
```

## Validation Philosophy

This repository follows a strict validation discipline:

```text
No new workflow unless the existing workflow cannot express the task.
No presentation page becomes receipt authority.
No theorem is considered covered without executable evidence.
No transition class is treated as valid merely because it is named.
No representation is consequence-bearing until role + transition + continuation path are bound.
No local allow implies global allow.
No replay is treated as reversal.
No Stage 6 ALLOW exists without IW containment and RE bound.
```

## Next Validation Targets

Recommended next validation targets:

### 1. Stable Report Preservation

Current runtime artifact routing may archive reports that should remain available as current proof outputs.

Next step:

```text
Add an intentional current-report preservation rule or reports/current/ mirror.
```

Goal:

```text
Public proof reports remain easy to locate after runtime archival.
```

### 2. Site Mirror Integrity

Validate that the Site mirror exactly matches the latest proof reports from this repository.

Possible task:

```text
site_mirror_integrity_tests
```

This should check:

```text
Site status JSON matches latest theorem reports.
Site discovery elements match theorem coverage.
Site transition table matches validated classes.
Site Stage 6 page matches latest Stage 6 result.
```

### 3. Stage 7 Candidate Discovery

Potential Stage 7 scope:

```text
multi-body transition expansion
element-to-element dependency closure
cross-element composition validation
public element page completeness
dynamic unlock progression
receipt-chain continuity across theorem layers
```

### 4. Representation-to-Transition Generalization

Representation Non-Consequence is now directly covered. The next proof extension should generalize beyond clinical and policy text examples.

Potential new domains:

```text
financial signal representation
identity assertion representation
AI model output representation
credential-state representation
physical-control representation
governance rule representation
```

## Current Bottom Line

The repository has now moved beyond isolated theorem tests.

It validates a connected proof surface:

```text
data representation
→ role binding
→ continuation path
→ compound admissibility
→ transition class
→ boundary coherence
→ Stage 6 unified gate
→ public Transition Table proof surface
```

The Transition Table is now more than a catalog.

It is becoming a validated public map of admissible transition classes, theorem coverage, and consequence-bearing state movement.
