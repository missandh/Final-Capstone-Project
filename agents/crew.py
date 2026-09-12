"""Multi-agent orchestration for the domain assistant."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class AgentTask:
    name: str
    instructions: str
    context: List[str] | None = None


class Crew:
    """Simple orchestration stub for a multi-agent workflow."""

    def __init__(self):
        self.tasks: List[AgentTask] = []

    def add_task(self, task: AgentTask) -> None:
        self.tasks.append(task)

    def run(self) -> List[str]:
        return [f"executed:{task.name}" for task in self.tasks]
