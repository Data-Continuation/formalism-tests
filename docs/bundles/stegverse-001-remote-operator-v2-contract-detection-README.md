# StegVerse-001 Remote Operator v2 Contract Detection

## Assumptions

1. Target install repo is `Data-Continuation/formalism-tests`.
2. `formalism-tests` is the transition-proof and command backdrop.
3. `core-lite` is the remote target.
4. The previous operator missed local import style: `from cge import generate_cge_fingerprint`.
5. Runtime clone output must not be committed under `.tmp/`.
6. This bundle does not patch `core-lite`.

## Done

This bundle is done when `formalism-tests` contains:

```text
tools/stegverse001_remote_core_lite_operator.py
tools/cleanup_stegverse001_runtime_artifacts.py
tools/tasks/stegverse001_remote_core_lite_tasks.json
docs/bundles/stegverse-001-remote-operator-v2-contract-detection-README.md
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

## What Changed

v2 detects all of these as CGE contract imports:

```text
from core_lite.cge import X
from cge import X
from .cge import X
```

It also clones `core-lite` into system temp space by default instead of:

```text
.tmp/stegverse-001-remote-core-lite/
```

Displayed without leading dot:

```text
tmp/stegverse-001-remote-core-lite/
```

Note: the actual previously committed runtime path began with `.tmp/`.

## Expected Corrected Finding

Given the latest evidence, the corrected plan should identify:

```text
classification: contractual_inclusion
target: core_lite/cge.py
required_exports:
  - generate_cge_fingerprint
```

## Cleanup

If `.tmp/stegverse-001-remote-core-lite/` is committed in `formalism-tests`, remove it from the repo tree. This bundle also includes:

```text
tools/cleanup_stegverse001_runtime_artifacts.py
```

That cleanup tool removes the runtime directory from the working tree when executed in a runner, but GitHub repo cleanup may still require deleting committed files through the UI or a commit.

## Boundary

```text
No target mutation.
No push to core-lite.
No workflow widening.
No incoming bundle submission.
Return corrected plan and receipt.
STOP.
```
