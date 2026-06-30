# Formalism-Tests Mirror Handoff

This file is the source of truth for continuing `Data-Continuation/formalism-tests` work across sessions.

## Current goal

Install target-side evaluation handoff support for StegClaw standing and transition artifacts.

## Current version

```text
0.1.0-stegclaw-evaluation-handoff
```

## Current status

```text
MIRROR_HANDOFF_PRESENT
STEGCLAW_EVALUATION_HANDOFF_PENDING
LOCAL_ONLY
```

## Source-of-truth documents

```text
docs/FORMALISM_TESTS_MIRROR_HANDOFF.md
```

## Bound upstream source

```text
repo:Data-Continuation:StegClaw
```

## Expected upstream artifact names

```text
standing_envelope.json
standing_receipt.json
ingestion_candidate.json
ingestion_candidate_receipt.json
outbound_envelope.json
outbound_receipt.json
live_integration_manifest.json
```

## Boundary rules

Formalism-tests evaluates admissibility evidence. It does not install StegClaw output, mutate target repos, or grant production authority.

StegClaw artifacts may enter here only as evaluation candidates.

## Next build candidate

Install a StegClaw evaluation declaration and local validator that confirms the expected upstream artifact contract and preserves proof-only authority.

## Handoff instruction

Continue from this file before relying on prior chat context.
