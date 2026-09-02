# formalism-tests

## Status

```text
repository: Data-Continuation/formalism-tests
status: active proof and declared-task repository
roadmap_status: Stages 1–34 passed; denial-reachability commit-boundary proof passed
primary_work_entity: StegVerse-001 / Beta_Orionis
proof_authority: formalism-tests
site_role: public mirror only
production_boundary: accredited participation, not sovereign authority
updated_on: 2026-07-13
```

## Purpose

`formalism-tests` is the executable proof and test repository for the Data Continuation / StegVerse admissibility roadmap.

It began with the core Data Continuation claim:

```text
same data does not imply same continuation admissibility
```

It now records the completed 34-stage proof roadmap and the post-roadmap denial-reachability proof at the consequence-binding commit boundary.

## Current proof additions

### Denial reachability at commit

A consequence-binding transition is governable only while denial remains both reachable and enforceable until the decision controls execution.

Installed declared task:

```text
denial_reachability_commit_boundary_tests
```

Run with:

```bash
python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests
```

Proof result:

```text
status: PASS
cases: 5
passed: 5
failed: 0
report_sha256: 8c2c460e3d7ae790a4f5fc347e44f9e91615db8b1913ee98c893e3071a5fb284
```

Cases:

```text
REACHABLE_DENY
UNREACHABLE_DENY
COSMETIC_GATING
LATE_REFUSAL
SPLIT_BOUNDARY_INSUFFICIENCY
```

The proof distinguishes prevention from post-hoc refusal: `LATE_REFUSAL` fails closed but records `execution_prevented: false` because consequence had already bound.

Canonical artifacts:

```text
tests/fixtures/denial_reachability_cases.json
tests/fixtures/denial_reachability_expected_outcomes.json
tools/run_denial_reachability_tests.py
tools/tasks/denial_reachability_tasks.json
reports/denial_reachability_report.json
reports/denial_reachability_continuation_report.md
receipts/denial_reachability_execution_receipts.jsonl
FORMALISM_TESTS_MIRROR_HANDOFF.md
```

## Repository Authority Model

```text
formalism-tests: proof/test authority
StegVerse-001 / Beta_Orionis: active governed AI work-entity
Site: public mirror only
core-lite: governed ingestion and execution substrate
master-records: canonical transition record, receipt lineage, and reconstruction authority
```

This repository is not sovereign production authority.

## Core Claims Proven

```text
same data does not imply same continuation admissibility
local allow plus local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay reconstructs consequence state but cannot reverse consequence
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
Discovery observes, models, compares, classifies, and proposes. Discovery does not install.
An install plan is a candidate transition, not installation authority.
The packet is portable evidence of a proposed governed transition, not installation authority.
Production means accredited participation, not sovereign authority.
Authorization without a reachable and enforceable deny path is inherited rather than decided.
```

## Roadmap Status

```text
Stages 1–34: PASSED
34-stage roadmap: COMPLETE
Admissibility-space geometry layer (32–34): PROVED
Denial-reachability commit-boundary proof: PASSED
StegVerse-001 / Beta_Orionis: ACTIVE as governed work-entity
```

## Current Task IDs

```text
stage17_self_audit_tests
stage18_sandbox_candidate_generation_tests
stage19_candidate_review_loop_tests
stage20_release_candidate_assembly_tests
stage21_canonical_upgrade_replay_tests
stage22_public_mirror_propagation_tests
stage23_ingestible_bundle_tests
stage24_test_plan_tests
stage25_entity_charter_tests
stage26_stegverse001_testing_loop_tests
stage27_discovery_to_canonical_state_tests
stage28_canonical_diff_install_plan_tests
stage29_node_status_finco_eligibility_tests
stage30_governed_instantiation_packet_tests
stage31_production_accreditation_revocation_tests
stage32_admissibility_space_coordinates_tests
stage33_transition_graph_geometry_tests
stage34_repair_nearest_admissible_transition_tests
stage35_stegverse001_bounded_autonomy_tests
denial_reachability_commit_boundary_tests
discover_core_lite_state
build_production_candidate_review_packet
export_master_record_candidate
canonicalize_root_docs_to_docs
enforce_build_stage_output_paths
```

## How to Run Declared Tasks

Use:

```bash
python tools/run_declared_tasks.py <manifest_path> --task-id <task_id>
```

The declared-task runner is the stable execution surface. Task manifests define what runs and which outputs prove completion. Task scripts perform the work and emit reports and receipts.

## Preferred Repository Structure

```text
README.md
README-Plus.md
pyproject.toml
manifest.json
bundle_manifest.json
BUILD_VERIFICATION.json
FORMALISM_TESTS_MIRROR_HANDOFF.md

docs/
  bundles/
  indexes/
  legacy/
  policies/
  roadmaps/
  site/
  stages/
  theorem/

tools/
  run_declared_tasks.py
  tasks/

tests/
  fixtures/

reports/
receipts/
dist/
```

Generated documentation belongs under `docs/`. Root remains limited to canonical repository files and the current mirror handoff.

## Artifact Indexes

The repository should maintain:

```text
docs/indexes/TASK_ID_INDEX.md
docs/indexes/ARTIFACT_INDEX.md
docs/theorem/THEOREM_PROOF_MAP.md
```

## Boundary

Completion of a proof does not itself grant installation, node, financial, publication, or sovereign authority. Every downstream transition remains independently governed and receipt-bound.


## Stage 35 — StegVerse-001 Bounded Autonomy

Stage 35 is additive to the completed 34-stage roadmap. It tests whether `StegVerse-001 / Beta_Orionis` can operate under a bounded autonomy lease while preserving external authority, commit-time denial reachability, revocation, receipt emission, and Stage-34 repair constraints.

Source completion or CI success does not establish authentic autonomous runtime operation.
