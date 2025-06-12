from typing import Any, Dict, Callable, Optional
import time

class ProceduralMemory:
    """Stores task routines or skills."""

    def __init__(self):
        self._routines: Dict[str, Callable[..., Any]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def add_routine(self, name: str, routine: Callable[..., Any], context: Optional[Dict[str, Any]] = None, source: Optional[str] = None):
        self._routines[name] = routine
        self._metadata[name] = {
            'timestamp': time.time(),
            'context': context,
            'source': source
        }

    def get_routine(self, name: str) -> Callable[..., Any]:
        return self._routines.get(name)

    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        return self._metadata.get(name)

    def list_routines(self):
        return list(self._routines.keys())

    def summarize(self, n: int = 10):
        # Example: summarize the last n routines (stub)
        if not self._routines:
            return None
        recent = list(self._routines.keys())[-n:]
        summary = f"Summary of last {len(recent)} routines."
        return summary
