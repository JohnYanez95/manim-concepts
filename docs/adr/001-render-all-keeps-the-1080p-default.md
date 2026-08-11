# ADR 001: `make render-all` keeps the shared 1080p default

Status: accepted — declines a review finding. *Raised twice.*

## Context

Review suggested `make render-all` should default to draft quality, since
rendering every module at 1080p is slow.

## Decision

`render` and `render-all` share one `QUALITY` default, and two sibling
targets disagreeing about what "no flag" means is more surprising than a slow
sweep. Rendering every topic at the 1080p default **is** the finalise step,
so that is the right default for it.

## Consequences

The help text already points at `QUALITY=draft` for a fast pass; anyone
iterating passes it explicitly.
