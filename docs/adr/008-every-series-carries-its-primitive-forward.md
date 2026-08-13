# ADR 008: every series carries its study-guide primitive forward

Status: accepted — maintainer directive, 2026-08-12 (plan 012's
standing note, executed after v1 of the CTC guide merged in PR #13).

## Context

The study-guide track (plan 012) ships textbook companions built from
per-series primitive `.tex` sections, stitched into objective-named
guides with glue transitions authored from the wiki's edges. Guide 1
(`study_guides/ctc-algorithm/`) was built retroactively: all eleven
existing series plus three guide-first chapters, fitted after the
fact in one large pass. Retrofitting works once; as a standing mode
it recreates the debt each new series would leave behind — a video
series without its written companion is a chapter the next guide has
to reconstruct from cold.

## Decision

Stitching is standing process. **A new series is not finished until
its primitive is**, and the work nests into the series' own plan
rather than accumulating as a separate track:

- The Step-0 phase table (CLAUDE.md) gains the primitive in phase 3:
  alongside the concepts table and references, the series' plan
  authors (or updates) `study_guides/primitives/<series>.tex` — the
  narrative retold from the scenes, problems with hints and
  solutions single-sourced, the answer script committed, and the
  chapter's anchors added to `anchors.yaml` citing the plan's own
  pinned verification report (the report exists by then; the
  anchors are a transcription of it, never fresh claims).
- The problems pass the independent solve gate (a fresh-context
  solver, statements only) before the phase closes — the same gate
  v1's fifty-eight problems passed.
- Guides that should retrieve the new primitive update their
  manifests and glue in the same change; the glue is authored from
  the wiki edges the series just landed, so the transition and the
  graph row cite the same connection.
- Guide-first primitives (chapters with no parent series — DP,
  gradient descent, decoding are the precedents) remain legitimate
  and double as phase-0 seed material when their video series is
  eventually built: the book drafts what the screen later animates.
- Past topics are already retrofitted — v1 was the retrofit; no
  further catch-up pass is owed.

## Consequences

- The plan template's phase 3 grows one deliverable; its gate
  (`make test`) already covers the study contract's structure tests,
  and `make study` covers the build and figure linter.
- The wiki stays screen-shaped (its scope boundary says so): print
  deliveries are recorded in plans, and a primitive never satisfies
  a wiki promise on its own — scenes do.
- The refinement loop (`REFINEMENTS.md` per guide) runs for each
  document's life, independent of any series plan.
- Still open, tracked in plan 012: the digit-literal lint's scoping
  rule (the maintainer's call).
