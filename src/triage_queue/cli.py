"""Interactive CLI menu for Triage Queue — Priority Queue Manager."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from triage_queue import Patient, TriageQueue  # noqa: E402
from triage_queue.triage_queue import EmptyTriageQueueError  # noqa: E402

MENU = """
===============================
 Triage Queue — Priority Queue
===============================
  1) Add a new patient
  2) Call the next patient
  3) View the current queue
  4) See queue stats
  5) Exit
===============================
"""


def _prompt_choice() -> str:
    return input("Choose an option [1-5]: ").strip()


def _add_patient(queue: TriageQueue) -> None:
    name = input("Patient name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    raw_level = input("Triage level (1=most urgent … 3=least): ").strip()
    try:
        level = int(raw_level)
        patient = Patient(name=name, triage_level=level)
    except ValueError as exc:
        print(f"Could not add patient: {exc}")
        return
    queue.enqueue(patient)
    print(
        f"Enqueued L{patient.triage_level} {patient.name} "
        f"(arrived {patient.arrived_at.strftime('%Y-%m-%d %H:%M:%S %Z')})"
    )


def _call_next(queue: TriageQueue) -> None:
    try:
        patient = queue.dequeue()
    except EmptyTriageQueueError as exc:
        print(exc)
        return
    print(f"Calling next: L{patient.triage_level} {patient.name}")


def _view_queue(queue: TriageQueue) -> None:
    waiting = queue.list_queue()
    if not waiting:
        print("Queue is empty.")
        return
    print(f"Waiting ({len(waiting)}) in attention order:")
    for i, patient in enumerate(waiting, start=1):
        print(
            f"  {i}. L{patient.triage_level} {patient.name} "
            f"(arrived {patient.arrived_at.strftime('%H:%M:%S')})"
        )


def _view_stats(queue: TriageQueue) -> None:
    stats = queue.stats()
    total = sum(stats.values())
    print(f"Waiting patients: {total}")
    for level in (1, 2, 3):
        print(f"  Level {level}: {stats[level]}")


def main() -> int:
    queue = TriageQueue()
    print("Triage Queue — Priority Queue Manager")
    print("Type menu numbers to interact. Ctrl+C also exits.\n")

    while True:
        print(MENU)
        try:
            choice = _prompt_choice()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return 0

        if choice == "1":
            _add_patient(queue)
        elif choice == "2":
            _call_next(queue)
        elif choice == "3":
            _view_queue(queue)
        elif choice == "4":
            _view_stats(queue)
        elif choice == "5":
            print("Goodbye.")
            return 0
        else:
            print("Invalid option. Enter 1–5.")


if __name__ == "__main__":
    raise SystemExit(main())
