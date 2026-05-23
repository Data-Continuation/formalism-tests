#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MILESTONES = Path("tracking/stegverse-001/roadmap_milestones.json")
REPORT_DIR = Path("reports/current/stegverse-001-roadmap")
RECEIPT_DIR = Path("receipts/current/stegverse-001-roadmap")
REPORT_JSON = REPORT_DIR / "milestone_status_report.json"
REPORT_MD = REPORT_DIR / "milestone_status_report.md"
RECEIPTS = RECEIPT_DIR / "receipts.jsonl"


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_dict(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def last_receipt_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    last = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            last = json.loads(line).get("receipt_hash")
        except json.JSONDecodeError:
            continue
    return last


def write_receipt(report: dict[str, Any]) -> dict[str, Any]:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema": "stegverse_001_roadmap_receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "actor": "StegVerse-001",
        "event_type": "roadmap_milestones_tracked",
        "decision": "STATUS_REPORTED",
        "basis": "Roadmap milestones were read and current status was reported.",
        "previous_receipt_hash": last_receipt_hash(RECEIPTS),
        "report_hash": hash_dict(report),
        "report": REPORT_JSON.as_posix(),
    }
    receipt["receipt_hash"] = hash_dict(receipt)
    with RECEIPTS.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(receipt) + "\n")
    return receipt


def status_counts(milestones: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for milestone in milestones:
        status = str(milestone.get("status", "UNKNOWN"))
        counts[status] = counts.get(status, 0) + 1
    return dict(sorted(counts.items()))


def write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# StegVerse-001 Roadmap Milestone Status",
        "",
        "## Status",
        "",
        "```text",
        f"actor: {report['actor']}",
        f"roadmap: {report['roadmap']}",
        f"active_gate: {report['active_gate']}",
        f"milestone_count: {report['milestone_count']}",
        "```",
        "",
        "## Status Counts",
        "",
        "```text",
    ]
    for status, count in report["status_counts"].items():
        lines.append(f"{status}: {count}")
    lines.extend(["```", "", "## Milestones", ""])

    for milestone in report["milestones"]:
        lines.extend([
            f"### {milestone['id']} — {milestone['name']}",
            "",
            "```text",
            f"status: {milestone['status']}",
            f"transition: {milestone['transition']}",
            "```",
            "",
        ])

    lines.extend([
        "## Operating Rule",
        "",
        "```text",
        report["operating_rule"],
        "```",
    ])
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not MILESTONES.exists():
        failure = {
            "schema": "stegverse_001_roadmap_status_report.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "error": "missing_milestones_file",
            "missing": MILESTONES.as_posix(),
        }
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    data = json.loads(MILESTONES.read_text(encoding="utf-8"))
    milestones = data.get("milestones", [])
    report = {
        "schema": "stegverse_001_roadmap_status_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": True,
        "actor": data.get("actor", "StegVerse-001"),
        "roadmap": data.get("roadmap", "Full Transition Table AI Block Build"),
        "active_gate": data.get("active_gate"),
        "operating_rule": data.get("operating_rule"),
        "milestone_count": len(milestones),
        "status_counts": status_counts(milestones),
        "milestones": milestones,
    }

    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report)
    receipt = write_receipt(report)
    print(json.dumps({"report": report, "receipt": receipt}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
