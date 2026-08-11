"""Conditional probability — re-measuring inside what you now know.

Six scenes on the same unit square as the independence series:
restriction and renormalization, the stepped cut finally named, the
multiplication rule as a rectangle identity, total probability and trees,
the inversion fallacy, and what conditioning is actually for.

    TheRestrictedSquare      dim what B rules out, re-inflate the band
    IndependenceRevisited    the step's height was P(A|B) all along
    TheMultiplicationRule    P(A and B) = P(B) P(A|B) — the aces license
    TotalProbabilityAndTrees add up the columns; the square drawn as a tree
    TwoSlicesOneSquare       same overlap, two denominators — the inversion
    WhenToCondition          what you condition on, and the CTC residual

Every number on screen is exact and machine-verified in plan 003.

Render:
    uv run python probability/conditional_probability_manim.py
    uv run python probability/conditional_probability_manim.py -s TwoSlicesOneSquare -q draft
"""

from manim import *

from utils import ConceptScene, render_cli


class TheRestrictedSquare(ConceptScene):
    """Conditioning is restriction then renormalization — the formula comes last."""

    def construct(self):
        self.play(FadeIn(self.title("The Restricted Square"), shift=0.3 * DOWN))
        self.wait(2)


class IndependenceRevisited(ConceptScene):
    """The stepped cut had a name: its height inside the band is P(A|B)."""

    def construct(self):
        self.play(FadeIn(self.title("Independence, Revisited"), shift=0.3 * DOWN))
        self.wait(2)


class TheMultiplicationRule(ConceptScene):
    """The definition rewritten: P(A and B) = P(B) P(A|B), one rectangle."""

    def construct(self):
        self.play(FadeIn(self.title("The Multiplication Rule"), shift=0.3 * DOWN))
        self.wait(2)


class TotalProbabilityAndTrees(ConceptScene):
    """Total probability adds the columns; a tree is the same square drawn."""

    def construct(self):
        self.play(FadeIn(self.title("Total Probability, and Trees"), shift=0.3 * DOWN))
        self.wait(2)


class TwoSlicesOneSquare(ConceptScene):
    """P(A|B) and P(B|A) share a numerator and nothing else — the inversion."""

    def construct(self):
        self.play(FadeIn(self.title("Two Slices, One Square"), shift=0.3 * DOWN))
        self.wait(2)


class WhenToCondition(ConceptScene):
    """What conditioning is for — and what exactly you condition on."""

    def construct(self):
        self.play(FadeIn(self.title("When to Condition"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
