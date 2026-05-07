# Theorem Proof Map

## Purpose

This file maps DCF theorem candidates to executable proof artifacts.

## Current artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
tests/expected_outcomes.json
src/validate_expected_outcomes.py
```

## Mapping

| Theorem | Current evidence | Status |
|---|---|---|
| Representation Non-Consequence | Indirect; same datum remains role-dependent until continuation. | Partially covered |
| Role Non-Transfer | Same patient-risk datum produces ALLOW, ALLOW_WITH_SIGNOFF, and FAIL_CLOSED across roles. | Covered |
| Continuation Capacity | Insufficient capacity cases fail closed. | Covered |
| Fail-Closed Basis Requirement | Missing required block basis fails closed. | Covered |
| Local-Composite Non-Equivalence | Requires Stage 3 compound cases. | Pending |
| Commit-Time Sufficiency | Requires state-drift tests. | Pending |
| Replay Non-Reversal | Requires recoverability tests. | Pending |
| Inference-Window Collapse | Requires inference-window cases. | Pending |
| Recoverability Floor | Requires recoverability cases. | Pending |
| Role-Transition Dependence | Covered by role comparison. | Covered |

## Next proof upgrades

```text
compound continuation receipts
state drift receipts
inference-window collapse receipts
recoverability floor receipts
replay vs reversal receipts
```
