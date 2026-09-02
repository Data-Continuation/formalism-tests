from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "build_sv011_commit_zero.py"
CHECKER = ROOT / "tools" / "check_sv011_destination_commit_zero.py"

def run_checker(path: Path):
    return subprocess.run([sys.executable, str(CHECKER), str(path)], capture_output=True, text=True)

def main():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        good = root / "good"
        b = subprocess.run([sys.executable, str(BUILDER), str(good)], capture_output=True, text=True)
        assert b.returncode == 0, b.stdout + b.stderr

        ok = run_checker(good)
        assert ok.returncode == 0, ok.stdout + ok.stderr

        changed = root / "changed"
        subprocess.run([sys.executable, str(BUILDER), str(changed)], check=True, capture_output=True, text=True)
        p = changed / "authority" / "initial-boundary.json"
        p.write_text(p.read_text() + "\n")
        assert run_checker(changed).returncode != 0

        extra = root / "extra"
        subprocess.run([sys.executable, str(BUILDER), str(extra)], check=True, capture_output=True, text=True)
        (extra / "unexpected.txt").write_text("not allowed\n")
        assert run_checker(extra).returncode != 0

        missing = root / "missing"
        subprocess.run([sys.executable, str(BUILDER), str(missing)], check=True, capture_output=True, text=True)
        (missing / "README.md").unlink()
        assert run_checker(missing).returncode != 0

        print("SV011_DESTINATION_COMMIT_ZERO_VERIFIER_PASS cases=4")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
