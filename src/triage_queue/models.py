"""Triage item model for the priority queue."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class TriageItem:
    """A work item ordered by priority (higher = more urgent).

    Comparison uses ``priority`` first, then earlier ``created_at`` as a tie-breaker
    so older items of equal severity surface first (stable triage).
    """

    priority: int
    title: str
    description: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.priority < 0:
            raise ValueError("priority must be >= 0")

    def __lt__(self, other: "TriageItem") -> bool:
        if not isinstance(other, TriageItem):
            return NotImplemented
        if self.priority != other.priority:
            return self.priority < other.priority
        # Older item is "greater" for max-heap tie-break (treat first).
        return self.created_at > other.created_at

    def __repr__(self) -> str:
        return (
            f"TriageItem(id={self.id!r}, priority={self.priority}, "
            f"title={self.title!r})"
        )
