# ADR 007: Plans pin research digests, not full transcripts

Status: accepted — declines a review finding.

## Context

Review asked plan 002 to embed the complete Phase-0 research reports (or
stable links to committed copies) so every on-screen number has full
provenance.

## Decision

The plan's "verified technical anchors" section *is* the durable
artifact: every number a scene displays, each with its verification
method (exact enumeration, primary-source quote, or both), plus the
sources list that lands in the topic README as human-gated references.
Full agent transcripts are ephemeral working material — embedding them
would bloat plans past readability while adding nothing checkable,
because the check on an anchor is re-verification, not re-reading a
transcript.

## Consequences

The anchors section must stay complete enough to rebuild the scenes
from: a number without its method, or a method without its source, is a
plan defect. That standard — not attached transcripts — is what review
should hold plans to.
