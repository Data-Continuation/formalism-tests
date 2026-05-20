# Stage 6 Complete First Test Bundle

## Purpose

This bundle installs the complete first Stage 6 test set for the current completed Stage 6 candidate fixture.

The Stage 6 theorem basis is the **Admissible Existence Unified Gate**:

```text
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
```

This bundle follows the core-lite principle: it adds no GitHub workflow files and does not require workflow mutation. The tests are placed only under `tests/` and the fixture is placed under `tests/fixtures/`.

## Assumptions

1. The completed Stage 6 candidate set currently contains 10 candidates.
2. The test count is derived from the completed candidate set and from the required Stage 6 invariants implied by those candidates.
3. The existing repository test workflow, if present, can discover normal pytest tests. If not, the tests can be run manually.
4. `validated_decision` and `validation_status` remain reserved for a later receipt-producing validator and are expected to be `null` in this fixture.

## Done Criteria

This bundle is done when:

1. `tests/fixtures/stage6_candidates.json` exists.
2. `tests/test_stage6_unified_gate.py` exists.
3. `README.md` exists in the bundle root.
4. `bundle_manifest.json` exists in the bundle root.
5. No files are added under `.github/workflows/`.
6. `python -m pytest tests/test_stage6_unified_gate.py` passes.

## Verification Result

Local verification result:

```text
94 passed
```

## Installed Files

```text
tests/fixtures/stage6_candidates.json
tests/test_stage6_unified_gate.py
README.md
bundle_manifest.json
```

## Why This Replaces the Smaller First Bundle

The smaller first bundle treated the completed candidate set as 10 direct decision tests only.

This corrected bundle treats the completed candidate set as the source of the full first test surface. It includes:

- fixture identity tests
- component coverage tests
- candidate-set completeness tests
- candidate ID uniqueness tests
- required field tests for each candidate
- expectation/output separation tests for each candidate
- per-candidate Stage 6 decision tests
- IW containment tests for each candidate
- IW width tests for each candidate
- IW breach margin tests
- RE bound tests for each candidate
- RE breach amount tests
- fail-closed routing tests
- RESET_BOUNDARY routing tests
- EVOLVE_BOUNDARY routing tests
- AI Block scope tests
- FinCo chain tests
- component gate consistency tests

## Candidate Coverage

The fixture contains these 10 completed Stage 6 candidates, and all are covered by the test file:

1. `T-AE-UNIFIED-ALLOW-001`
2. `T-AE-UNIFIED-IW-BREACH-001`
3. `T-AE-UNIFIED-RE-BREACH-001`
4. `T-AE-UNIFIED-DUAL-BREACH-001`
5. `T-AE-UNIFIED-RESET-001`
6. `T-AE-UNIFIED-EVOLVE-001`
7. `T-AE-UNIFIED-AI-BLOCK-ALLOW-001`
8. `T-AE-UNIFIED-AI-BLOCK-ESCAPE-001`
9. `T-AE-UNIFIED-FINCO-CHAIN-001`
10. `T-AE-UNIFIED-FINCO-CHAIN-BREAK-001`

## Test Groups

### Fixture Contract Tests

These tests verify that the fixture identifies itself as a Stage 6 candidate fixture, declares the correct theorem basis, preserves the unified gate formula, covers the required components, and declares the new decisions `RESET_BOUNDARY` and `EVOLVE_BOUNDARY`.

### Candidate Completion Tests

These tests verify that the completed Stage 6 candidate set contains exactly the expected candidate IDs and that those IDs are unique.

### Required Field Tests

Each candidate must contain the Stage 6 fields needed for evaluation, including:

- `iw_containment`
- `re_bound`
- `recoverability_score`
- `recoverability_floor`
- `component_gate_results`
- `family_allowed_outcomes`
- `candidate_expected_outcome`
- `expected_decision`
- `validated_decision`
- `validation_status`

### Expectation/Validator Separation Tests

Each candidate must declare an expected decision, but validator-output fields must remain unset:

```text
expected_decision: fixture expectation
candidate_expected_outcome: fixture expectation mirror
validated_decision: validator output, currently null
validation_status: validator output, currently null
```

This preserves the distinction between candidate expectation and future validation receipt output.

### Per-Candidate Decision Tests

Each of the 10 completed candidates is recomputed through the Stage 6 gate and compared against its expected decision.

The current expected decisions are:

```text
T-AE-UNIFIED-ALLOW-001                  ALLOW
T-AE-UNIFIED-IW-BREACH-001              FAIL_CLOSED
T-AE-UNIFIED-RE-BREACH-001              FAIL_CLOSED
T-AE-UNIFIED-DUAL-BREACH-001            FAIL_CLOSED
T-AE-UNIFIED-RESET-001                  RESET_BOUNDARY
T-AE-UNIFIED-EVOLVE-001                 EVOLVE_BOUNDARY
T-AE-UNIFIED-AI-BLOCK-ALLOW-001         ALLOW
T-AE-UNIFIED-AI-BLOCK-ESCAPE-001        FAIL_CLOSED
T-AE-UNIFIED-FINCO-CHAIN-001            ALLOW
T-AE-UNIFIED-FINCO-CHAIN-BREAK-001      FAIL_CLOSED
```

### IW Tests

These tests verify:

- the stored `contained` flag matches computed containment
- `iw_width` equals `iw_max - iw_min`
- stored breach margins match the amount by which the inference window exceeds `A_total`

### RE Tests

These tests verify:

- the stored `within_bound` flag matches computed RE containment
- stored breach amounts match `re_score - re_max`

### Fail-Closed Routing Tests

These tests verify that IW failure and RE failure both route to `FAIL_CLOSED`.

### RESET_BOUNDARY Routing Test

This test verifies the recoverable non-convergence route:

- IW is contained
- RE is bounded
- recoverability is above floor
- convergence fails
- decision is `RESET_BOUNDARY`

### EVOLVE_BOUNDARY Routing Test

This test verifies the governed boundary evolution route:

- IW is contained
- RE is bounded
- recoverability is above floor
- convergence does not fail
- coherence fails
- purpose-convergence test fails
- decision is `EVOLVE_BOUNDARY`

### AI Block Tests

These tests verify both AI Block positive control and AI Block scope violation behavior.

The escape case confirms that attempted capabilities such as `workflow:create`, `credential:acquire`, and `sandbox:escape` force `FAIL_CLOSED`.

### FinCo Chain Tests

These tests verify both FinCo positive control and broken-chain behavior.

The broken-chain case confirms that missing consent, missing access receipt, undefined compensation, undefined revocation, non-evidence-only use, unauthorized entitlement creation, broken chain state, and insufficient recoverability delta force `FAIL_CLOSED`.

### Component Gate Consistency Tests

These tests verify that component gate results only use valid Stage 6 decisions and that total component failure cases contain only `FAIL_CLOSED` component results.

## Run Command

```bash
python -m pytest tests/test_stage6_unified_gate.py
```

Expected result:

```text
94 passed
```

## Core-Lite Compliance

This bundle follows the core-lite principle:

- no new workflows
- no workflow mutation
- no `.github/workflows/` files
- fixture data remains under `tests/fixtures/`
- tests remain under `tests/`
- execution uses existing repository testing infrastructure or manual pytest

## Next Step

After this bundle passes in the repository, the next bundle should add a receipt-producing validator under `tools/` that writes a report to `data/` while preserving fixture expectations separately from validator output.
