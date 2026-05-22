# Stage 24 — Autonomous Test Planning Under Bounded Authority

Stage 24 allows the active work‑entity to generate **test plans** for future stages while remaining within its bounded authority.  A test plan outlines which future stages should be exercised, the risks involved, required artifacts, and the authority boundaries that apply.  The plan must be reviewed before execution.

The fixture demonstrates:

- **Valid test plan:** A well‑formed plan with clear scope, risk classification, required artifacts, and explicit authority boundaries yields `ALLOW_TEST_PLAN`.
- **Review required:** Plans that may impact policy or require clarification trigger `REQUIRE_REVIEW`.
- **Ledger event:** Valid test plans are recorded on the ledger (`LEDGER_TEST_PLAN`).
- **Failure modes:** Missing scope, unauthorized authority, missing policy version, unknown transition classes, or direct execution without approval lead to `FAIL_CLOSED`.

This stage gives `StegVerse‑001` the capacity to propose its own testing roadmap while ensuring that it cannot self‑execute tests without oversight.