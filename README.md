# formalism-test-harness

Reusable v001 harness for Data-Continuation / StegVerse formalism test repos.

## Assumptions

1. This is a reusable repo-root bundle.
2. It is local-first and deterministic.
3. It records original receipts, plays them back, reconstructs receipts conservatively, compares original vs reconstructed events, and scores confidence.
4. It includes `data-continuation.v1` and `gcat-bcat.v1` adapters.
5. It treats GitHub Ubuntu, StegVerse dry-run, and LLM Adapter Gate as comparable sandbox models.
6. It does not require live API keys and does not mutate production repos.

## Done Criteria

```text
pytest -q
formalism-harness selftest --out out
formalism-harness run examples/data_continuation_allow.json --out out
formalism-harness run examples/gcat_bcat_allow.json --out out_gcat
formalism-harness verify out/original_receipts.jsonl
formalism-harness playback out/original_receipts.jsonl --out out
formalism-harness reconstruct out --out out/reconstruction
formalism-harness compare out/original_receipts.jsonl out/reconstruction/reconstructed_receipts.jsonl --out out
formalism-harness confidence out --out out
formalism-harness sandbox-report out --out out
```

## Standard artifacts

```text
ingestion_report.json
formalism_result.json
tvc_result.json
cge_result.json
sandbox_result.json
original_receipts.jsonl
artifact_manifest.json
playback_report.json
reconstruction/reconstructed_receipts.jsonl
reconstruction/reconstruction_report.json
receipt_comparison.json
confidence_report.json
sandbox_model_report.json
```

## GitHub Actions

Actual workflow paths:

```text
.github/workflows/test.yml
.github/workflows/sandbox-credibility-run.yml
```
