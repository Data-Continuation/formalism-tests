# Stage 32–34: Admissibility-Space Formalism Tests

## Purpose

Stages 32–34 extend the formalism-test surface from existing governance and continuation tests into admissibility-space computation.

## Stage 32 — Admissibility-Space Coordinates

Defines measurable coordinate vectors for decision classes:

```text
ALLOW        = interior admissible region
DENY         = coherent exterior boundary crossing
SANDBOX      = bounded search shell
REVIEW       = observability-deficit shell
FAIL_CLOSED  = coherence collapse
QUARANTINE   = isolated preservation state
```

Outputs:

```text
reports/stage32_admissibility_space_report.json
reports/stage32_admissibility_space_receipts.jsonl
```

## Stage 33 — Transition Graph as Geometric Structure

Defines the bundle/candidate/task/receipt graph as a directed graph over admissibility-space.

Discovery becomes constrained shortest-path computation over receipt-bound admissible edges.

Outputs:

```text
reports/stage33_transition_graph_geometry_report.json
reports/stage33_transition_graph_geometry_receipts.jsonl
```

## Stage 34 — Repair as Nearest-Admissible-Transition

Defines repair as nearest admissible transition search. Sandbox becomes the bounded repair search space. Quarantine preserves failed states for future metric computation.

Outputs:

```text
reports/stage34_repair_nearest_admissible_transition_report.json
reports/stage34_repair_nearest_admissible_transition_receipts.jsonl
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage32_to_34_admissibility_space_tasks.json
```

Run one stage:

```bash
python tools/run_declared_tasks.py tools/tasks/stage32_to_34_admissibility_space_tasks.json --task-id stage32_admissibility_space_coordinates_tests
python tools/run_declared_tasks.py tools/tasks/stage32_to_34_admissibility_space_tasks.json --task-id stage33_transition_graph_geometry_tests
python tools/run_declared_tasks.py tools/tasks/stage32_to_34_admissibility_space_tasks.json --task-id stage34_repair_nearest_admissible_transition_tests
```

## Integration Direction

`Data-Continuation/formalism-tests` is the proof authority.

`StegVerse-002/core-lite` should later consume these report and receipt surfaces as computational formalism inputs during ingestion, Transition Table resolution, and CGE admissibility checks.
