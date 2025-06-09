import pickle
import gzip
from typing import Any, Dict
from pathlib import Path

class ArchivalMemory:
    """Long-term compressed storage."""

    def __init__(self, path: str = "archive.pkl.gz"):
        self.path = Path(path)
        if not self.path.exists():
            with gzip.open(self.path, 'wb') as f:
                pickle.dump([], f)

    def load(self) -> Dict:
        with gzip.open(self.path, 'rb') as f:
            return pickle.load(f)

    def save(self, data: Dict) -> None:
        with gzip.open(self.path, 'wb') as f:
            pickle.dump(data, f)

    def append(self, item: Any) -> None:
        """Append a single item to the archive."""
        data = self.load()
        data.append(item)
        self.save(data)
