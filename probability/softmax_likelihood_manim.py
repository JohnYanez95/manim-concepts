"""Softmax and likelihood — one table read two ways, and the machine that fills it.

The bridge series the CTC topic deferred: likelihood as the row lens
on a table the viewer already owns, the peak as the best explanation,
the log as the native scale of accumulating evidence, softmax as the
exp-then-normalize machine forced by shift invariance, temperature and
the base-change answer to "why e", and NLL — the loss that trains the
machine — as a visible gap on the log-sum-exp ruler.

Every number on screen traces to plan 008's verified anchors (main
report + addendum); probability arithmetic there ran in exact
fractions, and display roundings are forced manually.

Render:
    uv run python probability/softmax_likelihood_manim.py
    uv run python probability/softmax_likelihood_manim.py -s TheLikelihoodLens -q draft
"""

from manim import *

from utils import ConceptScene, render_cli


class TheLikelihoodLens(ConceptScene):
    """Probability and likelihood are one table read two ways."""

    def construct(self):
        self.play(FadeIn(self.title("The Likelihood Lens"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
