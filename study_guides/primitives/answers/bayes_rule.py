"""Answer anchors for the bayes-rule problem set (plan 012 R3).

Exact Fractions; every posterior is computed by at least two independent
routes (whole-person counts vs the odds form, full conditioning vs
likelihood-ratio multiplication, enumeration over protocols) and the
routes must agree — the same two-route discipline plan 004's verifier
used. Run: prints `problem_id: answer`.
"""

from fractions import Fraction


def diseasitis_counts() -> tuple[int, int]:
    """The cohort: 100 students, 20 sick (90% test positive), 80 healthy
    (30% test positive) — 18 and 24 positives."""
    sick_pos = 20 * 9 // 10
    healthy_pos = 80 * 3 // 10
    assert (sick_pos, healthy_pos) == (18, 24)
    return sick_pos, healthy_pos


def p1_diseasitis_by_counts() -> Fraction:
    """The share of positives who are sick — no formula needed."""
    sick_pos, healthy_pos = diseasitis_counts()
    posterior = Fraction(sick_pos, sick_pos + healthy_pos)
    assert posterior == Fraction(18, 42) == Fraction(3, 7)
    return posterior


def p2_diseasitis_by_odds() -> str:
    """Prior odds 1:4 times LR 3 = posterior odds 3:4 — same 3/7."""
    prior_odds = Fraction(20, 80)
    lr = Fraction(9, 10) / Fraction(3, 10)
    post_odds = prior_odds * lr
    assert prior_odds == Fraction(1, 4) and lr == 3
    assert post_odds == Fraction(3, 4)
    posterior = post_odds / (1 + post_odds)
    assert posterior == p1_diseasitis_by_counts() == Fraction(3, 7)
    return "1:4 x 3 = 3:4 -> 3/7 (agrees with the counts)"


def p3_one_test_two_patients() -> str:
    """LR 9 against two priors: 1:9 -> 1:1 -> 1/2; 1:99 -> 1:11 -> 1/12."""
    lr = Fraction(9, 10) / Fraction(1, 10)
    assert lr == 9
    results = []
    for prior_odds, counts in ((Fraction(1, 9), (9, 9)), (Fraction(1, 99), (9, 99))):
        post_odds = prior_odds * lr
        posterior = post_odds / (1 + post_odds)
        # the conditional chapter's whole-person counts, recovered exactly
        sick_pos, healthy_pos = counts
        assert posterior == Fraction(sick_pos, sick_pos + healthy_pos)
        results.append(posterior)
    assert results == [Fraction(1, 2), Fraction(1, 12)]
    return "1:1 -> 1/2 at 10% prevalence; 1:11 -> 1/12 at 1%"


def p4_iterated_coins() -> str:
    """Two coins (9/10 vs 1/10 heads), LR 9 per head: full conditioning
    agrees with multiplying likelihood ratios; H-then-T cancels to 1:1."""
    heads = {"good": Fraction(9, 10), "bad": Fraction(1, 10)}

    def posterior_good(seq: str) -> Fraction:
        weight = {}
        for coin, p in heads.items():
            w = Fraction(1, 2)
            for f in seq:
                w *= p if f == "H" else 1 - p
            weight[coin] = w
        return weight["good"] / (weight["good"] + weight["bad"])

    def by_odds(seq: str) -> Fraction:
        odds = Fraction(1)
        for f in seq:
            odds *= Fraction(9) if f == "H" else Fraction(1, 9)
        return odds / (1 + odds)

    for seq, expected_odds, expected_post in (
        ("H", Fraction(9), Fraction(9, 10)),
        ("HH", Fraction(81), Fraction(81, 82)),
        ("HT", Fraction(1), Fraction(1, 2)),
    ):
        assert posterior_good(seq) == by_odds(seq) == expected_post
        odds = posterior_good(seq) / (1 - posterior_good(seq))
        assert odds == expected_odds
    return "H: 9:1 (9/10); HH: 81:1 (81/82); HT: back to 1:1 (1/2)"


def p5_montys_protocols() -> str:
    """Same door opened, three protocols, three answers (Rosenthal).

    Contestant picks door 1; car uniform; condition on the host opening
    door 3 and revealing a goat; report P(switch wins) = P(car = 2 | that).
    """

    def posterior_switch(host_openings) -> Fraction:
        # host_openings(car) -> list of (door, prob) the host might open
        weight = {}
        for car in (1, 2, 3):
            for door, p in host_openings(car):
                if door == 3 and door != car:  # opened door 3, goat shown
                    weight[car] = weight.get(car, Fraction(0)) + Fraction(1, 3) * p
        return weight.get(2, Fraction(0)) / sum(weight.values())

    def standard(car):  # never the car, never door 1; coin-flip when free
        doors = [d for d in (2, 3) if d != car]
        return [(d, Fraction(1, len(doors))) for d in doors]

    def fall(car):  # slips: door 2 or 3 uniformly, may reveal the car
        return [(2, Fraction(1, 2)), (3, Fraction(1, 2))]

    def crawl(car):  # opens the lowest goat door available
        return [(min(d for d in (2, 3) if d != car), Fraction(1))]

    results = (posterior_switch(standard), posterior_switch(fall), posterior_switch(crawl))
    assert results == (Fraction(2, 3), Fraction(1, 2), Fraction(1))
    return "standard: 2/3; Monty Fall: 1/2; Monty Crawl (forced high): 1"


ANSWERS = {
    "bayes-rule.1": p1_diseasitis_by_counts,
    "bayes-rule.2": p2_diseasitis_by_odds,
    "bayes-rule.3": p3_one_test_two_patients,
    "bayes-rule.4": p4_iterated_coins,
    "bayes-rule.5": p5_montys_protocols,
}

if __name__ == "__main__":
    for key, fn in ANSWERS.items():
        print(f"{key}: {fn()}")
