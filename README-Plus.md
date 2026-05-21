# Representation Non-Consequence Test Bundle

## Assumptions

1. This bundle belongs in `formalism-tests`.
2. The existing `Data Continuation Tests` workflow remains the execution surface.
3. No new workflow files are added.
4. This closes the direct proof gap for Representation Non-Consequence.

## Done Definition

This bundle is done when:

1. `tests/fixtures/representation_non_consequence_cases.json` exists.
2. `tools/run_representation_non_consequence_tests.py` exists.
3. `tools/tasks/formalism_tests_tasks.json` includes `representation_non_consequence_tests`.
4. The runner emits:
   - `reports/representation_non_consequence_report.json`
   - `reports/representation_non_consequence_report.md`
   - `reports/representation_non_consequence_receipts.jsonl`
5. `THEOREM_PROOF_MAP.md` marks Representation Non-Consequence as covered.
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
task_id       = representation_non_consequence_tests
```

The existing workflow runs:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id representation_non_consequence_tests
```

The declared task runs:

```bash
python tools/run_representation_non_consequence_tests.py
```

## Expected Outputs

```text
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
reports/representation_non_consequence_receipts.jsonl
```

## Theorem Claim

```text
Representation alone has no consequence-bearing status until it is bound to a transition role and continuation path.
```

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
```
