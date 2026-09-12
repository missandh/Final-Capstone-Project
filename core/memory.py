"""In-memory session tracking for a local multi-agent system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SessionMemory:
    session_id: str
    messages: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def add_message(self, message: str) -> None:
        self.messages.append(message)

    def get_history(self) -> List[str]:
        return list(self.messages)


class MemoryStore:
    """Simple in-memory session store."""

    def __init__(self):
        self.sessions: Dict[str, SessionMemory] = {}

    def get_or_create(self, session_id: str) -> SessionMemory:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory(session_id=session_id)
        return self.sessions[session_id]
