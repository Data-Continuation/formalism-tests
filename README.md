# Theorem Map Consistency Test Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. The root `THEOREM_PROOF_MAP.md` should be the updated current theorem map.
3. `reports/current/THEOREM_PROOF_MAP.md` should match the root theorem map.
4. Representation Non-Consequence is now covered.
5. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `THEOREM_PROOF_MAP.md` is replaced with the updated current map.
2. `tools/run_theorem_map_consistency_tests.py` exists.
3. `tests/fixtures/theorem_map_consistency_policy.json` exists.
4. `tools/tasks/formalism_tests_tasks.json` includes `theorem_map_consistency_tests`.
5. The runner validates:
   - root theorem map has all required theorem rows
   - root theorem map marks all required theorems as Covered
   - root theorem map does not contain stale partial Representation Non-Consequence language
   - `reports/current/THEOREM_PROOF_MAP.md` is synchronized with root
   - latest proof reports agree with theorem-map status
6. The runner emits `reports/theorem_map_consistency_report.json`.
7. No workflow files are included.

## Run Through Existing Workflow

Use:

```text
Actions
→ Data Continuation Tests
→ Run workflow
```

Inputs:

```text
task_manifest = tools/tasks/formalism_tests_tasks.json
task_id       = theorem_map_consistency_tests
```

Expected output:

```text
reports/theorem_map_consistency_report.json
```

## Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
