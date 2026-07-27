#!/usr/bin/env python3
"""Validate the formalism proof package registry fail-closed."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/formalism_proof_package_registry.json"
OUTPUT = ROOT / "reports/formalism_proof_package_registry_verification.json"

REQUIRED_PACKAGES = {
    "denial-reachability",
    "fi-transition-continuity-interoperability",
    "morrison-runtime-commit-time-scope",
    "optimization-target-commit-boundary",
}
REQUIRED_ISSUES = {3, 4, 5, 6}
EXPECTED_PACKAGE_CONTRACTS = {
    "denial-reachability": {
        "issue": 3,
        "authority_posture": "REPRODUCTION_EVIDENCE_ONLY",
        "bounded_result": "PASS",
    },
    "fi-transition-continuity-interoperability": {
        "issue": 4,
        "authority_posture": "CONTINUITY_INTEROPERABILITY_ONLY",
        "bounded_result": "PASS",
    },
    "morrison-runtime-commit-time-scope": {
        "issue": 5,
        "authority_posture": "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY",
        "bounded_result": "PASS",
    },
    "optimization-target-commit-boundary": {
        "issue": 6,
        "authority_posture": "FORMALISM_TEST_EVIDENCE_ONLY",
        "bounded_result": "CONNECTOR_REPRODUCTION_PASS",
        "package_handoff": "docs/formalisms/OPTIMIZATION_TARGET_COMMIT_BOUNDARY_MIRROR_HANDOFF.md",
        "required_surface": "receipts/optimization_target_connector_materialized_reproduction.json",
    },
}
FALSE_AUTHORITY_FIELDS = {
    "execution_authority_granted",
    "publication_authority_granted",
    "release_authority_granted",
    "certification_authority_granted",
    "financial_authority_granted",
    "sovereign_authority_granted",
}


def main() -> int:
    errors: list[str] = []
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        registry = {}

    if registry.get("schema") != "stegverse.formalism-tests.proof-package-registry.v1":
        errors.append("registry schema mismatch")
    if registry.get("repository") != "Data-Continuation/formalism-tests":
        errors.append("repository mismatch")
    if registry.get("source_of_truth") != "FORMALISM_TESTS_MIRROR_HANDOFF.md":
        errors.append("source_of_truth mismatch")

    boundary = registry.get("authority_boundary")
    if not isinstance(boundary, dict):
        errors.append("authority_boundary must be an object")
    else:
        if set(boundary) != FALSE_AUTHORITY_FIELDS:
            errors.append("authority_boundary fields mismatch")
        for field in FALSE_AUTHORITY_FIELDS:
            if boundary.get(field) is not False:
                errors.append(f"{field} must remain false")

    packages = registry.get("packages")
    if not isinstance(packages, list):
        errors.append("packages must be an array")
        packages = []

    package_ids = [item.get("package_id") for item in packages if isinstance(item, dict)]
    if set(package_ids) != REQUIRED_PACKAGES:
        errors.append("registered package set mismatch")
    if len(package_ids) != len(set(package_ids)):
        errors.append("duplicate package_id detected")

    package_owner_issues: list[int] = []
    for package in packages:
        if not isinstance(package, dict):
            errors.append("package entry must be an object")
            continue
        package_id = package.get("package_id", "<unknown>")
        expected = EXPECTED_PACKAGE_CONTRACTS.get(package_id, {})

        if package.get("canonical_state") not in {
            "PENDING_CANONICAL_EXECUTION",
            "VERIFIED_CANONICAL_RUN",
        }:
            errors.append(f"{package_id}: invalid canonical_state")
        if package.get("authority_posture") != expected.get("authority_posture"):
            errors.append(f"{package_id}: authority posture mismatch")
        if package.get("bounded_result") != expected.get("bounded_result"):
            errors.append(f"{package_id}: bounded result mismatch")

        owner = package.get("canonical_owner")
        expected_issue = expected.get("issue")
        if not isinstance(owner, dict):
            errors.append(f"{package_id}: canonical_owner must be an object")
        else:
            if owner.get("repository") != "Data-Continuation/formalism-tests":
                errors.append(f"{package_id}: canonical owner repository mismatch")
            if owner.get("issue") != expected_issue:
                errors.append(
                    f"{package_id}: canonical owner issue must equal {expected_issue}"
                )
            if isinstance(owner.get("issue"), int):
                package_owner_issues.append(owner["issue"])

        if not str(package.get("downstream_activation", "")).startswith("PROHIBITED_"):
            errors.append(f"{package_id}: downstream activation must remain prohibited")

        expected_handoff = expected.get("package_handoff")
        if expected_handoff and package.get("package_handoff") != expected_handoff:
            errors.append(f"{package_id}: package handoff mismatch")

        surfaces = package.get("installed_surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            errors.append(f"{package_id}: installed_surfaces must be non-empty")
            continue
        if len(surfaces) != len(set(surfaces)):
            errors.append(f"{package_id}: duplicate installed surface")

        required_surface = expected.get("required_surface")
        if required_surface and required_surface not in surfaces:
            errors.append(f"{package_id}: required installed surface missing from registry")

        for surface in surfaces:
            path = ROOT / surface
            if not path.exists():
                errors.append(f"{package_id}: missing installed surface {surface}")

    if set(package_owner_issues) != REQUIRED_ISSUES:
        errors.append("package canonical owner set mismatch")
    if len(package_owner_issues) != len(set(package_owner_issues)):
        errors.append("duplicate package canonical owner detected")

    ownership = registry.get("active_issue_ownership")
    if not isinstance(ownership, list):
        errors.append("active_issue_ownership must be an array")
        ownership = []
    issues = [item.get("issue") for item in ownership if isinstance(item, dict)]
    if set(issues) != REQUIRED_ISSUES:
        errors.append("active issue ownership set mismatch")
    if len(issues) != len(set(issues)):
        errors.append("duplicate active issue owner detected")
    if set(issues) != set(package_owner_issues):
        errors.append("package owners and active issue ownership must match")

    policy = registry.get("policy")
    if not isinstance(policy, dict) or any(value is not True for value in policy.values()):
        errors.append("all registry policy flags must remain true")
    if registry.get("release_state") != "NOT_AUTHORIZED":
        errors.append("release_state must remain NOT_AUTHORIZED")
    if registry.get("manual_user_tasks_required") != []:
        errors.append("manual_user_tasks_required must remain empty")

    result = {
        "schema": "stegverse.formalism-tests.proof-package-registry-verification.v1",
        "status": "PASS" if not errors else "FAIL",
        "package_count": len(packages),
        "active_issue_count": len(ownership),
        "release_state": registry.get("release_state"),
        "errors": errors,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
