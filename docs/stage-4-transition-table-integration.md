# Stage 4 Transition Table Integration

## Purpose

Stage 4 integrates the Stage 3 continuation proof surface into the transition table construction.

The key shift is:

```text
A transition type is not only a label.
A transition type is an admissibility contract.
```

## Public proof claim

```text
A transition class is valid only if its admissibility contract specifies the conditions under which the transition may bind consequence.
```

## Files

```text
tests/transition_table_cases.json
src/transition_table_gate.py
reports/transition_table_receipts.jsonl
reports/transition_table_report.md
```

## Run

```bash
python src/transition_table_gate.py
```

## Expected outputs

```text
reports/transition_table_receipts.jsonl
reports/transition_table_report.md
```

## Transition-class contract fields

```text
transition_id
transition_name
transition_family
theorem_basis
role
consequence_mass
legitimacy_capacity_required
recoverability_floor
recoverability_score
inference_window_minimum
inference_window_width
commit_time_state_required
pre_commit_state_hash
commit_state_hash
replay_semantics
boundary_behavior
multi_body_coupling_class
allowed_outcomes
```

## Interpretation

Stage 4 verifies that tested continuation theorems can be represented as transition-table classes with explicit admissibility contracts.

This turns the transition table from a descriptive taxonomy into an executable governance surface.

A row in the transition table is not simply a named transition. It is a governed consequence-binding class with defined admissibility requirements.

## Connection to system-coherent boundaries

Stage 4 prepares the bridge into:

```text
Multi-Body Admissibility
System-Coherent Boundary Dynamics
Purpose-Convergence Test
Degraded-Authority Recoverability Test
Governed Boundary Reset
Governed Boundary Evolution
```

The next stage should add transition classes that explicitly exercise boundary reset, boundary evolution, system-coherence failure, and purpose-convergence failure.
