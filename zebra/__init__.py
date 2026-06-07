"""Neuro-Symbolic Zebra: solve and generate Zebra/Einstein logic puzzles.

Design rule: the symbolic CP-SAT layer (`zebra.core`) owns all logic, coherence,
and uniqueness; the small seq2seq models (`zebra.nlp`) only translate clue text
<-> formal constraint. The top-level namespace re-exports the lightweight core API;
heavier layers (nlp, training, app) are imported from their own subpackages.
"""
from __future__ import annotations

from .config import DEFAULT_CATEGORIES, N, CLUE_KINDS
from .core import (
    Constraint,
    parse_constraint,
    is_valid,
    build_model,
    solve,
    count_solutions,
    is_unique,
    generate_unique_puzzle,
    render_solution,
)

__all__ = [
    "DEFAULT_CATEGORIES",
    "N",
    "CLUE_KINDS",
    "Constraint",
    "parse_constraint",
    "is_valid",
    "build_model",
    "solve",
    "count_solutions",
    "is_unique",
    "generate_unique_puzzle",
    "render_solution",
]
