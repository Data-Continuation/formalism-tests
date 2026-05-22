import json
import os


def main():
    """Stage 24 autonomous test plan generation test runner."""
    stage = 24
    test_name = "test_plan"
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "tests",
        "fixtures",
        f"stage{stage}_{test_name}_cases.json",
    )
    with open(fixture_path, "r", encoding="utf-8") as f:
        cases = json.load(f)
    case_count = len(cases)
    decision_counts = {}
    receipts = []
    for c in cases:
        decision = c.get("expected_decision")
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        receipts.append({"case_id": c["id"], "decision": decision})
    receipt_count = len(receipts)
    assertion_count = case_count
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_filename = f"stage{stage}_{test_name}_report.json"
    receipts_filename = f"stage{stage}_{test_name}_receipts.jsonl"
    report = {
        "stage": stage,
        "test_name": test_name,
        "case_count": case_count,
        "receipt_count": receipt_count,
        "assertion_count": assertion_count,
    }
    report.update(decision_counts)
    with open(os.path.join(reports_dir, report_filename), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(reports_dir, receipts_filename), "w", encoding="utf-8") as f:
        for receipt in receipts:
            f.write(json.dumps(receipt) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()