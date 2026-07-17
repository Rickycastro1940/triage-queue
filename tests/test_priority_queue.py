"""Tests for Patient and TriageQueue data model."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import Patient, TriageQueue


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


def test_triage_queue_calls_most_urgent_first():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    q.arrive(Patient(name="Low", triage_level=3, arrived_at=now))
    q.arrive(Patient(name="Critical", triage_level=1, arrived_at=now))
    q.arrive(Patient(name="Medium", triage_level=2, arrived_at=now))

    assert q.call_next().name == "Critical"
    assert q.call_next().name == "Medium"
    assert q.call_next().name == "Low"
    assert q.is_empty


def test_equal_level_uses_earlier_arrival():
    q = TriageQueue()
    now = datetime.now(timezone.utc)
    later = Patient(name="Later", triage_level=1, arrived_at=now)
    earlier = Patient(name="Earlier", triage_level=1, arrived_at=now - timedelta(minutes=10))
    q.arrive(later)
    q.arrive(earlier)

    assert q.call_next().name == "Earlier"
    assert q.call_next().name == "Later"


def test_empty_call_next_raises():
    q = TriageQueue()
    with pytest.raises(IndexError):
        q.call_next()
