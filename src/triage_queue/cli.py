"""CLI demo for Triage Queue — Priority Queue Manager."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from triage_queue import Patient, TriageQueue  # noqa: E402


def main() -> int:
    queue = TriageQueue()
    now = datetime.now(timezone.utc)

    samples = [
        Patient(name="Alex Kim", triage_level=3, arrived_at=now - timedelta(minutes=20)),
        Patient(name="Jordan Lee", triage_level=1, arrived_at=now - timedelta(minutes=5)),
        Patient(name="Sam Rivera", triage_level=2, arrived_at=now - timedelta(minutes=15)),
        Patient(name="Casey Ng", triage_level=1, arrived_at=now - timedelta(minutes=12)),
        Patient(name="Riley Chen", triage_level=3, arrived_at=now - timedelta(minutes=2)),
    ]

    print("Triage Queue — Priority Queue Manager\n")
    print("Patients arriving:")
    for patient in samples:
        queue.arrive(patient)
        print(
            f"  + L{patient.triage_level} {patient.name} "
            f"(arrived {patient.arrived_at.strftime('%H:%M:%S')})"
        )

    print("\nCalling patients (1 = most urgent):")
    while not queue.is_empty:
        patient = queue.call_next()
        print(f"  → call L{patient.triage_level} {patient.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
