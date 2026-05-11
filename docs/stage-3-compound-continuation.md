# Stage 3 Compound Continuation Proof Cases

## Purpose

Stage 3 extends the Data Continuation Formalism proof surface beyond role comparison.

The Stage 2 proof claim was:

```text
same data ≠ same continuation admissibility
```

Stage 3 adds compound and temporal claims:

```text
local allow + local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay can reconstruct consequence state but cannot reverse consequence
recoverability and inference-window floors are admissibility conditions
```

## Files

```text
tests/compound_cases.json
src/compound_continuation_gate.py
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
```

## Run

```bash
python src/compound_continuation_gate.py
```

## Expected Outputs

```text
reports/compound_receipts.jsonl
reports/compound_continuation_report.md
```

## Theorem Coverage

| Theorem | Stage 3 coverage |
|---|---|
| Local-Composite Non-Equivalence | Covered |
| Commit-Time Sufficiency | Covered |
| Replay Non-Reversal | Covered |
| Inference-Window Collapse | Covered |
| Recoverability Floor | Covered |

## Interpretation

Stage 3 demonstrates that admissibility must be evaluated at the continuation boundary, not merely at representation time, local component time, or pre-commit time.

A compound transition may fail closed even when all local components appear admissible.

A transition may fail closed when the system state drifts before commit.

A replay may reconstruct what happened, but replay is not reversal.

A transition may also fail closed when the inference window collapses or the recoverability score falls below the required floor.
