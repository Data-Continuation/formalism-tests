from pathlib import Path
from formalism_test_harness.harness import ingest, eval_formalism, run_case, verify_chain, playback, reconstruct, compare, confidence

def test_data_continuation() -> None:
    i = ingest("examples/data_continuation_allow.json")
    f = eval_formalism(i)
    assert i["decision"] == "ALLOW"
    assert f["decision"] == "ALLOW"

def test_gcat_deny() -> None:
    i = ingest("examples/gcat_bcat_deny.json")
    assert eval_formalism(i)["decision"] == "DENY"

def test_full_run(tmp_path: Path) -> None:
    r = run_case("examples/sandbox_case.json", tmp_path)
    assert r["decision"] == "ALLOW"
    assert (tmp_path / "original_receipts.jsonl").exists()
    assert (tmp_path / "confidence_report.json").exists()

def test_reconstruct_compare_confidence(tmp_path: Path) -> None:
    run_case("examples/data_continuation_allow.json", tmp_path)
    assert playback(tmp_path / "original_receipts.jsonl", tmp_path)["decision"] == "ALLOW"
    assert reconstruct(tmp_path, tmp_path / "reconstruction")["decision"] == "ALLOW"
    assert compare(tmp_path / "original_receipts.jsonl", tmp_path / "reconstruction" / "reconstructed_receipts.jsonl", tmp_path)["alignment"] == 1.0
    assert confidence(tmp_path, tmp_path)["confidence"] >= 0.85

def test_tamper(tmp_path: Path) -> None:
    run_case("examples/data_continuation_allow.json", tmp_path)
    p = tmp_path / "original_receipts.jsonl"
    p.write_text(p.read_text().replace("ALLOW", "DENY", 1), encoding="utf-8")
    assert verify_chain(p)["decision"] == "FAIL_CLOSED"
