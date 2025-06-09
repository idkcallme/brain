from typing import Any, Dict, Callable

class ProceduralMemory:
    """Stores task routines or skills."""

    def __init__(self):
        self._routines: Dict[str, Callable[..., Any]] = {}

    def add_routine(self, name: str, routine: Callable[..., Any]):
        self._routines[name] = routine

    def get_routine(self, name: str) -> Callable[..., Any]:
        return self._routines.get(name)

    def list_routines(self):
        return list(self._routines.keys())
