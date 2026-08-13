"""Gradient descent — the walk downhill, one line applied over and over.

The derivative toolkit's payoff: the slope becomes an update
(w <- w - eta L'(w)), the learning rate's four fates fall out of one
per-step factor, the nudge square prices the cliff, the sign-change
habit stamps every stopping place, the walk is not a ball, and the
road's own 12-knob loss walks 0.7181 -> 0.0003 read entirely off the
loss-vs-step chart the bowl taught.

    TheSlopeBecomesAStep    the update derived, the bowl walked

Every number on screen traces to plan 014's verified anchors; bowl
and factor-table values are exact dyadic rationals, double-well and
road-walk values are float64 shown at 4 decimal places.

Render:
    uv run python calculus/gradient_descent_manim.py
    uv run python calculus/gradient_descent_manim.py -s TheSlopeBecomesAStep -q draft
"""

from manim import *

from utils import (
    BODY_SIZE,
    ConceptScene,
    caption,
    render_cli,
)


class TheSlopeBecomesAStep(ConceptScene):
    """A slope is a reason to move — one line turns it into motion."""

    def construct(self):
        self.play(FadeIn(self.title("The Slope Becomes a Step"), shift=0.3 * DOWN))
        opening = Text(
            "The toolkit reads which way is downhill. Now take the step.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        placeholder = caption("(scene under construction — plan 014 phase 2)")
        placeholder.move_to(1.0 * DOWN)
        self.play(FadeIn(placeholder))
        self.wait(1.0)


if __name__ == "__main__":
    render_cli()
