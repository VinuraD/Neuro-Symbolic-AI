"""Fine-tune the M4 clue renderer (constraint string -> sentence).

Run:  python -m zebra.training.train_renderer
Identical to the parser training except the M1 (sentence, constraint) pairs are
used with input and target swapped.
"""
from __future__ import annotations

from ..config import MODELS_DIR, RENDERER_MODEL_ID


def train_renderer(
    model_id: str = RENDERER_MODEL_ID,
    output_dir=MODELS_DIR,
    epochs: int = 10,
):
    """Train and persist the renderer; return the eval metrics dict."""
    raise NotImplementedError("M4: renderer fine-tuning not implemented")


if __name__ == "__main__":
    train_renderer()
