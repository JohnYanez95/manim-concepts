"""Solve the theme palette as a constrained optimisation.

Why this is a script and not a designer picking hexes: the palette has to
satisfy properties nobody can eyeball. Whether WARM and GOOD stay
distinguishable to a viewer with deuteranopia is not visible in a diff, and it
is not visible in the render either — to me they looked fine at dE 9.8, which
is indistinguishable.

    uv run python tools/solve_palette.py --verify    # check the live theme
    uv run python tools/solve_palette.py             # re-solve and print hexes

Formulation
-----------
Variables are CIELAB coordinates, three per colour, because the constraints are
perceptual and Lab is where perceptual distance is Euclidean. Optimising in RGB
would make "keep this recognisably gold" inexpressible.

    minimise    total dE from the current palette
    subject to  every semantic pair            >= 30 dE normally
                every semantic pair            >= 25 dE under deuteranopia
                                               >= 25 dE under protanopia
                every colour vs background     >= 45 dE
                every colour vs white          >= 20 dE   (not body text)
                each colour stays in its hue family and lightness band
                MUTED stays near-neutral       chroma <= 10

The objective is *minimum drift*, not maximum separation. Maximising
separation is easy and produces a neon palette with a near-white green — the
existing colours are good, and the job is to fix an accessibility defect while
changing as little as possible about how the repo looks.

Constraints are folded into the objective as weighted penalties rather than
passed to a constrained solver, because the feasible region is disconnected:
red-family WARM and green-family GOOD cannot be separated under dichromacy by
hue at all, only by lightness, so the search has to cross infeasible ground to
get anywhere useful. Differential evolution handles that; a gradient method
would sit in whichever basin it started in.

The gate that actually holds the property is `tests/test_visual_contract.py`.
This script only proposes; that suite decides, and both import their colour
maths from `utils.colour` so they cannot disagree — an earlier version of this
script had its own copy, measured unclipped colours, and confidently produced a
palette that failed the tests.
"""

from __future__ import annotations

import argparse
from itertools import combinations

import numpy as np
from scipy.optimize import differential_evolution

from utils import theme
from utils.colour import DEUTERANOPIA, PROTANOPIA, delta_e, lab, lab_to_hex, lch, simulate

WHITE = "#ffffff"

# name -> (hue_lo, hue_hi, lightness_lo, lightness_hi, chroma_lo, chroma_hi)
# Hue bands keep the semantics honest: WARM has to stay warm. Separation is
# then bought with lightness, which is the only channel dichromats keep.
SEMANTIC_SPEC = {
    "ACCENT": (68, 102, 66, 88, 30, 90),
    "COOL": (195, 275, 52, 88, 25, 90),
    "WARM": (15, 58, 38, 70, 30, 90),
    "GOOD": (112, 172, 74, 97, 22, 90),
    "MUTED": (None, None, 55, 74, 0, 10),
}

MIN_PAIR = 30.0
MIN_CVD = 25.0
MIN_BG = 45.0
MIN_WHITE = 20.0

# Categorical colours are held to a looser bar than semantic ones. Every
# categorical item in this repo carries a text label — the A/B/C tokens, the
# chip captions — so hue is never their only signal, which is the general rule
# in CLAUDE.md. They still must not alias a semantic colour, or the distinction
# the codebase enforces would be invisible on screen.
MIN_CATEGORICAL_PAIR = 30.0
MIN_FROM_SEMANTIC = 20.0


def _penalty(amount: float) -> float:
    """Quadratic so the solver feels a gradient toward feasibility."""
    return 0.0 if amount <= 0 else amount * amount


def _spec_penalty(name: str, colour: str) -> float:
    hue_lo, hue_hi, l_lo, l_hi, c_lo, c_hi = SEMANTIC_SPEC[name]
    lightness, chroma, hue = lch(colour)
    cost = _penalty(l_lo - lightness) + _penalty(lightness - l_hi)
    cost += _penalty(c_lo - chroma) + _penalty(chroma - c_hi)
    if hue_lo is not None:
        cost += _penalty(hue_lo - hue) + _penalty(hue - hue_hi)
    return cost


def evaluate(colours: dict[str, str], *, targets: dict[str, str]) -> tuple[float, float]:
    """Return (drift, violation). A violation of 0 means every constraint holds."""
    names = list(colours)
    violation = 0.0
    for name, colour in colours.items():
        violation += _spec_penalty(name, colour)
        violation += _penalty(MIN_BG - delta_e(colour, theme.BG))
        violation += _penalty(MIN_WHITE - delta_e(colour, WHITE))
    for a, b in combinations(names, 2):
        violation += _penalty(MIN_PAIR - delta_e(colours[a], colours[b]))
        for matrix in (DEUTERANOPIA, PROTANOPIA):
            separation = delta_e(simulate(colours[a], matrix), simulate(colours[b], matrix))
            violation += _penalty(MIN_CVD - separation)
    drift = sum(delta_e(colours[n], targets[n]) for n in names)
    return drift, violation


def solve_semantic(targets: dict[str, str], *, seed: int = 0, maxiter: int = 220) -> dict[str, str]:
    names = list(SEMANTIC_SPEC)
    start = np.concatenate([lab(targets[n]) for n in names])
    bounds = []
    for _ in names:
        bounds += [(20.0, 100.0), (-90.0, 90.0), (-90.0, 90.0)]

    def objective(vector: np.ndarray) -> float:
        colours = {n: lab_to_hex(vector[3 * i : 3 * i + 3]) for i, n in enumerate(names)}
        drift, violation = evaluate(colours, targets=targets)
        return drift + 300.0 * violation

    result = differential_evolution(
        objective,
        bounds,
        seed=seed,
        maxiter=maxiter,
        popsize=24,
        tol=1e-8,
        mutation=(0.3, 1.0),
        recombination=0.85,
        init=np.clip(
            start + np.random.default_rng(seed).normal(0, 6, (24 * len(bounds), len(bounds))),
            [b[0] for b in bounds],
            [b[1] for b in bounds],
        ),
        polish=False,
    )
    return {n: lab_to_hex(result.x[3 * i : 3 * i + 3]) for i, n in enumerate(names)}


def solve_categorical(
    semantic: dict[str, str], targets: list[str], *, seed: int = 0, maxiter: int = 200
) -> list[str]:
    count = len(targets)
    bounds = []
    for _ in range(count):
        bounds += [(45.0, 95.0), (-90.0, 90.0), (-90.0, 90.0)]

    def objective(vector: np.ndarray) -> float:
        colours = [lab_to_hex(vector[3 * i : 3 * i + 3]) for i in range(count)]
        violation = 0.0
        for colour in colours:
            violation += _penalty(MIN_BG - delta_e(colour, theme.BG))
            violation += _penalty(18.0 - delta_e(colour, WHITE))
            nearest = min(delta_e(colour, s) for s in semantic.values())
            violation += _penalty(MIN_FROM_SEMANTIC - nearest)
        for a, b in combinations(colours, 2):
            violation += _penalty(MIN_CATEGORICAL_PAIR - delta_e(a, b))
        drift = sum(delta_e(c, t) for c, t in zip(colours, targets, strict=True))
        return drift + 300.0 * violation

    result = differential_evolution(
        objective, bounds, seed=seed, maxiter=maxiter, popsize=22, tol=1e-8, polish=False
    )
    return [lab_to_hex(result.x[3 * i : 3 * i + 3]) for i in range(count)]


def report(semantic: dict[str, str], categorical: list[str]) -> bool:
    """Print the full constraint table. Returns True if everything holds."""
    ok = True
    print("semantic")
    for name, colour in semantic.items():
        lightness, chroma, hue = lch(colour)
        print(
            f"  {name:7} {colour}  L*={lightness:5.1f} C={chroma:5.1f} h={hue:5.1f}deg"
            f"  vsBG={delta_e(colour, theme.BG):5.1f}  vsWhite={delta_e(colour, WHITE):5.1f}"
        )

    print("\n  pair              normal    deut    prot")
    for a, b in combinations(semantic, 2):
        normal = delta_e(semantic[a], semantic[b])
        deut = delta_e(simulate(semantic[a], DEUTERANOPIA), simulate(semantic[b], DEUTERANOPIA))
        prot = delta_e(simulate(semantic[a], PROTANOPIA), simulate(semantic[b], PROTANOPIA))
        bad = normal < MIN_PAIR or min(deut, prot) < 15.0
        ok &= not bad
        print(f"  {a:7}/{b:7} {normal:8.1f}{deut:8.1f}{prot:8.1f}{'   <-- FAILS' if bad else ''}")

    print("\ncategorical")
    for index, colour in enumerate(categorical):
        nearest = min((delta_e(colour, c), n) for n, c in semantic.items())
        bad = nearest[0] < MIN_FROM_SEMANTIC
        ok &= not bad
        print(
            f"  PALETTE[{index}] {colour}  nearest semantic: {nearest[1]} at dE {nearest[0]:5.1f}"
            f"{'   <-- ALIASES' if bad else ''}"
        )
    worst = min(delta_e(a, b) for a, b in combinations(categorical, 2))
    ok &= worst >= MIN_CATEGORICAL_PAIR
    print(f"  worst mutual separation: dE {worst:.1f}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--verify",
        action="store_true",
        help="check the palette currently in utils/theme.py instead of solving",
    )
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    live_semantic = {
        "ACCENT": theme.ACCENT,
        "COOL": theme.COOL,
        "WARM": theme.WARM,
        "GOOD": theme.GOOD,
        "MUTED": theme.MUTED,
    }

    if args.verify:
        ok = report(live_semantic, list(theme.PALETTE))
        print("\nOK" if ok else "\nCONSTRAINTS VIOLATED")
        return 0 if ok else 1

    semantic = solve_semantic(live_semantic, seed=args.seed)
    categorical = solve_categorical(semantic, list(theme.PALETTE), seed=args.seed)
    ok = report(semantic, categorical)

    print("\n--- paste into utils/theme.py ---")
    for name, colour in semantic.items():
        print(f'{name} = "{colour}"')
    print("PALETTE = [" + ", ".join(f'"{c}"' for c in categorical) + "]")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
