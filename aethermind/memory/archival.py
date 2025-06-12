import pickle
import gzip
from typing import Any, Dict, List, Optional
from pathlib import Path
import time

class ArchivalMemory:
    """Long-term compressed storage."""

    def __init__(self, path: str = "archive.pkl.gz"):
        self.path = Path(path)
        if not self.path.exists():
            with gzip.open(self.path, 'wb') as f:
                pickle.dump([], f)

    def load(self) -> List[Dict]:
        with gzip.open(self.path, 'rb') as f:
            return pickle.load(f)

    def save(self, data: List[Dict]) -> None:
        with gzip.open(self.path, 'wb') as f:
            pickle.dump(data, f)

    def append(self, item: Any, context: Optional[Dict[str, Any]] = None, source: Optional[str] = None) -> None:
        """Append a single item to the archive with metadata."""
        data = self.load()
        entry = {
            'timestamp': time.time(),
            'data': item,
            'context': context,
            'source': source
        }
        data.append(entry)
        self.save(data)

    def summarize(self, n: int = 10):
        # Example: summarize the last n archival items (stub)
        data = self.load()
        if not data:
            return None
        recent = data[-n:]
        summary = f"Summary of last {len(recent)} archival items."
        return summary
