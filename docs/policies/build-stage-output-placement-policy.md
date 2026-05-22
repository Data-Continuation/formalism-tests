# Build-Stage Output Placement Policy

## Assumptions

1. Build-stage processes should not scatter generated documentation into the repository root.
2. Stage-specific documentation belongs under `docs/`.
3. Root should be reserved for canonical entry points and minimal repo metadata.
4. Cleanup should be governed, report-backed, and non-destructive.
5. This policy does not delete files.

## Done

This policy is done when future build-stage bundles and tasks place documentation into:

```text
docs/stages/
docs/theorem/
docs/indexes/
docs/roadmaps/
docs/site/
docs/legacy/
docs/policies/
```

and avoid placing generated stage documents at repo root.

## Rule

```text
Build-stage processes must place generated documentation under docs/, not at repository root.
```

## Root Policy

Allowed root markdown:

```text
README.md
```

Deprecated root markdown patterns:

```text
THEOREM_PROOF_MAP.md
THEOREM_PROOF_MAP.stage*.md
THEOREM_PROOF_MAP_STAGE*.md
STAGE*.md
STAGE*_*.md
stage*_*.md
*_README.md
```

These should be moved into governed `docs/` locations.

## Canonical Documentation Locations

```text
docs/stages/        stage-specific README and stage proof notes
docs/theorem/       theorem proof maps and theorem manifests
docs/indexes/       task ID index, artifact index, stage index
docs/roadmaps/      roadmap and next-integration plans
docs/site/          Site mirror and Site wiring docs
docs/legacy/        superseded historical docs
docs/policies/      build placement, hygiene, and output policies
```

## Canonical Root Files

Root should usually contain only:

```text
README.md
pyproject.toml
.gitignore
manifest.json
bundle_manifest.json
BUILD_VERIFICATION.json
```

Note: `.gitignore` is shown here with its leading dot because it is a real canonical repository path.

## Cleanup Boundary

```text
Report first.
Plan moves second.
Do not delete.
Do not overwrite canonical docs without explicit review.
```

## Build Process Requirement

Every future stage bundle should use this default placement pattern:

```text
docs/stages/STAGE##_NAME.md
docs/theorem/THEOREM_PROOF_MAP.md
docs/indexes/TASK_ID_INDEX.md
docs/indexes/ARTIFACT_INDEX.md
reports/<machine-readable-report>.json
receipts/<receipt-stream>.jsonl
tools/<runner>.py
tools/tasks/<task-manifest>.json
```

## Correction to Current Repo State

The current root-level stage files are understandable residue from rapid build iteration, but they are not the intended final structure.

They should be migrated through a governed canonicalization task.
