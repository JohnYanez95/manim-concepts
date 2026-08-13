"""Dynamic programming — the move the trellis performed without a name.

Six scenes. The repo's oldest promise: the alignment series ran a dynamic
program on screen and never said so; this series names the move — the
recursion tree folding into a small table — and re-reads two pictures the
viewer already owns as instances of it.

    TheQuestionAskedTwice   177 calls to settle 11 questions
    WriteTheAnswersDown     the tree folds; the move gets its name
    TheLatticeRecounted     shared prefixes, counted once — Pascal's sum
    TheTrellisWasAMemo      the forward trellis re-read as a stored answer
    WhatBreaksIt            DP pays exactly for how much past the future needs
    TheSignatureInTheWild   the two-part signature, mapped over the wild

Every number on screen traces to plan 013's verification pass (exact
integer arithmetic, two independent routes; the study guide's DP chapter
is the seed — ADR 008's pipeline running book-to-screen).

Render:
    uv run python algorithms/dynamic_programming_manim.py
    uv run python algorithms/dynamic_programming_manim.py -s WriteTheAnswersDown -q draft
"""

from manim import *

from utils import ConceptScene, caption, render_cli


class TheQuestionAskedTwice(ConceptScene):
    """Computed exactly as written, the recursion asks the same question over and over."""

    def construct(self):
        placeholder = caption("The question asked twice — built in phase 2.").move_to(ORIGIN)
        self.play(FadeIn(placeholder))
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(render_cli())
