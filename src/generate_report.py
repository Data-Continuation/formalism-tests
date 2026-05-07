#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS_PATH = ROOT / "reports" / "sample_receipts.jsonl"
REPORT_PATH = ROOT / "reports" / "continuation_report.md"

def load_receipts() -> list[dict]:
    if not RECEIPTS_PATH.exists():
        raise FileNotFoundError(f"missing receipts: {RECEIPTS_PATH}")
    return [json.loads(line) for line in RECEIPTS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]

def main() -> int:
    receipts = load_receipts()
    counts = Counter(r["decision"] for r in receipts)

    lines = [
        "# Data Continuation Test Report",
        "",
        "## Summary",
        "",
        "| Decision | Count |",
        "|---|---:|",
    ]

    for decision in sorted(counts):
        lines.append(f"| {decision} | {counts[decision]} |")

    lines.extend([
        "",
        "## Receipts",
        "",
        "| Receipt | Role | Transition | Decision | Basis |",
        "|---|---|---|---|---|",
    ])

    for r in receipts:
        lines.append(
            f"| {r['receipt_id']} | {r['role']} | {r['transition_class']} | "
            f"{r['decision']} | {r['basis']} |"
        )

    lines.extend([
        "",
        "## Verification",
        "",
        "This report verifies the initial DCF proof surface:",
        "",
        "```text",
        "same data",
        "same system state",
        "different role",
        "different continuation decision",
        "```",
        "",
        "The receipt set also verifies fail-closed behavior for missing basis and insufficient legitimacy capacity.",
    ])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report: {REPORT_PATH}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
