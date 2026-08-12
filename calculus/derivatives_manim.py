"""The derivative toolkit — naming what the zoom built, and just enough rules.

The series the CTC gradient waits on: the slope as a function (d/dx
names the settling ratio `ZoomUntilStraight` built), nudge geometry
for x², the sum and chain rules, e^x and ln in notation, the score
function finding the likelihood peak the probability series found by
grid, and the closer — the smooth max's sensitivities ARE the softmax
shares, leaving p − one-hot one subtraction away.

Every number on screen traces to plan 009's verified anchors; tables
use forward quotients (the symmetric quotient of a quadratic is exact
and would kill the settling narrative), and dt stays a real number
throughout.

Render:
    uv run python calculus/derivatives_manim.py
    uv run python calculus/derivatives_manim.py -s TheSlopeIsAFunction -q draft
"""

from manim import *

from utils import ConceptScene, render_cli


class TheSlopeIsAFunction(ConceptScene):
    """Every smooth curve carries a second curve: its slope at each point."""

    def construct(self):
        self.play(FadeIn(self.title("The Slope Is a Function"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
