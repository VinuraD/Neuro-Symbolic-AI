"""M7 evaluation — parser accuracy, end-to-end solve rate, generation
uniqueness sanity, round-trip faithfulness, and latency. Produces the results
dict the Gradio panel renders. Boilerplate stubs."""
from __future__ import annotations

from .metrics import (
    exact_match,
    valid_constraint_rate,
    solve_rate,
    round_trip_faithfulness,
)
from .evaluate import evaluate_all

__all__ = [
    "exact_match",
    "valid_constraint_rate",
    "solve_rate",
    "round_trip_faithfulness",
    "evaluate_all",
]
