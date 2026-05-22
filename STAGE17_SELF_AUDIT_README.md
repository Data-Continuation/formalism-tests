# Stage 17 — Active Work‑Entity Self‑Audit and Drift Detection

This stage introduces **self‑audit** and **drift detection** for the active governed work‑entity `StegVerse‑001`.  To maintain legitimacy, the work‑entity must periodically verify that its own authority, scope, dependency closure, policy version, and release lineage have not drifted from the declared state.  A successful self‑audit produces an `ALLOW_SELF_AUDIT` decision.  When drift is detected the system records a `LEDGER_DRIFT_EVENT` and may require additional governance review (`REQUIRE_REVIEW`).  If critical evidence is missing or an unauthorized authority is detected the transition fails closed (`FAIL_CLOSED`).

The accompanying fixture covers a variety of scenarios:

- **Valid audit:** All required evidence is present and the entity remains within its authority, producing `ALLOW_SELF_AUDIT`.
- **Drift detected:** Changes in release lineage or dependency closure trigger a `LEDGER_DRIFT_EVENT`.
- **Missing evidence:** Cases where the self‑audit lacks required receipts or scope declarations result in `FAIL_CLOSED`.
- **Review required:** Ambiguous or incomplete evidence triggers `REQUIRE_REVIEW`.

These tests ensure that a governed work‑entity cannot silently drift from its authorized state and must either prove continuity or fail closed.