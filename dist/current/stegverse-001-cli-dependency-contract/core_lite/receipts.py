from __future__ import annotations

from pathlib import Path
from typing import Any


class ReceiptRecorder:
    def __init__(self, path: Path) -> None:
        self.path = path

    def record(self, event_type: str, decision: str, basis: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"event_type": event_type, "decision": decision, "basis": basis, "metadata": metadata or {}}

def append_receipt(repo_root: Path | str = ".", receipt: dict[str, Any] | None = None, **metadata: Any) -> dict[str, Any]:
    root = Path(repo_root)
    recorder = ReceiptRecorder(root / ".stegverse" / "receipts" / "core_lite_receipts.jsonl")
    payload = receipt if receipt is not None else {}
    if not isinstance(payload, dict):
        payload = {"value": repr(payload)}
    if metadata:
        payload = {**payload, **metadata}
    return recorder.record(
        event_type=str(payload.get("event_type", "core_lite_cli_receipt")),
        decision=str(payload.get("decision", "RECORDED")),
        basis=str(payload.get("basis", "Core-Lite CLI receipt recorded.")),
        metadata=payload,
    )
