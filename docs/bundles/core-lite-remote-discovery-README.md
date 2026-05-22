# Core-Lite Remote Discovery Task Bundle

## Assumptions

1. The discovery task is being run from `Data-Continuation/formalism-tests`.
2. The target core-lite repo is `Data-Continuation/core-lite` unless overridden.
3. Discovery must not install, mutate, or push to the target repo.
4. The existing local discovery script is `tools/discover_core_lite_state.py`.
5. This bundle adds a wrapper task that clones core-lite into a temporary workspace and runs discovery against that checkout.

## Done

This bundle is done when the repo contains:

```text
tools/discover_core_lite_remote_state.py
tools/tasks/core_lite_remote_discovery_tasks.json
docs/bundles/core-lite-remote-discovery-README.md
reports/core_lite_remote_discovery_bundle_report.json
receipts/core_lite_remote_discovery_bundle_receipts.jsonl
```

and the task emits:

```text
reports/core_lite_remote_discovery_report.json
reports/core_lite_discovery_report.json
reports/core_lite_discovered_state.json
reports/core_lite_discovery_gap_report.md
reports/core_lite_state_diff.json
reports/core_lite_install_plan_candidate.json
receipts/core_lite_remote_discovery_receipts.jsonl
receipts/core_lite_discovery_receipts.jsonl
```

## Task ID

```text
discover_core_lite_remote_state
```

## Run

Default target:

```bash
python tools/run_declared_tasks.py tools/tasks/core_lite_remote_discovery_tasks.json --task-id discover_core_lite_remote_state
```

Override target repo:

```bash
CORE_LITE_REPO=Data-Continuation/core-lite CORE_LITE_BRANCH=main python tools/run_declared_tasks.py tools/tasks/core_lite_remote_discovery_tasks.json --task-id discover_core_lite_remote_state
```

Private repo token override:

```bash
CORE_LITE_TOKEN=<token> CORE_LITE_REPO=Data-Continuation/core-lite CORE_LITE_BRANCH=main python tools/run_declared_tasks.py tools/tasks/core_lite_remote_discovery_tasks.json --task-id discover_core_lite_remote_state
```

## Boundary

```text
Discovery observes.
Discovery does not install.
Discovery does not push to core-lite.
Install plans are candidates, not authority.
```

## Next Step After Discovery

After the task passes, review:

```text
reports/core_lite_discovery_gap_report.md
reports/core_lite_state_diff.json
reports/core_lite_install_plan_candidate.json
```

Then run:

```bash
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id build_production_candidate_review_packet
```
