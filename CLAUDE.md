# CLAUDE.md

Rules for working in this repo, derived from failures that actually happened
here and from review feedback. Keep this lean — add a rule when something goes
wrong twice, not speculatively.

This file is authoritative. `README.md` carries a shorter, user-facing version
of the same workflow; where they disagree, this one wins, and a rule should be
stated in full in exactly one of them.

The repo keeps its own books in `docs/`: plans live in
[`docs/plans/`](docs/plans/) (see Step 0), and decisions — including review
findings that were considered and declined — live as numbered ADRs in
[`docs/adr/`](docs/adr/README.md). Check the ADRs before re-opening an
argument.

## The narrative: three levels of understanding

Every concept in this repo is built to climb the same three levels, in order:

1. **What is it saying?** — state the claim plainly, in objects the viewer can
   see and count.
2. **Why is it true?** — the argument. Not a proof; the reason the shape of the
   formula is forced. This is the part a scene should spend its time on.
3. **When is it useful?** — where the result shows up once you leave the
   example. Without this a scene teaches a fact instead of a tool.

A concept that stops after level 2 is **incomplete**, and that is the default
failure mode — level 2 is the satisfying part to build, so it is where scenes
stop. The formula arriving last is not the end of the narrative; the formula is
the top of level 2.

The levels apply to a concept, not necessarily to one scene: a module of four
scenes may reach level 3 only in its last. But the topic README's concepts
table has a column for each level, and a blank one is a gap in the teaching,
not a formatting problem.

## Step 0: plan before touching a file

Any topic, any concept, anything non-trivial starts with a written plan broken
into numbered **phases**, each ending in a **commit gate** — a named checkpoint
that must be green before the next phase begins. No phase starts on top of a
red one, and each gate is one commit.

**Plans are repo history, not scratch.** Every plan lives in `docs/plans/` as
`NNN-slug.md`, numbered in the order begun, and is committed with the work it
gates. The directory is the track record of how this platform grew — how a
topic was scoped, what the research found, and what was deliberately deferred
— so a plan is updated as its phases complete, not deleted when they do.

**A new series starts on a fresh branch cut from an updated `main`.** Check out
`main`, pull, then branch — never stack a topic on another feature branch. The
first topic branch here was nearly built on a stale scaffold branch while the
scaffold PR had already merged; only the pull caught it.

**Before designing any scenes, research how the material is best conveyed.**
Find the canonical explanations and what order they teach in, the visual
devices they rely on, the misconceptions learners actually report, and verify
the technical details against primary sources — an animation that is subtly
wrong is worse than no animation. The scene design in the plan states what it
borrows and from where, and every source consulted lands in the topic README's
References as `- [ ]`.

The research pass runs as two repo agents, defined in `.claude/agents/`:
`pedagogy-researcher` (how the material is best taught) and
`source-verifier` (the exact facts and numbers, verified against primary
sources and by computation). Their reports are pinned into the plan — the
scene design is built from them, and every on-screen number traces to the
verifier's report.

The final phase is always a fully rendered PR. A plan that stops at "code
works" is not finished.

A new topic looks like this:

| Phase | Work | Commit gate |
| --- | --- | --- |
| 0 | Fresh branch from pulled `main`; research pass on how to teach the material | Scene design written into the plan |
| 1 | Topic dir, README skeleton, first scene stub | `make check` |
| 2 | Scenes, iterated at draft quality | Draft renders verified by eye |
| 3 | Numbered concepts table, references as `- [ ]`; new topic → re-render `docs/assets/welcome.gif` (its topic row is hand-listed) | `make test` |
| 4 | Local CodeRabbit pass + `connection-auditor` pass, findings addressed | Review clean |
| 5 | PR, bot review, finalise | `clean-drafts` + 1080p render |

## Workflow: draft first, review before PR, finalise last

Never render at the default 1080p while iterating.

1. **Plan** — step 0 above.
2. **Iterate** at `--quality draft` (480p15). Fast enough to actually loop.
3. **Verify the render** — see below. "The file exists" is not verification.
4. **Run the CodeRabbit review locally, before opening the PR.** Use the
   `coderabbit:code-review` skill on the branch. This is not optional and it
   is not the same as the bot: catching findings here means the PR opens clean
   instead of accumulating review rounds. Address what it finds, then re-run.
5. **Open the PR.** The bot reviews it as an independent second pass.
6. **Address the bot review and finalise.**
7. **`make clean-drafts`, then render at the 1080p default.** The PR is only
   done once the final render exists.

`make clean-drafts` removes sub-1080p output and keeps finals; `make clean`
removes everything.

## Verifying anything

A render that produced a file is not a render that worked. Two failures here
both passed a naive existence check:

- Four scenes silently rendered into one file. Check the *count* and that the
  names differ.
- Use `ffprobe` for frame count and duration, and extract a frame with
  `ffmpeg` and actually look at it when layout or colour changed.

**Never judge a gate through a pipe.** This has bitten three times: `$?` after
a pipeline reports the *last* command's status, not the interesting one; a
`grep` filter over `make check` hid a failing format check and made a red gate
look green; and `make list` piped into `sed` swallowed a module that could not
even import. Run `make check` unfiltered and read the exit code. When a test
harness pipes, use `PIPESTATUS`.

Also verify the verification: when adding a test that is supposed to catch
something, break the thing on purpose, watch the test fail, then restore. Two
tests in this repo passed against code that was already correct and would have
passed against code that was not.

Extracted frames are **samples**, not proof: a text overlap lived entirely
between two sample points and only the maintainer's eyes caught it. When a
scene replaces text in place, extract frames *inside the transition window*,
not just at the beats before and after it.

## Manim gotchas found here

- **Global config leaks across renders.** On finishing, manim writes the output
  path back into the global `config["output_file"]`
  (`SceneFileWriter.print_file_ready_message`), and the next scene's
  `init_output_directories` prefers it over the scene name. Scope `tempconfig`
  **per scene**, never per batch. This is why `utils/render.py` looks the way
  it does; do not "simplify" it back.
- Manim re-exports numpy, so `np` resolves under `from manim import *`. A
  module that *uses* numpy imports it explicitly anyway. A module that does not
  must not — an unused `import numpy as np` fails ruff F401.
- Geometry magic numbers (coordinates, buffs, run_times) are normal here. Do
  not extract them into named constants.

## Colour discipline

This is what review caught, twice, so check it before writing a scene:

- Never hardcode a hex. Use `utils.theme`.
- Scaffolding — empty slots, ordinal labels, connective arrows — is `MUTED`,
  **not** manim's `GREY_B`.
- `ACCENT` result being built toward · `COOL` primary quantity · `WARM` what
  gets cancelled or overcounted · `GOOD` confirmed object · `MUTED`
  scaffolding.
- `PALETTE` / `palette(i)` is a *categorical* cycle for "N distinct things with
  no ranking". Using `COOL`/`WARM`/`GOOD` for arbitrary categories is wrong
  even when it renders identically — and it does render identically, since
  those three *are* `PALETTE[0:3]`.

## Motion discipline

- **Replaced text leaves before its replacement arrives.** `FadeOut` the old
  string, *then* `FadeIn` the new one — a simultaneous swap (or a
  `FadeTransform` between different strings) renders both on top of each
  other mid-crossfade. Raised watching the alignment-problem caption swaps.
- **Scene timings are written against manim's defaults.** `ConceptScene.play`
  stretches every animation to the repo's native pace (`PLAYBACK_SPEED` in
  `utils/scene.py`, 0.75× — the speed the videos were actually being watched
  at; player-side slowdown judders 60 fps output). Never compensate for the
  pace inside a scene, and never add a `wait` override to "complete" the
  mechanism: waits route through `play` and would stretch twice — the first
  draft shipped exactly that bug.

## The picture is a claim

Two lessons review keeps re-teaching, so check them before every scene:

- **Geometry carries the repo's grammar, so a frame can contradict the math
  on screen.** Straight perpendicular cuts *mean* independence here — a scene
  drew them while teaching dependence; and a biased-die equation computed for
  B = {1,2,3,4} sat under a bar showing {1,2,3}. Whenever an equation is on
  screen, ask what the picture next to it asserts under the repo's own
  conventions, and make them agree.
- **Prose describing a scene is checked against the built scene.** README
  table cells, plan design sections, and wiki edges have all claimed beats no
  scene contains ("both squares stay on screen", "the prior as column width",
  a foreshadowed teaser that was never built). When a phase closes, the
  design prose is updated to describe what was *built* — or the missing beat
  is built. A promise of a visual is either rendered or removed, never left
  standing.

## Structure

- Scenes subclass `ConceptScene`, never `Scene`. Never set
  `camera.background_color` by hand.
- Reuse `utils.mobjects` (`token`, `chip`, `boxed`, `header`, `caption`) rather
  than rebuilding them inline.
- Every scene needs a docstring whose first line is a summary — that line is
  what `--list` prints. More lines are welcome (ADR 004).
- No `SCENES = [...]` list. `render_cli()` discovers scenes in source order.
- No `sys.path` manipulation. The project installs itself as a package.
- A new public name in `utils/` has to be **imported into**
  `utils/__init__.py` *and* listed in `__all__`. These do different jobs: the
  import is what makes `from utils import X` resolve in a concept module,
  while `__all__` covers wildcard imports and keeps ruff quiet — F401 rejects
  a re-export that is not listed. Doing only one of the two fails.
- `from manim import *` is allowed **only** in `*/*_manim.py`. `utils/` imports
  explicitly.

## Sequence

Source order is viewing order. Renders are numbered from it
(`03_CombinationRule.mp4`), and the topic README's concepts table must list
scenes in the same order with matching numbers. `tests/test_topic_contract.py`
enforces this — reordering scenes means updating the README in the same change.

## The connection graph

[`docs/wiki/`](docs/wiki/README.md) is the repo's knowledge graph: nodes
are concepts taught or promised, edges are the links between them, each
marked delivered or promised with the place it is stated. Two rules:

- **A series updates the graph in the change that lands it** — its node,
  the promised edges it opens, the promised edges it closes. An edge
  nobody can cite is a wish, not a connection.
- **Run the `connection-auditor` agent before opening a series PR** and
  when choosing what to build next. It reports promised-but-missing,
  delivered-but-unrecorded, and possible-but-unmade connections; the
  graph is only useful while it matches the content.

The wiki stays repo-shaped: nodes are things the repo teaches or has
promised to teach, nothing broader.

## Topic contract

A new topic directory without a `README.md` is an incomplete change. It needs
Scope (including what is deliberately **not** covered), a numbered concepts
table, References, and Ideas not yet built.

**Never tick a reference checkbox.** `- [ ]` is unverified and is the default
for anything you suggest; only a human moves it to `- [x]`. Unverified entries
are a to-do, not a defect — leave them alone.

## Lint

`make check` runs ruff, pytest and the hooks. Bugbear rules that have bitten
here: `zip()` needs `strict=` (silent truncation in a file full of parallel
lists), `E741` ambiguous names, `B007` unused loop variables. A new entry in
`per-file-ignores` needs a comment saying why.

## Tests

Test the render logic and the topic contract. Do **not** write pixel or
frame-comparison tests — they fail on a font update without anything being
wrong.
