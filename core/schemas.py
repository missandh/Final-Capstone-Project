"""Pydantic response models."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AgentResponseSchema(BaseModel):
    query: str
    response: str
    source_documents: List[str] = Field(default_factory=list)
    escalation_flag: bool = False
    confidence_score: float = Field(ge=0.0, le=1.0)
    audit_trace_id: str


class RiskAssessment(BaseModel):
    """Structured output for a clinical risk review."""

    urgency: str = Field(..., description="low, moderate, high, or critical")
    escalation_required: bool = Field(default=False)
    rationale: str
    citations: List[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Response envelope used across agents."""

    answer: str
    risk: RiskAssessment
    token_budget_used: int = 0
    session_id: Optional[str] = None
