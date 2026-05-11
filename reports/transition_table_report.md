# Stage 4 Transition Table Integration Report

## Public proof claim

```text
A transition class is valid only if its admissibility contract specifies the conditions under which the transition may bind consequence.
```

## Verification status

Success: `true`

## Decision summary

| Decision | Count |
|---|---:|
| ALLOW | 1 |
| FAIL_CLOSED | 5 |

## Transition class receipts

| Receipt | Transition ID | Family | Theorem basis | Coupling class | Decision | Basis |
|---|---|---|---|---|---|---|
| stage4-tt-compound-asset-transfer-001 | T-CONT-COMPOUND-ASSET-001 | compound_continuation | Local-Composite Non-Equivalence | shared-resource | FAIL_CLOSED | composite consequence mass exceeds legitimacy capacity |
| stage4-tt-policy-state-drift-001 | T-CONT-POLICY-DRIFT-001 | commit_time_state | Commit-Time Sufficiency | authority-transfer | FAIL_CLOSED | commit-time state drift detected |
| stage4-tt-clinical-window-collapse-001 | T-CONT-CLINICAL-WINDOW-001 | inference_window | Inference-Window Collapse | coherence-coupled | FAIL_CLOSED | inference window collapsed below transition-class minimum |
| stage4-tt-physical-recoverability-floor-001 | T-CONT-PHYSICAL-RECOVERABILITY-001 | recoverability_floor | Recoverability Floor | irreversible-consequence | FAIL_CLOSED | recoverability score below transition-class floor |
| stage4-tt-ledger-replay-non-reversal-001 | T-CONT-LEDGER-REPLAY-001 | replay_semantics | Replay Non-Reversal | irreversible-consequence | FAIL_CLOSED | transition-class replay semantics prohibit reversal |
| stage4-tt-compound-information-allow-001 | T-CONT-COMPOUND-INFO-001 | compound_continuation | Compound Continuation Positive Control | paired-boundary | ALLOW | transition class admissibility contract satisfied |

## Interpretation

Stage 4 turns Stage 3 continuation proofs into executable transition-table classes.

The transition table is no longer only descriptive. Each transition class now carries an admissibility contract containing consequence mass, required legitimacy capacity, recoverability floor, inference-window minimum, commit-time state requirements, replay semantics, boundary behavior, coupling class, and allowed outcomes.

This supports the construction of a transition periodic table in which each transition type is a governed consequence-binding class rather than a label.
