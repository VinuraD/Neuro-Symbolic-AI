"""Training scripts for the M2 parser and M4 renderer.

Both fine-tune a small seq2seq model on the M1 synthetic data via HF
`Seq2SeqTrainer` — the renderer reuses the parser's data with input/target
swapped. Boilerplate stubs."""
from __future__ import annotations

from .train_parser import train_parser
from .train_renderer import train_renderer

__all__ = ["train_parser", "train_renderer"]
