import random
from typing import Any, Optional, Dict
from .short_term import ShortTermCache, ShortTermItem
from .episodic import EpisodicMemory
from .semantic import SemanticVectorStore
from .procedural import ProceduralMemory
from .archival import ArchivalMemory
from .logging_util import logger
from .feedback import FeedbackProcessor
import numpy as np

class MemoryController:
    """Controls routing across memory tiers using a simple RL policy."""

    def __init__(self, semantic_dim: int = 32):
        self.short_term = ShortTermCache()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticVectorStore(dim=semantic_dim)
        self.procedural = ProceduralMemory()
        self.archival = ArchivalMemory()
        self.feedback = FeedbackProcessor(self)
        self.q_table = {}
        self.actions = ['short_term', 'episodic', 'semantic', 'procedural', 'archival']
        self.short_term_threshold = 10
        self.episodic_threshold = 100

    def _choose_action(self, state: str) -> str:
        """Epsilon-greedy policy."""
        epsilon = 0.1
        if random.random() < epsilon or state not in self.q_table:
            return random.choice(self.actions)
        return max(self.q_table[state], key=self.q_table[state].get)

    def _update_q(self, state: str, action: str, reward: float, lr=0.1, gamma=0.95):
        self.q_table.setdefault(state, {a: 0.0 for a in self.actions})
        current = self.q_table[state][action]
        self.q_table[state][action] = current + lr * (reward + gamma * max(self.q_table[state].values()) - current)

    def store(self, data: Any, vector: np.ndarray = None, weight: float = 1.0, context: Optional[Dict[str, Any]] = None, source: Optional[str] = None):
        state = 'store'
        action = self._choose_action(state)
        logger.info(f"Storing data via {action}")
        if action == 'short_term':
            self.short_term.add(ShortTermItem(data=data, weight=weight, context=context, source=source))
        elif action == 'episodic':
            self.episodic.add(data=data, weight=weight, context=context, source=source)
        elif action == 'semantic' and vector is not None:
            self.semantic.add(vector=vector, data=data, context=context, source=source)
        elif action == 'procedural' and callable(data):
            self.procedural.add_routine(getattr(data, '__name__', 'routine'), data, context=context, source=source)
        elif action == 'archival':
            self.archival.append(data, context=context, source=source)
        self._update_q(state, action, reward=1.0)
        self.consolidate()

    def recall(self, query: Any = None, vector: np.ndarray = None):
        state = 'recall'
        action = self._choose_action(state)
        logger.info(f"Recalling data via {action}")
        result = None
        if action == 'short_term':
            result = self.short_term.get_all()
        elif action == 'episodic':
            if isinstance(query, str):
                result = self.episodic.search(query)
            else:
                result = self.episodic.get_recent()
        elif action == 'semantic' and vector is not None:
            result = self.semantic.search(vector)
        elif action == 'procedural' and isinstance(query, str):
            result = self.procedural.get_routine(query)
        elif action == 'archival':
            result = self.archival.load()
        self._update_q(state, action, reward=1.0 if result else 0.0)
        return result

    def consolidate(self):
        """Move memories between tiers based on thresholds."""
        logger.info("Consolidation step")
        # move oldest short-term item to episodic if cache is full
        if len(self.short_term) >= self.short_term_threshold:
            oldest = self.short_term.pop_oldest()
            if oldest:
                self.episodic.add(data=oldest.data, weight=oldest.weight, context=oldest.context, source=oldest.source)

        # archive oldest episodic events when episodic memory grows large
        while len(self.episodic) > self.episodic_threshold:
            oldest_episode = self.episodic._events.pop(0)
            self.archival.append(
                oldest_episode.data,
                context=oldest_episode.context,
                source=oldest_episode.source
            )

    def summarize_all(self):
        return {
            'short_term': self.short_term.summarize(),
            'episodic': self.episodic.summarize(),
            'semantic': self.semantic.summarize(),
            'procedural': self.procedural.summarize(),
            'archival': self.archival.summarize(),
        }

    # Hooks for future federated or local storage options
    def export_memory(self) -> dict:
        return {
            'short_term': self.short_term.get_all(),
            'episodic': self.episodic.all_events(),
            'semantic_count': len(self.semantic),
            'procedural_routines': self.procedural.list_routines(),
            'q_table': self.q_table,
        }

    def clear_short_term(self):
        self.short_term.clear()
