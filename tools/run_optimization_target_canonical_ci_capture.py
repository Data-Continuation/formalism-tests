#!/usr/bin/env python3
"""Run and capture optimization-target canonical proof inside repository-owned GitHub Actions."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_MANIFEST = "tools/tasks/optimization_target_commit_boundary_tasks.json"
REPORT = ROOT / "reports/optimization_target_commit_boundary_report.json"
RECEIPTS = ROOT / "receipts/optimization_target_commit_boundary_execution_receipts.jsonl"
VERIFICATION = ROOT / "reports/optimization_target_commit_boundary_artifact_verification.json"
GATE = ROOT / "reports/optimization_target_canonical_evidence_gate.json"
EVIDENCE = ROOT / "receipts/optimization_target_canonical_execution_evidence.json"
EXPECTED = ROOT / "tests/fixtures/optimization_target_commit_boundary_expected_outcomes.json"
BASELINE = ROOT / "tests/fixtures/optimization_target_commit_boundary_artifact_baseline.json"
CHECKER = ROOT / "tools/check_optimization_target_canonical_evidence_gate.py"
HANDOFF = ROOT / "docs/formalisms/OPTIMIZATION_TARGET_COMMIT_BOUNDARY_MIRROR_HANDOFF.md"
AUTHORITY = "FORMALISM_TEST_EVIDENCE_ONLY"
TASKS = (
    "optimization_target_commit_boundary_tests",
    "verify_optimization_target_commit_boundary_artifacts",
    "check_optimization_target_canonical_evidence_gate",
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
    return f"python tools/run_declared_tasks.py {TASK_MANIFEST} --task-id {task_id}"


def run_task(task_id: str) -> None:
    proc = subprocess.run(command(task_id), cwd=ROOT, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"optimization-target canonical task failed: {task_id}")


def require_github_main() -> tuple[str, str]:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise SystemExit("canonical capture requires GitHub Actions")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise SystemExit("canonical capture requires refs/heads/main")
    commit_sha = os.environ.get("GITHUB_SHA", "")
    if len(commit_sha) != 40 or any(ch not in "0123456789abcdef" for ch in commit_sha):
        raise SystemExit("canonical capture requires a lowercase 40-character GITHUB_SHA")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if not run_id.isdigit():
        raise SystemExit("canonical capture requires numeric GITHUB_RUN_ID")
    return commit_sha, run_id


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
  optimization_target_commit_boundary_tests: PASS
  verify_optimization_target_commit_boundary_artifacts: PASS
  check_optimization_target_canonical_evidence_gate: PASS
report_sha256: {hashes['report_sha256']}
receipts_sha256: {hashes['receipts_sha256']}
artifact_verification_sha256: {hashes['artifact_verification_sha256']}
canonical_evidence_gate_sha256: {hashes['canonical_evidence_gate_sha256']}
report_equivalence: true
receipts_equivalence: true
expected_outcomes_equivalence: true
canonical_evidence_gate_equivalence: true
authority_posture: {AUTHORITY}
downstream_owner: StegVerse-Labs/admissibility-wiki
```

This is repository-owned canonical execution evidence for the optimization-target commit-boundary proof package. It establishes deterministic proof evidence only. It does not establish that an optimization target is objectively correct, nor grant installation, production, publication, financial, sovereign, certification, release, execution, or downstream mutation authority.
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
        raise SystemExit("generated optimization-target report is not byte-equivalent to committed baseline output")
    if RECEIPTS.read_bytes() != committed_receipts:
        raise SystemExit("generated optimization-target receipts are not byte-equivalent to committed baseline output")

    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if report.get("status") != "PASS" or report.get("authority_posture") != AUTHORITY:
        raise SystemExit("generated optimization-target report did not preserve PASS/evidence-only posture")

    run_task(TASKS[1])
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    if verification.get("status") != "PASS" or verification.get("authority_posture") != AUTHORITY:
        raise SystemExit("optimization-target artifact verification did not PASS")

    expected = json.loads(EXPECTED.read_text(encoding="utf-8")).get("expected", {})
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    if expected != baseline.get("required_case_results"):
        raise SystemExit("expected-outcome set diverges from committed optimization-target artifact baseline")

    hashes = {
        "report_sha256": sha256(REPORT),
        "receipts_sha256": sha256(RECEIPTS),
        "artifact_verification_sha256": sha256(VERIFICATION),
        "canonical_evidence_gate_sha256": sha256(CHECKER),
    }
    run_url = f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'Data-Continuation/formalism-tests')}/actions/runs/{run_id}"
    evidence = {
        "schema": "stegverse.optimization-target.canonical-execution-evidence.v1",
        "suite_id": "optimization-target-commit-boundary-v0.1",
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
            "The canonical evidence-gate SHA-256 binds the committed checker source, avoiding self-referential gate-output hashing.",
            "This proof grants no installation, production, publication, financial, sovereign, certification, release, or execution authority.",
        ],
    }
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    run_task(TASKS[2])
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    if gate.get("status") != "PASS" or gate.get("promotion_eligible") is not True:
        raise SystemExit("optimization-target canonical evidence gate did not PASS")
    if gate.get("canonical_evidence_gate_sha256") != hashes["canonical_evidence_gate_sha256"]:
        raise SystemExit("optimization-target gate checker digest differs from canonical evidence binding")

    append_handoff_observation(commit_sha, run_id, hashes)
    print("OPTIMIZATION TARGET CANONICAL CI CAPTURE: PASS")
    print(f"commit_sha={commit_sha}")
    print(f"run_id={run_id}")
    for key, value in hashes.items():
        print(f"{key}={value}")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
