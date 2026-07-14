# Formalism Tests Mirror Handoff

## Current source of truth

This file is the handoff source of truth for `Data-Continuation/formalism-tests` until superseded.

## Active goal

Implement executable proof fixtures for denial reachability at the consequence-binding commit boundary.

## Upstream durable source

```text
StegVerse-Labs/admissibility-wiki
  docs/formalisms/denial-reachability-at-commit.md
  static/formalisms/denial-reachability-at-commit.v0.1.json
```

## Required proof cases

```text
1. REACHABLE_DENY
   denial path exists and enforcement prevents consequence binding
   expected: DENY or FAIL_CLOSED with execution prevented

2. UNREACHABLE_DENY
   authorization is recomputed but no deny path remains
   expected: FAIL_CLOSED / INHERITED_AUTHORIZATION

3. COSMETIC_GATING
   a policy result exists but cannot affect the actuator
   expected: FAIL_CLOSED / COSMETIC_GATING

4. LATE_REFUSAL
   deny occurs only after consequence binding
   expected: FAIL_CLOSED / LATE_REFUSAL

5. SPLIT_BOUNDARY_INSUFFICIENCY
   state sufficiency, authority, and enforcement are resolved across separate layers without one effective deny boundary
   expected: FAIL_CLOSED / SPLIT_BOUNDARY_INSUFFICIENCY
```

## Required predicates

```text
ADMISSIBLE
AUTHORITY_CURRENT
STATE_SUFFICIENT
DENIAL_REACHABLE
DENIAL_ENFORCEABLE
```

## Required outputs

```text
machine-readable fixtures
expected outcomes
deterministic verifier
execution-control receipts
continuation report
```

## Authority boundary

```text
Data-Continuation/formalism-tests owns executable proof and test authority.
StegVerse-Labs/admissibility-wiki owns vocabulary and public explanation only.
StegVerse-Labs/Site and GCAT-BCAT-Engine/Publisher are downstream mirrors and must not infer proof from documentation alone.
```

## Completion event

This task is complete when all five cases are executable, deterministic, fail closed where required, and emit receipts proving whether the deny result controlled execution before consequence binding.

## Permitted continuation scope

Add fixtures, validators, expected outcomes, reports, and receipts needed for this goal. Do not add new GitHub workflows solely for this task; integrate with the repository's existing declared-task or validation surfaces.

## Archive posture

This handoff preserves the active goal, ownership, proof cases, authority boundary, outputs, and completion event so the originating conversation can be archived without additional context.
