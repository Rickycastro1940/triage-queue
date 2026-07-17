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
Manages priority-queue logic internally (max-heap). Core operations:

| Method | Description |
| --- | --- |
| `enqueue(patient)` | Add a patient (respects level + arrival order) |
| `dequeue()` | Remove/return next patient; raises if empty |
| `peek()` | Next patient without removing; raises if empty |
| `list_queue()` | All waiting patients in attention order |
| `stats()` | `{1: n, 2: n, 3: n}` waiting counts per level |

Equal triage levels break ties by **earlier** `arrived_at`.

## Correctness and edge cases

- A new **level-1** patient jumps ahead of waiting level-2/3 patients.
- Same triage level → **strict FIFO** by `arrived_at`.
- `dequeue()` / `peek()` on an empty queue raise `EmptyTriageQueueError` (CLI prints the message and continues).

## Quick start

```bash
cd triage-queue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Interactive menu: add / call next / view queue / stats / exit
PYTHONPATH=src python -m triage_queue.cli

PYTHONPATH=src pytest -q
```

### CLI menu
1. Add a new patient (name + triage level)
2. Call the next patient
3. View the current queue
4. See queue stats
5. Exit

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
