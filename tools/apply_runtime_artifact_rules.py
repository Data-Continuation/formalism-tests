#!/usr/bin/env python3
"""
Apply StegVerse runtime artifact rules.

This tool is meant to be called by the existing generic declared-task workflow.
It reads a rule file and moves runtime artifacts into a legacy archive directory.

It does not create workflows.
It does not delete artifacts.
It does not move Markdown reports unless the rule explicitly says to.
"""

from __future__ import annotations

import argparse
import glob
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def load_rules(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"rule file not found: {path}")

    rules = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(rules, dict):
        raise ValueError("runtime artifact rules must be a JSON object")

    if rules.get("schema") != "stegverse_runtime_artifact_rules.v1":
        raise ValueError("unsupported runtime artifact rule schema")

    return rules


def require_string_list(rules: Dict[str, Any], key: str) -> List[str]:
    value = rules.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")

    result: List[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{key} entries must be non-empty strings")
        result.append(item)

    return result


def unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    index = 2

    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def move_file(source: Path, destination_dir: Path) -> Dict[str, str]:
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(destination_dir / source.name)

    shutil.move(str(source), str(destination))

    return {
        "from": source.as_posix(),
        "to": destination.as_posix(),
    }


def collect_pattern_matches(patterns: List[str]) -> List[Path]:
    paths: List[Path] = []

    for pattern in patterns:
        for match in glob.glob(pattern):
            path = Path(match)
            if path.is_file():
                paths.append(path)

    return sorted(set(paths))


def apply_rules(rule_path: Path) -> Dict[str, Any]:
    rules = load_rules(rule_path)

    archive_root = Path(str(rules.get("archive_root", "legacy/runtime-artifacts")))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive_dir = archive_root / timestamp

    root_artifacts = require_string_list(rules, "root_runtime_artifacts")
    report_patterns = require_string_list(rules, "generated_report_patterns")

    archive_generated_reports = bool(rules.get("archive_generated_reports", True))
    archive_markdown_reports = bool(rules.get("archive_markdown_reports", False))
    write_archive_manifest = bool(rules.get("write_archive_manifest", True))

    moved: List[Dict[str, str]] = []

    for artifact_name in root_artifacts:
        artifact_path = Path(artifact_name)
        if artifact_path.exists() and artifact_path.is_file():
            moved.append(move_file(artifact_path, archive_dir / "root"))

    if archive_generated_reports:
        for report_path in collect_pattern_matches(report_patterns):
            moved.append(move_file(report_path, archive_dir / "reports"))

    if archive_markdown_reports:
        for report_path in collect_pattern_matches(["reports/*.md"]):
            moved.append(move_file(report_path, archive_dir / "markdown-reports"))

    manifest = {
        "schema": "stegverse_runtime_archive_manifest.v1",
        "rule_file": rule_path.as_posix(),
        "rule_id": rules.get("rule_id", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "archive_dir": archive_dir.as_posix(),
        "moved_count": len(moved),
        "moved": moved,
    }

    if moved and write_archive_manifest:
        archive_dir.mkdir(parents=True, exist_ok=True)
        (archive_dir / "archive_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply runtime artifact movement rules.")
    parser.add_argument(
        "rule_file",
        nargs="?",
        default="tools/rules/runtime_artifact_rules.json",
        help="Path to runtime artifact rule JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    apply_rules(Path(args.rule_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
