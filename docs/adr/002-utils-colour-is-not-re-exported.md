# ADR 002: `utils/colour.py` is not re-exported through the package root

Status: accepted — declines a review finding. *Raised twice.*

## Context

Review suggested `utils/colour.py` should be re-exported through
`utils/__init__.py` for symmetry with the other submodules.

## Decision

The package root is the surface **concept modules** import from, and a scene
never computes a colour distance or simulates dichromacy — only
`tools/solve_palette.py` and the test suite do, and both import
`utils.colour` directly. Re-exporting eight more names to satisfy a symmetry
rule would make the scene-facing API harder to read in exchange for nothing.

## Consequences

The re-export rule in CLAUDE.md is about names scenes need. The parity test
enforces the real invariant, which is that whatever `utils/__init__.py`
*does* import is also in its `__all__` — a submodule that is never imported
there is not in scope for it.
