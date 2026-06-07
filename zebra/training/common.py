"""Shared training plumbing for the M2 parser and M4 renderer.

Holds the common `Seq2SeqTrainingArguments`, the data collator, tokenization, and
the compute-metrics callback (exact-match + valid-constraint rate). Both training
scripts differ only in which field is the input and which is the target.
"""
from __future__ import annotations

from ..config import MODELS_DIR


def default_training_args(output_dir=MODELS_DIR, epochs: int = 10, lr: float = 3e-4):
    """Return a `Seq2SeqTrainingArguments` with CPU-friendly defaults + early stopping."""
    raise NotImplementedError("M2/M4: training arguments not implemented")


def make_collator(tokenizer):
    """Return a `DataCollatorForSeq2Seq` for dynamic padding."""
    raise NotImplementedError("M2/M4: data collator not implemented")


def tokenize_fn(tokenizer, input_field: str, target_field: str):
    """Return a `.map`-able function tokenizing (input_field -> target_field)."""
    raise NotImplementedError("M2/M4: tokenization function not implemented")


def compute_metrics_fn(tokenizer):
    """Return a compute_metrics callback: exact-match + valid-constraint rate."""
    raise NotImplementedError("M2/M4: metrics callback not implemented")
