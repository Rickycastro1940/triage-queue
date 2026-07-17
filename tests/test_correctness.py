"""Correctness and edge-case requirements (stdlib unittest)."""
from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import Patient, TriageQueue
from triage_queue import cli as triage_cli
from triage_queue.triage_queue import EmptyTriageQueueError


class CorrectnessTests(unittest.TestCase):
    def test_critical_patient_jumps_ahead_of_waiting_level_2_and_3(self):
        q = TriageQueue()
        t0 = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)
        q.enqueue(Patient(name="Waiter-L3", triage_level=3, arrived_at=t0))
        q.enqueue(
            Patient(name="Waiter-L2", triage_level=2, arrived_at=t0 + timedelta(minutes=1))
        )
        q.enqueue(
            Patient(
                name="Critical-L1",
                triage_level=1,
                arrived_at=t0 + timedelta(minutes=30),
            )
        )
        self.assertEqual(q.peek().name, "Critical-L1")
        self.assertEqual(
            [p.name for p in q.list_queue()],
            ["Critical-L1", "Waiter-L2", "Waiter-L3"],
        )
        self.assertEqual(q.dequeue().name, "Critical-L1")
        self.assertEqual(q.dequeue().name, "Waiter-L2")
        self.assertEqual(q.dequeue().name, "Waiter-L3")

    def test_same_triage_level_strict_arrival_fifo(self):
        q = TriageQueue()
        t0 = datetime(2026, 7, 17, 12, 0, tzinfo=timezone.utc)
        q.enqueue(
            Patient(name="Second", triage_level=2, arrived_at=t0 + timedelta(minutes=5))
        )
        q.enqueue(
            Patient(name="Third", triage_level=2, arrived_at=t0 + timedelta(minutes=10))
        )
        q.enqueue(Patient(name="First", triage_level=2, arrived_at=t0))
        self.assertEqual([p.name for p in q.list_queue()], ["First", "Second", "Third"])
        self.assertEqual(q.dequeue().name, "First")
        self.assertEqual(q.dequeue().name, "Second")
        self.assertEqual(q.dequeue().name, "Third")

    def test_empty_dequeue_and_peek_raise_without_crashing(self):
        q = TriageQueue()
        with self.assertRaises(EmptyTriageQueueError):
            q.dequeue()
        with self.assertRaises(EmptyTriageQueueError):
            q.peek()
        q.enqueue(Patient(name="Ada", triage_level=1))
        self.assertEqual(q.peek().name, "Ada")

    def test_cli_call_next_on_empty_queue_prints_message(self):
        q = TriageQueue()
        buf = StringIO()
        with patch("sys.stdout", buf):
            triage_cli._call_next(q)
        self.assertIn("empty", buf.getvalue().lower())
        self.assertEqual(len(q), 0)

    def test_cli_view_queue_on_empty_prints_message(self):
        q = TriageQueue()
        buf = StringIO()
        with patch("sys.stdout", buf):
            triage_cli._view_queue(q)
        self.assertIn("empty", buf.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
