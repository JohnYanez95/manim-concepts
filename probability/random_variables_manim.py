"""Random variables — the die as a function, and the pmf as sorted area.

Six scenes closing the graph's oldest promise: `counting-rules` →
binomial, open since the repo's first topic. The stamped square makes
the random variable a fixed labeling; sorting its cells births the pmf
as conserved area; the balance point defines expectation without the
long run; linearity works on dependent pairs; the binomial columns
close the promise with C(4,k) as a visible cell count; and the closer
quantifies the swamping `WhenToUseIt` seeded.

    TheStampedSquare     the function is ink; only the dart is random
    SortTheSquare        the pmf born as conserved, rearranged area
    TheBalancePoint      E as fulcrum; 3.5 is not a face
    SameOutcomesAdd      linearity over the same outcomes; no independence
    TheBinomialColumns   C(4,k) cells x p^k q^(4-k) areas — the promise closes
    ProportionsConverge  proportions converge, counts spread — quantified

Every number on screen traces to plan 007's verified anchors (main
report + addendum); all probability arithmetic there ran in exact
fractions, and display forms like /16 and /256 are forced manually.

Render:
    uv run python probability/random_variables_manim.py
    uv run python probability/random_variables_manim.py -s SortTheSquare -q draft
"""

from manim import *

from utils import (
    BODY_SIZE,
    ConceptScene,
    render_cli,
)


class TheStampedSquare(ConceptScene):
    """The die as a function, not a set: the label is ink, the dart is random.

    Stub — Phase 2 builds the full scene per plan 007's design.
    """

    def construct(self):
        self.play(FadeIn(self.title("The Stamped Square"), shift=0.3 * DOWN))
        opening = Text(
            "A random variable is a fixed rule reading a random outcome.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(render_cli())
