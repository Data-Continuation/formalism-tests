# SV-011 Commit-Zero Bootstrap Handoff

## Goal
Provide a deterministic Phase-0 file tree for the empty `SV-011/entity` destination.

## Boundary
This is a bootstrap template and validator. It is not the destination entity and grants no runtime or autonomous authority.

## Deterministic contents
The builder emits:
- canonical mirror handoff
- README
- E0 transition element
- external entity-registration binding
- Stage-25 charter binding
- exact canonical source pins
- authority-false initial boundary
- transition-ledger contract
- transition-ledger emitter
- commit-zero manifest with E0 SHA-256

The ledger emitter is the only Python executable in the generated destination tree. No inference, transport, boundary runtime, worker, tool, or consequence executor is present.

## Exit test
The test requires all authority flags false, runtime/boundary runtime absent, consequence path unreachable, nine source pins present, and exactly one Python executable: the ledger emitter.
