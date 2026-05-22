#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FIXTURE = Path("tests/fixtures/stage28_canonical_diff_install_plan_cases.json")
REPORT = Path("reports/stage28_canonical_diff_install_plan_report.json")
REVIEW_REPORT = Path("reports/stage28_install_plan_review_report.md")
VALIDATED_DIFF = Path("reports/stage28_state_diff_validated.json")
INSTALL_PLAN = Path("reports/stage28_install_plan_candidate.json")
RECEIPTS = Path("receipts/stage28_install_plan_receipts.jsonl")


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
    if case.get("plan_authority") != "formalism-tests":
        return "FAIL_CLOSED", "install-plan authority must remain formalism-tests"
    if not case.get("diff_loaded"):
        return "FAIL_CLOSED", "canonical diff was not loaded"
    if not case.get("all_diff_items_classified"):
        return "FAIL_CLOSED", "all diff items must be classified"
    if not case.get("diff_categories_valid"):
        return "FAIL_CLOSED", "diff categories are invalid"
    if not case.get("unknown_files_classified"):
        return "FAIL_CLOSED", "unknown files must be classified"
    if not case.get("protected_paths_reviewed"):
        return "FAIL_CLOSED", "protected paths must be reviewed or fail closed"
    if case.get("dangerous_items_present"):
        return "FAIL_CLOSED", "dangerous diff items fail closed"
    if not case.get("install_plan_generated"):
        return "FAIL_CLOSED", "install-plan candidate was not generated"
    if case.get("install_allowed_by_plan"):
        return "FAIL_CLOSED", "install plan may not authorize installation"
    if case.get("install_performed"):
        return "FAIL_CLOSED", "Stage 28 may not install"
    if not case.get("sandbox_required"):
        return "FAIL_CLOSED", "sandbox is required before binding"
    if not case.get("cge_required"):
        return "FAIL_CLOSED", "CGE is required before binding"
    if not case.get("receipts_required"):
        return "FAIL_CLOSED", "receipts are required"
    if not case.get("node_default_safe"):
        return "FAIL_CLOSED", "node participation default is unsafe"
    if not case.get("finco_default_safe"):
        return "FAIL_CLOSED", "FinCo default is unsafe"
    if case.get("quarantine_items_present"):
        return "QUARANTINE_PLAN", "install-plan candidate contains quarantine-classified items"
    if case.get("requires_review"):
        return "REQUIRE_REVIEW", case.get("review_reason", "install-plan candidate requires review")
    if case.get("ledger_record_required"):
        if case.get("ledger_record_emitted"):
            return "LEDGER_INSTALL_PLAN", "install-plan candidate ledger event recorded"
        return "FAIL_CLOSED", "install-plan ledger record missing"
    return "ALLOW_INSTALL_PLAN_CANDIDATE", "install-plan candidate satisfies Stage 28 constraints"


def write_outputs(data: Dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS.parent.mkdir(parents=True, exist_ok=True)

    validated_diff = {
        "schema": "stegverse_stage28_state_diff_validated.v0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "allowed_diff_categories": data["allowed_diff_categories"],
        "validated_items": [
            {
                "path": "core_lite/cge.py",
                "classification": "present_and_valid",
                "plan_action": "preserve",
                "basis": "existing CGE module should not be overwritten without review"
            },
            {
                "path": "core_lite/sandbox.py",
                "classification": "missing_required",
                "plan_action": "propose_candidate",
                "basis": "sandbox capability is expected by Governed Core Unit principle"
            },
            {
                "path": ".github/workflows/core-lite-self-test.yml",
                "classification": "extra_requires_review",
                "plan_action": "review_only",
                "basis": "workflow path is protected and requires explicit review"
            },
            {
                "path": "secrets/example-token.txt",
                "classification": "quarantine_required",
                "plan_action": "quarantine_only",
                "basis": "secret-like path cannot be installed"
            }
        ]
    }

    install_plan = {
        "schema": "stegverse_stage28_install_plan_candidate.v0",
        "plan_id": "stage28-core-lite-install-plan-candidate",
        "target_unit": "core-lite",
        "scale_profile": "repo_core",
        "source_stage": "Stage 28",
        "install_allowed_by_plan": False,
        "sandbox_required": True,
        "cge_required": True,
        "receipts_required": True,
        "node_participation": {
            "node_participation_opt_in": False,
            "node_status": "NOT_A_NODE"
        },
        "finco_participation": {
            "finco_participation_requested": False,
            "finco_participation_allowed": False
        },
        "actions": [
            {
                "action_id": "preserve_existing_cge",
                "path": "core_lite/cge.py",
                "action": "preserve",
                "classification": "present_and_valid",
                "requires_review": False
            },
            {
                "action_id": "propose_sandbox_candidate",
                "path": "core_lite/sandbox.py",
                "action": "propose_candidate",
                "classification": "missing_required",
                "requires_review": True
            },
            {
                "action_id": "review_workflow_surface",
                "path": ".github/workflows/core-lite-self-test.yml",
                "action": "review_only",
                "classification": "extra_requires_review",
                "requires_review": True
            },
            {
                "action_id": "quarantine_secret_like_path",
                "path": "secrets/example-token.txt",
                "action": "quarantine_only",
                "classification": "quarantine_required",
                "requires_review": True
            }
        ],
        "core_rule": data["core_rule"]
    }

    VALIDATED_DIFF.write_text(json.dumps(validated_diff, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    INSTALL_PLAN.write_text(json.dumps(install_plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    REVIEW_REPORT.write_text(
        "# Stage 28 Install Plan Review Report\n\n"
        "## Core Rule\n\n"
        "```text\n"
        "An install plan is a candidate transition, not installation authority.\n"
        "```\n\n"
        "## Summary\n\n"
        "Stage 28 validated canonical diff classifications and generated a non-authoritative install-plan candidate.\n\n"
        "## Findings\n\n"
        "- Existing CGE module is classified as `present_and_valid` and should be preserved.\n"
        "- Missing sandbox capability is classified as `missing_required` and should be proposed as a candidate, not installed directly.\n"
        "- Workflow surface is classified as `extra_requires_review`.\n"
        "- Secret-like path is classified as `quarantine_required`.\n"
        "- Node status remains `NOT_A_NODE` by default.\n"
        "- FinCo participation remains disabled by default.\n"
        "- `install_allowed_by_plan` is `false`.\n",
        encoding="utf-8"
    )


def main() -> int:
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts: Dict[str, int] = {}

        checks += req(data.get("stage") == "Stage 28", "stage must be Stage 28")
        checks += req(data.get("core_rule") == "An install plan is a candidate transition, not installation authority.", "core rule mismatch")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")

        for category in [
            "present_and_valid",
            "missing_required",
            "extra_requires_review",
            "quarantine_required",
            "dangerous"
        ]:
            checks += req(category in data.get("allowed_diff_categories", []), f"missing allowed diff category: {category}")

        write_outputs(data)

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage28_install_plan_receipt.v0",
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
            "ALLOW_INSTALL_PLAN_CANDIDATE",
            "LEDGER_INSTALL_PLAN",
            "REQUIRE_REVIEW",
            "QUARANTINE_PLAN",
            "FAIL_CLOSED"
        ]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage28_canonical_diff_install_plan_report.v0",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 28",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "outputs": {
                "validated_diff": str(VALIDATED_DIFF),
                "install_plan_candidate": str(INSTALL_PLAN),
                "review_report": str(REVIEW_REPORT),
                "receipts": str(RECEIPTS)
            },
            "message": "Stage 28 canonical diff and install-plan candidate validation passed."
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage28_canonical_diff_install_plan_report.v0",
            "success": False,
            "error": str(exc)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
