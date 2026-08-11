"""Logarithms — counting multiplicative steps, so multiplying becomes adding.

Six scenes on the two-row strip (a counter row over a value row): the
definition as reading the counter, the notation honesty beat, the product
law as hops, negative logs as shrink counts on the repo's own unit
square, and the two payoffs this series was built to deliver — the
evidence ruler for Bayes and the underflow cliff for CTC.

    TheCountingStrip     a logarithm reads the counter row
    OneFactThreeNotations  (2, 6, 64) asked three ways; undo, never cancel
    MultiplyIsAdd        hops add; the slide rule; the base is a unit
    ShrinkCounts         probabilities are shrink counts; log 0 is -inf
    TheEvidenceRuler     each head adds exactly +2 — evidence as length
    TheUnderflowCliff    the value row dies at 2^-1075; the counter walks on

Every number on screen is exact and machine-verified in plan 005; the
float claims are verified on the claimed dtypes.

Render:
    uv run python algebra/logarithms_manim.py
    uv run python algebra/logarithms_manim.py -s TheEvidenceRuler -q draft
"""

from manim import *

from utils import ConceptScene, render_cli


class TheCountingStrip(ConceptScene):
    """A logarithm reads the counter row: the exponent is a count of steps."""

    def construct(self):
        self.play(FadeIn(self.title("The Counting Strip"), shift=0.3 * DOWN))
        self.wait(2)


class OneFactThreeNotations(ConceptScene):
    """One triple, three questions — and logs undo, they never cancel."""

    def construct(self):
        self.play(FadeIn(self.title("One Fact, Three Notations"), shift=0.3 * DOWN))
        self.wait(2)


class MultiplyIsAdd(ConceptScene):
    """Multiplying values is adding counters — the slide rule made a law of it."""

    def construct(self):
        self.play(FadeIn(self.title("Multiply Is Add"), shift=0.3 * DOWN))
        self.wait(2)


class ShrinkCounts(ConceptScene):
    """Probabilities are shrink counts: negative logs fall out of the square."""

    def construct(self):
        self.play(FadeIn(self.title("Shrink Counts"), shift=0.3 * DOWN))
        self.wait(2)


class TheEvidenceRuler(ConceptScene):
    """The odds ladder on a base-3 ruler: each head adds exactly the same length."""

    def construct(self):
        self.play(FadeIn(self.title("The Evidence Ruler"), shift=0.3 * DOWN))
        self.wait(2)


class TheUnderflowCliff(ConceptScene):
    """Products die at float's floor; sums of logs walk on forever."""

    def construct(self):
        self.play(FadeIn(self.title("The Underflow Cliff"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
