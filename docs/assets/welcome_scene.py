"""The repo's front-door animation — rendered to docs/assets/welcome.gif.

Deliberately NOT a concept module: no `_manim.py` suffix, so the Makefile
glob, `make render-all`, and the topic-contract tests all skip it. It
still renders through the shared layer, so it speaks the repo's visual
language.

Render (from the repo root):
    uv run python docs/assets/welcome_scene.py -q draft
    then the ffmpeg palette pass in docs/assets/README.md.
"""

from manim import DOWN, RIGHT, UP, Arrow, Create, FadeIn, GrowArrow, LaggedStart, Text, VGroup

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
    LABEL_SIZE,
    MUTED,
    ConceptScene,
    boxed,
    chip,
    render_cli,
)


class Welcome(ConceptScene):
    """The three-level climb and the house motto, in nine seconds."""

    def construct(self):
        self.play(FadeIn(self.title("manim-concepts"), shift=0.3 * DOWN))

        motto = Text(
            "the formula is the last thing on screen", font_size=BODY_SIZE, color=MUTED
        ).next_to(self.head, DOWN, buff=0.35)
        self.play(FadeIn(motto), run_time=0.7)

        # The three levels are an ordered progression, not unranked
        # categories, so they carry semantic colours: the claim (primary
        # quantity), the argument building the result, the confirmed tool.
        levels = (
            VGroup(
                chip("what is it saying?", COOL, width=3.3),
                chip("why is it true?", ACCENT, width=3.0),
                chip("when is it useful?", GOOD, width=3.3),
            )
            .arrange(RIGHT, buff=0.9)
            .move_to(0.7 * UP)
        )
        arrows = VGroup(
            Arrow(
                levels[0].get_right(),
                levels[1].get_left(),
                buff=0.12,
                color=MUTED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            ),
            Arrow(
                levels[1].get_right(),
                levels[2].get_left(),
                buff=0.12,
                color=MUTED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            ),
        )
        self.play(FadeIn(levels[0], shift=0.2 * RIGHT), run_time=0.6)
        self.play(GrowArrow(arrows[0]), FadeIn(levels[1], shift=0.2 * RIGHT), run_time=0.6)
        self.play(GrowArrow(arrows[1]), FadeIn(levels[2], shift=0.2 * RIGHT), run_time=0.6)

        # Fourteen series across two rows keep every name readable without
        # shrinking the type.
        row_one = VGroup(
            *[
                Text(t, font_size=LABEL_SIZE, color=MUTED)
                for t in [
                    "counting",
                    "CTC",
                    "independence",
                    "conditioning",
                    "Bayes",
                    "logs",
                    "e & ln",
                ]
            ]
        ).arrange(RIGHT, buff=0.32)
        row_two = VGroup(
            *[
                Text(t, font_size=LABEL_SIZE, color=MUTED)
                for t in [
                    "random vars",
                    "softmax",
                    "derivatives",
                    "descent",
                    "CTC gradient",
                    "dyn. prog.",
                    "decoding",
                ]
            ]
        ).arrange(RIGHT, buff=0.32)
        topics = VGroup(row_one, row_two).arrange(DOWN, buff=0.28).move_to(0.95 * DOWN)
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=0.15 * UP) for row in topics for t in row], lag_ratio=0.12
            ),
            run_time=1.1,
        )

        claim = Text(
            "watch the objects, then the reasoning — the formula falls out",
            font_size=25,
            color=ACCENT,
        ).move_to(2.2 * DOWN)
        self.play(FadeIn(claim, shift=0.2 * UP), Create(boxed(claim, buff=0.25)), run_time=0.9)
        self.wait(1.6)


if __name__ == "__main__":
    raise SystemExit(render_cli())
