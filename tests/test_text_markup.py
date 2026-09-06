"""Text renders literally — TeX markup in a `Text`/`caption` is a rendering bug.

A frame shipped to the maintainer with a caption reading `p_k = (1/6)^k`:
Pango draws the underscore and the caret as typed. Only `MathTex` reads
TeX. The scan that found it turned up seventeen latent instances across
five modules, so the rule is enforced here rather than by eye: a string
literal handed to a text-rendering call carries no `^`, no `\\command`,
and no `_` glued to an index. Exponents and indices in prose use Unicode
super/subscripts (ᵏ, ⁴, ₖ) or words; anything heavier is a `MathTex`.

Source-level and exact — no pixels, no fonts (ADR 005).
"""

import ast
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MODULES = sorted(REPO.glob("*/*_manim.py")) + [REPO / "docs" / "assets" / "welcome_scene.py"]

# Every call whose first argument is rendered by Pango, not by TeX.
TEXT_CALLS = {"Text", "MarkupText", "Paragraph", "caption", "header", "chip", "token"}

# A caret, a backslash command, or an underscore glued to an index — the
# three ways TeX habits leak into a string that will be drawn as typed.
TEX_MARKUP = re.compile(r"\^|\\[A-Za-z]|_[A-Za-z0-9{(]")


def _literal(node: ast.AST) -> str | None:
    """The static text of a literal, a `+` chain of literals, or an f-string."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _literal(node.left), _literal(node.right)
        if left is None and right is None:
            return None
        return (left or "") + (right or "")
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value for v in node.values if isinstance(v, ast.Constant))
    return None


def _text_literals(path: Path):
    for node in ast.walk(ast.parse(path.read_text())):
        if not (isinstance(node, ast.Call) and node.args):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", "")
        if name in TEXT_CALLS:
            text = _literal(node.args[0])
            if text is not None:
                yield node.lineno, name, text


def test_scan_sees_text_calls():
    """Guards the check below from passing on a module it failed to read."""
    assert sum(1 for path in MODULES for _ in _text_literals(path)) > 100


@pytest.mark.parametrize("path", MODULES, ids=lambda p: p.name)
def test_text_literals_carry_no_tex_markup(path: Path):
    offenders = [
        f"{path.relative_to(REPO)}:{line}: {name}({text!r})"
        for line, name, text in _text_literals(path)
        if TEX_MARKUP.search(text)
    ]
    assert not offenders, (
        "TeX markup inside text that Pango renders literally — use MathTex, "
        "Unicode super/subscripts, or words:\n" + "\n".join(offenders)
    )
