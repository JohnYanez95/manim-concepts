"""The `utils` package surface.

Two rules that were documented and unenforced until review pointed at them.

The re-export rule was also documented *wrongly* — as "a name missing from
`__all__` is invisible to concept modules", which is false; `__all__` gates
wildcard imports, not direct ones. The real requirement has two halves, and a
test is a better place to keep them straight than a sentence that drifted
across two files.
"""

import ast
import re
import textwrap
from pathlib import Path

import pytest
from manim import DOWN, FadeIn, LaggedStart, Scene, Square
from manim.animation.animation import prepare_animation
from manim.mobject.mobject import Mobject

import utils
from utils.mobjects import header
from utils.scene import PLAYBACK_SPEED, ConceptScene

REPO = Path(__file__).resolve().parents[1]
INIT = REPO / "utils" / "__init__.py"

# A reST literal block: "...as usual::" then a blank line then an indented run.
CODE_BLOCK = re.compile(r"::\n\n((?:(?:[ \t]+[^\n]*)?\n)+)")


def imported_names() -> set[str]:
    """Public names `utils/__init__.py` pulls in from submodules."""
    tree = ast.parse(INIT.read_text(encoding="utf-8"))
    return {
        (alias.asname or alias.name)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
        if not (alias.asname or alias.name).startswith("_")
    }


def test_all_lists_exactly_what_is_imported():
    """Both halves of the re-export rule, in one assertion each.

    The import is what makes `from utils import X` resolve for a concept
    module. `__all__` is what covers `from utils import *` and what stops ruff
    F401 rejecting the re-export. Doing one without the other is the failure.
    """
    exported = set(utils.__all__)
    imported = imported_names()

    assert not (imported - exported), (
        f"imported into utils/__init__.py but missing from __all__: "
        f"{sorted(imported - exported)} — ruff F401 will reject these"
    )
    assert not (exported - imported), (
        f"listed in __all__ but not imported: {sorted(exported - imported)} — "
        "a wildcard import would raise AttributeError"
    )


def test_every_exported_name_actually_resolves():
    missing = [name for name in utils.__all__ if not hasattr(utils, name)]
    assert not missing, f"__all__ names that do not resolve: {missing}"


@pytest.mark.parametrize("source", sorted((REPO / "utils").glob("*.py")), ids=lambda p: p.name)
def test_docstring_examples_parse(source):
    """A copy-pasteable example that does not even parse is worse than none.

    Only syntax is checked here; the semantic half is pinned by
    `test_title_must_be_wrapped_in_an_animation` below, which is the invariant
    the ConceptScene example actually got wrong.
    """
    tree = ast.parse(source.read_text(encoding="utf-8"))
    nodes = [tree] + [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    for node in nodes:
        doc = ast.get_docstring(node, clean=False)
        if not doc:
            continue
        for block in CODE_BLOCK.findall(doc):
            snippet = textwrap.dedent(block)
            if not snippet.strip():
                continue
            try:
                compile(snippet, f"{source.name}:docstring", "exec")
            except SyntaxError as exc:  # pragma: no cover - the assert reports it
                pytest.fail(f"{source.name} docstring example does not parse: {exc}\n{snippet}")


def conceptscene_example() -> str:
    """The code block from ConceptScene's docstring, dedented."""
    tree = ast.parse((REPO / "utils" / "scene.py").read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ConceptScene")
    blocks = CODE_BLOCK.findall(ast.get_docstring(node, clean=False) or "")
    assert blocks, "ConceptScene's docstring no longer contains a code example"
    return textwrap.dedent(blocks[-1])


def test_documented_example_wraps_title_in_an_animation():
    """Guards the actual docstring text, not an equivalent written by hand.

    The example used to be ``self.play(self.title("My Rule"))``, which raises.
    The test below pins the underlying invariant, but it would happily pass
    while the docstring said the wrong thing again — so this one parses the
    documented snippet and checks the shape of the call.
    """
    tree = ast.parse(conceptscene_example())
    plays = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "play"
    ]
    assert plays, "the ConceptScene example no longer calls self.play"

    for call in plays:
        for argument in call.args:
            passed_bare = (
                isinstance(argument, ast.Call)
                and isinstance(argument.func, ast.Attribute)
                and argument.func.attr == "title"
            )
            assert not passed_bare, (
                "the documented example passes self.title(...) straight into self.play(), "
                "which raises TypeError — wrap it in an animation such as FadeIn"
            )


class _Probe(ConceptScene):
    """Instantiable stand-in; pacing is exercised without rendering."""

    def construct(self):  # pragma: no cover - never rendered
        pass


def test_conceptscene_stretches_play_to_the_native_pace(monkeypatch):
    """Every route into ``play`` must come out slowed by 1/PLAYBACK_SPEED.

    The pace exists because the videos were being watched at 0.75x manually,
    which judders a 60 fps file. All three call shapes are pinned: an explicit
    ``run_time`` kwarg, an animation's own default, and a composite whose lag
    structure has to stretch with it.
    """
    assert 0 < PLAYBACK_SPEED < 1, "a pace >= 1 would make this test vacuous"

    captured = {}

    def spy_play(self, *animations, **kwargs):
        captured["animations"] = animations
        captured["kwargs"] = kwargs

    monkeypatch.setattr(Scene, "play", spy_play)
    scene = _Probe()

    scene.play(FadeIn(Square()), run_time=1.5)
    assert captured["kwargs"]["run_time"] == pytest.approx(1.5 / PLAYBACK_SPEED)

    scene.play(FadeIn(Square()))  # manim's default run_time is 1.0
    assert captured["animations"][0].run_time == pytest.approx(1.0 / PLAYBACK_SPEED)

    group = LaggedStart(FadeIn(Square()), FadeIn(Square()), lag_ratio=0.5)
    original = group.run_time
    scene.play(group)
    assert captured["animations"][0].run_time == pytest.approx(original / PLAYBACK_SPEED)


def test_conceptscene_play_accepts_iterables_of_animations(monkeypatch):
    """``play([...])`` and generator arguments are manim API, not an accident.

    ``Scene.compile_animations`` flattens its arguments before preparing
    them; the pacing override sits in front of that and must do the same, or
    a list that manim would happily play raises TypeError in the override.
    """
    captured = {}

    def spy_play(self, *animations, **kwargs):
        captured["animations"] = animations

    monkeypatch.setattr(Scene, "play", spy_play)
    scene = _Probe()

    scene.play([FadeIn(Square()), FadeIn(Square())])
    assert len(captured["animations"]) == 2
    assert all(a.run_time == pytest.approx(1.0 / PLAYBACK_SPEED) for a in captured["animations"])

    scene.play(FadeIn(Square()) for _ in range(3))  # a generator, same contract
    assert len(captured["animations"]) == 3


def test_conceptscene_stretches_wait_exactly_once(monkeypatch):
    """A hold is part of the pacing — but scaled once, not twice.

    ``Scene.wait`` funnels a ``Wait`` animation through ``play``, so the
    override there already covers it; a separate ``wait`` override stretched
    every hold by 1/PLAYBACK_SPEED**2, which is the bug this test pins. The
    first draft of the pacing change shipped exactly that and a rendered
    scene came out 1.8 s too long.
    """
    captured = {}

    def spy_play(self, *animations, **kwargs):
        captured["animations"] = animations

    monkeypatch.setattr(Scene, "play", spy_play)
    _Probe().wait(2.0)

    (wait_animation,) = captured["animations"]
    assert wait_animation.run_time == pytest.approx(2.0 / PLAYBACK_SPEED)
    assert wait_animation.run_time != pytest.approx(2.0 / PLAYBACK_SPEED**2)


def test_title_must_be_wrapped_in_an_animation():
    """Pins the invariant the ConceptScene docstring example got wrong.

    `title()` returns a mobject so the caller controls how it enters. That is
    deliberate, but it means `self.play(self.title(...))` raises — which is
    exactly what the documented example used to say. Locking both directions
    here means the example cannot drift back.
    """
    built = header("My Rule")
    assert isinstance(built, Mobject)

    prepare_animation(FadeIn(built, shift=0.3 * DOWN))  # the documented form works

    with pytest.raises(TypeError):
        prepare_animation(header("My Rule"))  # a bare mobject does not
