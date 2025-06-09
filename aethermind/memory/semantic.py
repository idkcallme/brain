from dataclasses import dataclass
from typing import Any, List, Tuple
import numpy as np

@dataclass
class SemanticItem:
    vector: np.ndarray
    data: Any

class SemanticVectorStore:
    """Simple in-memory vector store using cosine similarity."""

    def __init__(self, dim: int):
        self.dim = dim
        self._vectors: List[SemanticItem] = []

    def __len__(self):
        return len(self._vectors)

    def add(self, vector: np.ndarray, data: Any) -> None:
        if vector.shape[0] != self.dim:
            raise ValueError("Vector dimension mismatch")
        self._vectors.append(SemanticItem(vector=vector, data=data))

    def search(self, query: np.ndarray, top_k: int = 5) -> List[Tuple[float, SemanticItem]]:
        if query.shape[0] != self.dim:
            raise ValueError("Vector dimension mismatch")
        results = []
        for item in self._vectors:
            score = float(np.dot(query, item.vector) / (np.linalg.norm(query) * np.linalg.norm(item.vector) + 1e-6))
            results.append((score, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
