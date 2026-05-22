# README-Plus Update Bundle

## Assumptions

1. `README-Plus.md` was created by the owner to protect the primary repo `README.md` from repeated bundle README overwrites.
2. `README-Plus.md` itself was then overwritten repeatedly by later bundle README files.
3. `README-Plus.md` should now be treated as a protected supplemental root file unless the owner explicitly moves it.
4. Future bundle README files should be placed under `docs/bundles/`, not root.
5. This bundle intentionally updates `README-Plus.md`.

## Done

This bundle is done when the repo contains:

```text
README-Plus.md
docs/policies/bundle-readme-handling-policy.md
data/root_docs_canonicalization_policy_patch.json
reports/readme_plus_update_report.json
receipts/readme_plus_update_receipts.jsonl
```

## What Changed

This bundle updates `README-Plus.md` into a stable supplemental status file that explains:

```text
why README-Plus.md exists
why bundle README files should not overwrite it
current Stage 1–31 status
current proof boundaries
future bundle README placement
```

## Future Rule

```text
Bundle-specific README files belong under docs/bundles/.
Do not silently overwrite README.md.
Do not silently overwrite README-Plus.md.
```

## Boundary

This bundle updates documentation only.

It does not run discovery.

It does not install core-lite.

It does not grant production authority.
