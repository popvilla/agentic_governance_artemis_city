"""Instruction loading and caching utilities.

These helpers provide lightweight instruction discovery from Markdown files and an
in-memory cache to avoid repeatedly reading the same content during test runs or
agent setup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class InstructionScope:
    """Represents a unit of instruction content."""

    level: str
    path: str
    content: str
    priority: int = 0


@dataclass
class InstructionSet:
    """Collection of instruction scopes."""

    scopes: List[InstructionScope] = field(default_factory=list)

    def add_scope(self, scope: InstructionScope) -> None:
        """Append a scope to the set."""
        self.scopes.append(scope)


class InstructionLoader:
    """Loads instruction files for a given agent."""

    def __init__(self) -> None:
        self.default_levels = ("agent", "global")

    def load(self, current_dir: str, agent_name: Optional[str] = None) -> InstructionSet:
        """Load instructions for the given agent name.

        Returns an InstructionSet even if no files are found so callers can rely on
        a stable return type.
        """
        base_dir = Path(current_dir)
        instruction_set = InstructionSet()
        candidates: List[Path] = []

        if agent_name:
            candidates.append(base_dir / "src" / "agents" / f"{agent_name}.md")
            candidates.append(base_dir / "agents" / f"{agent_name}.md")

        candidates.append(base_dir / "docs" / "instructions.md")

        for path in candidates:
            if not path.exists() or not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except OSError:
                continue

            instruction_set.add_scope(
                InstructionScope(
                    level=agent_name or "global",
                    path=str(path),
                    content=content,
                    priority=0,
                )
            )

        # If no scopes were discovered, still return an empty InstructionSet
        return instruction_set


class InstructionCache:
    """Simple in-memory cache for instruction sets."""

    def __init__(self) -> None:
        self._loader = InstructionLoader()
        self._cache: Dict[Tuple[str, str], InstructionSet] = {}

    def get(self, current_dir: str, agent_name: Optional[str] = None) -> InstructionSet:
        """Fetch an InstructionSet, populating the cache on first access."""
        key = (str(Path(current_dir).resolve()), agent_name or "")
        if key not in self._cache:
            self._cache[key] = self._loader.load(current_dir=current_dir, agent_name=agent_name)
        return self._cache[key]
