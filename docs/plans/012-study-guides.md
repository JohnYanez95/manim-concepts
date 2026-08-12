# Plan 012: study guides — the written companion track

Branch: `feat/study-guides`, cut from updated `main` (the plan-011
merge). Started: 2026-08-12.

The maintainer's directive (2026-08-12): beyond the rendered videos,
each topic gets a written study companion — a textbook-style
write-up with practice problems, LaTeX-rendered visuals, proper
sourcing per document — enabling a larger offline narrative and
independent study. Refined the same day: **section breakdown, think
textbook setup** — build the *primitive* of each topic and *stitch*
primitives toward a specific objective, with *glue transitions for
horizon viewing*; practice problems at the end of each section; a
**separate solutions manual**; and a reader-feedback loop — where
something doesn't make sense from the user's perspective, the reader
inputs what needs refinement.

This is a design proposal. **Phase 0's gate is the maintainer's
approval of the design**; nothing below it builds until then.

## The design

### The mapping the repo already gives us

The repo is already shaped like this book. A **primitive** is one
series (eleven exist); the **glue** is the wiki's edge table — every
delivered edge is a transition sentence waiting to be written in
prose; a **guide** is a walk through the connection graph toward an
objective. The narrative rule (plan 011) carries over verbatim:
section bodies ground backward in earlier sections; forward pointers
live in each section's closing "where this goes" notes — which is
exactly what makes the glue transitions and the horizon view work.

### Directory and build (maintainer-specified, 2026-08-12)

*(Design sketch — the as-built structure differs in details the later
checklists record: problems live inside primitives per R2, glue files
are numbered `glue-NN.tex`, and guide-owned macros sit in `macros.tex`;
build from the checklist, not this sketch.)*

One `study_guides/` directory; **one subdirectory per objective —
the subdirectory's name IS the objective**; each objective
subdirectory holds the outcome pair: the stitched guide PDF
(reading material + end-of-section practice problems) and the
solutions manual as the secondary PDF beside it.

```text
study_guides/
  theme.sty              -- palette + type mirroring utils/theme.py
  primitives/            -- one .tex per series, self-contained
    counting-rules.tex
    ctc-alignment.tex
    ...
  ctc-algorithm/         -- objective subdirectory (guide 1)
    guide.tex            -- declares its primitive retrievals, in
                         -- order, via \primitive{...}; the build
                         -- constructs the glue document from them
    glue.tex             -- roadmap figure + transition pages
    problems.tex         -- per-section problem sets (input by guide)
    solutions.tex        -- the solutions manual source
    REFINEMENTS.md       -- the reader-feedback loop
    ctc-algorithm.pdf            -- outcome, primary
    ctc-algorithm-solutions.pdf  -- outcome, secondary
```

- **Retrieval model**: primitives are hosted once in
  `primitives/*.tex`; a guide *retrieves* them — `guide.tex`'s
  ordered `\primitive{counting-rules}` … calls are the manifest, and
  the build resolves each to its hosted file, interleaving the glue.
  One primitive, many guides; edits propagate to every guide that
  retrieves it.
- `make study` builds every objective subdirectory's two PDFs into
  that subdirectory. LaTeX stays OUT of `make check` (toolchain
  weight); a lightweight pytest module
  (`tests/test_study_contract.py`) checks structure only: every
  primitive has the required blocks, every `\primitive{}` retrieval
  resolves to a hosted file, every problem has exactly one solution
  in the manual, references start `- [ ]`.
- The outcome PDFs live in the objective subdirectory per the
  maintainer's spec. Whether they are also *committed* is the one
  open sliver of D-A: the large-file hook caps additions at 512 KB
  and a full guide will exceed it, so committing means a hook
  exemption for `study_guides/**/*.pdf`. Proposal: commit them —
  the offline grab-and-go is the point of the track — with the
  exemption commented in the hook config.

### Anatomy of a primitive (one series → one textbook section)

1. **Narrative** — the series' three-level arc as prose: what it
   says (countable objects), why it is true (the argument, the
   scenes' own devices described), when it is useful. Written from
   the scenes and their plans, not from scratch — the prose cites
   the scene it retells, so the picture-is-a-claim rule has teeth
   here too.
2. **Figures** — TikZ/pgfplots redraws of the repo's owned devices
   (the trellis, the softmax bars, the unit square, the counting
   strip) in `theme.sty` colours, so print and video speak one
   visual language. Extracted video frames are an optional garnish
   behind a build step (`tools/extract_frames.py`, reading the
   1080p finals), never committed binaries. (Decision point D-B.)
3. **Worked examples** — the repo's own verified numbers (the AB
   trellis, the 0.4877 matrix, the aces, the biased die), each
   traceable to a plan anchor by citation.
4. **Practice problems** — at the end of the section, graded
   easy → stretch, numbered `<section>.<n>`. Problem *answers are
   never in the guide*; every problem's full worked solution appears
   in the solutions manual, keyed by the same, globally-complete
   number. **Single-sourced** (research addendum, R2): statement,
   hint, and solution live adjacent in ONE problem environment
   inside the primitive; the guide build suppresses solutions, the
   manual build emits them — there is no hand-maintained parallel
   solutions file to rot. The separate solutions-manual *PDF* (the
   maintainer's spec) is a build target, not a second source.
5. **Sources** — a per-document bibliography; entries land
   unchecked (`- [ ]`) and are human-gated exactly like the topic
   READMEs. New numbers not covered by an existing plan anchor
   trigger a source-verifier supplement pass before they print.
6. **Where this goes** — the section's closing notes: the delivered
   wiki edges out of this node, written as horizon pointers.

### The glue, and horizon viewing

Each guide opens with a **roadmap figure**: the wiki subgraph for
its objective drawn as a TikZ road — the reader sees the whole
horizon before section one. Between stitched primitives sits a
**transition page**: what was just built (the blocks now owned),
why the next section needs exactly those blocks, and where the road
now stands on the roadmap (the figure repeats, progress marked).
The transitions are authored from the wiki edge citations — an edge
nobody can cite still doesn't get written.

### Guide 1: `study_guides/ctc-algorithm/`

Objective: **full comprehension of CTC** — the alignment machinery,
the loss, and the gradient. Stitching order = the build order, which
is already the dependency order:

counting-rules → ctc-alignment (the problem, posed) → independence →
conditional-probability → bayes-rule → logarithms → e-and-ln →
random-variables → softmax-likelihood → derivative-toolkit →
ctc-gradient (the objective, landed).

All eleven series primitives — **plus two guide-first primitives the
video road never built**, both required for full comprehension of
the *learning algorithm* (maintainer, 2026-08-12):

- **`dynamic-programming.tex`** — the trellis scenes perform DP
  without naming it. This is the wiki's standing promised row
  (`ctc-alignment` → *(dynamic programming as its own concept)*),
  which already carries two recorded anchors: the log-space
  inheritance (`TheUnderflowCliff`) and the constant column as LOTP
  over the frame partition (`PathsThroughACell`). The primitive
  teaches the general move — overlapping subproblems, shared
  prefixes, the exponential sum reorganised — with the CTC trellis
  as its worked instance. Candidate slot: immediately after the
  ctc-alignment section, while the trellis is fresh (exact slot a
  phase-2 glue decision).
- **`gradient-descent.tex`** — the training-dynamics scenes run
  plain GD on screen ("plain gradient descent", named) without
  teaching descent. A short primitive — walk downhill, the learning
  rate, why the gradient's zero is the stopping story (the
  sign-change ribbon's habit) — slotted after derivative-toolkit and
  before ctc-gradient, so the error-signal trajectories land on
  taught ground. Lends itself to the guide's descent figure
  (the loss walk 0.7181 → … → 0.0003 as a downhill path).

- **`ctc-decoding.tex`** — the road uses decoding everywhere without
  teaching it (`ManyPathsOneWord` proves greedy fails; scene 6 reads
  an argmax path; scene 7's bias model decodes to the empty string).
  A modest primitive slotted after ctc-gradient, closing the loop
  (train → decode → deploy): best-path decoding, the sum-vs-max
  mismatch as a *decoding* problem, the collapsed-prefix beam sketch
  with its two-probabilities insight, spikes-not-timestamps
  inherited. Depth stays with the future beam-search series — this
  primitive seeds it.

Guide-first primitives follow every rule series primitives do
(anchored numbers, human-gated sources, backward grounding) but have
no parent scenes — their prose cites the scenes that *use* the
concept. Each doubles as phase-0 seed material for the eventual
video series (the DP series is already the roadmap's ungated
flexible insert), inverting the usual pipeline: the book drafts what
the screen later animates. The wiki stays screen-shaped — the DP
promise row stays promised until scenes exist; the plan records the
print delivery here.

The guide's frame story: the CTC sections pose
the problem early, the middle sections build the
blocks — now including the two the videos skipped — and the closing
sections spend them: the same shape the video road took, now
walkable offline in one sitting.

### The refinement loop

The reader is the review of record.
`study_guides/ctc-algorithm/REFINEMENTS.md`
holds maintainer inputs — "section 4's transition lost me",
"problem 7.3 assumes something unstated" — one dated bullet each;
the agent applies them and ticks the bullet with what changed.
Refinement rounds are cheap (LaTeX rebuild, no renders); the loop
runs for the document's life, not just its first PR.

### Verification and process rules carried over

- Every printed number traces to a verifier anchor (existing plan
  anchors reused by citation; new ones via supplement passes).
- References human-gated; ticks are the maintainer's.
- The narrative rule applies to section bodies; forward pointers
  only in transitions and "where this goes".
- Solutions manual entries are complete worked solutions (the
  reasoning, not just the answer) — they follow the same three-level
  discipline: state, derive, situate.

## Research addendum (two outside-perspective passes, 2026-08-12)

Two agents surveyed (1) agentic course-material pipelines and (2)
retrieval/single-sourcing architectures; full reports pinned in this
plan's history. What changes the design:

- **R1 — IDs, never retyped content (adopted; the retrieval
  optimization the maintainer asked about).** The universal agent
  contract becomes: emit stable IDs, let the build splice canonical
  text — `\primitive{name}` for sections, **`\anchor{plan.letter}`
  for every verified number**, `\cite{key}` for sources. Mechanism:
  `study_guides/anchors.yaml` (plan → anchor letter → exact values
  as strings + source + method, generated from the plan docs' pinned
  reports) compiles to `anchors.tex` macros; a digit-literal lint
  flags any number in guide prose that didn't come through an
  `\anchor` — the transcription step, deleted. (Deterministic-
  quoting pattern — Yeung; showyourwork's `\variable{}`; Quarto's
  computed-inline-values guidance. Table-QA error analyses show LLM
  numeric errors are dominated by grabbing the wrong nearby number,
  so the disambiguated key is the load-bearing part.)
- **R2 — statement+solution single-sourced, build-flag split
  (adopted).** PreTeXt's architecture, expressed in ~30 lines of
  LaTeX: one problem environment carries statement/hint/solution;
  two build targets emit guide vs manual. Evidence for never
  hand-maintaining a parallel solutions file: GSM-HARD's
  statement/answer divergence (25 of 50 audited "model errors" were
  label errors) and GSM8K's Platinum relabel.
- **R3 — independent-solve gate on every problem (adopted;
  upgrades D-D).** Each problem's answer is computed by a
  SymPy/NumPy script committed beside the primitive — the script IS
  the problem's anchor — and a fresh-context solver agent (never
  shown the authoring transcript) must independently agree before
  the problem ships. AutoCode measured the base rate this gate
  exists for: ~1 in 7 unverified LLM reference solutions wrong;
  dual verification lifted correctness 86% → 94%. Classic
  textbook-standard problems get perturbed parameters (recomputed
  anchors) to defeat solver memorization.
- **R4 — primitives carry no assembly-owned state (adopted).**
  Numbering, labels and cross-primitive references belong to the
  guide; any cross-primitive pointer goes through a per-guide macro
  layer (`\primref{node}`), never a hardcoded `\ref` inside a
  primitive — DITA's keyref pattern, which is what keeps one
  primitive serving many guides without `??`s.
- **R5 — bibliography single-sourcing (adopted).** The human-ticked
  markdown reference lists remain the source of truth (the
  never-tick rule untouched); a repo script syncs them into one
  `references.bib` carrying a `verified` field; biblatex prints
  per-document bibliographies from citations alone; `checkcites`
  joins the checks; the sync script refuses a build citing an
  unverified entry that isn't marked as such.
- **R6 — remix map formalized (adopted, cheap).** Each guide opens
  (in source) with the objective → primitives → justifying-wiki-edge
  table; ambiguous orderings are flagged to the maintainer, not
  guessed — LibreTexts' remix-map practice, and the repo's own
  "an edge nobody can cite is a wish" rule.
- **R7 — curated agent index (adopted).** `study_guides/INDEX.md`
  maps node → primitive file → its anchors → its bib keys, so
  authoring agents resolve IDs without crawling.
- **Avoided, deliberately**: toolchain migration to
  PreTeXt/DITA/Quarto (their architectures are borrowed above; the
  LaTeX+git+existing-agent stack keeps diffs and review native);
  LLM-judge as a sole quality gate (that bar produced training
  data, not reader-facing text); prose generated unanchored from
  the verified series content (the Learn-Your-Way lesson: the
  human-verified artifact is the invariant, generation is
  constrained transformation).

## Decision points for the maintainer

- **D-A — RESOLVED in structure** (outcome PDFs live in the
  objective subdirectory; maintainer-specified). Open sliver:
  commit them too? Proposal: yes, with a large-file-hook exemption
  for `study_guides/**/*.pdf`.
- **D-B — TikZ redraws vs extracted video frames.** Proposal: TikZ
  first (crisp in print, theme-consistent, no binaries); frames as
  optional garnish behind the build step. Reverse if fidelity to
  the videos matters more.
- **D-C — first-PR scope.** Proposal: scaffold + the first TWO
  primitives (counting-rules, ctc-alignment) + their problem sets,
  solutions manual started, roadmap figure drafted — a calibration
  PR so the format gets maintainer eyes before nine more sections
  inherit it.
- **D-D — problem verification depth.** Upgraded by R3: every
  problem gets a committed answer script (the problem's anchor) plus
  an independent fresh-context solve; per-batch source-verifier
  supplements cover narrative numbers not already anchored.
- **D-E — guide-first primitives** (dynamic-programming,
  gradient-descent, ctc-decoding). Proposal: yes, all three — they
  are what "full comprehension of the learning algorithm" requires,
  and each seeds its eventual video series. All three get the full
  research treatment (pedagogy + verifier passes) since no plan
  anchors exist for them yet.

## Phases

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | This design; decision points resolved | **Maintainer approves the design** |
| 1 | Scaffold: `study/` tree, `theme.sty`, `make study`, structure tests, skeleton primitive | `make check` + both PDFs build |
| 2 | Calibration content (per D-C): two primitives, problems, solutions manual, roadmap | `make study` green + maintainer format read |
| 3 | Local CodeRabbit + connection-auditor (prose-vs-scene, edge-vs-transition), findings addressed | Review clean |
| 4 | PR, bot review, finalise | Merge; refinement loop opens |

Then batches: the remaining nine primitives land in 2–3 further PRs
(probability trio · logs/e-ln/random-variables · softmax/derivatives/
gradient + final glue), each with the same gates, each extending the
solutions manual, until guide 1 assembles complete.

## Checklist

- [x] Phase 0: design approved as proposed, 2026-08-12 — D-A
  (outcome PDFs in the objective subdirectory AND committed, with a
  large-file-hook exemption), D-B (TikZ-first), D-C (calibration
  PR), D-D (as upgraded by R3), D-E (all THREE guide-first
  primitives: dynamic-programming, gradient-descent, ctc-decoding),
  plus research amendments R1–R7. Standing process note from the
  maintainer: once v1 of the guide ships, codify the stitching
  practice as an **ADR** — every new series carries its primitive
  forward as part of its plan, and past topics are retroactively
  fitted (guide 1's full sweep is that retrofit)
- [x] Phase 1: scaffold complete — `study_guides/` tree (`theme.sty`
  with the palette mirrored from `utils/theme.py`, the three
  retrieval contracts, and the single-sourced problem environments),
  `anchors.yaml` → `anchors.tex` (4 seed anchors from plans 009/010)
  and the README-synced `references.bib` (128 entries, 128 verified)
  with their generator scripts, the `ctc-algorithm/` objective
  subdirectory (guide + solutions wrappers sharing one
  `manifest.tex`, REFINEMENTS.md), the agent index, a skeleton
  counting-rules primitive with one calibration-placeholder problem,
  `make study`, eight structure tests, hook exemption for the
  committed outcome PDFs. Gate green: `make check` passes and both
  PDFs build; filtering verified both ways (guide shows hint not
  solution, manual shows solution not hint or narrative; numbering
  identical by shared manifest; the anchor splice renders
  P(AB|X) = 0.4877 from the yaml, never typed in prose)
- [x] Phase 2 (build side): the two calibration primitives authored
  in full — counting-rules (five-scene narrative, the TikZ
  outer-product grid, five problems) and ctc-alignment (six-scene
  narrative with the declared per-frame-score debt stated in prose,
  the TikZ unit-weight trellis landing 10 + 5 = 15 on plan 001's
  columns, five problems including the greedy-fails construction);
  glue-01 (the counting → alignment transition authored from the
  wiki edge) and the fourteen-station roadmap figure with progress
  marking; four new anchors (001.raw81, 001.paths15,
  001.astronomical, 010.N.t5paths) spliced via \anchor{}; answer
  scripts committed with enumeration asserted against every formula
  (plan 012 R3); **the independent solve gate passed 10/10** — a
  fresh-context agent given statements only reproduced every answer,
  including the 0.36-vs-0.64 greedy construction. `make check` and
  `make study` green; guide 12 pp + solutions manual verified by
  page (numbering shared, narrative and hints suppressed in the
  manual, zero solution leakage into the guide).
  Format read APPROVED 2026-08-12, with two refinements through the
  loop (both ticked in REFINEMENTS.md): the roadmap made serpentine,
  and the 1.1 grid trued — the latter spawning
  `tools/check_study_layout.py`, the print analogue of the scene
  linter (standalone-renders every TikZ figure incl. macro-generated
  states; text-overlap + ink-crowds-halo checks; gated in
  `make study`; verified by planting the broken figure and watching
  it flag)
- [x] Phase 3: local CodeRabbit returned nine findings, all applied
  (the glue's hardcoded 15/81 now anchor-spliced; the URL regex and
  LaTeX-escaping in the reference sync hardened and the bib
  regenerated; the linter now inherits the environment with timeouts;
  the sync test renders in memory; three doc drifts trued; the hook
  exemption narrowed to objective subdirectories). Audit: 13 findings
  applied — the top one built out **per-document sourcing** (biblatex
  in theme.sty, \cite calls in both primitives, \printbibliography in
  the guide, checkcites in `make study`) — plus the §5
  prose-vs-scene fix (the primitive attributed to `WhenToUseIt` the
  exact phrasing its code comment rejects; trued in the primitive AND
  the combinatorics README cell that seeded it), the root README's
  study-track paragraph + `make study` row, the wiki README's
  screen-shaped boundary line, the INDEX's reserved-anchor and
  underscore notes, the walker's-lattice pre-draft recorded on the
  combinatorics fifth-shape Ideas bullet, and the as-built note on
  the design sketch. **Open maintainer call (audit PND-2): R1's
  digit-literal lint needs scoping** — primitives legitimately carry
  small pedagogical digits (3 × 4 = 12), so the lint needs a rule
  (e.g. flag only ≥4-significant-digit literals, or only digits that
  match an anchored value) before "the transcription step, deleted"
  can be claimed; deferred to the next batch with John's pick
- [ ] Phase 4: PR, merge, refinement loop open
