# Triage Queue — Priority Queue Manager

A priority-queue manager for ER-style triage: **level 1** patients are called before **level 2–3**.

## Data model

### `Patient`
| Field | Type | Notes |
| --- | --- | --- |
| `name` | `str` | Required |
| `triage_level` | `int` | **1–3** (1 = most urgent, 3 = least) |
| `arrived_at` | `datetime` | Arrival timestamp (UTC default) |

### `TriageQueue`
Manages priority-queue logic internally (max-heap). Public operations:

| Method | Description |
| --- | --- |
| `arrive(patient)` | Enqueue a `Patient` |
| `peek_next()` | Look at next patient |
| `call_next()` | Dequeue highest-urgency patient |
| `add(name, triage_level, …)` | Convenience constructor + enqueue |

Equal triage levels break ties by **earlier** `arrived_at`.

## Quick start

```bash
cd triage-queue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=src python -m triage_queue.cli
PYTHONPATH=src pytest -q
```

## Layout

```text
src/triage_queue/
  models.py           # Patient
  triage_queue.py     # TriageQueue
  priority_queue.py   # Internal max-heap
  cli.py
tests/
```

## License

MIT
