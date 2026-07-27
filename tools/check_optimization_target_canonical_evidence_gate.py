#!/usr/bin/env python3
"""Validate optimization-target canonical execution evidence fail-closed."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "receipts/optimization_target_canonical_execution_evidence.pending.json"
CANONICAL = ROOT / "receipts/optimization_target_canonical_execution_evidence.json"
OUTPUT = ROOT / "reports/optimization_target_canonical_evidence_gate.json"
AUTHORITY = "FORMALISM_TEST_EVIDENCE_ONLY"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_pending(record: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "status": "PENDING_CANONICAL_EXECUTION",
        "promotion_prohibited_until_complete": True,
        "authority_posture": AUTHORITY,
        "repository": "Data-Continuation/formalism-tests",
        "issue": 6,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"pending.{key} must equal {value!r}")
    commands = record.get("required_commands")
    if not isinstance(commands, list) or len(commands) != 2:
        errors.append("pending.required_commands must contain exactly two commands")
    return errors


def validate_canonical(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("status") != "VERIFIED_CANONICAL_RUN":
        errors.append("canonical.status must be VERIFIED_CANONICAL_RUN")
    if record.get("authority_posture") != AUTHORITY:
        errors.append(f"canonical.authority_posture must be {AUTHORITY}")
    if not SHA40.fullmatch(str(record.get("commit_sha", ""))):
        errors.append("canonical.commit_sha must be a lowercase 40-character SHA")
    for field in ("report_sha256", "receipts_sha256", "artifact_verification_sha256"):
        if not SHA256.fullmatch(str(record.get(field, ""))):
            errors.append(f"canonical.{field} must be a lowercase SHA-256")
    required_tasks = {
        "optimization_target_commit_boundary_tests",
        "verify_optimization_target_commit_boundary_artifacts",
    }
    task_results = record.get("task_results")
    if not isinstance(task_results, dict) or set(task_results) != required_tasks:
        errors.append("canonical.task_results must contain exactly both declared optimization-target tasks")
    elif any(task_results.get(task) != "PASS" for task in required_tasks):
        errors.append("both canonical task results must equal PASS")
    for field in ("report_equivalence", "receipt_equivalence", "expected_outcome_equivalence"):
        if record.get(field) is not True:
            errors.append(f"canonical.{field} must be true")
    if record.get("promotion_eligible") is not True:
        errors.append("canonical.promotion_eligible must be true")
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
        "schema": "stegverse.optimization-target.canonical-evidence-gate-result.v1",
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
