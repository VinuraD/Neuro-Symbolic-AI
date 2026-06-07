"""M3 — end-to-end solve pipeline.

Parse every clue with the M2 parser, build the CP-SAT model, solve. On UNSAT or a
non-unique result, hand off to `refine` (the solver's error is treated as evidence
of a bad parse). The symbolic solver, not the model, decides correctness.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..config import DEFAULT_CATEGORIES
from ..core.ir import Constraint
from ..core.solver import Grid


@dataclass
class SolveResult:
    """Outcome of solving a clue set."""

    grid: Grid | None = None
    status: str = "unknown"          # "unique" | "unsat" | "non_unique"
    constraints: list[Constraint] = field(default_factory=list)
    parses: list[tuple[str, Constraint]] = field(default_factory=list)  # (sentence, parsed)
    refined: bool = False


class SolvePipeline:
    """Clue sentences -> parsed constraints -> CP-SAT solution."""

    def __init__(self, parser=None, categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
                 self_refine: bool = True):
        self.parser = parser
        self.categories = categories
        self.self_refine = self_refine

    def solve(self, clue_texts: list[str]) -> SolveResult:
        """Parse all clues, solve, and (optionally) self-refine on failure."""
        raise NotImplementedError("M3: end-to-end solve pipeline not implemented")
