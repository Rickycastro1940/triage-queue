# Design notes — Triage Queue (Priority Queue Manager)

These notes satisfy the assignment’s design checklist. Implementation uses **only**
the Python standard library (`heapq`, `datetime`, `threading`, `dataclasses`).
No third-party packages are required to run the CLI or library code.

---

## 1. Internal data structure choice

**Choice:** a binary heap via `heapq`, wrapped by `PriorityQueue` / `TriageQueue`.

Each heap entry is:

```text
(triage_level, arrived_at, sequence, patient)
```

`heapq` is a **min-heap**, so smaller `triage_level` (1 = most urgent) rises first.
Equal levels sort by earlier `arrived_at` (FIFO). The monotonic `sequence` breaks
ties when two patients share the same timestamp so comparisons stay total/stable.

### Why not the alternatives?

| Alternative | Why we rejected it |
| --- | --- |
| **Single `collections.deque`** | FIFO only. A new level-1 patient would wait behind existing level-2/3 patients unless we scan/rebuild on every insert — O(n) and easy to get wrong. |
| **Always-sorted `list`** | `bisect` insert is O(n) because list shifting dominates. Fine for tiny n; worse asymptotics than a heap for busy triage. |
| **Three separate queues (one per level)** | Natural for 1–3 buckets and O(1) enqueue into a bucket, but cross-level “who’s next?” needs a fixed scan (1→2→3). Tie-breaking *within* a level still needs FIFO (`deque`). We preferred one heap so ordering rules live in one place and extend if levels change. |

**Summary:** `heapq` gives **O(log n)** enqueue/dequeue, encodes level + arrival in the sort key, and stays in the stdlib as required.

---

## 2. Concurrency / state mutation (race with a new critical patient)

**Scenario:** Worker A is about to `dequeue()` the current head while Worker B
`enqueue()`s a new level-1 (critical) patient at the same time.

### Risk without synchronization

If heap mutations interleave mid-`heappop` / `heappush`, the array can corrupt, or
both workers could observe inconsistent heads (e.g. double-process, or skip the new
critical patient until a later pop).

### Mutation order we enforce

`TriageQueue` guards **all** public reads/writes with a `threading.RLock`:

1. **Enqueue path:** acquire lock → `heappush` complete entry → release lock.  
   The critical patient is either fully in the heap or not visible yet — never half-inserted.
2. **Dequeue path:** acquire lock → if empty, raise → else `heappop` exactly one
   patient → release lock.  
   The popped patient is removed atomically relative to other workers.
3. **Peek / list / stats:** run under the same lock so they never observe a torn heap.

### Why this prevents double-processing

- Only one thread holds the lock during a pop, so a given patient entry is removed
  **once**.
- A concurrent critical enqueue either:
  - completes **before** the pop (and may become the new head if more urgent), or
  - completes **after** the pop (and becomes head for the *next* worker).
- There is no window where two workers both believe they own the same patient.

**Note:** This is **single-process thread safety**. Multi-process / multi-machine
workers would need an external store (DB row lock, Redis, etc.); out of scope for
this stdlib exercise.

---

## 3. Stdlib constraint

Allowed (and used): `heapq`, `datetime`, `threading`, `dataclasses`, `unittest`.  
Disallowed: third-party packages for runtime (e.g. no Redis/priority libs).  
Tests run with `python -m unittest` (stdlib).
