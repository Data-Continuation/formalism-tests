# Stage 30 Theorem Proof Map Update

Add this section after Stage 29.

## Stage 30 — Governed Instantiation Packet (*.tar.gz)

Stage 30 validates that the StegVerse core instantiation packet can be generated, hashed, manifested, receipted, and replay-described without becoming installation authority.

Core rule:

```text
The packet is portable evidence of a proposed governed transition, not installation authority.
```

Stage 30 emits:

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

Expected decisions:

```text
ALLOW_PACKET
LEDGER_PACKET
REQUIRE_REVIEW
FAIL_CLOSED
```

Stage 30 establishes:

```text
A governed instantiation packet can be portable.
A governed instantiation packet can be hashed.
A governed instantiation packet can carry manifest, state, policy, node, FinCo, receipt, and replay context.
A governed instantiation packet cannot authorize its own installation.
Node status remains opt-in.
FinCo remains disabled by default.
Leading-dot paths require iosnoperiod mirrors and explicit mappings.
```

Next stage:

```text
Stage 31 — Production Accreditation and Revocation Boundary
```
