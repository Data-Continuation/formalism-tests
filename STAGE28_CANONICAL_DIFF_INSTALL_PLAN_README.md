# Stage 28 — Canonical Diff and Install Plan Candidate

## Assumptions

1. Stage 27 has passed and produced a discovered-state DB, canonical-state expectation, state diff, install-plan candidate, reports, and receipts.
2. Stage 28 deepens the Stage 27 output by validating the canonical diff and install-plan candidate as first-class governed artifacts.
3. Stage 28 remains non-installing. It must not mutate the target repo.
4. An install plan remains a candidate transition, not installation authority.
5. Node participation and FinCo participation remain disabled by default unless explicitly opted in.

## Done

Stage 28 is done when:

```text
tools/run_stage28_canonical_diff_install_plan_tests.py
```

returns success and emits:

```text
reports/stage28_canonical_diff_install_plan_report.json
reports/stage28_install_plan_review_report.md
reports/stage28_state_diff_validated.json
reports/stage28_install_plan_candidate.json
receipts/stage28_install_plan_receipts.jsonl
```

## Task ID

```text
stage28_canonical_diff_install_plan_tests
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage28_install_plan_tasks.json --task-id stage28_canonical_diff_install_plan_tests
```

## Core rule

```text
An install plan is a candidate transition, not installation authority.
```

## What Stage 28 validates

Stage 28 validates that canonical diffs and install-plan candidates are safe to hand forward into sandbox, CGE, and ingestion.

It checks:

```text
diff categories are recognized
unknown files are classified
protected-path changes require review or fail closed
dangerous changes fail closed
install_allowed_by_plan remains false
sandbox is required
CGE is required
receipts are required
node status defaults to NOT_A_NODE
FinCo participation defaults to disabled
```

## Expected decision surface

```text
ALLOW_INSTALL_PLAN_CANDIDATE
LEDGER_INSTALL_PLAN
REQUIRE_REVIEW
QUARANTINE_PLAN
FAIL_CLOSED
```

## What Stage 28 does not do

Stage 28 does not install files, mutate workflows, approve its own plan, claim canonical authority, enable node status, or enable FinCo participation.

## Next stage

```text
Stage 29 — Optional Node Status and FinCo Eligibility
```
