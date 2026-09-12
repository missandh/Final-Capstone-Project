"""Robust base LLM abstraction for deterministic local workflows."""

from __future__ import annotations

import os
import re
from typing import Any, List

from crewai.llms.base_llm import BaseLLM

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"


class DeterministicMockLLM(BaseLLM):
    """
    Zero-network local mock engine extending CrewAI's BaseLLM.
    Dispatches tool calls cleanly without matching prompt templates.
    """

    def __init__(self, model_name: str = "mock-practo-model"):
        super().__init__(model=model_name)

    def call(self, messages: List[dict], callbacks: Any = None) -> str:
        last_msg = messages[-1]["content"] if messages else ""

        match_id = re.search(r"PRAC-\d{4}", last_msg, re.IGNORECASE)
        if match_id and "Action: check_appointment_status" not in last_msg and "Observation:" not in last_msg:
            rec_id = match_id.group(0).upper()
            return f"Action: check_appointment_status\nAction Input: {{\"record_id\": \"{rec_id}\"}}"

        if "Observation:" in last_msg:
            obs = last_msg.split("Observation:")[-1].strip()
            return f"Final Answer: According to our hospital records, {obs}"

        if "Action: rag_lookup" not in last_msg and "Observation:" not in last_msg and (
            "policy" in last_msg.lower() or "fee" in last_msg.lower() or "cancel" in last_msg.lower()
        ):
            query_match = re.search(r"User Query: (.*)", last_msg)
            q = query_match.group(1) if query_match else "policy"
            return f"Action: rag_lookup\nAction Input: {{\"query\": \"{q}\"}}"

        return "Final Answer: The requested clinical support service has been processed in accordance with Practo regulations."


class BaseLLMWrapper:
    """Backward-compatible wrapper used by older code paths."""

    def __init__(self, model_name: str = "local-mock"):
        self.model_name = model_name

    def invoke(self, prompt: str, **kwargs: Any) -> str:
        lower_prompt = prompt.lower()
        if "triage" in lower_prompt or "escalate" in lower_prompt:
            return "Escalate to emergency clinical review and document rationale."
        if "summary" in lower_prompt:
            return "Summary: relevant policy context supports urgent evaluation."
        return f"Model={self.model_name}; prompt_tokens={len(prompt.split())}; status=ok"

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.invoke(prompt, **kwargs)


MockLLM = BaseLLMWrapper
