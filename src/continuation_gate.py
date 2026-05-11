#!/usr/bin/env python3
"""
Continuation gate for Data-Continuation/formalism-tests.

This gate is intentionally schema-tolerant.

It supports:

1. Legacy continuation cases that contain a `state` field.
2. New boundary-dynamics scenarios that contain:
   - boundary_integrity
   - recoverability
   - purpose_convergence
   - system_coherence
   - multi_body_coupling_risk
   - uncertainty
   - boundary_can_evolve
   - reset_path_available
   - immediate_harm_risk

The old failure was caused by assuming every case had `case["state"]`.
That is no longer valid after adding boundary-dynamics fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


REPORT_PATH = Path("continuation_gate_report.json")

BOUNDARY_REQUIRED_FIELDS = {
    "boundary_integrity",
    "recoverability",
    "purpose_convergence",
    "system_coherence",
    "multi_body_coupling_risk",
    "uncertainty",
    "boundary_can_evolve",
    "reset_path_available",
    "immediate_harm_risk",
}


def clamp_score(value: Any, field: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    score = float(value)
    if score < 0.0 or score > 1.0:
        raise ValueError(f"{field} must be between 0 and 1")
    return score


def require_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def fixture_paths() -> List[Path]:
    roots = [
        Path("tests/fixtures"),
        Path("fixtures"),
        Path("tests"),
    ]

    paths: List[Path] = []
    for root in roots:
        if root.exists():
            paths.extend(sorted(root.glob("*.json")))

    return sorted(set(paths))


def extract_cases(payload: Any, source: str) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        if isinstance(payload.get("scenarios"), list):
            return [normalize_case(case, source) for case in payload["scenarios"]]

        if isinstance(payload.get("cases"), list):
            return [normalize_case(case, source) for case in payload["cases"]]

        return [normalize_case(payload, source)]

    if isinstance(payload, list):
        return [normalize_case(case, source) for case in payload]

    raise ValueError(f"{source} must contain a JSON object or list")


def normalize_case(case: Any, source: str) -> Dict[str, Any]:
    if not isinstance(case, dict):
        raise ValueError(f"{source} contains a non-object case")

    normalized = dict(case)
    normalized["_source"] = source
    return normalized


def load_cases() -> List[Dict[str, Any]]:
    paths = fixture_paths()

    if not paths:
        return [
            {
                "case_id": "default_empty_repo_case",
                "state": "unknown",
                "expected": "FAIL_CLOSED",
                "_source": "generated-default",
            }
        ]

    cases: List[Dict[str, Any]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases.extend(extract_cases(payload, str(path)))

    return cases


def is_boundary_case(case: Dict[str, Any]) -> bool:
    return BOUNDARY_REQUIRED_FIELDS.issubset(case.keys())


def decide_boundary_case(case: Dict[str, Any]) -> Dict[str, Any]:
    scenario_id = str(
        case.get("scenario_id")
        or case.get("case_id")
        or case.get("id")
        or "unnamed_boundary_scenario"
    )

    boundary_integrity = clamp_score(case.get("boundary_integrity"), "boundary_integrity")
    recoverability = clamp_score(case.get("recoverability"), "recoverability")
    purpose_convergence = clamp_score(case.get("purpose_convergence"), "purpose_convergence")
    system_coherence = clamp_score(case.get("system_coherence"), "system_coherence")
    multi_body_coupling_risk = clamp_score(
        case.get("multi_body_coupling_risk"),
        "multi_body_coupling_risk",
    )
    uncertainty = clamp_score(case.get("uncertainty"), "uncertainty")

    boundary_can_evolve = require_bool(case.get("boundary_can_evolve"), "boundary_can_evolve")
    reset_path_available = require_bool(case.get("reset_path_available"), "reset_path_available")
    immediate_harm_risk = require_bool(case.get("immediate_harm_risk"), "immediate_harm_risk")

    reasons: List[str] = []

    if uncertainty >= 0.70:
        outcome = "FAIL_CLOSED"
        reasons.append("uncertainty exceeds fail-closed threshold")

    elif immediate_harm_risk and recoverability < 0.50:
        outcome = "DENY"
        reasons.append("immediate harm risk with insufficient recoverability")

    elif boundary_integrity < 0.35 and recoverability < 0.50:
        outcome = "DENY"
        reasons.append("boundary integrity and recoverability are both below minimum")

    elif purpose_convergence < 0.35 and reset_path_available:
        outcome = "RESET_BOUNDARY"
        reasons.append("purpose convergence is failing but a reset path exists")

    elif system_coherence < 0.45 and boundary_can_evolve and recoverability >= 0.50:
        outcome = "EVOLVE_BOUNDARY"
        reasons.append("system coherence is degraded and bounded boundary evolution is available")

    elif multi_body_coupling_risk > 0.75 and system_coherence < 0.60:
        outcome = "FAIL_CLOSED"
        reasons.append("high coupling risk with insufficient system coherence")

    elif (
        boundary_integrity >= 0.60
        and recoverability >= 0.60
        and purpose_convergence >= 0.60
        and system_coherence >= 0.60
        and multi_body_coupling_risk <= 0.60
        and uncertainty < 0.50
    ):
        outcome = "ALLOW"
        reasons.append("boundary is recoverable, convergent, coherent, and coupling risk is bounded")

    else:
        outcome = "FAIL_CLOSED"
        reasons.append("scenario does not satisfy allow thresholds and lacks a clean reset/evolution path")

    return {
        "id": scenario_id,
        "source": case.get("_source"),
        "schema": "boundary_dynamics",
        "outcome": outcome,
        "scores": {
            "boundary_integrity": boundary_integrity,
            "recoverability": recoverability,
            "purpose_convergence": purpose_convergence,
            "system_coherence": system_coherence,
            "multi_body_coupling_risk": multi_body_coupling_risk,
            "uncertainty": uncertainty,
        },
        "flags": {
            "boundary_can_evolve": boundary_can_evolve,
            "reset_path_available": reset_path_available,
            "immediate_harm_risk": immediate_harm_risk,
        },
        "reasons": reasons,
    }


def decide_legacy_state_case(case: Dict[str, Any]) -> Dict[str, Any]:
    case_id = str(
        case.get("case_id")
        or case.get("scenario_id")
        or case.get("id")
        or "unnamed_legacy_case"
    )

    state_raw = case.get("state", "unknown")
    state = str(state_raw).strip().lower()

    expected = case.get("expected")
    reasons: List[str] = []

    if state in {"ok", "allow", "allowed", "valid", "green", "pass"}:
        outcome = "ALLOW"
        reasons.append("legacy state maps to allow")

    elif state in {"deny", "denied", "invalid", "red", "blocked"}:
        outcome = "DENY"
        reasons.append("legacy state maps to deny")

    elif state in {"fail_closed", "fail-closed", "unknown", "uncertain", ""}:
        outcome = "FAIL_CLOSED"
        reasons.append("legacy state maps to fail-closed")

    else:
        outcome = "FAIL_CLOSED"
        reasons.append(f"unrecognized legacy state: {state_raw!r}")

    matched_expected = None
    if expected is not None:
        matched_expected = str(expected).strip().upper() == outcome

    return {
        "id": case_id,
        "source": case.get("_source"),
        "schema": "legacy_state",
        "outcome": outcome,
        "state": state_raw,
        "expected": expected,
        "matched_expected": matched_expected,
        "reasons": reasons,
    }


def decide(case: Dict[str, Any]) -> Dict[str, Any]:
    if is_boundary_case(case):
        return decide_boundary_case(case)

    return decide_legacy_state_case(case)


def main() -> int:
    receipts = [decide(case) for case in load_cases()]

    failures = [
        receipt
        for receipt in receipts
        if receipt.get("matched_expected") is False
    ]

    report = {
        "gate": "continuation_gate",
        "version": "0.2.0",
        "receipt_count": len(receipts),
        "success": len(failures) == 0,
        "receipts": receipts,
        "failures": failures,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2, sort_keys=True))

    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
