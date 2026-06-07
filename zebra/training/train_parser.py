"""Fine-tune the M2 clue parser (sentence -> constraint string).

Run:  python -m zebra.training.train_parser
Loads the M1 dataset, fine-tunes a small seq2seq via `Seq2SeqTrainer`, and saves
the checkpoint under `config.MODELS_DIR`.
"""
from __future__ import annotations

from ..config import MODELS_DIR, PARSER_MODEL_ID


def train_parser(
    model_id: str = PARSER_MODEL_ID,
    output_dir=MODELS_DIR,
    epochs: int = 10,
):
    """Train and persist the parser; return the eval metrics dict."""
    raise NotImplementedError("M2: parser fine-tuning not implemented")


if __name__ == "__main__":
    train_parser()
