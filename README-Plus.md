# Post-Stage-31 Integration Bundle

## Assumptions

1. Stages 1–31 have passed.
2. The next major items are documentation refresh, indexes, core-lite discovery, production-candidate review packet, and master-record export hardening.
3. Discovery may observe, classify, and propose. It may not install.
4. Packets are evidence, not installation authority.
5. Production means accredited participation, not sovereign authority.

## Done

This bundle is done when the repo contains:

```text
THEOREM_PROOF_MAP.md
docs/TASK_ID_INDEX.md
docs/ARTIFACT_INDEX.md
tools/discover_core_lite_state.py
tools/build_production_candidate_review_packet.py
tools/export_master_record_candidate.py
tools/tasks/post_stage31_integration_tasks.json
```

Optional workflow path:

```text
.github/workflows/post-stage31-integration.yml
```

Displayed without leading dot:

```text
github/workflows/post-stage31-integration.yml
```

## Task IDs

```text
discover_core_lite_state
build_production_candidate_review_packet
export_master_record_candidate
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id discover_core_lite_state
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id build_production_candidate_review_packet
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id export_master_record_candidate
```

## Core-Lite Discovery

To scan a separate checkout:

```bash
CORE_LITE_ROOT=/path/to/core-lite python tools/discover_core_lite_state.py
```

## Boundary

```text
Discovery observes. Discovery does not install.
Install plans are candidates, not authority.
Packets are evidence, not installation authority.
Production means accredited participation, not sovereign authority.
```
