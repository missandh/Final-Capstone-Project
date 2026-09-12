"""Core clinical workflow tools."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ToolResult:
    """Return value used by agent tooling."""
    score: float
    rationale: str
    escalated: bool = False


def calculate_escalation_score(symptoms: List[str], risk_level: str = "low") -> ToolResult:
    """Compute a simple escalation score from symptom severity and risk level."""
    risk_weights = {"low": 0.1, "moderate": 0.5, "high": 0.9, "critical": 1.2}
    symptom_weights = {
        "chest pain": 0.55,
        "shortness of breath": 0.6,
        "fever": 0.2,
        "lethargy": 0.45,
        "bleeding": 0.5,
        "fainting": 0.5,
        "suicidal": 0.8,
        "stroke": 0.7,
    }

    score = risk_weights.get(risk_level.lower(), 0.1)
    for symptom in symptoms:
        score += symptom_weights.get(symptom.lower(), 0.1)

    escalated = score >= 1.0
    rationale = (
        "Urgent escalation is recommended due to high-risk symptoms and severity indicators."
        if escalated
        else "Routine review is appropriate; continue with standard workflow and documentation."
    )
    return ToolResult(score=min(score, 2.5), rationale=rationale, escalated=escalated)


def check_appointment_status(record_id: str) -> dict:
    """Check appointment status and compute a follow-up escalation score."""
    with open("data/appointments.json", "r", encoding="utf-8") as handle:
        records = json.load(handle)

    rec = next((r for r in records if r["record_id"].upper() == record_id.strip().upper()), None)
    if not rec:
        return {"error": f"Record {record_id} not found in Practo system."}

    norm_recency = min(rec["days_since_created"] / 30.0, 1.0)
    follow_up_val = 1.0 if rec["follow_up_required"] else 0.0
    escalation_score = round((0.60 * follow_up_val) + (0.40 * norm_recency), 3)

    return {
        "record_id": rec["record_id"],
        "category": rec["category"],
        "status": rec["status"],
        "consultation_fee_inr": rec["consultation_fee_inr"],
        "follow_up_required": rec["follow_up_required"],
        "escalation_score": escalation_score,
        "escalation_recommended": escalation_score >= 0.70,
    }
