# Transition Table Public Surface Test Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. The existing `Data Continuation Tests` workflow remains the execution surface.
3. No new workflow files are added.
4. The Transition Table should now be validated as a complete public proof surface, not only as math fixtures.
5. Site-facing data is represented here as fixture snapshots under `tests/fixtures/site/`.

## Done Definition

This bundle is done when:

1. `tools/run_transition_table_public_surface_tests.py` exists.
2. `tools/tasks/formalism_tests_tasks.json` includes `transition_table_public_surface_tests`.
3. The runner validates:
   - single-source status data
   - Stage 6 verified status
   - Stage 6 declared-task result
   - discovery map coverage
   - unlocked Level 5 elements
   - transition class coverage
   - RESET_BOUNDARY / EVOLVE_BOUNDARY presence
   - public page contract
   - mobile presentation contract markers
4. The runner emits `reports/transition_table_public_surface_report.json`.
5. No workflow files are included.

## Files Included

| Path | Purpose |
|---|---|
| `tools/run_transition_table_public_surface_tests.py` | Standard-library public-surface validator. |
| `tools/tasks/formalism_tests_tasks.json` | Full replacement declared-task manifest with new task. |
| `tests/fixtures/site/transition-proof-surface.json` | Single-source Site status fixture. |
| `tests/fixtures/site/transition-discovery-map.json` | Transition discovery and element-page fixture. |
| `tests/fixtures/site/transition-table-classes.json` | Transition class fixture. |
| `tests/fixtures/site/site-public-surface-contract.json` | Public page and mobile contract fixture. |
| `README.md` | Bundle explanation. |
| `bundle_manifest.json` | Bundle manifest. |

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
task_id       = transition_table_public_surface_tests
```

The existing workflow runs:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id transition_table_public_surface_tests
```

The declared task runs:

```bash
python tools/run_transition_table_public_surface_tests.py
```

Expected output:

```text
reports/transition_table_public_surface_report.json
```

## What This Validates

```text
Stage 6 status is verified.
Stage 6 result contains 10 candidates and 320 assertions.
At least 12 elements are unlocked at Level 5.
Every mapped element has detail-page metadata.
Transition classes include RESET_BOUNDARY and EVOLVE_BOUNDARY.
The public table has a mobile presentation contract.
One shared status source controls all transition status pages.
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
