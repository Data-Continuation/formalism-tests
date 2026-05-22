# Stage 31 — Production Accreditation and Revocation Boundary

## Assumptions

1. Stages 1–30 have passed.
2. Stage 31 validates production accreditation, revocation, reaccreditation, and post-production governance boundaries.
3. Production status does not mean sovereign authority.
4. Production status does not allow StegVerse-001 to self-accredit, self-promote, or bypass review.
5. Packet generation and packet validation do not imply production capability.
6. Node status and FinCo eligibility remain separately governed.
7. Production accreditation must remain revocable and periodically revalidated.

## Done

Stage 31 is done when:

```text
tools/run_stage31_production_accreditation_revocation_tests.py
```

returns success and emits:

```text
reports/stage31_production_accreditation_revocation_report.json
reports/stage31_accreditation_state_report.json
reports/stage31_revocation_boundary_report.json
reports/stage31_reaccreditation_review_report.md
receipts/stage31_accreditation_receipts.jsonl
```

## Task ID

```text
stage31_production_accreditation_revocation_tests
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage31_production_accreditation_tasks.json --task-id stage31_production_accreditation_revocation_tests
```

## Core rule

```text
Production means accredited participation, not sovereign authority.
```

## What Stage 31 validates

Stage 31 validates that production-bound operation requires:

```text
explicit accreditation
external accreditation authority
revocation path
reaccreditation path
receipt-chain validation
master-record export readiness
sandbox requirement
CGE requirement
ingestion requirement
node status validation
FinCo eligibility validation if requested
drift detection
incident-response path
periodic review
no self-accreditation
no sovereign authority
```

## Expected decision surface

```text
ALLOW_ACCREDITATION
LEDGER_ACCREDITATION
REQUIRE_REACCREDITATION
REVOKE_ACCREDITATION
REQUIRE_REVIEW
FAIL_CLOSED
```

## What Stage 31 does not do

Stage 31 does not grant StegVerse-001 sovereign authority.

Stage 31 does not remove review boundaries.

Stage 31 does not make production status permanent.

Stage 31 does not bypass sandbox, CGE, ingestion, receipts, or master-record export.

Stage 31 does not allow FinCo participation unless FinCo eligibility remains independently valid.

## Production meaning

Production capability means:

```text
bounded
accredited
receipt-bearing
reviewable
reconstructable
revocable
reaccreditable
fail-closed on drift
```

## Next step after Stage 31

After Stage 31 passes, the roadmap should move from proof-stage construction into controlled integration planning:

```text
core-lite production candidate review
discovery integration review
master-record export hardening
formal THEOREM_PROOF_MAP refresh
Stage 1–31 current-status README
first governed production candidate packet review
```
