"""M1 — controlled clue grammar + synthetic data generation.

Authoring of paraphrase templates per clue kind, emission of
(sentence, constraint) and (puzzle, clue-set) example pairs, and HF
`datasets` build/split with held-out paraphrase templates for a real
generalization test. Boilerplate stubs."""
from __future__ import annotations

from .grammar import TEMPLATES, HELD_OUT, render_template
from .synth import gen_examples, gen_puzzle_examples
from .dataset import build_dataset
from .augment import augment_paraphrases, round_trip_ok

__all__ = [
    "TEMPLATES",
    "HELD_OUT",
    "render_template",
    "gen_examples",
    "gen_puzzle_examples",
    "build_dataset",
    "augment_paraphrases",
    "round_trip_ok",
]
