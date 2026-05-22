# Artifact Index

## Standard Artifact Directories

| Directory | Purpose |
|---|---|
| `reports/` | Human-readable and machine-readable validation reports. |
| `receipts/` | JSONL receipt streams for proof events and decisions. |
| `dist/` | Built packets, release candidates, hashes, and replay assets. |
| `docs/` | Roadmap, status, task, artifact, and theorem documentation. |
| `tests/fixtures/` | Declarative test cases for stage validation. |
| `tools/tasks/` | Declared task manifests. |

## Stage 26–31 Expected Artifacts

| Stage | Report | Receipts |
|---:|---|---|
| 26 | `reports/stage26_stegverse001_testing_loop_report.json` | `receipts/stage26_stegverse001_testing_loop_receipts.jsonl` |
| 27 | `reports/stage27_discovery_to_canonical_state_report.json` | `receipts/stage27_discovery_receipts.jsonl` |
| 28 | `reports/stage28_canonical_diff_install_plan_report.json` | `receipts/stage28_install_plan_receipts.jsonl` |
| 29 | `reports/stage29_node_status_finco_eligibility_report.json` | `receipts/stage29_node_finco_receipts.jsonl` |
| 30 | `reports/stage30_governed_instantiation_packet_report.json` | `receipts/stage30_instantiation_packet_receipts.jsonl` |
| 31 | `reports/stage31_production_accreditation_revocation_report.json` | `receipts/stage31_accreditation_receipts.jsonl` |

## Stage 30 Packet Artifacts

```text
dist/stage30/stegverse-core-instantiation.tar.gz
dist/stage30/stegverse-core-instantiation.sha256
dist/stage30/stegverse-core-instantiation.manifest.json
dist/stage30/stegverse-core-instantiation.receipt.json
dist/stage30/stegverse-core-instantiation.replay.json
```

## Post-Stage-31 Integration Artifacts

```text
reports/core_lite_discovered_state.json
reports/core_lite_discovery_gap_report.md
reports/core_lite_state_diff.json
reports/core_lite_install_plan_candidate.json
reports/production_candidate_review_report.md
reports/master_record_export_report.json
dist/production-candidate-review-packet.tar.gz
dist/production-candidate-review-packet.sha256
dist/master-record-export.json
receipts/core_lite_discovery_receipts.jsonl
receipts/production_candidate_review_receipts.jsonl
receipts/master_record_export_receipts.jsonl
```
