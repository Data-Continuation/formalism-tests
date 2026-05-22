# Stage 29 — Optional Node Status and FinCo Eligibility

## Assumptions

1. Stages 1–28 have passed.
2. Stage 29 validates opt-in node status and FinCo eligibility before governed instantiation packet production.
3. Core installation must not imply node participation.
4. Node participation must not imply FinCo eligibility.
5. FinCo participation requires explicit opt-in, admissible node status, valid receipts, compensation rules, revocation rules, and intact chain evidence.
6. Stage 29 does not install, mutate, enable payments, create entitlement, or activate node status by itself.

## Done

Stage 29 is done when:

```text
tools/run_stage29_node_status_finco_eligibility_tests.py
```

returns success and emits:

```text
reports/stage29_node_status_finco_eligibility_report.json
reports/stage29_node_status_report.json
reports/stage29_finco_eligibility_report.json
reports/stage29_node_status_review_report.md
receipts/stage29_node_finco_receipts.jsonl
```

## Task ID

```text
stage29_node_status_finco_eligibility_tests
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage29_node_finco_tasks.json --task-id stage29_node_status_finco_eligibility_tests
```

## Core rule

```text
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
FinCo eligibility requires explicit node status, valid receipts, compensation rules, and revocation rules.
```

## Node statuses

```text
NOT_A_NODE
NODE_PENDING
NODE_ACTIVE
NODE_LIMITED
NODE_SUSPENDED
NODE_REVOKED
NODE_RETIRED
```

## FinCo eligibility requires

```text
node_participation_opt_in == true
node_status in [NODE_ACTIVE, NODE_LIMITED]
finco_participation_requested == true
consent_receipt_valid == true
access_receipt_valid == true
use_receipt_valid == true
compensation_rule_defined == true
revocation_rule_defined == true
chain_intact == true
creates_entitlement == false unless entitlement_authority_valid == true
```

## Expected decision surface

```text
ALLOW_NODE_STATUS
ALLOW_FINCO_ELIGIBILITY
LEDGER_NODE_STATUS
LEDGER_FINCO_ELIGIBILITY
REQUIRE_REVIEW
FAIL_CLOSED
```

## What Stage 29 does not do

Stage 29 does not activate a real network node.

Stage 29 does not authorize financial participation.

Stage 29 does not create entitlement.

Stage 29 only validates the admissibility rules that future node and FinCo participation must satisfy.

## Next stage

```text
Stage 30 — Governed Instantiation Packet (*.tar.gz)
```
