"""Symbolic-first puzzle generator (M0).

Strategy: pick a random full solution, derive every clue that is true of it
(over-determined => unique), then greedily drop clues that aren't needed for
uniqueness. The CP-SAT solver — never a model — guarantees the result is uniquely
solvable. `prefer_relational` drops `pos` clues first for more interesting puzzles.
"""
from __future__ import annotations

import itertools
import random

from ..config import DEFAULT_CATEGORIES, n_houses
from .grid import Solution, render_clue, render_solution, where_map
from .ir import Constraint
from .solver import count_solutions, is_unique, solve


def random_solution(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    rng: random.Random | None = None,
    n: int | None = None,
) -> Solution:
    """A uniformly-random valid assignment of values to houses per category."""
    rng = rng or random.Random()
    n = n or n_houses(categories)
    grid: Solution = {h: {} for h in range(1, n + 1)}
    for cat, vals in categories.items():
        houses = list(range(1, n + 1))
        rng.shuffle(houses)
        for val, h in zip(vals, houses):
            grid[h][cat] = val
    return grid


def derive_true_clues(
    categories: dict[str, list[str]],
    solution: Solution,
    rng: random.Random,
    n: int | None = None,
) -> list[Constraint]:
    """A pool of `Constraint`s that all hold for `solution`.

    Includes every `pos` clue (so the pool alone pins the unique solution), all
    same-house pairs, all adjacency pairs (imm_left + next), and a sample of
    difference (neq) clues.
    """
    n = n or n_houses(categories)
    cats = list(categories.keys())
    where = where_map(solution, n)

    clues: list[Constraint] = []
    # fixed positions (guarantee the starting pool is uniquely solvable)
    for attr, h in where.items():
        clues.append(Constraint("pos", attr, h))
    # same-house pairs (one per distinct category pair per house)
    for h in range(1, n + 1):
        attrs = [(c, solution[h][c]) for c in cats]
        for a, b in itertools.combinations(attrs, 2):
            clues.append(Constraint("eq", a, b))
    # adjacency clues across adjacent houses
    for h in range(1, n):
        left = [(c, solution[h][c]) for c in cats]
        right = [(c, solution[h + 1][c]) for c in cats]
        for a in left:
            for b in right:
                clues.append(Constraint("imm_left", a, b))
                clues.append(Constraint("next", a, b))
    # a sample of difference clues (there are many; keep a handful)
    diff_pool: list[Constraint] = []
    attrs_all = list(where.keys())
    for a, b in itertools.combinations(attrs_all, 2):
        if where[a] != where[b]:
            diff_pool.append(Constraint("neq", a, b))
    rng.shuffle(diff_pool)
    clues.extend(diff_pool[: 2 * n])

    rng.shuffle(clues)
    return clues


def generate_unique_puzzle(
    categories: dict[str, list[str]] | None = None,
    seed: int | None = None,
    prefer_relational: bool = True,
) -> tuple[list[Constraint], Solution]:
    """Generate (clues, solution) where `clues` uniquely determine `solution`."""
    if categories is None:
        categories = DEFAULT_CATEGORIES
    rng = random.Random(seed)
    n = n_houses(categories)

    solution = random_solution(categories, rng, n)
    pool = derive_true_clues(categories, solution, rng, n)

    # sanity: the full pool must be uniquely solvable
    assert is_unique(categories, pool), "true-clue pool was not unique (bug)"

    # trimming order: drop 'pos' clues first for more relational puzzles
    order = list(range(len(pool)))
    rng.shuffle(order)
    if prefer_relational:
        order.sort(key=lambda i: 0 if pool[i].type == "pos" else 1)

    kept = list(pool)
    for i in order:
        clue = pool[i]
        if clue not in kept:
            continue
        trial = [c for c in kept if c is not clue]
        if is_unique(categories, trial):
            kept = trial
    return kept, solution


# --------------------------------------------------------------------------
# self-test:  python -m zebra.core.generator
# --------------------------------------------------------------------------
if __name__ == "__main__":
    cats = DEFAULT_CATEGORIES
    clues, solution = generate_unique_puzzle(cats, seed=7)

    print(f"Generated a puzzle with {len(clues)} clues.\n")
    for clue in clues:
        print("  - " + render_clue(clue) + f"   [{clue.to_str()}]")

    print("\nIntended solution:")
    print(render_solution(cats, solution))

    n_sols = count_solutions(cats, clues, limit=2)
    recovered = solve(cats, clues)
    print(f"\nself-test: solution count (capped at 2) = {n_sols}")
    print(f"self-test: unique = {is_unique(cats, clues)}")
    print(f"self-test: solver matches intended solution = {recovered == solution}")
