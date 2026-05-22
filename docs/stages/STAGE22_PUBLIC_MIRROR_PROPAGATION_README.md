# Stage 22 — Multi‑Repo / Multi‑Surface Propagation Boundary

Stage 22 governs the **propagation of proof artifacts** from the authoritative `formalism‑tests` repository to public mirrors such as Site or other repositories.  Propagation is permitted only when the content matches the canonical source, the hashes align, and no unauthorized authority is claimed.

The fixture includes cases where:

- **Propagation succeeds:** All checks pass and the proof surface is mirrored without claiming canonical authority (`ALLOW_PUBLIC_MIRROR_PROPAGATION`).
- **Hash or content mismatches:** Differences between the source and mirror cause `FAIL_CLOSED` outcomes.
- **Missing receipts or manifests:** The absence of required evidence results in `FAIL_CLOSED`.
- **Unauthorized canonical claims:** Attempts to elevate the mirror to proof authority or mutate canonical records cause `FAIL_CLOSED`.
- **Ledger sync:** Successful mirror synchronizations are recorded (`LEDGER_MIRROR_SYNC`) to provide auditable proof of propagation.

By constraining propagation, Stage 22 maintains a clear boundary between the proof authority repository and public mirrors and prevents accidental transfer of authority.