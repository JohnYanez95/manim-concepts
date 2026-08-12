"""The CTC gradient — softmax output minus how often the truth used each cell.

Seven scenes. The alignment series ended with the forward trellis computing
P(Y|X); this one differentiates it, and the promise three series made on
screen — "every frame of CTC hands this exact picture a different target" —
is kept.

    TheOtherHalfOfTheTrellis   β: every cell also knows how to finish
    PathsThroughACell          α·β, and every column sums to the same P
    WhereTheTruthSpendsItsTime occupancy γ — columns are soft targets
    TheSensitivityOfTheSum     nudge one cell, the loss moves by its share
    SoftmaxMinusOccupancy      the identity: ∂L/∂u = y − γ
    TheErrorSignalLearns       diffuse, localised, gone — Graves fig. 4
    WhyTheSpikesAppear         peakiness is topology + weight sharing

Every number on screen (the α, β, γ and gradient tables, the training
trajectories, the dominance counts) is machine-verified by exact rational
arithmetic, two independent routes, in plan 010.

Render:
    uv run python deep_learning/ctc_gradient_manim.py
    uv run python deep_learning/ctc_gradient_manim.py --scene SoftmaxMinusOccupancy --quality draft
"""

from manim import *

from utils import ConceptScene, caption, render_cli


class TheOtherHalfOfTheTrellis(ConceptScene):
    """β: α answered "how did we get here?" — β answers "how do we finish?"."""

    def construct(self):
        placeholder = caption("The other half of the trellis — built in phase 2.").move_to(ORIGIN)
        self.play(FadeIn(placeholder))
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(render_cli())
