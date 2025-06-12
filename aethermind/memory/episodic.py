from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
import time

@dataclass
class Episode:
    timestamp: float
    data: Any
    weight: float = 1.0
    context: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

class EpisodicMemory:
    """Chronological log of events."""

    def __init__(self):
        self._events: List[Episode] = []

    def add(self, data: Any, weight: float = 1.0, context: Optional[Dict[str, Any]] = None, source: Optional[str] = None) -> Episode:
        ep = Episode(timestamp=time.time(), data=data, weight=weight, context=context, source=source)
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

    def summarize(self, n: int = 10):
        # Example: summarize the last n episodes (stub)
        if not self._events:
            return None
        recent = self._events[-n:]
        summary = f"Summary of last {len(recent)} episodes."
        return summary

    def __len__(self):
        return len(self._events)
