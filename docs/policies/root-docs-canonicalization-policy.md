# Root Docs Canonicalization Policy

## Rule

```text
Build-stage processes must place generated documentation under docs/, not at repository root.
```

## Root Keep List

```text
README.md
README-Plus.md
ARCHITECTURE.md
PRODUCT.md
```

## Canonical Locations

```text
docs/stages/
docs/theorem/
docs/indexes/
docs/roadmaps/
docs/legacy/theorem/
docs/legacy/root-markdown/
docs/legacy/bundles/
```

## Safety Rule

```text
No deletion.
No overwrite.
Move with hash preservation.
Emit report and receipt.
```
