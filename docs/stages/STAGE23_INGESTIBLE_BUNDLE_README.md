# Stage 23 — Ingestion Compatibility and Bundle Custody

Stage 23 introduces rules for creating **ingestible bundles** of proof artifacts.  Such bundles allow other systems to install or analyze a release in a controlled manner while preserving custody, lineage, and integrity.

Important aspects covered in the tests:

- **Valid bundle:** A bundle with a valid manifest, correct hashes, and no unauthorized files is accepted (`ALLOW_INGESTIBLE_BUNDLE`).
- **Custody recording:** Proper custody events are logged (`LEDGER_BUNDLE_CUSTODY`) to ensure chain of custody.
- **Quarantine:** Bundles missing policy scope or containing unauthorized files are quarantined (`QUARANTINE_BUNDLE`).
- **Failure modes:** Missing manifests, hash mismatches, missing receipts, or unauthorized canonical claims result in `FAIL_CLOSED`.

The stage ensures that any exported bundle can be safely ingested by downstream tools without compromising the integrity of the proof surface and that questionable bundles are either quarantined or failed closed.