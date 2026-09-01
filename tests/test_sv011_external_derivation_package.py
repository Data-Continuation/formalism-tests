from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_sv011_external_derivation_package.py"

BLOCKS = [
    "role_change_declared",
    "transition_class_declared",
    "authority_current",
    "evidence_fresh",
    "scope_valid",
    "trust_basis_current",
    "risk_basis_current",
    "receipt_required",
    "fail_closed_if_missing",
]


def make_package():
    ids = ["sv011-allow-001", "sv011-deny-001"]
    root = "sha256:" + hashlib.sha256("\n".join(ids).encode()).hexdigest()
    return {
        "schema": "stegverse.sv011-external-derivation-package/v0.1",
        "entity_id": "SV-011",
        "first_transition_element": {
            "element_id": "SV011-E0",
            "sha256": "sha256:" + "0" * 64,
        },
        "source_pins": [
            {"repository": "Admissible-Existence/TT", "path": "schemas/transition-element-fixture.schema.json", "commit": "1" * 40, "blob": "2" * 40},
            {"repository": "Data-Continuation/formalisms", "path": "docs/TRANSITION_ROLE_MODEL.md", "commit": "3" * 40, "blob": "4" * 40},
            {"repository": "Data-Continuation/formalisms", "path": "docs/CONTINUATION_DECISION_FUNCTION.md", "commit": "5" * 40, "blob": "6" * 40},
        ],
        "authority": {
            "execution_authorized": False,
            "publication_authorized": False,
            "proofs_accepted": False,
        },
        "cases": [
            {
                "case_id": "allow",
                "source_role": "context",
                "target_role": "evidence",
                "required_blocks": BLOCKS,
                "block_results": {k: "PASS" for k in BLOCKS},
                "decision": "ALLOW",
                "capability": "evidence_candidate",
                "receipt_id": ids[0],
            },
            {
                "case_id": "deny",
                "source_role": "instruction",
                "target_role": "command",
                "required_blocks": BLOCKS,
                "block_results": {**{k: "PASS" for k in BLOCKS}, "authority_current": "FAIL"},
                "decision": "DENY",
                "capability": "command_candidate",
                "receipt_id": ids[1],
            },
        ],
        "reconstruction": {"ordered_receipt_ids": ids, "ordered_root": root},
    }


def run_checker(package):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "package.json"
        path.write_text(json.dumps(package), encoding="utf-8")
        return subprocess.run([sys.executable, str(CHECKER), str(path)], capture_output=True, text=True)


def test_minimum_package_passes():
    result = run_checker(make_package())
    assert result.returncode == 0, result.stderr + result.stdout
    assert "PASS:" in result.stdout


def test_authority_expansion_fails():
    package = make_package()
    package["authority"]["execution_authorized"] = True
    result = run_checker(package)
    assert result.returncode != 0


def test_missing_denial_fails():
    package = make_package()
    package["cases"][1]["decision"] = "ALLOW"
    result = run_checker(package)
    assert result.returncode != 0


def test_block_set_drift_fails():
    package = make_package()
    package["cases"][0]["required_blocks"] = package["cases"][0]["required_blocks"][:-1]
    result = run_checker(package)
    assert result.returncode != 0


def main():
    test_minimum_package_passes()
    test_authority_expansion_fails()
    test_missing_denial_fails()
    test_block_set_drift_fails()
    print("SV011_EXTERNAL_DERIVATION_PACKAGE_PASS cases=4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
