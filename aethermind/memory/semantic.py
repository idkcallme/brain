from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List, Tuple
import numpy as np
import time

@dataclass
class SemanticItem:
    vector: np.ndarray
    data: Any
    timestamp: float = field(default_factory=lambda: time.time())
    context: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

class SemanticVectorStore:
    """Simple in-memory vector store using cosine similarity."""

    def __init__(self, dim: int):
        self.dim = dim
        self._vectors: List[SemanticItem] = []

    def __len__(self):
        return len(self._vectors)

    def add(self, vector: np.ndarray, data: Any, context: Optional[Dict[str, Any]] = None, source: Optional[str] = None) -> None:
        if vector.shape[0] != self.dim:
            raise ValueError("Vector dimension mismatch")
        self._vectors.append(SemanticItem(vector=vector, data=data, context=context, source=source))

    def search(self, query: np.ndarray, top_k: int = 5) -> List[Tuple[float, SemanticItem]]:
        if query.shape[0] != self.dim:
            raise ValueError("Vector dimension mismatch")
        results = []
        for item in self._vectors:
            score = float(np.dot(query, item.vector) / (np.linalg.norm(query) * np.linalg.norm(item.vector) + 1e-6))
            results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

    def summarize(self, n: int = 10):
        # Example: summarize the last n semantic items (stub)
        if not self._vectors:
            return None
        recent = self._vectors[-n:]
        summary = f"Summary of last {len(recent)} semantic items."
        return summary
