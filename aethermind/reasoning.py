from __future__ import annotations
from typing import Any, Callable
from .brain import Brain
from .goals import GoalManager
from .safeguard import SelfModificationGuard, EmergencyShutdown

class ReasoningLoop:
    """Simple perceive-interpret-evaluate-act cycle."""

    def __init__(self, brain: Brain, goals: GoalManager,
                 guard: SelfModificationGuard | None = None,
                 shutdown: EmergencyShutdown | None = None):
        self.brain = brain
        self.goals = goals
        self.guard = guard or SelfModificationGuard()
        self.shutdown = shutdown or EmergencyShutdown()

    def perceive(self, data: Any) -> None:
        """Store raw input in working memory."""
        self.brain.remember(data)

    def interpret(self, data: Any) -> Any:
        """Placeholder for semantic interpretation."""
        return data

    def evaluate(self, interpreted: Any) -> str:
        """Evaluate the input in light of goals and safety."""
        self.shutdown.check_phrase(str(interpreted))
        goal = self.goals.next_goal()
        if goal:
            return f"Goal: {goal.description}"
        return "No goal"

    def decide(self, evaluation: str) -> Callable[[], Any] | None:
        if "ask" in evaluation.lower():
            return lambda: "ask"
        return None

    def act(self, action: Callable[[], Any] | None) -> Any:
        if action:
            return action()
        return None

    def cycle(self, data: Any) -> Any:
        """Run one reasoning iteration."""
        self.perceive(data)
        interpreted = self.interpret(data)
        evaluation = self.evaluate(interpreted)
        decision = self.decide(evaluation)
        return self.act(decision)

