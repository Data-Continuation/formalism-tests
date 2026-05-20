# Stage 6 Existing Workflow Task Bundle — Fix 2

## Assumptions

1. No workflow file should be added or changed.
2. The existing `Data Continuation Tests` workflow is the execution surface.
3. The workflow environment does not install `pytest`.
4. Stage 6 must therefore run through a standard-library declared-task runner.
5. Stage 6 candidates are already installed at `tests/fixtures/stage6_candidates.json`.

## Done Definition

This fix is done when:

1. `tools/run_stage6_unified_gate_tests.py` exists.
2. `tools/tasks/formalism_tests_tasks.json` points `stage6_unified_gate_tests` to the standard-library runner.
3. The existing workflow can run only Stage 6 using `task_id=stage6_unified_gate_tests`.
4. No workflow file is added or changed.

## What Failed

The existing workflow reached the Stage 6 task, but failed because the runner attempted:

```bash
python -m pytest tests/test_stage6_unified_gate.py
```

The GitHub-hosted Python environment reported:

```text
No module named pytest
```

## What Changed

This bundle adds:

```text
tools/run_stage6_unified_gate_tests.py
```

and changes the Stage 6 declared task to run:

```bash
python tools/run_stage6_unified_gate_tests.py
```

The runner uses only Python standard library modules.

## Files Included

| Path | Purpose |
|---|---|
| `tools/run_stage6_unified_gate_tests.py` | Standard-library Stage 6 test runner. |
| `tools/tasks/formalism_tests_tasks.json` | Full replacement manifest pointing Stage 6 to the runner. |
| `README.md` | This explanation and verification checklist. |
| `bundle_manifest.json` | Bundle manifest. |

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

The workflow runs:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id stage6_unified_gate_tests
```

The declared task runs:

```bash
python tools/run_stage6_unified_gate_tests.py
```

Expected result:

```json
{
  "success": true,
  "candidate_count": 10
}
```

## Boundary Rule

Do not add a workflow for Stage 6.

The existing workflow is the execution surface. The declared-task manifest is the extension point.
