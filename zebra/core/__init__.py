"""Symbolic core (M0): the canonical Constraint IR, the CP-SAT solver, the
uniqueness check, and the symbolic-first puzzle generator. All working code."""
from __future__ import annotations

from .ir import Constraint, Attr, ClueKind, parse_constraint, is_valid
from .solver import build_model, solve, count_solutions, is_unique
from .generator import random_solution, derive_true_clues, generate_unique_puzzle
from .grid import render_solution, where_map

__all__ = [
    "Constraint",
    "Attr",
    "ClueKind",
    "parse_constraint",
    "is_valid",
    "build_model",
    "solve",
    "count_solutions",
    "is_unique",
    "random_solution",
    "derive_true_clues",
    "generate_unique_puzzle",
    "render_solution",
    "where_map",
]
