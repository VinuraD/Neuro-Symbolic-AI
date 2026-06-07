"""M7 — individual evaluation metrics.

Pure functions over predictions/references and the symbolic core. They underpin
the results panel: parser quality, end-to-end solve quality, and the faithfulness
of generated clues.
"""
from __future__ import annotations

from ..config import DEFAULT_CATEGORIES
from ..core.ir import Constraint


def exact_match(pred: list[Constraint], gold: list[Constraint]) -> float:
    """Fraction of predicted constraints that equal their gold constraint."""
    raise NotImplementedError("M7: exact-match metric not implemented")


def valid_constraint_rate(pred_strings: list[str],
                          categories: dict[str, list[str]] = DEFAULT_CATEGORIES) -> float:
    """Fraction of predicted strings that parse to a structurally-valid constraint."""
    raise NotImplementedError("M7: valid-constraint-rate metric not implemented")


def solve_rate(predicted_clue_sets, gold_solutions,
               categories: dict[str, list[str]] = DEFAULT_CATEGORIES) -> float:
    """Fraction of puzzles whose parsed clues solve to the gold solution."""
    raise NotImplementedError("M7: end-to-end solve-rate metric not implemented")


def round_trip_faithfulness(sentences: list[str], gold: list[Constraint], parser) -> float:
    """Fraction of rendered sentences that re-parse to their original constraint."""
    raise NotImplementedError("M7: round-trip-faithfulness metric not implemented")
