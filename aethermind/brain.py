"""High-level Brain interface exposing memory operations."""
from typing import Any
import numpy as np
from .memory import MemoryController

class Brain:
    """Represents the core memory module of AetherMind."""

    def __init__(self, semantic_dim: int = 32):
        self.controller = MemoryController(semantic_dim=semantic_dim)

    def remember(self, data: Any, vector: np.ndarray = None, weight: float = 1.0):
        self.controller.store(data=data, vector=vector, weight=weight)

    def recall(self, query: Any = None, vector: np.ndarray = None):
        return self.controller.recall(query=query, vector=vector)

    def feedback(self, feedback: dict):
        self.controller.feedback.process(feedback)

    def export_memory(self) -> dict:
        return self.controller.export_memory()

    def consolidate(self):
        self.controller.consolidate()

    def clear_short_term(self):
        self.controller.clear_short_term()
