"""AetherMind core cognitive package."""

from .brain import Brain
from .goals import GoalManager, Goal, Belief
from .reasoning import ReasoningLoop
from .safeguard import SelfModificationGuard, EmergencyShutdown
from .identity import Identity

__all__ = [
    "Brain",
    "GoalManager",
    "Goal",
    "Belief",
    "ReasoningLoop",
    "SelfModificationGuard",
    "EmergencyShutdown",
    "Identity",
]
