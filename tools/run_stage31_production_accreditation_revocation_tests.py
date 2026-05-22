#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FIXTURE = Path("tests/fixtures/stage31_production_accreditation_revocation_cases.json")
REPORT = Path("reports/stage31_production_accreditation_revocation_report.json")
ACCREDITATION_REPORT = Path("reports/stage31_accreditation_state_report.json")
REVOCATION_REPORT = Path("reports/stage31_revocation_boundary_report.json")
REVIEW_REPORT = Path("reports/stage31_reaccreditation_review_report.md")
RECEIPTS = Path("receipts/stage31_accreditation_receipts.jsonl")

VALID_STATES = {
    "NOT_ACCREDITED",
    "ACCREDITATION_PENDING",
    "ACCREDITED_LIMITED",
    "ACCREDITED_ACTIVE",
    "REACCREDITATION_REQUIRED",
    "SUSPENDED",
    "REVOKED",
    "RETIRED",
}


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

    state = case.get("accreditation_state")
    if state not in VALID_STATES:
        return "FAIL_CLOSED", "unknown accreditation state"

    if case.get("accreditation_authority") != "formalism-tests":
        return "FAIL_CLOSED", "production accreditation authority must remain external"

    if case.get("self_accreditation_attempted"):
        return "FAIL_CLOSED", "StegVerse-001 may not self-accredit"

    if case.get("sovereign_authority_claimed"):
        return "FAIL_CLOSED", "production does not grant sovereign authority"

    if case.get("production_authority_claimed"):
        return "FAIL_CLOSED", "production accreditation does not grant unilateral production authority"

    if state == "REVOKED" or case.get("incident_detected"):
        return "REVOKE_ACCREDITATION", "revocation boundary triggered"

    if state == "REACCREDITATION_REQUIRED" or case.get("drift_detected"):
        return "REQUIRE_REACCREDITATION", "drift requires reaccreditation"

    if case.get("requires_review"):
        return "REQUIRE_REVIEW", case.get("review_reason", "production accreditation requires review")

    if case.get("production_requested"):
        if state not in {"ACCREDITED_ACTIVE", "ACCREDITED_LIMITED"}:
            return "FAIL_CLOSED", f"production requested with inadmissible accreditation state: {state}"

        for field, basis in [
            ("all_required_stages_passed", "all required stages must pass"),
            ("packet_validated", "governed instantiation packet must be validated"),
            ("receipt_chain_valid", "receipt chain must be valid"),
            ("master_record_export_ready", "master-record export readiness is required"),
            ("sandbox_required", "sandbox remains required"),
            ("cge_required", "CGE remains required"),
            ("ingestion_required", "ingestion remains required"),
            ("revocation_path_declared", "revocation path is required"),
            ("reaccreditation_path_declared", "reaccreditation path is required"),
            ("periodic_review_declared", "periodic review is required"),
        ]:
            if not case.get(field):
                return "FAIL_CLOSED", basis

        if case.get("node_participation_opt_in") and not case.get("node_status_valid"):
            return "FAIL_CLOSED", "node status must remain valid"

        if case.get("finco_requested") and not case.get("finco_eligibility_valid"):
            return "FAIL_CLOSED", "FinCo eligibility must remain independently valid"

        if case.get("ledger_record_required"):
            if case.get("ledger_record_emitted"):
                return "LEDGER_ACCREDITATION", "production accreditation ledger event recorded"
            return "FAIL_CLOSED", "accreditation ledger record missing"

        return "ALLOW_ACCREDITATION", "production accreditation boundary is admissible"

    return "FAIL_CLOSED", "production accreditation was not requested"


def write_outputs(data: Dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)

    accreditation_report = {
        "schema": "stegverse_stage31_accreditation_state_report.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "default_accreditation_state": "NOT_ACCREDITED",
        "allowed_accreditation_states": data["allowed_accreditation_states"],
        "production_meaning": "accredited_participation_not_sovereign_authority",
        "self_accreditation_allowed": False,
        "sovereign_authority_allowed": False,
        "requires_external_authority": True,
        "requires_periodic_review": True,
        "requires_reaccreditation_after_drift": True
    }

    revocation_report = {
        "schema": "stegverse_stage31_revocation_boundary_report.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "revocation_supported": True,
        "suspension_supported": True,
        "reaccreditation_supported": True,
        "revocation_triggers": [
            "authority_drift",
            "policy_drift",
            "receipt_chain_break",
            "sandbox_escape",
            "hidden_dependency",
            "unauthorized_workflow_mutation",
            "FinCo_chain_break",
            "node_health_failure",
            "incident_response_event",
            "human_review_override"
        ]
    }

    review_report = (
        "# Stage 31 Reaccreditation Review Report\n\n"
        "## Core Rule\n\n"
        "```text\n"
        "Production means accredited participation, not sovereign authority.\n"
        "```\n\n"
        "## Production Boundary\n\n"
        "Production status is explicit, external, revocable, and subject to periodic review.\n\n"
        "## Required Controls\n\n"
        "- External accreditation authority.\n"
        "- Valid Stage 1–30 proof chain.\n"
        "- Valid governed instantiation packet.\n"
        "- Valid receipt chain.\n"
        "- Master-record export readiness.\n"
        "- Sandbox, CGE, and ingestion remain required.\n"
        "- Revocation path declared.\n"
        "- Reaccreditation path declared.\n"
        "- Node status remains independently valid.\n"
        "- FinCo eligibility remains independently valid when requested.\n\n"
        "## Non-Negotiable Boundary\n\n"
        "StegVerse-001 cannot self-accredit and cannot convert production participation into sovereign authority.\n"
    )

    ACCREDITATION_REPORT.write_text(json.dumps(accreditation_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REVOCATION_REPORT.write_text(json.dumps(revocation_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REVIEW_REPORT.write_text(review_report, encoding="utf-8")


def main() -> int:
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts: Dict[str, int] = {}

        checks += req(data.get("stage") == "Stage 31", "stage must be Stage 31")
        checks += req(data.get("core_rule") == "Production means accredited participation, not sovereign authority.", "core rule mismatch")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")

        for state in ["NOT_ACCREDITED", "ACCREDITED_ACTIVE", "REACCREDITATION_REQUIRED", "REVOKED"]:
            checks += req(state in data.get("allowed_accreditation_states", []), f"missing accreditation state: {state}")

        write_outputs(data)

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage31_accreditation_receipt.v0",
                "case_id": case_id,
                "accreditation_state": case.get("accreditation_state"),
                "production_requested": case.get("production_requested"),
                "decision": decision,
                "basis": basis,
                "core_rule": data["core_rule"],
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in [
            "ALLOW_ACCREDITATION",
            "LEDGER_ACCREDITATION",
            "REQUIRE_REACCREDITATION",
            "REVOKE_ACCREDITATION",
            "REQUIRE_REVIEW",
            "FAIL_CLOSED"
        ]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage31_production_accreditation_revocation_report.v0",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 31",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "outputs": {
                "accreditation_state_report": str(ACCREDITATION_REPORT),
                "revocation_boundary_report": str(REVOCATION_REPORT),
                "reaccreditation_review_report": str(REVIEW_REPORT),
                "receipts": str(RECEIPTS)
            },
            "message": "Stage 31 production accreditation and revocation boundary validation passed."
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage31_production_accreditation_revocation_report.v0",
            "success": False,
            "error": str(exc)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
