#!/usr/bin/env python3
"""Verify committed FI continuity interoperability report against its canonical baseline."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests" / "fixtures" / "fi_transition_continuity_interop_artifact_baseline.json"
REPORT = ROOT / "reports" / "fi_transition_continuity_interop_report.json"
OUTPUT = ROOT / "reports" / "fi_transition_continuity_interop_artifact_verification.json"


def canonical_sha256(document: object) -> str:
    payload = json.dumps(document, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    actual_hash = canonical_sha256(report)
    expected_hash = baseline["canonical_report_sha256"]

    checks = {
        "canonical_report_hash_matches": actual_hash == expected_hash,
        "suite_id_matches": report.get("suite_id") == baseline.get("suite_id"),
        "suite_version_matches": report.get("suite_version") == baseline.get("suite_version"),
        "status_pass": report.get("status") == "PASS",
        "failed_zero": report.get("failed") == 0,
        "authority_posture_preserved": report.get("authority_posture") == baseline.get("authority_posture"),
    }

    valid = all(checks.values())
    result = {
        "verification_id": "FI-TRANSITION-CONTINUITY-INTEROP-ARTIFACT-VERIFY-001",
        "valid": valid,
        "expected_canonical_report_sha256": expected_hash,
        "actual_canonical_report_sha256": actual_hash,
        "checks": checks,
        "authority_posture": "REPRODUCTION_EQUIVALENCE_ONLY",
        "creates_execution_authority": False,
        "claims_cross_domain_support": False,
        "claims_universal_law": False,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
