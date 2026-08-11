"""Independence — when multiplying probabilities is legitimate.

Six scenes on the aligned unit square: probability as area, the product
rule as the definition of independence, the jewel example on a single die,
the mutual-exclusivity confusion, the chain over independent trials, and
the decision rule for assuming any of it.

    ProbabilityAsArea     the unit square: event = region, P = area
    TheProductRule        P(A and B) = P(A) P(B) — straight cuts
    OneDieTwoEvents       independent events on one roll; one pip flips it
    NotMutualExclusivity  disjoint means maximally dependent
    ChainsOfTrials        the product over a sequence — CTC's borrowed step
    WhenToUseIt           what installs independence, what breaks it

Every number on screen is exact and machine-verified in plan 002.

Render:
    uv run python probability/independence_manim.py
    uv run python probability/independence_manim.py --scene TheProductRule --quality draft
"""

from manim import *

from utils import ConceptScene, render_cli


class ProbabilityAsArea(ConceptScene):
    """The sample space is a unit square; probability is a region's share."""

    def construct(self):
        self.play(FadeIn(self.title("Probability as Area"), shift=0.3 * DOWN))
        self.wait(2)


class TheProductRule(ConceptScene):
    """Independence defined: the joint probability factors, cuts run straight."""

    def construct(self):
        self.play(FadeIn(self.title("The Product Rule"), shift=0.3 * DOWN))
        self.wait(2)


class OneDieTwoEvents(ConceptScene):
    """Two events on one roll can be independent — and one pip decides it."""

    def construct(self):
        self.play(FadeIn(self.title("One Die, Two Events"), shift=0.3 * DOWN))
        self.wait(2)


class NotMutualExclusivity(ConceptScene):
    """Mutually exclusive events are not independent; they are maximally dependent."""

    def construct(self):
        self.play(FadeIn(self.title("Not Mutual Exclusivity"), shift=0.3 * DOWN))
        self.wait(2)


class ChainsOfTrials(ConceptScene):
    """A sequence of independent trials multiplies — one factor per step."""

    def construct(self):
        self.play(FadeIn(self.title("Chains of Trials"), shift=0.3 * DOWN))
        self.wait(2)


class WhenToUseIt(ConceptScene):
    """What installs independence, what silently breaks it, and how to tell."""

    def construct(self):
        self.play(FadeIn(self.title("When to Assume It"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
