# Data Continuation Formalism Tests

This repository contains executable tests for the Data Continuation Formalism.

## Purpose

The first proof surface demonstrates:

```text
same data
same system state
different role
different continuation decision
```

This proves:

```text
same data ≠ same continuation admissibility
```

## Included files

```text
README.md
src/continuation_gate.py
tests/same_data_different_roles.json
tests/role_escalation_cases.json
tests/continuation_decision_cases.json
reports/sample_receipts.jsonl
```

## Run

```bash
python src/continuation_gate.py
```

## Done criteria

The test harness is done when it:

1. Loads JSON test cases.
2. Computes legitimacy capacity.
3. Computes capacity gap.
4. Evaluates required blocks.
5. Emits deterministic decisions.
6. Writes receipt records.
