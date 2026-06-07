# Neuro-Symbolic Zebra

- **Solve** — natural-language clues → solved grid (parse clues → CP-SAT → solution).
- **Generate** — seed words → a uniquely-solvable puzzle + answer key (symbolic-first
  generation, then neural rendering with a round-trip parse guard).

## Architecture

## Deploy (local)

```bash
conda create -n nesy python=3.11 -y
conda activate nesy
pip install -r zebra/requirements.txt

python -m zebra.core.generator   # M0 self-test (generate → verify unique → solve)
python app.py                    # launch the Gradio app
```

