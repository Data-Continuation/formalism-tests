# Core-Lite Discovery Artifact Routing Fix v2

## Assumptions

1. Core-lite remote discovery already ran successfully.
2. The next decision requires only three required current review files.
3. Optional context files should not fail the routing task if missing.
4. Historical artifacts are for audit.
5. `dist/current/` is for action.

## Done

This bundle is done when the repo contains:

```text
tools/route_core_lite_discovery_artifacts.py
tools/tasks/core_lite_discovery_artifact_routing_tasks.json
docs/bundles/core-lite-discovery-artifact-routing-v2-README.md
```

and the task emits:

```text
dist/current/core-lite-discovery/CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md
dist/current/core-lite-discovery/core_lite_discovery_gap_report.md
dist/current/core-lite-discovery/core_lite_state_diff.json
dist/current/core-lite-discovery/core_lite_install_plan_candidate.json
dist/current/core-lite-discovery-artifacts.zip
reports/core_lite_discovery_artifact_routing_report.json
receipts/core_lite_discovery_artifact_routing_receipts.jsonl
```

## Task ID

```text
route_core_lite_discovery_artifacts
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/core_lite_discovery_artifact_routing_tasks.json --task-id route_core_lite_discovery_artifacts
```

## What Changed From v1

v1 failed if optional context artifacts were missing.

v2 only fails when one of the three required current decision files is missing:

```text
reports/core_lite_discovery_gap_report.md
reports/core_lite_state_diff.json
reports/core_lite_install_plan_candidate.json
```

Optional files are copied when present and listed as warnings when missing.

## Review These First

```text
dist/current/core-lite-discovery/CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md
dist/current/core-lite-discovery/core_lite_discovery_gap_report.md
dist/current/core-lite-discovery/core_lite_state_diff.json
dist/current/core-lite-discovery/core_lite_install_plan_candidate.json
```

## Boundary

```text
Discovery observes.
Discovery does not install.
Artifact routing collects evidence.
Artifact routing does not grant authority.
Historical artifacts are for audit.
dist/current/ is for action.
```
