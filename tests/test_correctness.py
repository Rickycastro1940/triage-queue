"""Correctness and edge-case requirements for TriageQueue."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import Patient, TriageQueue
from triage_queue import cli as triage_cli
from triage_queue.triage_queue import EmptyTriageQueueError


def test_critical_patient_jumps_ahead_of_waiting_level_2_and_3():
    """A new level-1 arrival must be attended before waiting level-2/3 patients."""
    q = TriageQueue()
    t0 = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)

    q.enqueue(Patient(name="Waiter-L3", triage_level=3, arrived_at=t0))
    q.enqueue(Patient(name="Waiter-L2", triage_level=2, arrived_at=t0 + timedelta(minutes=1)))
    # Critical arrives later than both waiters.
    q.enqueue(
        Patient(name="Critical-L1", triage_level=1, arrived_at=t0 + timedelta(minutes=30))
    )

    assert q.peek().name == "Critical-L1"
    assert [p.name for p in q.list_queue()] == [
        "Critical-L1",
        "Waiter-L2",
        "Waiter-L3",
    ]
    assert q.dequeue().name == "Critical-L1"
    assert q.dequeue().name == "Waiter-L2"
    assert q.dequeue().name == "Waiter-L3"


def test_same_triage_level_strict_arrival_fifo():
    """Equal triage levels are attended in strict arrival order."""
    q = TriageQueue()
    t0 = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)

    # Enqueue out of arrival order on purpose.
    q.enqueue(Patient(name="Second", triage_level=2, arrived_at=t0 + timedelta(minutes=5)))
    q.enqueue(Patient(name="Third", triage_level=2, arrived_at=t0 + timedelta(minutes=10)))
    q.enqueue(Patient(name="First", triage_level=2, arrived_at=t0))

    assert [p.name for p in q.list_queue()] == ["First", "Second", "Third"]
    assert q.dequeue().name == "First"
    assert q.dequeue().name == "Second"
    assert q.dequeue().name == "Third"


def test_empty_dequeue_and_peek_raise_without_crashing():
    """Empty dequeue/peek must fail gracefully with a clear error (no crash)."""
    q = TriageQueue()
    with pytest.raises(EmptyTriageQueueError, match="empty"):
        q.dequeue()
    with pytest.raises(EmptyTriageQueueError, match="empty"):
        q.peek()
    # Queue remains usable after the empty operations.
    q.enqueue(Patient(name="Ada", triage_level=1))
    assert q.peek().name == "Ada"


def test_cli_call_next_on_empty_queue_prints_message(capsys):
    """CLI must not crash when calling next on an empty queue."""
    q = TriageQueue()
    triage_cli._call_next(q)
    out = capsys.readouterr().out
    assert "empty" in out.lower()
    assert len(q) == 0


def test_cli_view_queue_on_empty_prints_message(capsys):
    q = TriageQueue()
    triage_cli._view_queue(q)
    assert "empty" in capsys.readouterr().out.lower()
