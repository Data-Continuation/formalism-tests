# formalism-tests

## Repository Purpose

`formalism-tests` is the executable proof and validation repository for the StegVerse transition formalism.

This repository is the proof authority for the transition-table and admissibility work. It contains fixtures, declared tasks, headless validators, reports, receipts, theorem maps, runtime-artifact handling, and current-report preservation rules.

This repository is not the public presentation site. The public presentation surface is expected to live in:

```text
StegVerse-Labs/Site
```

The authority boundary is:

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
| Transition Table Classes | Verified | Transition types are treated as admissibility contracts, not labels. |
| Stage 6 Unified Gate | Verified | 10 Stage 6 candidates and 320 assertions validate the unified AE gate. |
| Representation Non-Consequence | Covered | Direct representation-only receipts prove representation is not consequence-bearing until bound to role, transition, and continuation path. |
| Transition Table Public Surface | Verified | Public proof-surface contract validates transition classes, elements, mobile behavior, and status source. |
| Site Mirror Integrity | Verified | Site mirror fixture snapshots match the latest proof surface. |
| Current Report Preservation | Verified | Latest proof outputs are preserved under stable `reports/current/` paths. |
| Theorem Map Consistency | Verified | Root and current theorem maps agree with latest successful proof reports. |

## Core Thesis

The current proof surface supports this claim:

```text
Admissibility is not local boundary compliance.
Admissibility is recoverable convergence across coherent, evolving, coupled boundary fields.
```

The repository validates this by separating and testing:

```text
representation
role binding
transition binding
continuation path
consequence authority
commit-time admissibility
replay/reconstruction
inference-window containment
recoverability floor
system-coherent boundary behavior
public mirror integrity
current-report preservation
theorem-map consistency
```

## Current Validated Chain

```text
Stage 2:
  same data != same continuation admissibility

Stage 3:
  local allow + local allow does not imply composite allow
  pre-commit allow does not imply commit-time allow after state drift
  replay can reconstruct receipt state but cannot reverse consequence
  recoverability and inference-window floors are admissibility conditions

Representation Non-Consequence:
  representation alone has no consequence-bearing status
  representation becomes consequence-bearing only when bound to role + transition + continuation path

Stage 6 Unified Gate:
  ALLOW(u) iff IW_tau(S,u) subset A_total
  AND RE(S -> Phi(S,u)) <= RE_max

Transition Table Public Surface:
  validated public map of transition classes, unlocked elements, mobile presentation, and single-source status

Site Mirror Integrity:
  validated Site mirror alignment with formalism-tests proof authority

Current Report Preservation:
  validated stable reports/current preservation

Theorem Map Consistency:
  validated root/current theorem-map agreement with latest reports
```

## Declared Task Chain

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

The declared-task manifest is:

```text
tools/tasks/formalism_tests_tasks.json
```

The declared-task runner is:

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

To run all enabled tasks, leave `task_id` blank.

To run a specific task, use one of:

```text
continuation_gate
compound_continuation_gate
stage6_unified_gate_tests
transition_table_public_surface_tests
representation_non_consequence_tests
site_mirror_integrity_tests
current_report_preservation_tests
theorem_map_consistency_tests
```

Example:

```text
task_id = theorem_map_consistency_tests
```

## Local Headless Run Examples

```bash
python tools/run_stage6_unified_gate_tests.py
python tools/run_transition_table_public_surface_tests.py
python tools/run_representation_non_consequence_tests.py
python tools/run_site_mirror_integrity_tests.py
python tools/run_current_report_preservation_tests.py
python tools/run_theorem_map_consistency_tests.py
```

Run a task through the declared-task runner:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id theorem_map_consistency_tests
```

## Stage 2 - Data Continuation

Public proof claim:

```text
same data != same continuation admissibility
```

Stage 2 proves that the same datum can produce different continuation decisions when assigned different consequence-bearing roles.

Validated role comparison:

| Data ID | Role | Transition | Decision |
|---|---|---|---|
| `patient-risk-text-001` | `informational_note` | `clinical_information_continuation` | `ALLOW` |
| `patient-risk-text-001` | `clinician_recommendation` | `clinical_recommendation_continuation` | `ALLOW_WITH_SIGNOFF` |
| `patient-risk-text-001` | `autonomous_medication_change` | `clinical_actuation_continuation` | `FAIL_CLOSED` |

Decision summary:

| Decision | Count |
|---|---:|
| ALLOW | 3 |
| ALLOW_WITH_SIGNOFF | 1 |
| FAIL_CLOSED | 4 |

Primary report:

```text
reports/continuation_report.md
```

Primary receipts:

```text
reports/sample_receipts.jsonl
```

Covered theorem group:

```text
Role Non-Transfer
Continuation Capacity
Fail-Closed Basis Requirement
Role-Transition Dependence
```

## Stage 3 - Compound and Temporal Continuation

Public proof claims:

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

Decision summary:

| Decision | Count |
|---|---:|
| ALLOW | 1 |
| FAIL_CLOSED | 5 |

Primary report:

```text
reports/compound_continuation_report.md
```

Primary receipts:

```text
reports/compound_receipts.jsonl
```

Covered theorem group:

```text
Local-Composite Non-Equivalence
Commit-Time Sufficiency
Replay Non-Reversal
Inference-Window Collapse
Recoverability Floor
Compound Continuation Positive Control
```

## Stage 6 - Admissible Existence Unified Gate

Stage 6 integrates AE, BC, CHF, DC, DaCo, and Triad into one unified gate.

Gate formula:

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
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

Previous status:

```text
Representation Non-Consequence: Partially covered
```

Current status:

```text
Representation Non-Consequence: Covered
```

## Transition Table Public Surface

The Transition Table is validated as a public proof surface, not merely an internal fixture set.

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
| Level 5 unlocked elements | 12+ |
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

## Site Mirror Integrity

Validated task:

```text
site_mirror_integrity_tests
```

Runner:

```text
tools/run_site_mirror_integrity_tests.py
```

Report:

```text
reports/site_mirror_integrity_report.json
```

Verified result:

| Metric | Value |
|---|---:|
| Success | true |
| Assertion count | 98 |
| Current stage | Stage 6 |
| Stage 6 candidates | 10 |
| Stage 6 assertions | 320 |
| Element count | 16 |
| Level 5 unlocked elements | 13 |
| Transition class count | 10 |
| Representation Non-Consequence status | Covered |
| Single status source | `data/formalism-tests/transition-proof-surface.json` |

This prevents drift between:

```text
formalism-tests proof authority
Site public mirror
```

## Current Report Preservation

Validated task:

```text
current_report_preservation_tests
```

Runner:

```text
tools/run_current_report_preservation_tests.py
```

Report:

```text
reports/current_report_preservation_report.json
```

Verified result:

| Metric | Value |
|---|---:|
| Success | true |
| Assertion count | 30 |
| Preserved count | 7 |
| Current directory | `reports/current` |

Current stable preserved reports:

```text
reports/current/continuation_report.md
reports/current/compound_continuation_report.md
reports/current/representation_non_consequence_report.json
reports/current/representation_non_consequence_report.md
reports/current/transition_table_public_surface_report.json
reports/current/site_mirror_integrity_report.json
reports/current/THEOREM_PROOF_MAP.md
```

Runtime artifact archival may continue under:

```text
legacy/runtime-artifacts/<timestamp>/
```

The rule is:

```text
archive old runtime outputs
preserve current proof outputs
do not let public proof evidence become hard to locate
```

## Theorem Map Consistency

Validated task:

```text
theorem_map_consistency_tests
```

Runner:

```text
tools/run_theorem_map_consistency_tests.py
```

Report:

```text
reports/theorem_map_consistency_report.json
```

Verified result:

| Metric | Value |
|---|---:|
| Success | true |
| Assertion count | 76 |
| Covered theorem count | 15 |
| Root theorem map | `THEOREM_PROOF_MAP.md` |
| Current theorem map | `reports/current/THEOREM_PROOF_MAP.md` |

This validates that:

```text
root THEOREM_PROOF_MAP.md is current
reports/current/THEOREM_PROOF_MAP.md matches root
Representation Non-Consequence is not stale
latest proof reports agree with theorem-map status
standalone fallback fixtures work when reports are not present
```

## Current Theorem Coverage

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
| Site Mirror Integrity | Covered |
| Current Report Preservation | Covered |
| Theorem Map Consistency | Covered |

## Transition Elements

Current Level 5 unlocked elements:

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
REPRESENTATION_NON_CONSEQUENCE
```

## Canonical and Noncanonical Receipts

Canonical receipt files:

```text
reports/sample_receipts.jsonl
reports/transition_table_receipts.jsonl
reports/representation_non_consequence_receipts.jsonl
```

Noncanonical duplicate:

```text
reports/transition_table_receipts 2.jsonl
```

The duplicate should not be treated as canonical proof evidence.

## Expected Repository Structure

```text
formalism-tests/
  README.md
  THEOREM_PROOF_MAP.md
  tools/
    run_declared_tasks.py
    run_stage6_unified_gate_tests.py
    run_transition_table_public_surface_tests.py
    run_representation_non_consequence_tests.py
    run_site_mirror_integrity_tests.py
    run_current_report_preservation_tests.py
    run_theorem_map_consistency_tests.py
    tasks/
      formalism_tests_tasks.json
    rules/
      runtime_artifact_rules.json
      apply_runtime_artifact_rules.py
  tests/
    fixtures/
      stage6_candidates.json
      representation_non_consequence_cases.json
      current_report_preservation_policy.json
      theorem_map_consistency_policy.json
      theorem_map_consistency_reports/
      site/
      site_mirror/
  reports/
    current/
    continuation_report.md
    compound_continuation_report.md
    representation_non_consequence_report.json
    representation_non_consequence_report.md
    representation_non_consequence_receipts.jsonl
    transition_table_public_surface_report.json
    site_mirror_integrity_report.json
    current_report_preservation_report.json
    theorem_map_consistency_report.json
  legacy/
    runtime-artifacts/
```

## Validation Philosophy

```text
No new workflow unless the existing workflow cannot express the task.
New validation should be added as a declared task.
Every theorem must eventually be tied to executable evidence.
Presentation pages do not become proof authority.
Representation alone is not consequence-bearing.
Role and transition binding determine continuation admissibility.
Local allow does not imply compound allow.
Replay is reconstruction, not reversal.
Stage 6 ALLOW requires IW containment and RE bound.
Current reports must remain findable even when runtime artifacts are archived.
Theorem maps must not drift from latest successful proof reports.
```

## Current Public Site Relationship

The Site-facing public model is:

```text
Transition Proof Surface
  -> current Stage 6 status from one shared source

Transition Discovery
  -> 0-5 color-coded element map

Transition Element Pages
  -> one page per transition element

Transition Table Classes
  -> desktop table
  -> mobile expandable periodic-style cards

Stage 6 Unified Gate
  -> public validation result
  -> 10 candidates
  -> 320 assertions
  -> PASS
```

The correct relationship remains:

```text
formalism-tests proves.
Site mirrors public proof data.
HTML pages render mirrored JSON.
```

## Next Validation Target

The next recommended validation layer is:

```text
element_dependency_closure_tests
```

Purpose:

```text
Validate that every unlocked transition element has declared dependencies
and that no Level 5 element depends on an uncovered or lower-confidence element
without an explicit boundary.
```

This moves the system from:

```text
Which elements are unlocked?
```

to:

```text
Can unlocked elements compose safely?
```

Expected checks:

```text
Each Level 5 element declares dependencies.
Every dependency resolves to a known element.
No Level 5 element depends on an uncovered theorem.
Cross-element dependencies are acyclic or explicitly cycle-bounded.
RESET_BOUNDARY and EVOLVE_BOUNDARY dependencies remain governed.
AI_BLOCK and FINCO_CHAIN dependencies cannot bypass authority or receipt-chain requirements.
```

Expected output:

```text
reports/element_dependency_closure_report.json
```

Expected task:

```text
element_dependency_closure_tests
```

## Current Bottom Line

`formalism-tests` has moved from isolated theorem tests into a validated proof operating surface.

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
-> public Transition Table proof surface
-> Site mirror integrity
-> current-report preservation
-> theorem-map consistency
```

The next step is dependency closure across unlocked transition elements.
