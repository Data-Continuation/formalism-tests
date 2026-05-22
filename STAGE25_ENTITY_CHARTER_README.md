# Stage 25 — Active Work‑Entity Operating Charter

Stage 25 culminates the early governance roadmap by formalizing an **operating charter** for `StegVerse‑001`.  The charter codifies the entity’s identity, authority boundaries, policy scope, receipt requirements, review requirements, shutdown conditions, and fail‑closed triggers.  Without a valid charter, the entity cannot continue to operate.

The test cases demonstrate:

- **Charter acceptance:** When identity, authority limits, policy scope, receipts, review and shutdown rules are all declared, the charter is accepted (`ALLOW_ENTITY_CHARTER`).
- **Ledger recording:** An accepted charter is logged on the ledger (`LEDGER_ENTITY_CHARTER`) for permanence.
- **Failure modes:** Missing identity, authority boundaries, policy scope, receipt requirements, fail‑closed conditions, transition table binding, or review requirements cause `FAIL_CLOSED`.  Unauthorized canonical claims are also failed closed.

By passing Stage 25, `StegVerse‑001` transitions from a provisional governed work‑entity into one with a durable and auditable charter, paving the way for more advanced governance in subsequent stages.