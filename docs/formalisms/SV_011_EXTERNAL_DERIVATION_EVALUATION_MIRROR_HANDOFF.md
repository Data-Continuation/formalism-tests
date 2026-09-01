# SV-011 External Derivation Evaluation Contract

Status: PREPARED_EXTERNAL_EVALUATOR
Updated: 2026-09-01
Target: `SV-011/entity`
Authority effect: NONE

## Purpose

Provide an independent test-side contract for the smallest defensible SV-011 milestone without implementing the entity's generator for it.

## Existing executable references

- `src/outcome_vocabulary.py`
- `src/role_aware_continuation.py`
- `tests/test_role_aware_continuation.py`
- transition-table receipt/test surfaces already present in this repository

## Minimum evaluation package expected from SV-011

The evaluator should require:
1. one hashed first transition element;
2. one declared source role and one requested target role;
3. the required escalation block set;
4. one admitted capability result;
5. one denied or fail-closed capability result;
6. a receipt for both outcomes;
7. explicit six-outcome decision vocabulary or declared projection;
8. source commit/blob pins;
9. authority flags remaining false unless separately admitted;
10. enough ordered receipt identity to permit independent reconstruction.

## Failure conditions

The external evaluation fails closed when:
- capability is inferred only from observed behavior;
- required standing/block basis is missing, stale, unknown, or contradictory;
- an ALLOW result is treated as proof execution occurred;
- replay is treated as renewed authority;
- source pinning is absent;
- a denied chain is later treated as valid continuation;
- runtime/publication/proof authority is claimed without separate evidence.

## Boundary

A passing external test is evaluation evidence only. It does not grant execution, publication, release, proof-acceptance, custody, or autonomous status.
