#!/usr/bin/env python3
"""
Generic declared-task runner for StegVerse / Data-Continuation repos.

The workflow should stay generic. Task intent belongs in JSON manifests under
tools/tasks/.

Usage:
    python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json
    python tools/run_declared_tasks.py tools/tasks/formalism_tests_tasks.json --task-id boundary_dynamics_evaluation
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPORT_PATH = Path("declared_task_report.json")


def load_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"task manifest not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict):
        raise ValueError("task manifest must be a JSON object")

    tasks = payload.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("task manifest must contain a tasks list")

    return payload


def validate_task(task: Dict[str, Any]) -> None:
    task_id = task.get("task_id")
    if not isinstance(task_id, str) or not task_id.strip():
        raise ValueError("each task must define a non-empty task_id")

    command = task.get("command")
    if not isinstance(command, list) or not command:
        raise ValueError(f"task {task_id} must define a non-empty command list")

    for item in command:
        if not isinstance(item, str) or not item:
            raise ValueError(f"task {task_id} command entries must be non-empty strings")

    expected_outputs = task.get("expected_outputs", [])
    if not isinstance(expected_outputs, list):
        raise ValueError(f"task {task_id} expected_outputs must be a list")

    for output in expected_outputs:
        if not isinstance(output, str) or not output:
            raise ValueError(f"task {task_id} expected output entries must be non-empty strings")


def select_tasks(manifest: Dict[str, Any], task_id: Optional[str]) -> List[Dict[str, Any]]:
    tasks = manifest["tasks"]

    if task_id:
        selected = [task for task in tasks if task.get("task_id") == task_id]
        if not selected:
            raise ValueError(f"task_id not found in manifest: {task_id}")
        return selected

    return [task for task in tasks if task.get("enabled", True) is True]


def run_task(task: Dict[str, Any]) -> Dict[str, Any]:
    validate_task(task)

    task_id = task["task_id"]
    command = task["command"]
    expected_outputs = task.get("expected_outputs", [])

    started_at = datetime.now(timezone.utc).isoformat()

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    finished_at = datetime.now(timezone.utc).isoformat()

    output_status = {
        output: Path(output).exists()
        for output in expected_outputs
    }

    success = completed.returncode == 0 and all(output_status.values())

    return {
        "task_id": task_id,
        "description": task.get("description", ""),
        "command": command,
        "started_at": started_at,
        "finished_at": finished_at,
        "returncode": completed.returncode,
        "success": success,
        "expected_outputs": output_status,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def write_report(manifest_path: Path, manifest: Dict[str, Any], results: List[Dict[str, Any]]) -> None:
    report = {
        "runner": "tools/run_declared_tasks.py",
        "manifest_path": str(manifest_path),
        "manifest_name": manifest.get("name", ""),
        "manifest_version": manifest.get("version", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_count": len(results),
        "success": all(result["success"] for result in results),
        "results": results,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run declared tasks from a JSON manifest.")
    parser.add_argument("manifest", help="Path to task manifest JSON.")
    parser.add_argument("--task-id", default=None, help="Optional task_id to run.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    tasks = select_tasks(manifest, args.task_id)

    if not tasks:
        raise ValueError("no enabled tasks selected")

    results = [run_task(task) for task in tasks]
    write_report(manifest_path, manifest, results)

    if all(result["success"] for result in results):
        return 0

    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        error_report = {
            "runner": "tools/run_declared_tasks.py",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "error": str(exc),
        }
        REPORT_PATH.write_text(json.dumps(error_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(error_report, indent=2, sort_keys=True), file=sys.stderr)
        raise SystemExit(1)
