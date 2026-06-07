"""M4 — neural clue renderer: canonical `Constraint` -> fluent sentence.

The inverse seq2seq of the M2 parser, trained on the same M1 data with input and
target swapped. When no model is loaded it falls back to the deterministic
templates in `core.grid.render_clue`, so the renderer is always callable.
"""
from __future__ import annotations

from ..config import RENDERER_MODEL_ID
from ..core.grid import render_clue
from ..core.ir import Constraint


class ClueRenderer:
    """Wraps a seq2seq checkpoint mapping constraint string -> clue text."""

    def __init__(self, model_id: str = RENDERER_MODEL_ID, model_path: str | None = None):
        self.model_id = model_id
        self.model_path = model_path
        self._model = None
        self._tokenizer = None

    def load(self) -> "ClueRenderer":
        """Lazily load the underlying model + tokenizer."""
        raise NotImplementedError("M4: renderer model loading not implemented")

    def render(self, constraint: Constraint) -> str:
        """Render a constraint as a fluent clue sentence.

        Until the model is trained, callers may use `render_template` for a
        deterministic fallback.
        """
        raise NotImplementedError("M4: neural clue rendering not implemented")

    @staticmethod
    def render_template(constraint: Constraint) -> str:
        """Deterministic, always-available fallback (delegates to core templates)."""
        return render_clue(constraint)
