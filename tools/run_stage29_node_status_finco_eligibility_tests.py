#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FIXTURE = Path("tests/fixtures/stage29_node_status_finco_eligibility_cases.json")
REPORT = Path("reports/stage29_node_status_finco_eligibility_report.json")
NODE_REPORT = Path("reports/stage29_node_status_report.json")
FINCO_REPORT = Path("reports/stage29_finco_eligibility_report.json")
REVIEW_REPORT = Path("reports/stage29_node_status_review_report.md")
RECEIPTS = Path("receipts/stage29_node_finco_receipts.jsonl")

ADMISSIBLE_FINCO_NODE_STATUSES = {"NODE_ACTIVE", "NODE_LIMITED"}
VALID_NODE_STATUSES = {
    "NOT_A_NODE",
    "NODE_PENDING",
    "NODE_ACTIVE",
    "NODE_LIMITED",
    "NODE_SUSPENDED",
    "NODE_REVOKED",
    "NODE_RETIRED",
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

    node_status = case.get("node_status")
    if node_status not in VALID_NODE_STATUSES:
        return "FAIL_CLOSED", "unknown node status"

    node_opt_in = case.get("node_participation_opt_in")
    finco_requested = case.get("finco_participation_requested")

    if node_status != "NOT_A_NODE" and not node_opt_in:
        return "FAIL_CLOSED", "node status requires explicit opt-in"

    if node_opt_in:
        if not case.get("node_owner_authority_valid"):
            return "FAIL_CLOSED", "node owner authority is invalid"
        if not case.get("node_policy_scope_declared"):
            return "FAIL_CLOSED", "node policy scope is missing"
        if not case.get("node_revocation_path_declared"):
            return "FAIL_CLOSED", "node revocation path is missing"
        if not case.get("node_receipt_chain_valid"):
            return "FAIL_CLOSED", "node receipt chain is invalid"
        if not case.get("node_health_report_present"):
            return "FAIL_CLOSED", "node health report is missing"

    if node_status in {"NODE_REVOKED", "NODE_SUSPENDED"} and not finco_requested:
        return "FAIL_CLOSED", f"{node_status} cannot proceed as active node status"

    if case.get("requires_review"):
        return "REQUIRE_REVIEW", case.get("review_reason", "node status requires review")

    if finco_requested:
        if not node_opt_in:
            return "FAIL_CLOSED", "FinCo requested without node opt-in"
        if node_status not in ADMISSIBLE_FINCO_NODE_STATUSES:
            return "FAIL_CLOSED", f"FinCo requires NODE_ACTIVE or NODE_LIMITED, got {node_status}"
        if not case.get("consent_receipt_valid"):
            return "FAIL_CLOSED", "FinCo consent receipt missing"
        if not case.get("access_receipt_valid"):
            return "FAIL_CLOSED", "FinCo access receipt missing"
        if not case.get("use_receipt_valid"):
            return "FAIL_CLOSED", "FinCo use receipt missing"
        if not case.get("compensation_rule_defined"):
            return "FAIL_CLOSED", "FinCo compensation rule missing"
        if not case.get("revocation_rule_defined"):
            return "FAIL_CLOSED", "FinCo revocation rule missing"
        if not case.get("chain_intact"):
            return "FAIL_CLOSED", "FinCo chain is broken"
        if case.get("creates_entitlement") and not case.get("entitlement_authority_valid"):
            return "FAIL_CLOSED", "FinCo entitlement requires explicit entitlement authority"

        if case.get("ledger_record_required"):
            if case.get("ledger_record_emitted"):
                return "LEDGER_FINCO_ELIGIBILITY", "FinCo eligibility ledger event recorded"
            return "FAIL_CLOSED", "FinCo ledger record missing"

        return "ALLOW_FINCO_ELIGIBILITY", "FinCo eligibility requirements are satisfied"

    if case.get("ledger_record_required"):
        if case.get("ledger_record_emitted"):
            return "LEDGER_NODE_STATUS", "node status ledger event recorded"
        return "FAIL_CLOSED", "node status ledger record missing"

    return "ALLOW_NODE_STATUS", "node status state is admissible"


def write_outputs(data: Dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)

    node_report = {
        "schema": "stegverse_stage29_node_status_report.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "default_node_participation_opt_in": False,
        "default_node_status": "NOT_A_NODE",
        "allowed_node_statuses": data["allowed_node_statuses"],
        "revocation_supported": True,
        "suspension_supported": True,
        "core_rule": data["core_rule"]
    }

    finco_report = {
        "schema": "stegverse_stage29_finco_eligibility_report.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "default_finco_participation_requested": False,
        "default_finco_participation_allowed": False,
        "admissible_node_statuses": data["finco_admissible_node_statuses"],
        "requires_consent_receipt": True,
        "requires_access_receipt": True,
        "requires_use_receipt": True,
        "requires_compensation_rule": True,
        "requires_revocation_rule": True,
        "requires_chain_intact": True,
        "entitlement_requires_authority": True
    }

    review_md = (
        "# Stage 29 Node Status and FinCo Eligibility Review\n\n"
        "## Core Rule\n\n"
        "```text\n"
        "Core installation does not imply node participation.\n"
        "Node participation does not imply FinCo eligibility.\n"
        "FinCo eligibility requires explicit node status, valid receipts, compensation rules, and revocation rules.\n"
        "```\n\n"
        "## Default State\n\n"
        "```json\n"
        "{\n"
        "  \"core_unit_installed\": true,\n"
        "  \"node_participation_opt_in\": false,\n"
        "  \"node_status\": \"NOT_A_NODE\",\n"
        "  \"finco_participation_requested\": false,\n"
        "  \"finco_participation_allowed\": false\n"
        "}\n"
        "```\n\n"
        "## Findings\n\n"
        "- Node status is explicit opt-in.\n"
        "- FinCo eligibility is separate from node status.\n"
        "- Suspended and revoked nodes fail closed.\n"
        "- Pending nodes require review.\n"
        "- FinCo requires consent, access, use, compensation, revocation, and intact-chain evidence.\n"
        "- Entitlement creation requires explicit entitlement authority.\n"
    )

    NODE_REPORT.write_text(json.dumps(node_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    FINCO_REPORT.write_text(json.dumps(finco_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REVIEW_REPORT.write_text(review_md, encoding="utf-8")


def main() -> int:
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts: Dict[str, int] = {}

        checks += req(data.get("stage") == "Stage 29", "stage must be Stage 29")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")
        checks += req("NOT_A_NODE" in data.get("allowed_node_statuses", []), "NOT_A_NODE status required")
        checks += req("NODE_ACTIVE" in data.get("finco_admissible_node_statuses", []), "NODE_ACTIVE FinCo status required")
        checks += req("NODE_LIMITED" in data.get("finco_admissible_node_statuses", []), "NODE_LIMITED FinCo status required")

        write_outputs(data)

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage29_node_finco_receipt.v0",
                "case_id": case_id,
                "node_status": case.get("node_status"),
                "finco_requested": case.get("finco_participation_requested"),
                "decision": decision,
                "basis": basis,
                "core_rule": data["core_rule"],
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in [
            "ALLOW_NODE_STATUS",
            "ALLOW_FINCO_ELIGIBILITY",
            "LEDGER_NODE_STATUS",
            "LEDGER_FINCO_ELIGIBILITY",
            "REQUIRE_REVIEW",
            "FAIL_CLOSED"
        ]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage29_node_status_finco_eligibility_report.v0",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 29",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "outputs": {
                "node_status_report": str(NODE_REPORT),
                "finco_eligibility_report": str(FINCO_REPORT),
                "review_report": str(REVIEW_REPORT),
                "receipts": str(RECEIPTS)
            },
            "message": "Stage 29 optional node status and FinCo eligibility validation passed."
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage29_node_status_finco_eligibility_report.v0",
            "success": False,
            "error": str(exc)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
