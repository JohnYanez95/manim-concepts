"""Shared visual language for every concept in this repo.

A viewer should be able to move between an animation about counting and one
about gradient descent and not have to re-learn what a colour means. That is
what this module is for: colour and type live here once, and concept modules
import them rather than redeclaring hex codes at the top of every file.

Semantic rule for the named colours
-----------------------------------
    ACCENT  the answer, the result, the thing being built toward
    COOL    the first/primary quantity in a comparison
    WARM    what is being removed, cancelled, or overcounted
    GOOD    a confirmed or collapsed-to-final object
    MUTED   scaffolding — labels, rules, slots the eye should skip

PALETTE is different: it is a categorical cycle for "these are N distinct
objects with no ranking between them", indexed by position. Do not reach into
it for semantic meaning.

Why the two sets do not share hexes
-----------------------------------
They used to. Four of the five semantic names were literally PALETTE entries
(ACCENT was PALETTE[3], COOL/WARM/GOOD were [0]/[1]/[2]), which meant the
distinction this module spends its docstring on was invisible in the rendered
video — two review fixes about semantic misuse came out pixel-identical. The
sets are now disjoint by at least dE 25, so "warm means this is about to be
cancelled" is something a viewer can actually learn across topics.

Colour-blind safety
-------------------
The semantic colours are separated under simulated deuteranopia and protanopia
as well as normal vision, because they carry meaning by hue. WARM against GOOD
used to collapse to dE 9.8 under deuteranopia — indistinguishable — and that
pair *is* the argument in CombinationRule, where an overcount collapses into a
confirmed set. The worst semantic pair is now dE 21.5 simulated. The numbers
are pinned by ``tests/test_visual_contract.py``; changing a hex here without
running that suite is how the property gets lost again.

PALETTE is held to a lower bar on purpose: categorical items in this repo carry
a text label (the A/B/C tokens, the chip captions), so hue is never their only
signal. Which is the general rule — see CLAUDE.md.
"""

# --- Canvas -----------------------------------------------------------------
BG = "#0f1117"

# --- Semantic colours -------------------------------------------------------
# Not hand-picked. Solved by tools/solve_palette.py, which minimises drift from
# the original palette subject to the constraints in the module docstring. Re-run
# `uv run python tools/solve_palette.py --verify` after touching any hex here.
ACCENT = "#ffcc5f"
COOL = "#66d9ff"
WARM = "#ea6c58"
GOOD = "#93ffb2"
MUTED = "#91959c"

# --- Categorical cycle ------------------------------------------------------
# Mutually >= dE 52 and >= dE 20 from every semantic colour above, so the
# categorical cycle can never be mistaken for a semantic statement.
PALETTE = ["#009ba9", "#ff7189", "#7cd26c", "#eab77b", "#d1a0ff"]


def palette(index: int) -> str:
    """Colour `index` of the categorical cycle, wrapping at the end.

    Lets a scene iterate over any number of objects without bounds-checking
    against ``len(PALETTE)``.
    """
    return PALETTE[index % len(PALETTE)]


# --- Type scale -------------------------------------------------------------
# Named steps rather than raw numbers. The original counting-rules file drifted
# between font_size 26, 27 and 28 for prose that plays the same role; a scale
# makes that drift impossible to reintroduce by accident.
TITLE_SIZE = 40
FORMULA_SIZE = 58
RESULT_SIZE = 52
BODY_SIZE = 27
LABEL_SIZE = 24
SMALL_SIZE = 20
