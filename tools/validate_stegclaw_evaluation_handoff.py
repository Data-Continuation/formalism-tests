from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DECLARATION = ROOT / "formalism_tests" / "stegclaw_evaluation_handoff.json"
REPORTS = ROOT / "reports"

REQUIRED = [
    "standing_envelope.json",
    "standing_receipt.json",
    "ingestion_candidate.json",
    "ingestion_candidate_receipt.json",
    "outbound_envelope.json",
    "outbound_receipt.json",
    "live_integration_manifest.json",
]


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    data = json.loads(DECLARATION.read_text(encoding="utf-8"))
    missing = [name for name in REQUIRED if name not in data.get("required_artifacts", [])]
    rules = data.get("local_rules", {})
    errors = list(missing)
    if rules.get("proof_only") is not True:
        errors.append("proof_only")
    if rules.get("install_authority") is not False:
        errors.append("install_authority")
    if rules.get("production_authority") is not False:
        errors.append("production_authority")
    if rules.get("requires_declared_task") is not True:
        errors.append("requires_declared_task")
    report = {
        "schema": "formalism_tests.stegclaw_evaluation_handoff_report.v1",
        "target_repo": data.get("target_repo"),
        "upstream_repo": data.get("upstream_repo"),
        "role": data.get("role", []),
        "missing_required_artifacts": missing,
        "validation_errors": errors,
        "decision": "ALLOW" if not errors else "FAIL_CLOSED",
    }
    (REPORTS / "stegclaw_evaluation_handoff.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(report["decision"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
