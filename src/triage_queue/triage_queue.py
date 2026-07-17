"""TriageQueue — priority queue manager for patients."""
from __future__ import annotations

from typing import Dict, List, Optional

from .models import Patient
from .priority_queue import PriorityQueue


class EmptyTriageQueueError(LookupError):
    """Raised when peek/dequeue is attempted on an empty triage queue."""


class TriageQueue:
    """Manages waiting patients with an internal max-heap priority queue.

    Patients are ordered by ``triage_level`` (1 = most urgent … 3 = least urgent),
    then by earlier ``arrived_at`` when levels match.
    """

    def __init__(self) -> None:
        self._pq: PriorityQueue[Patient] = PriorityQueue()

    def __len__(self) -> int:
        return len(self._pq)

    def __bool__(self) -> bool:
        return not self._pq.is_empty

    @property
    def is_empty(self) -> bool:
        return self._pq.is_empty

    def enqueue(self, patient: Patient) -> None:
        """Add a patient; position respects triage level and arrival order."""
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient instance")
        self._pq.enqueue(patient)

    def dequeue(self) -> Patient:
        """Remove and return the next patient to be attended."""
        if self.is_empty:
            raise EmptyTriageQueueError(
                "Cannot dequeue: the triage queue is empty"
            )
        return self._pq.dequeue()

    def peek(self) -> Patient:
        """Return the next patient without removing them."""
        if self.is_empty:
            raise EmptyTriageQueueError(
                "Cannot peek: the triage queue is empty"
            )
        return self._pq.peek()

    def list_queue(self) -> List[Patient]:
        """Return all waiting patients in attention order (most urgent first)."""
        # Patient.__lt__ treats more-urgent as "greater" for the max-heap.
        return sorted(self._pq.items(), reverse=True)

    def stats(self) -> Dict[int, int]:
        """Return counts of waiting patients per triage level (1–3)."""
        counts: Dict[int, int] = {1: 0, 2: 0, 3: 0}
        for patient in self._pq.items():
            counts[patient.triage_level] += 1
        return counts

    # --- aliases kept for earlier demos ---
    arrive = enqueue
    call_next = dequeue
    peek_next = peek

    def drain(self) -> List[Patient]:
        """Dequeue all patients in attention order."""
        seen: List[Patient] = []
        while not self.is_empty:
            seen.append(self.dequeue())
        return seen

    def add(
        self,
        name: str,
        triage_level: int,
        arrived_at: Optional[object] = None,
    ) -> Patient:
        """Convenience: build a ``Patient`` and enqueue them."""
        kwargs = {"name": name, "triage_level": triage_level}
        if arrived_at is not None:
            kwargs["arrived_at"] = arrived_at  # type: ignore[assignment]
        patient = Patient(**kwargs)  # type: ignore[arg-type]
        self.enqueue(patient)
        return patient
