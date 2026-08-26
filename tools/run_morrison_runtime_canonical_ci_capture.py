#!/usr/bin/env python3
"""Run and capture the Morrison Runtime canonical proof inside repository-owned GitHub Actions."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_MANIFEST = "tools/tasks/morrison_runtime_commit_time_scope_tasks.json"
REPORT = ROOT / "reports/morrison_runtime_commit_time_scope_report.json"
RECEIPTS = ROOT / "receipts/morrison_runtime_commit_time_scope_execution_receipts.jsonl"
VERIFICATION = ROOT / "reports/morrison_runtime_commit_time_scope_artifact_verification.json"
GATE = ROOT / "reports/morrison_runtime_canonical_evidence_gate.json"
EVIDENCE = ROOT / "receipts/morrison_runtime_canonical_execution_evidence.json"
EXPECTED = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_expected_outcomes.json"
BASELINE = ROOT / "tests/fixtures/morrison_runtime_commit_time_scope_artifact_baseline.json"
HANDOFF = ROOT / "MORRISON_RUNTIME_COMMIT_TIME_SCOPE_HANDOFF.md"
AUTHORITY = "EXTERNAL_FRAMEWORK_COMPARATIVE_EVIDENCE_ONLY"
TASKS = (
    "morrison_runtime_commit_time_scope_tests",
    "verify_morrison_runtime_commit_time_scope_artifacts",
    "check_morrison_runtime_canonical_evidence_gate",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(task_id: str) -> list[str]:
    return [
        sys.executable,
        "tools/run_declared_tasks.py",
        TASK_MANIFEST,
        "--task-id",
        task_id,
    ]


def command_text(task_id: str) -> str:
    return (
        "python tools/run_declared_tasks.py "
        f"{TASK_MANIFEST} --task-id {task_id}"
    )


def run_task(task_id: str) -> None:
    proc = subprocess.run(command(task_id), cwd=ROOT, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"Morrison canonical task failed: {task_id}")


def require_github_main() -> tuple[str, str]:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit("canonical capture requires GitHub Actions")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise SystemExit("canonical capture requires refs/heads/main")
    sha = os.environ.get("GITHUB_SHA", "")
    if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha):
        raise SystemExit("canonical capture requires a lowercase 40-character GITHUB_SHA")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if not run_id.isdigit():
        raise SystemExit("canonical capture requires numeric GITHUB_RUN_ID")
    return sha, run_id


def exact_expected_gate_bytes() -> bytes:
    payload = {
        "authority_posture": AUTHORITY,
        "errors": [],
        "mode": "CANONICAL_EVIDENCE_PRESENT",
        "promotion_eligible": True,
        "schema": "stegverse.morrison-runtime.canonical-evidence-gate-result.v1",
        "status": "PASS",
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def append_handoff_observation(commit_sha: str, run_id: str, hashes: dict[str, str]) -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    marker = "## Canonical GitHub Actions execution observed"
    block = f"""
{marker}

```text
status: VERIFIED_CANONICAL_RUN
commit_sha: {commit_sha}
execution_surface: GITHUB_ACTIONS
run_id: {run_id}
run_url: https://github.com/Data-Continuation/formalism-tests/actions/runs/{run_id}
task_results:
  morrison_runtime_commit_time_scope_tests: PASS
  verify_morrison_runtime_commit_time_scope_artifacts: PASS
  check_morrison_runtime_canonical_evidence_gate: PASS
report_sha256: {hashes['report_sha256']}
receipts_sha256: {hashes['receipts_sha256']}
verification_sha256: {hashes['verification_sha256']}
canonical_evidence_gate_sha256: {hashes['canonical_evidence_gate_sha256']}
report_equivalence: true
receipts_equivalence: true
expected_outcomes_equivalence: true
canonical_evidence_gate_equivalence: true
authority_posture: {AUTHORITY}
downstream_owner: StegVerse-Labs/admissibility-wiki#39
```

This is repository-owned canonical execution evidence for the bounded comparative proof package. It is not Morrison certification, endorsement, production validation, StegVerse execution authority, release authority, or downstream mutation authority. Downstream promotion remains separately gated by the admissibility-wiki canonical/public-route contracts.
"""
    if marker in text:
        text = text.split(marker, 1)[0].rstrip() + "\n" + block
    else:
        text = text.rstrip() + "\n" + block
    HANDOFF.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    commit_sha, run_id = require_github_main()

    committed_report = REPORT.read_bytes()
    committed_receipts = RECEIPTS.read_bytes()

    run_task(TASKS[0])
    if REPORT.read_bytes() != committed_report:
        raise SystemExit("generated Morrison report is not byte-equivalent to committed baseline output")
    if RECEIPTS.read_bytes() != committed_receipts:
        raise SystemExit("generated Morrison receipts are not byte-equivalent to committed baseline output")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "PASS" or report.get("authority_posture") != AUTHORITY:
        raise SystemExit("generated Morrison report did not preserve PASS/comparative-only posture")

    run_task(TASKS[1])
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    if verification.get("status") != "PASS" or verification.get("authority_posture") != AUTHORITY:
        raise SystemExit("Morrison artifact verification did not PASS")

    expected = json.loads(EXPECTED.read_text(encoding="utf-8")).get("expected", {})
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    expected_equivalent = expected == baseline.get("required_case_results")
    if not expected_equivalent:
        raise SystemExit("expected-outcome set diverges from committed artifact baseline")

    expected_gate = exact_expected_gate_bytes()
    gate_hash = hashlib.sha256(expected_gate).hexdigest()

    hashes = {
        "report_sha256": sha256(REPORT),
        "receipts_sha256": sha256(RECEIPTS),
        "verification_sha256": sha256(VERIFICATION),
        "canonical_evidence_gate_sha256": gate_hash,
    }
    run_url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'Data-Continuation/formalism-tests')}/actions/runs/{run_id}"
    evidence = {
        "schema": "stegverse.morrison-runtime.canonical-execution-evidence.v1",
        "suite_id": "morrison-runtime-commit-time-scope-v0.1",
        "repository": "Data-Continuation/formalism-tests",
        "commit_sha": commit_sha,
        "execution_surface": "GITHUB_ACTIONS",
        "run_url": run_url,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "commands": [command_text(task) for task in TASKS],
        "task_results": {task: "PASS" for task in TASKS},
        "artifact_hashes": hashes,
        "artifact_equivalence": {
            "report": True,
            "receipts": True,
            "expected_outcomes": True,
            "canonical_evidence_gate": True,
        },
        "authority_posture": AUTHORITY,
        "status": "VERIFIED_CANONICAL_RUN",
        "notes": [
            "Report and receipt outputs were byte-equivalent to their committed deterministic outputs before canonical capture.",
            "Expected-outcome mapping matched the committed artifact baseline.",
            "Canonical evidence-gate hash was pre-bound to the deterministic PASS gate output and verified after gate execution.",
            "This evidence grants no certification, endorsement, production-validation, release, or execution authority.",
        ],
    }
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    run_task(TASKS[2])
    actual_gate = GATE.read_bytes()
    if actual_gate != expected_gate:
        raise SystemExit("canonical gate output differs from the pre-bound deterministic PASS output")
    if sha256(GATE) != hashes["canonical_evidence_gate_sha256"]:
        raise SystemExit("canonical gate SHA-256 differs from canonical evidence binding")

    append_handoff_observation(commit_sha, run_id, hashes)
    print("MORRISON CANONICAL CI CAPTURE: PASS")
    print(f"commit_sha={commit_sha}")
    print(f"run_id={run_id}")
    for key, value in hashes.items():
        print(f"{key}={value}")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
