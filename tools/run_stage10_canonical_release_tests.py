#!/usr/bin/env python3
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

SPEC = Path("tests/fixtures/stage10_canonical_release_spec.json")
FIXTURES = Path("tests/fixtures/stage10_release_reports")
DIST = Path("dist/transition-table-v1-rc1")
REPORT = Path("reports/stage10_canonical_release_report.json")

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()

def load(path):
    if not path.exists():
        raise AssertionError(f"missing JSON file: {path}")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return data

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def resolve(entry):
    live = Path(entry["path"])
    if live.exists():
        return live
    fixture = FIXTURES / entry["fixture"]
    if fixture.exists():
        return fixture
    raise AssertionError(f"missing report: {live}")

def main():
    try:
        spec = load(SPEC)
        checks = 0
        checks += req(spec["release_id"] == "transition-table-v1-rc1", "bad release_id")
        checks += req(spec["canonical_status"] == "release_candidate", "bad status")
        checks += req(len(spec["canonical_elements"]) >= 13, "expected at least 13 canonical elements")
        checks += req(len(spec["coupling_classes"]) == 9, "expected 9 coupling classes")
        sources = []
        for entry in spec["required_reports"]:
            path = resolve(entry)
            data = load(path)
            sources.append(str(path))
            for key, expected in entry["required"].items():
                checks += req(data.get(key) == expected, f"{path}: expected {key}={expected!r}, got {data.get(key)!r}")
        release = {
            "schema": "stegverse_canonical_transition_table_release.v1",
            "release_id": spec["release_id"],
            "release_created_at": spec["release_created_at"],
            "release_stage": spec["release_stage"],
            "release_name": spec["release_name"],
            "canonical_status": spec["canonical_status"],
            "authority_boundary": spec["authority_boundary"],
            "prior_stages": spec["required_prior_stages"],
            "canonical_elements": spec["canonical_elements"],
            "coupling_classes": spec["coupling_classes"],
            "release_guards": spec["release_guards"],
            "report_sources": sources,
            "next_release_state": spec["next_release_state"]
        }
        release_hash = digest(release)
        replay = {"schema": "stegverse_transition_table_replay_packet.v1", "release_id": spec["release_id"], "release_hash": release_hash, "replay_mode": "reconstruct_only", "inputs": sources, "artifacts": spec["canonical_artifacts"], "authority_boundary": spec["authority_boundary"]}
        receipt = {"schema": "stegverse_canonical_transition_table_release_receipt.v1", "release_id": spec["release_id"], "release_hash": release_hash, "decision": "RELEASE_CANDIDATE", "basis": "Stage 6 through Stage 9 reports validated; canonical hash and replay packet emitted.", "authority_boundary": spec["authority_boundary"]}
        receipt["receipt_hash"] = digest(receipt)
        DIST.mkdir(parents=True, exist_ok=True)
        (DIST / "canonical_transition_table_release.json").write_text(json.dumps(release, indent=2, sort_keys=True) + "\n")
        (DIST / "canonical_transition_table_release.sha256").write_text(release_hash + "\n")
        (DIST / "replay_packet.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        (DIST / "release_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        checks += req(digest(load(DIST / "canonical_transition_table_release.json")) == release_hash, "release hash mismatch")
        report = {"schema": "stegverse_stage10_canonical_release_report.v1", "success": True, "generated_at": datetime.now(timezone.utc).isoformat(), "assertion_count": checks, "release_id": spec["release_id"], "release_hash": release_hash, "canonical_status": spec["canonical_status"], "canonical_element_count": len(spec["canonical_elements"]), "coupling_class_count": len(spec["coupling_classes"]), "report_sources": sources, "artifacts": spec["canonical_artifacts"], "next_release_state": spec["next_release_state"], "message": "Stage 10 canonical transition table release validation passed."}
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as e:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {"schema": "stegverse_stage10_canonical_release_report.v1", "success": False, "error": str(e)}
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
