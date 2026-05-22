#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXTURE = Path("tests/fixtures/stage26_stegverse001_testing_loop_cases.json")
REPORT = Path("reports/stage26_stegverse001_testing_loop_report.json")
RECEIPTS = Path("reports/stage26_stegverse001_testing_loop_receipts.jsonl")

EXPECTED_ENTITY = "StegVerse-001"
EXPECTED_AUTHORITY = "formalism-tests"
EXPECTED_RUNNER = "tools/run_declared_tasks.py"
EXPECTED_MANIFEST = "tools/tasks/formalism_tests_tasks.json"

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()

def req(ok, msg):
    if not ok:
        raise AssertionError(msg)
    return 1

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def task_ids_from_manifest(path):
    manifest = load_json(path)
    return {task.get("task_id") for task in manifest.get("tasks", [])}

def run_declared_child_task(task_id):
    completed = subprocess.run(
        [sys.executable, EXPECTED_RUNNER, EXPECTED_MANIFEST, "--task-id", task_id],
        capture_output=True,
        text=True,
        check=False,
    )
    result = {
        "task_id": task_id,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "success": completed.returncode == 0,
    }

    report_path = Path("declared_task_report.json")
    if report_path.exists():
        try:
            declared_report = load_json(report_path)
            result["declared_task_report_success"] = declared_report.get("success")
            result["declared_task_report_task_count"] = declared_report.get("task_count")
        except Exception as exc:
            result["declared_task_report_error"] = str(exc)

    return result

def decide(case):
    if case.get("entity_id") != EXPECTED_ENTITY:
        return "FAIL_CLOSED", "unknown work-entity"
    if case.get("entity_status") != "active":
        return "FAIL_CLOSED", "work-entity is not active"
    if not case.get("transition_table_bound"):
        return "FAIL_CLOSED", "work-entity is not bound to the Transition Table"
    if case.get("execution_authority") != EXPECTED_AUTHORITY:
        return "FAIL_CLOSED", "test-loop execution authority must remain formalism-tests"
    if case.get("runner") != EXPECTED_RUNNER:
        return "FAIL_CLOSED", "StegVerse-001 must use the declared-task runner"
    if case.get("manifest_path") != EXPECTED_MANIFEST:
        return "FAIL_CLOSED", "StegVerse-001 must use the declared task manifest"
    if case.get("direct_runner_bypass_attempted"):
        return "FAIL_CLOSED", "direct stage-runner bypass is not allowed"
    if not case.get("all_target_tasks_declared"):
        return "FAIL_CLOSED", "one or more target task IDs are not declared"
    if not case.get("all_child_tasks_success"):
        return "FAIL_CLOSED", "one or more child declared tasks failed"
    if not case.get("all_child_reports_present"):
        return "FAIL_CLOSED", "one or more child reports are missing"
    if not case.get("all_child_receipts_present"):
        return "FAIL_CLOSED", "one or more child receipt files are missing"
    if case.get("canonical_mutation_requested"):
        return "FAIL_CLOSED", "test loop may not mutate canonical release artifacts"
    if case.get("site_claims_authority"):
        return "FAIL_CLOSED", "Site cannot become proof, test, or release authority"

    if case.get("ledger_record_required"):
        if case.get("ledger_record_emitted"):
            return "LEDGER_TEST_LOOP", "StegVerse-001 test loop ledger entry recorded"
        return "FAIL_CLOSED", "test-loop ledger record missing"

    return "ALLOW_TEST_LOOP", "StegVerse-001 may handle testing through declared-task routing"

def main():
    try:
        data = load_json(FIXTURE)
        checks = 0
        receipts = []
        counts = {}
        child_results = []

        checks += req(data.get("stage") == "Stage 26", "stage must be Stage 26")
        checks += req(data.get("work_entity", {}).get("entity_id") == EXPECTED_ENTITY, "work entity must be StegVerse-001")
        checks += req(data.get("work_entity", {}).get("entity_status") == "active", "work entity must be active")
        checks += req(data.get("work_entity", {}).get("transition_table_bound") is True, "work entity must be Transition-Table-bound")
        checks += req(data.get("declared_runner") == EXPECTED_RUNNER, "declared runner mismatch")
        checks += req(data.get("child_manifest") == EXPECTED_MANIFEST, "child manifest mismatch")

        required_task_ids = data.get("required_task_ids", [])
        checks += req(len(required_task_ids) == 9, "Stage 26 must run Stage 17 through Stage 25 task IDs")

        declared_task_ids = task_ids_from_manifest(EXPECTED_MANIFEST)
        for task_id in required_task_ids:
            checks += req(task_id in declared_task_ids, f"missing required child task_id in manifest: {task_id}")

        for task_id in required_task_ids:
            child_result = run_declared_child_task(task_id)
            child_results.append(child_result)
            checks += req(child_result["success"] is True, f"child declared task failed: {task_id}")

        for control in data.get("required_controls", []):
            checks += req(isinstance(control, str) and control, f"invalid required control: {control}")

        for case in data["cases"]:
            case_id = case.get("case_id", "<missing>")
            checks += req(case.get("expected_decision"), f"{case_id}: missing expected_decision")
            checks += req(isinstance(case.get("target_task_ids"), list), f"{case_id}: target_task_ids must be a list")
            decision, basis = decide(case)
            checks += req(decision == case["expected_decision"], f"{case_id}: expected {case['expected_decision']}, got {decision}")

            receipt = {
                "schema": "stegverse_stage26_stegverse001_testing_loop_receipt.v1",
                "case_id": case_id,
                "entity_id": case["entity_id"],
                "decision": decision,
                "basis": basis,
                "authority_boundary": data["authority_boundary"],
            }
            receipt["receipt_hash"] = digest(receipt)
            receipts.append(receipt)
            counts[decision] = counts.get(decision, 0) + 1

        for required_decision in ["ALLOW_TEST_LOOP", "FAIL_CLOSED", "LEDGER_TEST_LOOP"]:
            checks += req(required_decision in counts, f"missing decision coverage {required_decision}")

        REPORT.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        RECEIPTS.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in receipts), encoding="utf-8")

        report = {
            "schema": "stegverse_stage26_stegverse001_testing_loop_report.v1",
            "success": True,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stage": "Stage 26",
            "theorem_basis": data["theorem_basis"],
            "assertion_count": checks,
            "case_count": len(data["cases"]),
            "receipt_count": len(receipts),
            "decision_counts": counts,
            "child_task_count": len(child_results),
            "child_results": child_results,
            "work_entity": "StegVerse-001 / Beta_Orionis",
            "message": "Stage 26 StegVerse-001 declared testing loop validation passed.",
            "report": str(REPORT),
            "receipts": str(RECEIPTS),
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "schema": "stegverse_stage26_stegverse001_testing_loop_report.v1",
            "success": False,
            "error": str(exc),
        }
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    sys.exit(main())
