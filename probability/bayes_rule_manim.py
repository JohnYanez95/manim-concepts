"""Bayes' rule — walking through the door the last series left open.

Six scenes: the one-line division and its renaming, counting the answer
out in whole people, the waterfall and the odds form, the prevalence pair
completed as a factorization, iterated updating, and Monty Hall at last —
with the host's protocol as the likelihood.

    ThroughTheFrontDoor   divide the standing identity; rename the parts
    CountingItOut         Diseasitis in whole students: 18/42 = 3/7
    TheOddsForm           the waterfall; prior odds x LR = posterior odds
    OneTestTwoPatients    LR = 9, two priors, two posteriors: 1/2 vs 1/12
    YesterdaysPosterior   odds multiply; a head and a tail cancel exactly
    TheHostsProtocol      Monty, Fall, Crawl — the likelihood is behavior

Every number on screen is exact and machine-verified in plan 004.

Render:
    uv run python probability/bayes_rule_manim.py
    uv run python probability/bayes_rule_manim.py -s TheHostsProtocol -q draft
"""

from manim import *

from utils import ConceptScene, render_cli


class ThroughTheFrontDoor(ConceptScene):
    """One line past the door: P(A|B) = P(B|A) P(A) / P(B), then rename it."""

    def construct(self):
        self.play(FadeIn(self.title("Through the Front Door"), shift=0.3 * DOWN))
        self.wait(2)


class CountingItOut(ConceptScene):
    """The first Bayes computation in whole people — no formula required."""

    def construct(self):
        self.play(FadeIn(self.title("Counting It Out"), shift=0.3 * DOWN))
        self.wait(2)


class TheOddsForm(ConceptScene):
    """The waterfall: prior odds times the likelihood ratio, nothing else."""

    def construct(self):
        self.play(FadeIn(self.title("The Odds Form"), shift=0.3 * DOWN))
        self.wait(2)


class OneTestTwoPatients(ConceptScene):
    """One test, one likelihood ratio — and two very different posteriors."""

    def construct(self):
        self.play(FadeIn(self.title("One Test, Two Patients"), shift=0.3 * DOWN))
        self.wait(2)


class YesterdaysPosterior(ConceptScene):
    """Yesterday's posterior is today's prior — and evidence can cancel exactly."""

    def construct(self):
        self.play(FadeIn(self.title("Yesterday's Posterior"), shift=0.3 * DOWN))
        self.wait(2)


class TheHostsProtocol(ConceptScene):
    """Monty Hall as ordinary Bayes: the likelihood is the host's behavior."""

    def construct(self):
        self.play(FadeIn(self.title("The Host's Protocol"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
