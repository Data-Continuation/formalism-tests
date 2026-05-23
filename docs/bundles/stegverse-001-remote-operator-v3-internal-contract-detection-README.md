# StegVerse-001 Remote Operator v3 Internal Contract Detection

Generated: 2026-05-23T07:14:53.703979+00:00

## Assumptions

1. Install target is `Data-Continuation/formalism-tests`.
2. `formalism-tests` remains the proof and command backdrop.
3. `Data-Continuation/core-lite` remains the remote target.
4. The active blocker is package-internal import/export contract detection.
5. This bundle does not mutate `core-lite`.
6. This bundle does not add workflows.
7. This bundle does not submit bundles to `incoming/`.

## Done

This bundle is done when `formalism-tests` contains:

```text
tools/stegverse001_remote_core_lite_operator.py
tools/tasks/stegverse001_remote_core_lite_tasks.json
docs/bundles/stegverse-001-remote-operator-v3-internal-contract-detection-README.md
```

and the remote operator emits:

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

## What Changed in v3

v3 detects all internal `core_lite` import/export mismatches, not only CGE.

It resolves:

```text
from .ingest import X
from ingest import X
from core_lite.ingest import X
from .cge import X
from cge import X
from core_lite.cge import X
```

## Expected Finding From Current Failure

```text
classification: internal_contractual_inclusion
target: core_lite/ingest.py
required_exports:
  - ingest_incoming
  - load_core_policy
required_by:
  - core_lite.cli
```

## Boundary

```text
No target mutation.
No push to core-lite.
No workflow widening.
No incoming bundle submission.
No production.
Return corrected plan and receipt.
STOP.
```
