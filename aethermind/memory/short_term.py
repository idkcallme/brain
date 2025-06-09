from collections import deque
from dataclasses import dataclass
from typing import Any

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
        self._cache.append(item)

    def get_all(self):
        return list(self._cache)

    def clear(self):
        self._cache.clear()
