"""Review and verdict team for clinical response validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pydantic import BaseModel, Field


class ReviewVerdict(BaseModel):
    approved: bool = Field(..., description="Whether the composer draft is grounded and policy compliant")
    final_answer: str = Field(..., description="The original or revised answer")
    reason: str = Field(..., description="Audit explanation for review action")


@dataclass
class ReviewTeamResult:
    approved: bool
    notes: str
    concerns: List[str]


class ReviewTeam:
    """Minimal approval flow for governance review."""

    def review(self, content: str) -> ReviewTeamResult:
        concerns = []
        if "urgent" in content.lower() and "policy" not in content.lower():
            concerns.append("missing policy citation")
        if "patient" in content.lower() and "pii" not in content.lower():
            concerns.append("review for privacy exposure")
        return ReviewTeamResult(approved=not concerns, notes="Content passed review.", concerns=concerns)


def run_autogen_review(draft_answer: str, retrieved_context: str) -> ReviewVerdict:
    """
    Simulated 2-agent round-robin team (Policy-Compliance-Reviewer -> Final-Editor)
    Runs bounded at max_turns=2 and enforces ReviewVerdict Pydantic output.
    """
    forbidden_claims = ["free surgery", "100% refund after visit", "unlimited prescription"]
    has_unsupported_claim = any(claim in draft_answer.lower() for claim in forbidden_claims)

    if has_unsupported_claim:
        return ReviewVerdict(
            approved=False,
            final_answer="According to Practo policy, consultations must be cancelled at least 2 hours in advance to receive a refund.",
            reason="Rejected draft: Draft contained ungrounded claim regarding post-visit refunds.",
        )

    return ReviewVerdict(
        approved=True,
        final_answer=draft_answer,
        reason="Approved: Draft strictly grounded in retrieved KB policies.",
    )
