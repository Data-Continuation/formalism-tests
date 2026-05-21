# Stage 11 Active Manifest Fix Bundle

## Assumptions

1. Stage 11 files were uploaded, but the active manifest was not updated.
2. The additive manifest run failed because the task_id field was set incorrectly.
3. This bundle updates the active manifest so the existing workflow can run Stage 11 normally.
4. No workflow files are included.

## Done Definition

1. tools/tasks/formalism_tests_tasks.json includes stage11_candidate_expansion_governance_tests.
2. The Stage 11 runner and fixture are present.
3. Local validation passes.

## Correct Workflow Inputs After Upload

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = stage11_candidate_expansion_governance_tests
```
