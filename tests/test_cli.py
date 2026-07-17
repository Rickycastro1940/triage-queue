"""Smoke tests for the interactive CLI menu helpers."""
from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from triage_queue import TriageQueue
from triage_queue import cli as triage_cli


def test_menu_add_call_view_stats_exit(capsys):
    queue = TriageQueue()
    inputs = iter(
        [
            "Ada Lovelace",
            "1",
            "Grace Hopper",
            "3",
        ]
    )
    with patch("builtins.input", side_effect=lambda *_a, **_k: next(inputs)):
        triage_cli._add_patient(queue)
        triage_cli._add_patient(queue)

    triage_cli._view_queue(queue)
    triage_cli._view_stats(queue)
    triage_cli._call_next(queue)

    out = capsys.readouterr().out
    assert "Ada Lovelace" in out
    assert "Grace Hopper" in out
    assert "Level 1: 1" in out or "L1 Ada Lovelace" in out
    assert "Calling next: L1 Ada Lovelace" in out
    assert len(queue) == 1


def test_main_exits_on_option_5():
    with patch("builtins.input", side_effect=["5"]):
        assert triage_cli.main() == 0
