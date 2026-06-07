"""M2 parser + M4 renderer — the only neural components.

`ClueParser` maps a clue sentence to a canonical Constraint; `ClueRenderer`
is its inverse. Both wrap a small seq2seq model and never decide logic.
Heavy deps (transformers/torch) are imported lazily inside methods so the
modules import cleanly without a model loaded. Boilerplate stubs."""
from __future__ import annotations

from .parser import ClueParser
from .renderer import ClueRenderer

__all__ = ["ClueParser", "ClueRenderer"]
