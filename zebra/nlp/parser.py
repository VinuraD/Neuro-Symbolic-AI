"""M2 — neural clue parser: natural-language clue -> canonical `Constraint`.

A fine-tuned small seq2seq model. It only translates; it never decides logic.
`parse_beam` exposes the top-k candidates so the solve-loop (M3) can re-rank when
the solver reports UNSAT or a non-unique result.
"""
from __future__ import annotations

from ..config import PARSER_MODEL_ID
from ..core.ir import Constraint


class ClueParser:
    """Wraps a seq2seq checkpoint mapping clue text -> constraint string."""

    def __init__(self, model_id: str = PARSER_MODEL_ID, model_path: str | None = None):
        self.model_id = model_id
        self.model_path = model_path
        self._model = None
        self._tokenizer = None

    def load(self) -> "ClueParser":
        """Lazily load the underlying model + tokenizer."""
        raise NotImplementedError("M2: parser model loading not implemented")

    def parse(self, sentence: str) -> Constraint:
        """Parse one clue sentence into a `Constraint` (greedy / top-1)."""
        raise NotImplementedError("M2: clue parsing not implemented")

    def parse_beam(self, sentence: str, k: int = 5) -> list[Constraint]:
        """Return up to `k` candidate constraints (well-formed ones only)."""
        raise NotImplementedError("M2: beam-candidate parsing not implemented")
