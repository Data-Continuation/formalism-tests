#!/usr/bin/env python3
"""Validate the Morrison Runtime canonical-evidence gate.

This check is intentionally fail-closed. Before canonical execution exists, it verifies
that the pending evidence record is explicit and cannot be mistaken for verified proof.
After a canonical evidence record is added, it validates the same contract represented
by schemas/morrison_runtime_canonical_execution_evidence.schema.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "receipts/morrison_runtime_canonical_execution_evidence.pending.json"
CANONICAL = ROOT / "receipts/morrison_runtime_canonical_execution_evidence.json"
OUTPUT = ROOT / "reports/morrison_runtime_canonical_evidence_gate.json"
AUTHORITY = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"
SUITE_ID = "morrison-runtime-commit-time-scope-v0.1"
REPOSITORY = "Data-Continuation/formalism-tests"
SCHEMA_ID = "stegverse.morrison-runtime.canonical-execution-evidence.v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
APPROVED_SURFACES = {"GITHUB_ACTIONS", "REPOSITORY_CHECKOUT", "EXISTING_CI"}
REQUIRED_TASKS = {
    "morrison_runtime_commit_time_scope_tests",
    "verify_morrison_runtime_commit_time_scope_artifacts",
}
REQUIRED_COMMAND_FRAGMENTS = {
    "--task-id morrison_runtime_commit_time_scope_tests",
    "--task-id verify_morrison_runtime_commit_time_scope_artifacts",
    "--task-id check_morrison_runtime_canonical_evidence_gate",
}


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_commands(commands: object, *, require_gate_command: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(commands, list) or not all(isinstance(item, str) for item in commands):
        return ["commands must be an array of strings"]
    required = set(REQUIRED_COMMAND_FRAGMENTS)
    if not require_gate_command:
        required.remove("--task-id check_morrison_runtime_canonical_evidence_gate")
    for fragment in required:
        if not any(fragment in command for command in commands):
            errors.append(f"commands must include {fragment}")
    return errors


def validate_pending(record: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema": "stegverse.morrison-runtime.canonical-execution-evidence.pending.v1",
        "suite_id": SUITE_ID,
        "status": "PENDING_CANONICAL_EXECUTION",
        "promotion_prohibited_until_complete": True,
        "authority_posture": AUTHORITY,
        "repository": REPOSITORY,
        "issue": 5,
        "required_schema": "schemas/morrison_runtime_canonical_execution_evidence.schema.json",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"pending.{key} must equal {value!r}")
    errors.extend(
        f"pending.{error}"
        for error in validate_commands(record.get("required_commands"), require_gate_command=True)
    )
    return errors


def validate_canonical(record: dict) -> list[str]:
    errors: list[str] = []
    expected_constants = {
        "schema": SCHEMA_ID,
        "suite_id": SUITE_ID,
        "repository": REPOSITORY,
        "authority_posture": AUTHORITY,
        "status": "VERIFIED_CANONICAL_RUN",
    }
    for key, value in expected_constants.items():
        if record.get(key) != value:
            errors.append(f"canonical.{key} must equal {value!r}")

    if not SHA40.fullmatch(str(record.get("commit_sha", ""))):
        errors.append("canonical.commit_sha must be a lowercase 40-character SHA")
    if record.get("execution_surface") not in APPROVED_SURFACES:
        errors.append("canonical.execution_surface must be an approved canonical surface")

    errors.extend(
        f"canonical.{error}"
        for error in validate_commands(record.get("commands"), require_gate_command=False)
    )

    task_results = record.get("task_results")
    if not isinstance(task_results, dict) or set(task_results) != REQUIRED_TASKS:
        errors.append("canonical.task_results must contain exactly both execution tasks")
    elif any(task_results.get(task) != "PASS" for task in REQUIRED_TASKS):
        errors.append("both canonical execution task results must equal PASS")

    artifact_hashes = record.get("artifact_hashes")
    required_hashes = {"report_sha256", "receipts_sha256", "verification_sha256"}
    if not isinstance(artifact_hashes, dict) or set(artifact_hashes) != required_hashes:
        errors.append("canonical.artifact_hashes must contain exactly report, receipts, and verification hashes")
    else:
        for field in sorted(required_hashes):
            if not SHA256.fullmatch(str(artifact_hashes.get(field, ""))):
                errors.append(f"canonical.artifact_hashes.{field} must be a lowercase SHA-256")

    equivalence = record.get("artifact_equivalence")
    required_equivalence = {"report", "receipts", "expected_outcomes"}
    if not isinstance(equivalence, dict) or set(equivalence) != required_equivalence:
        errors.append("canonical.artifact_equivalence must contain exactly report, receipts, and expected_outcomes")
    else:
        for field in sorted(required_equivalence):
            if equivalence.get(field) is not True:
                errors.append(f"canonical.artifact_equivalence.{field} must be true")

    allowed_fields = {
        "schema", "suite_id", "repository", "commit_sha", "execution_surface",
        "run_url", "executed_at", "commands", "task_results", "artifact_hashes",
        "artifact_equivalence", "authority_posture", "status", "notes",
    }
    extras = sorted(set(record) - allowed_fields)
    if extras:
        errors.append(f"canonical contains schema-prohibited fields: {extras}")
    return errors


def main() -> int:
    errors: list[str] = []
    mode: str

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
        "schema": "stegverse.morrison-runtime.canonical-evidence-gate-result.v1",
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
