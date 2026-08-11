"""Reusable mobject constructors — the visual nouns concepts are built from.

Everything here returns a plain mobject and animates nothing. Composition and
timing belong to the scene; this module only decides what things look like.

The constructors below were each duplicated inside the original
``counting_rules.py``. Extracting them is what makes a second topic cheap to
write: a calculus scene gets the same tokens and the same title rule for free.
"""

from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Line,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    VGroup,
    VMobject,
    config,
)

from utils.theme import ACCENT, LABEL_SIZE, MUTED, SMALL_SIZE, TITLE_SIZE


def header(label: str) -> VGroup:
    """Title plus a full-width underline, pinned to the top of the frame."""
    text = Text(label, font_size=TITLE_SIZE, weight=BOLD)
    text.to_edge(UP, buff=0.3)
    rule = Line(LEFT, RIGHT).set_width(config.frame_width - 1.6)
    rule.next_to(text, DOWN, buff=0.14).set_stroke(width=2, opacity=0.45)
    return VGroup(text, rule)


def token(label: str, color: str, radius: float = 0.34) -> VGroup:
    """A labelled coloured disc — the generic "one distinct object".

    Used wherever a scene needs countable, individually identifiable things:
    the shirts and pants of the multiplication rule, the five letters being
    permuted, the six objects being partitioned.
    """
    circle = Circle(radius=radius, color=color, fill_color=color, fill_opacity=0.28)
    circle.set_stroke(width=3)
    text = Text(label, font_size=LABEL_SIZE, weight=BOLD).move_to(circle)
    return VGroup(circle, text)


def chip(label: str, color: str, width: float = 1.25, height: float = 0.66) -> VGroup:
    """A rounded label box — one entry in an enumerated result set.

    Where `token` says "an object", a chip says "an outcome": the ten
    three-letter combinations, a row of computed values, a set of cases.
    """
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_width=2,
        color=color,
        fill_color=color,
        fill_opacity=0.14,
    )
    return VGroup(box, Text(label, font_size=LABEL_SIZE).move_to(box))


def boxed(mobject: VMobject, color: str = ACCENT, buff: float = 0.3) -> SurroundingRectangle:
    """A rounded frame around a mobject — "this is the takeaway".

    Reserved for the general formula a scene has been building toward, so the
    box reads as punctuation rather than decoration.
    """
    return SurroundingRectangle(mobject, color=color, buff=buff, corner_radius=0.12)


def caption(label: str, color: str = MUTED) -> Text:
    """Small muted prose — scaffolding the eye is meant to skim."""
    return Text(label, font_size=SMALL_SIZE, color=color)
