"""Answer anchors for the gradient-descent problem set (plan 012 R3).

Every descent is actually run — the 1-D examples in exact arithmetic
where the update is a clean ratio, and the chapter's headline loss walk
reproduced from scratch: plain GD on the repo matrix's free logits,
learning rate 1.0, gradient y - gamma computed by 15-path enumeration.
The recorded losses must match plan 010's anchor-M trajectory at 4 dp.
Run: prints `problem_id: answer`.
"""

from itertools import product
from math import exp, log

EPS = "e"  # blank, ASCII-safe

# The repo's worked matrix (plan 010, anchor K): rows t=1..4, cols (A, B, eps).
REPO_MATRIX = [
    (0.7, 0.2, 0.1),
    (0.6, 0.1, 0.3),
    (0.2, 0.1, 0.7),
    (0.1, 0.7, 0.2),
]
SYMBOLS = ("A", "B", EPS)


def collapse(path: tuple[str, ...]) -> str:
    merged = [ch for i, ch in enumerate(path) if i == 0 or path[i - 1] != ch]
    return "".join(ch for ch in merged if ch != EPS)


AB_PATHS = [p for p in product(SYMBOLS, repeat=4) if collapse(p) == "AB"]
assert len(AB_PATHS) == 15


def descend_parabola(w: float, lr: float, steps: int) -> list[float]:
    """w <- w - lr * f'(w) on f(w) = w^2 (so f'(w) = 2w)."""
    walk = [w]
    for _ in range(steps):
        w = w - lr * 2 * w
        walk.append(w)
    return walk


def p1_parabola_descent() -> str:
    """f(w) = w^2, w0 = 4, lr = 1/4: exact halving; below 0.01 at step 9."""
    walk = descend_parabola(4.0, 0.25, 3)
    assert walk == [4.0, 2.0, 1.0, 0.5]
    steps = 0
    w = 4.0
    while abs(w) >= 0.01:
        w /= 2
        steps += 1
    assert steps == 9 and abs(w) == 4 / 2**9
    return "4 -> 2 -> 1 -> 1/2; first below 0.01 after 9 steps"


def p2_learning_rates() -> str:
    """Same parabola, four rates: the update multiplies w by (1 - 2*lr)."""
    verdicts = []
    for lr, factor, verdict in (
        (0.25, 0.5, "converges"),
        (0.75, -0.5, "overshoots, converges"),
        (1.0, -1.0, "ping-pongs forever"),
        (1.25, -1.5, "diverges"),
    ):
        walk = descend_parabola(4.0, lr, 8)
        assert all(abs(b - factor * a) < 1e-12 for a, b in zip(walk, walk[1:], strict=False))
        assert (abs(walk[-1]) < abs(walk[0])) == (abs(factor) < 1)
        verdicts.append(f"lr {lr}: {verdict}")
    return "; ".join(verdicts)


def p3_stall_is_not_a_certificate() -> str:
    """Double well f = w^4/4 - w^2/2: descent stalls at the hilltop w = 0."""

    def slope(w: float) -> float:
        return w**3 - w

    def run(w: float) -> float:
        for _ in range(2000):
            w = w - 0.1 * slope(w)
        return w

    assert run(0.0) == 0.0  # slope exactly zero: the walk never moves
    assert abs(run(0.5) - 1.0) < 1e-9
    assert abs(run(-0.5) + 1.0) < 1e-9
    # The stall at 0 sits where the slope changes + to - : a hilltop.
    assert slope(-0.01) > 0 > slope(0.01)
    return "from 0.0 stays at 0.0 (hilltop); from +-0.5 reaches +-1"


def ctc_loss_and_gradient(logits: list[list[float]]) -> tuple[float, list[list[float]]]:
    """-ln P(AB|X) and its gradient y - gamma, by 15-path enumeration."""
    y = []
    for row in logits:
        top = max(row)
        exps = [exp(u - top) for u in row]
        total = sum(exps)
        y.append([v / total for v in exps])
    prob = 0.0
    occupancy = [[0.0] * 3 for _ in range(4)]
    for path in AB_PATHS:
        weight = 1.0
        for t, ch in enumerate(path):
            weight *= y[t][SYMBOLS.index(ch)]
        prob += weight
        for t, ch in enumerate(path):
            occupancy[t][SYMBOLS.index(ch)] += weight
    grad = [[y[t][k] - occupancy[t][k] / prob for k in range(3)] for t in range(4)]
    return -log(prob), grad


def p4_the_walk_is_front_loaded() -> str:
    """Reproduce the anchor-M walk (lr 1.0, from u = ln y) and compare
    the per-step shrink factor of its first and last recorded legs."""
    logits = [[log(v) for v in row] for row in REPO_MATRIX]
    recorded = {}
    for it in range(5001):
        loss, grad = ctc_loss_and_gradient(logits)
        if it in (0, 10, 50, 200, 5000):
            recorded[it] = loss
        logits = [
            [u - 1.0 * g for u, g in zip(row, grow, strict=True)]
            for row, grow in zip(logits, grad, strict=True)
        ]
    walk = {it: round(loss, 4) for it, loss in recorded.items()}
    assert walk == {0: 0.7181, 10: 0.1602, 50: 0.0356, 200: 0.0088, 5000: 0.0003}
    early = (recorded[10] / recorded[0]) ** (1 / 10)
    late = (recorded[5000] / recorded[200]) ** (1 / 4800)
    assert round(early, 2) == 0.86
    assert round(late, 4) == 0.9993
    return (
        f"walk reproduced {walk}; per-step shrink {early:.2f} over the first "
        f"ten steps vs {late:.4f} over the last 4800"
    )


ANSWERS = {
    "gradient-descent.1": p1_parabola_descent,
    "gradient-descent.2": p2_learning_rates,
    "gradient-descent.3": p3_stall_is_not_a_certificate,
    "gradient-descent.4": p4_the_walk_is_front_loaded,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
