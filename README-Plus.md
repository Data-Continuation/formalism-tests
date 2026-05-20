# Current Report Preservation Test Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. Runtime artifact archival may continue.
3. Current public proof reports need stable paths under `reports/current/`.
4. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `tools/run_current_report_preservation_tests.py` exists.
2. `tests/fixtures/current_report_preservation_policy.json` exists.
3. `tools/tasks/formalism_tests_tasks.json` includes `current_report_preservation_tests`.
4. The runner copies approved current proof outputs into `reports/current/`.
5. The runner emits `reports/current_report_preservation_report.json`.
6. `THEOREM_PROOF_MAP.md` marks Representation Non-Consequence as covered.
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
task_id       = current_report_preservation_tests
```

Expected output:

```text
reports/current_report_preservation_report.json
```

Expected current reports:

```text
reports/current/continuation_report.md
reports/current/compound_continuation_report.md
reports/current/representation_non_consequence_report.json
reports/current/representation_non_consequence_report.md
reports/current/transition_table_public_surface_report.json
reports/current/site_mirror_integrity_report.json
reports/current/THEOREM_PROOF_MAP.md
```

## Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
