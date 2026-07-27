#!/usr/bin/env python3
"""Validate denial-reachability canonical execution evidence fail-closed."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "receipts/denial_reachability_canonical_execution_evidence.pending.json"
CANONICAL = ROOT / "receipts/denial_reachability_canonical_execution_evidence.json"
OUTPUT = ROOT / "reports/denial_reachability_canonical_evidence_gate.json"
GATE_SOURCE = ROOT / "tools/check_denial_reachability_canonical_evidence_gate.py"
AUTHORITY = "REPRODUCTION_EVIDENCE_ONLY"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_COMMANDS = [
    "python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id denial_reachability_commit_boundary_tests",
    "python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id verify_denial_reachability_artifacts",
    "python tools/run_declared_tasks.py tools/tasks/denial_reachability_tasks.json --task-id check_denial_reachability_canonical_evidence_gate",
]
REQUIRED_TASKS = {
    "denial_reachability_commit_boundary_tests",
    "verify_denial_reachability_artifacts",
    "check_denial_reachability_canonical_evidence_gate",
}
REQUIRED_HASHES = {
    "report_sha256",
    "receipts_sha256",
    "artifact_verification_sha256",
    "canonical_evidence_gate_sha256",
}
REQUIRED_EQUIVALENCE = {
    "report",
    "receipts",
    "expected_outcomes",
    "canonical_evidence_gate",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_pending(record: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "status": "PENDING_CANONICAL_EXECUTION",
        "promotion_prohibited_until_complete": True,
        "authority_posture": AUTHORITY,
        "repository": "Data-Continuation/formalism-tests",
        "issue": 3,
        "required_evidence_schema": "schemas/denial_reachability_canonical_execution_evidence.schema.json",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"pending.{key} must equal {value!r}")
    if record.get("required_commands") != REQUIRED_COMMANDS:
        errors.append("pending.required_commands must equal the three declared commands in order")
    task_results = record.get("required_task_results")
    if not isinstance(task_results, dict) or set(task_results) != REQUIRED_TASKS:
        errors.append("pending.required_task_results must contain exactly all three tasks")
    elif any(task_results.get(task) != "PASS" for task in REQUIRED_TASKS):
        errors.append("pending.required_task_results values must all equal PASS")
    hashes = record.get("required_artifact_hashes")
    if not isinstance(hashes, dict) or set(hashes) != REQUIRED_HASHES:
        errors.append("pending.required_artifact_hashes must contain exactly four fields")
    elif any(hashes.get(field) != "PENDING" for field in REQUIRED_HASHES):
        errors.append("pending.required_artifact_hashes values must all equal PENDING")
    equivalence = record.get("required_artifact_equivalence")
    if not isinstance(equivalence, dict) or set(equivalence) != REQUIRED_EQUIVALENCE:
        errors.append("pending.required_artifact_equivalence must contain exactly four fields")
    elif any(equivalence.get(field) is not False for field in REQUIRED_EQUIVALENCE):
        errors.append("pending.required_artifact_equivalence values must all remain false")
    return errors


def validate_canonical(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("schema") != "stegverse.denial-reachability.canonical-execution-evidence.v1":
        errors.append("canonical.schema mismatch")
    if record.get("suite_id") != "denial-reachability-v0.1":
        errors.append("canonical.suite_id mismatch")
    if record.get("repository") != "Data-Continuation/formalism-tests":
        errors.append("canonical.repository mismatch")
    if record.get("status") != "VERIFIED_CANONICAL_RUN":
        errors.append("canonical.status must be VERIFIED_CANONICAL_RUN")
    if record.get("authority_posture") != AUTHORITY:
        errors.append(f"canonical.authority_posture must be {AUTHORITY}")
    if not SHA40.fullmatch(str(record.get("commit_sha", ""))):
        errors.append("canonical.commit_sha must be a lowercase 40-character SHA")
    if record.get("execution_surface") not in {"GITHUB_ACTIONS", "REPOSITORY_CHECKOUT", "EXISTING_CI"}:
        errors.append("canonical.execution_surface is not approved")
    if record.get("commands") != REQUIRED_COMMANDS:
        errors.append("canonical.commands must equal the three declared commands in order")
    task_results = record.get("task_results")
    if not isinstance(task_results, dict) or set(task_results) != REQUIRED_TASKS:
        errors.append("canonical.task_results must contain exactly all three declared tasks")
    elif any(task_results.get(task) != "PASS" for task in REQUIRED_TASKS):
        errors.append("all canonical task results must equal PASS")
    hashes = record.get("artifact_hashes")
    if not isinstance(hashes, dict) or set(hashes) != REQUIRED_HASHES:
        errors.append("canonical.artifact_hashes must contain exactly four required SHA-256 values")
    else:
        for field in REQUIRED_HASHES:
            if not SHA256.fullmatch(str(hashes.get(field, ""))):
                errors.append(f"canonical.artifact_hashes.{field} must be a lowercase SHA-256")
        if hashes.get("canonical_evidence_gate_sha256") != sha256(GATE_SOURCE):
            errors.append("canonical.artifact_hashes.canonical_evidence_gate_sha256 must hash the gate checker source")
    equivalence = record.get("artifact_equivalence")
    if not isinstance(equivalence, dict) or set(equivalence) != REQUIRED_EQUIVALENCE:
        errors.append("canonical.artifact_equivalence must contain exactly four required checks")
    else:
        for field in REQUIRED_EQUIVALENCE:
            if equivalence.get(field) is not True:
                errors.append(f"canonical.artifact_equivalence.{field} must be true")
    prohibited = {
        "promotion_eligible",
        "report_sha256",
        "receipts_sha256",
        "artifact_verification_sha256",
        "canonical_evidence_gate_sha256",
        "report_equivalence",
        "receipt_equivalence",
        "expected_outcome_equivalence",
        "canonical_evidence_gate_equivalence",
    }
    present = sorted(prohibited.intersection(record))
    if present:
        errors.append(f"canonical contains prohibited legacy flat fields: {present}")
    return errors


def main() -> int:
    errors: list[str] = []
    if CANONICAL.exists():
        mode = "CANONICAL_EVIDENCE_PRESENT"
        try:
            errors.extend(validate_canonical(load(CANONICAL)))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    else:
        mode = "PENDING_FAIL_CLOSED"
        try:
            errors.extend(validate_pending(load(PENDING)))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    result = {
        "schema": "stegverse.denial-reachability.canonical-evidence-gate-result.v1",
        "mode": mode,
        "status": "PASS" if not errors else "FAIL",
        "promotion_eligible": mode == "CANONICAL_EVIDENCE_PRESENT" and not errors,
        "authority_posture": AUTHORITY,
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
