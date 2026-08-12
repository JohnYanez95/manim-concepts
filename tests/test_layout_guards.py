"""The placement guards must actually guard.

`on_frame` and `clear_of` exist because text placed by estimated width
shipped two collisions and a round of edge clips. These tests pin the
behaviours the scenes rely on: a guard that silently did nothing would
pass every render and reintroduce the whole failure class.
"""

import numpy as np
import pytest
from manim import DOWN, LEFT, RIGHT, Square, config

from utils import clear_of, on_frame


def test_on_frame_pulls_an_offscreen_mobject_back_in():
    square = Square(side_length=1.0).move_to([config.frame_width / 2 + 2, 0, 0])
    on_frame(square, margin=0.2)
    assert square.get_right()[0] <= config.frame_width / 2 - 0.2 + 1e-6


def test_on_frame_leaves_a_well_placed_mobject_alone():
    square = Square(side_length=1.0).move_to([1.0, -1.0, 0])
    before = square.get_center().copy()
    on_frame(square)
    assert np.allclose(square.get_center(), before)


def test_on_frame_refuses_what_cannot_fit():
    wide = Square(side_length=1.0).stretch_to_fit_width(config.frame_width + 1)
    with pytest.raises(ValueError):
        on_frame(wide)


def test_clear_of_separates_overlapping_boxes():
    fixed = Square(side_length=2.0)
    mover = Square(side_length=2.0).move_to([0.5, 0.5, 0])
    clear_of(mover, fixed, direction=RIGHT, buff=0.1)
    assert mover.get_left()[0] >= fixed.get_right()[0] + 0.1 - 1e-6


def test_clear_of_leaves_non_overlapping_boxes_alone():
    fixed = Square(side_length=1.0)
    mover = Square(side_length=1.0).move_to([3, 0, 0])
    before = mover.get_center().copy()
    clear_of(mover, fixed, direction=LEFT)
    assert np.allclose(mover.get_center(), before)


def test_clear_of_moving_through_an_obstacle_exits_the_far_side():
    # A mover sitting ABOVE the obstacle, pushed DOWN, must come out
    # below it — the overlap depth alone would leave it embedded.
    fixed = Square(side_length=2.0)
    mover = Square(side_length=2.0).move_to([0, 1.5, 0])
    clear_of(mover, fixed, direction=DOWN, buff=0.1)
    assert mover.get_top()[1] <= fixed.get_bottom()[1] - 0.1 + 1e-6


def test_clear_of_rejects_diagonal_directions():
    with pytest.raises(ValueError):
        clear_of(Square(), Square(), direction=[1, 1, 0])
