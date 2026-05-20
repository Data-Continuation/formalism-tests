#!/usr/bin/env python3
"""Validate Site mirror integrity against formalism-tests proof status.

This standard-library runner checks fixture snapshots representing the Site
public mirror. It prevents drift between formalism-tests proof authority and
the Site presentation surface.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_DIR = Path("tests/fixtures/site_mirror")
REPORT_PATH = Path("reports/site_mirror_integrity_report.json")


def load_json(name: str) -> dict[str, Any]:
    path = FIXTURE_DIR / name
    if not path.exists():
        raise AssertionError(f"missing fixture: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data


def require(condition: bool, message: str) -> int:
    if not condition:
        raise AssertionError(message)
    return 1


def validate_status_source(proof: dict[str, Any]) -> int:
    checks = 0
    checks += require(proof.get("current_stage") == "Stage 6", "proof surface current_stage must be Stage 6")
    checks += require("Stage 6 verified" in proof.get("status", ""), "proof surface status must say Stage 6 verified")
    checks += require("Stage 6 next" not in json.dumps(proof), "proof surface must not contain stale 'Stage 6 next'")
    checks += require(proof.get("authority_boundary", "").startswith("formalism-tests produces receipts"), "authority boundary missing")
    checks += require("stage6_unified_gate_tests" in proof.get("verified_tasks", []), "Stage 6 task missing from verified_tasks")
    checks += require("representation_non_consequence_tests" in proof.get("verified_tasks", []), "Representation task missing from verified_tasks")
    return checks


def validate_stage6_mirror(proof: dict[str, Any], stage6: dict[str, Any]) -> int:
    checks = 0
    result = proof.get("stage6_result", {})
    checks += require(result.get("success") is True, "proof Stage 6 result must be successful")
    checks += require(stage6.get("success") is True, "Stage 6 public result must be successful")
    for key in ["candidate_count", "assertion_count", "decision_counts", "task_id", "runner"]:
        checks += require(result.get(key) == stage6.get(key), f"Stage 6 mirror mismatch for {key}")
    checks += require(result.get("candidate_count") == 10, "Stage 6 candidate_count must be 10")
    checks += require(result.get("assertion_count") == 320, "Stage 6 assertion_count must be 320")
    checks += require(result.get("decision_counts", {}).get("RESET_BOUNDARY") == 1, "RESET_BOUNDARY count mismatch")
    checks += require(result.get("decision_counts", {}).get("EVOLVE_BOUNDARY") == 1, "EVOLVE_BOUNDARY count mismatch")
    return checks


def validate_discovery(discovery: dict[str, Any], contract: dict[str, Any]) -> int:
    checks = 0
    elements = discovery.get("elements", [])
    checks += require(isinstance(elements, list) and len(elements) >= 16, "discovery must include at least 16 elements")
    unlocked = [element for element in elements if element.get("completion_level") == 5]
    checks += require(len(unlocked) >= 13, "expected at least 13 Level 5 elements after Representation Non-Consequence coverage")
    detail_pages = {element.get("detail_page") for element in elements}
    for page in contract.get("required_element_pages", []):
        checks += require(page in detail_pages, f"required element detail page missing: {page}")
    checks += require("transition-elements/representation-non-consequence.html" in detail_pages, "Representation Non-Consequence element page missing")
    ids = {element.get("element_id") for element in elements}
    checks += require("REPRESENTATION_NON_CONSEQUENCE" in ids, "Representation Non-Consequence element missing")
    return checks


def validate_transition_classes(classes_data: dict[str, Any], discovery: dict[str, Any]) -> int:
    checks = 0
    classes = classes_data.get("classes", [])
    checks += require(isinstance(classes, list) and len(classes) >= 10, "transition table must include at least 10 classes")
    decisions = {item.get("expected_decision") or item.get("verified_decision") or item.get("candidate_expected_outcome") for item in classes}
    for required in ["ALLOW", "FAIL_CLOSED", "RESET_BOUNDARY", "EVOLVE_BOUNDARY"]:
        checks += require(required in decisions, f"missing transition decision {required}")
    family_levels = discovery.get("classification_family_levels", {})
    decision_levels = discovery.get("transition_decision_levels", {})
    for item in classes:
        tid = item.get("transition_id")
        checks += require(bool(tid), "transition missing transition_id")
        checks += require(item.get("transition_family") in family_levels or (item.get("expected_decision") in decision_levels), f"{tid}: missing level mapping")
        checks += require(bool(item.get("basis")), f"{tid}: missing basis")
    return checks


def validate_representation_report(report: dict[str, Any], coverage: dict[str, Any], discovery: dict[str, Any]) -> int:
    checks = 0
    checks += require(report.get("success") is True, "Representation Non-Consequence report must be successful")
    checks += require(report.get("case_count") == 7, "Representation case_count must be 7")
    checks += require(report.get("receipt_count") == 7, "Representation receipt_count must be 7")
    checks += require(report.get("decision_counts", {}).get("NO_CONSEQUENCE") == 3, "NO_CONSEQUENCE count must be 3")
    checks += require("Representation Non-Consequence" in coverage.get("covered", []), "Representation theorem must be covered")
    checks += require("Representation Non-Consequence" not in coverage.get("partially_covered", []), "Representation theorem must not remain partially covered")
    match = next((element for element in discovery.get("elements", []) if element.get("element_id") == "REPRESENTATION_NON_CONSEQUENCE"), None)
    checks += require(match is not None, "Representation element missing from discovery")
    checks += require(match.get("completion_level") == 5, "Representation element should be Level 5 after direct proof")
    return checks


def validate_contract(proof: dict[str, Any], contract: dict[str, Any]) -> int:
    checks = 0
    checks += require(contract.get("single_status_source") == "data/formalism-tests/transition-proof-surface.json", "single status source mismatch")
    checks += require(contract.get("shared_renderer") == "assets/transition-site-status.js", "shared renderer mismatch")
    proof_pages = set(proof.get("site_pages", []))
    for page in contract.get("required_pages", []):
        checks += require(page in proof_pages, f"required page not listed in proof surface: {page}")
    markers = set(contract.get("required_mobile_markers", []))
    for marker in ["mobile-grid", "transition-tile", "renderMobile", "renderDesktop"]:
        checks += require(marker in markers, f"mobile contract marker missing: {marker}")
    checks += require("reports/transition_table_receipts.jsonl" in contract.get("canonical_receipt_files", []), "canonical transition table receipt missing")
    checks += require("reports/transition_table_receipts 2.jsonl" in contract.get("noncanonical_duplicates", []), "duplicate receipt file must be noncanonical")
    return checks


def main() -> int:
    try:
        proof = load_json("transition-proof-surface.json")
        stage6 = load_json("stage6-unified-gate-results.json")
        discovery = load_json("transition-discovery-map.json")
        classes = load_json("transition-table-classes.json")
        representation = load_json("representation-non-consequence-report.json")
        coverage = load_json("theorem-coverage-summary.json")
        contract = load_json("site-mirror-page-contract.json")

        checks = 0
        checks += validate_status_source(proof)
        checks += validate_stage6_mirror(proof, stage6)
        checks += validate_discovery(discovery, contract)
        checks += validate_transition_classes(classes, discovery)
        checks += validate_representation_report(representation, coverage, discovery)
        checks += validate_contract(proof, contract)

        unlocked = sum(1 for element in discovery.get("elements", []) if element.get("completion_level") == 5)
        report = {
            "schema": "stegverse_site_mirror_integrity_report.v1",
            "success": True,
            "assertion_count": checks,
            "current_stage": proof.get("current_stage"),
            "stage6_candidate_count": proof.get("stage6_result", {}).get("candidate_count"),
            "stage6_assertion_count": proof.get("stage6_result", {}).get("assertion_count"),
            "element_count": len(discovery.get("elements", [])),
            "unlocked_level_5_count": unlocked,
            "transition_class_count": len(classes.get("classes", [])),
            "representation_non_consequence_status": "Covered",
            "single_status_source": contract.get("single_status_source"),
            "message": "Site mirror integrity validation passed."
        }
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_site_mirror_integrity_report.v1",
            "success": False,
            "error": str(exc)
        }
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
