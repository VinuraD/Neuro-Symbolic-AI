# Roadmap — Small-Model NeSy Zebra Puzzle (Solve + Generate + Gradio)

**Goal.** A neurosymbolic system where a *small* neural model handles only
natural language, and a symbolic solver owns all logic. Two capabilities:
(1) **solve** a zebra puzzle given natural-language clues, and (2) **generate**
a coherent, uniquely-solvable puzzle from seed words. Ship it as a Gradio app.

**The one design rule everything depends on.** The symbolic layer owns *all*
reasoning and *all* coherence guarantees. The small model never decides logic
and never guarantees uniqueness — it only maps clue text → constraint and
constraint → clue text. Every milestone below respects this split.

**Why this project.** It is the structural twin of the tender/bid pipeline:
parse natural language into formal constraints, check logical coherence, and
generate instances that satisfy the constraints. Skills transfer directly.

**Status:** Milestone 0 is already built and verified (`zebra.py`).

---

## Milestone 0 — Symbolic core  ✅ DONE (~1 day, completed)

**Deliverable.** `zebra.py`: a CP-SAT solver, a solution counter / uniqueness
check, true-clue derivation from a random solution, and a generator that trims
clues to a minimal uniquely-solvable set. Verified: 40/40 generated puzzles are
unique and recovered exactly by the solver; ~1 s per generate-and-verify.

**Background required.**
- Constraint satisfaction modeling: variables, domains, constraints.
- The position-encoding of a zebra puzzle: one integer var per attribute in
  `[1..N]`, `AllDifferent` per category.
- Counting solutions to test *uniqueness* (enumerate, cap at 2).
- Generation by over-determination then greedy trimming to a minimal set
  (the same uniqueness-trim idea used for Futoshiki/Sudoku generation).

**Material.**
- OR-Tools CP-SAT Python docs: https://developers.google.com/optimization/cp/cp_solver
- The classic Zebra/Einstein puzzle formulation (any reference).
- `zebra.py` (this project).

---

## Milestone 1 — Controlled clue grammar + synthetic data  (~1 day)

**Deliverable.** A controlled-English grammar with paraphrase templates for each
of the 5 clue kinds (`pos`, `eq`, `neq`, `imm_left`, `next`), and a generator
that emits large datasets of `(clue sentence, formal constraint)` pairs plus
`(formal puzzle, clue-set text)` examples. Hold out some paraphrase patterns for
a generalization test set.

**Background required.**
- Semantic parsing framed as sequence-to-sequence (text → a canonical
  linearized constraint string).
- Controlled natural language: deliberately bounding phrasing so a small model
  can learn it reliably. (Unconstrained phrasing is the main failure mode.)
- Synthetic-data generation and train/val/test splitting; why holding out
  *paraphrase templates* (not just examples) measures real generalization.

**Material.**
- Paraphrase templates you author (e.g., for `next`: "X is next to Y", "Y is
  beside X", "X and Y are neighbours", ...).
- Optional: a larger LLM used *offline* to augment paraphrase variety (then
  filter by round-trip parseability). Augmentation only — not in the live app.
- HuggingFace `datasets` for storing/splitting: https://huggingface.co/docs/datasets

---

## Milestone 2 — Neural clue parser (NL → constraint)  (~1–1.5 days)

**Deliverable.** A fine-tuned small seq2seq model (T5-small/base or BART-base,
~60–250M params) mapping a clue sentence to its canonical constraint string,
e.g. `"The Swede is immediately left of the red house" -> imm_left(nation:Swede, color:red)`.
Report exact-match accuracy and "parses to a valid constraint" rate on the
held-out paraphrase test set.

**Background required.**
- Fine-tuning encoder-decoder transformers; tokenization; teacher forcing.
- Producing *structured* outputs reliably (canonical string format; optionally
  constrained decoding / grammar-constrained generation).
- Evaluation: exact-match vs execution accuracy (does the parsed constraint, fed
  to the solver, behave correctly?); early stopping to avoid overfitting on
  synthetic data.

**Material.**
- HuggingFace Transformers + `Trainer`/`Seq2SeqTrainer`:
  https://huggingface.co/docs/transformers
- T5 and BART model cards (start with `t5-small` / `facebook/bart-base`).
- Conceptual anchor (LLM → symbolic formulation): Logic-LM (see M3).

---

## Milestone 3 — Solver-in-the-loop + self-refinement  (~0.5–1 day)

**Deliverable.** End-to-end solving: parse all clues → build the CP-SAT model →
solve. When the result is unsatisfiable or non-unique, treat that as evidence of
a bad parse and refine (re-rank beam candidates, or re-parse the offending
clue). Report end-to-end solve accuracy vs parser-only.

**Background required.**
- Error-driven repair: using the solver's UNSAT / multiple-solutions signal as
  a feedback signal for the neural front-end (the same idea as the nonogram
  "logic corrects perception" loop).
- Beam search and candidate re-ranking.

**Material.**
- Logic-LM: Pan, Albalak, Wang, Wang. "Logic-LM: Empowering Large Language
  Models with Symbolic Solvers for Faithful Logical Reasoning." Findings of
  EMNLP 2023. https://arxiv.org/abs/2305.12295 — its self-refinement module
  (revise the formalization from the solver's error messages) is the blueprint.

---

## Milestone 4 — Neural renderer + symbolic-first generation + seeds  (~1–1.5 days)

**Deliverable.** Given seed words: map them to category values (auto-fill any
categories the seeds miss), generate a unique puzzle *symbolically* (M0), then
render each constraint into a fluent sentence with a small constraint→text
model. **Round-trip guard:** re-parse each rendered sentence with the M2 parser;
if it doesn't recover the original constraint, regenerate the sentence.

**Background required.**
- Symbolic-first generation: the solver guarantees coherence and uniqueness; the
  model only verbalizes. (Never let the model invent the puzzle.)
- Faithful/controllable generation and round-trip consistency as a correctness
  check that reuses the parser on the generation side.

**Material.**
- The renderer is the inverse seq2seq of M2 (constraint string → sentence),
  trained on the same M1 data with input/target swapped.
- Same Transformers stack as M2.

---

## Milestone 5 — (Optional) Differentiable variant via Scallop  (~1 day, stretch)

**Deliverable.** A differentiable version of the parse→solve pipe: the parser
emits *probabilistic* constraint facts, Scallop's Datalog encodes the puzzle
logic, and you supervise only on the final solution so gradients flow back into
the parser without per-clue labels.

**Background required.**
- Differentiable logical reasoning; probabilistic facts; provenance semirings as
  the gradient mechanism.
- Why a hard CP-SAT solver is *not* differentiable, and how Scallop's relaxed
  reasoning provides gradients instead.

**Material.**
- Scallop: Li et al. "Scallop: A Language for Neurosymbolic Programming."
  PLDI 2023. https://arxiv.org/abs/2304.04812
- `scallop-lang/scallop` + the `scallopy` PyTorch bindings:
  https://github.com/scallop-lang/scallop
- Honest note: this is the heaviest milestone. Build the supervised pipeline
  first; the architecture doesn't change when you swap in the differentiable
  trainer, so treat this as an upgrade, not a prerequisite.

---

## Milestone 6 — Gradio app  (~0.5–1 day)

**Deliverable.** Two tabs. **Solve:** enter/select clues → render the solution
grid (optionally animate the deduction). **Generate:** enter seed words → puzzle
text plus the answer key. Wired to the verified core and the M2/M4 models.

**Background required.**
- Gradio `Blocks` / `Interface`, components, and state.
- Rendering a table/grid (Gradio `Dataframe` or HTML) for the solution.

**Material.**
- Gradio docs: https://www.gradio.app/docs

---

## Milestone 7 — Deploy + evaluate + polish  (~0.5 day)

**Deliverable.** Deployed on a free **CPU** Hugging Face Space (CP-SAT is
pip-installable and CPU-only; single-request small-model inference is fine on
CPU — no GPU needed). A short results panel.

**Metrics to report.**
- Parser exact-match and valid-constraint rate (held-out paraphrases).
- End-to-end solve rate (parser-only vs with self-refinement).
- Generation uniqueness rate (≈100% by construction — it's a sanity check).
- Round-trip faithfulness of rendered clues.
- Latency per solve / per generate.

**Background required.**
- HF Spaces deployment, `requirements.txt` pinning, CPU inference.
- Basic evaluation methodology and honest reporting.

**Material.**
- HF Spaces docs: https://huggingface.co/docs/hub/spaces

---

## Order & dependencies

```
M0 (done) ── M1 ── M2 ── M3 ─┐
                 └── M4 ──────┼── M6 ── M7
                  (M5 optional, after M2/M3, before M6)
```

M1 feeds both M2 (parser) and M4 (renderer, the inverse model). M3 needs M2.
M6 needs the core (M0), the parser (M2/M3), and the generator+renderer (M4).

## Risks & guardrails (recurring failure modes)
1. **Unconstrained phrasing.** Keep the clue grammar narrow; a small model is
   reliable only on the bounded language it was trained on.
2. **Trusting the model for coherence.** Generation must be symbolic-first with
   a round-trip parse check; never let the model guarantee uniqueness.
3. **Time sink.** The generator's seed→category mapping and uniqueness trimming
   have fiddly edge cases — budget buffer in M4.

## References
- Pan, Albalak, Wang, Wang. *Logic-LM.* Findings of EMNLP 2023.
  https://arxiv.org/abs/2305.12295
- Li, Huang, et al. *Scallop: A Language for Neurosymbolic Programming.*
  PLDI 2023. https://arxiv.org/abs/2304.04812
- Google OR-Tools CP-SAT.
  https://developers.google.com/optimization/cp/cp_solver
- HuggingFace Transformers. https://huggingface.co/docs/transformers
- Gradio. https://www.gradio.app/docs
