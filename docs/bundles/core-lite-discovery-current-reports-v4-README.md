# Core-Lite Discovery Current Reports v4

## Assumptions

1. The stable dispatcher should remain unchanged.
2. The dispatcher already persists `reports/` and `receipts/`.
3. Current action artifacts should therefore be written to `reports/current_*`.
4. `dist/current/` may still be produced as an optional packet/cache surface, but task success should not depend on workflow changes.
5. This task does not install, mutate, or push to core-lite.

## Done

This bundle is done when the repo contains:

```text
tools/discover_core_lite_current_reports.py
tools/tasks/core_lite_discovery_current_reports_tasks.json
docs/bundles/core-lite-discovery-current-reports-v4-README.md
```

and the task emits:

```text
reports/current_core_lite_discovery_artifact_index.md
reports/current_core_lite_discovery_gap_report.md
reports/current_core_lite_state_diff.json
reports/current_core_lite_install_plan_candidate.json
reports/current_core_lite_discovery_packet_manifest.json
reports/current_core_lite_discovery_packet_report.json
receipts/current_core_lite_discovery_receipts.jsonl
```

## Task ID

```text
discover_core_lite_current_reports
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/core_lite_discovery_current_reports_tasks.json --task-id discover_core_lite_current_reports
```

## Review These First

```text
reports/current_core_lite_discovery_artifact_index.md
reports/current_core_lite_discovery_gap_report.md
reports/current_core_lite_state_diff.json
reports/current_core_lite_install_plan_candidate.json
```

## Rule

```text
reports/current_* is for action.
dist/current/ is optional packet/cache surface.
Historical artifacts are for audit.
```

## Boundary

```text
Discovery observes.
Discovery does not install.
Artifact routing collects evidence.
Artifact routing does not grant authority.
Stable dispatcher stays stable.
```
