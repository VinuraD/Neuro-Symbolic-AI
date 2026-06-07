"""M4 — symbolic-first generation pipeline.

seed words -> complete categories (`seeds_to_categories`) -> unique puzzle from the
CP-SAT generator (M0) -> render each constraint with the M4 renderer. A round-trip
guard re-parses every rendered sentence with the M2 parser; if it doesn't recover
the original constraint, that sentence is regenerated. The solver guarantees
coherence and uniqueness — the model only verbalizes.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..config import DEFAULT_CATEGORIES
from ..core.grid import Solution
from ..core.ir import Constraint


@dataclass
class GenerateResult:
    """A generated puzzle plus its verified answer key."""

    sentences: list[str] = field(default_factory=list)
    clues: list[Constraint] = field(default_factory=list)
    solution: Solution | None = None
    answer_key: str = ""
    round_trip_ok: bool = False


class GeneratePipeline:
    """Seed words -> uniquely-solvable puzzle text + answer key."""

    def __init__(self, parser=None, renderer=None,
                 categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
                 max_render_retries: int = 5):
        self.parser = parser
        self.renderer = renderer
        self.categories = categories
        self.max_render_retries = max_render_retries

    def generate(self, seeds: list[str] | None = None, seed: int | None = None) -> GenerateResult:
        """Generate a puzzle from seed words with a round-trip render guard."""
        raise NotImplementedError("M4: symbolic-first generation pipeline not implemented")
