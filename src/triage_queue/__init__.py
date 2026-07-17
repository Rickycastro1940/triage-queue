"""Package exports for Triage Queue — Priority Queue Manager."""

from .models import Patient
from .priority_queue import PriorityQueue
from .triage_queue import EmptyTriageQueueError, TriageQueue

__all__ = ["Patient", "TriageQueue", "PriorityQueue", "EmptyTriageQueueError"]
