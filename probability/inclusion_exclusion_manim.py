"""Inclusion–exclusion — the union rule, from two sets to n.

Seven scenes on the repo's own cells: the overlap counted twice on a die
strip and removed on the unit square, the per-cell ledger on the two-dice
grid that forces the three-set signs, the picture that breaks at four
sets and the two examples that share a coefficient row, the n-set formula
proved by pairing subsets, the matching problem climbing to 1 − 1/e, the
truncated sum as a bound, and the decision rule for reaching for any of it.

    TwoSetsOneOverlap       |A ∪ B| = |A| + |B| − |A ∩ B|, then as area
    ThreeSetsOneLedger      every cell stamped +1, −1, +1 — counted once
    FourSetsNoPicture       four circles make 14 regions; 4, 6, 4, 1 remain
    EveryPointCountedOnce   the n-set formula; the toggle pairing proves it
    TheMatchingLimit        1 − 1/2! + 1/3! − ⋯ → 1 − 1/e
    BracketsAndBounds       stop early and hold a bound — Boole, Bonferroni
    WhenToUseIt             add, complement, sieve, or bound

Every number on screen is exact and machine-verified in plan 016.

Render:
    uv run python probability/inclusion_exclusion_manim.py
    uv run python probability/inclusion_exclusion_manim.py --scene TwoSetsOneOverlap --quality draft
"""

from manim import *

from utils import (
    ACCENT,
    LABEL_SIZE,
    MUTED,
    ConceptScene,
    caption,
    palette,
    render_cli,
)

# Sets are distinct things with no ranking between them — the categorical
# cycle, in the same assignment the independence and conditional series use,
# so "the teal region is A" stays true across the whole topic.
A_COLOR = palette(0)
B_COLOR = palette(1)
C_COLOR = palette(2)
D_COLOR = palette(3)


def _die_strip(side: float = 1.05) -> VGroup:
    """A fair die as six equal cells in a row (the sibling modules' device —
    local on purpose: topic furniture, not repo-wide vocabulary).

    Cell i is ``strip[i]``; its face number is the second submobject.
    """
    cells = VGroup()
    for face in range(1, 7):
        square = Square(side_length=side, stroke_width=2, color=MUTED)
        label = Text(str(face), font_size=LABEL_SIZE).move_to(square)
        cells.add(VGroup(square, label))
    return cells.arrange(RIGHT, buff=0)


def _tint(cell: VGroup, color: str, opacity: float = 0.35) -> None:
    cell[0].set_fill(color, opacity=opacity)


class TwoSetsOneOverlap(ConceptScene):
    """Two sets: the overlap is counted twice, so subtract it once — as counts, then as area."""

    def construct(self):
        self.play(FadeIn(self.title("Two sets, one overlap"), shift=0.3 * DOWN))
        strip = _die_strip().move_to(0.4 * UP)
        self.play(Create(strip))
        for face in (2, 4, 6):
            _tint(strip[face - 1], A_COLOR)
        note = caption("A = even", color=A_COLOR).next_to(strip, DOWN, buff=0.4)
        self.play(FadeIn(note))
        stub = Text("(phase 1 stub)", font_size=LABEL_SIZE, color=ACCENT).move_to(1.8 * DOWN)
        self.play(FadeIn(stub))
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(render_cli())
