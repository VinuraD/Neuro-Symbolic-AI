"""Global configuration for the Neuro-Symbolic Zebra system.

Single place for the puzzle vocabulary, the canonical clue kinds, model ids, and
filesystem paths. Imported by every layer (core, data, nlp, pipeline, eval, app)
so the symbolic and neural sides agree on the same categories and constraint set.
"""
from __future__ import annotations

from pathlib import Path

# --- puzzle vocabulary --------------------------------------------------------
# Default 5x5 Zebra/Einstein instance. Each category must have the same number of
# values; that count is the number of houses (positions 1..N).
DEFAULT_CATEGORIES: dict[str, list[str]] = {
    "color":  ["red", "green", "white", "yellow", "blue"],
    "nation": ["brit", "swede", "dane", "norwegian", "german"],
    "pet":    ["dog", "bird", "cat", "horse", "fish"],
    "drink":  ["tea", "coffee", "milk", "beer", "water"],
    "hobby":  ["painting", "reading", "swimming", "guitar", "cooking"],
}


def n_houses(categories: dict[str, list[str]] = DEFAULT_CATEGORIES) -> int:
    """Number of houses = number of values per category (all categories equal)."""
    sizes = {len(v) for v in categories.values()}
    if len(sizes) != 1:
        raise ValueError(f"all categories must have equal length, got sizes {sizes}")
    return sizes.pop()


N: int = n_houses(DEFAULT_CATEGORIES)  # default house count (5)

# --- canonical constraint set (the neuro<->symbolic contract) -----------------
# The five clue kinds the whole system speaks. See core/ir.py for semantics.
CLUE_KINDS: tuple[str, ...] = ("pos", "eq", "neq", "imm_left", "next")

# --- neural model ids (M2 parser / M4 renderer) -------------------------------
PARSER_MODEL_ID: str = "t5-small"      # NL clue -> constraint string
RENDERER_MODEL_ID: str = "t5-small"    # constraint string -> NL clue

# --- filesystem paths ---------------------------------------------------------
PKG_ROOT: Path = Path(__file__).resolve().parent
REPO_ROOT: Path = PKG_ROOT.parent
DATA_DIR: Path = PKG_ROOT / "data" / "artifacts"   # generated datasets land here
MODELS_DIR: Path = PKG_ROOT / "models"              # fine-tuned checkpoints land here
