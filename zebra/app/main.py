"""M6 — Gradio app entry point.

Two tabs:
  Solve     enter/select clues -> solution grid
  Generate  enter seed words   -> puzzle text + answer key

`build_demo` constructs the Blocks and boots today; the Solve/Generate handlers
return clear "model not trained yet" placeholders until the M2 parser and M4
renderer are wired in (replace the bodies marked TODO). Gradio is imported lazily
so importing this module never requires gradio to be installed.
"""
from __future__ import annotations

from ..config import DEFAULT_CATEGORIES

_PLACEHOLDER_SOLVE = (
    "⚠️ The neural clue parser (M2) is not trained yet.\n"
    "The symbolic CP-SAT solver is ready — train the parser to enable "
    "natural-language solving, then wire SolvePipeline here."
)
_PLACEHOLDER_GENERATE = (
    "⚠️ The neural renderer (M4) is not trained yet.\n"
    "The symbolic generator is ready — train the renderer to verbalize puzzles, "
    "then wire GeneratePipeline here."
)


def _on_solve(clue_text: str) -> str:
    # TODO(M3): parse clue_text -> SolvePipeline.solve -> render grid
    return _PLACEHOLDER_SOLVE


def _on_generate(seed_words: str) -> str:
    # TODO(M4): seeds -> GeneratePipeline.generate -> puzzle text + answer key
    return _PLACEHOLDER_GENERATE


def build_demo(categories: dict[str, list[str]] = DEFAULT_CATEGORIES):
    """Build and return the Gradio `Blocks` app (does not launch it)."""
    import gradio as gr  # lazy import

    with gr.Blocks(title="Neuro-Symbolic Zebra") as demo:
        gr.Markdown("# Neuro-Symbolic Zebra\nSolve and generate Zebra logic puzzles.")
        with gr.Tab("Solve"):
            clues_in = gr.Textbox(label="Clues (one per line)", lines=8)
            solve_btn = gr.Button("Solve", variant="primary")
            solve_out = gr.Textbox(label="Solution", lines=8)
            solve_btn.click(_on_solve, inputs=clues_in, outputs=solve_out)
        with gr.Tab("Generate"):
            seeds_in = gr.Textbox(label="Seed words (comma-separated)")
            gen_btn = gr.Button("Generate", variant="primary")
            gen_out = gr.Textbox(label="Puzzle + answer key", lines=12)
            gen_btn.click(_on_generate, inputs=seeds_in, outputs=gen_out)
    return demo


if __name__ == "__main__":
    build_demo().launch()
