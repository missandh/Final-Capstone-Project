"""JSONL structured tracing utilities."""

from __future__ import annotations

import datetime
import json
import uuid

from core.guardrails import mask_pii_contact


def log_structured_event(event_type: str, raw_query: str, status_code: int, latency_ms: float):
    trace_id = str(uuid.uuid4())
    safe_query = mask_pii_contact(raw_query)
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "trace_id": trace_id,
        "event_type": event_type,
        "query": safe_query,
        "status_code": status_code,
        "latency_ms": round(latency_ms, 2),
    }
    with open("practo_audit.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(log_entry) + "\n")
    return trace_id


class JSONLTracer:
    """Minimal structured logger writing one JSON object per line."""

    def __init__(self, log_path: str = "./logs/trace.jsonl"):
        self.log_path = log_path

    def log(self, event: str, payload: dict | None = None) -> None:
        trace_id = log_structured_event(event, str(payload or {}), 200, 0.0)
        with open(self.log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"event": event, "trace_id": trace_id, "payload": payload or {}}) + "\n")
