# StegVerse-001 Remote Core-Lite Working Contract Report

## Status

```text
actor: StegVerse-001
mode: initialization
active_transition: Core-Lite Recorded Ingestion + CGE + Sandbox Result Return
decision: PLAN_RETURNED
blocker_count: 1
```

## Role Separation

```text
formalism-tests = proof and command backdrop
core-lite = remote target
StegVerse-001 = initialization-state remote operator
```

## Observed CGE Import Contract

- `cli` imports `generate_cge_fingerprint` from `cge`
- `cli` imports `generate_cge_fingerprint` from `cge`
- `ingest` imports `classify_sandbox_result, precheck_manifest` from `core_lite.cge`

## Missing CGE Exports

- `generate_cge_fingerprint` required by `cli`
- `generate_cge_fingerprint` required by `cli`

## Transition Requirements

```text
incoming_bundle_detected: True
manifest_validation_surface: True
cge_surface: True
sandbox_surface: True
receipt_surface: True
workflow_execution_surface: True
```

## Next Admissible Change

```json
{
  "basis": "Observed import contract requires these exports before existing intake/self-test surfaces can run.",
  "classification": "contractual_inclusion",
  "preserve_existing_exports": true,
  "required_exports": [
    "generate_cge_fingerprint"
  ],
  "target": "core_lite/cge.py"
}
```

## Boundary

```text
No target mutation.
No push.
No workflow widening.
No incoming bundle submission.
No production.
Runtime clone remains outside repo working tree by default.
Return plan and receipt.
STOP.
```
