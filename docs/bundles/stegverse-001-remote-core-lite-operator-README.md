# StegVerse-001 Remote Core-Lite Operator

## Assumptions

1. `formalism-tests` is the transition-proof and command-orchestration backdrop.
2. `core-lite` is the remote target.
3. StegVerse-001 should operate from `formalism-tests` before `core-lite` has its own generic worker surface.
4. The active transition is only:

```text
Core-Lite Recorded Ingestion + CGE + Sandbox Result Return
```

5. This task determines the working structure and plan only.
6. This task does not patch, push, submit incoming bundles, add workflows, or mutate `core-lite`.

## Done

This bundle is done when `formalism-tests` contains:

```text
tools/stegverse001_remote_core_lite_operator.py
tools/tasks/stegverse001_remote_core_lite_tasks.json
docs/bundles/stegverse-001-remote-core-lite-operator-README.md
```

and the task emits:

```text
reports/current/stegverse-001-remote-core-lite/working_contract_report.json
reports/current/stegverse-001-remote-core-lite/working_contract_report.md
reports/current/stegverse-001-remote-core-lite/remediation_plan.json
receipts/current/stegverse-001-remote-core-lite/receipts.jsonl
```

## Task ID

```text
stegverse001_determine_core_lite_remote_contract
```

## Run From formalism-tests

```bash
python tools/run_declared_tasks.py tools/tasks/stegverse001_remote_core_lite_tasks.json --task-id stegverse001_determine_core_lite_remote_contract
```

## Optional Environment Overrides

```bash
CORE_LITE_REPO=Data-Continuation/core-lite
CORE_LITE_BRANCH=main
CORE_LITE_TOKEN=<token-if-needed>
```

## What StegVerse-001 Does

```text
clones core-lite
inspects workflows
inspects task manifests
inspects core_lite/cli.py
inspects core_lite/cge.py
inspects core_lite/ingest.py
inspects core_lite/sandbox.py
inspects core_lite/receipts.py
detects observed import needs
detects missing contractual exports
detects transition surfaces
returns one plan
emits receipt
stops
```

## What StegVerse-001 Does Not Do

```text
does not patch core-lite
does not push to core-lite
does not submit to incoming/
does not add workflows
does not install
does not promote production
does not activate node status
does not activate FinCo
does not self-accredit
```

## Role Separation

```text
formalism-tests = proof and command backdrop
core-lite = remote target
StegVerse-001 = initialization-state remote operator
```

## Operating Rule

```text
Transition Table in.
One transition out.
Receipt.
Stop.
```
