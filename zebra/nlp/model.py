"""Shared seq2seq plumbing for the M2 parser and M4 renderer.

Thin wrappers over HuggingFace Transformers for loading/saving a small encoder-
decoder model (T5-small / BART-base) and its tokenizer, plus an optional
grammar-constrained decoding helper so the parser can be forced to emit only
well-formed constraint strings. `transformers`/`torch` are imported lazily.
"""
from __future__ import annotations

from ..config import PARSER_MODEL_ID


def load_seq2seq(model_id: str = PARSER_MODEL_ID):
    """Load and return (model, tokenizer). Imports `transformers` lazily."""
    raise NotImplementedError("M2: seq2seq model/tokenizer loading not implemented")


def save_seq2seq(model, tokenizer, path) -> None:
    """Persist a fine-tuned model + tokenizer to `path`."""
    raise NotImplementedError("M2: model persistence not implemented")


def generate(model, tokenizer, text: str, num_beams: int = 1, num_return: int = 1):
    """Run beam-search generation, returning a list of decoded strings."""
    raise NotImplementedError("M2: constrained/beam generation not implemented")
