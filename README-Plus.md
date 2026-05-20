# Site Mirror Integrity Test Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. The test validates Site mirror fixture snapshots.
3. The test does not fetch the live Site.
4. The existing `Data Continuation Tests` workflow remains the execution surface.
5. No workflow files are added or changed.

## Done Definition

This bundle is done when:

1. `tools/run_site_mirror_integrity_tests.py` exists.
2. `tools/tasks/formalism_tests_tasks.json` includes `site_mirror_integrity_tests`.
3. Fixture snapshots exist under `tests/fixtures/site_mirror/`.
4. The runner validates:
   - Stage 6 verified status
   - Stage 6 public result mirrors proof-surface result
   - Representation Non-Consequence is covered, not partially covered
   - transition discovery contains the required elements
   - element detail pages are declared
   - transition classes include required decisions
   - public pages use one status source
   - mobile table contract markers are present
   - duplicate transition receipt file is noncanonical
5. The runner emits `reports/site_mirror_integrity_report.json`.
6. No workflow files are included.

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
task_id       = site_mirror_integrity_tests
```

The existing workflow runs:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id site_mirror_integrity_tests
```

The declared task runs:

```bash
python tools/run_site_mirror_integrity_tests.py
```

Expected output:

```text
reports/site_mirror_integrity_report.json
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
