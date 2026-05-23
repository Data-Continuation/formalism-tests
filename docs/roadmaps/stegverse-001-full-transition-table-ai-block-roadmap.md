# StegVerse-001 Full Transition Table AI Block Build Roadmap

Generated: 2026-05-23T05:44:52.682112+00:00

## Purpose

This roadmap defines the path from the current StegVerse-001 remote-operator proof into a full Transition Table AI Block build.

The goal is not to create a general-purpose autonomous agent.

The goal is to create a scoped AI block that acts only through the Transition Table:

```text
Transition Table in.
One transition out.
Receipt.
Stop.
```

StegVerse-001 becomes useful when it can:

```text
read the active transition
determine the current target contract
perform only the admissible next action
record the result
return the report
stop
```

## Current Proven Baseline

The current proven baseline is:

```text
formalism-tests = proof and command backdrop
core-lite = remote target
StegVerse-001 = initialization-state remote operator
```

The latest successful transition proved:

```text
StegVerse-001 can run from formalism-tests.
StegVerse-001 can clone core-lite remotely.
StegVerse-001 can inspect the target contract.
StegVerse-001 can detect a contractual inclusion blocker.
StegVerse-001 can return a report, plan, and receipt.
StegVerse-001 can stop without mutating the target.
```

The current blocker identified by StegVerse-001 is:

```text
target: core_lite/cge.py
required_exports:
  - generate_cge_fingerprint
classification: contractual_inclusion
```

## Active Build Objective

The active build objective is:

```text
Build StegVerse-001 into a full Transition Table AI Block.
```

This means StegVerse-001 should eventually support all transition-table phases needed for initialization-state repo work:

```text
discover
classify
plan
prepare candidate
submit through allowed path
observe result
record receipt
stop
```

It must not silently cross into:

```text
install
production
node status
FinCo eligibility
self-accreditation
workflow widening
unreviewed target mutation
```

## AI Block Definition

A StegVerse-001 AI Block is a scoped executable actor with:

```text
identity
instruction source
transition table reference
current transition
allowed action surface
target surface
evidence inputs
decision output
receipt output
stop condition
```

An AI Block is not trusted because it is AI.

It is trusted only to the extent that its action is transition-bound, evidence-backed, and receipted.

## Build Phases

### Phase 0 — Proven Transition Proof Baseline

Status:

```text
COMPLETE
```

Evidence:

```text
remote operator ran
core-lite cloned
contract inspected
blocker detected
plan returned
receipt emitted
target not mutated
```

Completion criteria:

```text
reports/current/stegverse-001-remote-core-lite/working_contract_report.json exists
reports/current/stegverse-001-remote-core-lite/remediation_plan.json exists
receipts/current/stegverse-001-remote-core-lite/receipts.jsonl exists
```

### Phase 1 — Contractual Inclusion Candidate

Status:

```text
READY
```

Objective:

```text
Prepare the minimum candidate that adds generate_cge_fingerprint to core_lite/cge.py while preserving:
- CGEDecision
- precheck_manifest
- classify_sandbox_result
```

Allowed action:

```text
prepare candidate only
no direct target mutation unless later authorized by the active transition
```

Stop condition:

```text
candidate returned with report and receipt
```

### Phase 2 — Remote Contract Recheck

Status:

```text
PENDING
```

Objective:

```text
After the contractual inclusion candidate is applied through the allowed path, rerun StegVerse-001 remote contract determination.
```

Expected result:

```text
blockers: []
next_admissible_change:
  classification: run_existing_intake
  target: existing Core-Lite Intake workflow
```

Stop condition:

```text
remote contract report returned
receipt emitted
```

### Phase 3 — Intake Gate

Status:

```text
PENDING
```

Objective:

```text
Run existing Core-Lite Intake only after the remote contract check returns no blockers.
```

Allowed transition:

```text
Core-Lite Intake
```

Expected result:

```text
incoming bundle detected or intake no-op clearly reported
CGE fingerprint generated
CGE precheck available
sandbox path available
report/receipt emitted
```

Stop condition:

```text
intake result returned
receipt emitted
```

### Phase 4 — Recorded Ingestion + CGE + Sandbox Loop

Status:

```text
PENDING
```

Objective:

```text
Submit or process a sandbox-only candidate bundle through the intake path.
```

Expected chain:

```text
bundle detected
manifest validated
CGE precheck
sandbox experiment
sandbox result
CGE result classification
report returned
receipt emitted
STOP
```

Stop condition:

```text
recorded loop completes without install
```

### Phase 5 — Transition Table Instruction Block

Status:

```text
PENDING
```

Objective:

```text
Create a stable instruction structure so StegVerse-001 can receive only one active transition at a time.
```

Required fields:

```text
actor
mode
transition_id
target_repo
allowed_actions
forbidden_actions
evidence_inputs
expected_outputs
stop_condition
```

Stop condition:

```text
instruction block parsed
one transition selected
receipt emitted
```

### Phase 6 — Transition Class Registry

Status:

```text
PENDING
```

Objective:

```text
Define a machine-readable registry of transition classes used by StegVerse-001.
```

Initial transition classes:

```text
REMOTE_CONTRACT_DISCOVERY
CONTRACTUAL_INCLUSION_CANDIDATE
REMOTE_CONTRACT_RECHECK
RUN_EXISTING_INTAKE
INGEST_CANDIDATE_BUNDLE
CGE_PRECHECK
SANDBOX_EXPERIMENT
CGE_RESULT_CLASSIFICATION
RETURN_REPORT_AND_RECEIPT
STOP
```

Stop condition:

```text
registry produced
tracker recognizes transition IDs
receipt emitted
```

### Phase 7 — Milestone Tracker

Status:

```text
STARTED
```

Objective:

```text
Track roadmap progress as structured data.
```

Required outputs:

```text
tracking/stegverse-001/roadmap_milestones.json
reports/current/stegverse-001-roadmap/milestone_status_report.md
reports/current/stegverse-001-roadmap/milestone_status_report.json
receipts/current/stegverse-001-roadmap/receipts.jsonl
```

Stop condition:

```text
milestone state returned
receipt emitted
```

### Phase 8 — Public Documentation Track

Status:

```text
STARTED
```

Objective:

```text
Maintain public-facing documentation showing how the transition table enables governed AI action.
```

Current public proof document:

```text
docs/public/stegverse-001-transition-table-remote-operator-case-study.md
```

Stop condition:

```text
public explanation available
roadmap linked
receipt emitted
```

### Phase 9 — Full AI Block Candidate

Status:

```text
PENDING
```

Objective:

```text
Package StegVerse-001 as a full Transition Table AI Block candidate.
```

Required surfaces:

```text
identity
instruction channel
transition registry
contract inspector
candidate generator
receipt chain
report surface
stop enforcement
```

Stop condition:

```text
full AI block candidate package prepared
not production
not self-accredited
```

### Phase 10 — AI Block Review Gate

Status:

```text
PENDING
```

Objective:

```text
Review whether StegVerse-001 can advance from initialization remote operator to scoped AI Block.
```

Allowed output:

```text
ALLOW_REVIEW
REVIEW_REQUIRED
DENY
FAIL_CLOSED
```

Stop condition:

```text
review packet returned
receipt emitted
```

## Milestone Table

| ID | Milestone | Status |
|---|---|---|
| SV001-M0 | Proven remote operator baseline | COMPLETE |
| SV001-M1 | Contractual inclusion candidate | READY |
| SV001-M2 | Remote contract recheck | PENDING |
| SV001-M3 | Existing Intake gate | PENDING |
| SV001-M4 | Recorded ingestion/CGE/sandbox loop | PENDING |
| SV001-M5 | Transition instruction block | PENDING |
| SV001-M6 | Transition class registry | PENDING |
| SV001-M7 | Milestone tracker | STARTED |
| SV001-M8 | Public documentation track | STARTED |
| SV001-M9 | Full AI Block candidate | PENDING |
| SV001-M10 | AI Block review gate | PENDING |

## Immediate Next Gate

```text
Core-Lite CGE Contractual Inclusion Candidate
```

Done means:

```text
core_lite/cge.py preserves existing CGE surfaces
core_lite/cge.py adds generate_cge_fingerprint
candidate is prepared through the allowed path
report and receipt are returned
STOP
```

## Boundary

This roadmap does not grant:

```text
production authority
node status
FinCo eligibility
workflow widening
unreviewed target mutation
self-accreditation
```

It only tracks the path toward a full Transition Table AI Block candidate.

## Operating Rule

```text
Transition Table in.
One transition out.
Receipt.
Stop.
```
