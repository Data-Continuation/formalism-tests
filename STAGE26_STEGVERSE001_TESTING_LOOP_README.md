# Stage 26 — StegVerse-001 Declared Testing Loop

## Assumptions

1. Stages 17 through 25 have already been uploaded and their task IDs are present in `tools/tasks/formalism_tests_tasks.json`.
2. `StegVerse-001 / Beta_Orionis` is active, Transition-Table-bound, and governed by declared policy.
3. Stage 26 tests whether StegVerse-001 handles testing by using the declared-task runner, not by running stage scripts directly.

## Done

Stage 26 is done when:

```text
tools/run_stage26_stegverse001_testing_loop_tests.py
```

returns success and emits:

```text
reports/stage26_stegverse001_testing_loop_report.json
reports/stage26_stegverse001_testing_loop_receipts.jsonl
```

## Task ID

```text
stage26_stegverse001_testing_loop_tests
```

## How to run without editing the main manifest

Use the included Stage 26-only manifest:

```bash
python tools/run_declared_tasks.py tools/tasks/stage26_stegverse001_testing_loop_tasks.json --task-id stage26_stegverse001_testing_loop_tests
```

This lets Stage 26 call the main manifest as a child manifest:

```text
tools/tasks/formalism_tests_tasks.json
```

## What Stage 26 actually tests

Stage 26 invokes each of these child task IDs through `tools/run_declared_tasks.py`:

```text
stage17_self_audit_tests
stage18_sandbox_candidate_generation_tests
stage19_candidate_review_loop_tests
stage20_release_candidate_assembly_tests
stage21_canonical_upgrade_replay_tests
stage22_public_mirror_propagation_tests
stage23_ingestible_bundle_tests
stage24_test_plan_tests
stage25_entity_charter_tests
```

## Expected decision surface

```text
ALLOW_TEST_LOOP
FAIL_CLOSED
LEDGER_TEST_LOOP
```

## Main-manifest integration option

After this passes, add this task entry to `tools/tasks/formalism_tests_tasks.json`:

```json
{
  "task_id": "stage26_stegverse001_testing_loop_tests",
  "description": "Stage 26 - validate StegVerse-001 handling Stage 17 through Stage 25 tests via declared-task routing.",
  "enabled": true,
  "command": [
    "python",
    "tools/run_stage26_stegverse001_testing_loop_tests.py"
  ],
  "expected_outputs": [
    "reports/stage26_stegverse001_testing_loop_report.json",
    "reports/stage26_stegverse001_testing_loop_receipts.jsonl"
  ]
}
```

## Next logical stage

```text
Stage 27 — Cross-Entity Governance Readiness
```
