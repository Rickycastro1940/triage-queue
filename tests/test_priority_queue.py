"""Tests for the max-heap priority queue and triage manager."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import PriorityQueue, TriageItem, TriageQueueManager


def test_dequeue_returns_highest_priority_first():
    pq: PriorityQueue[TriageItem] = PriorityQueue()
    pq.enqueue(TriageItem(priority=2, title="low"))
    pq.enqueue(TriageItem(priority=9, title="critical"))
    pq.enqueue(TriageItem(priority=5, title="medium"))

    assert pq.dequeue().title == "critical"
    assert pq.dequeue().title == "medium"
    assert pq.dequeue().title == "low"
    assert pq.is_empty


def test_manager_treat_next_order():
    mgr = TriageQueueManager()
    mgr.submit("typo", priority=1)
    mgr.submit("outage", priority=10)
    mgr.submit("bug", priority=4)

    assert mgr.next().title == "outage"
    assert mgr.treat_next().title == "outage"
    assert mgr.treat_next().title == "bug"
    assert mgr.treat_next().title == "typo"


def test_empty_dequeue_raises():
    pq: PriorityQueue[int] = PriorityQueue()
    with pytest.raises(IndexError):
        pq.dequeue()


def test_negative_priority_rejected():
    with pytest.raises(ValueError):
        TriageItem(priority=-1, title="bad")
