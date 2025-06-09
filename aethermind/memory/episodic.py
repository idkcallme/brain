from dataclasses import dataclass, field
from typing import Any, List
import time

@dataclass
class Episode:
    timestamp: float
    data: Any
    weight: float = 1.0

class EpisodicMemory:
    """Chronological log of events."""

    def __init__(self):
        self._events: List[Episode] = []

    def add(self, data: Any, weight: float = 1.0) -> Episode:
        ep = Episode(timestamp=time.time(), data=data, weight=weight)
        self._events.append(ep)
        return ep

    def search(self, keyword: str, n: int = 5) -> List[Episode]:
        """Return episodes containing the keyword, ordered from newest."""
        matches = [e for e in reversed(self._events) if keyword.lower() in str(e.data).lower()]
        return matches[:n]

    def get_recent(self, n: int = 10) -> List[Episode]:
        return self._events[-n:]

    def all_events(self) -> List[Episode]:
        return list(self._events)

    def __len__(self):
        return len(self._events)
