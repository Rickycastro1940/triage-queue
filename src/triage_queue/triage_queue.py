"""TriageQueue — priority queue manager for patients."""
from __future__ import annotations

from typing import List, Optional

from .models import Patient
from .priority_queue import PriorityQueue


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

    def arrive(self, patient: Patient) -> None:
        """Enqueue a patient into the triage queue."""
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient instance")
        self._pq.enqueue(patient)

    def peek_next(self) -> Patient:
        """Return the next patient to see without removing them."""
        return self._pq.peek()

    def call_next(self) -> Patient:
        """Dequeue and return the highest-urgency patient."""
        return self._pq.dequeue()

    def drain(self) -> List[Patient]:
        """Call patients in priority order until the queue is empty."""
        seen: List[Patient] = []
        while not self.is_empty:
            seen.append(self.call_next())
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
        self.arrive(patient)
        return patient
