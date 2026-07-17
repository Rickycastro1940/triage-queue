"""Smoke tests for the interactive CLI menu helpers (stdlib unittest)."""
from __future__ import annotations

import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import TriageQueue
from triage_queue import cli as triage_cli


class CliMenuTests(unittest.TestCase):
    def test_menu_add_call_view_stats_exit(self):
        queue = TriageQueue()
        inputs = iter(["Ada Lovelace", "1", "Grace Hopper", "3"])
        with patch("builtins.input", side_effect=lambda *_a, **_k: next(inputs)):
            triage_cli._add_patient(queue)
            triage_cli._add_patient(queue)

        buf = StringIO()
        with patch("sys.stdout", buf):
            triage_cli._view_queue(queue)
            triage_cli._view_stats(queue)
            triage_cli._call_next(queue)
        out = buf.getvalue()
        self.assertIn("Ada Lovelace", out)
        self.assertIn("Grace Hopper", out)
        self.assertIn("Calling next: L1 Ada Lovelace", out)
        self.assertEqual(len(queue), 1)

    def test_main_exits_on_option_5(self):
        with patch("builtins.input", side_effect=["5"]):
            self.assertEqual(triage_cli.main(), 0)


if __name__ == "__main__":
    unittest.main()
