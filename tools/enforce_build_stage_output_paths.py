#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


POLICY_PATH = Path("data/build_stage_output_policy.json")
REPORT_PATH = Path("reports/build_stage_output_path_policy_report.json")
PLAN_PATH = Path("reports/root_doc_canonicalization_plan.json")
RECEIPT_PATH = Path("receipts/build_stage_output_path_policy_receipts.jsonl")


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_policy() -> Dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def matches_any(name: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def classify_root_file(path: Path, policy: Dict[str, Any]) -> Dict[str, Any] | None:
    if not path.is_file() or path.parent != Path("."):
        return None

    name = path.name
    if name in set(policy.get("root_markdown_allowed", [])):
        return {
            "path": name,
            "classification": "root_allowed",
            "proposed_action": "preserve"
        }

    if name.endswith(".md"):
        if matches_any(name, policy.get("root_markdown_deprecated", [])):
            target = "docs/stages/" + name
            if name.startswith("THEOREM_PROOF_MAP") or "theorem" in name.lower():
                target = "docs/legacy/theorem/" + name
            return {
                "path": name,
                "classification": "root_doc_deprecated",
                "proposed_action": "move_after_review",
                "target": target
            }
        return {
            "path": name,
            "classification": "root_markdown_requires_review",
            "proposed_action": "review"
        }

    if name in {"path_mappings.json", "bundle-manifest.json"}:
        return {
            "path": name,
            "classification": "bundle_residue_candidate",
            "proposed_action": "review_for_legacy_move",
            "target": "docs/legacy/bundles/" + name
        }

    return None


def main() -> int:
    policy = load_policy()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

    items = []
    for child in sorted(Path(".").iterdir(), key=lambda p: p.name.lower()):
        item = classify_root_file(child, policy)
        if item:
            items.append(item)

    counts: Dict[str, int] = {}
    for item in items:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1

    success = counts.get("root_doc_deprecated", 0) == 0 and counts.get("root_markdown_requires_review", 0) == 0

    report = {
        "schema": "stegverse_build_stage_output_path_policy_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": success,
        "policy_id": policy.get("policy_id"),
        "rule": policy.get("rule"),
        "classification_counts": counts,
        "items": items,
        "note": "This task reports and plans canonicalization. It does not move or delete files."
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    plan = {
        "schema": "stegverse_root_doc_canonicalization_plan.v1",
        "generated_at": report["generated_at"],
        "install_authority": False,
        "delete_authority": False,
        "move_authority": False,
        "requires_review": True,
        "moves": [
            {
                "from": item["path"],
                "to": item.get("target"),
                "classification": item["classification"]
            }
            for item in items
            if item.get("target")
        ],
        "core_rule": "Build-stage processes must place generated documentation under docs/, not at repository root."
    }
    PLAN_PATH.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_build_stage_output_path_policy_receipt.v1",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_REPORT_ONLY" if items else "ALLOW_CLEAN_ROOT",
        "basis": "Root documentation placement was evaluated without moving or deleting files.",
        "success": success,
        "classification_counts": counts,
        "report": str(REPORT_PATH),
        "plan": str(PLAN_PATH)
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
