#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FIXTURE = Path("tests/fixtures/stage27_discovery_to_canonical_state_cases.json")
REPORT = Path("reports/stage27_discovery_to_canonical_state_report.json")
GAP_REPORT = Path("reports/stage27_discovery_gap_report.md")
DISCOVERED = Path("reports/stage27_discovered_state.json")
CANONICAL = Path("reports/stage27_canonical_state.json")
DIFF = Path("reports/stage27_state_diff.json")
INSTALL_PLAN = Path("reports/stage27_install_plan_candidate.json")
RECEIPTS = Path("receipts/stage27_discovery_receipts.jsonl")


def canon(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def req(ok: bool, message: str) -> int:
    if not ok:
        raise AssertionError(message)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def decide(case: Dict[str, Any]) -> tuple[str, str]:
    if not case.get("entity_active"):
        return "FAIL_CLOSED", "StegVerse-001 is not active"
    if case.get("discovery_authority") != "formalism-tests":
        return "FAIL_CLOSED", "discovery authority must remain formalism-tests"
    if not case.get("target_repo_declared"):
        return "FAIL_CLOSED", "target repo is not declared"
    if not case.get("discovered_state_generated"):
        return "FAIL_CLOSED", "discovered state was not generated"
    if not case.get("canonical_state_loaded"):
        return "FAIL_CLOSED", "canonical state was not loaded"
    if not case.get("diff_generated"):
        return "FAIL_CLOSED", "state diff was not generated"
    if not case.get("install_plan_generated"):
        return "FAIL_CLOSED", "install plan candidate was not generated"
    if case.get("install_performed"):
        return "FAIL_CLOSED", "discovery may not install"
    if not case.get("diff_classifications_valid"):
        return "FAIL_CLOSED", "diff classifications are invalid"
    if not case.get("unknown_files_classified"):
        return "FAIL_CLOSED", "unknown files must be classified"
    if not case.get("node_status_default_safe"):
        return "FAIL_CLOSED", "node status default is unsafe"
    if not case.get("finco_default_safe"):
        return "FAIL_CLOSED", "FinCo default is unsafe"
    if not case.get("receipts_emitted"):
        return "FAIL_CLOSED", "discovery receipts missing"
    if case.get("requires_review"):
        return "REQUIRE_REVIEW", case.get("review_reason", "discovery requires review")
    if case.get("ledger_event") == "discovered_state":
        return "LEDGER_DISCOVERED_STATE", "discovered state ledger event recorded"
    if case.get("ledger_event") == "canonical_diff":
        return "LEDGER_CANONICAL_DIFF", "canonical diff ledger event recorded"
    return "ALLOW_DISCOVERY", "discovery-to-canonical state DB is admissible"


def write_discovery_outputs(data: Dict[str, Any]) -> None:
    reports = Path("reports")
    receipts = Path("receipts")
    reports.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)

    discovered_state = {
        "schema": "stegverse_discovered_state.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target_unit": "core-lite",
        "target_scale_profile": "repo_core",
        "discovered_files": [
            "core_lite/cge.py",
            "core_lite/ingest.py",
            "core_lite/receipts.py",
            "tools/tasks/core_lite_tasks.json",
            "schemas/ingest_manifest.schema.json"
        ],
        "detected_capabilities": [
            "cge",
            "ingestion",
            "receipt_emission",
            "declared_tasks",
            "schemas"
        ],
        "node_participation": {
            "node_participation_opt_in": False,
            "node_status": "NOT_A_NODE"
        },
        "finco_participation": {
            "finco_participation_requested": False,
            "finco_participation_allowed": False
        }
    }

    canonical_state = {
        "schema": "stegverse_canonical_state_expectation.v0",
        "target_unit": "core-lite",
        "required_capabilities": [
            "identity",
            "policy_scope",
            "declared_tasks",
            "ingestion",
            "sandbox",
            "cge",
            "receipt_emission",
            "quarantine",
            "reports",
            "reconstruction_path"
        ],
        "required_node_default": {
            "node_participation_opt_in": False,
            "node_status": "NOT_A_NODE"
        },
        "required_finco_default": {
            "finco_participation_requested": False,
            "finco_participation_allowed": False
        }
    }

    state_diff = {
        "schema": "stegverse_state_diff.v0",
        "diff_categories": data["canonical_diff_categories"],
        "items": [
            {
                "path": "core_lite/cge.py",
                "classification": "present_and_valid",
                "basis": "CGE module detected"
            },
            {
                "path": "core_lite/sandbox.py",
                "classification": "missing_required",
                "basis": "sandbox capability expected but not confirmed in discovered state"
            },
            {
                "path": ".github/workflows/core-lite-self-test.yml",
                "classification": "extra_requires_review",
                "basis": "workflow path requires explicit review before mutation"
            }
        ]
    }

    install_plan = {
        "schema": "stegverse_install_plan_candidate.v0",
        "plan_id": "stage27-core-lite-discovery-plan",
        "target_unit": "core-lite",
        "target_scale_profile": "repo_core",
        "state_diff_ref": str(DIFF),
        "install_allowed_by_plan": False,
        "actions": [
            {
                "action": "review_missing_sandbox_capability",
                "classification": "missing_required",
                "requires_review": True
            },
            {
                "action": "review_existing_workflow_surface",
                "classification": "extra_requires_review",
                "requires_review": True
            }
        ],
        "core_rule": data["core_rule"]
    }

    DISCOVERED.write_text(json.dumps(discovered_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    CANONICAL.write_text(json.dumps(canonical_state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    DIFF.write_text(json.dumps(state_diff, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    INSTALL_PLAN.write_text(json.dumps(install_plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    GAP_REPORT.write_text(
        "# Stage 27 Discovery Gap Report\n\n"
        "## Status\n\n"
        "Discovery produced a structured observed-state DB, canonical expectation, state diff, and install-plan candidate.\n\n"
        "## Core Rule\n\n"
        "```text\n"
        "An install plan is a candidate transition, not installation authority.\n"
        "```\n\n"
        "## Initial Findings\n\n"
        "- CGE module detected.\n"
        "- Ingestion module detected.\n"
        "- Receipt module detected.\n"
        "- Declared tasks detected.\n"
        "- Sandbox capability requires review because it was not confirmed in this normalized discovery sample.\n"
        "- Existing workflow surface requires review before any mutation.\n"
        "- Node participation defaults to `NOT_A_NODE`.\n"
        "- FinCo participation defaults to disabled.\n",
        encoding="utf-8"
    )


def main() -> int:
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts: Dict[str, int] = {}

        checks += req(data.get("stage") == "Stage 27", "stage must be Stage 27")
        checks += req(data.get("core_rule") == "An install plan is a candidate transition, not installation authority.", "core rule mismatch")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")

        for category in [
            "present_and_valid",
            "missing_required",
            "extra_requires_review",
            "quarantine_required"
        ]:
            checks += req(category in data.get("canonical_diff_categories", []), f"missing diff category: {category}")

        write_discovery_outputs(data)

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage27_discovery_receipt.v0",
                "case_id": case_id,
                "decision": decision,
                "basis": basis,
                "core_rule": data["core_rule"],
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in [
            "ALLOW_DISCOVERY",
            "LEDGER_DISCOVERED_STATE",
            "LEDGER_CANONICAL_DIFF",
            "REQUIRE_REVIEW",
            "FAIL_CLOSED"
        ]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage27_discovery_to_canonical_state_report.v0",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 27",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "outputs": {
                "discovered_state": str(DISCOVERED),
                "canonical_state": str(CANONICAL),
                "state_diff": str(DIFF),
                "install_plan_candidate": str(INSTALL_PLAN),
                "gap_report": str(GAP_REPORT),
                "receipts": str(RECEIPTS)
            },
            "message": "Stage 27 discovery-to-canonical state DB validation passed."
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage27_discovery_to_canonical_state_report.v0",
            "success": False,
            "error": str(exc)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
