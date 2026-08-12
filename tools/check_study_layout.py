"""Layout guardrails for the study guides' TikZ figures.

The print analogue of tools/check_layout.py, and born the same way — from
a shipped collision (the 1.1 outer-product grid missing its right rule,
its cells crowding the product label; REFINEMENTS.md 2026-08-12). Every
``tikzpicture`` in the study sources is rendered standalone, plus each
guide's macro-generated figures (the roadmap at empty and mid progress),
and two measured checks run on each:

- **text overlaps text** — word bounding boxes (pdftotext -bbox) from
  different lines must not intersect;
- **ink crowds text** — a halo ring around every word must be nearly
  clear of ink (rasterized at 150 dpi); a rule or arrow through a
  label's personal space is exactly the class of defect the maintainer
  flagged.

Like the scene linter, this measures geometry, not taste: findings are
fixed or explained, never ignored. Exit 1 on any finding.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
STUDY = ROOT / "study_guides"

DPI = 150
SCALE = DPI / 72.0  # bbox is in points
HALO_PX = 3
INK_THRESHOLD = 180  # gray level below which a pixel counts as ink
HALO_INK_FRACTION = 0.06  # ring more inked than this = crowded

PREAMBLE = r"""
\documentclass[margin=8pt]{standalone}
\providecommand{\StudyRoot}{%s}
\usepackage{theme}
\input{\StudyRoot/anchors}
%s
\begin{document}
%s
\end{document}
"""


def tikz_blocks(tex: Path) -> list[str]:
    body = tex.read_text(encoding="utf-8")
    return re.findall(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", body, re.S)


def figure_sources() -> list[tuple[str, str, str]]:
    """(name, extra-preamble, tikz-source) for every figure to lint."""
    figures = []
    for tex in sorted(STUDY.rglob("*.tex")):
        if tex.name in ("anchors.tex", "macros.tex"):
            continue
        for i, block in enumerate(tikz_blocks(tex), start=1):
            figures.append((f"{tex.parent.name}/{tex.stem}#{i}", "", block))
    # Macro-generated figures: each guide's macros.tex may define \roadmap;
    # render it empty and mid-progress so both states are checked.
    for macros in sorted(STUDY.glob("*/macros.tex")):
        if "\\roadmap" not in macros.read_text(encoding="utf-8"):
            continue
        extra = f"\\input{{{macros.resolve()}}}"
        for n in (0, 7):
            figures.append((f"{macros.parent.name}/roadmap#{n}", extra, f"\\roadmap{{{n}}}"))
    return figures


def render(name: str, extra: str, tikz: str, workdir: Path) -> Path | None:
    tex = workdir / "fig.tex"
    tex.write_text(PREAMBLE % (STUDY.resolve(), extra, tikz), encoding="utf-8")
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "fig.tex"],
        cwd=workdir,
        capture_output=True,
        text=True,
        env={"TEXINPUTS": f"{STUDY.resolve()}:", "PATH": "/usr/bin:/bin"},
    )
    pdf = workdir / "fig.pdf"
    if not pdf.exists():
        tail = "\n".join(result.stdout.splitlines()[-12:])
        print(f"   {name}: FAILED TO COMPILE standalone\n{tail}")
        return None
    return pdf


def word_boxes(pdf: Path) -> list[tuple[str, float, float, float, float]]:
    out = subprocess.run(
        ["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True
    ).stdout
    boxes = []
    # pdftotext -bbox emits XHTML with <word xMin=.. yMin=.. xMax=.. yMax=..>
    for m in re.finditer(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',
        out,
    ):
        x0, y0, x1, y1 = (float(m.group(i)) for i in range(1, 5))
        text = ET.fromstring(f"<w>{m.group(5)}</w>").text or ""
        boxes.append((text, x0, y0, x1, y1))
    return boxes


def overlapping(a, b) -> float:
    _, ax0, ay0, ax1, ay1 = a
    _, bx0, by0, bx1, by1 = b
    w = min(ax1, bx1) - max(ax0, bx0)
    h = min(ay1, by1) - max(ay0, by0)
    return max(w, 0) * max(h, 0)


def same_line(a, b) -> bool:
    _, _, ay0, _, ay1 = a
    _, _, by0, _, by1 = b
    mid_a, mid_b = (ay0 + ay1) / 2, (by0 + by1) / 2
    return abs(mid_a - mid_b) < max(ay1 - ay0, by1 - by0) * 0.5


def check_figure(name: str, pdf: Path, workdir: Path) -> list[str]:
    findings = []
    boxes = word_boxes(pdf)

    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            if not same_line(a, b) and overlapping(a, b) > 0.5:
                findings.append(f'text overlaps text: "{a[0]}" vs "{b[0]}"')

    subprocess.run(
        ["pdftoppm", "-png", "-r", str(DPI), "-gray", str(pdf), str(workdir / "fig")],
        capture_output=True,
    )
    pages = sorted(workdir.glob("fig*.png"))
    if not pages:
        return findings
    img = Image.open(pages[0]).convert("L")
    px = img.load()
    width, height = img.size

    def ink(x: int, y: int) -> bool:
        if 0 <= x < width and 0 <= y < height:
            return px[x, y] < INK_THRESHOLD
        return False

    for text, x0, y0, x1, y1 in boxes:
        left, top = int(x0 * SCALE), int(y0 * SCALE)
        right, bottom = int(x1 * SCALE), int(y1 * SCALE)
        ring_ink = ring_all = 0
        for x in range(left - HALO_PX, right + HALO_PX + 1):
            for y in range(top - HALO_PX, bottom + HALO_PX + 1):
                inside = left <= x <= right and top <= y <= bottom
                if inside:
                    continue
                ring_all += 1
                ring_ink += ink(x, y)
        if ring_all and ring_ink / ring_all > HALO_INK_FRACTION:
            findings.append(f'ink crowds text: "{text}" (halo {ring_ink / ring_all:.0%} inked)')
    return findings


def main() -> int:
    total = 0
    for name, extra, tikz in figure_sources():
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            pdf = render(name, extra, tikz, workdir)
            if pdf is None:
                total += 1
                continue
            findings = check_figure(name, pdf, workdir)
            if findings:
                total += len(findings)
                print(f"   {name}: {len(findings)} finding(s)")
                for f in findings:
                    print(f"      {f}")
            else:
                print(f"   {name}: clean")
    if total:
        print(f"\n{total} finding(s) — fix or explain before the gate")
        return 1
    print("\nall figures clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
