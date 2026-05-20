# Stage 6 Existing Workflow Task Bundle — Fix 1

## Assumptions

1. No workflow file should be added or changed.
2. The existing `Data Continuation Tests` workflow is the execution surface.
3. The failure shown in GitHub Actions is caused by the declared-task runner requiring `expected_outputs` to be a list.
4. Stage 6 tests are already installed at `tests/test_stage6_unified_gate.py`.
5. Stage 6 candidates are already installed at `tests/fixtures/stage6_candidates.json`.

## Done Definition

This fix is done when:

1. `tools/tasks/formalism_tests_tasks.json` parses as JSON.
2. Every task uses `expected_outputs` as a list.
3. The existing workflow can run only Stage 6 using `task_id=stage6_unified_gate_tests`.
4. No new workflow file is added.

## What Changed

The previous Stage 6 task used:

```json
"expected_outputs": {}
```

The current declared-task runner rejected that with:

```text
task stage6_unified_gate_tests expected_outputs must be a list
```

This replacement manifest changes it to:

```json
"expected_outputs": []
```

For consistency, all declared tasks in this replacement manifest now use list-form `expected_outputs`.

## Files Included

| Path | Purpose |
|---|---|
| `tools/tasks/formalism_tests_tasks.json` | Full replacement declared-task manifest with list-form `expected_outputs`. |
| `bundle_manifest.json` | Bundle manifest. |
| `README.md` | This explanation and verification checklist. |

## Run Stage 6 Through the Existing Workflow

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

Expected command inside the workflow:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id stage6_unified_gate_tests
```

The declared task then runs:

```bash
python -m pytest tests/test_stage6_unified_gate.py
```

Expected test result:

```text
94 passed
```

## Boundary Rule

Do not add a workflow for Stage 6.

The existing workflow is the execution surface. The declared-task manifest is the extension point.
