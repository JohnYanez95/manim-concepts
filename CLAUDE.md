# CLAUDE.md

Rules for working in this repo, derived from failures that actually happened
here. Keep this lean — add a rule when something goes wrong twice, not
speculatively. This file is authoritative; `README.md` carries the shorter
user-facing workflow, each rule stated in full in exactly one of the two.

Repo bookkeeping lives in `docs/`: plans in [`docs/plans/`](docs/plans/)
(see Step 0), decisions — including review findings considered and declined —
as numbered ADRs in [`docs/adr/`](docs/adr/README.md). Check the ADRs before
re-opening an argument.

## The narrative: three levels of understanding

Every concept climbs, in order: **1. What is it saying?** (the claim, in
objects the viewer can count) → **2. Why is it true?** (the argument — not a
proof, the reason the formula's shape is forced; where a scene spends its
time) → **3. When is it useful?** (where the result shows up beyond the
example). Stopping after level 2 is the default failure mode — it is the
satisfying part to build — and it teaches a fact instead of a tool. The
formula arriving last is the top of level 2, not the end.

The levels apply to a concept, not necessarily one scene: a module may reach
level 3 only in its last scene. But the topic README's concepts table has a
column per level, and a blank cell is a teaching gap, not a formatting one.

## Step 0: plan before touching a file

Anything non-trivial starts with a written plan in `docs/plans/NNN-slug.md`,
broken into numbered **phases**, each ending in a **commit gate** that must be
green before the next phase begins — one commit per gate, no phase on top of a
red one. Plans are repo history, not scratch: committed with the work they
gate, updated as phases complete, never deleted.

- **Fresh branch from pulled `main`** — never stack a topic on another
  feature branch (a stale scaffold branch nearly got built on once; only the
  pull caught it).
- **Research before scene design.** Two repo agents (`.claude/agents/`):
  `pedagogy-researcher` (how the material is best taught) and
  `source-verifier` (exact facts and numbers, against primary sources and by
  computation). Their reports are pinned into the plan; the scene design is
  built from them; **every on-screen number traces to the verifier's
  report**; every source consulted lands in the topic README's References
  as `- [ ]`.
- **The final phase is always a fully rendered PR.** "Code works" is not
  finished.

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research pass | Scene design written into the plan |
| 1 | Topic dir, README skeleton, first scene stub | `make check` |
| 2 | Scenes, iterated at draft quality | Layout linter clean + drafts verified by eye |
| 3 | Numbered concepts table, references as `- [ ]`; new series → re-render `docs/assets/welcome.gif` (its series row is hand-listed) | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p render |

## Workflow: draft first, review before PR, finalise last

Never render at the default 1080p while iterating.

Plan (Step 0) → iterate at `--quality draft` (480p15) → verify the render
(see below; "the file exists" is not verification) → **local CodeRabbit
review before the PR** (`coderabbit:code-review` skill on the branch — not
optional, and not the same as the bot) → open the PR, the bot as independent
second pass → address the bot review, finalise → `make clean-drafts`, then
render at the 1080p default — the PR is only done once the final render
exists. (`clean-drafts` keeps finals; `make clean` removes everything.)

## Verifying anything

A render that produced a file is not a render that worked:

- Check the file *count* and that names differ (four scenes once rendered
  silently into one file). `ffprobe` for frames and duration; extract frames
  with `ffmpeg` and look at them when layout or colour changed.
- Extracted frames are **samples**, not proof — a text overlap once lived
  entirely between two sample points. When a scene replaces text in place,
  extract frames *inside the transition window* too.
- **Never judge a gate through a pipe** (bitten three times: `$?` after a
  pipeline, a `grep` over `make check` hiding a red format check, `make
  list | sed` swallowing an unimportable module). Run `make check`
  unfiltered and read the exit code; in a harness that pipes, use
  `PIPESTATUS`.
- **Verify the verification**: break the thing on purpose, watch the new
  test fail, restore. Two tests here passed against code that was already
  correct and would have passed against broken code too.

## Layout discipline

Two collisions shipped to the maintainer (a caption overlapping a formula, a
bar grazing a caption) plus a round of edge-clipped captions — one root
cause: text placed by *estimated* width, and the estimates ran low.

- **Never budget text width by eye.** `caption`/SMALL_SIZE runs ≈ 0.16
  scene units per character, BODY_SIZE ≈ 0.21. A side column centered at
  |x| ≈ 3.5 holds ~35 characters per line; longer lines go *under* the
  figure at centered x, not beside it.
- **Guard far-from-center text at construction**: `utils.on_frame` (shift
  minimally back inside the frame) and `utils.clear_of` (nudge one box off
  another) on any caption centered beyond |x| ≈ 2.5. They are guards, not a
  layout engine — needing a big correction means the design is wrong.
- **Run `uv run python tools/check_layout.py <module>` before the draft
  render.** It dry-runs each scene and reports, at every hold: text–text
  overlaps, text at the frame edge, shapes crossing text — measured
  geometry, not pixels, so font updates don't break it; both shipped
  collisions reproduce under it. Phase-2 gate: findings all fixed or
  explained, *then* frames verified by eye. The linter catches what eyes
  skim; it replaces neither the render nor the eyes.

## Manim gotchas found here

- **Global config leaks across renders**: manim writes the finished output
  path back into global `config["output_file"]`, and the next scene's
  `init_output_directories` prefers it over the scene name. Scope
  `tempconfig` **per scene**, never per batch — this is why
  `utils/render.py` looks the way it does; do not "simplify" it back.
- Manim re-exports numpy, so `np` resolves under `from manim import *`. A
  module that uses numpy imports it explicitly; one that doesn't must not
  (unused `import numpy as np` fails ruff F401).
- Geometry magic numbers (coordinates, buffs, run_times) are normal here; do
  not extract them into named constants.

## Colour discipline

Review caught this twice — check before writing a scene:

- Never hardcode a hex; use `utils.theme`. Scaffolding is `MUTED`, **not**
  manim's `GREY_B`.
- `ACCENT` result being built toward · `COOL` primary quantity · `WARM`
  cancelled/overcounted · `GOOD` confirmed object · `MUTED` scaffolding.
- `PALETTE` / `palette(i)` is the *categorical* cycle for "N distinct things,
  no ranking". Using `COOL`/`WARM`/`GOOD` for arbitrary categories is wrong
  even though it renders identically (those three *are* `PALETTE[0:3]`).

## Motion discipline

- **Replaced text leaves before its replacement arrives**: `FadeOut` the old
  string, *then* `FadeIn` the new — a simultaneous swap or `FadeTransform`
  between different strings renders both on top of each other mid-crossfade.
- **Scene timings are written against manim's defaults.** `ConceptScene.play`
  stretches everything to the repo's native pace (`PLAYBACK_SPEED`, 0.75×,
  in `utils/scene.py`). Never compensate for the pace inside a scene, and
  never add a `wait` override — waits route through `play` and would stretch
  twice (the first draft shipped exactly that bug).

## The picture is a claim

- **Geometry carries the repo's grammar.** Straight perpendicular cuts
  *mean* independence here — a scene once drew them while teaching
  dependence; a biased-die equation for B = {1,2,3,4} sat under a bar
  showing {1,2,3}. Whenever an equation is on screen, ask what the picture
  next to it asserts under the repo's conventions, and make them agree.
- **Prose describing a scene is checked against the built scene.** README
  cells, plan design sections and wiki edges have all claimed beats no scene
  contains. When a phase closes, the prose is updated to describe what was
  *built* — or the missing beat is built. A promised visual is rendered or
  removed, never left standing.

## Structure

- Scenes subclass `ConceptScene`, never `Scene`; never set
  `camera.background_color` by hand.
- Reuse `utils.mobjects` (`token`, `chip`, `boxed`, `header`, `caption`)
  rather than rebuilding inline.
- Every scene needs a docstring; its first line is what `--list` prints
  (ADR 004). No `SCENES = [...]` list — `render_cli()` discovers scenes in
  source order. No `sys.path` manipulation; the project installs itself.
- A new public name in `utils/` must be **imported into**
  `utils/__init__.py` *and* listed in `__all__` — the import makes
  `from utils import X` resolve, `__all__` covers wildcards and F401; doing
  only one fails.
- `from manim import *` is allowed **only** in `*/*_manim.py`; `utils/`
  imports explicitly.

## Sequence

Source order is viewing order: renders are numbered from it
(`03_CombinationRule.mp4`) and the README concepts table must match order and
numbers — `tests/test_topic_contract.py` enforces it, so reordering scenes
means updating the README in the same change.

## The connection graph

[`docs/wiki/`](docs/wiki/README.md) is the repo's knowledge graph: nodes are
concepts taught or promised, edges marked delivered or promised with the
place each is stated — an edge nobody can cite is a wish. A series updates
the graph in the change that lands it (its node, the promised edges it opens
and closes). Run the `connection-auditor` agent before a series PR and when
choosing what to build next. The wiki stays repo-shaped: nothing broader than
what the repo teaches or has promised.

## Topic contract

A topic directory needs a `README.md` with Scope (including what is
deliberately **not** covered), a numbered concepts table, References, and
Ideas not yet built. **Never tick a reference checkbox** — `- [ ]` is the
default for anything you add; only a human moves it to `- [x]`, and unticked
entries are a to-do, not a defect.

## Lint and tests

`make check` runs ruff, pytest and the hooks. Bugbear rules that have bitten:
`zip()` needs `strict=`, `E741`, `B007`. A new `per-file-ignores` entry needs
a comment saying why. Test the render logic and the topic contract; do
**not** write pixel or frame-comparison tests — they fail on a font update
without anything being wrong. (The layout linter is a gate tool, not a test:
it checks geometry, not pixels.)
