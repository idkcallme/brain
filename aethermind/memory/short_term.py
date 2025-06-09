from collections import deque
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ShortTermItem:
    data: Any
    weight: float = 1.0  # emotional or importance weighting

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

    def __len__(self):
        return len(self._cache)
