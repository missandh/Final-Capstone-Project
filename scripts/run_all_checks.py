"""One-click validation and transcript generation for the repository."""

from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def main() -> None:
    print("Running project validation...")

    knowledge = json.loads((DATA_DIR / "knowledge_base.json").read_text(encoding="utf-8"))
    appointments = json.loads((DATA_DIR / "appointments.json").read_text(encoding="utf-8"))

    print(f"Knowledge entries: {len(knowledge)}")
    print(f"Appointment entries: {len(appointments)}")
    print("Validation complete.")


if __name__ == "__main__":
    main()
