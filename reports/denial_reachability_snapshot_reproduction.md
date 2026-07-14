# Denial Reachability Snapshot Reproduction

## Result

Both declared tasks passed on a connector-materialized snapshot of the committed repository sources:

```text
denial_reachability_commit_boundary_tests: PASS
verify_denial_reachability_artifacts: PASS
```

## Verified outputs

```text
proof cases: 5
passed: 5
failed: 0
proof report canonical SHA-256: 8c2c460e3d7ae790a4f5fc347e44f9e91615db8b1913ee98c893e3071a5fb284
generated report file SHA-256: f5a07da05497bdd8d85bd60e43ceb5d043eac656bad2f873a6d9aee2d65f95be
generated receipts file SHA-256: 9f1c0dc5463dc7396addf7a62147b8beb33f818b67add8f41bc069c96cef2953
byte equivalence to baseline: true
late-refusal non-prevention preserved: true
```

## Discovered defect

The initial artifact-verification task failed because the verifier compared raw file-byte hashes against canonical JSON hashes stored in the proof report.

The verifier was corrected to distinguish:

```text
canonical document hashes
raw file-byte hashes
```

The task now also verifies generated report and receipt bytes against `tests/fixtures/denial_reachability_artifact_baseline.json`.

## Evidence

```text
receipts/denial_reachability_connector_snapshot_run.json
```

## Boundary

This reproduction is durable deterministic evidence, but it is not represented as a GitHub Actions run or repository-checkout run. Canonical execution remains pending in a repository checkout or an existing CI execution surface.
