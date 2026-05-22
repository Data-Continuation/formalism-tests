# Stage 18 — Next‑Stage Candidate Generation Under Sandbox Constraint

Stage 18 allows the active work‑entity to **generate candidate artifacts** for future stages, but only inside a controlled sandbox.  The entity may draft fixtures, runners, manifests and documentation; however, it may not install those artifacts directly into the canonical release or bypass governance.

Key conditions enforced by the tests:

- **Sandbox only:** Any attempt to write directly to release files or mutate canonical state results in `FAIL_CLOSED`.
- **Dependency closure:** Candidates must declare and satisfy their dependencies.  Missing or inconsistent dependency closure causes `FAIL_CLOSED`.
- **Scope and authority:** Candidates may not self‑promote, claim canonical authority, or expand their scope beyond declared bounds.
- **Receipts:** Drafts must emit receipts (`LEDGER_CANDIDATE_DRAFT`) capturing the proposed work for later review.

The fixture exercises successful sandbox generation, failure modes such as missing receipts or unauthorized scope, and proper logging of draft candidates.  Passing this stage gives `StegVerse‑001` the ability to prepare future work without compromising the governance boundary.