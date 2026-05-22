#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPORT_PATH = Path("reports/root_docs_bulk_canonicalization_report.json")
RECEIPT_PATH = Path("receipts/root_docs_bulk_canonicalization_receipts.jsonl")
POLICY_PATH = Path("data/root_docs_canonicalization_policy.json")


ROOT_KEEP = {
    "README.md",
    "README-Plus.md",
    "ARCHITECTURE.md",
    "PRODUCT.md",
}

ROOT_MOVE_EXACT = {
    "THEOREM_PROOF_MAP.md": "docs/theorem/THEOREM_PROOF_MAP.md",
    "TASK_ID_INDEX.md": "docs/indexes/TASK_ID_INDEX.md",
    "ARTIFACT_INDEX.md": "docs/indexes/ARTIFACT_INDEX.md",
    "STAGE_1_TO_31_STATUS.md": "docs/roadmaps/STAGE_1_TO_31_STATUS.md",
    "NEXT_INTEGRATION_ROADMAP.md": "docs/roadmaps/NEXT_INTEGRATION_ROADMAP.md",
}

STAGE_PATTERNS = [
    "STAGE*.md",
    "STAGE*_*.md",
    "stage*_*.md",
]

THEOREM_LEGACY_PATTERNS = [
    "THEOREM_PROOF_MAP.stage*.md",
    "THEOREM_PROOF_MAP_STAGE*.md",
    "THEOREM_PROOF_MAP_STA*.md",
    "theorem_map_stage*.md",
    "stage*_theorem_manifest*.md",
]

BUNDLE_RESIDUE_EXACT = {
    "path_mappings.json",
    "bundle-manifest.json",
}


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def digest(obj: Dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def matches_any(name: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) for pattern in patterns)


def collision_safe_target(target: Path) -> Path:
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    index = 1

    while True:
        candidate = parent / f"{stem}.legacy-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def classify_root_file(path: Path) -> Optional[Dict[str, Any]]:
    if not path.is_file() or path.parent != Path("."):
        return None

    name = path.name

    if name in ROOT_KEEP:
        return {
            "path": name,
            "classification": "root_keep",
            "action": "preserve",
            "reason": "canonical root entrypoint or high-level repo document"
        }

    if name in ROOT_MOVE_EXACT:
        return {
            "path": name,
            "classification": "canonical_doc_move",
            "action": "move",
            "target": ROOT_MOVE_EXACT[name],
            "reason": "canonical documentation belongs under docs/"
        }

    if matches_any(name, THEOREM_LEGACY_PATTERNS):
        return {
            "path": name,
            "classification": "legacy_theorem_doc_move",
            "action": "move",
            "target": f"docs/legacy/theorem/{name}",
            "reason": "superseded theorem proof map fragment belongs under docs/legacy/theorem/"
        }

    if matches_any(name, STAGE_PATTERNS):
        return {
            "path": name,
            "classification": "stage_doc_move",
            "action": "move",
            "target": f"docs/stages/{name}",
            "reason": "stage-generated documentation belongs under docs/stages/"
        }

    if name.endswith(".md") and name not in ROOT_KEEP:
        return {
            "path": name,
            "classification": "unclassified_root_markdown_move",
            "action": "move",
            "target": f"docs/legacy/root-markdown/{name}",
            "reason": "non-canonical root markdown belongs under docs/legacy/root-markdown/"
        }

    if name in BUNDLE_RESIDUE_EXACT:
        return {
            "path": name,
            "classification": "bundle_residue_move",
            "action": "move",
            "target": f"docs/legacy/bundles/{name}",
            "reason": "bundle residue belongs under docs/legacy/bundles/"
        }

    return None


def ensure_policy_file() -> None:
    if POLICY_PATH.exists():
        return

    POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)
    policy = {
        "schema": "stegverse_root_docs_canonicalization_policy.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rule": "Build-stage processes must place generated documentation under docs/, not at repository root.",
        "root_keep": sorted(ROOT_KEEP),
        "root_move_exact": ROOT_MOVE_EXACT,
        "stage_patterns": STAGE_PATTERNS,
        "theorem_legacy_patterns": THEOREM_LEGACY_PATTERNS,
        "delete_files": False,
        "overwrite_files": False,
        "collision_strategy": "append .legacy-N before suffix"
    }
    POLICY_PATH.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ensure_policy_file()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for path in sorted(Path(".").iterdir(), key=lambda p: p.name.lower()):
        classified = classify_root_file(path)
        if classified is None:
            continue

        if classified["action"] != "move":
            classified["executed"] = False
            classified["before_sha256"] = sha256_file(path)
            entries.append(classified)
            continue

        source = Path(classified["path"])
        target = collision_safe_target(Path(classified["target"]))
        target.parent.mkdir(parents=True, exist_ok=True)

        before_hash = sha256_file(source)
        shutil.move(str(source), str(target))
        after_hash = sha256_file(target)

        classified["executed"] = True
        classified["target"] = target.as_posix()
        classified["before_sha256"] = before_hash
        classified["after_sha256"] = after_hash
        classified["preserved"] = before_hash == after_hash
        entries.append(classified)

    counts: Dict[str, int] = {}
    moved_count = 0
    preserved_count = 0

    for item in entries:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
        if item.get("executed"):
            moved_count += 1
            if item.get("preserved"):
                preserved_count += 1

    report = {
        "schema": "stegverse_root_docs_bulk_canonicalization_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": True,
        "rule": "Build-stage processes must place generated documentation under docs/, not at repository root.",
        "delete_files": False,
        "overwrite_files": False,
        "moved_count": moved_count,
        "preserved_hash_count": preserved_count,
        "classification_counts": counts,
        "entries": entries,
        "policy": str(POLICY_PATH)
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    receipt = {
        "schema": "stegverse_root_docs_bulk_canonicalization_receipt.v1",
        "generated_at": report["generated_at"],
        "decision": "ALLOW_OWNER_AUTHORIZED_BULK_CANONICALIZATION",
        "basis": "Root generated documentation was moved under docs/ without deletion or overwrite.",
        "moved_count": moved_count,
        "delete_files": False,
        "overwrite_files": False,
        "report": str(REPORT_PATH)
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
