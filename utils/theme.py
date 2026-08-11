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
"""

# --- Canvas -----------------------------------------------------------------
BG = "#0f1117"

# --- Semantic colours -------------------------------------------------------
ACCENT = "#f6c667"
COOL = "#5ec8e5"
WARM = "#ff7f6b"
GOOD = "#7ee081"
MUTED = "#9aa0ac"

# --- Categorical cycle ------------------------------------------------------
PALETTE = ["#5ec8e5", "#ff7f6b", "#7ee081", "#f6c667", "#c792ea"]


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
