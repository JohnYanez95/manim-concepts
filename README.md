# manim-concepts

Intuitive [Manim](https://www.manim.community/) visualisations of core concepts.

The bias of this repo is that a formula should be the *last* thing on screen,
not the first. Every scene shows the object being reasoned about, does the
reasoning visibly, and lets the expression fall out of what was just seen.

Concepts are grouped by topic. Each topic is a directory holding one or more
**concept modules** — a single runnable `*_manim.py` file per concept, each
defining the scenes for it — and every module renders itself:

```bash
uv run python combinatorics/counting_rules_manim.py
```

No `manim` CLI, no scene name, no quality flag required. That renders every
scene in the file at 1080p60. Add `--quality draft` for a fast 480p pass while
you are still iterating.

## Quickstart

```bash
uv sync                                                  # build the environment
uv run pre-commit install                                # install the lint gate
uv run python combinatorics/counting_rules_manim.py -q draft
```

Renders land in `media/videos/<module>/<resolution>/<Scene>.mp4`. That whole
directory is gitignored — every video here is reproducible from source in one
command, so none of them are committed.

## Topics

| Topic | Concepts |
| --- | --- |
| [`combinatorics/`](combinatorics/README.md) | Multiplication rule, permutations, combinations, partitions |

Topics are added as they are written. Likely next: `probability/`,
`calculus/`, `linear_algebra/`, `deep_learning/`. The layout is expected to
drift — if a topic only ever holds one file, it can collapse into a flatter
arrangement later without anything else changing.

### The topic contract

Every topic directory carries a `README.md`, and it is not optional. A scene
is only worth keeping if someone can tell what it claims to teach without
watching it first. Each topic README has four parts, in this order:

1. **Scope** — a short high-level explanation of what the topic covers *and
   what it deliberately does not*. The second half matters more: without it a
   topic quietly becomes a junk drawer.
2. **A numbered concepts table** — one row per scene, listing its position,
   the idea it carries, the formula it lands on, and the visual argument it
   makes. The visual-argument column is what stops two scenes from
   re-explaining the same intuition.

   The numbering is not decoration. Scenes in a module build toward one idea,
   so **source order is viewing order**: renders are named from it
   (`03_CombinationRule.mp4`), `--list` prints it, and the table must agree
   with both. Someone landing on a topic should be able to watch it top to
   bottom, or at minimum see the trajectory without playing anything.
   `tests/test_topic_contract.py` fails if the table and the code disagree.
3. **References** — the outside sources the topic is built from, under the
   verification rule below.
4. **Ideas not yet built** — the queue, so the gap between what exists and
   what was intended is visible in the repo rather than in someone's head.

Adding a new topic directory without its README is an incomplete change.

### Reference verification is human-gated

References are the one thing in this repo that cannot be checked by tooling.
A URL that resolves is not the same as a source that says what the row claims
it says, and a plausible-looking citation is exactly the kind of error that
survives review. So every reference is a checklist item with an explicit
state:

```markdown
- [ ] [Concrete Mathematics, ch. 5](https://example.org/…) — binomial
      coefficient identities; the source for the partition scene.
```

- `- [ ]` — **unverified.** The link has not been opened and confirmed by a
  person. This is the default, and anything suggested by a tool or an
  assistant starts here without exception.
- `- [x]` — **verified.** A human opened it, confirmed it covers what the
  entry claims, and is vouching for it.

Only a human moves a box from unchecked to checked. Nothing in CI, no hook,
and no assistant may flip one — an automated tick would defeat the only
purpose the box has. Unverified entries are fine to merge; they are a to-do,
not a defect. Silently *promoting* one is the defect.

## Rendering

Every concept module takes the same flags.

| Flag | Values | Default | Notes |
| --- | --- | --- | --- |
| `-q`, `--quality` | `draft` `medium` `high` `4k` | `high` | 480p15 / 720p30 / **1080p60** / 2160p60 |
| `-s`, `--scene` | scene name, repeatable | all scenes | Errors out on an unknown name rather than rendering nothing |
| `-f`, `--format` | `mp4` `gif` `png` `webm` `mov` | `mp4` | |
| `-p`, `--preview` | flag | off | Opens each render when it finishes |
| `-l`, `--list` | flag | — | Prints the scenes in the module and exits |
| `--no-cache` | flag | off | Ignores cached partial movies; use while iterating |
| `--transparent` | flag | off | Alpha channel instead of the theme background |

```bash
uv run python combinatorics/counting_rules_manim.py --list
uv run python combinatorics/counting_rules_manim.py -s CombinationRule -q high -p
uv run python combinatorics/counting_rules_manim.py -q draft --no-cache
```

The `-ql` / `-qm` / `-qh` spelling manim uses is deliberately not surfaced —
`--quality draft` says what it is for.

Renders are cached per animation, so re-running after editing one scene only
re-renders what changed. Pass `--no-cache` if a stale partial is suspected.

### Make targets

`make` wraps the common cases. `make help` lists everything.

| Target | Does |
| --- | --- |
| `make venv` | Build the environment from the lockfile |
| `make hooks` | Install the pre-commit gate |
| `make list` | Every concept module and the scenes it defines |
| `make render FILE=… [QUALITY=…] [SCENE=…]` | Render one module (1080p60 unless `QUALITY` says otherwise) |
| `make render-all [QUALITY=draft]` | Render every concept module |
| `make lint` / `make fmt` | Ruff check / format |
| `make test` | Run the test suite |
| `make check` | Ruff, tests and every hook, without committing |
| `make clean-drafts` | Delete sub-1080p renders, keep the final ones |
| `make clean` | Delete all rendered output |

### Working on a scene

Every non-trivial change starts with a plan broken into numbered phases. Each
phase ends in a **named commit gate** — one commit, and it has to be green
before the next phase starts. The last phase is always a fully rendered PR: a
plan that stops at "the code works" is not finished.

Iterating at 1080p is a waste of wall-clock, so the loop itself is draft-first:

1. `--quality draft` (480p15) until the scene is right.
2. Check the render actually worked. Confirm you got the expected number of
   files and that their names differ, probe one with `ffprobe` for frame count
   and duration, and when layout or colour changed, pull a frame out with
   `ffmpeg` and look at it. "It produced a file" is not verification — the two
   render bugs found so far both passed that check.
3. Run the CodeRabbit review locally, **before** opening the PR, and address
   what it finds. The PR should open clean rather than accumulate rounds.
4. Open the PR; the bot reviews it as an independent second pass.
5. Finalise, then `make clean-drafts` and render at the 1080p default.

```bash
uv run python combinatorics/counting_rules_manim.py -q draft   # iterate
# ... local review pass, then PR ...
make clean-drafts                                              # then finalise
uv run python combinatorics/counting_rules_manim.py            # 1080p60
```

## Adding a concept

1. Pick or create a topic directory: `probability/`. No `__init__.py` — topic
   directories hold scripts, not packages. A new directory needs a `README.md`
   meeting [the topic contract](#the-topic-contract) in the same change.
2. Add `probability/bayes_rule_manim.py`. The `_manim.py` suffix is what
   `make list` and `make render-all` glob for.
3. Write scenes as `ConceptScene` subclasses and end the file with:

   ```python
   if __name__ == "__main__":
       raise SystemExit(render_cli())
   ```

   `render_cli` finds every scene defined in the module automatically, in
   source order — there is no list to keep in sync.
4. Give each scene a one-line docstring. It is what `--list` prints.
5. Add a row to the topic README's concepts table, and add whatever you
   worked from to its references as `- [ ]`. Leave it unchecked; verifying it
   is the reader's job, not the author's.

A skeleton:

```python
"""Bayes' rule — updating a belief is re-weighting an area."""

from manim import *

from utils import ACCENT, ConceptScene, render_cli, token


class PriorAndPosterior(ConceptScene):
    """The prior as an area, the likelihood as a slice through it."""

    def construct(self):
        self.play(FadeIn(self.title("Bayes' Rule"), shift=0.3 * DOWN))
        ...


if __name__ == "__main__":
    raise SystemExit(render_cli())
```

## The `utils` layer

Shared so that a new topic starts with the repo's visual language rather than a
fresh set of hex codes:

| Module | Holds |
| --- | --- |
| `utils/theme.py` | Colours (`ACCENT`, `COOL`, `WARM`, `GOOD`, `MUTED`), the `PALETTE` cycle, the type scale |
| `utils/scene.py` | `ConceptScene` — applies the background, provides `self.title()` |
| `utils/mobjects.py` | `token`, `chip`, `boxed`, `header`, `caption` |
| `utils/render.py` | `render_cli` — the flags above, and the scene numbering |

Colours carry meaning and should be used for it: `ACCENT` is the result being
built toward, `WARM` is what gets cancelled or overcounted, `GOOD` is a
confirmed object, `MUTED` is scaffolding. `PALETTE` is different — it is a
categorical cycle for "N distinct things with no ranking", indexed by position.

Import from the package root, not the submodules:

```python
from utils import ACCENT, ConceptScene, render_cli, token
```

`utils` resolves from any topic directory because the project installs itself
as a package (see the comment at the top of `pyproject.toml`) — there is no
`sys.path` manipulation in any concept module.

## Tests

`make test`. The suite is deliberately narrow — there are no pixel or
frame-comparison tests, because they fail on a font update without anything
being wrong. What is covered is the part that can be wrong silently:

- `tests/test_render.py` — scene discovery, ordering, filename numbering,
  selection and its error paths, quality mapping. Includes a regression test
  for the one real bug found so far: a batch of scenes rendering into a single
  file.
- `tests/test_topic_contract.py` — enforces the contract above mechanically.
  Every topic has a README with all four sections, its Scope states exclusions,
  every scene is documented and listed, the table's numbering matches source
  order, and every reference carries a verification checkbox. Review can only
  see a diff; this catches a topic that has drifted since.

## Conventions

- Ruff enforces PEP 8 at 100 columns, with import sorting, pyflakes, bugbear,
  pyupgrade and simplify rules. `make check` runs the whole gate.
- Concept modules use `from manim import *`, the idiom manim's own docs use.
  This is the one lint exemption in the repo and it is scoped to the
  `*/*_manim.py` glob; `utils/` imports explicitly.
- Renders, `.venv/`, caches and WSL `:Zone.Identifier` files are gitignored.
  `check-added-large-files` at 512 KB is the backstop if one slips past.

## Prerequisites

Python and every Python dependency come from `uv sync`. Manim also needs
system libraries for text shaping, video muxing and LaTeX:

```bash
sudo apt-get install -y libcairo2-dev libpango1.0-dev pkg-config ffmpeg \
                        texlive texlive-latex-extra dvisvgm
```

LaTeX is only needed for `MathTex` / `Tex`, which most scenes here use.
