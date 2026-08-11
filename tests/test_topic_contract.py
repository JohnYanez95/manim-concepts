"""Mechanical enforcement of the topic contract.

The contract lives in the root README under "The topic contract". Prose that
nobody checks decays, and CodeRabbit reviewing a diff cannot see that a topic
added six months ago has since drifted — so the parts of the contract that can
be checked by a machine are checked here.

Modules are parsed with `ast` rather than imported: this needs class names,
docstrings and their source order, none of which require executing manim.
"""

import ast
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

REQUIRED_SECTIONS = ("## Scope", "## Concepts", "## References", "## Ideas not yet built")

# A markdown table row whose first cell is a number: "| 3 | `SceneName` | ..."
NUMBERED_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|")

# "not" as a word. Substring matching would accept "notation" or "another" and
# pass a Scope section that never states an exclusion.
STATES_AN_EXCLUSION = re.compile(r"\bnot\b")

# A reference list item, which must carry a verification checkbox. Both tick
# spellings are accepted: humans write "[X]" as often as "[x]", GitHub renders
# both as checked, and a human's tick must never red the gate over its case.
REFERENCE_ITEM = re.compile(r"^\s*-\s+(\[[ xX]\])\s")


def topic_dirs() -> list[Path]:
    """Every directory holding at least one concept module."""
    return sorted({path.parent for path in REPO.glob("*/*_manim.py")})


def concept_modules(topic: Path) -> list[Path]:
    return sorted(topic.glob("*_manim.py"))


def scenes_in(module: Path) -> list[ast.ClassDef]:
    """Scene classes defined in `module`, in source order."""
    tree = ast.parse(module.read_text(encoding="utf-8"))
    return [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(isinstance(b, ast.Name) and b.id.endswith("Scene") for b in node.bases)
    ]


def section(text: str, heading: str) -> str:
    """The body of one `##` section, up to the next `##`."""
    start = text.index(heading) + len(heading)
    rest = text[start:]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


TOPICS = topic_dirs()
MODULES = [module for topic in TOPICS for module in concept_modules(topic)]


def test_there_is_at_least_one_topic():
    """Guards the parametrised tests below from silently covering nothing."""
    assert TOPICS, "no topic directories found — the glob or the layout changed"


@pytest.mark.parametrize("topic", TOPICS, ids=lambda p: p.name)
def test_topic_has_a_readme(topic):
    assert (topic / "README.md").is_file(), (
        f"{topic.name}/ has concept modules but no README.md; "
        "a new topic directory without one is an incomplete change"
    )


@pytest.mark.parametrize("topic", TOPICS, ids=lambda p: p.name)
def test_topic_readme_has_every_required_section(topic):
    text = (topic / "README.md").read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_SECTIONS if heading not in text]
    assert not missing, f"{topic.name}/README.md is missing: {', '.join(missing)}"


@pytest.mark.parametrize("topic", TOPICS, ids=lambda p: p.name)
def test_topic_readme_sections_are_in_the_declared_order(topic):
    """The contract lists the four sections *in an order*, so check the order.

    Scope before the table before references is how a reader decides whether a
    topic is the one they want before being shown its contents.
    """
    text = (topic / "README.md").read_text(encoding="utf-8")
    positions = [text.index(heading) for heading in REQUIRED_SECTIONS if heading in text]
    assert positions == sorted(positions), (
        f"{topic.name}/README.md sections are out of order; expected "
        f"{' → '.join(REQUIRED_SECTIONS)}"
    )


@pytest.mark.parametrize("topic", TOPICS, ids=lambda p: p.name)
def test_scope_says_what_is_not_covered(topic):
    """The exclusions half is what keeps a topic from becoming a junk drawer."""
    scope = section((topic / "README.md").read_text(encoding="utf-8"), "## Scope").lower()
    assert STATES_AN_EXCLUSION.search(scope), (
        f"{topic.name}/README.md Scope does not say what the topic deliberately excludes"
    )


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_every_module_is_listed_in_its_topic_readme(module):
    text = (module.parent / "README.md").read_text(encoding="utf-8")
    assert module.name in text, f"{module.name} has no entry in {module.parent.name}/README.md"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_scenes_subclass_conceptscene(module):
    """Subclassing `Scene` directly skips the shared background and title.

    `scenes_in` matches any base ending in "Scene" precisely so that a class
    inheriting `Scene` is still *found* here and can be reported, rather than
    slipping past the whole contract suite unnoticed.
    """
    wrong = [
        scene.name
        for scene in scenes_in(module)
        if not any(isinstance(b, ast.Name) and b.id == "ConceptScene" for b in scene.bases)
    ]
    assert not wrong, f"{module.name}: scenes not subclassing ConceptScene: {wrong}"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_module_has_the_render_cli_entry_point(module):
    """Without it the module is not runnable, which is the repo's whole premise.

    `uv run python <topic>/<concept>_manim.py` is the documented way to render
    anything here; a concept file missing the block is importable but dead.
    """
    text = module.read_text(encoding="utf-8")
    assert 'if __name__ == "__main__":' in text, f"{module.name} has no __main__ block"
    assert "render_cli()" in text, f"{module.name} does not call render_cli()"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_every_scene_has_a_docstring(module):
    """The first line is what `--list` prints, so a missing one degrades the CLI."""
    undocumented = [scene.name for scene in scenes_in(module) if not ast.get_docstring(scene)]
    assert not undocumented, f"{module.name}: scenes without a docstring: {undocumented}"


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_readme_enumerates_scenes_in_source_order(module):
    """The concepts table is the viewing order, and must agree with the code.

    Scenes render numbered by source position (``03_CombinationRule``), so a
    README that lists them in a different order — or renumbers them by hand —
    sends a reader through the videos in an order the author did not intend.
    """
    text = (module.parent / "README.md").read_text(encoding="utf-8")
    source_order = [scene.name for scene in scenes_in(module)]

    rows = [NUMBERED_ROW.match(line) for line in text.splitlines()]
    listed = [(int(m.group(1)), m.group(2)) for m in rows if m]
    listed = [(n, name) for n, name in listed if name in source_order]

    assert [name for _, name in listed] == source_order, (
        f"{module.parent.name}/README.md lists {[n for _, n in listed]} "
        f"but {module.name} defines {source_order}"
    )
    assert [n for n, _ in listed] == list(range(1, len(source_order) + 1)), (
        f"{module.parent.name}/README.md scene numbers are not 1..n in order"
    )


@pytest.mark.parametrize("module", MODULES, ids=lambda p: p.name)
def test_every_scene_row_covers_all_three_levels(module):
    """Each row must answer what it says, why it's true, and when it's useful.

    The three levels of understanding are the repo's narrative spine, and the
    third is the one that gets skipped — "why is it true" is the satisfying
    part to build, so scenes stop there and teach a fact instead of a tool.
    A row can satisfy the numbering check with those cells blank, so they are
    checked separately here.
    """
    text = (module.parent / "README.md").read_text(encoding="utf-8")
    source_order = [scene.name for scene in scenes_in(module)]
    # number | scene | formula | what it says | why it's true | when it's useful
    levels = {3: "what it says", 4: "why it's true", 5: "when it's useful"}

    gaps = []
    for line in text.splitlines():
        match = NUMBERED_ROW.match(line)
        if not match or match.group(2) not in source_order:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            gaps.append(f"{match.group(2)} (only {len(cells)} columns, needs 6)")
            continue
        for index, label in levels.items():
            if not cells[index]:
                gaps.append(f"{match.group(2)} has no '{label}'")

    assert not gaps, f"{module.parent.name}/README.md: {gaps}"


@pytest.mark.parametrize("topic", TOPICS, ids=lambda p: p.name)
def test_references_carry_a_verification_checkbox(topic):
    """Every reference is human-gated, so every one needs an explicit state."""
    references = section((topic / "README.md").read_text(encoding="utf-8"), "## References")
    items = [line for line in references.splitlines() if line.lstrip().startswith("- ")]
    assert items, f"{topic.name}/README.md has an empty References section"

    unmarked = [line.strip() for line in items if not REFERENCE_ITEM.match(line)]
    assert not unmarked, (
        f"{topic.name}/README.md references without a '- [ ]' or '- [x]' checkbox: {unmarked}"
    )
