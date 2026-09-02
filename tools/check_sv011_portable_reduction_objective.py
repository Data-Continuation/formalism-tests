#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
REQUIRED_TESTS = {
    "admitted_capability",
    "denied_capability",
    "stale_or_unknown_basis",
    "stopped_chain",
    "replay_no_authority",
    "ordered_reconstruction",
}

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def check(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "stegverse.sv011-portable-reduction-objective/v0.1":
        fail("unexpected schema")
    if data.get("entity_id") != "SV-011":
        fail("entity_id must be SV-011")

    package_class = data.get("package_class")
    if package_class not in {"bootstrap_minimal", "offline_self_contained"}:
        fail("unsupported package_class")

    artifact = data.get("artifact") or {}
    if artifact.get("format") not in {"tar.gz", "zip"}:
        fail("artifact format must be tar.gz or zip")
    if not artifact.get("filename"):
        fail("artifact filename required")
    if not SHA256.fullmatch(str(artifact.get("sha256", ""))):
        fail("artifact sha256 required")
    for key in ("compressed_bytes", "file_count"):
        if not isinstance(artifact.get(key), int) or artifact[key] < 1:
            fail(f"{key} must be positive integer")
    if not isinstance(artifact.get("dependency_count"), int) or artifact["dependency_count"] < 0:
        fail("dependency_count must be non-negative integer")

    install = data.get("installation") or {}
    if install.get("fresh_destination") is not True:
        fail("installation must be proven in a fresh destination")
    if install.get("result") != "PASS":
        fail("fresh installation must PASS")
    if not install.get("steps"):
        fail("installation steps required")
    if package_class == "offline_self_contained" and install.get("network_required") is not False:
        fail("offline_self_contained must not require network")

    tests = data.get("self_tests") or []
    ids = [t.get("test_id") for t in tests]
    if set(ids) != REQUIRED_TESTS or len(ids) != len(REQUIRED_TESTS):
        fail("self_tests must contain each canonical test exactly once")
    for t in tests:
        if t.get("result") != "PASS" or not t.get("receipt_id"):
            fail("each self-test must PASS and emit a receipt")

    ablation = data.get("ablation") or {}
    if ablation.get("method") != "remove_rebuild_reinstall_retest":
        fail("ablation method drift")
    components = ablation.get("irreducible_components") or []
    if not components:
        fail("at least one irreducible component required")
    for item in components:
        if not item.get("component"):
            fail("ablation component name required")
        if item.get("removal_breaks_invariant") is not True:
            fail("irreducible component removal must break an invariant")
        if not item.get("failed_test_ids"):
            fail("ablation must name failed invariant tests")
        if not item.get("evidence_receipt_id"):
            fail("ablation evidence receipt required")

    authority = data.get("authority") or {}
    if authority.get("package_installation_is_runtime_authority") is not False:
        fail("package installation is not runtime authority")
    if authority.get("workflow_pass_is_runtime_authority") is not False:
        fail("workflow pass is not runtime authority")

    print("PASS: SV-011 portable reduction objective satisfies v0.1 contract")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_sv011_portable_reduction_objective.py <objective.json>")
    check(Path(sys.argv[1]))
