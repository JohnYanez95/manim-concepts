# Architecture decision records

One file per decision, numbered in the order recorded. Most entries here are
review findings that were considered and **declined**, with the reasoning —
this record exists because a declined finding came back: the `render-all`
draft default was raised, declined with reasoning, and raised again verbatim
one round later. The reviewer has no memory between runs, so without a record
the same argument gets re-litigated forever and the reasoning decays each
time.

A finding belongs here when it was understood and rejected on the merits. A
finding that was simply fixed does not. If a decision is later reversed, edit
the entry to say so rather than deleting it — the reversal is the interesting
part.

| ADR | Decision |
| --- | --- |
| [001](001-render-all-keeps-the-1080p-default.md) | `make render-all` keeps the shared 1080p default |
| [002](002-utils-colour-is-not-re-exported.md) | `utils/colour.py` is not re-exported through the package root |
| [003](003-readme-skeleton-does-not-import-numpy.md) | The README scene skeleton does not `import numpy` |
| [004](004-scene-docstrings-may-exceed-one-line.md) | Scene docstrings may exceed one line |
| [005](005-no-pixel-or-frame-comparison-tests.md) | No pixel or frame-comparison tests of rendered output |
| [006](006-human-ticked-references-stay-ticked.md) | Human-ticked reference checkboxes stay ticked |
