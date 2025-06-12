from collections import deque
from dataclasses import dataclass, field
from typing import Any, Optional, Dict
import time

@dataclass
class ShortTermItem:
    data: Any
    weight: float = 1.0  # emotional or importance weighting
    timestamp: float = field(default_factory=lambda: time.time())
    context: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

class ShortTermCache:
    """In-memory short-term cache simulating working memory."""

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._cache = deque(maxlen=capacity)

    def add(self, item: ShortTermItem) -> None:
        """Add an item to the short-term cache."""
        self._cache.append(item)

    def pop_oldest(self) -> Optional[ShortTermItem]:
        """Remove and return the oldest item if the cache is full."""
        if len(self._cache) == self.capacity:
            return self._cache.popleft()
        return None

    def get_all(self):
        """Return all cached items in order from oldest to newest."""
        return list(self._cache)

    def clear(self):
        """Remove all items from the cache."""
        self._cache.clear()

    def summarize(self):
        """Summarize cached items (stub for future implementation)."""
        if not self._cache:
            return None
        summary = f"Summary of {len(self._cache)} items."
        return summary

    def __len__(self):
        return len(self._cache)
