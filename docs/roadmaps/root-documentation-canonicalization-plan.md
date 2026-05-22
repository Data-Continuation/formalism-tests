# Root Documentation Canonicalization Plan

## Assumptions

1. Existing root-level stage documents are historical artifacts, not final root structure.
2. The cleanup should move documentation, not delete it.
3. Root `README.md` may remain as the primary repo entry point.
4. `THEOREM_PROOF_MAP.md` should be canonicalized under `docs/theorem/`.
5. Stage-specific files should be canonicalized under `docs/stages/`.

## Done

Canonicalization is done when:

```text
root contains only the repo entry README and non-doc metadata/source entrypoints
stage documents live under docs/stages/
theorem documents live under docs/theorem/
indexes live under docs/indexes/
legacy fragments live under docs/legacy/
a move plan report exists
a receipt exists
```

## Proposed Move Classes

### Stage docs

Move:

```text
STAGE*.md
STAGE*_*.md
stage*_*.md
```

to:

```text
docs/stages/
```

### Theorem maps

Move duplicate or superseded files matching:

```text
THEOREM_PROOF_MAP.stage*.md
THEOREM_PROOF_MAP_STAGE*.md
theorem_map_stage*.md
stage*_theorem_manifest*.md
```

to:

```text
docs/legacy/theorem/
```

Canonical theorem map should live at:

```text
docs/theorem/THEOREM_PROOF_MAP.md
```

### Indexes

Move or create indexes at:

```text
docs/indexes/TASK_ID_INDEX.md
docs/indexes/ARTIFACT_INDEX.md
```

### Bundle residue

Move bundle-specific planning files that are not active manifests to:

```text
docs/legacy/bundles/
```

Examples:

```text
path_mappings.json
bundle-manifest.json
```

Only after review.

## Non-Destructive Rule

```text
No deletion.
No silent overwrite.
Every move is recorded in a report and receipt.
```
