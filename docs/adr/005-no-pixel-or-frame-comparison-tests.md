# ADR 005: No pixel or frame-comparison tests of rendered output

Status: accepted — declines a review finding.

## Context

Review suggested snapshot-style tests of rendered frames to catch visual
regressions.

## Decision

A font update, a manim release, or an antialiasing change would fail them
with nothing actually wrong, and the maintenance cost lands every time.

## Consequences

The render path is mocked in tests on purpose; correctness of the *output*
is checked by rendering at draft and looking at it, which is a step in the
workflow rather than a test.
