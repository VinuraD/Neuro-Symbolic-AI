"""M1 (optional) — offline paraphrase augmentation.

A larger LLM may be used *offline* to widen paraphrase variety beyond the hand
templates. Every augmented sentence must pass a round-trip check (re-parse with
the M2 parser; keep only if it recovers the original constraint). This runs at
data-prep time only — never in the live app.
"""
from __future__ import annotations

from typing import Iterable

from ..core.ir import Constraint


def augment_paraphrases(
    examples: Iterable[dict],
    model: str = "claude-opus-4-8",
    n_variants: int = 3,
) -> Iterable[dict]:
    """Yield extra `{"sentence", "constraint"}` rows paraphrased by an offline LLM.

    Each candidate is filtered through `round_trip_ok`. Offline only.
    """
    raise NotImplementedError("M1: offline LLM paraphrase augmentation not implemented")


def round_trip_ok(sentence: str, target: Constraint, parser=None) -> bool:
    """True iff parsing `sentence` recovers `target` (the augmentation filter)."""
    raise NotImplementedError("M1: round-trip parseability filter not implemented")
