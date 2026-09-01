#!/usr/bin/env python3
"""Verify committed MindForge boundary-semantics artifacts against canonical fixtures."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"reports/mindforge_boundary_semantics_report.json"
RECEIPTS=ROOT/"receipts/mindforge_boundary_semantics_execution_receipts.jsonl"
EXPECTED=ROOT/"tests/fixtures/mindforge_boundary_semantics_expected_outcomes.json"
OUTPUT=ROOT/"reports/mindforge_boundary_semantics_artifact_verification.json"
AUTHORITY="ARCHITECTURAL_BOUNDARY_SEMANTICS_ONLY"

def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main()->int:
    expected=json.loads(EXPECTED.read_text())["expected_outcomes"]
    report=json.loads(REPORT.read_text())
    rows=[json.loads(line) for line in RECEIPTS.read_text().splitlines() if line.strip()]
    errors=[]
    if report.get("status")!="PASS": errors.append("report status != PASS")
    if report.get("case_count")!=10 or report.get("passed_count")!=10 or report.get("failed_count")!=0:
        errors.append("report counts are not 10/10/0")
    if report.get("allow_executes_transition") is not False:
        errors.append("ALLOW must not execute transition")
    if report.get("authority_posture")!=AUTHORITY:
        errors.append("authority posture mismatch")
    report_rows=report.get("results")
    if not isinstance(report_rows,list) or len(report_rows)!=10:
        errors.append("report results must contain 10 rows")
        report_rows=[]
    if len(rows)!=10:
        errors.append("receipt chain must contain 10 rows")
    by_report={r.get("case_id"):r for r in report_rows if isinstance(r,dict)}
    by_receipt={r.get("case_id"):r for r in rows if isinstance(r,dict)}
    if set(by_report)!=set(expected) or set(by_receipt)!=set(expected):
        errors.append("report/receipt case IDs must equal expected-outcome IDs")
    for case_id,outcome in expected.items():
        rr=by_report.get(case_id,{})
        rc=by_receipt.get(case_id,{})
        for obj,label in ((rr,"report"),(rc,"receipt")):
            if obj.get("expected")!=outcome or obj.get("result")!=outcome:
                errors.append(f"{case_id} {label} outcome mismatch")
            if obj.get("execution_invoked") is not False:
                errors.append(f"{case_id} {label} execution_invoked must be false")
        if rr and rc and rr!=rc:
            errors.append(f"{case_id} report/receipt semantic mismatch")
    result={
      "schema":"stegverse.mindforge-boundary-semantics.artifact-verification.v1",
      "status":"PASS" if not errors else "FAIL",
      "authority_posture":AUTHORITY,
      "case_count":len(expected),
      "report_receipt_equivalence":not any("semantic mismatch" in e for e in errors),
      "expected_outcome_equivalence":not any("outcome mismatch" in e for e in errors),
      "no_execution_invoked":not any("execution_invoked" in e for e in errors),
      "artifact_hashes":{
        "report_sha256":sha256(REPORT),
        "receipts_sha256":sha256(RECEIPTS),
        "expected_outcomes_sha256":sha256(EXPECTED),
      },
      "errors":errors,
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if not errors else 1

if __name__=="__main__":
    raise SystemExit(main())
