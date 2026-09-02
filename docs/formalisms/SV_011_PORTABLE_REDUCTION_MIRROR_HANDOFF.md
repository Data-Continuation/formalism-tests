# SV-011 Portable Reduction Mirror Handoff

## Goal

Define the machine-checkable reduction target for the SV-011 from-scratch entity experiment without implementing the destination entity in this repository.

## Experimental question

After SV-011 is constructed from its first transition element through standing, role escalation, commit-time admission, receipts, boundary operation, reconstruction, and accreditation semantics, what is the smallest installable archive that still preserves every declared governance invariant?

## Required package classes

- `bootstrap_minimal`: smallest verified archive; may retrieve immutable dependencies during installation only when their identities are pinned and verified.
- `offline_self_contained`: archive contains every byte required for installation and self-test; network access must be unnecessary.

## Required measurements

Each package record must preserve:

- compressed byte count
- file count
- dependency count
- exact archive SHA-256
- installation steps
- fresh-destination installation PASS
- canonical self-test receipts

## Canonical self-tests

The portable package must pass all six:

1. admitted capability
2. denied capability
3. stale or unknown basis
4. stopped-chain enforcement
5. replay grants no renewed authority
6. ordered-root reconstruction

## Irreducibility method

A component belongs in the minimum kernel only after this ablation sequence is evidenced:

`remove -> rebuild -> reinstall fresh -> rerun canonical self-tests`

If removing the component does not break a declared invariant, it is not demonstrated irreducible.

## Authority boundary

A package build, workflow PASS, compressed artifact, or successful installation does not independently grant runtime, execution, publication, custody, accreditation, or autonomous authority.

## Installed evaluator surfaces

- `schemas/sv011-portable-reduction-objective.schema.json`
- `tools/check_sv011_portable_reduction_objective.py`
- `tests/test_sv011_portable_reduction_objective.py`

This lane evaluates evidence emitted by `SV-011/entity`; it does not substitute for the destination construction.
