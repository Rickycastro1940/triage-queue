"""Tests for Patient and TriageQueue core operations."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import Patient, TriageQueue
from triage_queue.triage_queue import EmptyTriageQueueError


def test_patient_requires_fields():
    now = datetime.now(timezone.utc)
    p = Patient(name="Alex", triage_level=2, arrived_at=now)
    assert p.name == "Alex"
    assert p.triage_level == 2
    assert p.arrived_at == now


def test_triage_level_must_be_1_to_3():
    with pytest.raises(ValueError):
        Patient(name="Bad", triage_level=0)
    with pytest.raises(ValueError):
        Patient(name="Bad", triage_level=4)


def test_enqueue_dequeue_respects_triage_and_arrival():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    q.enqueue(Patient(name="Low", triage_level=3, arrived_at=now))
    q.enqueue(Patient(name="Critical", triage_level=1, arrived_at=now))
    q.enqueue(Patient(name="Medium", triage_level=2, arrived_at=now))

    assert q.dequeue().name == "Critical"
    assert q.dequeue().name == "Medium"
    assert q.dequeue().name == "Low"
    assert q.is_empty


def test_equal_level_uses_earlier_arrival():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    q.enqueue(Patient(name="Later", triage_level=1, arrived_at=now))
    q.enqueue(
        Patient(name="Earlier", triage_level=1, arrived_at=now - timedelta(minutes=10))
    )

    assert q.dequeue().name == "Earlier"
    assert q.dequeue().name == "Later"


def test_peek_does_not_remove():
    q = TriageQueue()
    q.enqueue(Patient(name="Only", triage_level=2))
    assert q.peek().name == "Only"
    assert len(q) == 1
    assert q.dequeue().name == "Only"


def test_dequeue_and_peek_empty_raise_meaningful_error():
    q = TriageQueue()
    with pytest.raises(EmptyTriageQueueError, match="empty"):
        q.dequeue()
    with pytest.raises(EmptyTriageQueueError, match="empty"):
        q.peek()


def test_list_queue_attention_order_without_mutating():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    q.enqueue(Patient(name="C", triage_level=3, arrived_at=now))
    q.enqueue(Patient(name="A", triage_level=1, arrived_at=now))
    q.enqueue(Patient(name="B", triage_level=2, arrived_at=now))

    names = [p.name for p in q.list_queue()]
    assert names == ["A", "B", "C"]
    assert len(q) == 3  # list_queue must not dequeue


def test_stats_counts_per_level():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    q.enqueue(Patient(name="A", triage_level=1, arrived_at=now))
    q.enqueue(Patient(name="B", triage_level=1, arrived_at=now))
    q.enqueue(Patient(name="C", triage_level=3, arrived_at=now))

    assert q.stats() == {1: 2, 2: 0, 3: 1}
