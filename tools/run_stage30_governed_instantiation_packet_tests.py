#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


FIXTURE = Path("tests/fixtures/stage30_governed_instantiation_packet_cases.json")
REPORT = Path("reports/stage30_governed_instantiation_packet_report.json")
VALIDATION_REPORT = Path("reports/stage30_packet_manifest_validation_report.json")
RECEIPTS = Path("receipts/stage30_instantiation_packet_receipts.jsonl")
DIST = Path("dist/stage30")
TAR_PATH = DIST / "stegverse-core-instantiation.tar.gz"
SHA_PATH = DIST / "stegverse-core-instantiation.sha256"
MANIFEST_PATH = DIST / "stegverse-core-instantiation.manifest.json"
PACKET_RECEIPT_PATH = DIST / "stegverse-core-instantiation.receipt.json"
REPLAY_PATH = DIST / "stegverse-core-instantiation.replay.json"


def canon(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def req(ok: bool, message: str) -> int:
    if not ok:
        raise AssertionError(message)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def decide(case: Dict[str, Any]) -> tuple[str, str]:
    if not case.get("entity_active"):
        return "FAIL_CLOSED", "StegVerse-001 is not active"
    for field in [
        "packet_manifest_present",
        "packet_tar_present",
        "packet_sha_present",
        "packet_receipt_present",
        "packet_replay_present",
        "packet_hash_valid",
        "manifest_scale_profile_valid",
        "authority_boundary_present",
        "policy_scope_present",
        "discovered_state_present",
        "canonical_state_present",
        "state_diff_present",
        "install_plan_present",
    ]:
        if not case.get(field):
            return "FAIL_CLOSED", f"required packet field failed: {field}"
    if case.get("install_allowed_by_packet"):
        return "FAIL_CLOSED", "packet may not authorize installation"
    if case.get("install_allowed_by_plan"):
        return "FAIL_CLOSED", "install plan may not authorize installation"
    if not case.get("sandbox_required"):
        return "FAIL_CLOSED", "sandbox is required"
    if not case.get("cge_required"):
        return "FAIL_CLOSED", "CGE is required"
    if not case.get("receipts_required"):
        return "FAIL_CLOSED", "receipts are required"
    if not case.get("node_default_safe"):
        return "FAIL_CLOSED", "node default is unsafe"
    if not case.get("finco_default_safe"):
        return "FAIL_CLOSED", "FinCo default is unsafe"
    if case.get("creates_entitlement") and not case.get("entitlement_authority_valid"):
        return "FAIL_CLOSED", "entitlement creation requires explicit authority"
    if not case.get("leading_dot_paths_have_ios_mirror"):
        return "FAIL_CLOSED", "leading-dot paths require iosnoperiod mirror"
    if not case.get("path_mappings_present"):
        return "FAIL_CLOSED", "path mappings are required"
    if case.get("production_authority_claimed"):
        return "FAIL_CLOSED", "packet may not claim production authority"
    if case.get("packet_install_performed"):
        return "FAIL_CLOSED", "Stage 30 may not install the packet"
    if case.get("requires_review"):
        return "REQUIRE_REVIEW", case.get("review_reason", "packet requires review")
    if case.get("ledger_record_required"):
        if case.get("ledger_record_emitted"):
            return "LEDGER_PACKET", "packet ledger event recorded"
        return "FAIL_CLOSED", "packet ledger record missing"
    return "ALLOW_PACKET", "governed instantiation packet satisfies Stage 30 constraints"


def tar_add_bytes(tar: tarfile.TarFile, arcname: str, payload: bytes, mtime: int = 0) -> None:
    info = tarfile.TarInfo(arcname)
    info.size = len(payload)
    info.mtime = mtime
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(payload))


def build_packet() -> Dict[str, Any]:
    DIST.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    packet_files: Dict[str, Any] = {
        "manifest/authority_boundary.json": {
            "schema": "stegverse_authority_boundary.v0",
            "packet_authority": "formalism-tests",
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "target_unit": "core-lite",
            "install_authority": False,
            "production_authority": False
        },
        "manifest/policy_scope.json": {
            "schema": "stegverse_policy_scope.v0",
            "scale_profile": "repo_core",
            "sandbox_required": True,
            "cge_required": True,
            "receipts_required": True,
            "secret_handling_allowed": False,
            "workflow_mutation_allowed_without_review": False
        },
        "manifest/node_status.json": {
            "schema": "stegverse_node_status.v0",
            "node_participation_opt_in": False,
            "node_status": "NOT_A_NODE"
        },
        "manifest/finco_participation.json": {
            "schema": "stegverse_finco_participation.v0",
            "finco_participation_requested": False,
            "finco_participation_allowed": False
        },
        "manifest/path_mappings.json": {
            "schema": "stegverse_path_mappings.v0",
            "mappings": {
                ".github/workflows/core-lite-self-test.yml": "iosnoperiod/github/workflows/core-lite-self-test-yml",
                ".stegverse/policy.json": "iosnoperiod/stegverse/policy-json"
            }
        },
        "state/discovered_state.json": {
            "schema": "stegverse_discovered_state.v0",
            "target_unit": "core-lite",
            "detected_capabilities": ["cge", "ingestion", "receipts", "declared_tasks"],
            "node_status": "NOT_A_NODE"
        },
        "state/canonical_state.json": {
            "schema": "stegverse_canonical_state.v0",
            "target_unit": "core-lite",
            "required_capabilities": ["identity", "ingestion", "sandbox", "cge", "receipts", "quarantine"]
        },
        "state/state_diff.json": {
            "schema": "stegverse_state_diff.v0",
            "items": [
                {"path": "core_lite/cge.py", "classification": "present_and_valid"},
                {"path": "core_lite/sandbox.py", "classification": "missing_required"},
                {"path": ".github/workflows/core-lite-self-test.yml", "classification": "extra_requires_review"}
            ]
        },
        "state/install_plan_candidate.json": {
            "schema": "stegverse_install_plan_candidate.v0",
            "plan_id": "stage30-core-lite-instantiation-plan",
            "install_allowed_by_plan": False,
            "sandbox_required": True,
            "cge_required": True,
            "receipts_required": True
        },
        "payload/core-lite/README.md": "# core-lite packet payload\n\nThis payload is a proposed governed transition, not installation authority.\n",
        "reports/discovery_report.json": {
            "schema": "stegverse_packet_discovery_report.v0",
            "success": True,
            "generated_at": now
        },
        "reports/install_plan_report.json": {
            "schema": "stegverse_packet_install_plan_report.v0",
            "install_allowed_by_plan": False,
            "generated_at": now
        },
        "receipts/build_receipt.json": {
            "schema": "stegverse_packet_build_receipt.v0",
            "decision": "ALLOW_PACKET_BUILD",
            "basis": "packet was built as non-installing governed transition evidence"
        },
        "schemas/instantiation_manifest.schema.json": {
            "schema": "stegverse_instantiation_manifest_schema.v0",
            "required": ["packet_id", "packet_version", "scale_profile", "target_unit", "install_allowed_by_packet"]
        },
        "iosnoperiod/github/workflows/core-lite-self-test-yml": "# iOS-safe mirror for .github/workflows/core-lite-self-test.yml\n",
        "iosnoperiod/stegverse/policy-json": "{}\n",
        "iosnoperiod.md": "# iosnoperiod\n\nThis directory mirrors leading-dot canonical paths for iOS-safe upload and extraction.\n"
    }

    instantiation_manifest = {
        "schema": "stegverse_instantiation_manifest.v0",
        "packet_id": "stegverse-core-instantiation-stage30",
        "packet_version": "0.1.0",
        "scale_profile": "repo_core",
        "target_unit": "core-lite",
        "target_repo": "Data-Continuation/core-lite",
        "source_canonical_version": "transition-table-v1-rc2",
        "generated_at": now,
        "install_allowed_by_packet": False,
        "production_authority": False,
        "discovered_state_ref": "state/discovered_state.json",
        "canonical_state_ref": "state/canonical_state.json",
        "state_diff_ref": "state/state_diff.json",
        "install_plan_ref": "state/install_plan_candidate.json",
        "authority_boundary_ref": "manifest/authority_boundary.json",
        "policy_scope_ref": "manifest/policy_scope.json",
        "path_mappings_ref": "manifest/path_mappings.json",
        "node_participation": {
            "node_participation_opt_in": False,
            "node_status": "NOT_A_NODE"
        },
        "finco_participation": {
            "finco_participation_requested": False,
            "finco_participation_allowed": False
        },
        "payload_file_count": len(packet_files) + 1
    }
    packet_files["manifest/instantiation_manifest.json"] = instantiation_manifest

    with tarfile.open(TAR_PATH, "w:gz") as tar:
        for arcname in sorted(packet_files):
            value = packet_files[arcname]
            if isinstance(value, str):
                payload = value.encode("utf-8")
            else:
                payload = json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n"
            tar_add_bytes(tar, arcname, payload)

    tar_bytes = TAR_PATH.read_bytes()
    packet_hash = sha256_bytes(tar_bytes)
    SHA_PATH.write_text(packet_hash + "  stegverse-core-instantiation.tar.gz\n", encoding="utf-8")
    MANIFEST_PATH.write_text(json.dumps(instantiation_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    packet_receipt = {
        "schema": "stegverse_stage30_packet_receipt.v0",
        "generated_at": now,
        "packet_path": str(TAR_PATH),
        "packet_sha256": packet_hash,
        "decision": "ALLOW_PACKET",
        "basis": "packet generated as governed transition evidence; not installation authority",
        "core_rule": "The packet is portable evidence of a proposed governed transition, not installation authority."
    }
    packet_receipt["receipt_hash"] = digest(packet_receipt)
    PACKET_RECEIPT_PATH.write_text(json.dumps(packet_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    replay = {
        "schema": "stegverse_stage30_packet_replay.v0",
        "generated_at": now,
        "packet_sha256": packet_hash,
        "replay_steps": [
            "verify sha256",
            "read instantiation manifest",
            "verify install_allowed_by_packet is false",
            "verify install_plan_candidate install_allowed_by_plan is false",
            "verify node status default is NOT_A_NODE",
            "verify FinCo default is disabled",
            "route to sandbox",
            "route to CGE",
            "route to ingestion only if admitted"
        ]
    }
    REPLAY_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "packet_hash": packet_hash,
        "manifest": instantiation_manifest,
        "packet_receipt": packet_receipt,
        "replay": replay
    }


def validate_packet(data: Dict[str, Any], packet: Dict[str, Any]) -> int:
    checks = 0
    for output in data["required_packet_outputs"]:
        checks += req(Path(output).is_file(), f"missing packet output: {output}")

    sha_recorded = SHA_PATH.read_text(encoding="utf-8").split()[0]
    sha_actual = sha256_bytes(TAR_PATH.read_bytes())
    checks += req(sha_recorded == sha_actual == packet["packet_hash"], "packet sha256 mismatch")

    manifest = load_json(MANIFEST_PATH)
    checks += req(manifest.get("install_allowed_by_packet") is False, "packet must not authorize installation")
    checks += req(manifest.get("production_authority") is False, "packet must not claim production authority")
    checks += req(manifest.get("scale_profile") == "repo_core", "scale_profile must be repo_core")
    checks += req(manifest.get("node_participation", {}).get("node_status") == "NOT_A_NODE", "node must default to NOT_A_NODE")
    checks += req(manifest.get("finco_participation", {}).get("finco_participation_allowed") is False, "FinCo must default false")

    with tarfile.open(TAR_PATH, "r:gz") as tar:
        names = set(tar.getnames())

    for required_path in data["required_internal_packet_paths"]:
        checks += req(required_path in names, f"missing internal packet path: {required_path}")

    checks += req("iosnoperiod/github/workflows/core-lite-self-test-yml" in names, "missing iOS-safe workflow mirror")
    checks += req("iosnoperiod/stegverse/policy-json" in names, "missing iOS-safe stegverse mirror")

    validation_report = {
        "schema": "stegverse_stage30_packet_manifest_validation_report.v0",
        "success": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "packet_sha256": packet["packet_hash"],
        "internal_path_count": len(names),
        "install_allowed_by_packet": manifest.get("install_allowed_by_packet"),
        "node_status": manifest.get("node_participation", {}).get("node_status"),
        "finco_participation_allowed": manifest.get("finco_participation", {}).get("finco_participation_allowed")
    }
    VALIDATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_REPORT.write_text(json.dumps(validation_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return checks


def main() -> int:
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts: Dict[str, int] = {}

        checks += req(data.get("stage") == "Stage 30", "stage must be Stage 30")
        checks += req(data.get("work_entity", {}).get("entity_id") == "StegVerse-001", "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")
        checks += req(data.get("core_rule") == "The packet is portable evidence of a proposed governed transition, not installation authority.", "core rule mismatch")

        packet = build_packet()
        checks += validate_packet(data, packet)

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage30_instantiation_packet_receipt.v0",
                "case_id": case_id,
                "decision": decision,
                "basis": basis,
                "packet_sha256": packet["packet_hash"],
                "core_rule": data["core_rule"],
                "authority_boundary": data["authority_boundary"]
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in ["ALLOW_PACKET", "LEDGER_PACKET", "REQUIRE_REVIEW", "FAIL_CLOSED"]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage30_governed_instantiation_packet_report.v0",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 30",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "packet_outputs": {
                "tar_gz": str(TAR_PATH),
                "sha256": str(SHA_PATH),
                "manifest": str(MANIFEST_PATH),
                "receipt": str(PACKET_RECEIPT_PATH),
                "replay": str(REPLAY_PATH),
                "receipts": str(RECEIPTS),
                "validation_report": str(VALIDATION_REPORT)
            },
            "packet_sha256": packet["packet_hash"],
            "message": "Stage 30 governed instantiation packet validation passed."
        }
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage30_governed_instantiation_packet_report.v0",
            "success": False,
            "error": str(exc)
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
