# StegVerse-001 CLI Dependency Contractual Inclusion Candidate Builder

Generated: 2026-05-23T07:31:45.097617+00:00

## Assumptions

1. Install target is `Data-Continuation/formalism-tests`.
2. `formalism-tests` remains the command backdrop.
3. `Data-Continuation/core-lite` remains the remote target.
4. Active blocker is `SV001-M3 Existing Intake gate`.
5. This task prepares candidates only.
6. This task does not mutate `core-lite`.
7. This task does not add workflows.
8. This task does not submit bundles to `incoming/`.

## Done

This bundle is done when `formalism-tests` contains:

```text
tools/stegverse001_prepare_cli_dependency_contract_candidate.py
tools/tasks/stegverse001_cli_dependency_contract_tasks.json
docs/bundles/stegverse-001-cli-dependency-contract-candidate-README.md
```

and the task emits:

```text
reports/current/stegverse-001-cli-dependency-contract/candidate_report.json
reports/current/stegverse-001-cli-dependency-contract/candidate_report.md
dist/current/stegverse-001-cli-dependency-contract/candidate_manifest.json
dist/current/stegverse-001-cli-dependency-contract/core_lite/ingest.py
dist/current/stegverse-001-cli-dependency-contract/core_lite/receipts.py
dist/current/stegverse-001-cli-dependency-contract/cli_dependency_contractual_inclusion.patch
receipts/current/stegverse-001-cli-dependency-contract/receipts.jsonl
```

## Task ID

```text
stegverse001_prepare_cli_dependency_contract_candidate
```

## Run From formalism-tests

```bash
python tools/run_declared_tasks.py tools/tasks/stegverse001_cli_dependency_contract_tasks.json --task-id stegverse001_prepare_cli_dependency_contract_candidate
```

## Operating Rule

```text
Transition Table in.
One transition out.
Receipt.
Stop.
```
