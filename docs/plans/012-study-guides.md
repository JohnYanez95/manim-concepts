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
   never in the guide*; every problem's full worked solution lives
   in the solutions manual, keyed by the same number.
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

The reader is the review of record. `study/guides/ctc/REFINEMENTS.md`
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
- **D-D — problem verification depth.** Proposal: problems reusing
  plan-anchor numbers cite them; problems with fresh numbers get a
  per-batch source-verifier supplement (one agent pass per PR, not
  per problem).
- **D-E — guide-first primitives** (dynamic-programming,
  gradient-descent). Proposal: yes, both — they are what "full
  comprehension of the learning algorithm" requires, and each seeds
  its eventual video series. Both get the full research treatment
  (pedagogy + verifier passes) since no plan anchors exist for them
  yet.

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

- [ ] Phase 0: design approved; D-A..D-D resolved
- [ ] Phase 1: scaffold, `make check` + PDFs build
- [ ] Phase 2: calibration content, maintainer format read
- [ ] Phase 3: reviews clean
- [ ] Phase 4: PR, merge, refinement loop open
