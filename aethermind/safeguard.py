class SelfModificationGuard:
    """Prevents the agent from altering its own code base."""

    allowed: bool = False

    def ensure_safe(self) -> None:
        if not self.allowed:
            # In real deployment this would check file system permissions.
            raise PermissionError("Self-modification is disallowed")


class EmergencyShutdown:
    """Triggers a safe exit when the special kill phrase is spoken."""

    PHRASE = "pen pinapple apple pen"

    def __init__(self) -> None:
        self.armed = True

    def disarm(self) -> None:
        self.armed = False

    def arm(self) -> None:
        self.armed = True

    def check_phrase(self, speech: str) -> None:
        if self.armed and self.PHRASE in speech.lower():
            raise SystemExit("Emergency shutdown command received")

