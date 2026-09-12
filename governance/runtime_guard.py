"""Runtime guard enforcing least autonomy and token budgets."""

from __future__ import annotations

MAX_TOKEN_BUDGET = 250


class SecurityException(Exception):
    pass


def execute_agent_tool(agent_name: str, tool_name: str, **kwargs):
    """
    Strict enforcement of Least Autonomy:
    Only Lookup_Agent is privileged to query clinical databases.
    """
    if tool_name == "check_appointment_status" and agent_name != "Lookup_Agent":
        raise SecurityException(
            f"GOVERNANCE VIOLATION: Agent '{agent_name}' attempted to invoke restricted tool '{tool_name}'."
        )
    return {"agent": agent_name, "tool": tool_name, "args": kwargs}


def runtime_token_guard(input_text: str):
    """Simulated token estimation: 1 token ~= 4 chars."""
    estimated_tokens = len(input_text) // 4
    if estimated_tokens > MAX_TOKEN_BUDGET:
        raise ValueError(
            f"BUDGET EXCEEDED: Request estimated at {estimated_tokens} tokens exceeds maximum limit of {MAX_TOKEN_BUDGET} tokens."
        )
    return True


class RuntimeGuard:
    """Simple governance gate for autonomy and token consumption."""

    def __init__(self, max_tokens: int = 500, max_autonomy: int = 2):
        self.max_tokens = max_tokens
        self.max_autonomy = max_autonomy
        self.tokens_used = 0
        self.autonomy_level = 0

    def update(self, tokens_used: int, autonomy_level: int | None = None) -> bool:
        self.tokens_used += tokens_used
        if autonomy_level is not None:
            self.autonomy_level = autonomy_level
        return self.tokens_used <= self.max_tokens and self.autonomy_level <= self.max_autonomy

    def allow(self) -> bool:
        return self.tokens_used <= self.max_tokens and self.autonomy_level <= self.max_autonomy
