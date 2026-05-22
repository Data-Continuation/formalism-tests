# Task ID Index

## Stage Task IDs

| Stage | Task ID |
|---:|---|
| 17 | `stage17_self_audit_tests` |
| 18 | `stage18_sandbox_candidate_generation_tests` |
| 19 | `stage19_candidate_review_loop_tests` |
| 20 | `stage20_release_candidate_assembly_tests` |
| 21 | `stage21_canonical_upgrade_replay_tests` |
| 22 | `stage22_public_mirror_propagation_tests` |
| 23 | `stage23_ingestible_bundle_tests` |
| 24 | `stage24_test_plan_tests` |
| 25 | `stage25_entity_charter_tests` |
| 26 | `stage26_stegverse001_testing_loop_tests` |
| 27 | `stage27_discovery_to_canonical_state_tests` |
| 28 | `stage28_canonical_diff_install_plan_tests` |
| 29 | `stage29_node_status_finco_eligibility_tests` |
| 30 | `stage30_governed_instantiation_packet_tests` |
| 31 | `stage31_production_accreditation_revocation_tests` |

## Post-Stage-31 Integration Task IDs

| Task | Purpose |
|---|---|
| `discover_core_lite_state` | Discover current core-lite repo state and generate capability/diff/install-plan candidate reports. |
| `build_production_candidate_review_packet` | Build a non-installing production-candidate review packet from discovery output. |
| `export_master_record_candidate` | Export master-record-compatible event bundle and receipts. |

## Runner Pattern

```bash
python tools/run_declared_tasks.py tools/tasks/post_stage31_integration_tasks.json --task-id <task_id>
```
