"""CTC decoding — from scores to a transcript: greedy, and the honest beam.

The road's loop closed: training scored a given transcript; deployment
must find one. Best-path decoding reads the frame favourites and
collapses; the construction that justified training on the sum returns
in its deployment costume (greedy hears nothing, the sum hears an A);
the collapsed-prefix beam searches transcripts with two ledgers per
prefix — the collapse map's grammar carried into the search — and the
unpruned beam IS the forward recurrence. Pruning is the only
approximation, and one flagship table shows exactly what it costs.

    TheInverseProblem       nobody deploys a loss — decoding as search

Every number on screen traces to plan 015's verified anchors (the
012.dec anchors and the pinned verifier digest); small examples run
in exact fractions in print, floats shown at displayed precision.

Render:
    uv run python deep_learning/ctc_decoding_manim.py
    uv run python deep_learning/ctc_decoding_manim.py -s TheInverseProblem -q draft
"""

from manim import *

from utils import (
    BODY_SIZE,
    ConceptScene,
    caption,
    render_cli,
)


class TheInverseProblem(ConceptScene):
    """Nobody deploys a loss — decoding is the road's inverse problem."""

    def construct(self):
        self.play(FadeIn(self.title("The Inverse Problem"), shift=0.3 * DOWN))
        opening = Text(
            "Training scored a given transcript. Deployment gets a clip.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))
        placeholder = caption("(scene under construction — plan 015 phase 2)")
        placeholder.move_to(1.0 * DOWN)
        self.play(FadeIn(placeholder))
        self.wait(1.0)


if __name__ == "__main__":
    raise SystemExit(render_cli())
