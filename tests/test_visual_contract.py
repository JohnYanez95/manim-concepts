"""The visual contract, enforced where a machine can enforce it.

Colour was the single largest category of review findings on this repo — five
across three rounds, every one in a concept module, every one a colour that
should have come from `utils.theme`. Two of them (`GREY_B` on the permutation
slots, `WHITE` on the tree root) are pure pattern matches. Paying for a review
round to catch a pattern match is a waste of the reviewer, so they are caught
here instead.

What is *not* here is semantics. Whether `WARM` was the right choice for a
particular mobject is a judgement about the argument the scene is making, and
that stays with review. The rule this file enforces is narrower and absolute:
a concept module names its colours through the theme, never directly.
"""

import ast
import re
from itertools import combinations
from pathlib import Path

import manim
import pytest
from manim.utils.color import ManimColor

from utils import theme
from utils.colour import DEUTERANOPIA, PROTANOPIA, delta_e, simulate

REPO = Path(__file__).resolve().parents[1]

# Discovered from manim at runtime rather than hardcoded, so a manim upgrade
# that adds colours cannot quietly open a gap in this check.
MANIM_COLOURS = {name for name in dir(manim) if isinstance(getattr(manim, name, None), ManimColor)}

HEX_LITERAL = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")

MODULES = sorted(REPO.glob("*/*_manim.py"))


def test_manim_colour_constants_were_discovered():
    """Guards the checks below from silently passing on an empty set."""
    assert len(MANIM_COLOURS) > 50, "manim colour introspection returned almost nothing"
    assert {"WHITE", "BLACK", "GREY_B"} <= MANIM_COLOURS


def test_there_is_at_least_one_concept_module():
    assert MODULES, "no concept modules found — the glob or the layout changed"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_no_raw_manim_colour_constants(module):
    """Concept modules take colour from `utils.theme`, never from manim.

    `from manim import *` makes all 89 of manim's colours available by name, so
    reaching for `WHITE` or `GREY_B` is a one-word slip that renders fine and
    silently leaves the repo's palette. Both of those exact slips reached
    review before this test existed.
    """
    tree = ast.parse(module.read_text(encoding="utf-8"))
    used = sorted(
        {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and node.id in MANIM_COLOURS
        }
    )
    assert not used, (
        f"{module.name} uses manim colour constants {used}; "
        "use a name from utils.theme (ACCENT/COOL/WARM/GOOD/MUTED) or palette(i)"
    )


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_no_hex_colour_literals(module):
    """Hex belongs in `utils/theme.py` and nowhere else.

    A literal here is worse than a manim constant: it is invisible to grep for
    a colour name and it cannot be changed repo-wide.
    """
    tree = ast.parse(module.read_text(encoding="utf-8"))
    literals = sorted(
        {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and HEX_LITERAL.match(node.value)
        }
    )
    assert not literals, f"{module.name} hardcodes colours {literals}; move them to utils/theme.py"


# ---------------------------------------------------------------------------
# The palette itself
#
# These pin properties that are invisible in code review: whether two hexes
# stay distinguishable to a colour-blind viewer is not something anyone can
# eyeball from a diff. WARM against GOOD once collapsed to dE 9.8 under
# simulated deuteranopia while looking fine to me, and that pair carries the
# whole argument in CombinationRule.
# ---------------------------------------------------------------------------

SEMANTIC = {
    "ACCENT": theme.ACCENT,
    "COOL": theme.COOL,
    "WARM": theme.WARM,
    "GOOD": theme.GOOD,
    "MUTED": theme.MUTED,
}
WHITE = "#ffffff"


@pytest.mark.parametrize("name,colour", SEMANTIC.items())
def test_semantic_colour_is_legible_on_the_background(name, colour):
    assert delta_e(colour, theme.BG) > 45, f"{name} is too close to the background"


@pytest.mark.parametrize("name,colour", SEMANTIC.items())
def test_semantic_colour_is_not_mistakable_for_body_text(name, colour):
    assert delta_e(colour, WHITE) > 20, f"{name} reads as plain white text"


@pytest.mark.parametrize("a,b", list(combinations(SEMANTIC, 2)))
def test_semantic_colours_are_distinct(a, b):
    assert delta_e(SEMANTIC[a], SEMANTIC[b]) > 28, f"{a} and {b} are too similar"


@pytest.mark.parametrize(
    "vision,matrix", [("deuteranopia", DEUTERANOPIA), ("protanopia", PROTANOPIA)]
)
@pytest.mark.parametrize("a,b", list(combinations(SEMANTIC, 2)))
def test_semantic_colours_survive_colour_blindness(a, b, vision, matrix):
    """Semantic colours carry meaning by hue, so they must survive losing hue.

    The regression this exists for: WARM/GOOD at dE 9.8 under deuteranopia,
    which made CombinationRule's central visual argument invisible to roughly
    one man in sixteen.
    """
    separation = delta_e(simulate(SEMANTIC[a], matrix), simulate(SEMANTIC[b], matrix))
    assert separation > 15, f"{a} and {b} collapse under {vision} (dE {separation:.1f})"


@pytest.mark.parametrize("index", range(len(theme.PALETTE)))
def test_categorical_colours_do_not_alias_the_semantic_ones(index):
    """The two sets must stay disjoint, or the distinction is source-only.

    They were not always: four of five semantic names were literally PALETTE
    entries, so a scene using the wrong one rendered identically to a scene
    using the right one.
    """
    nearest = min((delta_e(theme.PALETTE[index], c), n) for n, c in SEMANTIC.items())
    assert nearest[0] > 20, f"PALETTE[{index}] is indistinguishable from {nearest[1]}"


@pytest.mark.parametrize("i,j", list(combinations(range(5), 2)))
def test_categorical_colours_are_distinct(i, j):
    assert delta_e(theme.PALETTE[i], theme.PALETTE[j]) > 28


def test_palette_helper_wraps():
    assert theme.palette(0) == theme.PALETTE[0]
    assert theme.palette(len(theme.PALETTE)) == theme.PALETTE[0]
