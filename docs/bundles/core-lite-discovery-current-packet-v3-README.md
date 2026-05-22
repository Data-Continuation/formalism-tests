# Core-Lite Discovery Current Packet v3

## Assumptions

1. The previous routing task failed because it was run in a fresh workflow checkout where prior discovery reports were not present.
2. GitHub Actions artifacts from earlier runs are not automatically available to later workflow runs.
3. Routing must happen in the same run that creates the discovery outputs.
4. The correct fix is a single declared task that runs discovery and then routes the resulting current artifacts immediately.
5. This task does not install, mutate, or push to core-lite.

## Done

This bundle is done when the repo contains:

```text
tools/discover_and_route_core_lite_current.py
tools/tasks/core_lite_discovery_current_packet_tasks.json
docs/bundles/core-lite-discovery-current-packet-v3-README.md
```

and the task emits:

```text
dist/current/core-lite-discovery/CORE_LITE_DISCOVERY_ARTIFACT_INDEX.md
dist/current/core-lite-discovery/core_lite_discovery_gap_report.md
dist/current/core-lite-discovery/core_lite_state_diff.json
dist/current/core-lite-discovery/core_lite_install_plan_candidate.json
dist/current/core-lite-discovery-artifacts.zip
reports/core_lite_discovery_current_packet_report.json
receipts/core_lite_discovery_current_packet_receipts.jsonl
```

## Task ID

```text
discover_and_route_core_lite_current
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/core_lite_discovery_current_packet_tasks.json --task-id discover_and_route_core_lite_current
```

## Why v2 Failed

v2 correctly separated required and optional artifacts.

But it still assumed the discovery reports already existed in the same checkout.

In GitHub Actions, each run starts from the repository state. Outputs from a previous workflow run are not automatically present unless they were committed to the repo or explicitly downloaded from an artifact.

Therefore the proper action task is:

```text
discover core-lite
then route current artifacts
in the same declared task
in the same workflow run
```

## Review These First

After the task passes, review:

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
dist/current/ is for action.
Historical artifacts are for audit.
```
