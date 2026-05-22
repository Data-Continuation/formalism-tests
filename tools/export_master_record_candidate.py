#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

DIST, REPORTS, RECEIPTS = Path("dist"), Path("reports"), Path("receipts")
EXPORT = DIST / "master-record-export.json"
REPORT = REPORTS / "master_record_export_report.json"
RECEIPT = RECEIPTS / "master_record_export_receipts.jsonl"

def sha256_file(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def digest(obj): return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def artifact(path, kind): return {"path": path, "kind": kind, "exists": Path(path).exists(), "sha256": sha256_file(path)}
def main():
    DIST.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True); RECEIPTS.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    artifacts = [
        artifact("THEOREM_PROOF_MAP.md","proof_map"), artifact("docs/TASK_ID_INDEX.md","task_index"),
        artifact("docs/ARTIFACT_INDEX.md","artifact_index"), artifact("reports/core_lite_discovered_state.json","discovery_state"),
        artifact("reports/core_lite_state_diff.json","state_diff"), artifact("reports/core_lite_install_plan_candidate.json","install_plan_candidate"),
        artifact("dist/production-candidate-review-packet.tar.gz","production_candidate_review_packet"),
        artifact("dist/production-candidate-review-packet.sha256","packet_hash")
    ]
    export = {"schema":"stegverse_master_record_export.v1","generated_at":now,"source_repository":"formalism-tests","target_system":"master-records","export_type":"post_stage31_integration_candidate","production_authority":False,"install_authority":False,"core_rule":"Production means accredited participation, not sovereign authority.","artifacts":artifacts}
    export["export_hash"] = digest(export)
    EXPORT.write_text(json.dumps(export, indent=2, sort_keys=True)+"\n")
    report = {"schema":"stegverse_master_record_export_report.v1","generated_at":now,"success":True,"export":str(EXPORT),"export_hash":export["export_hash"],"artifact_count":len(artifacts),"missing_artifacts":[a["path"] for a in artifacts if not a["exists"]]}
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    receipt = {"schema":"stegverse_master_record_export_receipt.v1","generated_at":now,"decision":"ALLOW_MASTER_RECORD_EXPORT_CANDIDATE","basis":"Export records post-Stage-31 integration evidence without production or install authority.","export_hash":export["export_hash"]}
    receipt["receipt_hash"] = digest(receipt)
    RECEIPT.write_text(json.dumps(receipt, sort_keys=True)+"\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
