from dataclasses import dataclass
from typing import List


@dataclass
class Belief:
    """Simple belief representation used by the planner."""
    statement: str
    truth: bool = True

@dataclass
class Goal:
    """Represents a high-level desire or objective."""
    description: str
    priority: int = 0
    satisfied: bool = False

class GoalManager:
    """Manages goals, beliefs, and intentions using a BDI-style approach."""

    def __init__(self):
        self.goals: List[Goal] = []
        self.beliefs: List[Belief] = []

    def add_goal(self, description: str, priority: int = 0) -> Goal:
        goal = Goal(description=description, priority=priority)
        self.goals.append(goal)
        # keep goals ordered by priority (highest first)
        self.goals.sort(key=lambda g: g.priority, reverse=True)
        return goal

    def update_belief(self, statement: str, truth: bool = True) -> Belief:
        belief = Belief(statement=statement, truth=truth)
        self.beliefs.append(belief)
        return belief

    def drop_goal(self, description: str) -> None:
        self.goals = [g for g in self.goals if g.description != description]

    def complete_goal(self, description: str) -> None:
        for g in self.goals:
            if g.description == description:
                g.satisfied = True
                break

    def next_goal(self) -> Goal | None:
        for g in self.goals:
            if not g.satisfied:
                return g
        return None

    def active_goals(self) -> List[Goal]:
        return [g for g in self.goals if not g.satisfied]

    def list_goals(self) -> List[Goal]:
        """Return a copy of all goals, regardless of state."""
        return list(self.goals)

