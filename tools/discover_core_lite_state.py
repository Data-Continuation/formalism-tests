#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

REPORT_DIR = Path("reports")
RECEIPT_DIR = Path("receipts")
DISCOVERED = REPORT_DIR / "core_lite_discovered_state.json"
GAP_MD = REPORT_DIR / "core_lite_discovery_gap_report.md"
DIFF_JSON = REPORT_DIR / "core_lite_state_diff.json"
PLAN_JSON = REPORT_DIR / "core_lite_install_plan_candidate.json"
REPORT_JSON = REPORT_DIR / "core_lite_discovery_report.json"
RECEIPTS = RECEIPT_DIR / "core_lite_discovery_receipts.jsonl"
PROTECTED_PREFIXES = (".github/workflows/", "github/workflows/", "iosnoperiod/github/workflows/")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def digest(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def classify_path(path: str, required: set[str]) -> str:
    lower = path.lower()
    if path in required: return "present_and_valid"
    if any(lower.startswith(prefix) for prefix in PROTECTED_PREFIXES): return "extra_requires_review"
    if any(token in lower for token in ["secret", "token", "credential", ".env", "private_key"]): return "quarantine_required"
    if lower.endswith((".md", ".json", ".yml", ".yaml", ".py", ".html", ".css", ".js", ".txt")): return "local_extension"
    return "present_but_unknown"

def detect_capabilities(paths: set[str]) -> dict:
    return {
        "identity": any(p.endswith(".stegverse/core-lite.json") or p.endswith("stegverse/core-lite.json") for p in paths),
        "ingest_manifest": any(p.endswith(".stegverse/ingest_manifest.json") or p.endswith("stegverse/ingest_manifest.json") for p in paths),
        "cge": "core_lite/cge.py" in paths,
        "ingestion": "core_lite/ingest.py" in paths,
        "sandbox": "core_lite/sandbox.py" in paths,
        "receipts": "core_lite/receipts.py" in paths or "receipts/workstream_receipts.jsonl" in paths,
        "declared_tasks": "tools/tasks/core_lite_tasks.json" in paths,
        "schemas": any(p.startswith("schemas/") and p.endswith(".json") for p in paths),
        "reports": any(p.startswith("reports/") for p in paths),
        "workflows": any(p.startswith(".github/workflows/") or p.startswith("github/workflows/") for p in paths),
        "iosnoperiod": any(p.startswith("iosnoperiod/") for p in paths)
    }

def discover(root: Path) -> dict:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts: continue
        rel = path.relative_to(root).as_posix()
        try:
            files.append({"path": rel, "size": path.stat().st_size, "sha256": sha256_file(path)})
        except OSError:
            continue
    return {
        "schema": "stegverse_core_lite_discovered_state.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root.resolve()),
        "file_count": len(files),
        "files": files,
        "detected_capabilities": detect_capabilities({f["path"] for f in files})
    }

def main() -> int:
    root = Path(os.environ.get("CORE_LITE_ROOT", ".")).resolve()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    required = {
        ".stegverse/core-lite.json", ".stegverse/ingest_manifest.json", "core_lite/cge.py",
        "core_lite/ingest.py", "core_lite/sandbox.py", "core_lite/receipts.py",
        "tools/tasks/core_lite_tasks.json", "schemas/ingest_manifest.schema.json",
        "reports/workstream_status.json", "receipts/workstream_receipts.jsonl"
    }
    discovered = discover(root)
    paths = {f["path"] for f in discovered["files"]}
    diff_items = []
    for req_path in sorted(required):
        diff_items.append({"path": req_path, "classification": "present_and_valid" if req_path in paths else "missing_required", "required": True})
    for path in sorted(paths - required):
        diff_items.append({"path": path, "classification": classify_path(path, required), "required": False})
    counts = {}
    for item in diff_items:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    state_diff = {"schema": "stegverse_core_lite_state_diff.v1", "generated_at": datetime.now(timezone.utc).isoformat(), "classification_counts": counts, "items": diff_items}
    install_plan = {
        "schema": "stegverse_core_lite_install_plan_candidate.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": "core-lite",
        "install_allowed_by_plan": False,
        "sandbox_required": True,
        "cge_required": True,
        "receipts_required": True,
        "actions": [{"path": i["path"], "classification": i["classification"], "action": ("preserve" if i["classification"]=="present_and_valid" else "propose_candidate" if i["classification"]=="missing_required" else "quarantine_only" if i["classification"]=="quarantine_required" else "review_only")} for i in diff_items],
        "core_rule": "An install plan is a candidate transition, not installation authority."
    }
    DISCOVERED.write_text(json.dumps(discovered, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    DIFF_JSON.write_text(json.dumps(state_diff, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    PLAN_JSON.write_text(json.dumps(install_plan, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    gap = "# Core-Lite Discovery Gap Report\n\n## Core Rule\n\n```text\nDiscovery observes, models, compares, classifies, and proposes. Discovery does not install.\n```\n\n## Classification Counts\n\n"
    for k,v in sorted(counts.items()): gap += f"- `{k}`: {v}\n"
    gap += "\n## Missing Required\n\n"
    missing = [i for i in diff_items if i["classification"] == "missing_required"]
    gap += "".join(f"- `{i['path']}`\n" for i in missing) if missing else "No required paths are missing.\n"
    GAP_MD.write_text(gap, encoding="utf-8")
    receipt = {
        "schema": "stegverse_core_lite_discovery_receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision": "ALLOW_DISCOVERY_REPORT",
        "basis": "Discovery observed and classified current core-lite state without installation.",
        "discovered_state_sha256": sha256_file(DISCOVERED),
        "state_diff_sha256": sha256_file(DIFF_JSON),
        "install_plan_sha256": sha256_file(PLAN_JSON),
        "install_allowed_by_plan": False
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPTS.write_text(json.dumps(receipt, sort_keys=True)+"\n", encoding="utf-8")
    report = {"schema": "stegverse_core_lite_discovery_report.v1", "generated_at": datetime.now(timezone.utc).isoformat(), "success": True, "root": str(root), "file_count": discovered["file_count"], "classification_counts": counts, "outputs": {"discovered_state": str(DISCOVERED), "gap_report": str(GAP_MD), "state_diff": str(DIFF_JSON), "install_plan_candidate": str(PLAN_JSON), "receipts": str(RECEIPTS)}}
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0
if __name__ == "__main__": raise SystemExit(main())
