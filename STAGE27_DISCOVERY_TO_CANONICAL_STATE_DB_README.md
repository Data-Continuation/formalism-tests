# Stage 27 — Discovery-to-Canonical State DB

## Assumptions

1. Stages 1–25 have passed.
2. Stage 26 tests whether `StegVerse-001 / Beta_Orionis` can run the prior stages through declared-task routing.
3. Stage 27 begins the discovery-to-instantiation sequence.
4. Discovery observes, models, compares, and proposes.
5. Discovery does not install.

## Done

Stage 27 is done when:

```text
tools/run_stage27_discovery_to_canonical_state_tests.py
```

returns success and emits:

```text
reports/stage27_discovery_to_canonical_state_report.json
reports/stage27_discovery_gap_report.md
reports/stage27_discovered_state.json
reports/stage27_canonical_state.json
reports/stage27_state_diff.json
reports/stage27_install_plan_candidate.json
receipts/stage27_discovery_receipts.jsonl
```

## Task ID

```text
stage27_discovery_to_canonical_state_tests
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage27_discovery_tasks.json --task-id stage27_discovery_to_canonical_state_tests
```

## Core rule

```text
An install plan is a candidate transition, not installation authority.
```

## What Stage 27 proves

Stage 27 proves that the system can build a structured discovered-state DB, compare it to a canonical expectation, classify differences, and produce an install-plan candidate without mutating the target repo.

## Expected decision surface

```text
ALLOW_DISCOVERY
LEDGER_DISCOVERED_STATE
LEDGER_CANONICAL_DIFF
REQUIRE_REVIEW
FAIL_CLOSED
```

## Next stage

```text
Stage 28 — Canonical Diff and Install Plan Candidate
```
