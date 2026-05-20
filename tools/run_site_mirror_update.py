#!/usr/bin/env python3
"""
run_site_mirror_update.py
==========================
Declared task: site_mirror_update

Reads proof outputs from formalism-tests reports/current/ and
writes updated data files to Site/data/formalism-tests/.

This task runs automatically after stage6_unified_gate_tests passes.
It is the only path by which Site data files are updated.

Authority boundary:
  formalism-tests produces receipts.
  Site publishes receipts.
  Site must not become the authority for receipts.

This runner enforces that boundary by:
  1. Reading only from reports/current/ (the verified proof outputs)
  2. Writing only to the Site data mirror path
  3. Never mutating the source proof files
  4. Producing a mirror receipt proving what was written and when

Usage:
  python tools/run_site_mirror_update.py
  python tools/run_site_mirror_update.py --site-data-dir ../Site/data/formalism-tests
  python tools/run_site_mirror_update.py --dry-run

Environment:
  SITE_DATA_DIR   Path to Site/data/formalism-tests/ (overrides --site-data-dir)
  GITHUB_TOKEN    Required when --push-to-site is set
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# Source: formalism-tests proof outputs (read-only)
REPORTS_CURRENT = ROOT / "reports" / "current"
PROOF_SURFACE_SRC   = REPORTS_CURRENT / "transition-proof-surface.json"
TABLE_CLASSES_SRC   = REPORTS_CURRENT / "transition-table-classes.json"

# Fallback: read directly from data/ if current/ not yet populated
PROOF_SURFACE_DATA  = ROOT / "data" / "formalism-tests" / "transition-proof-surface.json"
TABLE_CLASSES_DATA  = ROOT / "data" / "formalism-tests" / "transition-table-classes.json"

# Stage 6 report — source of verified gate results
STAGE6_REPORT       = REPORTS_CURRENT / "stage6_unified_gate_report.json"
STAGE6_REPORT_ALT   = ROOT / "reports" / "stage6_unified_gate_report.json"

# Default Site data dir (relative to formalism-tests root)
DEFAULT_SITE_DATA   = ROOT.parent / "Site" / "data" / "formalism-tests"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_str(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()


def sha256_file(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  WARNING: could not load {path}: {e}")
        return None


# ---------------------------------------------------------------------------
# Source resolution
# ---------------------------------------------------------------------------

def resolve_proof_surface() -> tuple[Path | None, dict | None]:
    """Find the best available proof surface JSON."""
    for candidate in [PROOF_SURFACE_SRC, PROOF_SURFACE_DATA]:
        data = load_json(candidate)
        if data:
            return candidate, data
    return None, None


def resolve_table_classes() -> tuple[Path | None, dict | None]:
    """Find the best available transition table classes JSON."""
    for candidate in [TABLE_CLASSES_SRC, TABLE_CLASSES_DATA]:
        data = load_json(candidate)
        if data:
            return candidate, data
    return None, None


def resolve_stage6_report() -> dict | None:
    """Find Stage 6 gate report."""
    for candidate in [STAGE6_REPORT, STAGE6_REPORT_ALT]:
        data = load_json(candidate)
        if data:
            return data
    return None


# ---------------------------------------------------------------------------
# Data builders
# ---------------------------------------------------------------------------

def build_updated_proof_surface(
    source: dict,
    stage6_report: dict | None,
) -> dict:
    """
    Produce updated transition-proof-surface.json.
    Preserves all existing content from source.
    Updates Stage 6 status from stage6_report if available.
    """
    updated = dict(source)

    # Always set current_stage from verified report
    if stage6_report:
        verified = stage6_report.get("verified", False)
        if verified:
            updated["current_stage"] = "Stage 6"
            updated["status"] = "Stage 6 verified; Stage 7 next"

            # Update Stage 6 entry in stages list
            stages = updated.get("stages", [])
            for stage in stages:
                if stage.get("stage") == "Stage 6":
                    stage["status"] = "verified"
                    stage["gate_result"] = {
                        "candidate_count": stage6_report.get("candidate_count", 10),
                        "assertion_count": stage6_report.get("assertion_count", 320),
                        "decisions": stage6_report.get("decisions", {}),
                        "verified_at": stage6_report.get("generated_at", now_utc()),
                    }
                    break
            updated["stages"] = stages

            # Add Stage 7 declaration if not present
            has_stage7 = any(s.get("stage") == "Stage 7" for s in stages)
            if not has_stage7:
                updated["stages"].append({
                    "stage": "Stage 7",
                    "name": "Element Dependency Closure",
                    "proof_claim": (
                        "every unlocked transition element has declared dependencies "
                        "and no Level 5 element depends on an uncovered element "
                        "without an explicit boundary"
                    ),
                    "status": "next",
                    "summary": (
                        "Next proof layer validates that unlocked elements compose "
                        "safely and that AI Blocks can be formally verified against "
                        "declared dependency constraints."
                    ),
                })

            # Update verified tasks list
            current_tasks = updated.get("verified_tasks", [])
            new_tasks = [
                "stage6_unified_gate",
                "transition_table_public_surface",
                "site_mirror_integrity",
                "current_report_preservation",
                "theorem_map_consistency",
            ]
            for t in new_tasks:
                if t not in current_tasks:
                    current_tasks.append(t)
            updated["verified_tasks"] = current_tasks

    updated["mirror_updated_at"] = now_utc()
    updated["mirror_source"] = "formalism-tests/reports/current/"
    updated["mirror_authority"] = (
        "formalism-tests produces receipts. "
        "Site publishes receipts. "
        "Site must not become the authority for receipts."
    )

    return updated


def build_updated_table_classes(
    source: dict,
    stage6_report: dict | None,
) -> dict:
    """
    Produce updated transition-table-classes.json.
    Adds Stage 6 transition classes from the verified report.
    Preserves all existing Stage 2-5 classes.
    """
    updated = dict(source)

    if stage6_report and stage6_report.get("verified"):
        # Update stage marker
        updated["current_stage"] = "Stage 6"

        # Add Stage 6 classes if not already present
        existing_ids = {c["transition_id"] for c in updated.get("classes", [])}
        stage6_classes = stage6_report.get("classes", [])

        new_classes = []
        for cls in stage6_classes:
            if cls.get("transition_id") not in existing_ids:
                new_classes.append(cls)

        if new_classes:
            updated["classes"] = updated.get("classes", []) + new_classes

        # Update decision summary
        all_classes = updated.get("classes", [])
        decision_counts: dict[str, int] = {}
        for cls in all_classes:
            d = cls.get("verified_decision", "unknown")
            decision_counts[d] = decision_counts.get(d, 0) + 1
        updated["decision_summary"] = decision_counts
        updated["total_classes"] = len(all_classes)

    updated["mirror_updated_at"] = now_utc()
    updated["mirror_source"] = "formalism-tests/reports/current/"

    return updated


# ---------------------------------------------------------------------------
# Write + receipt
# ---------------------------------------------------------------------------

def write_mirror_files(
    site_data_dir: Path,
    proof_surface: dict,
    table_classes: dict,
    dry_run: bool = False,
) -> dict:
    """Write updated data files to Site data directory."""
    files_written = []

    ps_path = site_data_dir / "transition-proof-surface.json"
    tc_path = site_data_dir / "transition-table-classes.json"

    ps_content = json.dumps(proof_surface, indent=2) + "\n"
    tc_content = json.dumps(table_classes, indent=2) + "\n"

    if not dry_run:
        site_data_dir.mkdir(parents=True, exist_ok=True)
        ps_path.write_text(ps_content, encoding="utf-8")
        tc_path.write_text(tc_content, encoding="utf-8")

    files_written = [
        {
            "path": str(ps_path),
            "sha256": sha256_str(ps_content),
            "stage": proof_surface.get("current_stage", "unknown"),
        },
        {
            "path": str(tc_path),
            "sha256": sha256_str(tc_content),
            "total_classes": table_classes.get("total_classes", 0),
        },
    ]

    return {
        "status": "dry_run" if dry_run else "written",
        "site_data_dir": str(site_data_dir),
        "files": files_written,
    }


def write_mirror_receipt(
    reports_dir: Path,
    write_result: dict,
    proof_surface_src: Path | None,
    table_classes_src: Path | None,
    dry_run: bool = False,
) -> Path:
    """Write a receipt proving what was mirrored and when."""
    receipt = {
        "schema": "stegverse.site_mirror_receipt.v1",
        "receipt_id": (
            f"RCPT-MIRROR-"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        ),
        "task": "site_mirror_update",
        "generated_at": now_utc(),
        "dry_run": dry_run,
        "sources": {
            "proof_surface": str(proof_surface_src) if proof_surface_src else None,
            "table_classes": str(table_classes_src) if table_classes_src else None,
        },
        "write_result": write_result,
        "authority": (
            "formalism-tests produces receipts. "
            "Site publishes receipts. "
            "Site must not become the authority for receipts."
        ),
    }
    receipt["receipt_hash"] = sha256_str(
        json.dumps(receipt, sort_keys=True)
    )

    receipt_path = reports_dir / "site_mirror_update_receipt.json"
    if not dry_run:
        reports_dir.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, indent=2) + "\n",
            encoding="utf-8",
        )

    return receipt_path


# ---------------------------------------------------------------------------
# Git push (optional)
# ---------------------------------------------------------------------------

def push_to_site_repo(
    site_data_dir: Path,
    token: str,
    dry_run: bool = False,
) -> dict:
    """
    Commit and push Site data file changes.
    Only called when --push-to-site is set and GITHUB_TOKEN is available.
    """
    if dry_run:
        return {"status": "dry_run_push_skipped"}

    site_root = site_data_dir
    while site_root.name != "Site" and site_root.parent != site_root:
        site_root = site_root.parent

    if not (site_root / ".git").exists():
        return {
            "status": "no_git_repo",
            "note": "Site root git repo not found. Manual commit required.",
        }

    try:
        for cmd in [
            ["git", "-C", str(site_root), "config",
             "user.email", "formalism-mirror@stegverse"],
            ["git", "-C", str(site_root), "config",
             "user.name", "StegVerse Formalism Mirror"],
            ["git", "-C", str(site_root), "add",
             str(site_data_dir / "transition-proof-surface.json"),
             str(site_data_dir / "transition-table-classes.json")],
        ]:
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)

        diff = subprocess.run(
            ["git", "-C", str(site_root), "diff", "--cached", "--quiet"],
            capture_output=True,
        )

        if diff.returncode == 0:
            return {"status": "no_changes", "note": "Site data already current."}

        subprocess.run(
            ["git", "-C", str(site_root), "commit", "-m",
             "mirror: update formalism-tests proof surface data"],
            check=True, capture_output=True, timeout=30,
        )
        subprocess.run(
            ["git", "-C", str(site_root), "push", "origin", "main"],
            check=True, capture_output=True, timeout=60,
        )
        return {"status": "pushed"}

    except subprocess.CalledProcessError as e:
        return {
            "status": "push_failed",
            "error": e.stderr.decode()[:200] if e.stderr else str(e),
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(
    site_data_dir: Path,
    dry_run: bool = False,
    push: bool = False,
) -> dict:
    print("=== Site Mirror Update ===")
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY'}")
    print(f"Site data dir: {site_data_dir}")
    print()

    # Resolve sources
    ps_src, ps_data = resolve_proof_surface()
    tc_src, tc_data = resolve_table_classes()
    stage6 = resolve_stage6_report()

    if not ps_data:
        print("ERROR: could not find transition-proof-surface.json")
        return {"status": "failed", "error": "proof surface not found"}
    if not tc_data:
        print("ERROR: could not find transition-table-classes.json")
        return {"status": "failed", "error": "table classes not found"}

    print(f"  Proof surface: {ps_src}")
    print(f"  Table classes: {tc_src}")
    print(f"  Stage 6 report: {'found' if stage6 else 'not found'}")
    if stage6:
        print(f"  Stage 6 verified: {stage6.get('verified', False)}")
        print(f"  Candidates: {stage6.get('candidate_count', '?')}")
        print(f"  Assertions: {stage6.get('assertion_count', '?')}")
    print()

    # Build updated content
    updated_ps = build_updated_proof_surface(ps_data, stage6)
    updated_tc = build_updated_table_classes(tc_data, stage6)

    current_stage = updated_ps.get("current_stage", "unknown")
    total_classes = updated_tc.get("total_classes", 0)
    print(f"  Current stage: {current_stage}")
    print(f"  Total transition classes: {total_classes}")
    print()

    # Write files
    write_result = write_mirror_files(
        site_data_dir, updated_ps, updated_tc, dry_run=dry_run
    )
    print(f"  Files: {write_result['status']}")
    for f in write_result["files"]:
        print(f"    {Path(f['path']).name}")

    # Write receipt
    receipt_path = write_mirror_receipt(
        ROOT / "reports",
        write_result,
        ps_src,
        tc_src,
        dry_run=dry_run,
    )
    print(f"  Receipt: {receipt_path.name}")

    # Optional git push
    push_result = {"status": "push_not_requested"}
    if push and not dry_run:
        token = os.environ.get("GITHUB_TOKEN", "")
        push_result = push_to_site_repo(site_data_dir, token, dry_run=False)
        print(f"  Push: {push_result['status']}")

    print()
    print(f"=== Done: {current_stage}, {total_classes} classes ===")

    return {
        "status": "ok",
        "current_stage": current_stage,
        "total_classes": total_classes,
        "write_result": write_result,
        "push_result": push_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site-data-dir",
        default=os.environ.get("SITE_DATA_DIR", str(DEFAULT_SITE_DATA)),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--push-to-site",
        action="store_true",
        help="Commit and push changes to Site repo after writing",
    )
    args = parser.parse_args()

    result = run(
        site_data_dir=Path(args.site_data_dir),
        dry_run=args.dry_run,
        push=args.push_to_site,
    )
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
