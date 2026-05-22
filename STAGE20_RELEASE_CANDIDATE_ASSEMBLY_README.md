# Stage 20 — Release Candidate Assembly From Accepted Candidates

Stage 20 governs the **assembly of a release candidate** from previously accepted Stage 19 outputs.  Only candidates that have been accepted after review, have closed dependencies, and possess complete receipt chains may be assembled into a new release candidate.

Highlights of the test logic:

- **Success path:** A release candidate assembled with correct manifest, receipts, and lineage produces `ALLOW_RELEASE_CANDIDATE_ASSEMBLY`.
- **Failure modes:** Missing receipts, stale candidates, incomplete dependency closure, invalid manifests, or mismatched hashes result in `FAIL_CLOSED`.
- **Ledger event:** A successful assembly is recorded on the ledger (`LEDGER_RELEASE_CANDIDATE_ASSEMBLY`) to ensure future traceability.

By enforcing these conditions, Stage 20 ensures that only properly reviewed and documented work moves toward canonical status and that improper assemblies are halted.