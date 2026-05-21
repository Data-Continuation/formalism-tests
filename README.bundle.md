# Stage 9 Reconciliation Fix 1 Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. The previous failure happened because the runner expected the exact string `Stage 7 - Element Dependency Closure`.
3. The README may contain equivalent wording such as `Stage 7 Element Dependency Closure`.
4. No workflow files are added or changed.

## Done Definition

1. `tools/run_stage9_reconciliation_tests.py` validates grouped semantic markers.
2. `tests/fixtures/stage9_reconciliation_policy.json` uses marker groups.
3. `stage9_reconciliation_tests` can run without failing on harmless README punctuation differences.
4. The task remains `stage9_reconciliation_tests`.

## Run

```text
Actions
-> Data Continuation Tests
-> Run workflow
```

Inputs:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = stage9_reconciliation_tests
```
