"""Unit tests for the render CLI.

What is worth testing in a repo of animations is a narrow question. Comparing
rendered frames pixel-by-pixel is brittle and would fail on a font update
without anything being wrong, so none of that is here. What *is* here is the
logic around the renderer: scene discovery, ordering, filename numbering and
argument handling. That layer is pure, fast to exercise, and has already
produced one real bug — four scenes rendering into one file.
"""

from contextlib import contextmanager

import pytest
from manim import Scene

from utils.render import (
    DEFAULT_QUALITY,
    QUALITIES,
    _discover_scenes,
    _select,
    media_root,
    numbered_stem,
    render_cli,
    scene_order,
)
from utils.scene import ConceptScene


class Alpha(Scene):
    """First."""


class Beta(Scene):
    """Second."""


class Gamma(Scene):
    """Third."""


SCENES = [Alpha, Beta, Gamma]


# --- ordering and naming ----------------------------------------------------


def test_scene_order_follows_source_order():
    assert scene_order(SCENES) == {"Alpha": 1, "Beta": 2, "Gamma": 3}


def test_numbered_stem_zero_pads():
    assert numbered_stem(Alpha, scene_order(SCENES)) == "01_Alpha"


def test_numbered_stem_is_independent_of_selection():
    """Rendering the third scene alone must still produce ``03_``.

    The number is a position in the module, not a counter over whatever was
    asked for. If it were the latter, the same scene would land under a
    different filename depending on the flags used, and the numbering would
    stop meaning "watch these in this order".
    """
    order = scene_order(SCENES)
    only_gamma = _select(SCENES, ["Gamma"])
    assert [numbered_stem(s, order) for s in only_gamma] == ["03_Gamma"]


# --- scene selection --------------------------------------------------------


def test_select_returns_every_scene_by_default():
    assert _select(SCENES, None) == SCENES
    assert _select(SCENES, []) == SCENES


def test_select_preserves_requested_order():
    assert _select(SCENES, ["Gamma", "Alpha"]) == [Gamma, Alpha]


def test_select_drops_duplicates():
    assert _select(SCENES, ["Beta", "Beta"]) == [Beta]


def test_select_rejects_unknown_scene():
    """A typo must fail loudly rather than render nothing and report success."""
    with pytest.raises(SystemExit) as excinfo:
        _select(SCENES, ["Bta"])
    message = str(excinfo.value)
    assert "Bta" in message
    # The error has to be actionable, so it lists what was actually available.
    assert "Alpha" in message and "Beta" in message


def test_select_rejects_a_batch_containing_one_bad_name():
    with pytest.raises(SystemExit):
        _select(SCENES, ["Alpha", "Nope"])


# --- discovery --------------------------------------------------------------


def test_discover_finds_scenes_defined_in_the_module():
    namespace = {"__name__": "fake_module"}
    for cls in SCENES:
        cls.__module__ = "fake_module"
    try:
        namespace.update({cls.__name__: cls for cls in SCENES})
        assert _discover_scenes(namespace) == SCENES
    finally:
        for cls in SCENES:
            cls.__module__ = __name__


def test_discover_ignores_imported_scene_classes():
    """``ConceptScene`` is imported by every concept module and is not content.

    Without the ``__module__`` check it would be discovered as a renderable
    scene and every module would render one extra, empty video.
    """
    namespace = {"__name__": "fake_module", "ConceptScene": ConceptScene, "Scene": Scene}
    assert _discover_scenes(namespace) == []


def test_discover_ignores_non_scene_values():
    namespace = {"__name__": "fake_module", "PALETTE": ["#000"], "helper": lambda: None}
    assert _discover_scenes(namespace) == []


# --- quality presets --------------------------------------------------------


def test_quality_names_map_to_real_manim_presets():
    from manim.constants import QUALITIES as MANIM_QUALITIES

    for preset in QUALITIES.values():
        assert preset in MANIM_QUALITIES


def test_default_quality_is_1080p():
    from manim.constants import QUALITIES as MANIM_QUALITIES

    assert DEFAULT_QUALITY in QUALITIES
    assert MANIM_QUALITIES[QUALITIES[DEFAULT_QUALITY]]["pixel_height"] == 1080


# --- media root -------------------------------------------------------------


def test_media_root_defaults_into_the_repo():
    root = media_root()
    assert root.name == "media"
    assert (root.parent / "pyproject.toml").exists()


def test_media_root_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("MANIM_CONCEPTS_MEDIA_DIR", str(tmp_path))
    assert media_root() == tmp_path.resolve()


# --- the regression that motivated the per-scene config scope ---------------


@pytest.fixture
def recorded_renders(monkeypatch):
    """Run render_cli without rendering, capturing the config each scene gets."""
    seen: list[dict] = []

    @contextmanager
    def fake_tempconfig(overrides):
        seen.append(dict(overrides))
        yield

    monkeypatch.setattr("utils.render.tempconfig", fake_tempconfig)
    monkeypatch.setattr(Scene, "render", lambda self, *a, **k: None)
    return seen


def test_every_scene_gets_a_distinct_output_file(recorded_renders):
    """The bug this guards: four scenes rendering into one file.

    On finishing a render manim writes the output path back into the global
    config, and the next scene prefers that over its own name. A batch sharing
    one config scope therefore collapses onto the first scene's filename. The
    fix is a per-scene scope with an explicit output_file, so the invariant
    worth pinning is simply that the names differ and are numbered.
    """
    exit_code = render_cli(SCENES, description="test", argv=["--quality", "draft"])

    assert exit_code == 0
    stems = [config["output_file"] for config in recorded_renders]
    assert stems == ["01_Alpha", "02_Beta", "03_Gamma"]
    assert len(set(stems)) == len(stems)


def test_quality_flag_reaches_the_config(recorded_renders):
    render_cli(SCENES, description="test", argv=["--quality", "draft", "-s", "Alpha"])
    assert recorded_renders[0]["quality"] == QUALITIES["draft"]


def test_output_is_pinned_to_the_media_root(recorded_renders):
    render_cli(SCENES, description="test", argv=["-s", "Alpha"])
    assert recorded_renders[0]["media_dir"] == str(media_root())
