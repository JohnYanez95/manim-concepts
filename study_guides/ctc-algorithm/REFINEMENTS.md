# Refinements — the CTC algorithm guide

The reader-feedback loop (plan 012): where the guide loses you, add one
dated bullet saying what didn't land; the agent applies a refinement and
ticks the bullet with what changed. This file lives for the document's
life, not just its first PR.

- [x] 2026-08-12 (maintainer): the roadmap's arrows overlap — the
  row-break arrow from logarithms sweeps across the whole second row,
  reading as a loop through decoding/gradient/descent/dyn. prog. on its
  way to e & ln. **Applied**: the roadmap is now serpentine — row two
  runs right-to-left, e & ln sits directly under logarithms, and the
  row break is a short vertical hop; no arrow crosses a station.
- [x] 2026-08-12 (maintainer): the 1.1 outer-product grid has an odd
  collision, and TikZ imagery needs guardrails generally. **Applied**:
  the grid's missing right rule restored and both labels moved clear;
  and `tools/check_study_layout.py` now standalone-renders every TikZ
  figure (plus macro-generated ones) and measures two checks —
  text-overlaps-text and ink-crowds-text-halo — wired into
  `make study` as a gate. Verified the verification: the pre-fix
  figure trips the linter; the fixed one passes.
