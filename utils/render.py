"""Turn a concept module into a self-contained, runnable program.

The point of this module is that nobody has to remember manim's CLI. Instead of

    manim -qm combinatorics/counting_rules_manim.py MultiplicativeRule

a concept renders with

    uv run python combinatorics/counting_rules_manim.py

and every knob has a spelled-out name (``--quality high``, not ``-qh``). The
concept module opts in with two lines at the bottom::

    if __name__ == "__main__":
        render_cli()

``render_cli`` drives manim's own ``tempconfig`` + ``Scene.render()`` API
directly, so this is not a subprocess wrapper around the manim binary — the
scenes render in-process with configuration this module controls.
"""

from __future__ import annotations

import argparse
import inspect
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from types import FrameType

from manim import Scene, tempconfig

__all__ = ["QUALITIES", "media_root", "numbered_stem", "render_cli", "scene_order"]


# Long names for manim's quality presets. The -ql/-qm/-qh/-qk spelling is
# deliberately never surfaced: "draft" says what it is for, "-ql" does not.
QUALITIES: dict[str, str] = {
    "draft": "low_quality",  # 480p15  — iterating on timing and layout
    "medium": "medium_quality",  # 720p30  — quick review copy
    "high": "high_quality",  # 1080p60 — the default; publishable as-is
    "4k": "fourk_quality",  # 2160p60 — slow; only when it must be 4K
}

# 1080p by default: the finished artifact is the point of this repo, and a
# render nobody would actually share is a worse default than one that costs a
# little more wall-clock. Use `--quality draft` while iterating on a scene.
DEFAULT_QUALITY = "high"
FORMATS = ("mp4", "gif", "png", "webm", "mov")


def media_root() -> Path:
    """Where renders are written.

    Pinned to ``<repo>/media`` rather than the working directory, so
    ``python combinatorics/foo.py`` and ``cd combinatorics && python foo.py``
    put their output in the same place. ``MANIM_CONCEPTS_MEDIA_DIR`` overrides
    it for one-off renders outside the repo.
    """
    override = os.environ.get("MANIM_CONCEPTS_MEDIA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    # utils/render.py -> utils/ -> repo root. Correct under an editable install,
    # which is how uv installs this project.
    return Path(__file__).resolve().parents[1] / "media"


def _caller_frame() -> FrameType:
    """The frame of the concept module that called ``render_cli``."""
    stack = inspect.stack()
    # [0] is _caller_frame, [1] is render_cli, [2] is the concept module.
    return stack[2].frame


def _discover_scenes(namespace: dict[str, object]) -> list[type[Scene]]:
    """Every Scene subclass defined *in* the calling module, in source order.

    Auto-discovery rather than a hand-maintained ``SCENES = [...]`` list: the
    list would be one more thing to forget when adding a scene, and the failure
    mode is silent (the new scene simply never renders). ``__module__`` is
    checked so that Scene classes merely *imported* into the module — including
    ``ConceptScene`` itself — are not mistaken for renderable content. Module
    dicts preserve insertion order, so scenes come out in the order written.
    """
    module_name = namespace.get("__name__")
    return [
        obj
        for obj in namespace.values()
        if isinstance(obj, type)
        and issubclass(obj, Scene)
        and obj.__module__ == module_name
        and not obj.__name__.startswith("_")
    ]


def scene_order(scenes: Sequence[type[Scene]]) -> dict[str, int]:
    """Map each scene name to its 1-based position in the module.

    Source order *is* the intended viewing order — a concept module is written
    as a sequence that builds toward one idea, so the order the scenes are
    defined in is the order someone should watch them in.
    """
    return {scene.__name__: i for i, scene in enumerate(scenes, start=1)}


def numbered_stem(scene: type[Scene], order: dict[str, int]) -> str:
    """Output filename stem for `scene`, prefixed with its position.

    ``02_PermutationRule``. The prefix is what lets a directory listing be
    watched top to bottom without cross-referencing the topic README.

    The position is taken over *every* scene in the module, never over the
    selected subset: rendering the third scene on its own must still produce
    ``03_``, or the number would mean something different depending on which
    flags were passed.
    """
    return f"{order[scene.__name__]:02d}_{scene.__name__}"


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def _build_parser(description: str, scenes: Sequence[type[Scene]]) -> argparse.ArgumentParser:
    names = ", ".join(scene.__name__ for scene in scenes) or "none found"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=f"Scenes in this module: {names}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=list(QUALITIES),
        default=DEFAULT_QUALITY,
        help=f"render quality (default: {DEFAULT_QUALITY})",
    )
    parser.add_argument(
        "-s",
        "--scene",
        action="append",
        dest="scene_names",
        metavar="NAME",
        help="render only this scene; repeat for several (default: all)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=FORMATS,
        default="mp4",
        help="output container (default: mp4)",
    )
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        help="open each render when it finishes",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list_only",
        help="print the scenes in this module and exit",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=_positive_int,
        default=1,
        metavar="N",
        help=(
            "render scenes in N parallel processes — scene renders are "
            "independent, so this can cut a module's wall-clock deeply "
            "(cores permitting); run a draft pass first so the shared "
            "LaTeX cache is warm"
        ),
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="ignore cached partial movies; use while iterating on a scene",
    )
    parser.add_argument(
        "--transparent",
        action="store_true",
        help="render with an alpha channel instead of the theme background",
    )
    return parser


def _select(scenes: Sequence[type[Scene]], wanted: list[str] | None) -> list[type[Scene]]:
    """Filter `scenes` down to `wanted`, or return all of them.

    Raises SystemExit with the valid names on a typo — a misspelled scene name
    should not quietly render nothing and report success.
    """
    if not wanted:
        return list(scenes)
    by_name = {scene.__name__: scene for scene in scenes}
    unknown = [name for name in wanted if name not in by_name]
    if unknown:
        available = ", ".join(by_name) or "none"
        raise SystemExit(
            f"error: no such scene: {', '.join(unknown)}\n       available scenes: {available}"
        )
    # Preserve the order the user asked for, and drop duplicates.
    return list(dict.fromkeys(by_name[name] for name in wanted))


def _render_parallel(selected: Sequence[type[Scene]], args, namespace: dict[str, object]) -> int:
    """Fan the selected scenes out over subprocesses, one scene each.

    Subprocesses rather than threads or per-scene tempconfig: manim's
    config is a process-global (see render_cli below), so true isolation
    needs separate interpreters. Each child is this same CLI with one
    ``-s``, which also keeps the ``02_`` numbering correct — the child
    numbers over the whole module, not the subset.

    Output is captured per scene and replayed only on failure, since six
    interleaved progress bars are noise nobody can read.
    """
    import subprocess
    from concurrent.futures import ThreadPoolExecutor

    module_file = str(namespace.get("__file__", ""))

    def run(scene: type[Scene]) -> tuple[str, subprocess.CompletedProcess]:
        command = [sys.executable, module_file, "-s", scene.__name__]
        command += ["-q", args.quality, "-f", args.format]
        if args.no_cache:
            command.append("--no-cache")
        if args.transparent:
            command.append("--transparent")
        if args.preview:
            command.append("--preview")
        result = subprocess.run(command, capture_output=True, text=True)
        return scene.__name__, result

    jobs = min(args.jobs, len(selected))
    print(f"Rendering {len(selected)} scenes across {jobs} processes ({args.quality})")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(run, selected))

    failed = False
    for name, result in results:
        if result.returncode == 0:
            print(f"  {name}: ok")
        else:
            failed = True
            print(f"  {name}: FAILED (exit {result.returncode})")
            output = "\n".join(part for part in (result.stdout, result.stderr) if part)
            tail = output[-2000:]
            if tail:
                print(tail)
    print(f"\nOutput under {media_root()}")
    return 1 if failed else 0


def render_cli(
    scenes: Sequence[type[Scene]] | None = None,
    *,
    description: str | None = None,
    argv: Sequence[str] | None = None,
) -> int:
    """Parse arguments and render. Returns a process exit code.

    Args:
        scenes: Scene classes to expose. Defaults to every Scene subclass
            defined in the calling module, in source order.
        description: ``--help`` blurb. Defaults to the calling module's
            docstring.
        argv: Argument list, for testing. Defaults to ``sys.argv[1:]``.
    """
    frame = _caller_frame()
    namespace = frame.f_globals

    if scenes is None:
        scenes = _discover_scenes(namespace)
    if description is None:
        doc = namespace.get("__doc__")
        description = doc.strip() if isinstance(doc, str) else "Render this concept."

    args = _build_parser(description, scenes).parse_args(argv)

    if args.list_only:
        # Numbered, because the list doubles as the viewing order.
        listing_order = scene_order(scenes)
        for scene in scenes:
            summary = (scene.__doc__ or "").strip().splitlines()
            position = listing_order[scene.__name__]
            print(f"{position:>2}. {scene.__name__:<24}{summary[0] if summary else ''}".rstrip())
        return 0

    selected = _select(scenes, args.scene_names)
    if not selected:
        print(f"No scenes found in {namespace.get('__file__', 'this module')}.", file=sys.stderr)
        return 1

    if args.jobs > 1 and len(selected) > 1:
        return _render_parallel(selected, args, namespace)

    root = media_root()
    order = scene_order(scenes)

    overrides = {
        "quality": QUALITIES[args.quality],
        "media_dir": str(root),
        "format": args.format,
        "preview": args.preview,
        "disable_caching": args.no_cache,
        "transparent": args.transparent,
        # Manim names the output directory after the input file's stem. Without
        # this, every module's renders would collide in one anonymous folder.
        "input_file": str(namespace.get("__file__", "")),
    }

    for position, scene_class in enumerate(selected, start=1):
        stem = numbered_stem(scene_class, order)
        print(f"[{position}/{len(selected)}] {stem} ({args.quality})")
        # One config scope per scene, not one for the batch. Two things depend
        # on this. First, output_file has to differ per scene, and manim reads
        # it from the global config. Second, on finishing a render manim writes
        # the finished path *back* into that global config
        # (SceneFileWriter.print_file_ready_message), and the next scene's
        # init_output_directories prefers config["output_file"] over the scene
        # name — so a batch sharing one scope silently collapses onto the first
        # scene's filename. tempconfig restores the config on exit, which
        # discards that leak before the next scene starts.
        with tempconfig({**overrides, "output_file": stem}):
            scene_class().render()

    print(f"\nOutput under {root}")
    return 0
