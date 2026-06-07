"""M7 — evaluation harness.

Runs the metric suite over the held-out test set and the generators, returning the
results dict the Gradio panel renders: parser exact-match / valid-constraint rate,
end-to-end solve rate (parser-only vs self-refined), generation uniqueness sanity,
round-trip faithfulness, and latency per solve / per generate.

Run:  python -m zebra.eval.evaluate
"""
from __future__ import annotations


def evaluate_all(parser=None, renderer=None, n_puzzles: int = 200, seed: int | None = None) -> dict:
    """Run the full evaluation suite and return a metrics dict."""
    raise NotImplementedError("M7: full evaluation harness not implemented")


if __name__ == "__main__":
    print(evaluate_all())
