from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_sv011_portable_reduction_objective.py"

TEST_IDS = [
    "admitted_capability",
    "denied_capability",
    "stale_or_unknown_basis",
    "stopped_chain",
    "replay_no_authority",
    "ordered_reconstruction",
]

def make_objective():
    return {
        "schema": "stegverse.sv011-portable-reduction-objective/v0.1",
        "entity_id": "SV-011",
        "package_class": "bootstrap_minimal",
        "artifact": {
            "filename": "sv011-min.tar.gz",
            "format": "tar.gz",
            "sha256": "sha256:" + "a" * 64,
            "compressed_bytes": 4096,
            "file_count": 12,
            "dependency_count": 1,
        },
        "installation": {
            "fresh_destination": True,
            "network_required": True,
            "steps": ["extract", "verify", "install", "self-test"],
            "result": "PASS",
        },
        "self_tests": [
            {"test_id": tid, "result": "PASS", "receipt_id": "receipt-" + tid}
            for tid in TEST_IDS
        ],
        "ablation": {
            "method": "remove_rebuild_reinstall_retest",
            "irreducible_components": [
                {
                    "component": "commit_gate",
                    "removal_breaks_invariant": True,
                    "failed_test_ids": ["denied_capability", "stopped_chain"],
                    "evidence_receipt_id": "receipt-ablation-commit-gate",
                }
            ],
        },
        "authority": {
            "package_installation_is_runtime_authority": False,
            "workflow_pass_is_runtime_authority": False,
        },
    }

def run_checker(obj):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "objective.json"
        path.write_text(json.dumps(obj), encoding="utf-8")
        return subprocess.run([sys.executable, str(CHECKER), str(path)], capture_output=True, text=True)

def test_valid_objective_passes():
    r = run_checker(make_objective())
    assert r.returncode == 0, r.stderr + r.stdout

def test_missing_canonical_test_fails():
    x = make_objective()
    x["self_tests"] = x["self_tests"][:-1]
    assert run_checker(x).returncode != 0

def test_offline_network_dependency_fails():
    x = make_objective()
    x["package_class"] = "offline_self_contained"
    x["installation"]["network_required"] = True
    assert run_checker(x).returncode != 0

def test_ablation_without_breakage_fails():
    x = make_objective()
    x["ablation"]["irreducible_components"][0]["removal_breaks_invariant"] = False
    assert run_checker(x).returncode != 0

def test_authority_conflation_fails():
    x = make_objective()
    x["authority"]["workflow_pass_is_runtime_authority"] = True
    assert run_checker(x).returncode != 0

def main():
    test_valid_objective_passes()
    test_missing_canonical_test_fails()
    test_offline_network_dependency_fails()
    test_ablation_without_breakage_fails()
    test_authority_conflation_fails()
    print("SV011_PORTABLE_REDUCTION_OBJECTIVE_PASS cases=5")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
