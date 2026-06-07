"""M1 — synthetic example generation.

Emits the two datasets the neural models train on:
  - (sentence, constraint) pairs  -> M2 parser  /  M4 renderer (swapped)
  - (puzzle, clue-set) examples   -> whole-puzzle context, optional

Each example pairs a controlled-English sentence (via `data.grammar`) with the
canonical constraint string (`Constraint.to_str()`).
"""
from __future__ import annotations

from typing import Iterable

from ..config import DEFAULT_CATEGORIES


def gen_examples(
    n: int,
    seed: int | None = None,
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
    held_out: bool = False,
) -> Iterable[dict]:
    """Yield `n` examples `{"sentence": str, "constraint": str}`.

    `held_out=True` draws phrasings from `grammar.HELD_OUT` for the test split.
    """
    raise NotImplementedError("M1: (sentence, constraint) example generation not implemented")


def gen_puzzle_examples(
    n: int,
    seed: int | None = None,
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
) -> Iterable[dict]:
    """Yield `n` examples `{"puzzle": str, "clue_set": str}` for whole-puzzle context."""
    raise NotImplementedError("M1: (puzzle, clue-set) example generation not implemented")
