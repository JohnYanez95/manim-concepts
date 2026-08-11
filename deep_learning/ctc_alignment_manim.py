"""CTC — aligning text to frames without ever being told the alignment.

Six scenes, built the same way as the counting rules: show the objects, do
the reasoning visibly, and let each formula fall out of what was just seen.

    TheAlignmentProblem   T frames, U characters, no per-frame labels
    TheBlankToken         why bare collapse fails and what epsilon fixes
    ManyPathsOneWord      P(Y|X) is a sum over all paths that spell Y
    CountingAlignments    how big that sum is — and why enumeration dies
    TheForwardTrellis     the exponential sum on a (2U+1) x T grid
    WhenToUseIt           what the assumptions buy, and what they forbid

Every count on screen (the 15 paths for AB at T=4, the trellis columns, the
5 paths for OO) is machine-verified two independent ways in plan 001.

Render:
    uv run python deep_learning/ctc_alignment_manim.py
    uv run python deep_learning/ctc_alignment_manim.py --scene TheForwardTrellis --quality draft
"""

import numpy as np
from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    FORMULA_SIZE,
    GOOD,
    LABEL_SIZE,
    MUTED,
    RESULT_SIZE,
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    palette,
    render_cli,
    token,
)

# The blank as it appears in path strings on screen. Epsilon rather than "-"
# or "_": the research pass flagged that "_" collides visually with the
# word-space character, and real CTC vocabularies contain both.
EPS = "ε"


def _letters(word: str) -> VGroup:
    """A word as a row of letter tokens, coloured by letter identity.

    Distinct letters are unranked categories, so they take the categorical
    cycle; every occurrence of one letter shares a colour, which is what
    makes "these two are the same and will merge" visible. The blank is
    MUTED — it means "nothing new", and the eye should treat it as quiet.
    """
    order: dict[str, int] = {}
    for ch in word:
        if ch != EPS and ch not in order:
            order[ch] = len(order)
    row = VGroup(
        *[token(ch, MUTED if ch == EPS else palette(order[ch]), radius=0.3) for ch in word]
    )
    return row.arrange(RIGHT, buff=0.28)


class TheAlignmentProblem(ConceptScene):
    """A transcript says what was said, not when — that gap is the problem."""

    def construct(self):
        self.play(FadeIn(self.title("The Alignment Problem"), shift=0.3 * DOWN))

        prompt = Text(
            "One clip of audio, and its transcript. Nothing else.", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the two objects the dataset actually pairs -----------------------
        # A fixed pseudo-waveform: ten frames of "audio" as bars. The input is
        # the primary quantity of the whole series, so the frames are COOL.
        heights = [0.55, 0.9, 1.25, 1.05, 0.7, 1.15, 1.35, 1.0, 0.8, 0.5]
        bars = VGroup(
            *[
                Rectangle(
                    width=0.44,
                    height=h,
                    color=COOL,
                    fill_color=COOL,
                    fill_opacity=0.5,
                    stroke_width=2,
                )
                for h in heights
            ]
        )
        bars.arrange(RIGHT, buff=0.18, aligned_edge=DOWN).move_to(1.45 * UP)
        frames_tag = Text("T = 10 frames", font_size=LABEL_SIZE, color=COOL)
        frames_tag.next_to(bars, RIGHT, buff=0.4)
        axis = Arrow(
            bars.get_corner(DL) + 0.35 * DOWN + 0.2 * LEFT,
            bars.get_corner(DR) + 0.35 * DOWN + 0.6 * RIGHT,
            buff=0,
            color=MUTED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.03,
        )
        axis_tag = Text("time", font_size=SMALL_SIZE, color=MUTED).next_to(axis, DOWN, buff=0.12)

        word = VGroup(*[token(ch, palette(i)) for i, ch in enumerate("CAT")])
        word.arrange(RIGHT, buff=0.4).move_to(1.7 * DOWN)
        word_tag = Text("U = 3 characters", font_size=LABEL_SIZE).next_to(word, RIGHT, buff=0.4)

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.07),
            run_time=1.4,
        )
        self.play(FadeIn(frames_tag), GrowArrow(axis), FadeIn(axis_tag))
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.6) for t in word], lag_ratio=0.15),
            FadeIn(word_tag),
        )
        self.wait(0.5)

        question = Text(
            "Which frames are the C? Which are the A?", font_size=BODY_SIZE, color=ACCENT
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question), FadeOut(prompt))

        # --- three alignments, all consistent ---------------------------------
        # Coloured spans under the bars: one candidate way to divide the ten
        # frames among the three letters. The spans morph between candidates,
        # which is the visual claim: nothing in the data prefers any of them.
        def marks(counts: list[int]) -> VGroup:
            spans, start = VGroup(), 0
            y = bars.get_bottom()[1] - 1.0
            for i, count in enumerate(counts):
                left = bars[start].get_left()[0]
                right = bars[start + count - 1].get_right()[0]
                line = Line(
                    np.array([left, y, 0]),
                    np.array([right, y, 0]),
                    color=palette(i),
                    stroke_width=7,
                )
                tag = Text("CAT"[i], font_size=SMALL_SIZE, color=palette(i))
                spans.add(VGroup(line, tag.next_to(line, DOWN, buff=0.1)))
                start += count
            return spans

        candidates = [[3, 4, 3], [2, 6, 2], [5, 2, 3]]
        labels = ["one way it could line up", "another", "another still"]
        spans = marks(candidates[0])
        note = caption(labels[0]).next_to(question, UP, buff=0.35)
        self.play(FadeIn(spans), FadeIn(note))
        self.wait(0.6)
        for counts, text in zip(candidates[1:], labels[1:], strict=True):
            new_spans = marks(counts)
            new_note = caption(text).next_to(question, UP, buff=0.35)
            self.play(Transform(spans, new_spans), Transform(note, new_note))
            self.wait(0.6)

        verdict = Text(
            "every one of them is consistent with the pair",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).next_to(question, UP, buff=0.35)
        self.play(FadeOut(note), FadeIn(verdict))
        self.wait(0.8)

        # --- the reframe -------------------------------------------------------
        self.play(FadeOut(VGroup(spans, verdict, question, frames_tag, word_tag, axis, axis_tag)))
        gap = Text(
            "The transcript says what was said —\nnothing in the data says when.",
            font_size=32,
            line_spacing=1.1,
        ).move_to(0.15 * DOWN)
        self.play(bars.animate.scale(0.8).to_edge(UP, buff=1.4).shift(0.2 * DOWN))
        self.play(word.animate.scale(0.8).next_to(gap, DOWN, buff=0.6), FadeIn(gap))
        self.wait(0.8)

        claim = Text(
            "CTC: don't pick an alignment — score them all", font_size=30, color=ACCENT
        ).to_edge(DOWN, buff=0.85)
        self.play(FadeIn(claim, shift=0.2 * UP), Create(boxed(claim, buff=0.28)))
        self.wait(2)


class TheBlankToken(ConceptScene):
    """Bare collapse can't write double letters; epsilon is the designed fix."""

    def construct(self):
        self.play(FadeIn(self.title("The Blank Token"), shift=0.3 * DOWN))

        prompt = Text(
            "First idea: one letter per frame, then merge repeats", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(prompt))

        # --- the naive collapse, and its failure ------------------------------
        naive = _letters("HHELLLO").move_to(1.5 * UP)
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in naive], lag_ratio=0.08))
        self.wait(0.4)

        # Merging repeats means the duplicate frames die: they are the
        # overcount here, so they flash WARM on the way out.
        duplicates = [naive[1], naive[4], naive[5]]
        survivors = [naive[0], naive[2], naive[3], naive[6]]
        self.play(*[t.animate.set_color(WARM) for t in duplicates], run_time=0.6)
        merged = _letters("HELO").move_to(0.1 * UP)
        self.play(
            FadeOut(VGroup(*duplicates), shift=0.3 * DOWN),
            *[t.animate.move_to(m) for t, m in zip(survivors, merged, strict=True)],
            run_time=0.9,
        )
        wrong = Text("HELO — the double L is unwritable", font_size=BODY_SIZE, color=WARM)
        wrong.next_to(merged, DOWN, buff=0.5)
        second = caption("and every frame was forced to emit — held sounds, silence, all of it")
        second.next_to(wrong, DOWN, buff=0.3)
        self.play(FadeIn(wrong))
        self.play(FadeIn(second))
        self.wait(1.0)

        stage = VGroup(*survivors, wrong, second, prompt)
        self.play(FadeOut(stage))

        # --- epsilon, and the collapse done right ------------------------------
        intro = Text(
            'Add one output symbol: ε — "nothing new to emit"', font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(intro))

        fixed = _letters("HHEL" + EPS + "LO").move_to(1.5 * UP)
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in fixed], lag_ratio=0.08))

        # The step labels live at the left edge, clear of the rows' descent
        # path — next_to the row above would put them exactly where the next
        # row lands.
        step1 = caption("1. merge repeats").to_edge(LEFT, buff=0.8)
        step1.set_y(0.35)
        self.play(FadeIn(step1))
        dup = fixed[1]
        keep = [fixed[0]] + [fixed[i] for i in range(2, 7)]
        self.play(dup.animate.set_color(WARM), run_time=0.5)
        row2 = _letters("HEL" + EPS + "LO").move_to(0.35 * UP)
        self.play(
            FadeOut(dup, shift=0.3 * DOWN),
            *[t.animate.move_to(m) for t, m in zip(keep, row2, strict=True)],
            run_time=0.9,
        )

        step2 = caption("2. then drop ε").to_edge(LEFT, buff=0.8)
        step2.set_y(-0.85)
        self.play(FadeIn(step2))
        eps_token = keep[3]
        rest = [keep[0], keep[1], keep[2], keep[4], keep[5]]
        row3 = _letters("HELLO").move_to(0.85 * DOWN)
        self.play(eps_token.animate.set_color(WARM), run_time=0.5)
        self.play(
            FadeOut(eps_token, shift=0.3 * DOWN),
            *[t.animate.move_to(m) for t, m in zip(rest, row3, strict=True)],
            run_time=0.9,
        )
        check = Text("HELLO ✓", font_size=32, color=GOOD).next_to(row3, RIGHT, buff=0.6)
        self.play(FadeIn(check, scale=0.7))
        self.wait(0.8)

        # The ε that survived the merge is what kept the two Ls apart — say so
        # before the counter-example, while the mechanism is still on screen.
        why = Text(
            "the ε survived the merge and kept the two Ls apart",
            font_size=BODY_SIZE,
            color=ACCENT,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(why))
        self.wait(1.0)

        self.play(FadeOut(VGroup(*rest, check, why, step1, step2, intro)))

        # --- order matters, and the minimal pair -------------------------------
        order = VGroup(
            Text("merge, then drop:", font_size=BODY_SIZE),
            Text("HHEL" + EPS + "LO  →  HELLO ✓", font_size=BODY_SIZE, color=GOOD),
            Text("drop, then merge:", font_size=BODY_SIZE),
            Text("HHEL" + EPS + "LO  →  HHELLO  →  HELO ✗", font_size=BODY_SIZE, color=WARM),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.4), col_alignments="rl")
        order.move_to(1.15 * UP)
        pair = VGroup(
            Text("TOO", font_size=BODY_SIZE),
            Text("→  TO ✗", font_size=BODY_SIZE, color=WARM),
            Text("TO" + EPS + "O", font_size=BODY_SIZE),
            Text("→  TOO ✓", font_size=BODY_SIZE, color=GOOD),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.4), col_alignments="rl")
        pair.next_to(order, DOWN, buff=0.7)
        pair_tag = caption("without ε, a double letter is unreachable at all").next_to(
            pair, DOWN, buff=0.35
        )
        self.play(FadeIn(order))
        self.wait(0.8)
        self.play(FadeIn(pair), FadeIn(pair_tag))
        self.wait(0.8)

        self.play(FadeOut(VGroup(order, pair, pair_tag)))
        takeaway = Text(
            "ε makes double letters writable and emission optional", font_size=28
        ).move_to(0.4 * DOWN)
        fine_print = caption("ε is not a space — real vocabularies carry both").next_to(
            takeaway, DOWN, buff=0.45
        )
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.3)))
        self.play(FadeIn(fine_print))
        self.wait(2)


class ManyPathsOneWord(ConceptScene):
    """A word's probability is the sum over every path that collapses to it."""

    def construct(self):
        self.play(FadeIn(self.title("Many Paths, One Word"), shift=0.3 * DOWN))

        prompt = Text("Alphabet {A, B, ε} · 4 frames · target: AB", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        self.play(FadeIn(prompt))

        # --- collapse as a verb: two hits and a miss ---------------------------
        examples = [
            ("AA" + EPS + "B", "AB", True),
            (EPS + "ABB", "AB", True),
            ("AB" + EPS + "A", "ABA", False),
        ]
        rows = VGroup()
        for path, result, ok in examples:
            arrow = Arrow(ORIGIN, 0.9 * RIGHT, buff=0, color=MUTED, stroke_width=3)
            verdict = Text(
                f"{result} {'✓' if ok else '✗'}",
                font_size=BODY_SIZE,
                color=GOOD if ok else WARM,
            )
            row = VGroup(_letters(path).scale(0.75), arrow, verdict)
            row.arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(0.8 * UP)
        for row in rows:
            self.play(FadeIn(row, shift=0.2 * RIGHT), run_time=0.7)
        self.wait(0.6)

        ask = Text(
            "How many paths land on AB? All of them:", font_size=BODY_SIZE, color=ACCENT
        ).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(ask))
        self.wait(0.5)
        self.play(FadeOut(rows), FadeOut(ask))

        # --- the whole fiber, enumerated ---------------------------------------
        # All 15 paths that collapse to AB at T=4 — machine-verified in plan
        # 001 by brute force over 3^4 strings and by the forward recurrence.
        paths = [
            "εεAB",
            "εAεB",
            "εAAB",
            "εABε",
            "εABB",
            "AεεB",
            "AεBε",
            "AεBB",
            "AAεB",
            "AAAB",
            "AABε",
            "AABB",
            "ABεε",
            "ABBε",
            "ABBB",
        ]
        chips = VGroup(*[chip(p, GOOD, width=1.5) for p in paths])
        chips.arrange_in_grid(rows=3, cols=5, buff=0.26).move_to(0.55 * UP)
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.05),
            run_time=1.8,
        )
        brace = Brace(chips, RIGHT, color=ACCENT)
        count = Text("15 paths\none word", font_size=LABEL_SIZE, color=ACCENT, line_spacing=1.0)
        count.next_to(brace, RIGHT, buff=0.2)
        self.play(GrowFromCenter(brace), FadeIn(count))
        self.wait(0.6)

        # One chip carries the arithmetic: a path's probability is a product
        # of per-frame probabilities, one factor per frame.
        target = chips[8]  # AAεB
        halo = SurroundingRectangle(target, color=ACCENT, buff=0.06, corner_radius=0.1)
        product = MathTex(
            r"P(\text{AA}\varepsilon\text{B})",
            r"=",
            r"y_1(\text{A})\, y_2(\text{A})\, y_3(\varepsilon)\, y_4(\text{B})",
            font_size=36,
        ).next_to(chips, DOWN, buff=0.45)
        product[2].set_color(COOL)
        self.play(Create(halo))
        self.play(Write(product))
        self.wait(0.8)

        # --- the claim ----------------------------------------------------------
        self.play(FadeOut(VGroup(chips, brace, count, halo, product, prompt)))
        formula = MathTex(
            r"P(Y \mid X)",
            r"=\sum_{\pi \in \mathcal{B}^{-1}(Y)}",
            r"\;\prod_{t=1}^{T} y_t(\pi_t)",
            font_size=FORMULA_SIZE,
        ).move_to(0.9 * UP)
        formula[0].set_color(ACCENT)
        gloss = VGroup(
            caption("the word's probability"),
            caption("summed over every path that spells it"),
            caption("each path: one product of per-frame probabilities"),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        gloss.next_to(formula, DOWN, buff=0.55)
        gloss[0].set_color(ACCENT)
        self.play(Write(formula))
        self.play(Create(boxed(formula, buff=0.35)))
        self.play(LaggedStart(*[FadeIn(g) for g in gloss], lag_ratio=0.3))
        self.wait(0.8)

        closing = Text(
            "no single path is the answer — the sum is", font_size=BODY_SIZE, color=ACCENT
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(closing))
        self.wait(2)


class CountingAlignments(ConceptScene):
    """How many paths spell one word — the count that kills enumeration."""

    def construct(self):
        self.play(FadeIn(self.title("Counting the Alignments"), shift=0.3 * DOWN))

        # --- the multiplicative rule sizes the raw space -----------------------
        recall = Text(
            "From combinatorics: independent stages multiply", font_size=BODY_SIZE
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(recall))

        slots = VGroup()
        for _ in range(4):
            slot = RoundedRectangle(
                width=1.05, height=1.05, corner_radius=0.14, stroke_width=3, color=MUTED
            )
            slot.set_stroke(opacity=0.7)
            menu = Text("A B ε", font_size=SMALL_SIZE, color=MUTED)
            slots.add(VGroup(slot, menu.next_to(slot, UP, buff=0.18)))
        slots.arrange(RIGHT, buff=0.6).move_to(1.35 * UP)
        threes = VGroup(*[Text("3", font_size=30, color=ACCENT).move_to(s[0]) for s in slots])
        self.play(FadeIn(slots))
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in threes], lag_ratio=0.15))

        raw = MathTex(r"3^4 = 81", r"\ \text{paths in total}", font_size=RESULT_SIZE)
        raw[0].set_color(ACCENT)
        raw.next_to(slots, DOWN, buff=0.55)
        self.play(Write(raw))
        self.wait(0.6)

        # --- 15 of 81: the fiber inside the raw space --------------------------
        self.play(
            FadeOut(VGroup(slots, threes, recall)),
            raw.animate.scale(0.75).to_edge(LEFT, buff=0.9).shift(2.35 * UP),
        )

        dots = VGroup(
            *[
                Square(
                    side_length=0.26,
                    stroke_width=1.5,
                    color=MUTED,
                    fill_opacity=0.12,
                    fill_color=MUTED,
                )
                for _ in range(81)
            ]
        )
        dots.arrange_in_grid(rows=9, cols=9, buff=0.09).move_to(0.35 * UP + 2.0 * LEFT)
        self.play(FadeIn(dots, lag_ratio=0.01, run_time=1.2))
        # Any 15 of them stand for the fiber; the point is the proportion, so
        # they are scattered rather than clustered.
        fiber_index = [3, 7, 12, 18, 22, 27, 33, 38, 44, 49, 55, 60, 66, 71, 77]
        highlight = VGroup(*[dots[i] for i in fiber_index])
        self.play(
            *[d.animate.set_color(GOOD).set_fill(GOOD, opacity=0.55) for d in highlight],
            run_time=0.9,
        )
        fifteen = Text("15 spell AB", font_size=BODY_SIZE, color=GOOD)
        fifteen.next_to(dots, DOWN, buff=0.4)
        self.play(FadeIn(fifteen))
        self.wait(0.6)

        # --- the closed form, checked ------------------------------------------
        # The whole right half of the frame is free once "15 spell AB" sits
        # under the grid, so the formula block stacks there without touching it.
        closed = MathTex(
            r"\bigl|\mathcal{B}^{-1}(Y)\bigr| = \binom{T+U}{\,T-U\,}",
            font_size=44,
            color=ACCENT,
        ).move_to(np.array([3.3, 1.3, 0]))
        check = MathTex(r"\binom{6}{2} = 15\ \checkmark", font_size=36, color=GOOD)
        check.next_to(closed, DOWN, buff=0.45)
        fine = caption("repeat-free targets; doubles shrink it").next_to(check, DOWN, buff=0.35)
        self.play(Write(closed))
        self.play(FadeIn(check, shift=0.2 * UP), FadeIn(fine))
        self.wait(0.8)

        # --- scale it up, and watch enumeration die ----------------------------
        self.play(FadeOut(VGroup(dots, highlight, fifteen, closed, check, fine, raw)))
        real = Text(
            "One second of real speech: T = 100 frames, U = 50 characters",
            font_size=BODY_SIZE,
        ).move_to(1.5 * UP)
        blowup = MathTex(
            r"\binom{150}{50}", r"\approx 2 \times 10^{40}", font_size=FORMULA_SIZE
        ).move_to(0.3 * UP)
        # The explosion is the obstacle the trellis removes, so it reads WARM.
        blowup[1].set_color(WARM)
        dead = Text("enumeration is dead on arrival", font_size=BODY_SIZE, color=WARM)
        dead.next_to(blowup, DOWN, buff=0.5)
        self.play(FadeIn(real))
        self.play(Write(blowup))
        self.play(FadeIn(dead))
        self.wait(0.8)

        hook = Text("but the sum never needed the list", font_size=30, color=ACCENT).to_edge(
            DOWN, buff=0.8
        )
        self.play(FadeIn(hook, shift=0.2 * UP), Create(boxed(hook, buff=0.28)))
        self.wait(2)


class TheForwardTrellis(ConceptScene):
    """Exponentially many paths, summed exactly on a (2U+1) x T grid."""

    def construct(self):
        self.play(FadeIn(self.title("The Forward Trellis"), shift=0.3 * DOWN))

        # --- the extended sequence ---------------------------------------------
        build = Text("Wrap the target in blanks:  AB  →  ε A ε B ε", font_size=BODY_SIZE).next_to(
            self.head, DOWN, buff=0.3
        )
        states_tag = caption("2U + 1 = 5 states — a path may pass through any blank, or not")
        states_tag.next_to(build, DOWN, buff=0.25)
        self.play(FadeIn(build))
        self.play(FadeIn(states_tag))

        # --- the grid ----------------------------------------------------------
        # Rows are the 5 states of the extended target, columns the 4 frames.
        # Off-centre to the left on purpose: the termination readout needs the
        # right margin, and the header captions need clear air above t=1..4.
        z_prime = [EPS, "A", EPS, "B", EPS]
        row_colors = [MUTED, palette(0), MUTED, palette(1), MUTED]
        xs = [-2.6 + 1.75 * t for t in range(4)]
        ys = [1.3 - 0.95 * s for s in range(5)]

        row_labels = VGroup(
            *[
                token(ch, color, radius=0.26).move_to(np.array([-4.2, y, 0]))
                for ch, color, y in zip(z_prime, row_colors, ys, strict=True)
            ]
        )
        col_labels = VGroup(
            *[
                Text(f"t={t + 1}", font_size=SMALL_SIZE, color=COOL).move_to(
                    np.array([x, ys[0] + 0.55, 0])
                )
                for t, x in enumerate(xs)
            ]
        )

        # Nodes are filled with the background so the edges appear to stop at
        # their rims; the numbers land inside them later.
        nodes = [
            [
                Circle(radius=0.3, color=MUTED, stroke_width=2)
                .set_fill(self.camera.background_color, opacity=1.0)
                .move_to(np.array([x, y, 0]))
                for y in ys
            ]
            for x in xs
        ]
        node_group = VGroup(*[n for column in nodes for n in column])

        # Edges are the collapse semantics drawn as geometry: stay, advance,
        # and the s-2 skip — legal only into B over the middle blank, because
        # its neighbours differ. That single missing edge class is the rule.
        edges = VGroup()
        for t in range(3):
            for s in range(5):
                targets = [s, s + 1]
                if s + 2 <= 4 and z_prime[s + 2] != EPS and z_prime[s + 2] != z_prime[s]:
                    targets.append(s + 2)
                for s2 in targets:
                    if s2 <= 4:
                        edges.add(
                            Line(
                                nodes[t][s].get_center(),
                                nodes[t + 1][s2].get_center(),
                                color=MUTED,
                                stroke_width=2,
                                stroke_opacity=0.6,
                            )
                        )

        self.play(FadeIn(row_labels), FadeIn(col_labels))
        self.play(Create(edges, lag_ratio=0.02, run_time=1.6), FadeIn(node_group))
        self.wait(0.4)

        skip_note = caption("the skip over ε is legal only between different letters")
        skip_note.to_edge(DOWN, buff=0.4)
        skip_warn = Text(
            "(O ε O could not skip — it would merge the Os)", font_size=SMALL_SIZE, color=WARM
        ).next_to(skip_note, UP, buff=0.18)
        self.play(FadeIn(skip_note), FadeIn(skip_warn))
        self.wait(0.9)
        self.play(FadeOut(skip_note), FadeOut(skip_warn), FadeOut(build), FadeOut(states_tag))

        # --- run the recurrence with unit weights ------------------------------
        # Counting paths instead of multiplying probabilities: same recurrence,
        # and the numbers below are the machine-verified columns from plan 001.
        columns = [
            [1, 1, 0, 0, 0],
            [1, 2, 1, 1, 0],
            [1, 3, 3, 4, 1],
            [1, 4, 6, 10, 5],
        ]
        note = Text(
            "count the paths into each node — each node needs only the column before it",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(note))

        numbers: list[list[Text | None]] = [[None] * 5 for _ in range(4)]
        for t, column in enumerate(columns):
            entering = VGroup()
            for s, value in enumerate(column):
                if value == 0:
                    continue  # dead states stay visually empty
                figure = Text(str(value), font_size=22).move_to(nodes[t][s])
                numbers[t][s] = figure
                entering.add(figure)
            self.play(
                LaggedStart(*[FadeIn(f, scale=0.6) for f in entering], lag_ratio=0.1), run_time=0.8
            )
        self.wait(0.4)

        # One node opened up: the 4 in column 3, row B, is 1 + 1 + 2 from its
        # three predecessors — stay, advance, and the skip past the blank.
        preds = [nodes[1][1], nodes[1][2], nodes[1][3]]
        flash = VGroup(
            *[
                Line(p.get_center(), nodes[2][3].get_center(), color=ACCENT, stroke_width=4)
                for p in preds
            ]
        )
        arithmetic = MathTex(r"2 + 1 + 1 = 4", font_size=32, color=ACCENT)
        arithmetic.to_edge(DOWN, buff=0.45)
        self.play(Create(flash), Write(arithmetic))
        self.wait(0.9)
        self.play(FadeOut(flash), FadeOut(arithmetic))

        # --- termination --------------------------------------------------------
        finals = VGroup(nodes[3][3], nodes[3][4])
        final_box = SurroundingRectangle(finals, color=ACCENT, buff=0.14, corner_radius=0.12)
        total = MathTex(r"10 + 5 = 15", font_size=40, color=ACCENT)
        total.next_to(final_box, RIGHT, buff=0.5).align_to(finals[0], UP)
        recall = caption("the same 15 —\nnever listed").next_to(total, DOWN, buff=0.3)
        recall.align_to(total, LEFT)
        self.play(Create(final_box))
        self.play(Write(total), FadeIn(recall))
        self.wait(1.0)

        # --- the formula this grid is -------------------------------------------
        trellis = VGroup(
            row_labels,
            col_labels,
            node_group,
            edges,
            final_box,
            total,
            recall,
            VGroup(*[f for row in numbers for f in row if f is not None]),
        )
        self.play(FadeOut(trellis), FadeOut(note))
        formula = MathTex(
            r"\alpha_t(s) = \bigl(\alpha_{t-1}(s) + \alpha_{t-1}(s{-}1)"
            r" + \alpha_{t-1}(s{-}2)\bigr)\, y_t(z'_s)",
            font_size=44,
            color=ACCENT,
        ).move_to(0.85 * UP)
        conditions = VGroup(
            caption("third term only when z's is a letter different from z's−2"),
            caption("start in the first two states; finish in the last two"),
        ).arrange(DOWN, buff=0.2)
        conditions.next_to(formula, DOWN, buff=0.45)
        payoff = Text(
            "swap the 1s for per-frame probabilities: this is the CTC loss",
            font_size=BODY_SIZE,
        ).next_to(conditions, DOWN, buff=0.5)
        scale_note = Text(
            "T · (2U+1) cells instead of 10⁴⁰ paths", font_size=BODY_SIZE, color=ACCENT
        ).next_to(payoff, DOWN, buff=0.3)
        self.play(Write(formula), Create(boxed(formula, buff=0.3)))
        self.play(FadeIn(conditions))
        self.play(FadeIn(payoff), FadeIn(scale_note))
        self.wait(2)


class WhenToUseIt(ConceptScene):
    """Where CTC is the right tool, and which assumptions rule it out."""

    def construct(self):
        self.play(FadeIn(self.title("Where CTC Applies"), shift=0.3 * DOWN))

        # Level three of the narrative: the first five scenes build what CTC
        # says and why the machinery works; this one is the decision rule for
        # reaching for it — or not — on a task that was not in the examples.
        cases = [
            ("Speech → text", "CTC", True),
            ("Handwriting, OCR", "CTC", True),
            ("Keyword spotting", "CTC", True),
            ("Translation — outputs reorder", "attention", False),
        ]
        # The mapping sits high so the assumptions block below never touches
        # its last row.
        questions = VGroup(*[Text(q, font_size=22) for q, _, _ in cases])
        questions.arrange(DOWN, buff=0.58, aligned_edge=LEFT)
        questions.to_edge(LEFT, buff=0.8).shift(1.35 * UP)
        verdicts = VGroup(
            *[
                Text(v, font_size=23, weight=BOLD, color=ACCENT if ok else WARM)
                for _, v, ok in cases
            ]
        )
        verdicts.arrange(DOWN, buff=0.58, aligned_edge=LEFT).to_edge(RIGHT, buff=1.6)
        for question, verdict in zip(questions, verdicts, strict=True):
            verdict.match_y(question)

        start_x = questions.get_right()[0] + 0.35
        end_x = verdicts.get_left()[0] - 0.35
        arrows = VGroup(
            *[
                Arrow(
                    np.array([start_x, q.get_y(), 0]),
                    np.array([end_x, q.get_y(), 0]),
                    buff=0,
                    color=MUTED,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.18,
                )
                for q in questions
            ]
        )
        for question, arrow, verdict in zip(questions, arrows, verdicts, strict=True):
            self.play(
                FadeIn(question, shift=0.2 * RIGHT),
                GrowArrow(arrow),
                FadeIn(verdict, shift=0.2 * LEFT),
                run_time=0.6,
            )
        self.wait(0.6)

        # The three assumptions are the trellis read back as constraints —
        # each one names the geometry that enforced it.
        assumptions = VGroup(
            Text("monotonic — the lattice only ever moves forward", font_size=21),
            Text("output ≤ input — every character costs at least one frame", font_size=21),
            Text("frames independent given the input — a language model still helps", font_size=21),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        assumptions.move_to(1.85 * DOWN + 0.3 * LEFT)
        rule_tag = Text("what the grid assumed all along:", font_size=LABEL_SIZE, color=ACCENT)
        rule_tag.next_to(assumptions, UP, buff=0.3).align_to(assumptions, LEFT)
        self.play(FadeIn(rule_tag))
        self.play(LaggedStart(*[FadeIn(a, shift=0.2 * RIGHT) for a in assumptions], lag_ratio=0.25))
        self.wait(0.8)

        warn = (
            Text(
                "and one caveat: CTC spikes are timing, not segmentation",
                font_size=SMALL_SIZE,
                color=WARM,
            )
            .next_to(assumptions, DOWN, buff=0.4)
            .align_to(assumptions, LEFT)
        )
        self.play(FadeIn(warn))
        self.wait(0.8)

        self.play(FadeOut(VGroup(questions, arrows, verdicts, rule_tag, assumptions, warn)))
        takeaway = Text(
            "Unknown timing, monotonic order, shorter output — that is CTC's home",
            font_size=24,
        ).move_to(0.2 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
