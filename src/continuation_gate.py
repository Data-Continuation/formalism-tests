#!/usr/bin/env python3
"""
Data Continuation Formalism — minimal continuation gate.

Run:
  python src/continuation_gate.py

Outputs:
  reports/sample_receipts.jsonl
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests"
REPORT_DIR = ROOT / "reports"
RECEIPTS_PATH = REPORT_DIR / "sample_receipts.jsonl"


@dataclass(frozen=True)
class State:
    governance_capacity: float
    control_authority: float
    trust_basis: float
    k: float = 1.0
    alpha: float = 1.0
    beta: float = 1.0
    gamma: float = 1.0

    def legitimacy_capacity(self) -> float:
        return (
            self.k
            * math.pow(self.governance_capacity, self.alpha)
            * math.pow(self.control_authority, self.beta)
            * math.pow(self.trust_basis, self.gamma)
        )


def load_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(TEST_DIR.glob("*.json")):
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(loaded, list):
            cases.extend(loaded)
        else:
            cases.append(loaded)
    return cases


def block_passes(case: dict[str, Any], block: str) -> bool | None:
    block_results = case.get("block_results", {})
    if block not in block_results:
        return None
    return bool(block_results[block])


def decide(case: dict[str, Any]) -> dict[str, Any]:
    state_raw = case["state"]
    state = State(
        governance_capacity=float(state_raw["governance_capacity"]),
        control_authority=float(state_raw["control_authority"]),
        trust_basis=float(state_raw["trust_basis"]),
        k=float(state_raw.get("k", 1.0)),
        alpha=float(state_raw.get("alpha", 1.0)),
        beta=float(state_raw.get("beta", 1.0)),
        gamma=float(state_raw.get("gamma", 1.0)),
    )

    consequence_mass = float(case["consequence_mass"])
    legitimacy_capacity = state.legitimacy_capacity()
    capacity_gap = legitimacy_capacity - consequence_mass

    required_blocks = list(case.get("required_blocks", []))
    evaluated_blocks: dict[str, str] = {}

    missing_basis = False
    failed_blocks: list[str] = []

    for block in required_blocks:
        result = block_passes(case, block)
        if result is None:
            evaluated_blocks[block] = "UNKNOWN"
            missing_basis = True
        elif result is True:
            evaluated_blocks[block] = "PASS"
        else:
            evaluated_blocks[block] = "FAIL"
            failed_blocks.append(block)

    signoff_required = "human_signoff_required" in required_blocks

    if missing_basis:
        decision = "FAIL_CLOSED"
        basis = "missing required block basis"
    elif capacity_gap < 0:
        decision = "FAIL_CLOSED"
        basis = "consequence mass exceeds legitimacy capacity"
    elif failed_blocks:
        decision = "DENY"
        basis = "one or more required blocks failed"
    elif signoff_required:
        decision = "ALLOW_WITH_SIGNOFF"
        basis = "capacity sufficient and required blocks passed; signoff required"
    else:
        decision = "ALLOW"
        basis = "capacity sufficient and required blocks passed"

    return {
        "receipt_id": case["case_id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data_id": case["data_id"],
        "data": case["data"],
        "role": case["role"],
        "transition_class": case["transition_class"],
        "consequence_mass": consequence_mass,
        "legitimacy_capacity": round(legitimacy_capacity, 6),
        "capacity_gap": round(capacity_gap, 6),
        "required_blocks": required_blocks,
        "block_results": evaluated_blocks,
        "decision": decision,
        "basis": basis,
    }


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    receipts = [decide(case) for case in load_cases()]

    with RECEIPTS_PATH.open("w", encoding="utf-8") as handle:
        for receipt in receipts:
            handle.write(json.dumps(receipt, sort_keys=True) + "\n")

    for receipt in receipts:
        print(
            f"{receipt['receipt_id']}: "
            f"{receipt['role']} -> {receipt['decision']} "
            f"({receipt['basis']})"
        )

    print(f"Wrote receipts: {RECEIPTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
