#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_DIR = Path("reports/current/stegverse-001-remote-core-lite")
RECEIPT_DIR = Path("receipts/current/stegverse-001-remote-core-lite")
REPORT_JSON = REPORT_DIR / "working_contract_report.json"
REPORT_MD = REPORT_DIR / "working_contract_report.md"
PLAN_JSON = REPORT_DIR / "remediation_plan.json"
RECEIPTS = RECEIPT_DIR / "receipts.jsonl"

DEFAULT_REPO = "Data-Continuation/core-lite"
DEFAULT_BRANCH = "main"
DEFAULT_WORK_DIR = Path(tempfile.gettempdir()) / "stegverse-001-remote-core-lite"


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_dict(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class ReceiptChain:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.previous_hash = self._last_hash()

    def _last_hash(self) -> str | None:
        if not self.path.exists():
            return None
        last = None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                last = json.loads(line).get("receipt_hash")
            except json.JSONDecodeError:
                continue
        return last

    def record(self, event_type: str, decision: str, basis: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        receipt = {
            "schema": "stegverse_001_remote_operator_receipt.v2",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "actor": "StegVerse-001",
            "event_type": event_type,
            "decision": decision,
            "basis": basis,
            "previous_receipt_hash": self.previous_hash,
            "metadata": metadata or {},
        }
        receipt["receipt_hash"] = hash_dict(receipt)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(receipt) + "\n")
        self.previous_hash = receipt["receipt_hash"]
        return receipt


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def parse_python(path: Path, repo_root: Path) -> dict[str, Any]:
    rel = path.relative_to(repo_root).as_posix() if path.exists() and repo_root in path.parents else path.as_posix()
    text = read_text(path)
    contract: dict[str, Any] = {
        "path": rel,
        "exists": path.exists() and path.is_file(),
        "sha256": sha256_file(path),
        "functions": [],
        "classes": [],
        "import_from": [],
        "imports": [],
        "parse_error": None,
    }

    if not text:
        return contract

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        contract["parse_error"] = f"{exc.__class__.__name__}: {exc}"
        return contract

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            contract["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            contract["classes"].append(node.name)
        elif isinstance(node, ast.ImportFrom):
            contract["import_from"].append({
                "module": node.module or "",
                "level": node.level,
                "names": [alias.name for alias in node.names],
            })
        elif isinstance(node, ast.Import):
            contract["imports"].extend(alias.name for alias in node.names)

    contract["functions"] = sorted(set(contract["functions"]))
    contract["classes"] = sorted(set(contract["classes"]))
    contract["imports"] = sorted(set(contract["imports"]))
    return contract


def import_targets_cge(import_item: dict[str, Any]) -> bool:
    module = import_item.get("module", "")
    level = int(import_item.get("level", 0) or 0)

    return (
        module == "core_lite.cge"
        or module == "cge"
        or (level == 1 and module == "cge")
    )


def inspect_workflows(repo_root: Path) -> list[dict[str, Any]]:
    workflow_dir = repo_root / ".github" / "workflows"
    if not workflow_dir.exists():
        return []

    workflows: list[dict[str, Any]] = []
    for path in sorted(workflow_dir.glob("*")):
        if not path.is_file():
            continue
        text = read_text(path)
        workflows.append({
            "path": path.relative_to(repo_root).as_posix(),
            "sha256": sha256_file(path),
            "mentions_incoming": "incoming" in text,
            "mentions_intake": "intake" in text.lower(),
            "mentions_cge": "cge" in text.lower(),
            "mentions_cli": "cli" in text.lower(),
            "mentions_reports_current": "reports/current" in text,
            "python_commands": re.findall(r"python[^\n]+", text),
            "workflow_dispatch": "workflow_dispatch" in text,
        })
    return workflows


def inspect_task_manifests(repo_root: Path) -> list[dict[str, Any]]:
    task_dir = repo_root / "tools" / "tasks"
    if not task_dir.exists():
        return []

    manifests: list[dict[str, Any]] = []
    for path in sorted(task_dir.glob("*.json")):
        entry: dict[str, Any] = {
            "path": path.relative_to(repo_root).as_posix(),
            "sha256": sha256_file(path),
            "task_ids": [],
            "commands": [],
            "parse_error": None,
        }
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for task in data.get("tasks", []):
                if isinstance(task, dict):
                    if task.get("task_id"):
                        entry["task_ids"].append(task["task_id"])
                    if task.get("command"):
                        entry["commands"].append(task["command"])
        except Exception as exc:
            entry["parse_error"] = f"{exc.__class__.__name__}: {exc}"
        manifests.append(entry)
    return manifests


def clone_or_use_local(receipts: ReceiptChain) -> tuple[Path | None, dict[str, Any]]:
    local = os.environ.get("CORE_LITE_LOCAL_PATH", "").strip()
    repo = os.environ.get("CORE_LITE_REPO", DEFAULT_REPO).strip() or DEFAULT_REPO
    branch = os.environ.get("CORE_LITE_BRANCH", DEFAULT_BRANCH).strip() or DEFAULT_BRANCH
    token = os.environ.get("CORE_LITE_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""

    if local:
        local_path = Path(local)
        meta = {
            "mode": "local",
            "repo": repo,
            "branch": branch,
            "root": local_path.as_posix(),
            "success": local_path.exists(),
        }
        receipts.record(
            "target_repo_selected",
            "LOCAL_PATH_SELECTED" if meta["success"] else "FAIL_CLOSED",
            "StegVerse-001 selected local target path for inspection.",
            meta,
        )
        return (local_path if local_path.exists() else None), meta

    work_dir = Path(os.environ.get("CORE_LITE_WORK_DIR", str(DEFAULT_WORK_DIR)))
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    clone_dir = work_dir / "core-lite"
    if repo.startswith(("http://", "https://")):
        url = repo
        safe_repo = repo
    else:
        safe_repo = repo
        url = f"https://x-access-token:{token}@github.com/{repo}.git" if token else f"https://github.com/{repo}.git"

    proc = subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", branch, url, str(clone_dir)],
        text=True,
        capture_output=True,
    )

    meta = {
        "mode": "clone",
        "repo": safe_repo,
        "branch": branch,
        "root": clone_dir.as_posix(),
        "runtime_work_dir": work_dir.as_posix(),
        "success": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "runtime_committed_path": False,
    }
    receipts.record(
        "target_repo_cloned",
        "CLONED" if proc.returncode == 0 else "FAIL_CLOSED",
        "StegVerse-001 cloned target repo into runtime temp space for inspection.",
        meta,
    )
    return (clone_dir if proc.returncode == 0 else None), meta


def determine_contract(repo_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    py_targets = {
        "cli": repo_root / "core_lite" / "cli.py",
        "cge": repo_root / "core_lite" / "cge.py",
        "ingest": repo_root / "core_lite" / "ingest.py",
        "sandbox": repo_root / "core_lite" / "sandbox.py",
        "receipts": repo_root / "core_lite" / "receipts.py",
    }
    py_contracts = {name: parse_python(path, repo_root) for name, path in py_targets.items()}

    cge_exports = set(py_contracts["cge"]["functions"]) | set(py_contracts["cge"]["classes"])
    observed_cge_imports: list[dict[str, Any]] = []
    missing_cge_exports: list[dict[str, str]] = []

    for module_name, contract in py_contracts.items():
        for item in contract.get("import_from", []):
            if import_targets_cge(item):
                need = {
                    "importing_module": module_name,
                    "from_module": item.get("module", ""),
                    "level": item.get("level", 0),
                    "names": item.get("names", []),
                }
                observed_cge_imports.append(need)
                for name in need["names"]:
                    if name not in cge_exports:
                        missing_cge_exports.append({"name": name, "required_by": module_name})

    workflows = inspect_workflows(repo_root)
    task_manifests = inspect_task_manifests(repo_root)

    surfaces = {
        "incoming": {
            "path": "incoming/",
            "exists": (repo_root / "incoming").exists(),
            "file_count": len([p for p in (repo_root / "incoming").rglob("*") if p.is_file()]) if (repo_root / "incoming").exists() else 0,
        },
        "reports_current": {
            "path": "reports/current/",
            "exists": (repo_root / "reports" / "current").exists(),
        },
        "receipts_current": {
            "path": "receipts/current/",
            "exists": (repo_root / "receipts" / "current").exists(),
        },
        "workflows": workflows,
        "task_manifests": task_manifests,
    }

    transition_requirements = {
        "incoming_bundle_detected": surfaces["incoming"]["exists"],
        "manifest_validation_surface": py_contracts["ingest"]["exists"],
        "cge_surface": py_contracts["cge"]["exists"],
        "sandbox_surface": py_contracts["sandbox"]["exists"],
        "receipt_surface": py_contracts["receipts"]["exists"],
        "workflow_execution_surface": bool(workflows),
    }

    blockers: list[dict[str, Any]] = []
    if missing_cge_exports:
        blockers.append({
            "type": "cge_contractual_inclusion",
            "basis": "Target modules import symbols from cge/core_lite.cge that are not exported by the current cge.py.",
            "items": missing_cge_exports,
        })

    for key, present in transition_requirements.items():
        if not present:
            blockers.append({
                "type": "missing_transition_surface",
                "basis": f"Required surface absent for active transition: {key}",
                "items": [key],
            })

    if missing_cge_exports:
        next_change = {
            "classification": "contractual_inclusion",
            "target": "core_lite/cge.py",
            "required_exports": sorted({item["name"] for item in missing_cge_exports}),
            "preserve_existing_exports": True,
            "basis": "Observed import contract requires these exports before existing intake/self-test surfaces can run.",
        }
    elif blockers:
        next_change = {
            "classification": "minimal_surface_completion",
            "target": "first_missing_transition_surface",
            "basis": "Complete only the missing surface required by the active transition.",
        }
    else:
        next_change = {
            "classification": "run_existing_intake",
            "target": "existing Core-Lite Intake workflow",
            "basis": "No structural blocker observed for the active transition.",
        }

    report = {
        "schema": "stegverse_001_remote_core_lite_working_contract_report.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": True,
        "actor": "StegVerse-001",
        "mode": "initialization",
        "target_repo_root": repo_root.resolve().as_posix(),
        "active_transition": "Core-Lite Recorded Ingestion + CGE + Sandbox Result Return",
        "python_contracts": py_contracts,
        "observed_cge_imports": observed_cge_imports,
        "cge_exports": sorted(cge_exports),
        "missing_cge_exports": missing_cge_exports,
        "surfaces": surfaces,
        "transition_requirements": transition_requirements,
        "blockers": blockers,
        "decision": "PLAN_RETURNED",
        "boundary": [
            "formalism-tests is the proof and command backdrop.",
            "core-lite is the remote target.",
            "This task does not patch, push, submit incoming bundles, or change workflows.",
            "Runtime clone is outside the repo working tree by default.",
            "STOP after report, plan, and receipt.",
        ],
    }

    plan = {
        "schema": "stegverse_001_remote_core_lite_remediation_plan.v2",
        "generated_at": report["generated_at"],
        "actor": "StegVerse-001",
        "transition": report["active_transition"],
        "decision": "RETURN_PLAN_ONLY",
        "install_authority": False,
        "production_authority": False,
        "workflow_change_authority": False,
        "push_authority": False,
        "incoming_submission_authority": False,
        "blockers": blockers,
        "next_admissible_change": next_change,
        "stop_condition": "Return plan and receipt. Do not mutate target repo.",
    }
    return report, plan


def write_markdown(report: dict[str, Any], plan: dict[str, Any]) -> None:
    lines = [
        "# StegVerse-001 Remote Core-Lite Working Contract Report",
        "",
        "## Status",
        "",
        "```text",
        f"actor: {report['actor']}",
        f"mode: {report['mode']}",
        f"active_transition: {report['active_transition']}",
        f"decision: {report['decision']}",
        f"blocker_count: {len(report['blockers'])}",
        "```",
        "",
        "## Role Separation",
        "",
        "```text",
        "formalism-tests = proof and command backdrop",
        "core-lite = remote target",
        "StegVerse-001 = initialization-state remote operator",
        "```",
        "",
        "## Observed CGE Import Contract",
        "",
    ]

    if report["observed_cge_imports"]:
        for item in report["observed_cge_imports"]:
            lines.append(
                f"- `{item['importing_module']}` imports `{', '.join(item['names'])}` from `{item['from_module']}`"
            )
    else:
        lines.append("No direct CGE imports observed in inspected modules.")

    lines.extend(["", "## Missing CGE Exports", ""])
    if report["missing_cge_exports"]:
        for item in report["missing_cge_exports"]:
            lines.append(f"- `{item['name']}` required by `{item['required_by']}`")
    else:
        lines.append("No missing CGE exports observed.")

    lines.extend(["", "## Transition Requirements", "", "```text"])
    for key, value in report["transition_requirements"].items():
        lines.append(f"{key}: {value}")

    lines.extend(["```", "", "## Next Admissible Change", "", "```json"])
    lines.append(json.dumps(plan["next_admissible_change"], indent=2, sort_keys=True))
    lines.extend([
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "No target mutation.",
        "No push.",
        "No workflow widening.",
        "No incoming bundle submission.",
        "No production.",
        "Runtime clone remains outside repo working tree by default.",
        "Return plan and receipt.",
        "STOP.",
        "```",
    ])

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    receipts = ReceiptChain(RECEIPTS)
    receipts.record(
        "remote_operator_started",
        "RECEIVED",
        "StegVerse-001 remote operator v2 started from formalism-tests backdrop.",
        {
            "target_repo": os.environ.get("CORE_LITE_REPO", DEFAULT_REPO),
            "branch": os.environ.get("CORE_LITE_BRANCH", DEFAULT_BRANCH),
        },
    )

    target_root, clone_meta = clone_or_use_local(receipts)
    if target_root is None:
        failure = {
            "schema": "stegverse_001_remote_core_lite_working_contract_report.v2",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "decision": "FAIL_CLOSED",
            "basis": "Could not access target repo.",
            "target_access": clone_meta,
        }
        REPORT_JSON.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        PLAN_JSON.write_text(json.dumps({
            "schema": "stegverse_001_remote_core_lite_remediation_plan.v2",
            "decision": "FAIL_CLOSED",
            "basis": "Could not access target repo.",
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        receipts.record("remote_operator_failed", "FAIL_CLOSED", "Could not access target repo.", clone_meta)
        print(json.dumps(failure, indent=2, sort_keys=True))
        return 1

    report, plan = determine_contract(target_root)
    report["target_access"] = clone_meta

    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PLAN_JSON.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(report, plan)

    receipts.record(
        "remote_contract_determined",
        "PLAN_RETURNED",
        "StegVerse-001 determined remote core-lite working contract and returned a plan.",
        {
            "report": REPORT_JSON.as_posix(),
            "plan": PLAN_JSON.as_posix(),
            "blocker_count": len(report["blockers"]),
            "next_admissible_change": plan["next_admissible_change"],
        },
    )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
