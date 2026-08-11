# CLAUDE.md

Rules for working in this repo, derived from failures that actually happened
here and from review feedback. Keep this lean — add a rule when something goes
wrong twice, not speculatively.

## Workflow: draft first, finalise last

Never render at the default 1080p while iterating. The loop is:

1. `--quality draft` (480p15) until the scene is right. Fast enough to iterate.
2. Verify the render — see below. "The file exists" is not verification.
3. Open a PR for the topic. Let CodeRabbit review it.
4. Address the review, finalise.
5. `make clean-drafts`, then render at the 1080p default.

`make clean-drafts` removes sub-1080p output and keeps finals; `make clean`
removes everything.

## Verifying a render

A render that produced a file is not a render that worked. Two failures here
both passed a naive existence check:

- Four scenes silently rendered into one file. Check the *count* and that the
  names differ.
- Use `ffprobe` for frame count and duration, and extract a frame with
  `ffmpeg` and actually look at it when layout or colour changed.

## Manim gotchas found here

- **Global config leaks across renders.** On finishing, manim writes the output
  path back into the global `config["output_file"]`
  (`SceneFileWriter.print_file_ready_message`), and the next scene's
  `init_output_directories` prefers it over the scene name. Scope `tempconfig`
  **per scene**, never per batch. This is why `utils/render.py` looks the way
  it does; do not "simplify" it back.
- Manim re-exports numpy, so `np` resolves under `from manim import *`. Import
  it explicitly anyway.
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

## Structure

- Scenes subclass `ConceptScene`, never `Scene`. Never set
  `camera.background_color` by hand.
- Reuse `utils.mobjects` (`token`, `chip`, `boxed`, `header`, `caption`) rather
  than rebuilding them inline.
- Every scene needs a one-line docstring — it is what `--list` prints.
- No `SCENES = [...]` list. `render_cli()` discovers scenes in source order.
- No `sys.path` manipulation. The project installs itself as a package.
- A new public name in `utils/` must be re-exported in `utils/__init__.py`'s
  `__all__`, or concept modules cannot see it.
- `from manim import *` is allowed **only** in `*/*_manim.py`. `utils/` imports
  explicitly.

## Sequence

Source order is viewing order. Renders are numbered from it
(`03_CombinationRule.mp4`), and the topic README's concepts table must list
scenes in the same order with matching numbers. `tests/test_topic_contract.py`
enforces this — reordering scenes means updating the README in the same change.

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
