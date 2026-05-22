# README-Plus

## Status

```text
repository: Data-Continuation/formalism-tests
document_type: supplemental_root_readme
purpose: bundle intake shield, current supplemental status, and repo hygiene note
status: active
updated_on: 2026-05-22
```

## Why This File Exists

`README-Plus.md` exists because bundle-generated `README.md` files were repeatedly included at bundle root.

To avoid overwriting the primary repository `README.md`, the incoming bundle README was manually renamed to:

```text
README-Plus.md
```

That protected the main repo README, but it also caused a different problem:

```text
README-Plus.md was repeatedly overwritten by later bundle README files.
```

This file now records the intended role of `README-Plus.md` so future bundles do not accidentally treat it as a disposable bundle README.

---

# Correct Rule Going Forward

## Primary Repo README

```text
README.md
```

Role:

```text
canonical public entry point for the repository
```

It should not be overwritten by bundle-level README files.

## Supplemental Root README

```text
README-Plus.md
```

Role:

```text
owner-defined supplemental repo status and bundle-intake note
```

It should not be overwritten by bundle-level README files.

## Bundle README Files

Bundle-specific README files should go under:

```text
docs/bundles/
```

Recommended pattern:

```text
docs/bundles/<bundle-name>-README.md
```

Example:

```text
docs/bundles/stage31-production-accreditation-revocation-README.md
docs/bundles/post-stage31-integration-README.md
docs/bundles/root-docs-bulk-canonicalization-README.md
```

---

# Current Repo Status

```text
Stages 1–31: PASSED
Initial 31-stage roadmap: COMPLETE
StegVerse-001 / Beta_Orionis: active governed work-entity
Production meaning: accredited participation, not sovereign authority
Site role: public mirror only
Proof authority: formalism-tests
```

The repository has moved from early continuation tests into a completed 31-stage proof roadmap covering:

```text
data-role admissibility
compound continuation
commit-time sufficiency
replay non-reversal
unified AE gate
StegVerse-001 governed work-entity operation
discovery-to-canonical state modeling
install-plan candidate generation
optional node status
FinCo eligibility
governed instantiation packets
production accreditation and revocation
```

---

# Current Core Rules

```text
same data does not imply same continuation admissibility
local allow plus local allow does not imply composite allow
pre-commit allow does not imply commit-time allow after state drift
replay reconstructs consequence state but cannot reverse consequence
ALLOW(u) iff IW_tau(S,u) subset A_total AND RE(S -> Phi(S,u)) <= RE_max
Discovery observes, models, compares, classifies, and proposes. Discovery does not install.
An install plan is a candidate transition, not installation authority.
Core installation does not imply node participation.
Node participation does not imply FinCo eligibility.
The packet is portable evidence of a proposed governed transition, not installation authority.
Production means accredited participation, not sovereign authority.
```

---

# Current Documentation Placement Rule

Generated documentation should not accumulate at repository root.

Root may keep:

```text
README.md
README-Plus.md
pyproject.toml
.gitignore
manifest.json
bundle_manifest.json
BUILD_VERIFICATION.json
```

Generated documentation belongs under:

```text
docs/stages/
docs/theorem/
docs/indexes/
docs/roadmaps/
docs/site/
docs/bundles/
docs/legacy/
docs/policies/
```

---

# Bundle README Handling

Future bundles should avoid a root `README.md` unless the bundle is explicitly intended to replace the repo README.

Preferred bundle README placement:

```text
docs/bundles/<bundle-name>-README.md
```

If a downloadable standalone README is needed for ChatGPT delivery, the downloadable file may have a descriptive name such as:

```text
POST_STAGE31_INTEGRATION_README.md
SITE_COLOR_PRESERVING_WIRING_README.md
BUILD_STAGE_DOCS_TO_DOCS_POLICY_README.md
```

But inside the repo bundle, it should be placed under:

```text
docs/bundles/
```

not at root.

---

# Current Required Indexes

The repo should maintain:

```text
docs/indexes/TASK_ID_INDEX.md
docs/indexes/ARTIFACT_INDEX.md
docs/theorem/THEOREM_PROOF_MAP.md
```

The root-level `THEOREM_PROOF_MAP.md`, if present, should either be intentionally preserved as a compatibility copy or moved to:

```text
docs/theorem/THEOREM_PROOF_MAP.md
```

The preferred canonical location is:

```text
docs/theorem/THEOREM_PROOF_MAP.md
```

---

# Next Integration Work

The current post-Stage-31 workstream is:

```text
1. Canonicalize root docs into docs/.
2. Update THEOREM_PROOF_MAP.md under docs/theorem/.
3. Build task ID and artifact indexes under docs/indexes/.
4. Run discovery against current core-lite state.
5. Prepare production-candidate review packet.
6. Harden master-record export.
7. Keep all generated documentation out of root unless explicitly approved.
```

---

# Boundary

```text
README.md is the canonical public repo entry point.
README-Plus.md is a protected supplemental owner file.
Bundle README files belong under docs/bundles/.
Generated documentation belongs under docs/.
No bundle should silently overwrite README.md or README-Plus.md.
```
