# Formalism Test Harness Architecture

## Pipeline

```text
case -> ingestion -> formalism adapter -> TVC -> CGE -> sandbox
     -> original receipts -> playback -> reconstruction
     -> receipt comparison -> confidence report -> sandbox model report
```

## Confidence dimensions

```text
receipt_chain_integrity
artifact_hash_alignment
formalism_decision_alignment
tvc_alignment
cge_alignment
sandbox_decision_alignment
playback_alignment
reconstruction_alignment
missing_data_penalty
unexpected_mutation_penalty
unexplained_gap_penalty
```
