# StegClaw Evaluation Handoff

## Purpose

This document records formalism-tests target-side evaluation handoff support for StegClaw standing, ingestion, outbound, and target-binding artifacts.

Formalism-tests is currently bound as:

```text
GCAT/BCAT evaluator target
proof-only authority
```

## Declaration

```text
formalism_tests/stegclaw_evaluation_handoff.json
```

## Validator

```text
python tools/validate_stegclaw_evaluation_handoff.py
```

Expected result:

```text
ALLOW
```

The validator writes:

```text
reports/stegclaw_evaluation_handoff.json
```

## Workflow artifact coverage

The workflow path is displayed here without the leading dot: `github/workflows/stegclaw-evaluation-handoff.yml`. The actual path is `.github/workflows/stegclaw-evaluation-handoff.yml`.

The workflow uploads:

```text
reports/stegclaw_evaluation_handoff.json
```

inside the `stegclaw-evaluation-handoff` artifact.

## Boundary

This evaluation handoff is local-only. It validates that the expected StegClaw handoff artifacts are named and that formalism-tests remains proof-only, non-installing, and non-production-authorizing.

## Next step

Inspect the next visible `stegclaw-evaluation-handoff` workflow artifact and confirm the evaluation report is present.
