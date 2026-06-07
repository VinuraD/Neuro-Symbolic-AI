"""CP-SAT symbolic solver (M0). Builds an OR-Tools model from a category set and
a list of constraints, solves it, and counts solutions to verify uniqueness.

Position-encoding: one IntVar per attribute in [1..N], `AddAllDifferent` per
category. The five canonical clue kinds map to arithmetic on those vars.
"""
from __future__ import annotations

from typing import Iterable, Union

from ortools.sat.python import cp_model

from ..config import DEFAULT_CATEGORIES, n_houses
from .ir import Constraint

Clue = Union[Constraint, tuple]
Grid = dict[int, dict[str, str]]


def _as_constraint(clue: Clue) -> Constraint:
    return clue if isinstance(clue, Constraint) else Constraint.from_tuple(clue)


def build_model(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    clues: Iterable[Clue] = (),
    n: int | None = None,
):
    """Return (CpModel, variables) where variables maps (category, value) -> IntVar.

    `clues` may be `Constraint`s or `(type, a, b)` tuples; both are normalized.
    """
    n = n or n_houses(categories)
    model = cp_model.CpModel()
    variables: dict[tuple[str, str], cp_model.IntVar] = {}
    for cat, vals in categories.items():
        for v in vals:
            variables[(cat, v)] = model.NewIntVar(1, n, f"{cat}_{v}")
        model.AddAllDifferent([variables[(cat, v)] for v in vals])

    for clue in clues:
        _add_constraint(model, variables, _as_constraint(clue), n)
    return model, variables


def _add_constraint(model, variables, c: Constraint, n: int) -> None:
    va = variables[c.a]
    if c.type == "pos":
        model.Add(va == int(c.b))
        return
    vb = variables[c.b]  # type: ignore[index]
    if c.type == "eq":
        model.Add(va == vb)
    elif c.type == "neq":
        model.Add(va != vb)
    elif c.type == "imm_left":
        model.Add(va == vb - 1)
    elif c.type == "next":
        diff = model.NewIntVar(-n, n, "")
        dist = model.NewIntVar(0, n, "")
        model.Add(diff == va - vb)
        model.AddAbsEquality(dist, diff)
        model.Add(dist == 1)
    else:
        raise ValueError(f"unknown clue type {c.type!r}")


class _SolutionCounter(cp_model.CpSolverSolutionCallback):
    """Stops the search once `limit` solutions are seen (uniqueness needs only 2)."""

    def __init__(self, limit: int = 2):
        super().__init__()
        self.count = 0
        self._limit = limit

    def on_solution_callback(self) -> None:
        self.count += 1
        if self.count >= self._limit:
            self.StopSearch()


def count_solutions(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    clues: Iterable[Clue] = (),
    limit: int = 2,
    n: int | None = None,
) -> int:
    """Count solutions, capped at `limit` (enumeration stops early)."""
    model, _ = build_model(categories, clues, n)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    counter = _SolutionCounter(limit)
    solver.Solve(model, counter)
    return counter.count


def solve(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    clues: Iterable[Clue] = (),
    n: int | None = None,
) -> Grid | None:
    """Return the solution grid {house: {category: value}} or None if UNSAT."""
    n = n or n_houses(categories)
    model, variables = build_model(categories, clues, n)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    grid: Grid = {h: {} for h in range(1, n + 1)}
    for (cat, val), var in variables.items():
        grid[solver.Value(var)][cat] = val
    return grid


def is_unique(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    clues: Iterable[Clue] = (),
) -> bool:
    """True iff the clue set has exactly one solution."""
    clues = list(clues)
    return count_solutions(categories, clues, limit=2) == 1
