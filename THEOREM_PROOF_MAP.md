# Theorem Proof Map

## Purpose

This file maps DCF and transition-table theorem candidates to executable proof artifacts in `formalism-tests`.

## Authority Boundary

```text
formalism-tests produces receipts.
Site publishes receipts.
Site must not become the authority for receipts.
StegVerse-001 / Beta_Orionis may be active as a governed work-entity, but must not become canonical authority.
```

## Current Workflow Evidence

The declared-task workflow now supports the validated transition proof chain through Stage 13:

```text
archive_runtime_artifacts
continuation_gate
compound_continuation_gate
transition_table_gate
boundary_transition_gate
stage6_unified_gate_tests
element_dependency_closure_tests
stage8_ai_domain_tests
stage9_multi_body_coupling_tests
stage9_reconciliation_tests
stage10_canonical_release_tests
stage11_candidate_expansion_governance_tests
stage12_candidate_promotion_queue_tests
stage13_active_work_entity_release_delta_tests
transition_table_public_surface_tests
representation_non_consequence_tests
site_mirror_integrity_tests
current_report_preservation_tests
theorem_map_consistency_tests
```

## Current Proof Artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
reports/transition_table_receipts.jsonl
reports/boundary_transition_receipts.jsonl
reports/representation_non_consequence_receipts.jsonl
reports/representation_non_consequence_report.json
reports/representation_non_consequence_report.md
reports/transition_table_public_surface_report.json
reports/site_mirror_integrity_report.json
reports/current_report_preservation_report.json
reports/theorem_map_consistency_report.json
reports/element_dependency_closure_report.json
reports/element_dependency_closure_receipts.jsonl
reports/stage8_ai_domain_report.json
reports/stage8_ai_domain_receipts.jsonl
reports/stage9_multi_body_coupling_report.json
reports/stage9_multi_body_coupling_receipts.jsonl
reports/stage9_reconciliation_report.json
reports/stage10_canonical_release_report.json
reports/stage11_candidate_expansion_governance_report.json
reports/stage11_candidate_expansion_governance_receipts.jsonl
reports/stage12_candidate_promotion_queue_report.json
reports/stage12_candidate_promotion_queue_receipts.jsonl
reports/stage13_active_work_entity_release_delta_report.json
reports/stage13_active_work_entity_release_delta_receipts.jsonl
dist/transition-table-v1-rc1/canonical_transition_table_release.json
dist/transition-table-v1-rc1/canonical_transition_table_release.sha256
dist/transition-table-v1-rc1/replay_packet.json
dist/transition-table-v1-rc1/release_receipt.json
```

## Theorem Mapping

| Theorem / Proof Layer | Current evidence | Status |
|---|---|---|
| Representation Non-Consequence | Direct representation-only receipts show `NO_CONSEQUENCE` until a datum is bound to a consequence-bearing role, transition, and continuation path. | Covered |
| Role Non-Transfer | Same patient-risk datum produces `ALLOW`, `ALLOW_WITH_SIGNOFF`, and `FAIL_CLOSED` across roles. | Covered |
| Continuation Capacity | Insufficient legitimacy capacity produces `FAIL_CLOSED`. | Covered |
| Fail-Closed Basis Requirement | Missing required block basis produces `FAIL_CLOSED`. | Covered |
| Local-Composite Non-Equivalence | Stage 3 proves local `ALLOW` plus local `ALLOW` can fail closed when composite consequence mass exceeds legitimacy capacity. | Covered |
| Commit-Time Sufficiency | Stage 3 proves pre-commit state is not sufficient when commit-time state drift occurs. | Covered |
| Replay Non-Reversal | Stage 3 proves replay can reconstruct receipt state but cannot reverse consequence. | Covered |
| Inference-Window Collapse | Stage 3 proves collapsed inference windows fail closed. | Covered |
| Recoverability Floor | Stage 3 proves recoverability below the required floor fails closed. | Covered |
| Role-Transition Dependence | Covered by role comparison and same-data continuation decisions. | Covered |
| Compound Continuation Positive Control | Stage 3 proves compound continuation may allow when capacity and recoverability bounds hold. | Covered |
| Stage 6 Unified Gate | Stage 6 validates the AE unified gate across 10 candidates and 320 assertions. | Covered |
| Stage 7 Element Dependency Closure | Stage 7 validates unlocked element dependency closure across 13 elements and 105 assertions. | Covered |
| Stage 8 AI Domain Transition Classes | Stage 8 validates AI governance, derivation, verification, quorum, hidden authority, dependency closure, and scope transition classes. | Covered |
| Stage 9 Multi-Body Coupling Closure | Stage 9 validates 10 candidates, 80 assertions, and all 9 declared multi-body coupling classes. | Covered |
| Stage 9 Reconciliation | Stage 9 reconciliation validates documentation, theorem map, policies, and declared-task state through Stage 10. | Covered |
| Stage 10 Canonical Transition Table Release | Stage 10 emits a deterministic canonical release candidate, hash, replay packet, and release receipt. | Covered |
| Stage 11 Candidate Expansion Governance | Stage 11 validates that `StegVerse-001 / Beta_Orionis` may propose, draft, sandbox-test, reject, supersede, and queue candidates without self-promoting into canonical authority. | Covered |
| Stage 12 Governed Candidate Promotion and Release Queue | Stage 12 validates that accepted Stage 11 candidates may enter a governed release queue only through formalism-tests authority, accepted review, closed dependencies, receipts, manifest validation, hash validation, lineage validation, and queue ledger recording. | Covered |
| Stage 13 Active Work-Entity Release Candidate Delta | Stage 13 validates that active `StegVerse-001 / Beta_Orionis` may propose release-candidate deltas from `transition-table-v1-rc1` toward `transition-table-v1-rc2` only while formalism-tests retains canonical upgrade authority, lineage continuity, receipts, delta hashes, replay packets, and Site mirror boundaries. | Covered |
| Transition Table Public Surface | Public surface runner validates transition classes, elements, single-source status, and mobile/public presentation contracts. | Covered |
| Site Mirror Integrity | Site mirror runner validates that Site mirrors proof data without becoming proof authority. | Covered |
| Current Report Preservation | Current-report runner preserves latest successful proof reports under stable `reports/current/` paths. | Covered |
| Theorem Map Consistency | Theorem-map runner verifies root and current theorem maps agree with latest successful proof reports. | Covered |

## Stage 2 Proof Surface

```text
same data != same continuation admissibility
```

Stage 2 proves that data content alone does not determine continuation admissibility. The same datum can be safe as an informational note, conditional as a clinician recommendation, and inadmissible as autonomous actuation.

## Stage 3 Proof Surface

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

Stage 3 extends continuation testing into compound and temporal admissibility.

## Stage 6 Unified Gate Proof Surface

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

Validated decision surface:

```text
ALLOW: 3
FAIL_CLOSED: 5
RESET_BOUNDARY: 1
EVOLVE_BOUNDARY: 1
```

## Stage 7 Element Dependency Closure

Stage 7 validates that unlocked transition elements cannot be treated as release-ready unless their dependencies are declared, closed, and compatible with the current proof surface.

## Stage 8 AI Domain Transition Classes

Stage 8 validates that AI-domain participation is admissible only under scoped transition classes, dependency closure, quorum checks, and hidden-authority prevention.

## Stage 9 Multi-Body Coupling Closure

Stage 9 validates that admissibility cannot always be evaluated in isolation. Coupled entity states require composite evaluation across coupling classes:

```text
authority-transfer
coherence-coupled
distributed-node
irreversible-consequence
isolated
multi-agent-cascade
paired-boundary
shared-resource
trust-field
```

## Stage 10 Canonical Transition Table Release

Stage 10 produces the canonical release candidate:

```text
release_id: transition-table-v1-rc1
canonical_status: release_candidate
canonical_elements: 13
coupling_classes: 9
next_release_state: transition-table-v1
```

## Stage 11 Candidate Expansion Governance

Stage 11 validates the governance model for allowing an AI work-entity to help expand the Transition Table without becoming canonical authority.

```text
entity_id: StegVerse-001
entity_alias: Beta_Orionis
entity_type: governed_ai_work_entity
```

Stage 11 decision coverage:

```text
ALLOW_SANDBOX
ALLOW_RELEASE_QUEUE
FAIL_CLOSED
LEDGER_REJECTION
LEDGER_SUPERSESSION
```

## Stage 12 Governed Candidate Promotion and Release Queue

Stage 12 validates that candidates cannot move from proposal or review into a release queue merely because they exist, passed sandbox checks, or were produced by an AI work-entity.

Promotion into the governed release queue requires:

```text
formalism-tests authority
accepted review
closed dependency closure
receipt emission
release manifest presence
release hash validation
supersession lineage validation
queue ledger recording
Site remaining public mirror only
```

Stage 12 decision coverage:

```text
ALLOW_QUEUE_ENTRY
FAIL_CLOSED
LEDGER_QUEUE_ENTRY
```

Validated Stage 12 result:

```text
case_count: 11
receipt_count: 11
assertion_count: 59
ALLOW_QUEUE_ENTRY: 2
FAIL_CLOSED: 8
LEDGER_QUEUE_ENTRY: 1
```

## Stage 13 Active Work-Entity Release Candidate Delta

Stage 13 validates that `StegVerse-001 / Beta_Orionis` is active, but bounded.

Active status means the work-entity may participate in release-candidate delta formation. It does not mean the work-entity may become canonical authority, self-promote, bypass formalism-tests authority, or cause Site to become proof authority.

Stage 13 requires:

```text
active work-entity status
formalism-tests canonical upgrade authority
source release hash presence
accepted queue entry state
accepted review
closed dependency closure
valid receipt chain
delta manifest presence
delta manifest hash validation
replay packet presence
lineage continuity from transition-table-v1-rc1 to transition-table-v1-rc2
canonical upgrade ledger recording for ledger actions
Site remaining public mirror only
```

Stage 13 decision coverage:

```text
ALLOW_RELEASE_CANDIDATE_DELTA
FAIL_CLOSED
LEDGER_CANONICAL_UPGRADE
```

Validated Stage 13 target result:

```text
case_count: 11
receipt_count: 11
assertion_count: 70+
ALLOW_RELEASE_CANDIDATE_DELTA: 1
FAIL_CLOSED: 9
LEDGER_CANONICAL_UPGRADE: 1
```

## Current Interpretation

The proof surface now spans:

```text
data representation
role binding
transition binding
continuation path
compound admissibility
commit-time admissibility
replay/reconstruction
inference-window containment
recoverability floor
system-coherent boundary behavior
element dependency closure
AI-domain participation
multi-body coupling closure
canonical release-candidate generation
candidate expansion governance
governed candidate promotion
release queue ledgering
active governed work-entity participation
release-candidate delta continuity
canonical upgrade boundary preservation
public mirror integrity
current-report preservation
theorem-map consistency
```

The next proof layer should validate how the Stage 13 release-candidate delta becomes a fully reconstructed canonical upgrade packet, likely:

```text
Stage 14 - Canonical Upgrade Replay and Continuity Receipt
```
