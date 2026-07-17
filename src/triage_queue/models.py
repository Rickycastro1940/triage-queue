"""Patient data model for the triage queue."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Patient:
    """A patient waiting for care.

    Required fields:
    - ``name``: patient display name
    - ``triage_level``: int from 1 (most urgent) to 3 (least urgent)
    - ``arrived_at``: arrival timestamp (UTC by default)
    """

    name: str
    triage_level: int
    arrived_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not isinstance(self.triage_level, int) or not (1 <= self.triage_level <= 3):
            raise ValueError("triage_level must be an int in the range 1–3")
        if not self.name or not str(self.name).strip():
            raise ValueError("name must be a non-empty string")

    def __lt__(self, other: "Patient") -> bool:
        """Order for a max-heap: more urgent / earlier arrival is "greater".

        Level 1 is most urgent; level 3 is least urgent. Equal levels break ties
        by earlier ``arrived_at`` (FIFO).
        """
        if not isinstance(other, Patient):
            return NotImplemented
        if self.triage_level != other.triage_level:
            # Higher level number ⇒ less urgent ⇒ "less" in max-heap order.
            return self.triage_level > other.triage_level
        # Older arrival is more urgent among equals.
        return self.arrived_at > other.arrived_at

    def __repr__(self) -> str:
        return (
            f"Patient(name={self.name!r}, triage_level={self.triage_level}, "
            f"arrived_at={self.arrived_at.isoformat()})"
        )
