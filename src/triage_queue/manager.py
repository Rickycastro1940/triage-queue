"""High-level triage queue manager."""
from __future__ import annotations

import uuid
from typing import Iterable, List, Optional

from .models import TriageItem
from .priority_queue import PriorityQueue


class TriageQueueManager:
    """Manages triage items with a max-heap priority queue."""

    def __init__(self) -> None:
        self._queue: PriorityQueue[TriageItem] = PriorityQueue()

    def __len__(self) -> int:
        return len(self._queue)

    @property
    def is_empty(self) -> bool:
        return self._queue.is_empty

    def submit(
        self,
        title: str,
        priority: int,
        description: str = "",
        **metadata,
    ) -> TriageItem:
        """Enqueue a new triage item and return it."""
        item = TriageItem(
            priority=priority,
            title=title,
            description=description,
            metadata=dict(metadata),
            id=str(uuid.uuid4())[:8],
        )
        self._queue.enqueue(item)
        return item

    def next(self) -> TriageItem:
        """Peek at the highest-priority item."""
        return self._queue.peek()

    def treat_next(self) -> TriageItem:
        """Dequeue (treat) the highest-priority item."""
        return self._queue.dequeue()

    def drain(self) -> List[TriageItem]:
        """Dequeue all items in priority order."""
        out: List[TriageItem] = []
        while not self.is_empty:
            out.append(self.treat_next())
        return out

    def seed(self, items: Iterable[TriageItem]) -> None:
        for item in items:
            if item.id is None:
                item.id = str(uuid.uuid4())[:8]
            self._queue.enqueue(item)
