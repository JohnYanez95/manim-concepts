"""CTC — aligning text to frames without ever being told the alignment.

Six scenes, built the same way as the counting rules: show the objects, do
the reasoning visibly, and let each formula fall out of what was just seen.

    TheAlignmentProblem   T frames, U characters, no per-frame labels
    TheBlankToken         why bare collapse fails and what epsilon fixes
    ManyPathsOneWord      P(Y|X) is a sum over all paths that spell Y
    CountingAlignments    how big that sum is — and why enumeration dies
    TheForwardTrellis     the exponential sum on a (2U+1) x T grid
    WhenToUseIt           what the assumptions buy, and what they forbid

Render:
    uv run python deep_learning/ctc_alignment_manim.py
    uv run python deep_learning/ctc_alignment_manim.py --scene TheForwardTrellis --quality draft
"""

from manim import *

from utils import ConceptScene, render_cli


class TheAlignmentProblem(ConceptScene):
    """A transcript says what was said, not when — that gap is the problem."""

    def construct(self):
        self.play(FadeIn(self.title("The Alignment Problem"), shift=0.3 * DOWN))
        self.wait(2)


class TheBlankToken(ConceptScene):
    """Bare collapse can't write double letters; epsilon is the designed fix."""

    def construct(self):
        self.play(FadeIn(self.title("The Blank Token"), shift=0.3 * DOWN))
        self.wait(2)


class ManyPathsOneWord(ConceptScene):
    """A word's probability is the sum over every path that collapses to it."""

    def construct(self):
        self.play(FadeIn(self.title("Many Paths, One Word"), shift=0.3 * DOWN))
        self.wait(2)


class CountingAlignments(ConceptScene):
    """How many paths spell one word — the count that kills enumeration."""

    def construct(self):
        self.play(FadeIn(self.title("Counting the Alignments"), shift=0.3 * DOWN))
        self.wait(2)


class TheForwardTrellis(ConceptScene):
    """Exponentially many paths, summed exactly on a (2U+1) x T grid."""

    def construct(self):
        self.play(FadeIn(self.title("The Forward Trellis"), shift=0.3 * DOWN))
        self.wait(2)


class WhenToUseIt(ConceptScene):
    """Where CTC is the right tool, and which assumptions rule it out."""

    def construct(self):
        self.play(FadeIn(self.title("Where CTC Applies"), shift=0.3 * DOWN))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
