# Decisions

Review findings that were considered and **declined**, with the reasoning.

This file exists because a declined finding came back. The `render-all` draft
default was raised, declined with reasoning, and raised again verbatim one
round later — the reviewer has no memory between runs, so without a record the
same argument gets re-litigated forever and the reasoning decays each time.

A finding belongs here when it was understood and rejected on the merits. A
finding that was simply fixed does not. If a decision is later reversed, edit
the entry to say so rather than deleting it — the reversal is the interesting
part.

## Declined

### `make render-all` should default to draft quality

*Raised twice.* `render` and `render-all` share one `QUALITY` default, and two
sibling targets disagreeing about what "no flag" means is more surprising than
a slow sweep. Rendering every topic at the 1080p default **is** the finalise
step, so that is the right default for it. The help text already points at
`QUALITY=draft` for a fast pass.

### `utils/colour.py` should be re-exported through `utils/__init__.py`

*Raised twice.* The package root is the surface **concept modules** import
from, and a scene never computes a colour distance or simulates dichromacy —
only `tools/solve_palette.py` and the test suite do, and both import
`utils.colour` directly. Re-exporting eight more names to satisfy a symmetry
rule would make the scene-facing API harder to read in exchange for nothing.

The re-export rule in CLAUDE.md is about names scenes need. The parity test
enforces the real invariant, which is that whatever `utils/__init__.py` *does*
import is also in its `__all__` — a submodule that is never imported there is
not in scope for it.

### The README scene skeleton should `import numpy as np`

The skeleton does not use numpy, and an unused import fails our own ruff F401
gate — so following the suggestion would hand a new contributor a template
that breaks on first `make check`. Verified against the linter. The underlying
rule is conditional and now says so: a module that *uses* numpy imports it
explicitly; one that does not must not import it at all.

### Scene docstrings must be exactly one line

`--list` prints only the first line, so a longer docstring with a good summary
line is legitimate and often better. The requirement that matters — a non-empty
summary — is already enforced by `test_every_scene_has_a_docstring`.

### Pixel or frame-comparison tests of rendered output

A font update, a manim release, or an antialiasing change would fail them with
nothing actually wrong, and the maintenance cost lands every time. The render
path is mocked in tests on purpose; correctness of the *output* is checked by
rendering at draft and looking at it, which is a step in the workflow rather
than a test.
