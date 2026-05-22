#!/usr/bin/env python3
from __future__ import annotations
import hashlib, io, json, tarfile
from datetime import datetime, timezone
from pathlib import Path

DIST, REPORTS, RECEIPTS = Path("dist"), Path("reports"), Path("receipts")
PACKET = DIST / "production-candidate-review-packet.tar.gz"
SHA = DIST / "production-candidate-review-packet.sha256"
MANIFEST = DIST / "production-candidate-review-packet.manifest.json"
REPORT = REPORTS / "production_candidate_review_report.md"
RECEIPTS_OUT = RECEIPTS / "production_candidate_review_receipts.jsonl"

def sha256_file(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def add_bytes(tar, arcname, data):
    info = tarfile.TarInfo(arcname); info.size = len(data); info.mode = 0o644; info.mtime = 0; tar.addfile(info, io.BytesIO(data))
def read_optional(path):
    p = Path(path)
    return p.read_bytes() if p.exists() else (json.dumps({"missing": path}, indent=2)+"\n").encode()
def main():
    DIST.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True); RECEIPTS.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    manifest = {"schema":"stegverse_production_candidate_review_packet_manifest.v1","generated_at":now,"packet_type":"production_candidate_review","target":"core-lite","install_authority":False,"production_authority":False,"requires_review":True,"requires_sandbox":True,"requires_cge":True,"requires_ingestion":True,"requires_master_record_export":True,"core_rule":"Production means accredited participation, not sovereign authority."}
    with tarfile.open(PACKET, "w:gz") as tar:
        add_bytes(tar, "manifest/production_candidate_manifest.json", (json.dumps(manifest, indent=2, sort_keys=True)+"\n").encode())
        for src, arc in [
            ("reports/core_lite_discovered_state.json","reports/core_lite_discovered_state.json"),
            ("reports/core_lite_state_diff.json","reports/core_lite_state_diff.json"),
            ("reports/core_lite_install_plan_candidate.json","reports/core_lite_install_plan_candidate.json"),
            ("reports/core_lite_discovery_gap_report.md","reports/core_lite_discovery_gap_report.md"),
            ("receipts/core_lite_discovery_receipts.jsonl","receipts/core_lite_discovery_receipts.jsonl"),
            ("THEOREM_PROOF_MAP.md","docs/THEOREM_PROOF_MAP.md"),
            ("docs/TASK_ID_INDEX.md","docs/TASK_ID_INDEX.md"),
            ("docs/ARTIFACT_INDEX.md","docs/ARTIFACT_INDEX.md"),
        ]: add_bytes(tar, arc, read_optional(src))
    packet_hash = sha256_file(PACKET)
    SHA.write_text(packet_hash+"  production-candidate-review-packet.tar.gz\n")
    manifest["packet_sha256"] = packet_hash
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n")
    REPORT.write_text("# Production Candidate Review Packet\n\nA non-installing production-candidate review packet has been generated.\n\n```text\nProduction means accredited participation, not sovereign authority.\nThe packet is portable evidence of a proposed governed transition, not installation authority.\n```\n\n## Packet SHA256\n\n```text\n"+packet_hash+"\n```\n")
    receipt = {"schema":"stegverse_production_candidate_review_receipt.v1","generated_at":now,"decision":"ALLOW_PRODUCTION_CANDIDATE_REVIEW_PACKET","basis":"Packet is non-installing review evidence and does not grant production authority.","packet_sha256":packet_hash,"production_authority":False,"install_authority":False}
    receipt["receipt_hash"] = digest(receipt)
    RECEIPTS_OUT.write_text(json.dumps(receipt, sort_keys=True)+"\n")
    print(json.dumps({"success": True, "packet": str(PACKET), "sha256": packet_hash}, indent=2))
    return 0
if __name__ == "__main__": raise SystemExit(main())
