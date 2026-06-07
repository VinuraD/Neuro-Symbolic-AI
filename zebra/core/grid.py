"""Solution-grid helpers and template-based rendering (M0).

`render_solution` formats an answer key; `render_clue` is the deterministic
template fallback the neural renderer (`nlp.renderer.ClueRenderer`) falls back to
when no model is loaded. These templates are *not* the controlled-English
paraphrases of M1 — they are plain, unambiguous defaults.
"""
from __future__ import annotations

from ..config import DEFAULT_CATEGORIES, n_houses
from .ir import Constraint

Solution = dict[int, dict[str, str]]


def where_map(solution: Solution, n: int | None = None) -> dict[tuple[str, str], int]:
    """Invert a solution grid to {(category, value): house}."""
    n = n or len(solution)
    where: dict[tuple[str, str], int] = {}
    for h in range(1, n + 1):
        for cat, val in solution[h].items():
            where[(cat, val)] = h
    return where


def render_solution(
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    solution: Solution | None = None,
    n: int | None = None,
) -> str:
    """Render the answer key as a fixed-width ASCII table (one row per category)."""
    if solution is None:
        raise ValueError("solution is required")
    n = n or n_houses(categories)
    cats = list(categories.keys())
    width = max(len(c) for c in cats) + 1
    lines = ["house: " + "  ".join(f"{h:>8}" for h in range(1, n + 1))]
    for c in cats:
        row = "  ".join(f"{solution[h][c]:>8}" for h in range(1, n + 1))
        lines.append(f"{c:<{width}}: {row}")
    return "\n".join(lines)


def render_clue(clue: Constraint | tuple) -> str:
    """Deterministic English rendering of a single constraint (template fallback)."""
    c = clue if isinstance(clue, Constraint) else Constraint.from_tuple(clue)
    if c.type == "pos":
        (cat, val), pos = c.a, c.b
        return f"The {val} ({cat}) is in house {pos}."
    (c1, v1) = c.a
    (c2, v2) = c.b  # type: ignore[misc]
    if c.type == "eq":
        return f"The {v1} ({c1}) shares a house with the {v2} ({c2})."
    if c.type == "neq":
        return f"The {v1} ({c1}) is not in the same house as the {v2} ({c2})."
    if c.type == "imm_left":
        return f"The {v1} ({c1}) is immediately left of the {v2} ({c2})."
    if c.type == "next":
        return f"The {v1} ({c1}) is next to the {v2} ({c2})."
    return str(c)
