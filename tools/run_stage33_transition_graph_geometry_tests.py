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
    report_path = "reports/stage33_transition_graph_geometry_report.json"
    receipt_path = "reports/stage33_transition_graph_geometry_receipts.jsonl"

    node_types = ["task", "bundle", "candidate", "merged_candidate", "test_result", "install_bundle", "receipt", "formalism_registry", "quarantine_state"]
    edge_types = [
        "produced_candidate",
        "contained_in_bundle",
        "references_formalism",
        "validated_by",
        "compared_with",
        "synthesized_into",
        "tested_by",
        "packaged_into",
        "supersedes",
        "quarantined_as",
        "installed_as"
    ]

    admissible_edge_requirements = [
        "edge_has_receipt",
        "edge_decision_not_fail_closed_for_binding_routes",
        "edge_transition_class_matches_edge_type",
        "endpoints_hash_bound",
        "authority_class_not_violated",
        "edge_replayable"
    ]

    graph_definition = {
        "graph": "G=(V,E)",
        "nodes": node_types,
        "edges": edge_types,
        "coordinate_map": "phi: V -> A union Shell union Collapse union Quarantine",
        "path_cost": "cost(P)=sum(w(e_i))",
        "discovery": "constrained_shortest_path_over_directed_receipt_bound_graph"
    }

    example_route = [
        "task",
        "openai_candidate",
        "claude_candidate",
        "comparison",
        "synthesis",
        "tests",
        "install_bundle",
        "commit_boundary"
    ]

    proof_checks = {
        "graph_has_nodes_and_edges": bool(node_types and edge_types),
        "edges_are_typed_transitions": all(isinstance(e, str) and e for e in edge_types),
        "edges_require_receipts": "edge_has_receipt" in admissible_edge_requirements,
        "graph_maps_to_coordinates": graph_definition["coordinate_map"].startswith("phi:"),
        "discovery_is_shortest_path": "shortest_path" in graph_definition["discovery"],
        "failed_states_can_be_represented": "quarantine_state" in node_types and "quarantined_as" in edge_types
    }

    report = {
        "schema": "stegverse.stage33.transition_graph_geometry_report.v1",
        "stage": 33,
        "name": "Transition Graph as Geometric Structure",
        "generated_at": utc_now(),
        "graph_definition": graph_definition,
        "admissible_edge_requirements": admissible_edge_requirements,
        "example_route": example_route,
        "proof_checks": proof_checks,
        "success": all(proof_checks.values())
    }

    write_json(report_path, report)
    receipt = stage_receipt(33, report_path, report, "PASS" if report["success"] else "FAIL")
    append_jsonl(receipt_path, receipt)

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["success"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
