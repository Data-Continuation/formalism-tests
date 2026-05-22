# Stage 21 — Canonical Upgrade Replay and Continuity Receipt

Stage 21 validates that any proposed release upgrade can be **replayed** from the previous canonical state and produce a continuous chain of evidence.  The work‑entity must prove that it can reconstruct both the source and target releases, the delta manifest, and the upgrade process itself without altering canonical authority.

Key test scenarios include:

- **Successful replay:** The source release, target release, and delta manifest are all present and hash‑match, resulting in `ALLOW_CANONICAL_UPGRADE_REPLAY`.
- **Failure:** Missing source/target releases, missing delta manifests, mismatched hashes, unauthorized authority, or missing receipts lead to `FAIL_CLOSED`.
- **Ledger recording:** When continuity is demonstrated, a `LEDGER_REPLAY_CONTINUITY` event is emitted to document the upgrade.

The tests ensure that upgrades are provably reproducible and that any missing piece of evidence results in a fail‑closed outcome.  Replay alone cannot grant canonical authority; it merely proves continuity of the proposed upgrade.