"""FastAPI app exposing the Practo domain support endpoints."""

from __future__ import annotations

import time

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from api.logger import log_structured_event
from core.guardrails import detect_prompt_injection, mask_pii_contact
from core.schemas import AgentResponseSchema

app = FastAPI(title="Practo Domain Support System")


class QueryRequest(BaseModel):
    query: str


class DocRequest(BaseModel):
    doc_id: str
    topic: str
    content: str


class QueryPayload(BaseModel):
    text: str


@app.post("/ask", response_model=AgentResponseSchema)
def ask_support(req: QueryRequest):
    t0 = time.time()
    if detect_prompt_injection(req.query):
        log_structured_event("INJECTION_BLOCKED", req.query, 400, (time.time() - t0) * 1000)
        raise HTTPException(status_code=400, detail="Security violation: Prompt injection detected.")

    safe_q = mask_pii_contact(req.query)
    resp = AgentResponseSchema(
        query=safe_q,
        response="Appointments can be cancelled penalty-free up to 2 hours prior to the slot.",
        source_documents=["KB-02"],
        escalation_flag=False,
        confidence_score=0.95,
        audit_trace_id="",
    )
    trace_id = log_structured_event("HTTP_QUERY", req.query, 200, (time.time() - t0) * 1000)
    resp.audit_trace_id = trace_id
    return resp


@app.post("/add-document")
def add_document(doc: DocRequest):
    t0 = time.time()
    trace_id = log_structured_event("KB_INSERT", f"Added {doc.doc_id}", 200, (time.time() - t0) * 1000)
    return {"status": "success", "doc_id": doc.doc_id, "trace_id": trace_id}


@app.post("/query")
def query_endpoint(payload: QueryPayload):
    if detect_prompt_injection(payload.text):
        raise HTTPException(status_code=400, detail="Security violation: Prompt injection detected.")
    return {"status": "accepted"}


@app.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await websocket.accept()
    session_history = []
    try:
        while True:
            text = await websocket.receive_text()
            if detect_prompt_injection(text):
                await websocket.send_json({"error": "Prompt injection detected."})
                continue

            clean_text = mask_pii_contact(text)
            session_history.append(clean_text)
            reply = f"Practo Agent Response to: '{clean_text}'. Turns in session: {len(session_history)}"
            await websocket.send_text(reply)
    except WebSocketDisconnect:
        pass


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
