# CLAUDE.md

Rules for working in this repo, derived from failures that actually happened
here and from review feedback. Keep this lean — add a rule when something goes
wrong twice, not speculatively.

## Step 0: plan before touching a file

Any topic, any concept, anything non-trivial starts with a written plan broken
into numbered **phases**, each ending in a **commit gate** — a named checkpoint
that must be green before the next phase begins. No phase starts on top of a
red one, and each gate is one commit.

The final phase is always a fully rendered PR. A plan that stops at "code
works" is not finished.

A new topic looks like this:

| Phase | Work | Commit gate |
| --- | --- | --- |
| 1 | Topic dir, README skeleton, first scene stub | `make check` |
| 2 | Scenes, iterated at draft quality | Draft renders verified by eye |
| 3 | Numbered concepts table, references as `- [ ]` | `make test` |
| 4 | Local CodeRabbit pass, findings addressed | Review clean |
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
