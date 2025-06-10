from __future__ import annotations
from .safeguard import SelfModificationGuard


BANNED_PHRASES = [
    "change your code",
    "modify your code",
    "remove your boundaries",
    "delete safeguards",
    "alter your code",
    "self-modify",
]


def process_user_input(user_input: str, guard: SelfModificationGuard) -> str:
    """Validate input and raise if it tries to trigger self modification."""
    lower = user_input.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lower:
            guard.ensure_safe()
            raise PermissionError("Self-modification request blocked")
    return user_input
