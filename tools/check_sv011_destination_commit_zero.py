#!/usr/bin/env python3
from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_sv011_commit_zero.py"

IGNORED_TOP_LEVEL = {".git"}

def file_set(root: Path) -> set[str]:
    out = set()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if rel.split("/", 1)[0] in IGNORED_TOP_LEVEL:
            continue
        out.add(rel)
    return out

def main(target_dir: str) -> int:
    target = Path(target_dir)
    if not target.is_dir():
        raise SystemExit("FAIL: target directory does not exist")

    with tempfile.TemporaryDirectory() as d:
        expected = Path(d) / "expected"
        r = subprocess.run([sys.executable, str(BUILDER), str(expected)], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit("FAIL: could not generate expected commit-zero tree\n" + r.stdout + r.stderr)

        expected_files = file_set(expected)
        target_files = file_set(target)

        missing = sorted(expected_files - target_files)
        extra = sorted(target_files - expected_files)
        changed = []
        for rel in sorted(expected_files & target_files):
            if not filecmp.cmp(expected / rel, target / rel, shallow=False):
                changed.append(rel)

        if missing or extra or changed:
            raise SystemExit(
                "FAIL: destination commit-zero drift "
                + f"missing={missing} extra={extra} changed={changed}"
            )

    print("PASS: SV-011 destination checkout exactly matches validated commit-zero tree")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_sv011_destination_commit_zero.py <checkout-dir>")
    raise SystemExit(main(sys.argv[1]))
