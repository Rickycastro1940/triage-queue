# Triage Queue — Priority Queue Manager

A priority-queue manager for triage workflows: highest-severity items are dequeued first.

## Goals

- Implement a **max-heap priority queue** (array-backed binary heap)
- Manage triage items with a severity / priority score
- Support enqueue, peek, dequeue (treat next), and size/empty checks
- Keep the schedule and API simple enough for demos and unit tests

## Quick start

```bash
cd triage-queue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Demo
python -m triage_queue.cli

# Tests
pytest -q
```

## Core API

| Method | Description |
| --- | --- |
| `enqueue(item)` | Insert a triage item; heap-order by priority (max first) |
| `peek()` | Look at the highest-priority item without removing it |
| `dequeue()` | Remove and return the highest-priority item |
| `size` / `is_empty` | Queue length helpers |

## Project layout

```text
triage-queue/
├── src/triage_queue/
│   ├── models.py          # TriageItem
│   ├── priority_queue.py  # Max-heap priority queue
│   ├── manager.py         # TriageQueueManager façade
│   └── cli.py             # Small interactive demo
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## License

MIT
