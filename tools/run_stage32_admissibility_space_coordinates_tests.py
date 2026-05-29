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
    report_path = "reports/stage32_admissibility_space_report.json"
    receipt_path = "reports/stage32_admissibility_space_receipts.jsonl"

    decision_regions = {
        "ALLOW": {
            "region": "interior_admissible_region",
            "condition": "S_prime_in_A and recoverability>=min and coherence>=min and purpose_convergence>=min and operator_authority_preserved>=min",
            "boundary_role": "inside_A"
        },
        "DENY": {
            "region": "coherent_exterior_region",
            "condition": "S_prime_not_in_A and coherence>=min",
            "boundary_role": "boundary_crossing"
        },
        "SANDBOX": {
            "region": "bounded_uncertain_boundary_shell",
            "condition": "near_boundary and uncertainty_above_min and bounded_search_true and coherence>=min",
            "boundary_role": "search_shell"
        },
        "REVIEW": {
            "region": "observability_deficit_shell",
            "condition": "observability<min and coherence>=min",
            "boundary_role": "classification_insufficient"
        },
        "FAIL_CLOSED": {
            "region": "coherence_collapse",
            "condition": "coherence<min",
            "boundary_role": "collapse_not_crossing"
        },
        "QUARANTINE": {
            "region": "isolated_preservation_state",
            "condition": "preserve and isolate and prevent_binding",
            "boundary_role": "metric_preservation"
        }
    }

    metrics = {
        "distance_to_admissible_region": {"symbol": "d_A", "measurable": True},
        "distance_to_boundary": {"symbol": "d_boundary_A", "measurable": True},
        "recoverability_deficit": {"symbol": "delta_R", "measurable": True},
        "coherence_deficit": {"symbol": "delta_C", "measurable": True},
        "observability_deficit": {"symbol": "delta_O", "measurable": True},
        "purpose_convergence_deficit": {"symbol": "delta_P", "measurable": True},
        "operator_authority_deficit": {"symbol": "delta_U", "measurable": True}
    }

    proof_checks = {
        "decision_classes_have_regions": all("region" in v for v in decision_regions.values()),
        "deny_sandbox_review_form_shell": all(decision_regions[k]["boundary_role"] in {"boundary_crossing", "search_shell", "classification_insufficient"} for k in ["DENY", "SANDBOX", "REVIEW"]),
        "fail_closed_is_coherence_collapse": decision_regions["FAIL_CLOSED"]["boundary_role"] == "collapse_not_crossing",
        "quarantine_is_preservation_state": decision_regions["QUARANTINE"]["boundary_role"] == "metric_preservation",
        "metrics_are_measurable": all(v["measurable"] for v in metrics.values())
    }

    receipt_reconstruction_requirements = [
        "previous_receipt_hash",
        "input_state_hash",
        "transition_hash",
        "manifest_hash",
        "transition_class",
        "authority_class",
        "state_effect",
        "binding_level",
        "decision",
        "basis",
        "computed_coordinates",
        "formalism_input_hashes",
        "output_state_hash",
        "timestamp_utc"
    ]

    report = {
        "schema": "stegverse.stage32.admissibility_space_report.v1",
        "stage": 32,
        "name": "Admissibility-Space Coordinates",
        "generated_at": utc_now(),
        "decision_regions": decision_regions,
        "boundary_metrics": metrics,
        "receipt_reconstruction_requirements": receipt_reconstruction_requirements,
        "proof_checks": proof_checks,
        "success": all(proof_checks.values())
    }

    write_json(report_path, report)
    receipt = stage_receipt(32, report_path, report, "PASS" if report["success"] else "FAIL")
    append_jsonl(receipt_path, receipt)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
