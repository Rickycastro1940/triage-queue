"""Small CLI demo for Triage Queue — Priority Queue Manager."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow `python -m triage_queue.cli` from repo root without install.
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from triage_queue import TriageQueueManager  # noqa: E402


def main() -> int:
    mgr = TriageQueueManager()
    samples = [
        ("Login button broken on mobile", 3),
        ("Production outage — payments down", 10),
        ("Typo in footer copyright year", 1),
        ("API latency spike in checkout", 8),
        ("Dark mode contrast issue", 2),
    ]
    print("Triage Queue — Priority Queue Manager\n")
    print("Submitting items:")
    for title, priority in samples:
        item = mgr.submit(title, priority=priority)
        print(f"  + [{item.priority:>2}] {item.title} ({item.id})")

    print("\nTreating in priority order:")
    while not mgr.is_empty:
        item = mgr.treat_next()
        print(f"  → treat [{item.priority:>2}] {item.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
