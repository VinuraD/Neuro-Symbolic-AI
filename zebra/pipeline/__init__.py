"""M3 solve-loop + M4 generate-loop — orchestration that wires the neural
front-end to the symbolic core.

`SolvePipeline` parses clues then solves with CP-SAT (with optional
self-refinement on UNSAT / non-unique). `GeneratePipeline` turns seed words
into a uniquely-solvable puzzle symbolically, then renders each constraint with
a round-trip parse guard. Boilerplate stubs."""
from __future__ import annotations

from .seeds import seeds_to_categories
from .solve import SolvePipeline, SolveResult
from .refine import refine
from .generate import GeneratePipeline, GenerateResult

__all__ = [
    "seeds_to_categories",
    "SolvePipeline",
    "SolveResult",
    "refine",
    "GeneratePipeline",
    "GenerateResult",
]
