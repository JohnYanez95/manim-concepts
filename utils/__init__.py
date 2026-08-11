"""Shared layer every concept module builds on.

A concept module should need exactly one import from this package::

    from utils import ACCENT, COOL, ConceptScene, chip, render_cli, token

Keeping the public surface here means topic modules never reach into
``utils.mobjects`` or ``utils.theme`` directly, so those files can be
reorganised without touching a single scene.
"""

from utils.mobjects import boxed, caption, chip, header, token
from utils.render import QUALITIES, media_root, numbered_stem, render_cli, scene_order
from utils.scene import ConceptScene
from utils.theme import (
    ACCENT,
    BG,
    BODY_SIZE,
    COOL,
    FORMULA_SIZE,
    GOOD,
    LABEL_SIZE,
    MUTED,
    PALETTE,
    RESULT_SIZE,
    SMALL_SIZE,
    TITLE_SIZE,
    WARM,
    palette,
)

__all__ = [
    "ACCENT",
    "BG",
    "BODY_SIZE",
    "COOL",
    "FORMULA_SIZE",
    "GOOD",
    "LABEL_SIZE",
    "MUTED",
    "PALETTE",
    "QUALITIES",
    "RESULT_SIZE",
    "SMALL_SIZE",
    "TITLE_SIZE",
    "WARM",
    "ConceptScene",
    "boxed",
    "caption",
    "chip",
    "header",
    "media_root",
    "numbered_stem",
    "palette",
    "render_cli",
    "scene_order",
    "token",
]
