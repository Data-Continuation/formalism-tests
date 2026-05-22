# Stage 29 Theorem Proof Map Update

Add this section after Stage 28.

## Stage 29 — Optional Node Status and FinCo Eligibility

Stage 29 validates node status and FinCo eligibility as explicit opt-in layers.

It establishes:

```text
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
FinCo eligibility requires explicit node status, valid receipts, compensation rules, and revocation rules.
```

Stage 29 emits:

```text
reports/stage29_node_status_finco_eligibility_report.json
reports/stage29_node_status_report.json
reports/stage29_finco_eligibility_report.json
reports/stage29_node_status_review_report.md
receipts/stage29_node_finco_receipts.jsonl
```

Expected decisions:

```text
ALLOW_NODE_STATUS
ALLOW_FINCO_ELIGIBILITY
LEDGER_NODE_STATUS
LEDGER_FINCO_ELIGIBILITY
REQUIRE_REVIEW
FAIL_CLOSED
```

Next stage:

```text
Stage 30 — Governed Instantiation Packet (*.tar.gz)
```
