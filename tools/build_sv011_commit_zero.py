#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT / "data" / "sv011_canonical_source_pins.json"

FILES = {
    "SV_011_ENTITY_MIRROR_HANDOFF.md": """# SV-011 Entity Mirror Handoff

## State
PHASE-0 / COMMIT-ZERO CONSTRUCTION

## Authority
execution_authorized: false
publication_authorized: false
proofs_accepted: false

## Construction rule
This repository begins from one declared transition element. No execution path, boundary runtime, inference service, transport runtime, or autonomous worker is installed at commit zero.

## Next allowed work
1. validate E0 and its hash
2. validate external entity-slot binding
3. emit first transition-ledger receipt
4. prove no execution path exists
5. only then enter standing-surface construction

## Prohibited inference
Source presence, CI, merge, installation, or receipt emission does not imply runtime activation or autonomous status.
""",
    "README.md": """# SV-011

SV-011 is the from-scratch governed-entity construction experiment.

Commit zero establishes origin, immutable source bindings, an authority-false boundary, and a transition ledger. It intentionally contains no consequence execution path.
""",
    "construction/first-transition-element.json": json.dumps({
        "fixture_id": "SV011-E0-FIXTURE",
        "transition_id": "T-011",
        "transition_name": "sv011_construction_origin",
        "purpose": "Declare the first transition element from which SV-011 capability derivation will be tested.",
        "input": {
            "entity_id": "SV-011",
            "source_role": "context",
            "target_role": "context",
            "authority_effect": "NONE"
        },
        "expected": {
            "decision": "PENDING",
            "implementation_status": "implemented"
        }
    }, indent=2) + "\n",
    "construction/entity-instantiation.json": json.dumps({
        "schema": "stegverse.sv011-entity-instantiation/v0.1",
        "entity_id": "SV-011",
        "canonical_repo": "SV-011/entity",
        "external_registration": "Data-Continuation/core-lite:entity-architecture.json#sequence_id=011",
        "status": "phase0_declared_not_active",
        "execution_authorized": False,
        "publication_authorized": False,
        "proofs_accepted": False
    }, indent=2) + "\n",
    "construction/entity-charter-binding.json": json.dumps({
        "schema": "stegverse.sv011-entity-charter-binding/v0.1",
        "entity_id": "SV-011",
        "inherits_stage25_charter": True,
        "stage25_pin_id": "stage25_entity_charter_runner",
        "creates_parallel_charter": False,
        "authority_effect": "NONE"
    }, indent=2) + "\n",
    "authority/initial-boundary.json": json.dumps({
        "schema": "stegverse.sv011-authority-boundary/v0.1",
        "entity_id": "SV-011",
        "execution_authorized": False,
        "publication_authorized": False,
        "proofs_accepted": False,
        "runtime_installed": False,
        "boundary_runtime_installed": False,
        "autonomous_status_claimed": False,
        "consequence_path_reachable": False
    }, indent=2) + "\n",
    ".stegverse/transition-ledger/contract.json": json.dumps({
        "schema": "stegverse.transition-ledger.contract/v0.1",
        "entity_id": "SV-011",
        "append_only": True,
        "hash_algorithm": "sha256",
        "receipt_required_for_every_transition": True,
        "authority_effect": "NONE"
    }, indent=2) + "\n",
    ".stegverse/transition-ledger/emit.py": """#!/usr/bin/env python3
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: emit.py <event.json> <receipt.json>")
    event = json.loads(Path(sys.argv[1]).read_text())
    receipt = {
        "schema": "stegverse.transition-ledger.receipt/v0.1",
        "entity_id": "SV-011",
        "event_sha256": "sha256:" + hashlib.sha256(canonical(event)).hexdigest(),
        "execution_authorized": False,
        "publication_authorized": False,
        "proofs_accepted": False,
        "emitted_at": datetime.now(timezone.utc).isoformat()
    }
    Path(sys.argv[2]).write_text(json.dumps(receipt, indent=2) + "\n")
if __name__ == "__main__":
    main()
"""
}

def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()

def main(outdir: str):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    pins = json.loads(PINS.read_text())
    (out / "construction").mkdir(exist_ok=True)
    (out / "authority").mkdir(exist_ok=True)
    (out / ".stegverse" / "transition-ledger").mkdir(parents=True, exist_ok=True)
    for rel, content in FILES.items():
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    (out / "construction" / "canonical-source-pins.json").write_text(json.dumps(pins, indent=2) + "\n", encoding="utf-8")
    e0 = (out / "construction" / "first-transition-element.json").read_bytes()
    manifest = {
        "schema": "stegverse.sv011-commit-zero-manifest/v0.1",
        "entity_id": "SV-011",
        "phase": "PHASE-0",
        "first_transition_element_sha256": sha256_bytes(e0),
        "authority": {
            "execution_authorized": False,
            "publication_authorized": False,
            "proofs_accepted": False
        },
        "no_execution_path": True,
        "file_count": sum(1 for p in out.rglob("*") if p.is_file())
    }
    (out / "construction" / "commit-zero-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, sort_keys=True))
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: build_sv011_commit_zero.py <outdir>")
    raise SystemExit(main(sys.argv[1]))
