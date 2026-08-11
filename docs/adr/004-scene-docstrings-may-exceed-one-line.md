# ADR 004: Scene docstrings may exceed one line

Status: accepted — declines a review finding.

## Context

Review suggested requiring scene docstrings to be exactly one line, since
`--list` prints a single line per scene.

## Decision

`--list` prints only the first line, so a longer docstring with a good
summary line is legitimate and often better.

## Consequences

The requirement that matters — a non-empty summary — is already enforced by
`test_every_scene_has_a_docstring`.
