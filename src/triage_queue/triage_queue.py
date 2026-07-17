"""TriageQueue — priority queue manager for patients.

Uses only the Python standard library (``heapq``, ``datetime``, ``threading``).
See DESIGN.md for structure choice and concurrency notes.
"""
from __future__ import annotations

import threading
from typing import Dict, List, Optional

from .models import Patient
from .priority_queue import PriorityQueue


class EmptyTriageQueueError(LookupError):
    """Raised when peek/dequeue is attempted on an empty triage queue."""


class TriageQueue:
    """Manages waiting patients with an internal ``heapq``-backed priority queue.

    Patients are ordered by ``triage_level`` (1 = most urgent … 3 = least urgent),
    then by earlier ``arrived_at`` when levels match.

    All public mutating operations take ``self._lock`` so a concurrent enqueue of a
    critical patient cannot interleave mid-dequeue (see DESIGN.md).
    """

    def __init__(self) -> None:
        self._pq = PriorityQueue()
        self._lock = threading.RLock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._pq)

    def __bool__(self) -> bool:
        with self._lock:
            return not self._pq.is_empty

    @property
    def is_empty(self) -> bool:
        with self._lock:
            return self._pq.is_empty

    def enqueue(self, patient: Patient) -> None:
        """Add a patient; position respects triage level and arrival order."""
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient instance")
        with self._lock:
            self._pq.enqueue(patient)

    def dequeue(self) -> Patient:
        """Remove and return the next patient to be attended."""
        with self._lock:
            if self._pq.is_empty:
                raise EmptyTriageQueueError(
                    "Cannot dequeue: the triage queue is empty"
                )
            return self._pq.dequeue()

    def peek(self) -> Patient:
        """Return the next patient without removing them."""
        with self._lock:
            if self._pq.is_empty:
                raise EmptyTriageQueueError(
                    "Cannot peek: the triage queue is empty"
                )
            return self._pq.peek()

    def list_queue(self) -> List[Patient]:
        """Return all waiting patients in attention order (most urgent first)."""
        with self._lock:
            return sorted(
                self._pq.items(),
                key=lambda p: (p.triage_level, p.arrived_at),
            )

    def stats(self) -> Dict[int, int]:
        """Return counts of waiting patients per triage level (1–3)."""
        with self._lock:
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
        while True:
            with self._lock:
                if self._pq.is_empty:
                    break
                seen.append(self._pq.dequeue())
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
