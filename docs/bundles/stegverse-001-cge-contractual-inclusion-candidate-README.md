# StegVerse-001 CGE Contractual Inclusion Candidate Builder

Generated: 2026-05-23T06:05:21.511873+00:00

## Assumptions

1. Install target is `Data-Continuation/formalism-tests`.
2. `formalism-tests` remains the command backdrop.
3. `Data-Continuation/core-lite` remains the remote target.
4. Active gate is `Core-Lite CGE Contractual Inclusion Candidate`.
5. This task prepares a candidate only.
6. This task does not mutate `core-lite`.
7. This task does not add workflows.
8. This task does not submit bundles to `incoming/`.

## Done

This bundle is done when `formalism-tests` contains:

```text
tools/stegverse001_prepare_cge_contractual_inclusion_candidate.py
tools/tasks/stegverse001_cge_contractual_inclusion_tasks.json
docs/bundles/stegverse-001-cge-contractual-inclusion-candidate-README.md
```

and the task emits:

```text
reports/current/stegverse-001-cge-contractual-inclusion/candidate_report.json
reports/current/stegverse-001-cge-contractual-inclusion/candidate_report.md
dist/current/stegverse-001-cge-contractual-inclusion/candidate_manifest.json
dist/current/stegverse-001-cge-contractual-inclusion/core_lite/cge.py
dist/current/stegverse-001-cge-contractual-inclusion/core_lite_cge_contractual_inclusion.patch
receipts/current/stegverse-001-cge-contractual-inclusion/receipts.jsonl
```

## Task ID

```text
stegverse001_prepare_cge_contractual_inclusion_candidate
```

## Run From formalism-tests

```bash
python tools/run_declared_tasks.py tools/tasks/stegverse001_cge_contractual_inclusion_tasks.json --task-id stegverse001_prepare_cge_contractual_inclusion_candidate
```

## What It Does

```text
clones core-lite into runtime temp space
reads core_lite/cge.py
confirms existing CGE surfaces are present
adds generate_cge_fingerprint if missing
writes candidate replacement file under dist/current/
writes patch under dist/current/
writes report and receipt
stops
```

## What It Does Not Do

```text
does not patch core-lite
does not push to core-lite
does not submit to incoming/
does not change workflows
does not run Core-Lite Intake
does not grant production, node, or FinCo authority
```

## Operating Rule

```text
Transition Table in.
One transition out.
Receipt.
Stop.
```
