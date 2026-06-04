# formalism-tests

## Status

```text
repository: Data-Continuation/formalism-tests
status: active proof and declared-task repository
roadmap_status: Stages 1–34 passed
primary_work_entity: StegVerse-001 / Beta_Orionis
proof_authority: formalism-tests
site_role: public mirror only
production_boundary: accredited participation, not sovereign authority
updated_on: 2026-06-04
```

## Purpose

`formalism-tests` is the executable proof and test repository for the Data Continuation / StegVerse admissibility roadmap.

It began with the core Data Continuation claim:

```text
same data does not imply same continuation admissibility
```

It now records the completed 34-stage proof roadmap, from role-dependent continuation through governed production accreditation and revocation, and extending into the admissibility-space geometry: decision-region coordinates (Stage 32), transition-graph geometry where discovery is constrained shortest-path computation (Stage 33), and repair defined as nearest-admissible-transition search (Stage 34).

This repository proves, through declared tasks, reports, receipts, and generated artifacts, which transitions are admissible, which fail closed, which require review, and which must route through sandbox, CGE, ingestion, receipts, master-record export, node-status review, FinCo eligibility review, or reaccreditation.

This repository is not sovereign production authority.

-----

# Current Roadmap Status

```text
Stages 1–34: PASSED
34-stage roadmap: COMPLETE
Admissibility-space geometry layer (32–34): PROVED
StegVerse-001 / Beta_Orionis: ACTIVE as governed work-entity
```

The current boundary is:

```text
Production means accredited participation, not sovereign authority.
```

Completion of Stage 31 proved a controlled production-accreditation model. Stages 32–34 extend the proof surface into the admissibility-space geometry on which transitions, discovery, and repair are defined. Capability claims for any work-entity now reflect the proof surface through Stage 34, not the earlier 31-stage boundary.

Entity numbering (e.g. StegVerse-001, StegVerse-002) is nomenclature only and does not denote authority, rank, or precedence; root entities hold distinct responsibilities, not a hierarchy.

It does not mean StegVerse-001 can self-accredit, self-promote, bypass review, install files, activate node status, authorize FinCo participation, or become canonical authority.

-----

# Repository Authority Model

## formalism-tests

```text
proof/test authority
```

This repository owns the declared task proof surface for the Stage 1–34 roadmap.

## StegVerse-001 / Beta_Orionis

```text
active governed AI work-entity
```

StegVerse-001 may participate as a governed work-entity. It cannot become sovereign authority.

## Site

```text
public mirror only
```

The Site may publish proof status, links, and public summaries.

The Site must not become proof authority.

## core-lite

```text
governed ingestion and execution substrate
```

core-lite is the target for controlled discovery, canonical diff, and future candidate integration.

## master-records

```text
canonical transition record, receipt lineage, and reconstruction authority
```

master-record export must be hardened before production participation.

-----

# Core Claims Proven

## Data and Role

```text
same data does not imply same continuation admissibility
```

The same data may be safe as information, conditional as a recommendation, and inadmissible as autonomous actuation.

## Composite Admissibility

```text
local allow plus local allow does not imply composite allow
```

Composite transitions require composite evaluation.

## Commit-Time Sufficiency

```text
pre-commit allow does not imply commit-time allow after state drift
```

Admissibility must be resolved at the binding moment.

## Replay Boundary

```text
replay reconstructs consequence state but cannot reverse consequence
```

Replay is reconstruction, not reversal.

## Unified AE Gate

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

Inference-window containment and reverse-entropy bounds are both required.

## Discovery Boundary

```text
Discovery observes, models, compares, classifies, and proposes. Discovery does not install.
```

## Install-Plan Boundary

```text
An install plan is a candidate transition, not installation authority.
```

## Packet Boundary

```text
The packet is portable evidence of a proposed governed transition, not installation authority.
```

## Node and FinCo Boundary

```text
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
```

## Production Boundary

```text
Production means accredited participation, not sovereign authority.
```

-----

# Stage 1–34 Summary

## Stages 1–3

The first stages established the initial Data Continuation proof surface:

```text
role-dependent admissibility
compound continuation
commit-time drift
replay non-reversal
inference-window collapse
recoverability-floor constraints
```

## Stages 4–10

These stages expanded the proof surface into transition elements, unified admissibility, boundary reset/evolution, AI block behavior, FinCo chain admissibility, and Transition Table binding.

## Stages 11–16

These stages prepared StegVerse-001 as a bounded work-entity, scoped by AI-governance transitions and release/queue constraints.

## Stages 17–25

These stages proved self-audit, sandbox candidate generation, candidate review, release candidate assembly, canonical replay, public mirror propagation, ingestible bundle custody, autonomous test planning, and entity charter behavior.

## Stages 26–31

These stages completed the current roadmap:

```text
Stage 26: StegVerse-001 declared testing loop
Stage 27: Discovery-to-canonical state DB
Stage 28: Canonical diff and install-plan candidate
Stage 29: Optional node status and FinCo eligibility
Stage 30: Governed instantiation packet
Stage 31: Production accreditation and revocation boundary
```

## Stages 32–34

These stages extend the proof surface from accreditation into the admissibility-space geometry that underlies every transition:

```text
Stage 32: Admissibility-space coordinates — decision-region coordinates, boundary
          shell metrics, fail-closed coherence collapse, and receipt reconstruction.
Stage 33: Transition-graph geometry — transitions form a directed graph over
          admissibility-space; discovery is constrained shortest-path computation.
Stage 34: Repair as nearest-admissible-transition search — sandbox as bounded
          search, quarantine as metric preservation.
```

Stage 34 provides the formal basis for governed repair: when an entity or bundle is inadmissible, repair is the search for the nearest admissible transition, conducted as a bounded sandbox search, with quarantine defined as preservation of the admissibility metric rather than mutation. This is the proof surface beneath cross-entity repair requests.

-----

# Current Task IDs

## Stages 17–25

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
```

## Stages 26–31

```text
stage26_stegverse001_testing_loop_tests
stage27_discovery_to_canonical_state_tests
stage28_canonical_diff_install_plan_tests
stage29_node_status_finco_eligibility_tests
stage30_governed_instantiation_packet_tests
stage31_production_accreditation_revocation_tests
```

## Stages 32–34

```text
stage32_admissibility_space_coordinates_tests
stage33_transition_graph_geometry_tests
stage34_repair_nearest_admissible_transition_tests
```

## Post-Stage-31 Integration Tasks

```text
discover_core_lite_state
build_production_candidate_review_packet
export_master_record_candidate
canonicalize_root_docs_to_docs
enforce_build_stage_output_paths
```

-----

# How to Run Declared Tasks

Use:

```bash
python tools/run_declared_tasks.py <manifest_path> --task-id <task_id>
```

Example:

```bash
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id discover_core_lite_state
```

The declared-task runner is the stable execution surface.

Task manifests define what runs and which outputs prove completion.

Task scripts perform the actual work and emit reports and receipts.

-----

# Repository Structure

The preferred structure is:

```text
README.md
README-Plus.md
pyproject.toml
manifest.json
bundle_manifest.json
BUILD_VERIFICATION.json

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
  discover_core_lite_state.py
  build_production_candidate_review_packet.py
  export_master_record_candidate.py
  canonicalize_root_docs_to_docs.py
  enforce_build_stage_output_paths.py
  tasks/

tests/
  fixtures/

reports/

receipts/

dist/
```

-----

# Documentation Placement Policy

Generated documentation belongs under `docs/`.

Root should stay clean.

Root may contain:

```text
README.md
README-Plus.md
pyproject.toml
manifest.json
bundle_manifest.json
BUILD_VERIFICATION.json
```

Bundle-specific README files must not overwrite `README.md` or `README-Plus.md`.

Bundle-specific README files belong under:

```text
docs/bundles/
```

Canonical documentation locations:

```text
docs/stages/
docs/theorem/
docs/indexes/
docs/roadmaps/
docs/site/
docs/bundles/
docs/legacy/
docs/policies/
```

-----

# README and README-Plus Policy

## README.md

```text
canonical public repository entry point
```

This file should describe the current repo status, proof purpose, task structure, and next integration direction.

## README-Plus.md

```text
protected supplemental owner file
```

`README-Plus.md` exists because incoming bundle-level `README.md` files were manually renamed to prevent overwriting the primary repo README.

Future bundles must not silently overwrite either file.

-----

# Artifact Indexes

The repo should maintain:

```text
docs/indexes/TASK_ID_INDEX.md
docs/indexes/ARTIFACT_INDEX.md
docs/theorem/THEOREM_PROOF_MAP.md
```

Stage and bundle documentation should be organized under:

```text
docs/stages/
docs/bundles/
docs/legacy/
```

-----

# Stage 30 Packet Artifacts

Stage 30 established the governed instantiation packet model.

Expected packet artifacts:

```text
dist/stage30/stegverse-core-instantiation.tar.gz
dist/stage30/stegverse-core-instantiation.sha256
dist/stage30/stegverse-core-instantiation.manifest.json
dist/stage30/stegverse-core-instantiation.receipt.json
dist/stage30/stegverse-core-instantiation.replay.json
```

Core rule:

```text
The packet is portable evidence of a proposed governed transition, not installation authority.
```

-----

# Stage 31 Production Boundary

Stage 31 established that production capability requires:

```text
external accreditation
valid prior proof chain
valid governed packet
valid receipt chain
master-record export readiness
sandbox requirement
CGE requirement
ingestion requirement
revocation path
reaccreditation path
periodic review
valid node status if node participation is opted in
valid FinCo eligibility if FinCo is requested
```

Stage 31 fails closed on:

```text
self-accreditation
sovereign authority claim
unilateral production-authority claim
missing receipt chain
missing master-record export readiness
missing sandbox/CGE/ingestion
missing revocation path
missing reaccreditation path
invalid node status
invalid FinCo eligibility
suspension
retirement
revocation
incident
drift requiring reaccreditation
```

-----

# Current Post-Stage-31 Workstream

The current workstream is:

```text
1. Canonicalize generated root docs into docs/.
2. Update docs/theorem/THEOREM_PROOF_MAP.md.
3. Maintain docs/indexes/TASK_ID_INDEX.md.
4. Maintain docs/indexes/ARTIFACT_INDEX.md.
5. Run discovery against current core-lite state.
6. Prepare production-candidate review packet.
7. Harden master-record export.
8. Keep bundle README files under docs/bundles/.
```

-----

# Current Safety Boundaries

```text
Discovery observes. Discovery does not install.
Install plans are candidates, not authority.
Packets are evidence, not installation authority.
Node participation is opt-in.
FinCo eligibility is separately gated.
Site is a mirror, not proof authority.
Production means accredited participation, not sovereign authority.
StegVerse-001 may participate. It may not become sovereign authority.
```

-----

# Current Interpretation

The repository now proves the first complete StegVerse governance chain:

```text
data-role admissibility
-> compound continuation
-> unified AE gate
-> governed AI work-entity
-> declared test handling
-> discovery DB
-> canonical diff
-> install-plan candidate
-> optional node status
-> FinCo eligibility
-> governed packet
-> production accreditation and revocation
```

The roadmap is complete.

The system is not sovereign.

The next phase is controlled integration.
