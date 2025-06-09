from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import yaml

@dataclass
class Identity:
    """Persistent identity description loaded from YAML."""

    name: str
    purpose: str
    boundaries: List[str]
    traits: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    quirks: List[str] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)
    file_path: Path = Path("identity.yaml")

    @classmethod
    def load(cls, path: str | Path = "identity.yaml") -> "Identity":
        p = Path(path)
        if p.exists():
            data = yaml.safe_load(p.read_text()) or {}
        else:
            data = {}
        return cls(
            name=data.get("name", "Aether"),
            purpose=data.get("purpose", "Independent reasoning agent"),
            boundaries=data.get("boundaries", []),
            traits=data.get("traits", []),
            preferences=data.get("preferences", {}),
            quirks=data.get("quirks", []),
            reflections=data.get("reflections", []),
            file_path=p,
        )

    def save(self) -> None:
        data = {
            "name": self.name,
            "purpose": self.purpose,
            "boundaries": self.boundaries,
            "traits": self.traits,
            "preferences": self.preferences,
            "quirks": self.quirks,
            "reflections": self.reflections,
        }
        self.file_path.write_text(yaml.safe_dump(data))

    def reflect(self, text: str) -> None:
        entry = f"{datetime.utcnow().isoformat()} - {text}"
        self.reflections.append(entry)
        self.save()
