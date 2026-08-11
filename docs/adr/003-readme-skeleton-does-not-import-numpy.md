# ADR 003: The README scene skeleton does not `import numpy`

Status: accepted — declines a review finding.

## Context

Review suggested the scene skeleton in the root README should
`import numpy as np`, since concept modules commonly use numpy.

## Decision

The skeleton does not use numpy, and an unused import fails our own ruff
F401 gate — so following the suggestion would hand a new contributor a
template that breaks on first `make check`. Verified against the linter.

## Consequences

The underlying rule is conditional and now says so: a module that *uses*
numpy imports it explicitly; one that does not must not import it at all.
