"""Answer anchors for the ctc-gradient problem set (plan 012 R3).

The forward/backward machinery is implemented from scratch in exact
fractions (the 2012 exclusive-beta convention, plan 010 decision 1) and
checked against brute-force path enumeration — the same two independent
routes plan 010's verifier used. The identity y - gamma is additionally
checked against finite differences of the loss at the logits, and the
free-logit training walk reproduces the plan's pinned losses. Run:
prints `problem_id: answer`.
"""

from fractions import Fraction
from itertools import product
from math import exp, isclose, log

EPS = "e"  # blank, ASCII-safe
CLASSES = ("A", "B", EPS)


def wrap(target: str) -> tuple[str, ...]:
    """AB -> (e, A, e, B, e): the blank-wrapped state sequence."""
    states: list[str] = [EPS]
    for ch in target:
        states.extend((ch, EPS))
    return tuple(states)


def collapse(path: str) -> str:
    """Merge adjacent repeats, THEN drop blanks."""
    merged = [ch for i, ch in enumerate(path) if i == 0 or path[i - 1] != ch]
    return "".join(ch for ch in merged if ch != EPS)


def skip_legal(states: tuple[str, ...], s: int) -> bool:
    """A skip lands on s from s-2: legal only onto a label differing from s-2's."""
    return s >= 2 and states[s] != EPS and states[s] != states[s - 2]


def forward(y: list[dict], states: tuple[str, ...]) -> list[list]:
    n, zero = len(states), 0 * y[0][EPS]
    alpha = [[zero] * n for _ in y]
    alpha[0][0] = y[0][states[0]]
    alpha[0][1] = y[0][states[1]]
    for t in range(1, len(y)):
        for s in range(n):
            total = alpha[t - 1][s]
            if s >= 1:
                total = total + alpha[t - 1][s - 1]
            if skip_legal(states, s):
                total = total + alpha[t - 1][s - 2]
            alpha[t][s] = total * y[t][states[s]]
    return alpha


def backward(y: list[dict], states: tuple[str, ...]) -> list[list]:
    """The 2012 convention: beta's product starts at t+1, so beta_T = 1 at
    the two accepting states — no emission is ever pocketed twice."""
    n, one, zero = len(states), 1 * y[0][EPS] ** 0, 0 * y[0][EPS]
    beta = [[zero] * n for _ in y]
    beta[-1][n - 1] = beta[-1][n - 2] = one
    for t in range(len(y) - 2, -1, -1):
        for s in range(n):
            total = beta[t + 1][s] * y[t + 1][states[s]]
            if s + 1 < n:
                total = total + beta[t + 1][s + 1] * y[t + 1][states[s + 1]]
            if s + 2 < n and skip_legal(states, s + 2):
                total = total + beta[t + 1][s + 2] * y[t + 1][states[s + 2]]
            beta[t][s] = total
    return beta


def brute_probability(y: list[dict], target: str):
    total = 0 * y[0][EPS]
    for path in product("AB" + EPS, repeat=len(y)):
        if collapse("".join(path)) == target:
            weight = y[0][path[0]] ** 0
            for t, sym in enumerate(path):
                weight = weight * y[t][sym]
            total = total + weight
    return total


def class_occupancy(y: list[dict], target: str) -> list[dict]:
    """gamma folded from states into classes: blank owns three grid rows."""
    states = wrap(target)
    alpha, beta = forward(y, states), backward(y, states)
    p = sum(alpha[-1][-2:])
    columns = []
    for t in range(len(y)):
        col = dict.fromkeys(CLASSES, 0 * p)
        for s, lab in enumerate(states):
            col[lab] = col[lab] + alpha[t][s] * beta[t][s] / p
        columns.append(col)
    return columns


MATRIX = [  # rows A/B/eps as dict, one entry per frame t = 1..4 (plan 010 K)
    {"A": Fraction(7, 10), "B": Fraction(2, 10), EPS: Fraction(1, 10)},
    {"A": Fraction(6, 10), "B": Fraction(1, 10), EPS: Fraction(3, 10)},
    {"A": Fraction(2, 10), "B": Fraction(1, 10), EPS: Fraction(7, 10)},
    {"A": Fraction(1, 10), "B": Fraction(7, 10), EPS: Fraction(2, 10)},
]
UNIT = [dict.fromkeys((*CLASSES,), Fraction(1)) for _ in range(4)]
UNIFORM = [dict.fromkeys((*CLASSES,), Fraction(1, 3)) for _ in range(4)]
STATES_AB = wrap("AB")


def p1_backward_counts() -> str:
    """Unit-weight suffix counts: t=1 reads (5, 10, 6, 4, 1); 5 + 10 = 15."""
    beta = backward(UNIT, STATES_AB)
    assert beta[2] == [0, 1, 1, 2, 1]
    assert beta[1] == [1, 4, 3, 3, 1]  # beta_2(A) = 1 + 1 + 2, the legal skip
    assert beta[0] == [5, 10, 6, 4, 1]
    assert beta[0][0] + beta[0][1] == 15  # the flagship count from the far end
    # Two independent routes: enumeration agrees (suffix counts via brute force).
    assert brute_probability(UNIT, "AB") == 15
    return "t=1 column (5, 10, 6, 4, 1); initial states 5 + 10 = 15"


def p2_constant_column() -> str:
    """alpha*beta columns each sum to 15 at unit weights, to P = 0.4877 real."""
    alpha, beta = forward(UNIT, STATES_AB), backward(UNIT, STATES_AB)
    products = [[alpha[t][s] * beta[t][s] for s in range(5)] for t in range(4)]
    assert products == [
        [5, 10, 0, 0, 0],
        [1, 8, 3, 3, 0],
        [0, 3, 3, 8, 1],
        [0, 0, 0, 10, 5],
    ]
    assert all(sum(col) == 15 for col in products)
    assert products[1][1] == 2 * 4  # the waist: prefixes x suffixes
    # The real matrix: every column prices the same exact P(AB|X).
    alpha, beta = forward(MATRIX, STATES_AB), backward(MATRIX, STATES_AB)
    p = brute_probability(MATRIX, "AB")
    assert p == Fraction(4877, 10000)
    assert round(-log(float(p)), 4) == 0.7181
    for t in range(4):
        assert sum(alpha[t][s] * beta[t][s] for s in range(5)) == p
    # The dwell times the chapter reads off the occupancy rows (anchor S).
    occ = class_occupancy(MATRIX, "AB")
    dwell = {k: sum(col[k] for col in occ) for k in CLASSES}
    assert dwell == {
        "A": Fraction(8573, 4877),
        "B": Fraction(5472, 4877),
        EPS: Fraction(5463, 4877),
    }
    assert sum(dwell.values()) == 4
    return "unit columns sum to 15; real columns each sum to 4877/10000 = 0.4877"


def p3_uniform_outputs() -> str:
    """Uniform y: P = 5/27, gamma = path counts / 15, gradient in pure fractions."""
    p = brute_probability(UNIFORM, "AB")
    assert p == Fraction(5, 27) == 15 * Fraction(1, 3) ** 4
    occ = class_occupancy(UNIFORM, "AB")
    assert occ[0] == {"A": Fraction(2, 3), "B": 0, EPS: Fraction(1, 3)}
    grad = {k: Fraction(1, 3) - occ[0][k] for k in CLASSES}
    assert grad == {"A": Fraction(-1, 3), "B": Fraction(1, 3), EPS: 0}
    return "P = 5/27; gamma_1 = (2/3, 0, 1/3); y - gamma = (-1/3, +1/3, 0)"


def p4_frame_one_gradient() -> str:
    """y - gamma at t=1: (-0.2028, +0.2000, +0.0028); B exact since occ = 0."""
    occ = class_occupancy(MATRIX, "AB")
    grad = {k: MATRIX[0][k] - occ[0][k] for k in CLASSES}
    assert {k: round(float(v), 4) for k, v in grad.items()} == {
        "A": -0.2028,
        "B": 0.2000,
        EPS: 0.0028,
    }
    assert grad["B"] == Fraction(2, 10)  # exact: the B state is unreachable at t=1
    assert sum(grad.values()) == 0
    # Wrong transcript BA: the same mechanism flips t=1 A to exactly +0.7000.
    assert brute_probability(MATRIX, "BA") == Fraction(363, 10000)
    occ_ba = class_occupancy(MATRIX, "BA")
    assert MATRIX[0]["A"] - occ_ba[0]["A"] == Fraction(7, 10)
    return "(-0.2028, +0.2000, +0.0028), sums to 0; BA flips A to +0.7000"


def p5_identity_by_finite_differences() -> str:
    """y - gamma equals the numerical gradient of -ln P at the logits."""
    u = [[log(float(MATRIX[t][k])) for k in CLASSES] for t in range(4)]

    def loss(logits: list[list[float]]) -> float:
        y = []
        for row in logits:
            top = max(row)
            exps = [exp(v - top) for v in row]
            total = sum(exps)
            y.append(dict(zip(CLASSES, [v / total for v in exps], strict=True)))
        alpha = forward(y, STATES_AB)
        return -log(alpha[-1][-1] + alpha[-1][-2])

    occ = class_occupancy(MATRIX, "AB")
    for t in range(4):
        for i, k in enumerate(CLASSES):
            bumped = [row[:] for row in u]
            dipped = [row[:] for row in u]
            bumped[t][i] += 1e-6
            dipped[t][i] -= 1e-6
            fd = (loss(bumped) - loss(dipped)) / 2e-6
            analytic = float(MATRIX[t][k] - occ[t][k])
            assert isclose(fd, analytic, rel_tol=0, abs_tol=1e-8)
    return "finite differences match y - gamma at all 12 cells"


def p6_blank_dominance() -> str:
    """Label cells over all AB-paths: (21, 21, 18) at T=4; (56, 56, 63) at T=5."""
    tallies = {}
    for t_frames in (4, 5):
        counts = dict.fromkeys(CLASSES, 0)
        paths = 0
        for path in product("AB" + EPS, repeat=t_frames):
            if collapse("".join(path)) == "AB":
                paths += 1
                for sym in path:
                    counts[sym] += 1
        tallies[t_frames] = (paths, counts)
    assert tallies[4] == (15, {"A": 21, "B": 21, EPS: 18})  # blank NOT dominant
    assert tallies[5] == (35, {"A": 56, "B": 56, EPS: 63})  # dominance starts here
    return "T=4: (21, 21, 18), labels lead; T=5: 35 paths, (56, 56, 63), blank ahead"


def _verify_training_walk() -> str:
    """Prose anchors (plan 010 anchors M/S, float64): plain GD, lr 1.0, from
    u = ln(matrix); losses 0.7181 -> 0.1602 -> 0.0356 -> 0.0003, and frame 3
    converging to the mixed (0.032, 0.218, 0.750)."""
    u = [[log(float(MATRIX[t][k])) for k in CLASSES] for t in range(4)]
    seen = {}
    for it in range(5001):
        y = []
        for row in u:
            top = max(row)
            exps = [exp(v - top) for v in row]
            total = sum(exps)
            y.append(dict(zip(CLASSES, [v / total for v in exps], strict=True)))
        alpha = forward(y, STATES_AB)
        seen[it] = -log(alpha[-1][-1] + alpha[-1][-2])
        occ = class_occupancy(y, "AB")
        for t in range(4):
            for i, k in enumerate(CLASSES):
                u[t][i] -= y[t][k] - float(occ[t][k])
    assert round(seen[0], 4) == 0.7181
    assert round(seen[10], 4) == 0.1602
    assert round(seen[50], 4) == 0.0356
    assert round(seen[5000], 4) == 0.0003
    top = max(u[2])
    exps = [exp(v - top) for v in u[2]]
    frame3 = [v / sum(exps) for v in exps]
    assert [round(v, 3) for v in frame3] == [0.032, 0.218, 0.750]
    return "loss 0.7181 -> 0.1602 -> 0.0356 -> 0.0003; frame 3 (0.032, 0.218, 0.750)"


ANSWERS = {
    "ctc-gradient.1": p1_backward_counts,
    "ctc-gradient.2": p2_constant_column,
    "ctc-gradient.3": p3_uniform_outputs,
    "ctc-gradient.4": p4_frame_one_gradient,
    "ctc-gradient.5": p5_identity_by_finite_differences,
    "ctc-gradient.6": p6_blank_dominance,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
    print(f"prose-anchors: {_verify_training_walk()}")
