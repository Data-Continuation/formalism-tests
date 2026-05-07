# Public Proof Surface: Data Continuation

## What this proves

This repository demonstrates that data continuation must be governed by role and transition, not merely by data content.

The first proof surface verifies:

```text
same data
same system state
different role
different continuation decision
```

## Why that matters

Most automated systems treat data output as if the main question is whether the data is correct, useful, explainable, or logged.

Data Continuation asks a different question:

```text
What is this data being allowed to become?
```

The same data can be:

```text
safe as context
conditional as a recommendation
inadmissible as autonomous action
```

## Verified behavior

The current receipt set verifies:

```text
ALLOW
ALLOW_WITH_SIGNOFF
FAIL_CLOSED
```

The fail-closed cases are not failures of the test system.

They are expected governance outcomes.

## Continuation rule

```text
No admissibility at commit means no continuation.
```

## Proof artifacts

```text
reports/sample_receipts.jsonl
reports/continuation_report.md
```

## Reader checklist

A reader should be able to inspect the report and answer:

```text
What data attempted continuation?
What role was assigned?
What transition class was used?
Was consequence mass supported by legitimacy capacity?
Which required blocks passed, failed, or were missing?
Why was the decision ALLOW, ALLOW_WITH_SIGNOFF, DENY, or FAIL_CLOSED?
```

## Current limitation

This proof surface is intentionally minimal.

It does not yet prove compound continuation, inference-window collapse, transition charge, or recoverability constraints.

Those are Stage 3+ proof surfaces.
