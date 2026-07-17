"""Stdlib unittest suite for Patient and TriageQueue."""
from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import Patient, TriageQueue
from triage_queue.triage_queue import EmptyTriageQueueError


class PatientModelTests(unittest.TestCase):
    def test_patient_requires_fields(self):
        now = datetime.now(timezone.utc)
        p = Patient(name="Alex", triage_level=2, arrived_at=now)
        self.assertEqual(p.name, "Alex")
        self.assertEqual(p.triage_level, 2)
        self.assertEqual(p.arrived_at, now)

    def test_triage_level_must_be_1_to_3(self):
        with self.assertRaises(ValueError):
            Patient(name="Bad", triage_level=0)
        with self.assertRaises(ValueError):
            Patient(name="Bad", triage_level=4)


class CoreOperationsTests(unittest.TestCase):
    def test_enqueue_dequeue_respects_triage_and_arrival(self):
        q = TriageQueue()
        now = datetime.now(timezone.utc)
        q.enqueue(Patient(name="Low", triage_level=3, arrived_at=now))
        q.enqueue(Patient(name="Critical", triage_level=1, arrived_at=now))
        q.enqueue(Patient(name="Medium", triage_level=2, arrived_at=now))
        self.assertEqual(q.dequeue().name, "Critical")
        self.assertEqual(q.dequeue().name, "Medium")
        self.assertEqual(q.dequeue().name, "Low")
        self.assertTrue(q.is_empty)

    def test_peek_does_not_remove(self):
        q = TriageQueue()
        q.enqueue(Patient(name="Only", triage_level=2))
        self.assertEqual(q.peek().name, "Only")
        self.assertEqual(len(q), 1)
        self.assertEqual(q.dequeue().name, "Only")

    def test_list_queue_attention_order_without_mutating(self):
        q = TriageQueue()
        now = datetime.now(timezone.utc)
        q.enqueue(Patient(name="C", triage_level=3, arrived_at=now))
        q.enqueue(Patient(name="A", triage_level=1, arrived_at=now))
        q.enqueue(Patient(name="B", triage_level=2, arrived_at=now))
        self.assertEqual([p.name for p in q.list_queue()], ["A", "B", "C"])
        self.assertEqual(len(q), 3)

    def test_stats_counts_per_level(self):
        q = TriageQueue()
        now = datetime.now(timezone.utc)
        q.enqueue(Patient(name="A", triage_level=1, arrived_at=now))
        q.enqueue(Patient(name="B", triage_level=1, arrived_at=now))
        q.enqueue(Patient(name="C", triage_level=3, arrived_at=now))
        self.assertEqual(q.stats(), {1: 2, 2: 0, 3: 1})

    def test_empty_dequeue_and_peek_raise(self):
        q = TriageQueue()
        with self.assertRaises(EmptyTriageQueueError):
            q.dequeue()
        with self.assertRaises(EmptyTriageQueueError):
            q.peek()


if __name__ == "__main__":
    unittest.main()
