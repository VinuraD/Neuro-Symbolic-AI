"""M1 — dataset assembly and splitting (HuggingFace `datasets`).

Builds a `DatasetDict` with train/val/test. The crucial split rule: the test set
holds out whole *paraphrase templates* (see `grammar.HELD_OUT`), not just random
rows, so accuracy on it reflects real generalization to unseen phrasing.
"""
from __future__ import annotations

from ..config import DATA_DIR, DEFAULT_CATEGORIES


def build_dataset(
    n_train: int = 20000,
    n_val: int = 2000,
    n_test: int = 2000,
    seed: int | None = None,
    categories: dict[str, list[str]] = DEFAULT_CATEGORIES,
):
    """Build and return a `datasets.DatasetDict` with train/val/test splits.

    Test split uses held-out paraphrase templates. `datasets` is imported lazily.
    """
    raise NotImplementedError("M1: dataset build/split not implemented")


def save_dataset(dataset, path=DATA_DIR) -> None:
    """Persist a built dataset to disk (`save_to_disk`)."""
    raise NotImplementedError("M1: dataset persistence not implemented")


def load_dataset(path=DATA_DIR):
    """Load a previously-built dataset from disk (`load_from_disk`)."""
    raise NotImplementedError("M1: dataset loading not implemented")
