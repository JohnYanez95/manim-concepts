"""Layout linter: dry-run every scene and flag text collisions at each hold.

Two shipped defects motivated this tool, both invisible to the existing
gates: a caption pair overlapping a formula (`SortTheSquare`) and a bar
grazing a caption (`TheBalancePoint`). Frame sampling missed them because
eyes skim, and the test suite deliberately has no pixel tests. This tool
checks the *geometry* instead — the measured bounding boxes manim itself
lays out — so it is exact where an eyeball is approximate, and immune to
the font-update fragility that keeps pixel tests banned from tests/.

At every ``wait()`` — a scene's steady beats — three checks run over the
mobjects on screen:

1. **text–text overlap**: two text units whose boxes interpenetrate.
2. **frame clipping**: a text unit extending past the visible frame.
3. **shape-through-text**: a stroked/filled shape's outline passing
   through a text unit's (slightly inflated) box — bars, rules and
   curves crossing captions. Containment is fine (a ``boxed`` takeaway
   *should* surround its text); crossing is not.

Findings are reports, not proof of ugliness — a flagged pair can be
deliberate. The gate is "every finding explained or fixed", not zero
findings at any cost.

Run:
    uv run python tools/check_layout.py                       # every module
    uv run python tools/check_layout.py probability/foo_manim.py [...]
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from manim import (
    MarkupText,
    Paragraph,
    Scene,
    SingleStringMathTex,
    Text,
    VMobject,
    tempconfig,
)

REPO = Path(__file__).resolve().parents[1]

TEXT_TYPES = (SingleStringMathTex, Text, MarkupText, Paragraph)

# Interpenetration below this depth (scene units) is ignored: kissing
# boxes at the threshold read fine on screen, and Text boxes carry a few
# hundredths of padding around the ink anyway.
OVERLAP_TOLERANCE = 0.03
# Text boxes are inflated by this much for the shape check, so a shape
# *grazing* a caption — the TheBalancePoint failure — still trips it.
SHAPE_MARGIN = 0.06
# The visible frame is ±frame_width/2, ±frame_height/2; flag anything
# closer to the edge than this, since 480p review already misses it.
EDGE_MARGIN = 0.05


def _text_units(scene: Scene):
    """Top text mobjects on screen: descend groups, never into text."""
    units = []

    def walk(mobject):
        if isinstance(mobject, TEXT_TYPES):
            if mobject.width > 1e-3 and mobject.height > 1e-3:
                units.append(mobject)
            return
        for sub in mobject.submobjects:
            walk(sub)

    for top in scene.mobjects:
        walk(top)
    return units


def _shape_leaves(scene: Scene):
    """Visible non-text leaf VMobjects — the things that can cross text."""
    leaves = []

    def walk(mobject):
        if isinstance(mobject, TEXT_TYPES):
            return
        if mobject.submobjects:
            for sub in mobject.submobjects:
                walk(sub)
            return
        if not isinstance(mobject, VMobject) or mobject.get_num_points() == 0:
            return
        if max(mobject.get_stroke_opacity(), mobject.get_fill_opacity()) > 0.1:
            leaves.append(mobject)

    for top in scene.mobjects:
        walk(top)
    return leaves


def _bbox(mobject, margin=0.0):
    left, bottom, _ = mobject.get_corner([-1, -1, 0])
    right, top, _ = mobject.get_corner([1, 1, 0])
    return left - margin, right + margin, bottom - margin, top + margin


def _outline_points(shape) -> np.ndarray:
    """Sample a shape's outline densely enough that no text box slips through.

    A fixed sample count lets a long path cross a small label between
    two samples; scaling the count with arc length caps the spacing at
    ~0.1 scene units, smaller than any readable text box.
    """
    length = shape.get_arc_length()
    count = int(np.clip(length / 0.1, 16, 1024))
    return np.array([shape.point_from_proportion(t) for t in np.linspace(0, 1, count)])


def _label(mobject) -> str:
    raw = getattr(mobject, "text", None) or getattr(mobject, "tex_string", None) or ""
    raw = " ".join(str(raw).split())
    return raw[:48] + ("…" if len(raw) > 48 else "")


def _check_beat(scene: Scene, beat: int, frame_w: float, frame_h: float) -> list[str]:
    findings = []
    units = _text_units(scene)

    # 1. text–text interpenetration.
    for i, a in enumerate(units):
        al, ar, ab, at = _bbox(a)
        for b in units[i + 1 :]:
            bl, br, bb, bt = _bbox(b)
            dx = min(ar, br) - max(al, bl)
            dy = min(at, bt) - max(ab, bb)
            if dx > OVERLAP_TOLERANCE and dy > OVERLAP_TOLERANCE:
                findings.append(
                    f'beat {beat}: text overlap ({dx:.2f}x{dy:.2f}): "{_label(a)}" vs "{_label(b)}"'
                )

    # 2. frame clipping.
    half_w, half_h = frame_w / 2 - EDGE_MARGIN, frame_h / 2 - EDGE_MARGIN
    for a in units:
        al, ar, ab, at = _bbox(a)
        if al < -half_w or ar > half_w or ab < -half_h or at > half_h:
            findings.append(
                f"beat {beat}: text at frame edge (x [{al:.2f}, {ar:.2f}], "
                f'y [{ab:.2f}, {at:.2f}]): "{_label(a)}"'
            )

    # 3. shape outlines crossing text boxes.
    boxes = [(_bbox(a, SHAPE_MARGIN), a) for a in units]
    for shape in _shape_leaves(scene):
        sl, sr, sb, st = _bbox(shape)
        near = [
            (box, a)
            for box, a in boxes
            if min(sr, box[1]) - max(sl, box[0]) > 0 and min(st, box[3]) - max(sb, box[2]) > 0
        ]
        if not near:
            continue
        samples = _outline_points(shape)
        for (bl, br, bb, bt), a in near:
            inside = (
                (samples[:, 0] > bl)
                & (samples[:, 0] < br)
                & (samples[:, 1] > bb)
                & (samples[:, 1] < bt)
            )
            if inside.any():
                findings.append(
                    f'beat {beat}: shape crosses text: {type(shape).__name__} through "{_label(a)}"'
                )
    return findings


def _scenes_in(path: Path) -> tuple[object, list[type[Scene]]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scenes = [
        obj
        for obj in vars(module).values()
        if isinstance(obj, type)
        and issubclass(obj, Scene)
        and obj.__module__ == path.stem
        and not obj.__name__.startswith("_")
    ]
    return module, scenes


def check_module(path: Path) -> dict[str, list[str]]:
    """Dry-run every scene in `path`; return findings keyed by scene name."""
    _, scenes = _scenes_in(path)
    report: dict[str, list[str]] = {}
    for scene_cls in scenes:
        findings: list[str] = []
        with tempconfig(
            {
                "dry_run": True,
                "quality": "low_quality",
                "frame_rate": 1,
                "input_file": str(path),
            }
        ):
            scene = scene_cls()
            beats = {"count": 0}
            original_wait = scene.wait

            def wait(*args, _scene=scene, _f=findings, _b=beats, _w=original_wait, **kwargs):
                _b["count"] += 1
                _f.extend(
                    _check_beat(
                        _scene,
                        _b["count"],
                        _scene.camera.frame_width,
                        _scene.camera.frame_height,
                    )
                )
                return _w(*args, **kwargs)

            scene.wait = wait
            scene.render()
        report[scene_cls.__name__] = findings
    return report


def main(argv: list[str]) -> int:
    paths = [Path(arg).resolve() for arg in argv] or sorted(REPO.glob("*/*_manim.py"))
    failed = False
    for path in paths:
        print(f"== {path.relative_to(REPO)}")
        for scene_name, findings in check_module(path).items():
            status = "clean" if not findings else f"{len(findings)} finding(s)"
            print(f"   {scene_name}: {status}")
            for finding in findings:
                failed = True
                print(f"      {finding}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
