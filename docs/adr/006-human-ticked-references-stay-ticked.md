# ADR 006: Human-ticked reference checkboxes stay ticked

Status: accepted — declines a review finding.

## Context

Review asked for newly ticked reference checkboxes in
`deep_learning/README.md` (and `combinatorics/README.md`) to be reset to
unchecked, on the reasonable prior that references added in the same change
should start unverified.

## Decision

The prior is right and the conclusion is wrong. The verification rule says
only a human may move a box from `- [ ]` to `- [x]` — and that is what
happened: the maintainer opened every reference, confirmed it, and ticked
the boxes themselves, then asked for the state to be committed. A reviewer
looking at a diff cannot tell a human tick from an automated one, which is
why the commit recording the ticks says explicitly that a human made them.

## Consequences

The signal a reviewer should look for is the commit message: a commit that
flips checkboxes must state that the verification was done by a person.
Reset requests against such a commit are declined without new evidence
(e.g. a link that plainly does not cover what its entry claims).
