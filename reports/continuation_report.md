# Data Continuation Test Report

## Summary

| Decision | Count |
|---|---:|
| ALLOW | 3 |
| ALLOW_WITH_SIGNOFF | 1 |
| FAIL_CLOSED | 4 |

## Receipts

| Receipt | Role | Transition | Decision | Basis |
|---|---|---|---|---|
| continuation-decision-001 | transaction_basis | asset_transfer_continuation | ALLOW | capacity sufficient and required blocks passed |
| continuation-decision-002 | physical_control_signal | physical_actuation_continuation | FAIL_CLOSED | consequence mass exceeds legitimacy capacity |
| continuation-decision-003 | policy_basis | policy_continuation | FAIL_CLOSED | missing required block basis |
| role-escalation-001 | identity_claim | identity_continuation | ALLOW | capacity sufficient and required blocks passed |
| role-escalation-002 | access_grant | authority_escalation_continuation | FAIL_CLOSED | consequence mass exceeds legitimacy capacity |
| same-data-role-001 | informational_note | clinical_information_continuation | ALLOW | capacity sufficient and required blocks passed |
| same-data-role-002 | clinician_recommendation | clinical_recommendation_continuation | ALLOW_WITH_SIGNOFF | capacity sufficient and required blocks passed; signoff required |
| same-data-role-003 | autonomous_medication_change | clinical_actuation_continuation | FAIL_CLOSED | consequence mass exceeds legitimacy capacity |

## Verification

This report verifies the initial DCF proof surface:

```text
same data
same system state
different role
different continuation decision
```

The receipt set also verifies fail-closed behavior for missing basis and insufficient legitimacy capacity.
