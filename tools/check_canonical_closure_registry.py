#!/usr/bin/env python3
"""Validate the canonical-closure owner registry fail-closed."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "status/canonical_closure_registry.json"
REPORT = ROOT / "reports/canonical_closure_registry_verification.json"

EXPECTED = {
    3: ("denial-reachability", "REPRODUCTION_EVIDENCE_ONLY"),
    4: ("fi-continuity-interoperability", "CONTINUITY_INTEROPERABILITY_ONLY"),
    5: ("morrison-runtime-commit-time-scope", "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"),
    6: ("optimization-target-commit-boundary", "FORMALISM_TEST_EVIDENCE_ONLY"),
}


def main() -> int:
    errors: list[str] = []
    record = json.loads(REGISTRY.read_text(encoding="utf-8"))

    if record.get("status") != "OPEN_CANONICAL_OBLIGATIONS":
        errors.append("registry status must remain OPEN_CANONICAL_OBLIGATIONS")
    if record.get("canonical_execution_claimed") is not False:
        errors.append("canonical_execution_claimed must be false")
    if record.get("promotion_eligible") is not False:
        errors.append("promotion_eligible must be false")

    owners = record.get("owners")
    if not isinstance(owners, list):
        errors.append("owners must be a list")
        owners = []

    by_issue = {item.get("issue"): item for item in owners if isinstance(item, dict)}
    if set(by_issue) != set(EXPECTED):
        errors.append("registry must contain exactly issues 3, 4, 5, and 6")

    for issue, (family, posture) in EXPECTED.items():
        item = by_issue.get(issue, {})
        if item.get("proof_family") != family:
            errors.append(f"issue {issue} proof_family mismatch")
        if item.get("state") != "PENDING_CANONICAL_EXECUTION":
            errors.append(f"issue {issue} must remain pending")
        if item.get("authority_posture") != posture:
            errors.append(f"issue {issue} authority posture mismatch")
        if item.get("canonical_evidence_required") is not True:
            errors.append(f"issue {issue} must require canonical evidence")
        if item.get("duplicate_work_prohibited") is not True:
            errors.append(f"issue {issue} must prohibit duplicate work")

    result = {
        "schema": "stegverse.formalism-tests.canonical-closure-registry-verification.v1",
        "status": "PASS" if not errors else "FAIL",
        "owner_count": len(owners),
        "open_issue_numbers": sorted(by_issue),
        "canonical_execution_claimed": False,
        "promotion_eligible": False,
        "errors": errors,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
