"""M1 — controlled-English clue grammar.

A deliberately narrow set of paraphrase templates per clue kind. Bounded phrasing
is what lets a small model learn the mapping reliably (unconstrained phrasing is
the #1 failure mode). A subset of templates is held out (`HELD_OUT`) and used only
in the test split, so evaluation measures generalization to *unseen phrasings*,
not just unseen examples.

Author the templates here; placeholders use `{a}` / `{b}` for the two attributes
(e.g. "the swede") and `{pos}` for a position.
"""
from __future__ import annotations

from ..core.ir import ClueKind, Constraint

# Training-visible templates. Fill these in during M1.
# Example shape (to be authored):
#   "next": ["{a} is next to {b}", "{b} is beside {a}", "{a} and {b} are neighbours"]
TEMPLATES: dict[ClueKind, list[str]] = {
    "pos": [],
    "eq": [],
    "neq": [],
    "imm_left": [],
    "next": [],
}

# Held-out templates reserved for the generalization test split (never trained on).
HELD_OUT: dict[ClueKind, list[str]] = {
    "pos": [],
    "eq": [],
    "neq": [],
    "imm_left": [],
    "next": [],
}


def render_template(c: Constraint, template: str) -> str:
    """Fill a paraphrase `template` with the attributes/position of `c`.

    Returns a natural-language clue sentence. Inverse target is `c.to_str()`.
    """
    raise NotImplementedError("M1: controlled-grammar template rendering not implemented")
