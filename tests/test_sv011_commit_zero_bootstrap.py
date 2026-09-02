from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/"tools"/"build_sv011_commit_zero.py"

def main():
    with tempfile.TemporaryDirectory() as d:
        out=Path(d)/"entity"
        r=subprocess.run([sys.executable,str(BUILD),str(out)],capture_output=True,text=True)
        assert r.returncode==0, r.stdout+r.stderr
        required=[
            "SV_011_ENTITY_MIRROR_HANDOFF.md",
            "README.md",
            "construction/first-transition-element.json",
            "construction/entity-instantiation.json",
            "construction/entity-charter-binding.json",
            "construction/canonical-source-pins.json",
            "construction/commit-zero-manifest.json",
            "authority/initial-boundary.json",
            ".stegverse/transition-ledger/contract.json",
            ".stegverse/transition-ledger/emit.py",
        ]
        for rel in required: assert (out/rel).is_file(), rel
        auth=json.loads((out/"authority/initial-boundary.json").read_text())
        assert auth["execution_authorized"] is False
        assert auth["publication_authorized"] is False
        assert auth["proofs_accepted"] is False
        assert auth["runtime_installed"] is False
        assert auth["boundary_runtime_installed"] is False
        assert auth["consequence_path_reachable"] is False
        manifest=json.loads((out/"construction/commit-zero-manifest.json").read_text())
        assert manifest["no_execution_path"] is True
        pins=json.loads((out/"construction/canonical-source-pins.json").read_text())
        assert pins["entity_id"]=="SV-011"
        assert len(pins["pins"])==9
        py=list(out.rglob("*.py"))
        assert [p.relative_to(out).as_posix() for p in py]==[".stegverse/transition-ledger/emit.py"]
        print("SV011_COMMIT_ZERO_BOOTSTRAP_PASS files="+str(manifest["file_count"]))
    return 0
if __name__=="__main__": raise SystemExit(main())
