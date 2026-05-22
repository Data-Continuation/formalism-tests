# Stage 28 Theorem Proof Map Update

Add this section after Stage 27.

## Stage 28 — Canonical Diff and Install Plan Candidate

Stage 28 validates that a canonical diff can be transformed into an install-plan candidate without becoming install authority.

Canonical rule:

```text
An install plan is a candidate transition, not installation authority.
```

Stage 28 emits:

```text
reports/stage28_canonical_diff_install_plan_report.json
reports/stage28_install_plan_review_report.md
reports/stage28_state_diff_validated.json
reports/stage28_install_plan_candidate.json
receipts/stage28_install_plan_receipts.jsonl
```

Expected decisions:

```text
ALLOW_INSTALL_PLAN_CANDIDATE
LEDGER_INSTALL_PLAN
REQUIRE_REVIEW
QUARANTINE_PLAN
FAIL_CLOSED
```

Stage 28 establishes:

```text
A diff must classify every difference.
Unknown files are not automatically overwritten.
Protected paths require review or fail closed.
Dangerous changes fail closed.
The install plan cannot authorize itself.
Sandbox, CGE, and receipts are required before binding.
Node status and FinCo remain opt-in only.
```

Next stage:

```text
Stage 29 — Optional Node Status and FinCo Eligibility
```
