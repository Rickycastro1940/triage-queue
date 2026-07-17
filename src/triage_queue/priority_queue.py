"""Array-backed max-heap priority queue (1-based indexing)."""
from __future__ import annotations

from typing import Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """Max-oriented binary heap.

    Index 0 is unused so parent/child math stays simple:
    - parent(i) = i // 2
    - left(i) = 2 * i
    - right(i) = 2 * i + 1
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._heap: List[Optional[T]] = [None]
        if items:
            for item in items:
                self.enqueue(item)

    def __len__(self) -> int:
        return len(self._heap) - 1

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def enqueue(self, item: T) -> None:
        self._heap.append(item)
        self._swim(len(self))

    def peek(self) -> T:
        if self.is_empty:
            raise IndexError("peek from empty priority queue")
        return self._heap[1]  # type: ignore[return-value]

    def dequeue(self) -> T:
        if self.is_empty:
            raise IndexError("dequeue from empty priority queue")
        top = self._heap[1]
        last = self._heap.pop()
        if not self.is_empty:
            self._heap[1] = last
            self._sink(1)
        return top  # type: ignore[return-value]

    def items(self) -> List[T]:
        """Return a shallow copy of heap items (unordered)."""
        return [item for item in self._heap[1:] if item is not None]

    def _swim(self, i: int) -> None:
        while i > 1:
            parent = i // 2
            if not self._less(parent, i):
                break
            self._exch(parent, i)
            i = parent

    def _sink(self, i: int) -> None:
        n = len(self)
        while 2 * i <= n:
            j = 2 * i
            if j < n and self._less(j, j + 1):
                j += 1
            if not self._less(i, j):
                break
            self._exch(i, j)
            i = j

    def _less(self, i: int, j: int) -> bool:
        """True if heap[i] has lower urgency than heap[j] (max-heap)."""
        a = self._heap[i]
        b = self._heap[j]
        return a < b  # type: ignore[operator]

    def _exch(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
