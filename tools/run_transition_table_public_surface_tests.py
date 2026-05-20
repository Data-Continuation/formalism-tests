#!/usr/bin/env python3
"""Validate the Transition Table public proof-surface contract.

This is a standard-library runner intended for the existing declared-task
workflow. It validates Site-facing fixture snapshots and emits a JSON report.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path("tests/fixtures/site")
REPORT_PATH = Path("reports/transition_table_public_surface_report.json")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise AssertionError(f"missing fixture: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"fixture must be a JSON object: {path}")
    return data


def require(condition: bool, message: str) -> int:
    if not condition:
        raise AssertionError(message)
    return 1


def validate_proof_surface(data: dict[str, Any]) -> int:
    checks = 0
    checks += require(data.get("current_stage") == "Stage 6", "current_stage must be Stage 6")
    checks += require("Stage 6 verified" in data.get("status", ""), "status must say Stage 6 verified")
    checks += require(data.get("authority_boundary", "").startswith("formalism-tests produces receipts"), "authority boundary missing")
    stages = data.get("stages", [])
    checks += require(isinstance(stages, list) and len(stages) >= 5, "stages must include at least Stage 2 through Stage 6")
    stage6 = next((stage for stage in stages if stage.get("stage") == "Stage 6"), None)
    checks += require(stage6 is not None, "Stage 6 entry missing")
    checks += require(stage6.get("status") == "verified", "Stage 6 status must be verified")
    result = data.get("stage6_result", {})
    checks += require(result.get("success") is True, "stage6_result.success must be true")
    checks += require(result.get("candidate_count") == 10, "Stage 6 candidate_count must be 10")
    checks += require(result.get("assertion_count") == 320, "Stage 6 assertion_count must be 320")
    checks += require(result.get("decision_counts", {}).get("RESET_BOUNDARY") == 1, "RESET_BOUNDARY count must be 1")
    checks += require(result.get("decision_counts", {}).get("EVOLVE_BOUNDARY") == 1, "EVOLVE_BOUNDARY count must be 1")
    checks += require("stage6_unified_gate_tests" in data.get("verified_tasks", []), "Stage 6 task missing from verified_tasks")
    return checks


def validate_discovery_map(data: dict[str, Any]) -> int:
    checks = 0
    scale = data.get("scale", {})
    levels = scale.get("levels", [])
    checks += require(scale.get("minimum") == 0 and scale.get("maximum") == 5, "completion scale must be 0-5")
    checks += require(isinstance(levels, list) and len(levels) == 6, "completion scale must include 6 levels")
    elements = data.get("elements", [])
    checks += require(isinstance(elements, list) and len(elements) >= 16, "expected at least 16 transition elements")
    ids = set()
    unlocked = 0
    for element in elements:
        element_id = element.get("element_id")
        ids.add(element_id)
        checks += require(bool(element_id), "element missing element_id")
        checks += require(bool(element.get("name")), f"{element_id}: missing name")
        checks += require(isinstance(element.get("completion_level"), int), f"{element_id}: completion_level must be int")
        checks += require(0 <= element["completion_level"] <= 5, f"{element_id}: completion_level out of range")
        checks += require(bool(element.get("summary")), f"{element_id}: missing summary")
        checks += require(bool(element.get("detail_page")), f"{element_id}: missing detail_page")
        checks += require(element["detail_page"].startswith("transition-elements/"), f"{element_id}: detail_page must be under transition-elements/")
        checks += require(isinstance(element.get("details"), list) and len(element["details"]) > 0, f"{element_id}: missing details")
        if element["completion_level"] == 5:
            unlocked += 1
    checks += require(unlocked >= 12, "expected at least 12 unlocked Level 5 elements")
    for required in ["AE", "BC", "CHF", "DC", "DaCo", "Triad", "IW", "RE", "RESET_BOUNDARY", "EVOLVE_BOUNDARY", "AI_BLOCK", "FINCO_CHAIN"]:
        checks += require(required in ids, f"missing unlocked element {required}")
    return checks


def validate_transition_classes(classes_data: dict[str, Any], discovery_data: dict[str, Any]) -> int:
    checks = 0
    classes = classes_data.get("classes", [])
    checks += require(isinstance(classes, list) and len(classes) >= 10, "expected at least 10 transition classes")
    family_levels = discovery_data.get("classification_family_levels", {})
    decision_levels = discovery_data.get("transition_decision_levels", {})
    seen_decisions = set()
    for item in classes:
        tid = item.get("transition_id")
        checks += require(bool(tid), "transition class missing transition_id")
        for key in ["transition_name", "transition_family", "theorem_basis", "role", "multi_body_coupling_class", "boundary_behavior", "replay_semantics", "basis"]:
            checks += require(bool(item.get(key)), f"{tid}: missing {key}")
        decision = item.get("expected_decision") or item.get("verified_decision") or item.get("candidate_expected_outcome")
        seen_decisions.add(decision)
        checks += require(decision in {"ALLOW", "FAIL_CLOSED", "RESET_BOUNDARY", "EVOLVE_BOUNDARY", "DENY", "ALLOW_WITH_SIGNOFF"}, f"{tid}: invalid decision {decision}")
        checks += require(item.get("transition_family") in family_levels or decision in decision_levels, f"{tid}: no level mapping")
        checks += require(float(item.get("inference_window_width", 0)) >= float(item.get("inference_window_minimum", 0)), f"{tid}: IW width below minimum")
        checks += require(float(item.get("recoverability_score", 0)) >= 0, f"{tid}: invalid recoverability_score")
    checks += require("RESET_BOUNDARY" in seen_decisions, "transition classes must include RESET_BOUNDARY")
    checks += require("EVOLVE_BOUNDARY" in seen_decisions, "transition classes must include EVOLVE_BOUNDARY")
    return checks


def validate_public_contract(contract: dict[str, Any], proof: dict[str, Any]) -> int:
    checks = 0
    checks += require(contract.get("single_status_source") == "data/formalism-tests/transition-proof-surface.json", "wrong single status source")
    required_pages = set(contract.get("required_pages", []))
    proof_pages = set(proof.get("site_pages", []))
    checks += require(required_pages.issubset(proof_pages), "contract required_pages must be included in proof surface site_pages")
    checks += require("stage6-unified-gate-results.html" in required_pages, "Stage 6 page missing from contract")
    checks += require("transition-table-classes.html" in required_pages, "transition class page missing from contract")
    checks += require("transition-elements/index.html" in required_pages, "element index missing from contract")
    markers = contract.get("required_mobile_markers", [])
    checks += require("mobile-grid" in markers, "mobile-grid marker required")
    checks += require("transition-tile" in markers, "transition-tile marker required")
    checks += require("renderMobile" in markers and "renderDesktop" in markers, "mobile/desktop renderer markers required")
    return checks


def main() -> int:
    try:
        proof = load_json(FIXTURE_DIR / "transition-proof-surface.json")
        discovery = load_json(FIXTURE_DIR / "transition-discovery-map.json")
        classes = load_json(FIXTURE_DIR / "transition-table-classes.json")
        contract = load_json(FIXTURE_DIR / "site-public-surface-contract.json")

        checks = 0
        checks += validate_proof_surface(proof)
        checks += validate_discovery_map(discovery)
        checks += validate_transition_classes(classes, discovery)
        checks += validate_public_contract(contract, proof)

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_transition_table_public_surface_report.v1",
            "success": True,
            "assertion_count": checks,
            "current_stage": proof.get("current_stage"),
            "stage6_status": proof.get("status"),
            "stage6_result": proof.get("stage6_result"),
            "element_count": len(discovery.get("elements", [])),
            "unlocked_level_5_count": sum(1 for element in discovery.get("elements", []) if element.get("completion_level") == 5),
            "transition_class_count": len(classes.get("classes", [])),
            "single_status_source": contract.get("single_status_source"),
            "message": "Transition Table public proof-surface validation passed."
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_transition_table_public_surface_report.v1",
            "success": False,
            "error": str(exc)
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
