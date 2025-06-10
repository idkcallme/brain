"""AetherMind core cognitive package."""

from .brain import Brain
from .goals import GoalManager, Goal, Belief
from .reasoning import ReasoningLoop
from .safeguard import SelfModificationGuard, EmergencyShutdown
from .input_handler import process_user_input
from .identity import Identity
from .llm import chat

__all__ = [
    "Brain",
    "GoalManager",
    "Goal",
    "Belief",
    "ReasoningLoop",
    "SelfModificationGuard",
    "EmergencyShutdown",
    "Identity",
    "chat",
    "process_user_input",
]
