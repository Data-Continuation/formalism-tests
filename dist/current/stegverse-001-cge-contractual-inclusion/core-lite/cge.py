from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CGEDecision:
    decision: str
    basis: str

    def to_dict(self) -> dict[str, Any]:
        return {"decision": self.decision, "basis": self.basis}


def _declared_paths(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return []


def precheck_manifest(manifest: dict[str, Any]) -> CGEDecision:
    return CGEDecision("ALLOW_SANDBOX", "mock")


def classify_sandbox_result(result: dict[str, Any]) -> CGEDecision:
    return CGEDecision("REVIEW_REQUIRED", "mock")


def generate_cge_fingerprint(*args: Any, **kwargs: Any) -> dict[str, Any]:
    # Additive compatibility surface for core-lite CLI.
    import hashlib
    import json
    from datetime import datetime, timezone

    def _safe(value: Any) -> Any:
        try:
            json.dumps(value, sort_keys=True, default=str)
            return value
        except TypeError:
            return repr(value)

    payload = {
        "schema": "stegverse_core_lite_cge_fingerprint_input.v1",
        "args": [_safe(value) for value in args],
        "kwargs": {str(key): _safe(value) for key, value in sorted(kwargs.items())},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    input_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    return {
        "schema": "stegverse_core_lite_cge_fingerprint.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision_scope": "initialization_contractual_inclusion",
        "input_hash": input_hash,
        "available_cge_surfaces": [
            "CGEDecision",
            "precheck_manifest",
            "classify_sandbox_result",
        ],
        "install_authority": False,
        "production_authority": False,
        "node_status": False,
        "finco_eligibility": False,
    }
