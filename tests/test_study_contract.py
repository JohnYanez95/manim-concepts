"""The study-guide track's structural contract (plan 012).

Structure only — LaTeX compilation is `make study`'s job, kept out of the
test suite for toolchain weight. What must never drift silently:
retrievals resolve, anchors are in sync and well-formed, problems carry
their single-sourced solutions, and generated files match their sources.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "study_guides"
PRIMITIVES = STUDY / "primitives"

GUIDES = sorted(d for d in STUDY.iterdir() if d.is_dir() and d.name != "primitives")


def tex_sources():
    return sorted(STUDY.rglob("*.tex"))


def test_every_retrieval_resolves():
    """A \\primitive{name} call must point at a hosted primitive file."""
    for tex in tex_sources():
        for name in re.findall(r"\\primitive\{([^}]+)\}", tex.read_text(encoding="utf-8")):
            target = PRIMITIVES / f"{name}.tex"
            assert target.exists(), f"{tex.name} retrieves missing primitive {name!r}"


def test_guides_share_one_manifest():
    """Guide and solutions manual must input the same manifest — the
    single-source rule that keeps their numbering identical."""
    for guide_dir in GUIDES:
        for wrapper in ("guide.tex", "solutions.tex"):
            text = (guide_dir / wrapper).read_text(encoding="utf-8")
            assert re.search(r"\\input\{manifest\}", text), (
                f"{guide_dir.name}/{wrapper} does not input the shared manifest"
            )
            assert "\\primitive{" not in text, (
                f"{guide_dir.name}/{wrapper} retrieves primitives directly; "
                "retrievals belong in manifest.tex"
            )


def test_anchor_keys_exist():
    """Every \\anchor{key} used anywhere must exist in anchors.yaml."""
    known = set(yaml.safe_load((STUDY / "anchors.yaml").read_text(encoding="utf-8")))
    for tex in tex_sources():
        for key in re.findall(r"\\anchor\{([^}]+)\}", tex.read_text(encoding="utf-8")):
            assert key in known, f"{tex.name} uses unknown anchor key {key!r}"


def test_anchor_entries_carry_provenance():
    entries = yaml.safe_load((STUDY / "anchors.yaml").read_text(encoding="utf-8"))
    for key, meta in entries.items():
        for field in ("value", "source", "method"):
            assert field in meta, f"anchor {key!r} missing {field!r}"


def test_generated_files_in_sync():
    """anchors.tex and references.bib must match a fresh generator run.

    Runs the real scripts against a scratch copy is overkill; instead the
    scripts are deterministic, so regenerating in place and comparing bytes
    would dirty the tree on failure. Import their render paths instead.
    """
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import build_anchors
        import sync_references

        entries = yaml.safe_load(build_anchors.YAML_PATH.read_text(encoding="utf-8"))
        assert build_anchors.TEX_PATH.read_text(encoding="utf-8") == build_anchors.render(
            entries
        ), "anchors.tex out of sync — run tools/build_anchors.py"
        assert sync_references.BIB_PATH.read_text(encoding="utf-8") == sync_references.render(
            sync_references.collect()
        ), "references.bib out of sync — run tools/sync_references.py"
    finally:
        sys.path.pop(0)


def test_every_problem_has_a_solution():
    """Single-sourcing means EXACTLY one solution inside each problem —
    cardinality alone would pass a doubled solution next to a missing one."""
    for tex in PRIMITIVES.glob("*.tex"):
        body = tex.read_text(encoding="utf-8")
        starts = [m.start() for m in re.finditer(r"\\begin\{problem\}", body)]
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else len(body)
            inside = len(re.findall(r"\\begin\{solution\}", body[start:end]))
            assert inside == 1, f"{tex.name}: problem {i + 1} contains {inside} solution env(s)"


def test_every_citation_resolves():
    """Every \\cite key in the study sources exists in references.bib.

    This replaces checkcites in the build gate: its bcf parsing rejects
    the relative bib path, and this check is stronger anyway — it runs
    without LaTeX, inside `make check`. (Unused entries are fine by
    design: the bib carries every README reference; documents print only
    what they cite.)
    """
    bib = (STUDY / "references.bib").read_text(encoding="utf-8")
    known = set(re.findall(r"@misc\{([^,]+),", bib))
    for tex in tex_sources():
        for keys in re.findall(r"\\cite\{([^}]+)\}", tex.read_text(encoding="utf-8")):
            for key in keys.split(","):
                assert key.strip() in known, f"{tex.name} cites unknown key {key.strip()!r}"


def test_ticks_untouched_by_sync():
    """The sync script must never write markdown — the never-tick rule.

    Structural guarantee: the script's only write_text call targets
    BIB_PATH. A second write target would need a new argument here, which
    is exactly the review speed bump this test exists to create.
    """
    script = (ROOT / "tools" / "sync_references.py").read_text(encoding="utf-8")
    writes = re.findall(r"(\w+)\.write_text", script)
    assert writes == ["BIB_PATH"], f"sync_references.py writes to {writes}"


def test_verified_state_survives():
    """Spot-check: a maintainer-ticked entry lands verified={yes}.

    Renders in memory — the test must never write references.bib itself.
    """
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import sync_references

        bib = sync_references.render(sync_references.collect())
    finally:
        sys.path.pop(0)
    assert "verified = {yes}" in bib
