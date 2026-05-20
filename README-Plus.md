# Stage 6 Existing Workflow Task Bundle

## Assumptions

1. No new workflow file is added.
2. The existing Data Continuation Tests workflow remains the execution surface.
3. Stage 6 tests are already installed at `tests/test_stage6_unified_gate.py`.
4. Stage 6 candidates are already installed at `tests/fixtures/stage6_candidates.json`.

## Done Definition

This bundle is done when:

1. `tools/tasks/formalism_tests_tasks.json` includes `stage6_unified_gate_tests`.
2. The existing workflow can run only Stage 6 by using `workflow_dispatch` with `task_id=stage6_unified_gate_tests`.
3. The existing workflow can run all enabled tasks, including Stage 6, when `task_id` is blank.
4. No new workflow file is added.

## Files Included

| Path | Purpose |
|---|---|
| `tools/tasks/formalism_tests_tasks.json` | Full replacement declared-task manifest with Stage 6 added. |
| `bundle_manifest.json` | Bundle manifest. |
| `README.md` | This file. |

## How to Run Stage 6 Through the Existing Workflow

Open GitHub Actions for `formalism-tests`.

Select:

```text
Data Continuation Tests
```

Click:

```text
Run workflow
```

Use these inputs:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = stage6_unified_gate_tests
```

The workflow will execute:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id stage6_unified_gate_tests
```

That declared task runs:

```bash
python -m pytest tests/test_stage6_unified_gate.py
```

Expected result:

```text
94 passed
```

## Run All Declared Tasks

Leave `task_id` blank to run all enabled declared tasks.

That will run:

```text
archive_runtime_artifacts
continuation_gate
compound_continuation_gate
transition_table_gate
boundary_transition_gate
stage6_unified_gate_tests
```

## Boundary Rule

Do not add a workflow for Stage 6.

The existing workflow is the execution surface. The declared-task manifest is the extension point.
