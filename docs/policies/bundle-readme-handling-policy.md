# Bundle README Handling Policy

## Rule

```text
Bundle-specific README files must not overwrite README.md or README-Plus.md.
```

## Root README Files

The root may contain:

```text
README.md
README-Plus.md
```

`README.md` is the canonical public repo entry point.

`README-Plus.md` is the owner-created supplemental status and bundle-intake shield.

## Bundle README Placement

Bundle-specific README files belong under:

```text
docs/bundles/
```

Use descriptive names:

```text
docs/bundles/<bundle-name>-README.md
```

## Why This Policy Exists

Previous bundles included root-level `README.md` files.

The owner renamed those files to `README-Plus.md` to avoid overwriting the main repository README. That protected `README.md`, but later bundle READMEs overwrote `README-Plus.md`.

This policy prevents both problems.

## Future Bundle Rule

Every future bundle should use:

```text
docs/bundles/<bundle-name>-README.md
```

and should only include root `README.md` or root `README-Plus.md` when the user explicitly asks for a full root file replacement.

## Boundary

```text
Do not silently overwrite root README.md.
Do not silently overwrite root README-Plus.md.
Do not place generated bundle documentation at root.
```
