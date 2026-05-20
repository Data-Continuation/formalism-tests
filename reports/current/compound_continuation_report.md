# Stage 3 Compound Continuation Test Report

## Public proof claims

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

## Verification status

Success: `true`

## Decision summary

| Decision | Count |
|---|---:|
| ALLOW | 1 |
| FAIL_CLOSED | 5 |

## Theorem mapping

| Theorem | Status |
|---|---|
| Commit-Time Sufficiency | Covered |
| Compound Continuation Positive Control | Covered |
| Inference-Window Collapse | Covered |
| Local-Composite Non-Equivalence | Covered |
| Recoverability Floor | Covered |
| Replay Non-Reversal | Covered |

## Receipts

| Receipt | Theorem | Role | Transition | Decision | Basis |
|---|---|---|---|---|---|
| stage3-compound-local-001 | Local-Composite Non-Equivalence | compound_asset_transfer_basis | compound_asset_transfer_continuation | FAIL_CLOSED | composite consequence mass exceeds legitimacy capacity |
| stage3-drift-commit-001 | Commit-Time Sufficiency | policy_basis | policy_continuation_with_state_drift | FAIL_CLOSED | commit-time state drift detected |
| stage3-inference-collapse-001 | Inference-Window Collapse | clinical_recommendation_basis | clinical_recommendation_with_collapsed_window | FAIL_CLOSED | inference window collapsed below continuation threshold |
| stage3-recoverability-floor-001 | Recoverability Floor | physical_control_signal | physical_actuation_continuation | FAIL_CLOSED | recoverability score below required floor |
| stage3-replay-non-reversal-001 | Replay Non-Reversal | transaction_basis | ledger_transfer_replay_attempt | FAIL_CLOSED | replay may reconstruct receipt state but may not reverse consequence |
| stage3-compound-allow-001 | Compound Continuation Positive Control | compound_informational_basis | compound_information_continuation | ALLOW | compound continuation remains within capacity and recoverability bounds |

## Interpretation

Stage 3 extends continuation testing beyond role comparison into compound and temporal admissibility.

The new receipt set demonstrates that local admissibility does not compose automatically into global admissibility. A transition may fail closed because the composite consequence mass exceeds legitimacy capacity, because state drift occurred at commit time, because the inference window collapsed, because recoverability fell below the required floor, or because replay was incorrectly treated as reversal.

This supports the next formal move from data-role continuation toward system-coherent boundary dynamics and coupled admissibility fields.
