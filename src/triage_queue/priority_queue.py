"""Priority queue backed by ``heapq`` (stdlib binary heap)."""
from __future__ import annotations

import heapq
from typing import Generic, List, Tuple, TypeVar

from .models import Patient

T = TypeVar("T")

# Heap entry: (triage_level, arrived_at, sequence, patient)
# heapq is a min-heap, so smaller triage_level (more urgent) rises first;
# earlier arrived_at breaks ties; sequence makes equal timestamps stable/unique.
_HeapEntry = Tuple[int, object, int, Patient]


class PriorityQueue:
    """Min-heap over urgency keys using ``heapq``.

    Why ``heapq`` (see DESIGN.md): O(log n) enqueue/dequeue while preserving
    triage level + arrival order, without maintaining a fully sorted list.
    """

    def __init__(self) -> None:
        self._heap: List[_HeapEntry] = []
        self._seq = 0

    def __len__(self) -> int:
        return len(self._heap)

    @property
    def is_empty(self) -> bool:
        return not self._heap

    def enqueue(self, patient: Patient) -> None:
        entry: _HeapEntry = (
            patient.triage_level,
            patient.arrived_at,
            self._seq,
            patient,
        )
        self._seq += 1
        heapq.heappush(self._heap, entry)

    def peek(self) -> Patient:
        if self.is_empty:
            raise IndexError("peek from empty priority queue")
        return self._heap[0][3]

    def dequeue(self) -> Patient:
        if self.is_empty:
            raise IndexError("dequeue from empty priority queue")
        return heapq.heappop(self._heap)[3]

    def items(self) -> List[Patient]:
        """Return waiting patients (heap order, not attention order)."""
        return [entry[3] for entry in self._heap]
