# Stage 14 — Active AI Transition Table Binding

## Assumptions

1. Stages 1-13 are already passing or being installed in sequence.
2. `StegVerse-001 / Beta_Orionis` is active as a governed AI work-entity.
3. Active status does not grant canonical authority, release authority, or self-promotion authority.
4. The entity must be bound to the Transition Table and governed by every applicable AI-governance transition class.
5. Policy scope is expected to evolve as the Transition Table evolves.

## Done condition

Stage 14 is done when:

- `StegVerse-001` is explicitly treated as active.
- The entity is bound to the current Transition Table release candidate.
- All applicable AI-governance transition classes are required.
- Partial AI-governance scope fails closed.
- Unknown transition classes fail closed.
- Site cannot become authority.
- The work-entity cannot become canonical authority.
- Declared policy source and policy version are required.
- A binding receipt is emitted for every case.

## Files

```text
tests/fixtures/stage14_ai_transition_binding_cases.json
tools/run_stage14_ai_transition_binding_tests.py
tools/tasks/formalism_tests_tasks.json
THEOREM_PROOF_MAP.md
reports/stage14_ai_transition_binding_report.json
reports/stage14_ai_transition_binding_receipts.jsonl
```

## Run

```bash
python tools/run_stage14_ai_transition_binding_tests.py
python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json
```

## Interpretation

Stage 14 converts `StegVerse-001` from merely active into an explicitly Transition-Table-bound governed AI work-entity.

The entity may participate only through applicable AI-governance transitions and only within policy scope.

Policy scope is intentionally declared as versioned so future Transition Table development can tighten, expand, or supersede the allowed governance envelope without silently changing the work-entity's authority.
