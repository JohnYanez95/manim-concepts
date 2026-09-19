# ADR 010: study-guide work waits for an explicit request

Status: accepted — maintainer directive, 2026-09-19 (given on plan 019's
branch, before its PR). Suspends ADR 008's standing process; reverses
none of what was built under it.

## Context

ADR 008 made the study-guide primitive a standing phase-3 deliverable: a
series was not finished until its written chapter, solve-gated problems,
answer script and anchors were. Sixteen primitives and two guides exist
under that rule — the last of them plan 019's `spectrum` chapter and the
`air-to-log-mel` objective, which the maintainer had approved that
morning and which were already built and verified when this directive
arrived.

The primitive is the most expensive single deliverable in a series'
phase 3: a chapter, a figure set, six to eight problems, an answer
script, an independent solve gate and a LaTeX build. The repo is a space
for expanding on the questions the maintainer is working through; the
written companion is worth that cost when he wants one, and not as a
toll on every series.

## Decision

Study-guide work happens **when the maintainer asks for it explicitly**,
and not otherwise:

- A series' phase 3 no longer includes a primitive, problems, an answer
  script, anchors in `anchors.yaml`, guide manifests or glue. A plan
  lists them only when the maintainer has asked for them for that
  series.
- Nothing is proposed either: plans, audits and PR descriptions do not
  raise a missing primitive as a gap, a debt or a to-do. A series with no
  chapter is complete.
- What exists stays: both guides, every primitive, the tests in
  `tests/test_study_contract.py`, `make study`, the reference sync, and
  each guide's `REFINEMENTS.md` loop. They are maintained when touched —
  a README reference change still re-syncs `references.bib`, because the
  sync test runs for every change.
- The verifier's pinned anchors stay in each plan as before — they serve
  the scenes first. They are transcribed into `anchors.yaml` only when a
  chapter is requested.
- When a chapter *is* requested, ADR 008's method applies unchanged:
  narrative retold from the built scenes, problems single-sourced with
  solutions, the committed answer script, plan-cited anchors, the
  independent solve gate, glue authored from the wiki's edges.

## Consequences

- `air-to-log-mel` may stay a one-chapter guide while the road's later
  series (convolution, the short-time transform, mel) land without
  chapters; its front matter says its stations are written when asked
  for, not "with their series".
- Guide-first chapters and retrofits are likewise on request only.
- ADR 008's status line records the suspension; CLAUDE.md's phase-3 row
  drops the deliverable and points here.
