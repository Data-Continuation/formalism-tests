#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PATH = ROOT / "tests" / "expected_outcomes.json"
RECEIPTS_PATH = ROOT / "reports" / "sample_receipts.jsonl"

def main() -> int:
    expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
    receipts = [
        json.loads(line)
        for line in RECEIPTS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    actual = {receipt["receipt_id"]: receipt["decision"] for receipt in receipts}

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatches = {
        receipt_id: {"expected": expected[receipt_id], "actual": actual[receipt_id]}
        for receipt_id in expected
        if receipt_id in actual and expected[receipt_id] != actual[receipt_id]
    }

    if missing or extra or mismatches:
        print("Expected outcome validation failed.")
        if missing:
            print("Missing receipts:", ", ".join(missing))
        if extra:
            print("Unexpected receipts:", ", ".join(extra))
        if mismatches:
            print("Mismatches:", json.dumps(mismatches, indent=2))
        return 1

    print("Expected outcome validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
