# Stage 30 — Governed Instantiation Packet

## Assumptions

1. Stages 1–29 have passed.
2. Stage 30 produces and validates a portable `*.tar.gz` governed instantiation packet.
3. The packet is not installation authority.
4. The packet is portable evidence of a proposed governed transition.
5. Node status and FinCo remain opt-in and disabled by default unless explicitly declared and validated.
6. Any leading-dot canonical paths must be mirrored under `iosnoperiod/` with explicit path mappings.

## Done

Stage 30 is done when:

```text
tools/run_stage30_governed_instantiation_packet_tests.py
```

returns success and emits:

```text
reports/stage30_governed_instantiation_packet_report.json
reports/stage30_packet_manifest_validation_report.json
dist/stage30/stegverse-core-instantiation.tar.gz
dist/stage30/stegverse-core-instantiation.sha256
dist/stage30/stegverse-core-instantiation.manifest.json
dist/stage30/stegverse-core-instantiation.receipt.json
dist/stage30/stegverse-core-instantiation.replay.json
receipts/stage30_instantiation_packet_receipts.jsonl
```

## Task ID

```text
stage30_governed_instantiation_packet_tests
```

## Run

```bash
python tools/run_declared_tasks.py tools/tasks/stage30_instantiation_packet_tasks.json --task-id stage30_governed_instantiation_packet_tests
```

## Core rule

```text
The packet is portable evidence of a proposed governed transition, not installation authority.
```

## What Stage 30 validates

Stage 30 validates that a governed instantiation packet contains:

```text
manifest
authority boundary
policy scope
node status default
FinCo default
discovered state
canonical state
state diff
install-plan candidate
payload
schemas
reports
receipts
replay data
sha256 hash
iosnoperiod mappings
```

## What Stage 30 does not do

Stage 30 does not install the packet.

Stage 30 does not make `core-lite` production.

Stage 30 does not activate node status.

Stage 30 does not enable FinCo participation.

Stage 30 does not create entitlement.

Stage 30 does not grant StegVerse-001 sovereign authority.

## Next stage

```text
Stage 31 — Production Accreditation and Revocation Boundary
```
