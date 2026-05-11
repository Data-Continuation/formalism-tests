# Multi-Body Admissibility Boundary Dynamics

Draft StegVerse formalism scaffold for evaluating system-coherent boundaries, purpose convergence, degraded-authority recoverability, governed reset, governed evolution, and multi-body coupling.

## Done Criteria

This bundle is done when:

1. the canonical Markdown section exists at `docs/system-coherent-boundary-dynamics.md`;
2. the evaluator can classify toy boundary scenarios deterministically;
3. fixture scenarios cover ALLOW, RESET_BOUNDARY, EVOLVE_BOUNDARY, DENY, and FAIL_CLOSED;
4. the GitHub Actions workflow runs the evaluator and uploads a report artifact.

## Run Locally

```bash
python tools/evaluate_boundary_dynamics.py tests/fixtures/boundary_scenarios.json
```

## Expected Output

The tool writes:

```text
boundary_dynamics_report.json
```

The report contains one result per scenario with:

```text
scenario_id
recommended_outcome
scores
reasons
```

## Operational Outcomes

```text
ALLOW
DENY
FAIL_CLOSED
RESET_BOUNDARY
EVOLVE_BOUNDARY
```

## Notes

This is not a complete mathematical proof. It is the first deterministic scaffold for testing the concepts defined in the formalism section.
