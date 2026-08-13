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
    TheFrameFavourites      best-path: argmax, collapse, and its caveat
    TheModelHeardNothing    sum vs max in the deployment costume
    SearchTheTranscripts    the collapsed-prefix beam — the DP move
    TheTwoLedgers           p_b and p_nb, forced by the collapse map
    ThePriceOfPruning       width 1 wrong, width 2 exact — priced
    TheLoopClosed           greedy or beam, the LM splice, the loop

Every number on screen traces to plan 015's verified anchors (the
012.dec anchors and the pinned verifier digest); the small examples
are exact fractions displayed as decimals.

Render:
    uv run python deep_learning/ctc_decoding_manim.py
    uv run python deep_learning/ctc_decoding_manim.py -s TheInverseProblem -q draft
"""

from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
    MUTED,
    WARM,
    ConceptScene,
    boxed,
    caption,
    chip,
    on_frame,
    palette,
    render_cli,
)

PB = palette(0)  # the ending-in-blank ledger
PNB = palette(1)  # the ending-in-letter ledger
NEW = palette(2)  # the new-letter stream

ROWS = ["A", "B", "ε"]


def _matrix(columns, x=0.0, y=0.0, cell=0.72, highlight=None):
    """A per-frame score table: rows A/B/ε, one column per frame.

    `columns` is a list of (a, b, eps) probability triples; `highlight`
    is an optional list of row indices to ring per column (the argmax).
    Returns (group, cells) with cells[t][r] the square mobject.
    """
    group = VGroup()
    cells = []
    for t, col in enumerate(columns):
        cells.append([])
        for r, v in enumerate(col):
            sq = Square(side_length=cell, color=MUTED, stroke_width=2)
            sq.set_fill(MUTED, opacity=0.08)
            sq.move_to([x + t * cell, y - r * cell, 0])
            val = Text(f"{v:.1f}", font_size=20).move_to(sq)
            group.add(sq, val)
            cells[t].append(sq)
    for r, name in enumerate(ROWS):
        tag = Text(name, font_size=22, color=MUTED)
        tag.next_to(cells[0][r], LEFT, buff=0.25)
        group.add(tag)
    for t in range(len(columns)):
        tag = Text(f"t={t + 1}", font_size=18, color=MUTED)
        tag.next_to(cells[t][0], UP, buff=0.18)
        group.add(tag)
    rings = VGroup()
    if highlight is not None:
        for t, r in enumerate(highlight):
            rings.add(
                SurroundingRectangle(cells[t][r], color=ACCENT, buff=0.04, corner_radius=0.06)
            )
    return group, cells, rings


def _ledger_chip(label, pb, pnb, x=0.0, y=0.0, scale=4.0):
    """A prefix candidate with its two ledgers as stacked bars."""
    box = RoundedRectangle(width=3.6, height=1.1, corner_radius=0.12, stroke_width=2, color=MUTED)
    box.move_to([x, y, 0])
    name = Text(label, font_size=24).move_to([x - 1.45, y, 0])
    bar_b = Rectangle(width=max(pb * scale, 0.02), height=0.22, color=PB, fill_color=PB)
    bar_b.set_fill(opacity=0.6).set_stroke(width=1)
    bar_b.move_to([x - 0.95 + max(pb * scale, 0.02) / 2, y + 0.2, 0])
    bar_nb = Rectangle(width=max(pnb * scale, 0.02), height=0.22, color=PNB, fill_color=PNB)
    bar_nb.set_fill(opacity=0.6).set_stroke(width=1)
    bar_nb.move_to([x - 0.95 + max(pnb * scale, 0.02) / 2, y - 0.2, 0])
    vb = Text(f"{pb:.2f}", font_size=16, color=PB).next_to(bar_b, RIGHT, buff=0.1)
    vnb = Text(f"{pnb:.2f}", font_size=16, color=PNB).next_to(bar_nb, RIGHT, buff=0.1)
    return VGroup(box, name, bar_b, bar_nb, vb, vnb)


class TheInverseProblem(ConceptScene):
    """Nobody deploys a loss — decoding is the road's inverse problem."""

    def construct(self):
        self.play(FadeIn(self.title("The Inverse Problem"), shift=0.3 * DOWN))
        opening = Text(
            "Training scored a given transcript. Deployment gets a clip.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The road's loop, with a hole where the answer should be.
        stops = [
            chip("waveform", MUTED, width=1.9),
            chip("scores yₜ", COOL, width=1.9),
            chip("???", ACCENT, width=1.4),
            chip("words", GOOD, width=1.6),
        ]
        row = VGroup(*stops).arrange(RIGHT, buff=1.0).move_to(0.9 * UP)
        arrows = VGroup(
            *[
                Arrow(a.get_right(), b.get_left(), buff=0.12, color=MUTED, stroke_width=3)
                for a, b in zip(stops[:-1], stops[1:], strict=True)
            ]
        )
        self.play(LaggedStart(*[FadeIn(s, shift=0.15 * UP) for s in stops], lag_ratio=0.2))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
        self.wait(1.2)
        gap = caption("training never searched — the transcript was handed to it")
        gap.next_to(row, DOWN, buff=0.4)
        self.play(FadeIn(gap))
        self.wait(2.2)

        # The honest target, and the honest admission.
        quote = caption('"we do not know of a general, tractable')
        quote2 = caption('decoding algorithm" — Graves et al., 2006')
        quote.move_to(0.0 * RIGHT + 0.9 * DOWN)
        quote2.next_to(quote, DOWN, buff=0.13)
        self.play(FadeIn(quote), FadeIn(quote2))
        two = caption("so: two approximations — the cheap one, and the honest one")
        two.next_to(quote2, DOWN, buff=0.35)
        self.play(FadeIn(two))
        self.wait(2.4)

        # Formula last.
        self.play(FadeOut(opening), FadeOut(quote), FadeOut(quote2), FadeOut(two))
        target = MathTex(r"Y^* = \operatorname*{argmax}_{Y} \; P(Y \mid X)", font_size=42)
        target.move_to(0.0 * RIGHT + 2.6 * DOWN)
        sumtag = caption("P: the alignment series' sum over paths")
        sumtag.next_to(target, DOWN, buff=0.55)
        self.play(Write(target))
        self.play(Create(boxed(target)), FadeIn(sumtag))
        self.wait(3.6)


class TheFrameFavourites(ConceptScene):
    """Best-path decoding: take each frame's favourite, collapse — and its caveat."""

    def construct(self):
        self.play(FadeIn(self.title("The Frame Favourites"), shift=0.3 * DOWN))
        opening = Text(
            "The obvious decoder: ask each frame, then collapse the answers.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        cols = [(0.5, 0.2, 0.3), (0.4, 0.3, 0.3), (0.2, 0.3, 0.5)]
        grid, _cells, rings = _matrix(cols, x=-4.6, y=0.9, highlight=[0, 0, 2])
        self.play(FadeIn(grid))
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3))
        path = MathTex(
            r"A,\ A,\ \varepsilon \;\xrightarrow{\ \mathcal{B}\ }\; \text{A}", font_size=32
        )
        path.next_to(grid, DOWN, buff=0.5)
        self.play(Write(path))
        fast = caption("T lookups, one collapse — fast enough for anything")
        fast.next_to(path, DOWN, buff=0.3)
        on_frame(fast)
        self.play(FadeIn(fast))
        self.wait(2.0)

        # The honest check: all 27 paths, grouped by transcript.
        board_title = caption("all 27 paths, grouped by transcript:")
        board_title.move_to(3.3 * RIGHT + 2.0 * UP)
        on_frame(board_title)
        entries = [
            ("A", 0.3170, ACCENT),
            ("AB", 0.2610, MUTED),
            ("B", 0.1770, MUTED),
            ("BA", 0.0980, MUTED),
            ('""', 0.0450, MUTED),
        ]
        board = VGroup()
        for i, (name, mass, color) in enumerate(entries):
            bar = Rectangle(width=mass * 9.0, height=0.34, color=color, fill_color=color)
            bar.set_fill(opacity=0.45).set_stroke(width=1.5)
            bar.move_to([1.6 + mass * 4.5, 1.35 - 0.55 * i, 0])
            tag = Text(name, font_size=22).next_to(bar, LEFT, buff=0.25)
            val = Text(f"{mass:.4f}", font_size=18, color=color).next_to(bar, RIGHT, buff=0.15)
            on_frame(val)
            board.add(VGroup(bar, tag, val))
        self.play(FadeIn(board_title))
        self.play(LaggedStart(*[FadeIn(b, shift=0.15 * RIGHT) for b in board], lag_ratio=0.2))
        right = caption("greedy got this one right — one favourite", color=GOOD)
        right2 = caption("chain clearly ahead, the max speaks for the sum", color=GOOD)
        right.move_to(3.3 * RIGHT + 1.6 * DOWN)
        right2.next_to(right, DOWN, buff=0.13)
        on_frame(right)
        on_frame(right2)
        self.play(FadeIn(right), FadeIn(right2))
        self.wait(2.4)

        # The caveat that owns the next scene.
        self.play(FadeOut(opening))
        caveat = caption('"trivial to compute … not guaranteed to find', color=WARM)
        caveat2 = caption('the most probable labelling" — Graves et al.', color=WARM)
        caveat.move_to(3.3 * RIGHT + 2.7 * DOWN)
        caveat2.next_to(caveat, DOWN, buff=0.13)
        on_frame(caveat)
        on_frame(caveat2)
        self.play(FadeIn(caveat), FadeIn(caveat2))
        rule = MathTex(
            r"h(x) \approx \mathcal{B}\!\left(\text{argmax per frame}\right)", font_size=34
        )
        rule.move_to(3.6 * LEFT + 3.0 * DOWN)
        on_frame(rule)
        self.play(Write(rule))
        self.play(Create(boxed(rule, buff=0.18)))
        self.wait(3.6)


class TheModelHeardNothing(ConceptScene):
    """Sum vs max, wearing its deployment costume: greedy decodes the empty string."""

    def construct(self):
        self.play(FadeIn(self.title("The Model Heard Nothing"), shift=0.3 * DOWN))
        opening = Text(
            "Two frames, two candidates — and the frames hedge.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # y(A) = 0.4, y(ε) = 0.6 at both frames.
        grid = VGroup()
        vals = [[0.4, 0.4], [0.6, 0.6]]
        names = ["A", "ε"]
        cells = []
        for r in range(2):
            cells.append([])
            for t in range(2):
                sq = Square(side_length=0.8, color=MUTED, stroke_width=2)
                sq.set_fill(MUTED, opacity=0.08)
                sq.move_to([-5.2 + t * 0.8, 1.5 - r * 0.8, 0])
                v = Text(f"{vals[r][t]:.1f}", font_size=22).move_to(sq)
                grid.add(sq, v)
                cells[r].append(sq)
            grid.add(
                Text(names[r], font_size=22, color=MUTED).next_to(cells[r][0], LEFT, buff=0.25)
            )
        rings = VGroup(
            SurroundingRectangle(cells[1][0], color=WARM, buff=0.04, corner_radius=0.06),
            SurroundingRectangle(cells[1][1], color=WARM, buff=0.04, corner_radius=0.06),
        )
        self.play(FadeIn(grid))
        self.play(Create(rings))
        greedy_says = caption("greedy: ε, ε — the empty transcript", color=WARM)
        greedy_says.next_to(grid, DOWN, buff=0.4).shift(0.4 * RIGHT)
        on_frame(greedy_says)
        self.play(FadeIn(greedy_says))

        # The team of paths pools past the single path.
        bar_empty = Rectangle(width=0.36 * 8, height=0.5, color=WARM, fill_color=WARM)
        bar_empty.set_fill(opacity=0.5).set_stroke(width=1.5)
        bar_empty.move_to([0.9 + 0.36 * 4, 1.6, 0])
        tag_empty = Text('""', font_size=24).next_to(bar_empty, LEFT, buff=0.3)
        val_empty = Text("0.36", font_size=20, color=WARM).next_to(bar_empty, RIGHT, buff=0.15)
        team = caption("A pools its three paths:  AA 0.16 + Aε 0.24 + εA 0.24")
        team.move_to(2.4 * RIGHT + 0.75 * UP)
        on_frame(team)
        bar_a = Rectangle(width=0.64 * 8, height=0.5, color=COOL, fill_color=COOL)
        bar_a.set_fill(opacity=0.5).set_stroke(width=1.5)
        bar_a.move_to([0.9 + 0.64 * 4, 0.0, 0])
        tag_a = Text("A", font_size=24).next_to(bar_a, LEFT, buff=0.3)
        val_a = Text("0.64", font_size=20, color=COOL).next_to(bar_a, RIGHT, buff=0.15)
        on_frame(val_a)
        self.play(FadeIn(bar_empty), FadeIn(tag_empty), FadeIn(val_empty))
        self.play(FadeIn(team))
        self.play(FadeIn(bar_a), FadeIn(tag_a), FadeIn(val_a))
        verdict = caption("read correctly, it heard an A; read greedily, nothing", color=ACCENT)
        verdict.move_to(1.6 * RIGHT + 0.75 * DOWN)
        on_frame(verdict)
        self.play(FadeIn(verdict))
        self.wait(2.4)

        # The dial: how badly must the frames hedge before greedy lies?
        line = Line([-5.6, -2.2, 0], [5.6, -2.2, 0], color=MUTED, stroke_width=2)
        half = Line([-2.8, -2.32, 0], [-2.8, -2.08, 0], color=MUTED, stroke_width=2)
        root2 = Line([2.0, -2.32, 0], [2.0, -2.08, 0], color=MUTED, stroke_width=2)
        band = Line([-2.8, -2.2, 0], [2.0, -2.2, 0], color=WARM, stroke_width=7)
        half_tag = MathTex(r"q = \tfrac12", font_size=26).next_to(half, DOWN, buff=0.2)
        root2_tag = MathTex(r"q = \tfrac{1}{\sqrt{2}} \approx 0.7071", font_size=26)
        root2_tag.next_to(root2, DOWN, buff=0.2)
        dial = caption("y(ε) = q: greedy goes empty past ½ —")
        dial2 = caption("the empty answer is TRUE only past 1/√2")
        dial.move_to(0.0 * RIGHT + 1.55 * DOWN)
        dial2.next_to(dial, DOWN, buff=0.13)
        self.play(FadeIn(dial), FadeIn(dial2))
        self.play(Create(line), Create(half), Create(root2), FadeIn(half_tag), FadeIn(root2_tag))
        self.play(Create(band))
        lies = caption("the band where greedy lies (at q = 0.7: 0.49 vs 0.51)", color=WARM)
        lies.next_to(root2_tag, DOWN, buff=0.3).shift(2.0 * LEFT)
        on_frame(lies)
        self.play(FadeIn(lies))
        self.wait(2.4)

        # Why greedy is nonetheless the production default.
        self.play(FadeOut(opening))
        excuse = Text(
            "Trained outputs are peaked: the max usually speaks for the sum.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        excuse2 = caption("the hedging inputs — accents, noise — are exactly where it stops")
        excuse2.next_to(lies, DOWN, buff=0.3)
        on_frame(excuse2)
        self.play(FadeIn(excuse), FadeIn(excuse2))
        self.wait(3.6)


class SearchTheTranscripts(ConceptScene):
    """The collapsed-prefix beam: candidates are transcripts, and masses merge."""

    def construct(self):
        self.play(FadeIn(self.title("Search the Transcripts"), shift=0.3 * DOWN))
        opening = Text(
            "Doing better means searching — but searching the right things.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The natural wrong design: a beam over paths.
        wrong = VGroup(
            chip("path AA   0.16", WARM, width=2.6),
            chip("path Aε   0.24", WARM, width=2.6),
            chip("path εA   0.24", WARM, width=2.6),
        ).arrange(DOWN, buff=0.25)
        wrong.move_to(5.0 * LEFT + 1.0 * UP)
        on_frame(wrong)
        wrong_tag = caption("a beam over paths:")
        wrong_tag2 = caption("three slots, one transcript")
        wrong_tag3 = caption("— its mass split three ways")
        wrong_tag.next_to(wrong, DOWN, buff=0.3)
        wrong_tag2.next_to(wrong_tag, DOWN, buff=0.13)
        wrong_tag3.next_to(wrong_tag2, DOWN, buff=0.13)
        for m in (wrong_tag, wrong_tag2, wrong_tag3):
            on_frame(m)
        self.play(LaggedStart(*[FadeIn(w, shift=0.15 * UP) for w in wrong], lag_ratio=0.2))
        self.play(FadeIn(wrong_tag), FadeIn(wrong_tag2), FadeIn(wrong_tag3))
        self.wait(2.2)

        # Relabel the axis: candidates are collapsed prefixes; masses merge.
        start = chip("start  1.0", MUTED, width=1.9).move_to(1.2 * RIGHT + 1.9 * UP)
        n_empty = chip("∅  0.6", MUTED, width=1.5).move_to(0.6 * LEFT + 0.4 * UP)
        n_a1 = chip("A  0.4", COOL, width=1.5).move_to(3.4 * RIGHT + 0.4 * UP)
        n_empty2 = chip("∅  0.36", MUTED, width=1.7).move_to(0.6 * LEFT + 1.4 * DOWN)
        n_a2 = chip("A  0.64", ACCENT, width=1.7).move_to(3.4 * RIGHT + 1.4 * DOWN)
        e1 = Arrow(start.get_bottom(), n_empty.get_top(), color=MUTED, buff=0.1, stroke_width=3)
        e2 = Arrow(start.get_bottom(), n_a1.get_top(), color=NEW, buff=0.1, stroke_width=3)
        e3 = Arrow(n_empty.get_bottom(), n_empty2.get_top(), color=PB, buff=0.1, stroke_width=3)
        e4 = Arrow(n_empty.get_bottom(), n_a2.get_top(), color=NEW, buff=0.1, stroke_width=3)
        e5 = Arrow(n_a1.get_bottom(), n_a2.get_top(), color=PB, buff=0.1, stroke_width=3)
        e6 = CurvedArrow(n_a1.get_right(), n_a2.get_right(), angle=-0.9, color=PNB, stroke_width=3)
        self.play(FadeIn(start))
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(n_empty), FadeIn(n_a1))
        self.play(GrowArrow(e3), GrowArrow(e4), GrowArrow(e5), Create(e6))
        self.play(FadeIn(n_empty2), FadeIn(n_a2))
        streams = caption("three streams meet in the prefix A:")
        streams2 = caption("new letter · blank extension · silent merge")
        streams.move_to(1.2 * RIGHT + 2.45 * DOWN)
        streams2.next_to(streams, DOWN, buff=0.13)
        self.play(FadeIn(streams), FadeIn(streams2))
        dp = caption("masses pouring into one prefix MERGE —")
        dp2 = caption("the move algorithms/ named: shared prefixes, stored once")
        dp.next_to(streams2, DOWN, buff=0.25)
        dp2.next_to(dp, DOWN, buff=0.13)
        self.play(FadeIn(dp), FadeIn(dp2))
        self.wait(2.4)

        # Exactness bookkeeping: the zero-mass candidate, shown at zero.
        self.play(FadeOut(wrong), FadeOut(wrong_tag), FadeOut(wrong_tag2), FadeOut(wrong_tag3))
        aa = chip("AA  0.00", MUTED, width=1.7).move_to(5.0 * LEFT + 1.0 * UP)
        on_frame(aa)
        aa_tag = caption("the third candidate")
        aa_tag2 = caption("carries exactly zero —")
        aa_tag3 = caption("width 2 keeps every")
        aa_tag4 = caption("candidate with mass")
        aa_tag.next_to(aa, DOWN, buff=0.3)
        aa_tag2.next_to(aa_tag, DOWN, buff=0.13)
        aa_tag3.next_to(aa_tag2, DOWN, buff=0.13)
        aa_tag4.next_to(aa_tag3, DOWN, buff=0.13)
        for m in (aa_tag, aa_tag2, aa_tag3, aa_tag4):
            on_frame(m)
        self.play(FadeIn(aa), FadeIn(aa_tag), FadeIn(aa_tag2), FadeIn(aa_tag3), FadeIn(aa_tag4))
        self.wait(2.2)

        self.play(FadeOut(opening))
        close = Text(
            "Pruning, when it bites, is the beam's only approximation.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(close))
        self.wait(3.6)


class TheTwoLedgers(ConceptScene):
    """p_b and p_nb per prefix — the collapse map's grammar carried into the search."""

    def construct(self):
        self.play(FadeIn(self.title("The Two Ledgers"), shift=0.3 * DOWN))
        opening = Text(
            "One subtlety makes CTC's beam unlike every textbook beam.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # A prefix carries two masses, because the two halves have different futures.
        a_chip = _ledger_chip("A", 0.24, 0.40, x=-4.3, y=1.1)
        self.play(FadeIn(a_chip))
        legend = VGroup(
            caption("ends in blank — p_b", color=PB),
            caption("ends in its letter — p_nb", color=PNB),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        legend.next_to(a_chip, DOWN, buff=0.35)
        on_frame(legend)
        self.play(FadeIn(legend))

        # The repeat fork: only the blank half can open a double letter.
        fork_tag = caption("propose the letter A onto the prefix A:")
        fork_tag.move_to(2.6 * RIGHT + 2.1 * UP)
        on_frame(fork_tag)
        aa_child = chip("AA", GOOD, width=1.3).move_to(4.6 * RIGHT + 0.6 * UP)
        on_frame(aa_child)
        door = Arrow([-3.2, 1.3, 0], aa_child.get_left(), color=PB, buff=0.15, stroke_width=4)
        merge_back = CurvedArrow(
            [-3.2, 0.9, 0], [-4.3, 0.45, 0], angle=1.2, color=PNB, stroke_width=4
        )
        door_tag = caption("only the p_b share passes — a blank", color=PB)
        door_tag2 = caption("stood between: a genuine double letter", color=PB)
        door_tag.move_to(2.6 * RIGHT + 0.0 * UP)
        door_tag2.next_to(door_tag, DOWN, buff=0.13)
        on_frame(door_tag)
        on_frame(door_tag2)
        merge_tag = caption("the p_nb share merges silently back", color=PNB)
        merge_tag.next_to(legend, DOWN, buff=0.3)
        on_frame(merge_tag)
        self.play(FadeIn(fork_tag))
        self.play(GrowArrow(door), FadeIn(aa_child), FadeIn(door_tag), FadeIn(door_tag2))
        self.play(Create(merge_back), FadeIn(merge_tag))
        self.wait(2.4)

        # Collapse the two numbers into one and the beam must lie: the coin frames.
        self.play(
            FadeOut(fork_tag),
            FadeOut(aa_child),
            FadeOut(door),
            FadeOut(merge_back),
            FadeOut(door_tag),
            FadeOut(door_tag2),
            FadeOut(merge_tag),
            FadeOut(legend),
            FadeOut(a_chip),
        )
        coin = caption("coin frames — y(A) = y(ε) = ½, three frames:")
        coin.move_to(3.6 * LEFT + 1.7 * UP)
        on_frame(coin)
        truth = VGroup(
            chip("true P(AA) = 1/8", GOOD, width=3.0),
            caption("only AεA collapses to AA"),
        ).arrange(DOWN, buff=0.18)
        truth.move_to(3.9 * LEFT + 0.55 * UP)
        on_frame(truth)
        lie = VGroup(
            chip("one ledger says 3/8", WARM, width=3.5),
            caption("it credited AAε and εAA —", color=WARM),
            caption("both truly collapse to A", color=WARM),
        ).arrange(DOWN, buff=0.16)
        lie.move_to(3.9 * LEFT + 1.35 * DOWN)
        on_frame(lie)
        wrongness = caption("a 3× overcount: wrong answers, not slow ones", color=WARM)
        wrongness.move_to(3.6 * LEFT + 2.9 * DOWN)
        on_frame(wrongness)
        self.play(FadeIn(coin))
        self.play(FadeIn(truth))
        self.play(FadeIn(lie))
        self.play(FadeIn(wrongness))

        # The repo-native close: the beam IS the forward recurrence.
        table = VGroup(
            caption("the unpruned ledgers, frame 2:"),
            MathTex(r'\text{""}: 0.36 \qquad \text{A}: 0.24 + 0.40 = 0.64', font_size=30),
            caption("digit for digit, the trellis's final column —"),
            caption("the beam is the forward recurrence"),
            caption("wearing a search harness"),
        ).arrange(DOWN, buff=0.2)
        table.move_to(3.3 * RIGHT + 0.3 * UP)
        on_frame(table)
        self.play(FadeIn(table))
        init = caption("init: p_b(∅) = 1 — before any frame,")
        init2 = caption("all mass ends in blank")
        init.move_to(3.3 * RIGHT + 1.75 * DOWN)
        init2.next_to(init, DOWN, buff=0.13)
        on_frame(init)
        on_frame(init2)
        self.play(FadeIn(init), FadeIn(init2))
        self.wait(2.4)

        self.play(FadeOut(opening))
        score = MathTex(r"P(\text{prefix}) = p_b + p_{nb}", font_size=40)
        score.move_to(3.3 * RIGHT + 3.1 * DOWN)
        on_frame(score)
        self.play(Write(score))
        self.play(Create(boxed(score, buff=0.18)))
        self.wait(3.6)


class ThePriceOfPruning(ConceptScene):
    """Width 1 answers wrong — and wrong differently from greedy. Priced exactly."""

    def construct(self):
        self.play(FadeIn(self.title("The Price of Pruning"), shift=0.3 * DOWN))
        opening = Text(
            "Pruning is the beam's only approximation. Here is its bill.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        cols = [(0.5, 0.1, 0.4), (0.5, 0.1, 0.4), (0.5, 0.4, 0.1)]
        grid, _cells, rings = _matrix(cols, x=-5.0, y=1.2, highlight=[0, 0, 0])
        self.play(FadeIn(grid), Create(rings))
        posterior = caption("exact posterior: A 0.37 · AB 0.285 · AA 0.10 …")
        posterior.next_to(grid, DOWN, buff=0.45).shift(0.7 * RIGHT)
        on_frame(posterior)
        self.play(FadeIn(posterior))

        verdicts = VGroup(
            chip("greedy → A  ✓", GOOD, width=2.6),
            chip("width 2 → A  ✓   kept 0.37", GOOD, width=4.9),
            chip("width 1 → AB  ✗", WARM, width=2.8),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        verdicts.move_to(3.4 * RIGHT + 1.0 * UP)
        on_frame(verdicts)
        for v in verdicts:
            self.play(FadeIn(v, shift=0.15 * UP), run_time=0.5)
        self.wait(1.2)
        exact_note = caption("width 2's kept total IS the posterior here —")
        exact_note2 = caption("only because no A-feeder was ever pruned")
        exact_note.move_to(3.4 * RIGHT + 0.5 * DOWN)
        exact_note2.next_to(exact_note, DOWN, buff=0.13)
        on_frame(exact_note)
        on_frame(exact_note2)
        self.play(FadeIn(exact_note), FadeIn(exact_note2))
        self.wait(2.2)

        # The mechanism: frame 1's cut deletes a fifth of all mass.
        cut = caption("width 1 at frame 1: keep A (0.5) — cut ∅ (0.4), B (0.1)")
        cut.move_to(1.4 * LEFT + 1.9 * DOWN)
        struck = caption("the cut deleted a fifth of all mass — every drop bound for A", color=WARM)
        struck.next_to(cut, DOWN, buff=0.15)
        inside = caption("frame 3, inside the beam: AB 0.18 beats A 0.17 —", color=WARM)
        inside2 = caption("wrong, and wrong differently from greedy", color=WARM)
        inside.next_to(struck, DOWN, buff=0.3)
        inside2.next_to(inside, DOWN, buff=0.13)
        self.play(FadeIn(cut))
        self.play(FadeIn(struck))
        self.play(FadeIn(inside), FadeIn(inside2))
        self.wait(2.4)

        self.play(FadeOut(opening))
        moral = Text(
            "Kept totals understate posteriors; the price is paid where mass hedges.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(moral))
        self.wait(3.6)


class TheLoopClosed(ConceptScene):
    """Greedy when peaked, the beam when hedging, the LM at the splice — deploy."""

    def construct(self):
        self.play(FadeIn(self.title("The Loop Closed"), shift=0.3 * DOWN))
        opening = Text(
            "Train on the sum; decode by the favourites or the ledgers; deploy.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # The decision rule, mapped.
        shapes = VGroup(
            caption("outputs peaked (trained CTC)"),
            caption("mass hedges (accents, noise)"),
            caption("language left on the table"),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        shapes.move_to(3.9 * LEFT + 1.0 * UP)
        on_frame(shapes)
        verdicts = VGroup(
            caption("greedy — the production default", color=GOOD),
            caption("the beam — width where it matters", color=COOL),
            caption("an LM, spliced at the extension", color=ACCENT),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        verdicts.move_to(2.9 * RIGHT + 1.0 * UP)
        on_frame(verdicts)
        arrows = VGroup(
            *[
                Arrow(s.get_right(), v.get_left(), buff=0.25, color=MUTED, stroke_width=3)
                for s, v in zip(shapes, verdicts, strict=True)
            ]
        )
        for s, a, v in zip(shapes, arrows, verdicts, strict=True):
            self.play(FadeIn(s), GrowArrow(a), FadeIn(v), run_time=0.6)
        self.wait(2.0)

        # The splice, written out — tuned, not derived.
        fusion = MathTex(
            r"Q(c) = \log P(c \mid x) + \alpha \log P_{\mathrm{lm}}(c)"
            r" + \beta\,\mathrm{word\_count}(c)",
            font_size=32,
        ).move_to(0.0 * RIGHT + 1.1 * DOWN)
        fusion_tag = caption("α, β tuned by cross-validation; beams 1000–8000 (Deep Speech)")
        fusion_tag.next_to(fusion, DOWN, buff=0.2)
        self.play(Write(fusion), FadeIn(fusion_tag))
        logspace = caption("production ledgers run in log space — the merge is the")
        logspace2 = caption("log-add the logarithms series taught, never a max")
        logspace.next_to(fusion_tag, DOWN, buff=0.3)
        logspace2.next_to(logspace, DOWN, buff=0.13)
        self.play(FadeIn(logspace), FadeIn(logspace2))
        self.wait(2.4)

        # The inherited caution, restated at deployment's door.
        self.play(FadeOut(fusion), FadeOut(fusion_tag), FadeOut(logspace), FadeOut(logspace2))
        spikes = caption("the loss never paid for timing — spike positions are")
        spikes2 = caption("not calibrated segment boundaries: a decoder returns")
        spikes3 = caption("WHAT was said; WHEN is forced alignment, another tool")
        spikes.move_to(0.0 * RIGHT + 1.3 * DOWN)
        spikes2.next_to(spikes, DOWN, buff=0.13)
        spikes3.next_to(spikes2, DOWN, buff=0.13)
        self.play(FadeIn(spikes), FadeIn(spikes2), FadeIn(spikes3))
        self.wait(2.4)

        # The loop, closed.
        self.play(FadeOut(opening))
        loop = (
            VGroup(
                chip("waveform", MUTED, width=1.9),
                chip("weights", COOL, width=1.7),
                chip("words", GOOD, width=1.6),
            )
            .arrange(RIGHT, buff=1.1)
            .move_to(2.9 * DOWN)
        )
        loop_arrows = VGroup(
            *[
                Arrow(a.get_right(), b.get_left(), buff=0.12, color=MUTED, stroke_width=3)
                for a, b in zip(loop[:-1], loop[1:], strict=True)
            ]
        )
        self.play(FadeIn(loop), GrowArrow(loop_arrows[0]), GrowArrow(loop_arrows[1]))
        closed = Text(
            "The road's loop is closed.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(closed))
        self.wait(4.0)


if __name__ == "__main__":
    raise SystemExit(render_cli())
