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

## Boundary

This evaluation handoff is local-only. It validates that the expected StegClaw handoff artifacts are named and that formalism-tests remains proof-only, non-installing, and non-production-authorizing.

## Next step

Add workflow artifact coverage for the StegClaw evaluation handoff validator.
