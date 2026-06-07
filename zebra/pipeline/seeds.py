"""M4 — seed-word handling for generation.

Maps user-supplied seed words (e.g. "swede", "cat", "tea") onto category values
and auto-fills any categories the seeds don't cover from the defaults, producing a
complete category set ready for symbolic generation. This mapping has fiddly edge
cases (unknown words, duplicates, partial categories) — see roadmap risk #3.
"""
from __future__ import annotations

from ..config import DEFAULT_CATEGORIES


def seeds_to_categories(
    words: list[str],
    base: dict[str, list[str]] = DEFAULT_CATEGORIES,
) -> dict[str, list[str]]:
    """Return a complete category set incorporating `words`, auto-filling the rest."""
    raise NotImplementedError("M4: seed-word -> category mapping not implemented")
