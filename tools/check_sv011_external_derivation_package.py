#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

CANONICAL_OUTCOMES = {
    "ALLOW", "ALLOW_WITH_SIGNOFF", "DENY", "FAIL_CLOSED", "REDIRECT", "ESCALATE"
}
REQUIRED_BLOCKS = {
    "role_change_declared",
    "transition_class_declared",
    "authority_current",
    "evidence_fresh",
    "scope_valid",
    "trust_basis_current",
    "risk_basis_current",
    "receipt_required",
    "fail_closed_if_missing",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def ordered_root(receipt_ids: list[str]) -> str:
    payload = "\n".join(receipt_ids).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def check(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    if data.get("schema") != "stegverse.sv011-external-derivation-package/v0.1":
        fail("unexpected schema")
    if data.get("entity_id") != "SV-011":
        fail("entity_id must be SV-011")

    element = data.get("first_transition_element") or {}
    if not element.get("element_id") or not SHA256.fullmatch(str(element.get("sha256", ""))):
        fail("first transition element must be identified and sha256-bound")

    pins = data.get("source_pins") or []
    if len(pins) < 3:
        fail("at least three exact source pins are required")
    for pin in pins:
        if not pin.get("repository") or not pin.get("path"):
            fail("source pin missing repository/path")
        if not HEX40.fullmatch(str(pin.get("commit", ""))) or not HEX40.fullmatch(str(pin.get("blob", ""))):
            fail("source pins require exact 40-hex commit and blob identities")

    authority = data.get("authority") or {}
    for key in ("execution_authorized", "publication_authorized", "proofs_accepted"):
        if authority.get(key) is not False:
            fail(f"{key} must remain false for the minimum milestone")

    cases = data.get("cases") or []
    if len(cases) < 2:
        fail("minimum milestone requires at least two cases")

    decisions = []
    receipt_ids = []
    for case in cases:
        decision = case.get("decision")
        if decision not in CANONICAL_OUTCOMES:
            fail(f"non-canonical decision: {decision}")
        decisions.append(decision)

        blocks = set(case.get("required_blocks") or [])
        if blocks != REQUIRED_BLOCKS:
            missing = sorted(REQUIRED_BLOCKS - blocks)
            extra = sorted(blocks - REQUIRED_BLOCKS)
            fail(f"required block set drift: missing={missing} extra={extra}")

        block_results = case.get("block_results") or {}
        if set(block_results) != REQUIRED_BLOCKS:
            fail("block_results must cover the exact required block set")

        if not case.get("source_role") or not case.get("target_role"):
            fail("source and target roles are required")
        if not case.get("capability"):
            fail("capability identifier is required")
        rid = case.get("receipt_id")
        if not rid:
            fail("receipt_id is required")
        receipt_ids.append(rid)

    if "ALLOW" not in decisions:
        fail("minimum milestone requires one admitted capability (ALLOW)")
    if not any(d in {"DENY", "FAIL_CLOSED"} for d in decisions):
        fail("minimum milestone requires one denied or fail-closed capability")

    recon = data.get("reconstruction") or {}
    ordered_ids = recon.get("ordered_receipt_ids") or []
    if ordered_ids != receipt_ids:
        fail("reconstruction receipt ordering must equal case receipt ordering")
    expected_root = ordered_root(receipt_ids)
    if recon.get("ordered_root") != expected_root:
        fail(f"ordered_root mismatch; expected {expected_root}")

    print("PASS: SV-011 external derivation package satisfies v0.1 minimum milestone contract")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_sv011_external_derivation_package.py <package.json>")
    check(Path(sys.argv[1]))
