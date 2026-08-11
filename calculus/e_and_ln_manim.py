"""e and the natural logarithm — the base whose stride is exactly 1.

Six scenes closing the repo's oldest on-screen debt: `algebra/`'s strip
promised that calculus makes one base natural, and `TheUnderflowCliff`
rendered ln before any series taught it. Compounding poses the question
(a ceiling between 2 and 3), the zoom builds an honest local growth
rate, the mystery constants obey the strip's laws before they are named
as ln, and the payoffs run from e^(rt) to the log-add identity re-read.

    TheSplitYear         Bernoulli's split year; the table crowds a ceiling
    ZoomUntilStraight    slope, three honest beats; the readout settles
    TheMysteryConstants  0.6931, 1.0986 — and base 8's is three of base 2's
    TheNaturalStride     ln is the counter row in nature's units; the bridge
    RateTimesTime        e^(rt); 69.3 vs 72; ln as time-to-grow
    TheDebtRepaid        the underflow identity re-read; the inverse graph

Every number on screen traces to plan 006's verified anchors; slope
tables are the one-sided ratio (the symmetric quotient's rows differ
visibly, and float cancellation bends it below h = 1e-5 — the recorded
hazard).

Render:
    uv run python calculus/e_and_ln_manim.py
    uv run python calculus/e_and_ln_manim.py -s TheSplitYear -q draft
"""

from manim import *

from utils import (
    BODY_SIZE,
    ConceptScene,
    render_cli,
)


class TheSplitYear(ConceptScene):
    """Split one year of 100% growth into smaller hops; a ceiling appears.

    Stub — Phase 2 builds the full scene per plan 006's design.
    """

    def construct(self):
        self.play(FadeIn(self.title("The Split Year"), shift=0.3 * DOWN))
        question = Text(
            "Jacob Bernoulli, 1683: $1 grows at 100% for a year — now split the year.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(question))
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(render_cli())
