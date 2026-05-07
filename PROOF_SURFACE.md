# Data Continuation Proof Surface

## Purpose

This proof surface demonstrates the first operational claim of the Data Continuation Formalism:

```text
same data ≠ same continuation admissibility
```

## Core doctrine

Data is not governed because it exists.

Data is governed when it seeks continuation into consequence.

A datum may be admissible as representation while inadmissible as authority, command, actuation, or irreversible consequence.

## Current proof surface

The matching test repository verifies three behaviors:

```text
1. Same data can produce different continuation decisions under different roles.
2. Missing required basis produces FAIL_CLOSED.
3. Consequence mass exceeding legitimacy capacity produces FAIL_CLOSED.
```

## Decision model

```text
ALLOW
  Data may continue into the requested role and transition.

ALLOW_WITH_SIGNOFF
  Data may continue only after the required human/signoff boundary resolves.

DENY
  Data has a known failed block or explicit rejected basis.

FAIL_CLOSED
  Data may not continue because required basis is missing, stale, unknown, or insufficient.
```

## Formal relation

```text
Λ(x) = K·g^α·c^β·t^γ
I(D, r, T, x) = M(D, r, T) - Λ(x)
```

A continuation may proceed only if:

```text
I(D, r, T, x) ≤ 0
and
all required transition blocks resolve
```

## Public claim

```text
Data may exist freely as representation.
Data may continue into consequence only when admissibility resolves at commit.
```

## Repository relationship

```text
Data-Continuation/formalisms
  Defines the ontology and admissibility doctrine.

Data-Continuation/formalism-tests
  Produces executable receipts and a public report.
```

## Proof-surface status

```text
Status: Live initial proof surface
Scope: Primitive role-based continuation decisions
Next: Compound continuation, transition charge, inference-window viability, recoverability floor
```
