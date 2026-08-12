"""The CTC gradient — softmax output minus how often the truth used each cell.

Seven scenes. The alignment series ended with the forward trellis computing
P(Y|X); this one differentiates it, and the promise the softmax and
derivative closers spoke on screen — "every frame of CTC hands this exact
picture a different target" — is kept.

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

import numpy as np
from manim import *

from utils import (
    ACCENT,
    BODY_SIZE,
    COOL,
    GOOD,
    MUTED,
    SMALL_SIZE,
    WARM,
    ConceptScene,
    boxed,
    caption,
    clear_of,
    on_frame,
    palette,
    render_cli,
    token,
)

# Same blank glyph as the alignment series — the two modules share a grid.
EPS = "ε"

# The extended target for Y = AB and its row colours, exactly as
# TheForwardTrellis drew them: letters take the categorical cycle, the
# blank is scaffolding the eye should treat as quiet.
Z_PRIME = [EPS, "A", EPS, "B", EPS]
ROW_COLORS = [MUTED, palette(0), MUTED, palette(1), MUTED]
CLASSES = ["A", "B", EPS]
CLASS_COLORS = [palette(0), palette(1), MUTED]

# --- Plan-010 verified tables (anchor letters refer to the plan) -----------
# The per-frame softmax matrix; columns t=1..4, rows A/B/ε. Columns 1-3 are
# the plan-008 matrix TheLossThatTrains scored; column 4 is anchor K's
# ratified extension.
Y_MATRIX = [
    [0.7, 0.6, 0.2, 0.1],
    [0.2, 0.1, 0.1, 0.7],
    [0.1, 0.3, 0.7, 0.2],
]

# Unit-weight path counts, stored column-major (one list per frame, rows
# s = 1..5 over ε A ε B ε). Forward counts are plan 001's; backward counts
# are anchor P (the forward table read in a mirror).
FWD_COUNTS = [[1, 1, 0, 0, 0], [1, 2, 1, 1, 0], [1, 3, 3, 4, 1], [1, 4, 6, 10, 5]]
BWD_COUNTS = [[5, 10, 6, 4, 1], [1, 4, 3, 3, 1], [0, 1, 1, 2, 1], [0, 0, 0, 1, 1]]

# α, β (2012 convention: β starts at t+1, β_T = 1 at the two final states)
# and γ = αβ/P on the real matrix — anchor K, column-major.
ALPHA = [
    [0.1, 0.7, 0, 0, 0],
    [0.03, 0.48, 0.21, 0.07, 0],
    [0.021, 0.102, 0.483, 0.076, 0.049],
    [0.0042, 0.0123, 0.117, 0.4627, 0.025],
]
BETA = [
    [0.474, 0.629, 0.197, 0.065, 0.042],
    [0.14, 0.72, 0.58, 0.23, 0.14],
    [0, 0.7, 0.7, 0.9, 0.2],
    [0, 0, 0, 1, 1],
]
GAMMA = [
    [0.0972, 0.9028, 0, 0, 0],
    [0.0086, 0.7086, 0.2497, 0.0330, 0],
    [0, 0.1464, 0.6933, 0.1403, 0.0201],
    [0, 0, 0, 0.9487, 0.0513],
]
P_TRUTH = 0.4877  # P(AB|X), exact — anchor K

# Per-class occupancy and the gradient y − γ, rows t=1..4, classes A/B/ε —
# anchor K. Row sums are digit-exact at 4 dp (FLAG 11), so the scenes may
# show the sums on screen.
OCC = [
    [0.9028, 0, 0.0972],
    [0.7086, 0.0330, 0.2584],
    [0.1464, 0.1403, 0.7133],
    [0, 0.9487, 0.0513],
]
GRAD = [
    [-0.2028, 0.2000, 0.0028],
    [-0.1086, 0.0670, 0.0416],
    [0.0536, -0.0403, -0.0133],
    [0.1000, -0.2487, 0.1487],
]

# Trellis geometry — identical to TheForwardTrellis, so the viewer returns
# to a picture they own. Off-centre left: the readouts need the right margin.
GRID_XS = [-2.6 + 1.75 * t for t in range(4)]
GRID_YS = [1.3 - 0.95 * s for s in range(5)]


def _skip_targets(s: int) -> list[int]:
    """Rows reachable from row `s` in one frame — stay, advance, legal skip."""
    targets = [s, s + 1]
    if s + 2 <= 4 and Z_PRIME[s + 2] != EPS and Z_PRIME[s + 2] != Z_PRIME[s]:
        targets.append(s + 2)
    return [s2 for s2 in targets if s2 <= 4]


def _trellis(background_color) -> dict:
    """The (2U+1) x T grid of the alignment series, ready to fade in.

    Returns the pieces separately so scenes can highlight rows, columns and
    edge bundles; `group` carries everything for a single FadeIn/FadeOut.
    """
    row_labels = VGroup(
        *[
            token(ch, color, radius=0.26).move_to(np.array([-4.2, y, 0]))
            for ch, color, y in zip(Z_PRIME, ROW_COLORS, GRID_YS, strict=True)
        ]
    )
    col_labels = VGroup(
        *[
            Text(f"t={t + 1}", font_size=SMALL_SIZE, color=COOL).move_to(
                # 0.62 rather than the alignment module's 0.55: this module
                # draws boxes around whole columns, and the labels must clear
                # their top edge.
                np.array([x, GRID_YS[0] + 0.62, 0])
            )
            for t, x in enumerate(GRID_XS)
        ]
    )
    nodes = [
        [
            Circle(radius=0.3, color=MUTED, stroke_width=2)
            .set_fill(background_color, opacity=1.0)
            .move_to(np.array([x, y, 0]))
            for y in GRID_YS
        ]
        for x in GRID_XS
    ]
    edges = VGroup()
    for t in range(3):
        for s in range(5):
            for s2 in _skip_targets(s):
                edges.add(
                    Line(
                        nodes[t][s].get_center(),
                        nodes[t + 1][s2].get_center(),
                        color=MUTED,
                        stroke_width=2,
                        stroke_opacity=0.6,
                    )
                )
    node_group = VGroup(*[n for column in nodes for n in column])
    return {
        "row_labels": row_labels,
        "col_labels": col_labels,
        "nodes": nodes,
        "node_group": node_group,
        "edges": edges,
        "group": VGroup(row_labels, col_labels, edges, node_group),
    }


def _fill_columns(scene, nodes, columns, font_size=22, color=None, reverse=False):
    """Drop a number into every live node, one column at a time.

    `columns` is column-major; zeros stay visually empty, exactly as the
    alignment series drew dead states. `reverse` fills right-to-left — the
    order a backward recurrence actually runs. Returns the column-major
    grid of Text mobjects (None where empty).
    """
    figures: list[list[Text | None]] = [[None] * 5 for _ in range(4)]
    order = reversed(range(len(columns))) if reverse else range(len(columns))
    for t in order:
        entering = VGroup()
        for s, value in enumerate(columns[t]):
            if value == 0:
                continue
            # Strings pass through untouched so a scene can pin the exact
            # display precision of a verified number ("0.0250", "8/15").
            label = value if isinstance(value, str) else f"{value:g}"
            # color=None keeps Text's own default (the counting scenes' look)
            # without naming a raw manim constant.
            kwargs = {"color": color} if color is not None else {}
            figure = Text(label, font_size=font_size, **kwargs).move_to(nodes[t][s])
            figures[t][s] = figure
            entering.add(figure)
        scene.play(
            LaggedStart(*[FadeIn(f, scale=0.6) for f in entering], lag_ratio=0.1),
            run_time=0.7,
        )
    return figures


def _figures_group(figures) -> VGroup:
    return VGroup(*[f for column in figures for f in column if f is not None])


class TheOtherHalfOfTheTrellis(ConceptScene):
    """β: α answered "how did we get here?" — β answers "how do we finish?"."""

    def construct(self):
        self.play(FadeIn(self.title("The Other Half of the Trellis"), shift=0.3 * DOWN))

        opening = Text(
            "α counted the ways into each cell. β counts the ways out.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        trellis = _trellis(self.camera.background_color)
        recall = caption("the alignment series' grid — same rows, same skip rule")
        recall.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(trellis["group"]), FadeIn(recall))
        self.wait(0.6)

        # --- backward counts, right to left ------------------------------------
        self.play(FadeOut(opening), FadeOut(recall))
        note = Text(
            "count the ways to finish — each column needs only the column after it",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(note))
        nodes = trellis["nodes"]
        figures: list[list[Text | None]] = [[None] * 5 for _ in range(4)]
        for t in (3, 2, 1, 0):
            entering = VGroup()
            for s, value in enumerate(BWD_COUNTS[t]):
                if value == 0:
                    continue
                figure = Text(str(value), font_size=22).move_to(nodes[t][s])
                figures[t][s] = figure
                entering.add(figure)
            self.play(
                LaggedStart(*[FadeIn(f, scale=0.6) for f in entering], lag_ratio=0.1),
                run_time=0.7,
            )
        self.wait(0.4)

        # One node opened: β at (t=2, A) gathers stay, advance and the skip —
        # the same three edges as the forward 4, now read the other way.
        succs = [nodes[2][1], nodes[2][2], nodes[2][3]]
        flash = VGroup(
            *[
                Line(nodes[1][1].get_center(), s.get_center(), color=ACCENT, stroke_width=4)
                for s in succs
            ]
        )
        arithmetic = MathTex(r"1 + 1 + 2 = 4", font_size=32, color=ACCENT)
        arithmetic.to_edge(DOWN, buff=0.45)
        self.play(Create(flash), Write(arithmetic))
        self.wait(0.9)
        self.play(FadeOut(flash), FadeOut(arithmetic))

        # --- the mirror ---------------------------------------------------------
        mirror = caption(
            "this palindrome's mirror — the forward table time-reversed, A and B swapped"
        )
        mirror.to_edge(DOWN, buff=0.4)
        starts = VGroup(nodes[0][0], nodes[0][1])
        start_box = SurroundingRectangle(starts, color=ACCENT, buff=0.1, corner_radius=0.12)
        # The readout lives in the right margin — left of the start states is
        # row-label territory.
        total = MathTex(r"5 + 10 = 15", font_size=40, color=ACCENT).move_to([4.6, 1.1, 0])
        on_frame(total)
        self.play(FadeIn(mirror))
        self.play(Create(start_box), Write(total))
        recall15 = caption("the same 15 —\nfrom the other end").next_to(total, DOWN, buff=0.3)
        on_frame(recall15)
        self.play(FadeIn(recall15))
        self.wait(1.0)

        # --- the ledger cut -----------------------------------------------------
        # Each frame's emission is a coin exactly one variable may pocket. The
        # cut goes between t and t+1: α owns its own column, β starts after it.
        self.play(FadeOut(mirror), FadeOut(note))
        cut_x = (GRID_XS[1] + GRID_XS[2]) / 2
        cut = DashedLine(
            np.array([cut_x, GRID_YS[0] + 0.75, 0]),
            np.array([cut_x, GRID_YS[4] - 0.45, 0]),
            color=WARM,
            stroke_width=3,
        )
        ledger = Text(
            "each frame's probability is a coin exactly one variable may pocket",
            font_size=SMALL_SIZE,
        ).to_edge(DOWN, buff=0.75)
        ledger2 = caption("α's column pockets frame t's y — β starts at t+1")
        ledger2.next_to(ledger, DOWN, buff=0.18)
        # Above the column labels, not beside the cut's top — the labels own
        # the 1.9-band and the tags collided with them there.
        alpha_tag = MathTex(r"\alpha", font_size=36, color=COOL).move_to([cut_x - 0.55, 2.45, 0])
        beta_tag = MathTex(r"\beta", font_size=36, color=ACCENT).move_to([cut_x + 0.55, 2.45, 0])
        self.play(FadeIn(ledger), Create(cut), FadeIn(alpha_tag), FadeIn(beta_tag))
        self.play(FadeIn(ledger2))
        self.wait(1.1)
        self.play(
            FadeOut(VGroup(cut, alpha_tag, beta_tag, ledger, ledger2, start_box, total, recall15))
        )

        # --- real weights land --------------------------------------------------
        weights = Text(
            "now the real per-frame probabilities — the matrix the softmax series scored",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(weights), FadeOut(_figures_group(figures)))
        beta_figures = _fill_columns(self, nodes, BETA, font_size=17, reverse=True)
        self.wait(0.3)
        # Below the grid: the grid's lowest circles bottom out at -2.8, so
        # the readout and its one-line caption stack under them.
        readout = MathTex(
            r"0.1 \times 0.474 + 0.7 \times 0.629 = 0.4877",
            font_size=30,
            color=ACCENT,
        ).move_to([-0.8, -3.3, 0])
        readout_tag = caption(
            "weight the two start states by frame 1 — the number, from the other end"
        )
        readout_tag.next_to(readout, DOWN, buff=0.18)
        on_frame(readout_tag)
        self.play(Write(readout))
        self.play(FadeIn(readout_tag))
        self.wait(1.1)

        # --- the formula this sweep is ------------------------------------------
        self.play(
            FadeOut(trellis["group"]),
            FadeOut(_figures_group(beta_figures)),
            FadeOut(VGroup(weights, readout, readout_tag)),
        )
        base = MathTex(
            r"\beta_T(s) = 1 \text{ at the two final states}",
            font_size=40,
            color=ACCENT,
        ).move_to(1.35 * UP)
        formula = MathTex(
            r"\beta_t(s) = \sum_{i} \beta_{t+1}(s{+}i)\, y_{t+1}(z'_{s+i})",
            font_size=40,
            color=ACCENT,
        ).move_to(0.45 * UP)
        formula_note = caption("each successor weighted by its own frame-(t+1) probability;")
        formula_note2 = caption("the skip term only where the alignment grid allows it")
        formula_note.move_to(0.35 * DOWN)
        formula_note2.next_to(formula_note, DOWN, buff=0.15)
        self.play(Write(base))
        self.play(Write(formula))
        self.play(FadeIn(formula_note), FadeIn(formula_note2))
        lineage = caption("the backward half of forward–backward — the HMM lineage (Rabiner 1989)")
        lineage.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(lineage))
        self.wait(1.6)


class PathsThroughACell(ConceptScene):
    """α·β is the probability of the truth's paths through a cell — and every column sums to P."""

    def construct(self):
        self.play(FadeIn(self.title("Paths Through a Cell"), shift=0.3 * DOWN))

        opening = Text(
            "α knows the ways in. β knows the ways out. Multiply.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        trellis = _trellis(self.camera.background_color)
        self.play(FadeIn(trellis["group"]))
        nodes = trellis["nodes"]

        # --- one cell as a waist ------------------------------------------------
        # Everything left of (t=2, A) converges in; everything right diverges
        # out. Prefixes times suffixes — the multiplicative rule, weighted.
        cell = nodes[1][1]
        waist = SurroundingRectangle(cell, color=ACCENT, buff=0.1, corner_radius=0.12)
        into = VGroup(
            *[
                Line(nodes[0][s].get_center(), cell.get_center(), color=COOL, stroke_width=4)
                for s in (0, 1)
            ]
        )
        out_of = VGroup(
            *[
                Line(cell.get_center(), nodes[2][s].get_center(), color=ACCENT, stroke_width=4)
                for s in (1, 2, 3)
            ]
        )
        self.play(Create(waist), Create(into), Create(out_of))
        # The "2" and "4" wear the bundle colours instead of floating labels —
        # the grid's airspace is full of edges.
        product = MathTex(
            r"{{2}} \times {{4}} = 8 \text{ of the 15 paths cross here}", font_size=32
        )
        product.set_color(ACCENT)
        product[0].set_color(COOL)
        product.to_edge(DOWN, buff=0.85)
        rule = caption("the multiplicative rule from counting — now carrying probability")
        rule.next_to(product, DOWN, buff=0.2)
        self.play(Write(product), FadeIn(rule))
        self.wait(1.1)
        self.play(FadeOut(VGroup(waist, into, out_of, product, rule, opening)))

        # --- the checksum at unit weights ---------------------------------------
        note = Text(
            "α·β in every cell — then sum each column",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(note))
        unit_products = [
            [a * b for a, b in zip(fc, bc, strict=True)]
            for fc, bc in zip(FWD_COUNTS, BWD_COUNTS, strict=True)
        ]
        figures = _fill_columns(self, nodes, unit_products, font_size=22)
        sums = VGroup()
        sweep = None
        for t in range(4):
            column = VGroup(*[nodes[t][s] for s in range(5)])
            new_sweep = SurroundingRectangle(column, color=COOL, buff=0.12, corner_radius=0.12)
            total = Text("15", font_size=24, color=ACCENT).next_to(new_sweep, DOWN, buff=0.12)
            if sweep is None:
                self.play(Create(new_sweep), FadeIn(total))
            else:
                self.play(ReplacementTransform(sweep, new_sweep), FadeIn(total))
            sweep = new_sweep
            sums.add(total)
        why = caption("every path crosses every column exactly once")
        why.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(why))
        self.wait(1.1)

        # --- the checksum on the real matrix ------------------------------------
        self.play(FadeOut(VGroup(sweep, sums, why, note)), FadeOut(_figures_group(figures)))
        real_note = Text(
            "real weights: the same sweep, the same constant",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(real_note))
        # Anchor Q: per-cell α·β products at 4 dp; each column sums to 0.4877
        # exactly, and the 4-dp cells sum to it digit-by-digit too.
        real_products = [
            ["0.0474", "0.4403", 0, 0, 0],
            ["0.0042", "0.3456", "0.1218", "0.0161", 0],
            [0, "0.0714", "0.3381", "0.0684", "0.0098"],
            [0, 0, 0, "0.4627", "0.0250"],
        ]
        real_figures = _fill_columns(self, nodes, real_products, font_size=13)
        real_sums = VGroup()
        sweep = None
        for t in range(4):
            column = VGroup(*[nodes[t][s] for s in range(5)])
            new_sweep = SurroundingRectangle(column, color=COOL, buff=0.12, corner_radius=0.12)
            total = Text("0.4877", font_size=20, color=ACCENT).next_to(new_sweep, DOWN, buff=0.12)
            if sweep is None:
                self.play(Create(new_sweep), FadeIn(total))
            else:
                self.play(ReplacementTransform(sweep, new_sweep), FadeIn(total))
            sweep = new_sweep
            real_sums.add(total)
        constant = caption("P(AB | X) = 0.4877 — four sweeps, one number")
        constant.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(constant))
        self.wait(1.0)
        check = caption("a double-pocketed emission would scale its column — the sweep catches it")
        self.play(FadeOut(constant))
        check.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(check))
        self.wait(1.0)

        # --- the formula this sweep is ------------------------------------------
        self.play(
            FadeOut(trellis["group"]),
            FadeOut(_figures_group(real_figures)),
            FadeOut(VGroup(sweep, real_sums, check, real_note)),
        )
        formula = MathTex(
            r"P(Y \mid X) \;=\; \sum_{s} \alpha_t(s)\,\beta_t(s)"
            r"\qquad \text{for any } t",
            font_size=46,
            color=ACCENT,
        ).move_to(0.85 * UP)
        closing = caption("the constant column — the identity the gradient is about to lean on")
        closing.move_to(0.25 * DOWN)
        self.play(Write(formula))
        self.play(FadeIn(closing))
        self.wait(1.6)


class WhereTheTruthSpendsItsTime(ConceptScene):
    """Occupancy: divide each column by its own sum and it becomes the truth's soft target."""

    def construct(self):
        self.play(FadeIn(self.title("Where the Truth Spends Its Time"), shift=0.3 * DOWN))

        opening = Text(
            "Divide each column by its own sum.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        trellis = _trellis(self.camera.background_color)
        self.play(FadeIn(trellis["group"]))
        nodes = trellis["nodes"]
        # The α·β products of the previous scene, divided through by their
        # constant column sum: each column becomes a distribution, γ.
        divide = MathTex(r"\div\ 0.4877", font_size=32, color=ACCENT)
        divide.next_to(trellis["group"], RIGHT, buff=0.4).shift(0.5 * UP)
        on_frame(divide)
        gamma_display = [[f"{v:.4f}" if v else 0 for v in column] for column in GAMMA]
        gamma_figures = _fill_columns(self, nodes, gamma_display, font_size=13, color=GOOD)
        self.play(Write(divide))
        ones = VGroup()
        for t in range(4):
            column = VGroup(*[nodes[t][s] for s in range(5)])
            # The cells are rounded to 4 dp; only the exact column sum is 1
            # (the 4-dp digits add to 0.9999 at t=2 and 1.0001 at t=3 —
            # FLAG 11's digit-exactness covers the OCC/GRAD rows, not these
            # 5-state columns).
            one = MathTex(r"= 1", font_size=24, color=GOOD).next_to(column, DOWN, buff=0.25)
            ones.add(one)
        self.play(LaggedStart(*[FadeIn(o) for o in ones], lag_ratio=0.15))
        named = caption("γ — each column a distribution: where the truth spends frame t")
        named.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(named))
        self.wait(1.0)
        why = caption("columns sum to 1 because each path occupies exactly one cell per frame")
        self.play(FadeOut(named))
        why.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(why))
        self.wait(1.0)
        # The conditional series' own move, named: dividing a slice by its
        # own mass is renormalization, and the condition here is Y.
        renorm = caption("the renormalized slice again — this time conditioned on the transcript")
        self.play(FadeOut(why))
        renorm.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(renorm))
        self.wait(1.0)

        # --- fold states into classes, once -------------------------------------
        # lab(z, k): the blank owns three rows; a class's occupancy is a sum
        # over its states. Drawn exactly once, here, before any bars claim
        # to be γ.
        self.play(FadeOut(opening), FadeOut(renorm), FadeOut(divide))
        fold_note = Text(
            "blank owns three rows — a class's occupancy sums its states",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(fold_note))
        t_show = 1  # column t=2, the richest column
        col_box = SurroundingRectangle(
            VGroup(*[nodes[t_show][s] for s in range(5)]),
            color=GOOD,
            buff=0.12,
            corner_radius=0.12,
        )
        # Three bars side by side in the right margin: the folded column.
        bars = VGroup()
        for i, (label, color, value) in enumerate(
            zip(CLASSES, CLASS_COLORS, OCC[t_show], strict=True)
        ):
            x = 3.6 + i * 1.05
            bar = Rectangle(
                width=0.6,
                height=max(value * 2.4, 0.02),
                stroke_width=2,
                color=color,
                fill_color=color,
                fill_opacity=0.35,
            ).move_to([x, -0.6 + value * 1.2, 0])
            tag = Text(label, font_size=SMALL_SIZE, color=MUTED).move_to([x, -0.95, 0])
            val = Text(f"{value:.4f}", font_size=15, color=color).next_to(bar, UP, buff=0.12)
            bars.add(VGroup(bar, tag, val))
        bars_title = Text("t=2, by class", font_size=SMALL_SIZE, color=GOOD)
        bars_title.move_to([4.75, 1.75, 0])
        on_frame(bars_title)
        self.play(Create(col_box))
        self.play(FadeIn(bars), FadeIn(bars_title))
        self.wait(1.1)

        # --- rows are expectations, not probabilities ---------------------------
        self.play(FadeOut(fold_note), FadeOut(col_box))
        row_note = Text(
            "rows are NOT probabilities — A's row sums to 1.7578 frames",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        row_box = SurroundingRectangle(
            VGroup(*[nodes[t][1] for t in range(4)]),
            color=palette(0),
            buff=0.16,
            corner_radius=0.12,
        )
        dwell = caption("an expected dwell time — the balance point, back under new weights")
        dwell.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(row_note), Create(row_box))
        self.play(FadeIn(dwell))
        self.wait(1.1)

        # --- strip the input away: uniform outputs ------------------------------
        self.play(
            FadeOut(VGroup(row_note, row_box, dwell, bars, bars_title, ones)),
            FadeOut(_figures_group(gamma_figures)),
        )
        uniform_note = Text(
            "make every output 1/3 — γ collapses to path counts over 15",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(uniform_note))
        uniform = [
            ["5/15", "10/15", 0, 0, 0],
            ["1/15", "8/15", "3/15", "3/15", 0],
            [0, "3/15", "3/15", "8/15", "1/15"],
            [0, 0, 0, "10/15", "5/15"],
        ]
        uniform_figures: list[list[Text | None]] = [[None] * 5 for _ in range(4)]
        for t in range(4):
            entering = VGroup()
            for s, value in enumerate(uniform[t]):
                if value == 0:
                    continue
                figure = Text(value, font_size=14, color=GOOD).move_to(nodes[t][s])
                uniform_figures[t][s] = figure
                entering.add(figure)
            self.play(
                LaggedStart(*[FadeIn(f, scale=0.6) for f in entering], lag_ratio=0.1),
                run_time=0.6,
            )
        counting = caption("the alignment series' counting scene, reborn as a target")
        counting.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(counting))
        dwell_sum = MathTex(
            r"\text{dwell: } 1.4 + 1.4 + 1.2 = 4 = T",
            font_size=26,
            color=ACCENT,
        ).move_to([5.1, 0.9, 0])
        on_frame(dwell_sum)
        self.play(Write(dwell_sum))
        self.wait(1.2)

        # --- the formula, and the promise's phrase ------------------------------
        self.play(
            FadeOut(trellis["group"]),
            FadeOut(_figures_group(uniform_figures)),
            FadeOut(VGroup(uniform_note, counting, dwell_sum)),
        )
        formula = MathTex(
            r"\gamma_t(s) \;=\; \frac{\alpha_t(s)\,\beta_t(s)}{P(Y \mid X)}",
            font_size=44,
            color=ACCENT,
        ).move_to(1.9 * UP)
        self.play(Write(formula))

        # The promised juxtaposition: a γ column stood beside the one-hot
        # bar the calculus series left on screen — the target, gone soft.
        trios = VGroup()
        for x0, values, colors, labels, title_text in (
            (
                -3.7,
                OCC[1],
                CLASS_COLORS,
                [f"{v:.4f}" for v in OCC[1]],
                "γ at t=2 — gone soft",
            ),
            (1.6, [1, 0, 0], [COOL] * 3, ["1", "0", "0"], "the one-from-N you know"),
        ):
            trio = VGroup()
            for i, (cls, color, value, label) in enumerate(
                zip(CLASSES, colors, values, labels, strict=True)
            ):
                x = x0 + i * 1.05
                height = max(value * 1.6, 0.02)
                trio.add(
                    Rectangle(
                        width=0.55,
                        height=height,
                        stroke_width=2,
                        color=color,
                        fill_color=color,
                        fill_opacity=0.35,
                    ).move_to([x, -1.2 + height / 2, 0])
                )
                trio.add(Text(cls, font_size=SMALL_SIZE, color=MUTED).move_to([x, -1.55, 0]))
                trio.add(
                    Text(label, font_size=14, color=color).move_to([x, -1.2 + height + 0.2, 0])
                )
            trio.add(
                Text(title_text, font_size=SMALL_SIZE, color=GOOD if x0 < 0 else COOL).move_to(
                    [x0 + 1.05, 0.95, 0]
                )
            )
            trios.add(trio)
        self.play(FadeIn(trios[1]))
        self.play(FadeIn(trios[0]))
        phrase = Text(
            '"how often the truth used each cell" — the promise, now an object',
            font_size=BODY_SIZE,
        ).move_to(2.45 * DOWN)
        lineage = caption("the soft alignment implementations compute — Baum–Welch's E-step object")
        lineage.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(phrase))
        self.play(FadeIn(lineage))
        self.wait(1.6)


class TheSensitivityOfTheSum(ConceptScene):
    """Nudge one cell's probability and the loss moves by exactly that cell's occupancy."""

    def construct(self):
        self.play(FadeIn(self.title("The Sensitivity of the Sum"), shift=0.3 * DOWN))

        opening = Text(
            "Nudge one cell. How much does the loss care?",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # --- P is linear in any single cell -------------------------------------
        linear = MathTex(
            r"P(Y \mid X) \;=\; \underbrace{C}_{\text{paths through the cell}}"
            r" \cdot\, y_2(A) \;+\; \underbrace{D}_{\text{paths that miss it}}",
            font_size=40,
        ).move_to(1.2 * UP)
        why_linear = caption("each path uses frame 2 exactly once — the variable appears")
        why_linear2 = caption("to power 0 or 1, so the sum is linear in it")
        why_linear.move_to(0.05 * UP)
        why_linear2.next_to(why_linear, DOWN, buff=0.15)
        slope = Text(
            "the slope of a linear function is its coefficient — no new calculus",
            font_size=SMALL_SIZE,
        ).move_to(1.0 * DOWN)
        self.play(Write(linear))
        self.play(FadeIn(why_linear), FadeIn(why_linear2))
        self.play(FadeIn(slope))
        self.wait(1.1)

        # --- the multiplicative nudge -------------------------------------------
        self.play(FadeOut(VGroup(linear, why_linear, why_linear2, slope, opening)))
        nudge_head = Text(
            "scale the cell instead: multiply y₂(A) by (1 + h)",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        scale_fact = MathTex(
            r"\text{every path through the cell scales by } (1+h)"
            r"\text{ — every other path stands still}",
            font_size=34,
        ).move_to(1.3 * UP)
        moves = MathTex(
            r"\Delta \ln P \;\approx\; \gamma_2(A) \cdot h",
            font_size=42,
            color=ACCENT,
        ).move_to(0.45 * UP)
        share_read = MathTex(
            r"\frac{\partial \ln P}{\partial \ln y_2(A)} = \gamma_2(A) = 0.7086",
            font_size=40,
            color=ACCENT,
        ).move_to(0.55 * DOWN)
        lse_recall = caption("in LSE each term owned its own score; here 8 of the 15 paths")
        lse_recall2 = caption("share the cell — their shares add into occupancy")
        lse_recall.move_to(1.55 * DOWN)
        lse_recall2.next_to(lse_recall, DOWN, buff=0.15)
        self.play(FadeIn(nudge_head))
        self.play(Write(scale_fact))
        self.play(Write(moves))
        self.play(Write(share_read))
        self.play(FadeIn(lse_recall), FadeIn(lse_recall2))
        self.wait(1.3)

        # --- the score function does the bookkeeping ----------------------------
        self.play(
            FadeOut(VGroup(nudge_head, scale_fact, moves, share_read, lse_recall, lse_recall2))
        )
        score_head = Text(
            "the score function again: d ln f = f′/f",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        score_note = caption("products become sums of relative rates — the move that found")
        score_note2 = caption("the likelihood's peak now reads the trellis")
        score_note.move_to(1.35 * UP)
        score_note2.next_to(score_note, DOWN, buff=0.15)
        formula = MathTex(
            r"\frac{\partial L}{\partial \ln y_t(k)} \;=\; -\,\gamma_t(k)",
            font_size=48,
            color=ACCENT,
        ).move_to(0.15 * DOWN)
        reading = Text(
            "the loss listens to a cell exactly as often as the truth uses it",
            font_size=BODY_SIZE,
        ).move_to(1.25 * DOWN)
        self.play(FadeIn(score_head))
        self.play(FadeIn(score_note), FadeIn(score_note2))
        self.play(Write(formula))
        self.play(FadeIn(reading))
        self.wait(1.6)


class SoftmaxMinusOccupancy(ConceptScene):
    """The identity: the per-frame gradient of the CTC loss is softmax output minus occupancy."""

    def construct(self):
        self.play(FadeIn(self.title("Softmax Minus Occupancy"), shift=0.3 * DOWN))

        opening = Text(
            "Each frame's outputs come from a softmax. Finish the chain.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # --- the derivation, in owned steps -------------------------------------
        jacobian = MathTex(
            r"\frac{\partial \ln y_j}{\partial u_k} = \delta_{jk} - y_k",
            font_size=40,
        ).move_to(1.75 * UP)
        jacobian_note = caption("one line from ∇LSE = softmax — the toolkit's identity")
        jacobian_note.next_to(jacobian, DOWN, buff=0.18)
        chain = MathTex(
            r"\frac{\partial L}{\partial u_k}"
            r" = \sum_j \gamma_j\,(y_k - \delta_{jk})"
            r" = y_k \underbrace{\textstyle\sum_j \gamma_j}_{=\,1} - \gamma_k",
            font_size=40,
        ).move_to(0.55 * DOWN)
        checksum_note = caption("the constant column, load-bearing: the shares sum to 1")
        checksum_note.next_to(chain, DOWN, buff=0.3)
        self.play(Write(jacobian), FadeIn(jacobian_note))
        self.play(Write(chain))
        self.play(FadeIn(checksum_note))
        self.wait(1.2)

        self.play(FadeOut(VGroup(jacobian, jacobian_note, chain, checksum_note, opening)))
        identity = MathTex(
            r"\frac{\partial L}{\partial u_t(k)} \;=\; y_t(k) - \gamma_t(k)",
            font_size=52,
            color=ACCENT,
        ).move_to(1.35 * UP)
        sign_note = caption("the slope of the loss — descending it climbs the likelihood")
        sign_note.next_to(identity, DOWN, buff=0.25)
        self.play(Write(identity))
        self.play(FadeIn(sign_note))
        self.wait(0.8)

        # --- the table, on the owned matrix -------------------------------------
        rows = [
            r"t=1:\ -0.2028 \;\; +0.2000 \;\; +0.0028",
            r"t=2:\ -0.1086 \;\; +0.0670 \;\; +0.0416",
            r"t=3:\ +0.0536 \;\; -0.0403 \;\; -0.0133",
            r"t=4:\ +0.1000 \;\; -0.2487 \;\; +0.1487",
        ]
        header_row = MathTex(r"\quad\ A \qquad\quad B \qquad\quad \varepsilon", font_size=28)
        header_row.set_color(MUTED)
        header_row.move_to(3.35 * LEFT + 0.15 * DOWN)
        table = VGroup(
            *[
                MathTex(row, font_size=28).move_to(3.35 * LEFT + (0.65 + 0.55 * i) * DOWN)
                for i, row in enumerate(rows)
            ]
        )
        sums_note = caption("every row sums to 0.0000 — a nudge that")
        sums_note2 = caption("re-slices probability never adds any")
        sums_note.move_to(3.35 * LEFT + 2.95 * DOWN)
        on_frame(sums_note)
        clear_of(sums_note, table[3])
        # next_to is a one-time placement — it must come after clear_of has
        # settled sums_note, or the second line strands where the first was.
        sums_note2.next_to(sums_note, DOWN, buff=0.15)
        on_frame(sums_note2)
        self.play(FadeIn(header_row), FadeIn(table))
        self.play(FadeIn(sums_note), FadeIn(sums_note2))

        # Frame 1 opened: the truth never uses B there, so the whole B bar is
        # overcount — its gradient is exactly its own output.
        b_read = MathTex(
            r"t{=}1,\ B:\ \gamma = 0 \ \Rightarrow\ \text{gradient} = y = +0.2000",
            font_size=30,
            color=WARM,
        ).move_to(3.15 * RIGHT + 0.85 * DOWN)
        on_frame(b_read)
        b_note = caption("never used by the truth:\nthe whole bar is overcount")
        b_note.next_to(b_read, DOWN, buff=0.25)
        on_frame(b_note)
        self.play(Write(b_read))
        self.play(FadeIn(b_note))
        self.wait(1.2)

        # --- degeneration: one path survives ------------------------------------
        self.play(
            FadeOut(VGroup(header_row, table, sums_note, sums_note2, b_read, b_note, sign_note))
        )
        degen_head = Text(
            "let one path carry everything — γ's columns snap to one-hot",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        degen = MathTex(
            r"y - \gamma \;\longrightarrow\; p - \text{one-hot}",
            font_size=44,
            color=ACCENT,
        ).move_to(0.45 * UP)
        recall = MathTex(
            r"(-0.3348,\ 0.2447,\ 0.0900)",
            font_size=36,
        ).move_to(0.35 * DOWN)
        bridle = caption('Bridle\'s "output minus a one-from-N target" — the target, gone soft')
        bridle.move_to(1.15 * DOWN)
        promise = Text(
            '"every frame of CTC hands this exact picture a different target" — kept',
            font_size=SMALL_SIZE,
            color=GOOD,
        ).move_to(1.85 * DOWN)
        self.play(FadeIn(degen_head))
        self.play(Write(degen))
        self.play(Write(recall))
        self.play(FadeIn(bridle))
        self.play(FadeIn(promise))
        self.wait(1.3)

        # --- the gradient reads the target, not the letters ---------------------
        self.play(FadeOut(VGroup(degen_head, degen, recall, bridle, promise)))
        swap_head = Text(
            "score the wrong transcript — BA instead of AB",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        swap = MathTex(
            r"t{=}1,\ A:\ \text{state unreachable} \ \Rightarrow\ \gamma = 0"
            r"\ \Rightarrow\ \text{gradient} = +0.7000",
            font_size=34,
        ).move_to(0.35 * UP)
        swap_note = caption("the same output that was rewarded is now pure overcount —")
        swap_note2 = caption("the gradient reads the target's trellis, not the letters")
        swap_note.move_to(0.55 * DOWN)
        swap_note2.next_to(swap_note, DOWN, buff=0.15)
        self.play(FadeIn(swap_head))
        self.play(Write(swap))
        self.play(FadeIn(swap_note), FadeIn(swap_note2))
        self.wait(1.2)

        # --- when useful: the identity in the wild ------------------------------
        self.play(FadeOut(VGroup(swap_head, swap, swap_note, swap_note2, identity)))
        wild = Text(
            "This identity is the backward pass CTC implementations hard-code.",
            font_size=BODY_SIZE,
        ).move_to(0.85 * UP)
        trap = caption("feed it anything but a true log-softmax and the loss stays right")
        trap2 = caption("while the gradient goes silently wrong (PyTorch issue #122243)")
        trap.move_to(0.05 * UP)
        trap2.next_to(trap, DOWN, buff=0.15)
        takeaway = Text(
            "softmax output minus how often the truth used each cell",
            font_size=24,
        ).move_to(1.35 * DOWN)
        self.play(FadeIn(wild))
        self.play(FadeIn(trap), FadeIn(trap2))
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


# --- Training-dynamics data (plan 010 anchors L, M, S) ---------------------
# Push ≜ γ − y = −∂L/∂u: the sign Graves' figure 4 plots — above the axis,
# raise this output. Uniform-outputs push is exact fractions (anchor L);
# the iteration snapshots are the float64 free-logit run from the repo
# matrix (anchor S) — display only, no exactness beats off iteration 0.
UNIFORM_PUSH = [
    [1 / 3, -1 / 3, 0],
    [1 / 5, -2 / 15, -1 / 15],
    [-2 / 15, 1 / 5, -1 / 15],
    [-1 / 3, 1 / 3, 0],
]
SNAPSHOTS = [
    # (label, loss, y by frame, push by frame)
    (
        "iter 0",
        "0.7181",
        [[0.7, 0.2, 0.1], [0.6, 0.1, 0.3], [0.2, 0.1, 0.7], [0.1, 0.7, 0.2]],
        [
            [0.2028, -0.2000, -0.0028],
            [0.1086, -0.0670, -0.0416],
            [-0.0536, 0.0403, 0.0133],
            [-0.1000, 0.2487, -0.1487],
        ],
    ),
    (
        "iter 10",
        "0.1602",
        [
            [0.9120, 0.0404, 0.0476],
            [0.8192, 0.0379, 0.1429],
            [0.1378, 0.1170, 0.7452],
            [0.0241, 0.9371, 0.0388],
        ],
        [
            [0.0439, -0.0404, -0.0035],
            [0.0497, -0.0321, -0.0176],
            [-0.0176, 0.0105, 0.0072],
            [-0.0241, 0.0566, -0.0326],
        ],
    ),
    (
        "iter 50",
        "0.0356",
        [
            [0.9689, 0.0094, 0.0217],
            [0.9457, 0.0092, 0.0452],
            [0.0927, 0.1309, 0.7764],
            [0.0059, 0.9858, 0.0083],
        ],
        [
            [0.0100, -0.0094, -0.0006],
            [0.0124, -0.0079, -0.0045],
            [-0.0039, 0.0025, 0.0014],
            [-0.0059, 0.0130, -0.0071],
        ],
    ),
]


def _bar_panel(values_by_t, origin, scale, signed=False) -> VGroup:
    """A 4-frame x 3-class bar panel growing from a baseline at `origin`.

    Unsigned panels (outputs) draw COOL bars upward; signed panels (the
    push) draw GOOD above the axis and WARM below, with the axis itself
    drawn in. All panels in a scene share `scale`, so shrinking bars mean
    shrinking numbers — the vanishing IS the story, never a rescale.
    """
    panel = VGroup()
    if signed:
        panel.add(
            Line(
                np.array([origin[0] - 0.25, origin[1], 0]),
                np.array([origin[0] + 3.6, origin[1], 0]),
                color=MUTED,
                stroke_width=1.5,
            )
        )
    for t, values in enumerate(values_by_t):
        for c, value in enumerate(values):
            if value == 0 and signed:
                continue  # a zero push is the absence of a bar
            height = max(abs(value) * scale, 0.015)
            color = (GOOD if value >= 0 else WARM) if signed else COOL
            y_mid = origin[1] + (height / 2 if value >= 0 else -height / 2)
            panel.add(
                Rectangle(
                    width=0.18,
                    height=height,
                    stroke_width=1.5,
                    color=color,
                    fill_color=color,
                    fill_opacity=0.4,
                ).move_to([origin[0] + t * 1.0 + (c - 1) * 0.24, y_mid, 0])
            )
    return panel


def _frame_ticks(origin) -> VGroup:
    return VGroup(
        *[
            Text(f"t={t + 1}", font_size=14, color=MUTED).move_to(
                np.array([origin[0] + t * 1.0, origin[1], 0])
            )
            for t in range(4)
        ]
    )


class TheErrorSignalLearns(ConceptScene):
    """Watch y − γ over training: diffuse, localised, gone — Graves' figure 4, made countable."""

    def construct(self):
        self.play(FadeIn(self.title("The Error Signal Learns"), shift=0.3 * DOWN))

        opening = Text(
            "Train on the loss and watch its gradient breathe.",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        credit = caption(
            "the arc of Graves et al. 2006, figure 4 — rebuilt on four countable frames"
        )
        credit.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(opening), FadeIn(credit))

        # Sign pinned the moment the first axis appears: these panels plot
        # the push γ − y, the negative of the loss's slope.
        sign_pin = caption(
            "panels plot the push, γ − y: a bar above the axis says raise this output"
        )
        self.play(FadeOut(credit))
        sign_pin.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(sign_pin))

        # --- before training: outputs that know nothing -------------------------
        uniform_out = _bar_panel([[1 / 3] * 3] * 4, (-4.6, -0.4), 1.6)
        uniform_push = _bar_panel(UNIFORM_PUSH, (1.0, -0.4), 1.6, signed=True)
        out_tag = Text("outputs (all 1/3)", font_size=SMALL_SIZE, color=COOL)
        out_tag.move_to([-3.1, 1.15, 0])
        push_tag = Text("push", font_size=SMALL_SIZE, color=GOOD).move_to([2.5, 1.15, 0])
        fractions = MathTex(
            r"t{=}1:\ \left(+\tfrac{1}{3},\ -\tfrac{1}{3},\ 0\right)",
            font_size=28,
            color=ACCENT,
        ).move_to([2.5, -1.75, 0])
        ticks = VGroup(_frame_ticks((-4.6, -1.35)), _frame_ticks((1.0, -1.35)))
        self.play(FadeIn(uniform_out), FadeIn(uniform_push), FadeIn(out_tag), FadeIn(push_tag))
        self.play(FadeIn(ticks), Write(fractions))
        quote_a = caption('"the error is determined by the target sequence only" — pure fractions:')
        quote_a2 = caption("with outputs carrying no information, the push is γ itself, minus 1/3")
        self.play(FadeOut(sign_pin))
        quote_a.to_edge(DOWN, buff=0.6)
        quote_a2.next_to(quote_a, DOWN, buff=0.15)
        on_frame(quote_a2)
        self.play(FadeIn(quote_a), FadeIn(quote_a2))
        self.wait(1.3)

        # --- the run itself: three snapshots, one shared scale ------------------
        self.play(
            FadeOut(
                VGroup(
                    uniform_out,
                    uniform_push,
                    out_tag,
                    push_tag,
                    fractions,
                    ticks,
                    quote_a,
                    quote_a2,
                    opening,
                )
            )
        )
        run_head = Text(
            "now train the scored matrix — same panels, three moments",
            font_size=SMALL_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(run_head))
        baselines = [1.7, 0.35, -1.05]
        # Row notes stay short — the right margin past the push panel holds
        # about fifteen characters; the Graves quotes get the bottom line.
        stage_notes = ["diffuse", "localising", "nearly gone"]
        rows = VGroup()
        for (label, loss, y_snap, push_snap), y0, stage_note in zip(
            SNAPSHOTS, baselines, stage_notes, strict=True
        ):
            out_panel = _bar_panel(y_snap, (-4.9, y0), 0.75)
            push_panel = _bar_panel(push_snap, (0.7, y0), 2.0, signed=True)
            stage = Text(f"{label}\nloss {loss}", font_size=15, color=MUTED, line_spacing=0.8)
            stage.move_to([-6.15, y0 + 0.3, 0])
            on_frame(stage)
            note = Text(stage_note, font_size=14, color=MUTED).move_to([5.5, y0 + 0.3, 0])
            on_frame(note)
            row = VGroup(out_panel, push_panel, stage, note)
            rows.add(row)
            self.play(FadeIn(row), run_time=0.9)
            self.wait(0.5)
        quote_bc = caption('"the error localises around them" — then it "virtually disappears"')
        quote_bc.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(quote_bc))
        self.wait(1.0)

        # --- the long tail, and why it flattens ---------------------------------
        self.play(FadeOut(rows), FadeOut(run_head), FadeOut(quote_bc))
        tail = MathTex(
            r"\text{loss: } 0.7181 \to 0.1602 \to 0.0356 \to 0.0088 \to 0.0003",
            font_size=34,
        ).move_to(1.5 * UP)
        tail_note = caption("iterations 0, 10, 50, 200, 5000 — plain gradient descent")
        tail_note.next_to(tail, DOWN, buff=0.2)
        gem = Text(
            "frame 3 never goes one-hot: it settles at (0.032, 0.218, 0.750)",
            font_size=BODY_SIZE,
        ).move_to(0.1 * UP)
        gem_why = caption("with frames 1, 2, 4 saying A, A, B, all three frame-3 choices")
        gem_why2 = caption("collapse to AB — AAAB, AAεB, AABB — so the loss goes indifferent")
        gem_why.move_to(0.65 * DOWN)
        gem_why2.next_to(gem_why, DOWN, buff=0.15)
        self.play(Write(tail), FadeIn(tail_note))
        self.play(FadeIn(gem))
        self.play(FadeIn(gem_why), FadeIn(gem_why2))
        self.wait(1.2)
        takeaway = Text(
            "the error dies when y matches γ — indifference, not certainty",
            font_size=24,
        ).move_to(2.35 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


class WhyTheSpikesAppear(ConceptScene):
    """Peaky outputs are topology plus weight sharing — and the identity's family is everywhere."""

    def construct(self):
        self.play(FadeIn(self.title("Why the Spikes Appear"), shift=0.3 * DOWN))

        opening = Text(
            '"Never read spike timing as segmentation." Here is why the spikes happen.',
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(opening))

        # --- blank's head start is counted, not heard ---------------------------
        # Label-occurrence totals over all AB-collapsing paths, uniform
        # weight (anchor N): the input never enters this computation.
        count_rows = [
            (r"T=4:\quad 15 \text{ paths}\quad A\ 21 \quad B\ 21 \quad \varepsilon\ 18", MUTED),
            (r"T=5:\quad 35 \text{ paths}\quad A\ 56 \quad B\ 56 \quad \varepsilon\ 63", ACCENT),
            (
                r"T=10:\quad 495 \text{ paths}\quad A\ 1287 \quad B\ 1287 \quad \varepsilon\ 2376",
                ACCENT,
            ),
        ]
        counts = VGroup(
            *[
                MathTex(row, font_size=32, color=color).move_to((1.3 - 0.75 * i) * UP)
                for i, (row, color) in enumerate(count_rows)
            ]
        )
        counts_note = caption("our 4-frame example is the fair case — one frame more and blank")
        counts_note2 = caption("pulls ahead for good; the input never entered this count")
        counts_note.move_to(1.0 * DOWN)
        counts_note2.next_to(counts_note, DOWN, buff=0.15)
        for row in counts:
            self.play(Write(row), run_time=0.8)
        self.play(FadeIn(counts_note), FadeIn(counts_note2))
        self.wait(1.2)

        # --- the single-letter companion: the share has a limit -----------------
        self.play(FadeOut(VGroup(counts, counts_note, counts_note2, opening)))
        single_head = Text(
            "one letter, growing T — blank's share of the uniform posterior",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        single = MathTex(
            r"\text{target A:}\quad \tfrac{1}{2}\ (T{=}4)"
            r"\;\longrightarrow\; 0.6600\ (T{=}100)"
            r"\;\longrightarrow\; \tfrac{2}{3}",
            font_size=40,
            color=ACCENT,
        ).move_to(0.85 * UP)
        single_note = caption("per-frame A counts at T=4: 4, 6, 6, 4 — a 20 : 20 tie with blank,")
        single_note2 = caption("the boundary case; expected label frames = (T+2)/3, so blank → 2/3")
        single_note.move_to(0.0 * UP)
        single_note2.next_to(single_note, DOWN, buff=0.15)
        condition = caption("(uniform outputs, growing T — a trained model's dwell differs)")
        condition.next_to(single_note2, DOWN, buff=0.25)
        self.play(FadeIn(single_head))
        self.play(Write(single))
        self.play(FadeIn(single_note), FadeIn(single_note2))
        self.play(FadeIn(condition))
        self.wait(1.2)

        # --- weight sharing springs the trap ------------------------------------
        self.play(FadeOut(VGroup(single_head, single, single_note, single_note2, condition)))
        shared_head = Text(
            "force one softmax to serve every frame, and descend",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(shared_head))
        outcomes = [
            ("T = 4", [0.4, 0.4, 0.2], "A and B tie at 0.4 —\nno blank takeover", GOOD, -3.1),
            (
                "T = 12",
                [0.0919, 0.0919, 0.8162],
                'argmax ε, every frame:\ndecodes to "" — 100% error',
                WARM,
                1.9,
            ),
        ]
        panels = VGroup()
        for label, dist, verdict, verdict_color, x0 in outcomes:
            bars = VGroup()
            for i, (cls, color, value) in enumerate(zip(CLASSES, CLASS_COLORS, dist, strict=True)):
                x = x0 + i * 1.0
                height = max(value * 2.2, 0.02)
                bars.add(
                    Rectangle(
                        width=0.55,
                        height=height,
                        stroke_width=2,
                        color=color,
                        fill_color=color,
                        fill_opacity=0.35,
                    ).move_to([x, -0.35 + height / 2, 0])
                )
                bars.add(Text(cls, font_size=SMALL_SIZE, color=MUTED).move_to([x, -0.7, 0]))
                bars.add(
                    Text(f"{value:.4f}", font_size=14, color=color).move_to(
                        [x, -0.35 + height + 0.2, 0]
                    )
                )
            tag = Text(label, font_size=SMALL_SIZE, color=COOL).move_to([x0 + 1.0, 1.75, 0])
            verdict_m = Text(verdict, font_size=SMALL_SIZE, color=verdict_color, line_spacing=0.9)
            verdict_m.move_to([x0 + 1.0, -1.45, 0])
            panels.add(VGroup(bars, tag, verdict_m))
        self.play(FadeIn(panels[0]))
        self.play(FadeIn(panels[1]))
        zeyer = caption("Zeyer, Schlüter & Ney (arXiv, 2021): proved for a feed-forward net")
        zeyer2 = caption("from uniform init — a local optimum; the global optimum has zero error")
        zeyer.move_to(2.35 * DOWN)
        zeyer2.next_to(zeyer, DOWN, buff=0.15)
        on_frame(zeyer2)
        self.play(FadeIn(zeyer), FadeIn(zeyer2))
        self.wait(1.3)
        fix = caption("a label prior in the loss prevents it — and our free-logit run never")
        fix2 = caption("spiked at all: peakiness needs weight sharing and long T")
        self.play(FadeOut(zeyer), FadeOut(zeyer2))
        fix.move_to(2.35 * DOWN)
        fix2.next_to(fix, DOWN, buff=0.15)
        on_frame(fix2)
        self.play(FadeIn(fix), FadeIn(fix2))
        self.wait(1.2)

        # --- the family portrait -------------------------------------------------
        self.play(FadeOut(VGroup(shared_head, panels, fix, fix2)))
        family_head = Text(
            "one gradient family: softmax output minus a target",
            font_size=BODY_SIZE,
        ).next_to(self.head, DOWN, buff=0.3)
        self.play(FadeIn(family_head))
        pairs = [
            ("one-hot cross-entropy", "the degenerate case — γ snapped to a path"),
            ("distillation", "same shape — the teacher's soft outputs"),
            ("CTC", "target = occupancy, from forward–backward"),
            ("output spikes", "a training artifact — steerable, not timestamps"),
        ]
        table = VGroup()
        for i, (left, right) in enumerate(pairs):
            y = 1.35 - 0.75 * i
            left_m = Text(left, font_size=SMALL_SIZE, color=COOL).move_to([-3.6, y, 0])
            arrow = Arrow(
                start=np.array([-1.7, y, 0]),
                end=np.array([-0.9, y, 0]),
                color=MUTED,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            right_m = Text(right, font_size=SMALL_SIZE, color=GOOD).move_to([2.5, y, 0])
            on_frame(right_m)
            table.add(VGroup(left_m, arrow, right_m))
        for row in table:
            self.play(FadeIn(row), run_time=0.6)
        self.wait(0.8)
        takeaway = Text(
            "softmax minus target — CTC's target is where the truth spends its time",
            font_size=24,
        ).move_to(2.35 * DOWN)
        self.play(FadeIn(takeaway, shift=0.2 * UP), Create(boxed(takeaway, buff=0.28)))
        self.wait(2)


if __name__ == "__main__":
    raise SystemExit(render_cli())
