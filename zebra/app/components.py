"""M6 — reusable Gradio UI pieces.

Grid/answer-key rendering (Gradio `Dataframe` or HTML), the clue-input widgets for
the Solve tab, and the metrics results panel. Kept separate from `main.py` so the
layout and the rendering helpers can evolve independently. Boilerplate stubs —
`main.build_demo` wires placeholders until these are filled in.
"""
from __future__ import annotations

from ..core.grid import Solution


def grid_to_dataframe(categories: dict[str, list[str]], solution: Solution):
    """Convert a solution grid to a Gradio `Dataframe`-ready table (rows=categories)."""
    raise NotImplementedError("M6: solution-grid Dataframe rendering not implemented")


def results_panel_md(metrics: dict) -> str:
    """Format an evaluation metrics dict as Markdown for the results panel."""
    raise NotImplementedError("M6: results panel rendering not implemented")
