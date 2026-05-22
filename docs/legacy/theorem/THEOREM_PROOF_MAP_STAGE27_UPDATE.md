# Stage 27 Theorem Proof Map Update

Add this section after Stage 26.

## Stage 27 — Discovery-to-Canonical State DB

Stage 27 validates the discovery-first rule.

It produces:

```text
reports/stage27_discovered_state.json
reports/stage27_canonical_state.json
reports/stage27_state_diff.json
reports/stage27_install_plan_candidate.json
reports/stage27_discovery_gap_report.md
receipts/stage27_discovery_receipts.jsonl
```

It establishes:

```text
Discovery may observe.
Discovery may model.
Discovery may compare.
Discovery may classify.
Discovery may propose an install-plan candidate.
Discovery may not install.
```

Canonical rule:

```text
An install plan is a candidate transition, not installation authority.
```

Expected decisions:

```text
ALLOW_DISCOVERY
LEDGER_DISCOVERED_STATE
LEDGER_CANONICAL_DIFF
REQUIRE_REVIEW
FAIL_CLOSED
```

Next stage:

```text
Stage 28 — Canonical Diff and Install Plan Candidate
```
