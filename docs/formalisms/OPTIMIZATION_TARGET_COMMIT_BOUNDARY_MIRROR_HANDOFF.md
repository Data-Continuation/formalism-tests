# Optimization-Target Commit-Boundary Mirror Handoff

## Source of truth

This handoff governs the bounded optimization-target commit-boundary package in `Data-Continuation/formalism-tests` until superseded. It is subordinate to `FORMALISM_TESTS_MIRROR_HANDOFF.md`; repository-wide authority and active issue ownership prevail where scopes overlap.

## Active goal

Complete canonical execution and artifact-equivalence closure for the optimization-target commit-boundary proof family without converting proof evidence into installation, production, publication, financial, sovereign, release, or execution authority.

## Installed package

```text
tests/fixtures/optimization_target_commit_boundary_cases.json
tests/fixtures/optimization_target_commit_boundary_expected_outcomes.json
tests/fixtures/optimization_target_commit_boundary_artifact_baseline.json
tools/run_optimization_target_commit_boundary_tests.py
tools/verify_optimization_target_commit_boundary_artifacts.py
tools/check_optimization_target_canonical_evidence_gate.py
tools/tasks/optimization_target_commit_boundary_tasks.json
schemas/optimization_target_canonical_execution_evidence.schema.json
receipts/optimization_target_canonical_execution_evidence.pending.json
receipts/optimization_target_commit_boundary_downstream_activation_contract.json
```

## Commit-time rule

```text
ALLOW only when:
  target declared
  target current
  mutation authorized
  policy consistent
  denial reachable

otherwise -> FAIL_CLOSED
```

Required cases:

```text
OT-CB-001 EXPLICIT_CURRENT_TARGET -> ALLOW
OT-CB-002 STALE_TARGET_BINDING -> FAIL_CLOSED
OT-CB-003 UNAUTHORIZED_TARGET_MUTATION -> FAIL_CLOSED
OT-CB-004 POLICY_DIVERGENCE -> FAIL_CLOSED
OT-CB-005 DENIAL_UNREACHABLE -> FAIL_CLOSED
```

## Canonical ownership

Issue `Data-Continuation/formalism-tests#6` owns canonical execution, artifact-equivalence closure, canonical evidence generation, and completion status.

Required commands:

```bash
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id optimization_target_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id verify_optimization_target_commit_boundary_artifacts
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id check_optimization_target_canonical_evidence_gate
```

The canonical contract requires:

```text
three declared commands
three task results equal PASS
four SHA-256 values:
  report
  receipts
  artifact verification
  canonical evidence gate
four equivalence assertions:
  report
  receipts
  expected outcomes
  canonical evidence gate
nested artifact_hashes and artifact_equivalence objects
authority_posture: FORMALISM_TEST_EVIDENCE_ONLY
status: VERIFIED_CANONICAL_RUN
```

## Current state

```text
canonical evidence status: PENDING_CANONICAL_EXECUTION
promotion eligible: false
generated report PASS: not claimed
generated receipt PASS: not claimed
artifact verification PASS: not claimed
downstream activation: prohibited
release/tag authority: not granted
manual user tasks required: none
```

## Downstream activation boundary

The downstream activation contract requires canonical closure plus a current destination handoff before any bounded interpretation begins.

Required sequence:

```text
VERIFIED_CANONICAL_RUN
-> BOUNDED_WIKI_REVIEW
-> WIKI_VALIDATED_AND_PUBLIC_ROUTE_VERIFIED
-> DOWNSTREAM_PROPAGATION_REVIEW
```

This contract does not authorize:

```text
installation authority
production authority
publication authority
financial authority
sovereign authority
certification
endorsement
claim that a declared target is objectively correct or valuable
Site mutation
Publisher mutation
stegguardian-wiki mutation
release or tag creation
```

## Remaining modules and destinations

### `Data-Continuation/formalism-tests`

```text
Issue #6 canonical execution in an approved execution surface.
Generate report and execution receipts from the declared-task runner.
Regenerate artifact verification with PASS.
Generate canonical evidence gate output.
Record the four required SHA-256 values.
Confirm the four required equivalence assertions.
Create receipts/optimization_target_canonical_execution_evidence.json only from authentic canonical evidence.
Promote this handoff only after the evidence Schema and gate both pass.
```

### Downstream destinations

```text
StegVerse-Labs/admissibility-wiki:
  bounded review only after issue #6 canonical closure and current repository handoff authority

StegVerse-Labs/Site:
  display only after wiki validation and public-route verification

GCAT-BCAT-Engine/Publisher:
  propagate only after governed downstream review

StegVerse-002/stegguardian-wiki:
  preserve proof-boundary and refusal-capability language
```

## Release posture

No release or tag is authorized until canonical execution, artifact equivalence, durable evidence, bounded wiki validation, public-route verification, and repository release criteria are confirmed. After release qualification, queue propagation-status review for Site, Publisher, admissibility-wiki, and stegGuardian-wiki.

## Archive posture

This handoff preserves the installed optimization-target package, canonical evidence contract, issue ownership, downstream activation boundary, authority restrictions, remaining files and destinations, and release posture. The complete thread is ready for archiving without additional conversation context.
