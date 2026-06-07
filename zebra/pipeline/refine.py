"""M3 — solver-in-the-loop self-refinement (Logic-LM blueprint).

When the parsed clue set is unsatisfiable or non-unique, that is evidence of a bad
parse. Re-rank the parser's beam candidates for the offending clue(s) and re-solve,
iterating until the result is unique or a retry budget is exhausted. Pure repair
logic — it never invents constraints the model didn't propose.
"""
from __future__ import annotations

from ..config import DEFAULT_CATEGORIES


def refine(
    result,
    parser,
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    max_rounds: int = 3,
):
    """Attempt to repair a failed `SolveResult` using the solver's signal.

    Returns an updated `SolveResult` (unique if repair succeeds).
    """
    raise NotImplementedError("M3: solver-in-the-loop self-refinement not implemented")
