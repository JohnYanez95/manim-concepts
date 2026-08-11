"""Colour maths — CIELAB distance and dichromacy simulation.

This module exists because of a specific bug. The palette was chosen by a
solver and checked by a test, each with its own copy of these formulas, and the
copies disagreed: the solver compared simulated colours *before* clipping them
back into the displayable gamut, which inflates the distance. It reported a
comfortable dE 44 where the test measured dE 9.7, and the palette it produced
failed the gate it was supposed to satisfy.

So the rule is: whatever picks the colours and whatever verifies them import
from here. One implementation, no drift.

Deliberately **not** re-exported through ``utils/__init__.py`` — scenes never
need it. Only ``tools/solve_palette.py`` and ``tests/test_visual_contract.py``
import it.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "DEUTERANOPIA",
    "PROTANOPIA",
    "delta_e",
    "hex_to_rgb",
    "lab",
    "lab_to_hex",
    "lch",
    "rgb_to_hex",
    "simulate",
]

# Machado, Oliveira & Fernandes (2009), full-severity dichromacy matrices,
# applied in *linear* RGB.
DEUTERANOPIA = np.array(
    [
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ]
)
PROTANOPIA = np.array(
    [
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ]
)

_XYZ = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_XYZ_INV = np.linalg.inv(_XYZ)
_D65 = np.array([0.9505, 1.0, 1.089])


def hex_to_rgb(colour: str) -> np.ndarray:
    """``"#5ec8e5"`` to sRGB floats in [0, 1]."""
    return np.array([int(colour[i : i + 2], 16) / 255 for i in (1, 3, 5)])


def rgb_to_hex(rgb: np.ndarray) -> str:
    """sRGB floats to ``"#rrggbb"``, clipped to the displayable range.

    Clipping here rather than at the call site is the whole point of this
    module: an unclipped "colour" is not something a screen can show, and
    measuring distances between unshowable values is what caused the bug in
    the docstring above.
    """
    red, green, blue = (int(round(v * 255)) for v in np.clip(rgb, 0, 1))
    return f"#{red:02x}{green:02x}{blue:02x}"


def _to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _from_linear(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def lab(colour: str) -> np.ndarray:
    """CIELAB (L*, a*, b*) of a hex colour, D65."""
    xyz = _XYZ @ _to_linear(hex_to_rgb(colour)) / _D65
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def lab_to_hex(values: np.ndarray) -> str:
    """Inverse of `lab`, clipped into gamut."""
    fy = (values[0] + 16) / 116
    f = np.array([fy + values[1] / 500, fy, fy - values[2] / 200])
    xyz = np.where(f**3 > 0.008856, f**3, (f - 16 / 116) / 7.787) * _D65
    return rgb_to_hex(_from_linear(_XYZ_INV @ xyz))


def lch(colour: str) -> tuple[float, float, float]:
    """Lightness, chroma, hue angle in degrees — the axes a designer thinks in."""
    values = lab(colour)
    return (
        float(values[0]),
        float(np.hypot(values[1], values[2])),
        float(np.degrees(np.arctan2(values[2], values[1])) % 360),
    )


def delta_e(a: str, b: str) -> float:
    """CIE76 colour difference.

    Rough scale: under 2 is invisible, under 10 subtle, over 25 unmistakable.
    CIE76 rather than CIEDE2000 on purpose — it is a plain Euclidean distance
    in Lab, so a threshold in this repo means one thing and can be reasoned
    about without a reference table.
    """
    return float(np.linalg.norm(lab(a) - lab(b)))


def simulate(colour: str, matrix: np.ndarray) -> str:
    """How `colour` appears to a dichromat, as a displayable hex.

    Returning hex rather than raw floats forces the clip-and-quantise step
    that the original buggy solver skipped.
    """
    return rgb_to_hex(_from_linear(matrix @ _to_linear(hex_to_rgb(colour))))
