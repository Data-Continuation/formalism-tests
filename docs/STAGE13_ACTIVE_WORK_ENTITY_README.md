# Stage 13 Active Work-Entity Release Delta Bundle

## Purpose

This bundle advances `Data-Continuation/formalism-tests` beyond the already-passing Stage 1-12 suite.

Stage 13 treats `StegVerse-001 / Beta_Orionis` as an active governed AI work-entity and validates whether it may contribute queued release-candidate deltas from `transition-table-v1-rc1` toward `transition-table-v1-rc2` without becoming canonical authority.

## Assumptions

1. Stages 1-12 are already passing.
2. `StegVerse-001 / Beta_Orionis` is active as a governed AI work-entity.
3. Active status permits bounded work-entity participation, not self-promotion.
4. Canonical upgrade authority remains `formalism-tests`.
5. `Site` remains a public mirror only.

## Done Means

Stage 13 is complete when:

- The fixture loads.
- All Stage 13 cases evaluate deterministically.
- Active status is required.
- Self-promotion fails closed.
- Site authority claims fail closed.
- Broken lineage fails closed.
- Open dependencies fail closed.
- Invalid receipt chains fail closed.
- Invalid delta hashes fail closed.
- Missing replay packets fail closed.
- Non-queued candidates fail closed.
- A valid active work-entity delta is allowed.
- A valid canonical upgrade ledger entry is recorded.

## Files

```text
tests/fixtures/stage13_active_work_entity_release_delta_cases.json
tools/run_stage13_active_work_entity_release_delta_tests.py
tools/tasks/formalism_tests_tasks.json
THEOREM_PROOF_MAP.md
```

## Expected Stage 13 Report Outputs

```text
reports/stage13_active_work_entity_release_delta_report.json
reports/stage13_active_work_entity_release_delta_receipts.jsonl
```

## Run

```bash
python tools/run_stage13_active_work_entity_release_delta_tests.py
```

Then run the declared-task suite:

```bash
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json
```

## Expected Decision Coverage

```text
ALLOW_RELEASE_CANDIDATE_DELTA: 1
FAIL_CLOSED: 9
LEDGER_CANONICAL_UPGRADE: 1
```

## Boundary Statement

```text
StegVerse-001 / Beta_Orionis is active.
Active does not mean canonical.
Active does not mean self-promoting.
Active means bounded participation through formalism-tests authority.
```
