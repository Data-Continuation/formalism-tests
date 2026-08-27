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

Required commands, in exact order:

```bash
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id optimization_target_commit_boundary_tests
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id verify_optimization_target_commit_boundary_artifacts
python tools/run_declared_tasks.py tools/tasks/optimization_target_commit_boundary_tasks.json --task-id check_optimization_target_canonical_evidence_gate
```

The canonical contract requires:

```text
three declared commands in exact order
three task results equal PASS
four SHA-256 values:
  report
  receipts
  artifact verification
  committed canonical-evidence gate checker source
four equivalence assertions:
  report
  receipts
  expected outcomes
  canonical-evidence gate checker source
nested artifact_hashes and artifact_equivalence objects
authority_posture: FORMALISM_TEST_EVIDENCE_ONLY
status: VERIFIED_CANONICAL_RUN
```

`artifact_hashes.canonical_evidence_gate_sha256` is the SHA-256 of the committed source file:

```text
tools/check_optimization_target_canonical_evidence_gate.py
```

It is not the digest of the gate's generated output. This removes self-referential receipt construction while preserving exact gate-version custody. The gate recomputes that source digest and rejects a mismatch. `artifact_equivalence.canonical_evidence_gate=true` therefore means the executed gate checker is byte-identical to the committed checker source identified by that digest.

## 2026-08-26 repository-owned canonical CI activation

The existing `continuation-tests.yml` workflow is the approved execution surface for issue #6; no duplicate workflow is required.

```text
1e8bc4542f2468bbfe824a2533efd27d41387e0b — deterministic report baseline committed
36a88e1156a1ce561eb7a968b80360a8d106831d — deterministic receipt baseline committed
75b461a89b7d139fa9dd7b7db9c2fedd9016a42b — repository-owned canonical capture runner installed
```

The capture runner requires GitHub Actions on `refs/heads/main`, regenerates all five cases, requires byte-equivalence to the committed report/receipt outputs, regenerates artifact verification, verifies expected outcomes against the committed baseline, binds four SHA-256 values including the non-self-referential committed gate-checker source, writes schema-shaped canonical evidence, runs the canonical evidence gate, and appends exact run evidence here only after the entire contract passes.

Source installation is not canonical execution. Issue #6 remains open until a hosted run completes and its generated evidence is durably committed.

## Current state

```text
canonical evidence status: VERIFIED_CANONICAL_RUN
canonical run: 33025167959
canonical commit: 70d4780dcaddf9371feb17e1247c401c0c3038d1
promotion eligible for bounded downstream review: true
generated report: PASS / 5_OF_5
generated receipts: PASS / byte-equivalent
artifact verification: PASS
downstream activation: still prohibited pending bounded Wiki review
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
Issue #6 canonical execution: COMPLETE / CLOSED.
Canonical evidence: receipts/optimization_target_canonical_execution_evidence.json.
Next owner: StegVerse-Labs/admissibility-wiki bounded review.
Require Wiki validation and public-route proof before any downstream propagation or release.
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

This handoff preserves the installed optimization-target package, exact-command canonical evidence contract, non-self-referential gate-checker hash custody, issue ownership, downstream activation boundary, authority restrictions, remaining files and destinations, and release posture. The complete thread is ready for archiving without additional conversation context.

## Canonical GitHub Actions execution observed

```text
status: VERIFIED_CANONICAL_RUN
commit_sha: 921c80ae6604ff97642d62adafeeaa94c774731f
execution_surface: GITHUB_ACTIONS
run_id: 33035686454
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/33035686454
task_results:
  optimization_target_commit_boundary_tests: PASS
  verify_optimization_target_commit_boundary_artifacts: PASS
  check_optimization_target_canonical_evidence_gate: PASS
report_sha256: db39b4a8cd4b8f244265e68141ab88b9b2291cd6eeab2fabdbc3059f21c37860
receipts_sha256: ab4fad099af436cfa941785770ec016afe96adb4c59f92cbb5f1bddee4f3d44d
artifact_verification_sha256: 739a35d5b986dd7bd545f24be966c9cafca6af408c525e9101cc1e18b85a2cdd
canonical_evidence_gate_sha256: 47ac4a3ff3ebedb7a127bdaa0add64dc7a35cc0d7698d9aaefd96153990f2915
report_equivalence: true
receipts_equivalence: true
expected_outcomes_equivalence: true
canonical_evidence_gate_equivalence: true
authority_posture: FORMALISM_TEST_EVIDENCE_ONLY
downstream_owner: StegVerse-Labs/admissibility-wiki
```

This is repository-owned canonical execution evidence for the optimization-target commit-boundary proof package. It establishes deterministic proof evidence only. It does not establish that an optimization target is objectively correct, nor grant installation, production, publication, financial, sovereign, certification, release, execution, or downstream mutation authority.
