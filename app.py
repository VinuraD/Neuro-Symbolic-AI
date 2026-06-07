"""Hugging Face Space entry point.

Thin shim so the Space (and `python app.py`) launch the Gradio UI defined in
`zebra.app.main`. All real logic lives in the `zebra` package.
"""
from zebra.app.main import build_demo

demo = build_demo()

if __name__ == "__main__":
    demo.launch()
