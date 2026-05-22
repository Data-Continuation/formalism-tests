# Core-Lite Discovery Artifact Routing Fix

## Assumptions

1. Core-lite remote discovery already ran successfully.
2. The discovery outputs exist under `reports/` and `receipts/`.
3. The current artifact UX is poor because the owner should not need to search through many historical artifact folders.
4. The fix should collect current discovery outputs into one folder and one zip.
5. This task does not rerun discovery, install core-lite, or mutate core-lite.

## Done

This bundle is done when the repo contains:

```text
tools/route_core_lite_discovery_artifacts.py
tools/tasks/core_lite_discovery_artifact_routing_tasks.json
docs/bundles/core-lite-discovery-artifact-routing-README.md
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

## What to Review After Running

Open:

```text
dist/current/core-lite-discovery/CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md
dist/current/core-lite-discovery/core_lite_discovery_gap_report.md
dist/current/core-lite-discovery/core_lite_state_diff.json
dist/current/core-lite-discovery/core_lite_install_plan_candidate.json
```

or download:

```text
dist/current/core-lite-discovery-artifacts.zip
```

## Boundary

```text
Discovery observes.
Discovery does not install.
Artifact routing collects evidence.
Artifact routing does not grant authority.
```
