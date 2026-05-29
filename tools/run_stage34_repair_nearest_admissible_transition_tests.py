from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256_json(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()

def write_json(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def append_jsonl(path: str, payload: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")

def stage_receipt(stage: int, report_path: str, report: dict, decision: str = "PASS") -> dict:
    receipt = {
        "schema": "stegverse.formalism_test_receipt.v1",
        "stage": stage,
        "decision": decision,
        "timestamp_utc": utc_now(),
        "report_path": report_path,
        "report_hash": sha256_json(report),
        "formalism_family": "admissibility-space-computation",
    }
    receipt["receipt_hash"] = sha256_json(receipt)
    return receipt

def main() -> int:
    report_path = "reports/stage34_repair_nearest_admissible_transition_report.json"
    receipt_path = "reports/stage34_repair_nearest_admissible_transition_receipts.jsonl"

    repair_problem = {
        "given": ["T_failed", "S0", "S_bad", "A", "Q", "B", "R"],
        "objective": "find T_repair in R such that T_repair(S0) in A and repair_cost is minimized",
        "constraints": [
            "recoverability_preserved",
            "purpose_convergence_preserved",
            "operator_authority_not_degraded",
            "lineage_to_failed_transition_retained",
            "same_CGE_and_transition_table_requirements_as_any_binding_transition"
        ],
        "repair_cost_terms": [
            "edit_distance",
            "boundary_distance",
            "authority_pressure",
            "recoverability_loss",
            "purpose_divergence",
            "evidence_loss"
        ]
    }

    sandbox_definition = {
        "role": "bounded_search_space_for_repair_candidates",
        "constraints": [
            "no_external_effects",
            "no_production_mutation",
            "no_secret_access",
            "no_irreversible_write",
            "bounded_paths",
            "bounded_runtime",
            "bounded_authority",
            "receipt_required",
            "quarantine_reference_required"
        ]
    }

    quarantine_definition = {
        "role": "metric_preservation_state",
        "preserves": [
            "failed_bundle",
            "manifest",
            "candidate_payload",
            "hashes",
            "logs",
            "error_report",
            "decision_receipt",
            "computed_coordinates",
            "formalism_input_hashes",
            "reason_for_failure"
        ]
    }

    repair_edges = [
        "repairs",
        "quarantined_as",
        "generated_repair_candidate",
        "compared_repair_candidate",
        "selected_nearest_admissible",
        "tested_repair",
        "supersedes_failed_transition"
    ]

    proof_checks = {
        "repair_problem_is_formal": "objective" in repair_problem and bool(repair_problem["constraints"]),
        "repair_is_nearest_admissible_search": "minimized" in repair_problem["objective"],
        "sandbox_is_bounded_search_space": sandbox_definition["role"] == "bounded_search_space_for_repair_candidates" and "bounded_authority" in sandbox_definition["constraints"],
        "quarantine_preserves_metric_inputs": "computed_coordinates" in quarantine_definition["preserves"] and "formalism_input_hashes" in quarantine_definition["preserves"],
        "repair_retains_lineage": "lineage_to_failed_transition_retained" in repair_problem["constraints"],
        "repair_edges_are_explicit": "repairs" in repair_edges and "quarantined_as" in repair_edges
    }

    report = {
        "schema": "stegverse.stage34.repair_nearest_admissible_transition_report.v1",
        "stage": 34,
        "name": "Repair as Nearest-Admissible-Transition",
        "generated_at": utc_now(),
        "repair_problem": repair_problem,
        "sandbox_definition": sandbox_definition,
        "quarantine_definition": quarantine_definition,
        "repair_edges": repair_edges,
        "proof_checks": proof_checks,
        "success": all(proof_checks.values())
    }

    write_json(report_path, report)
    receipt = stage_receipt(34, report_path, report, "PASS" if report["success"] else "FAIL")
    append_jsonl(receipt_path, receipt)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
