"""M6 Gradio app — two tabs (Solve, Generate) wired to the verified core and
the M2/M4 models. Gradio is imported lazily inside `build_demo`. Boilerplate
stub."""
from __future__ import annotations

from .main import build_demo

__all__ = ["build_demo"]
