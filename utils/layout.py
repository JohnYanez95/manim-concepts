"""Numerical placement guards — keep text on the frame and out of collisions.

Two shipped defects (a caption under a formula, a bar through a caption)
and a round of edge-clipped captions in the softmax series all trace to
the same root: text was placed by *estimating* its width, and the
estimates ran low. These helpers replace the estimate with the measured
bounding box manim already has at construction time.

They are guards, not a layout engine: place a mobject where the design
wants it, then let the guard make the minimal correction. If a guard has
to move something far, the design is wrong — `tools/check_layout.py`
still runs as the gate, and a scene that *needs* big corrections should
be restructured instead of nudged.
"""

from __future__ import annotations

import numpy as np
from manim import Mobject, config

__all__ = ["clear_of", "on_frame"]


def on_frame(mobject: Mobject, margin: float = 0.2) -> Mobject:
    """Shift `mobject` the minimum distance needed to sit inside the frame.

    Call it *after* positioning: ``on_frame(cap.move_to([5.9, 1, 0]))``.
    A mobject wider or taller than the frame cannot be saved by shifting;
    that raises, because silently scaling text would change the type
    scale the theme pins down.
    """
    half_w = config.frame_width / 2 - margin
    half_h = config.frame_height / 2 - margin
    if mobject.width > 2 * half_w or mobject.height > 2 * half_h:
        raise ValueError(
            f"mobject ({mobject.width:.2f} x {mobject.height:.2f}) cannot fit "
            f"the frame; shorten the text or restructure the layout"
        )
    shift = np.zeros(3)
    left, right = mobject.get_left()[0], mobject.get_right()[0]
    bottom, top = mobject.get_bottom()[1], mobject.get_top()[1]
    if left < -half_w:
        shift[0] = -half_w - left
    elif right > half_w:
        shift[0] = half_w - right
    if bottom < -half_h:
        shift[1] = -half_h - bottom
    elif top > half_h:
        shift[1] = half_h - top
    return mobject.shift(shift)


def clear_of(mobject: Mobject, *others: Mobject, direction=None, buff: float = 0.15) -> Mobject:
    """Nudge `mobject` along `direction` until its box clears every other.

    ``direction`` defaults to DOWN-like ``[0, -1, 0]``; it must be a
    cardinal axis (UP, DOWN, LEFT, RIGHT — exactly one of x/y nonzero),
    because a diagonal escape has no single well-defined exit distance.
    The nudge is computed in one step from the boxes: the displacement
    that puts the mobject's *trailing* edge past the other's far edge,
    plus ``buff`` of daylight — overlap depth alone is not enough when
    the movement direction points *into* the obstacle. Mobjects that do
    not overlap are left untouched.
    """
    axis = np.array([0.0, -1.0, 0.0]) if direction is None else np.asarray(direction, dtype=float)
    if (axis[0] != 0) == (axis[1] != 0):
        raise ValueError("direction must be a cardinal axis: UP, DOWN, LEFT or RIGHT")
    needed = 0.0
    for other in others:
        dx = min(mobject.get_right()[0], other.get_right()[0]) - max(
            mobject.get_left()[0], other.get_left()[0]
        )
        dy = min(mobject.get_top()[1], other.get_top()[1]) - max(
            mobject.get_bottom()[1], other.get_bottom()[1]
        )
        if dx <= 0 or dy <= 0:
            continue
        if axis[0] > 0:
            escape = other.get_right()[0] - mobject.get_left()[0]
        elif axis[0] < 0:
            escape = mobject.get_right()[0] - other.get_left()[0]
        elif axis[1] > 0:
            escape = other.get_top()[1] - mobject.get_bottom()[1]
        else:
            escape = mobject.get_top()[1] - other.get_bottom()[1]
        needed = max(needed, escape + buff)
    if needed:
        mobject.shift(axis / np.linalg.norm(axis) * needed)
    return mobject
