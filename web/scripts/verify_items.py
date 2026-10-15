#!/usr/bin/env python3
"""Recompute every answer key in web/content/items.ts with SymPy and compare.

How to run (from the repo root, needs Python 3 and SymPy >= 1.12):

    python3 web/scripts/verify_items.py

The script reads items.ts directly (the regex parser in itembank.py, shared with
lint_items.py; no JSON export to keep in sync), looks up a SymPy computation for each item id in CHECKS below, and
prints one row per item. It exits non-zero if any item fails or if an item in
items.ts has no check here, so a new item isn't "verified" until someone adds its
computation.

What is checked per item:
  * MC: the key choice, parsed from its LaTeX, equals the SymPy result, and no
    distractor does (so exactly one choice is correct).
  * SPR: every `answers` entry equals the SymPy result exactly, and the reduced
    fraction or a full-width decimal fits Bluebook's 5 (positive) / 6 (negative)
    character limit.
  * Scaffold placeholders are checked too.

Adding an item: write a function that returns the exact answer as a SymPy object
(Rational, Integer, or an expression such as 2304*pi), register it in CHECKS
under the item id, and rerun. For an MC item whose choices aren't numbers (for
example an equation), return a callable that takes the list of choice strings
and the expected index and returns (ok, detail); see psda_regression_line.
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, pi, sqrt, sin, cos, tan, asin, log, Eq
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from itembank import ITEMS_TS, parse_items  # noqa: E402  (shared with lint_items.py)

MAX_POSITIVE_LENGTH = 5
MAX_NEGATIVE_LENGTH = 6

# ---------------------------------------------------------------------------
# Choice parsing: a small LaTeX subset ($-\frac{4}{5}$, $2304\pi$, $37.5$ ...)
# ---------------------------------------------------------------------------

_TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def latex_to_sympy(text: str):
    s = text.strip().strip("$")
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"((\1)/(\2))", s)
    s = s.replace("\\pi", "pi").replace("\\cdot", "*").replace("\\left", "").replace("\\right", "")
    s = s.replace("{", "(").replace("}", ")").replace("^", "**")
    s = s.replace(",", "")  # thousands separators
    return parse_expr(s, transformations=_TRANSFORMS, local_dict={"pi": pi})


# ---------------------------------------------------------------------------
# Per-item SymPy computations. Each returns the exact answer, or a callable
# (choices, answer_index) -> (ok, detail) for MC items with non-numeric choices.
# ---------------------------------------------------------------------------

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")


def sample_tangent_system():
    # Choices are words; count real solutions and map to the choice text.
    sols = sp.solve([Eq(y, x**2 - 6 * x + 11), Eq(y, 2 * x - 5)], [x, y], dict=True)
    count = len([sol for sol in sols if all(v.is_real for v in sol.values())])
    words = {0: "Zero", 1: "Exactly one", 2: "Exactly two"}

    def check(choices, idx):
        return choices[idx] == words[count], f"{count} real solution(s) -> '{words[count]}'"

    return check


def sample_positive_root():
    return max(sp.solve(6 * x**2 - x - 2, x))


def sample_tilde_constants():
    sol = sp.solve(sp.Poly(sp.expand((2 * x + c) * (x - 3) - (2 * x**2 + b * x - 15)), x).all_coeffs(), [b, c])
    return sol[b]


def alg_no_solution_k():
    # Parallel: determinant of the coefficient matrix is 0; then confirm no solution.
    kk = sp.solve(sp.Matrix([[5, -k], [15, 12]]).det(), k)[0]
    assert sp.linsolve([5 * x - kk * y - 8, 15 * x + 12 * y - 2], [x, y]) == sp.S.EmptySet
    return kk


def alg_identity_sum():
    poly = sp.Poly(sp.expand(4 * ((a * x + 12) / 4 - (3 * x / 2 + b))), x)
    sol = sp.solve(poly.all_coeffs(), [a, b])
    return sol[a] + sol[b]


def alg_print_shop_rate():
    sol = sp.solve([Eq(40 * a + b, 23), Eq(110 * a + b, 44)], [a, b])
    return sol[a] * 75 + sol[b]


def alg_inequality_integer_a():
    cond = sp.And(5 > 3 * a - 7, 5 <= -a + 9)
    ints = [i for i in range(-20, 21) if bool(cond.subs(a, i))]
    return Integer(max(ints))


def alg_perpendicular_x_intercept():
    m1 = sp.solve(Eq(4 * x - 6 * y, 5), y)[0].coeff(x)
    m2 = -1 / m1
    line = Eq(y - 7, m2 * (x + 3))
    return sp.solve(line.subs(y, 0), x)[0]


def alg_no_solution_one_var():
    lhs, rhs = sp.expand(k * (x - 4) + 3 * x), 7 * x - 10
    kk = sp.solve(Eq(lhs.coeff(x), rhs.coeff(x)), k)[0]
    assert sp.solve(Eq(lhs.subs(k, kk), rhs), x) == []  # genuinely no solution
    return kk


def alg_decimal_system_difference():
    sol = sp.solve([Eq(Rational(3, 10) * x + Rational(1, 2) * y, Rational(51, 10)), Eq(2 * x - 3 * y, -4)], [x, y])
    return sol[x] - sol[y]


def adv_rational_remainder():
    q, rem = sp.div(6 * x**2 + 7 * x - 13, 2 * x + 5, x)
    assert sp.expand(q) == 3 * x - 4
    return rem


def adv_symmetric_square():
    sols = sp.solve([Eq(x**2 + y**2, 50), Eq(x * y, 7)], [x, y])
    vals = {sp.simplify((sx - sy) ** 2) for sx, sy in sols}
    assert len(vals) == 1
    return vals.pop()


def adv_tangent_k():
    disc = sp.discriminant(x**2 - 2 * k * x + 5 * k, x)
    return max(v for v in sp.solve(disc, k) if v > 0)


def adv_parabola_line_y_product():
    sols = sp.solve([Eq(y, x**2 - 3 * x - 4), Eq(y, 2 * x + 10)], [x, y])
    assert len(sols) == 2
    return sp.prod(sy for _, sy in sols)


def adv_exponential_two_points():
    sol = [sol for sol in sp.solve([Eq(a * b, 12), Eq(a * b**3, 48)], [a, b], dict=True) if sol[b] > 0][0]
    return sol[a] * sol[b] ** 0


def adv_vertex_evaluate():
    f = 2 * x**2 + b * x + c
    sol = sp.solve([Eq(sp.diff(f, x).subs(x, 3), 0), Eq(f.subs(x, 3), -5)], [b, c])
    return f.subs(sol).subs(x, -1)


def adv_exponent_k():
    # Compare exponents: (3/4)k - 1/2 = 5/2.
    kk = sp.solve(Eq(Rational(3, 4) * k - Rational(1, 2), Rational(5, 2)), k)[0]
    assert sp.simplify((x ** Rational(3, 4)) ** kk * x ** Rational(-1, 2) - x ** Rational(5, 2)) == 0
    return kk


def psda_mean_equals_median():
    data = [5, 9, 12, 16, 17, 20]
    xx = sp.solve(Eq(sp.Rational(sum(data)) / 7 + x / 7, 16), x)[0]
    full = sorted(data + [xx])
    assert xx > 16 and full[3] == 16 and sp.Rational(sum(full), 7) == full[3]
    return xx


def psda_percent_return():
    return sp.solve(Eq(Rational(13, 10) * (1 - p / 100), Rational(91, 100)), p)[0]


def psda_conditional_table():
    return Rational(72, 54 + 72)


def psda_regression_line():
    xs = [1, 2, 3, 4, 5]
    ys = [Rational(4), Rational(13, 2), Rational(7), Rational(19, 2), Rational(11)]
    xbar, ybar = Rational(sum(xs), 5), sum(ys) / 5
    m = sum((xi - xbar) * (yi - ybar) for xi, yi in zip(xs, ys)) / sum((xi - xbar) ** 2 for xi in xs)
    bb = ybar - m * xbar
    expected = m * x + bb

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = latex_to_sympy(ch.split("=")[1])
            if sp.simplify(sp.nsimplify(rhs) - expected) == 0:
                matches.append(i)
        return matches == [idx], f"least squares y = {m}x + {bb}; matching choices {matches}"

    return check


def psda_growth_year():
    nn = sp.ceiling(log(Rational(4000, 2400)) / log(Rational(106, 100)))
    assert 2400 * Rational(106, 100) ** (nn - 1) <= 4000 < 2400 * Rational(106, 100) ** nn
    return Integer(2015) + nn


def geo_circle_point_k():
    sols = sp.solve(Eq(5**2 + y**2 - 10 * 5 + 6 * y + 18, 0), y)
    return max(sols)


def geo_tan_complement():
    A = asin(Rational(5, 13))
    return sp.nsimplify(sp.simplify(tan(pi / 2 - A)))


def geo_inscribed_square():
    return sp.solve(Eq(s / 9 + s / 12, 1), s)[0]


def geo_sin_cos_degrees():
    expr = sin(x * pi / 180) - cos((2 * x + 15) * pi / 180)
    sols = sorted({sp.nsimplify(v) for v in sp.solve(expr, x) if v.is_real and 0 < v < 90})
    # Also confirm numerically that there is exactly one root in (0, 90).
    roots = {round(float(sp.nsolve(expr, x, g)), 6) for g in range(5, 90, 10) if 0 < sp.nsolve(expr, x, g) < 90}
    assert len(roots) == 1, roots
    return sols[0] if sols else sp.nsimplify(roots.pop())


def geo_cylinder_sphere():
    rr = sp.solve(Eq(pi * r**2 * 5, 720 * pi), r)
    rr = [v for v in rr if v > 0][0]
    return Rational(4, 3) * pi * rr**3


# ---------------------------------------------------------------------------
# Batch 2 checks
# ---------------------------------------------------------------------------

j_, k_, m_, bb_, cc_ = symbols("j k m b c")


def _split_equation(text: str):
    """'$lhs = rhs$' -> (lhs, rhs) as SymPy expressions."""
    lhs, rhs = text.strip().strip("$").split("=")
    return latex_to_sympy(lhs), latex_to_sympy(rhs)


def alg_which_equation_no_solution():
    given = Eq(6 * x - 9 * y, 14)

    def check(choices, idx):
        none = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            if sp.linsolve([given.lhs - given.rhs, lhs - rhs], [x, y]) == sp.S.EmptySet:
                none.append(i)
        return none == [idx], f"choices giving no solution: {none}"

    return check


def alg_point_on_every_line_r():
    expr = sp.expand((r + 2) * x + (1 - 3 * r) * y - (6 * r + 5))
    sol = sp.solve(sp.Poly(expr, r).all_coeffs(), [x, y])
    # Confirm the point works for a few r values.
    for rv in (-3, 0, 1, Rational(7, 2)):
        assert expr.subs({x: sol[x], y: sol[y], r: rv}) == 0
    return sol[x] - sol[y]


def alg_sum_difference_trick():
    sol = sp.solve([Eq(7 * j_ + 2 * k_, 61), Eq(4 * j_ + 5 * k_, 37)], [j_, k_])
    return 7 * (sol[j_] - sol[k_])


def alg_interpret_intercept():
    E = 14 * n + 65
    at_open, slope, after14 = E.subs(n, 0), sp.diff(E, n), E.subs(n, 14)

    def check(choices, idx):
        # The key must describe the value at n = 0; every distractor must claim a number the model contradicts.
        key_ok = "when it opened" in choices[idx] and at_open == 65
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("each week" in ch and slope != 65)
            or ("first week" in ch and slope != 65)
            or ("14 weeks" in ch and after14 != 65))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"E(0)={at_open}, slope={slope}, E(14)={after14}; contradicted distractors {wrong}"

    return check


def adv_discriminant_max_ac():
    best = 0
    for av in range(1, 101):
        for cv in range(1, 101):
            if sp.discriminant(av * x**2 + 18 * x + cv, x) > 0:
                best = max(best, av * cv)
    return Integer(best)


def adv_vieta_sum_to_product():
    poly = 3 * x**2 - (k + 5) * x + 2 * k
    roots = sp.solve(poly, x)
    kk = sp.solve(Eq(sp.simplify(sum(roots)), 6), k)[0]
    assert sp.discriminant(poly.subs(k, kk), x) > 0
    return sp.simplify(sp.prod(roots).subs(k, kk))


def adv_vieta_other_root():
    cc = sp.solve(Eq((4 * x**2 - 11 * x + c).subs(x, 3), 0), c)[0]
    roots = sp.solve(4 * x**2 - 11 * x + cc, x)
    assert 3 in roots
    return [rt for rt in roots if rt != 3][0]


def adv_shift_from_table():
    pts = {-1: 8, 0: 3, 2: 5, 3: 12}
    f = a * x**2 + b * x + c
    sol = sp.solve([Eq(f.subs(x, xv), yv) for xv, yv in list(pts.items())[:3]], [a, b, c])
    f = f.subs(sol)
    assert f.subs(x, 3) == pts[3], "fourth table point must fit the same quadratic"
    g = f.subs(x, x + 4)
    return g.subs(x, 0)


def adv_composite_from_table():
    F = {1: 3, 2: 1, 3: 4, 4: 2}
    G = {1: 2, 2: 4, 3: 1, 4: 3}
    h = lambda v: Rational(2 * F[v] + 1, G[v] - 1)
    return h(4) - h(2)


def adv_absolute_one_solution_k():
    xr = Symbol("x", real=True)
    f = -2 * sp.Abs(xr - 5) + 9
    ones = [kv for kv in range(-30, 31) if len(sp.solve(Eq(f, kv), xr)) == 1]
    assert len(ones) == 1
    return Integer(ones[0])


def adv_absolute_no_solution_c():
    xr = Symbol("x", real=True)
    f = sp.Abs(4 * xr - 1) + c
    samples = [Rational(v, 2) for v in range(-8, 12)]
    no_solution = {cv for cv in samples if sp.solve(Eq(f.subs(c, cv), 2), xr) == []}

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            text = ch.strip("$")
            op = "<" if "<" in text else ">"
            lhs, rhs = (latex_to_sympy(t) for t in text.split(op))
            holds = {cv for cv in samples if bool((lhs < rhs if op == "<" else lhs > rhs).subs(c, cv))}
            if holds == no_solution:
                matches.append(i)
        return matches == [idx], f"no-solution set on samples matches choices {matches}"

    return check


def adv_exponential_form_displays_value():
    f = 3 * 2**x
    target = f.subs(x, 2)
    test_xs = [0, 1, 2, Rational(5, 2), 7, -3]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = latex_to_sympy(ch.split("=")[1])
            equivalent = all(sp.simplify(rhs.subs(x, xv) - f.subs(x, xv)) == 0 for xv in test_xs)
            coeff = rhs.as_coeff_Mul()[0]
            if equivalent and coeff == target:
                matches.append(i)
        return matches == [idx], f"f(2)={target}; equivalent forms with that coefficient: {matches}"

    return check


def adv_decay_rate_interpretation():
    M = 820 * Rational(94, 100) ** (t / 3)
    three_day = sp.simplify(M.subs(t, 3) / M.subs(t, 0))
    one_day = sp.simplify(M.subs(t, 1) / M.subs(t, 0))

    def check(choices, idx):
        pct3 = (1 - three_day) * 100
        key_ok = "6%" in choices[idx] and "every 3 days" in choices[idx] and pct3 == 6
        # Daily factor is 0.94^(1/3): not a 2% drop and not a 6% drop.
        daily_ok = one_day != Rational(98, 100) and one_day != Rational(94, 100)
        return key_ok and daily_ok, f"3-day factor {three_day} ({pct3}% drop); 1-day factor {float(one_day):.4f}"

    return check


def adv_factor_theorem_constant():
    def check(choices, idx):
        zero = []
        for i, ch in enumerate(choices):
            pexpr = latex_to_sympy(ch)
            val = sp.simplify(pexpr.subs(x, 3 * bb_))
            if val == 0:
                zero.append(i)
            else:
                assert val.subs(bb_, 2) != 0  # nonzero for a positive b
        return zero == [idx], f"p(3b) = 0 for choices {zero}"

    return check


def adv_sqrt_extraneous_root():
    sols = sp.solve(Eq(sqrt(2 * x + 11), x - 2), x)
    assert len(sols) == 1
    return sols[0]


def psda_mixing_saline():
    sol = sp.solve([Eq(x + y, 350), Eq(Rational(12, 100) * x + Rational(40, 100) * y, Rational(28, 100) * 350)], [x, y])
    return sol[y]


def psda_weighted_mean_new_members():
    total_after = 30 * Rational(161, 10)
    total_before = 24 * Rational(155, 10)
    return (total_after - total_before) / 6


def psda_sd_frequency_smallest():
    freqs = {"W": [4, 4, 4, 4, 4], "X": [10, 0, 0, 0, 10], "Y": [0, 5, 10, 5, 0], "Z": [2, 4, 8, 4, 2]}

    def sd(fr):
        data = [v for v, f in zip(range(1, 6), fr) for _ in range(f)]
        assert len(data) == 20
        mean = Rational(sum(data), len(data))
        return sqrt(sum((d - mean) ** 2 for d in data) / len(data))

    sds = {name: sd(fr) for name, fr in freqs.items()}
    smallest = min(sds, key=lambda nm: sds[nm])

    def check(choices, idx):
        return choices[idx] == f"Data set {smallest}", f"SDs {{{', '.join(f'{nm}: {float(v):.3f}' for nm, v in sds.items())}}} -> {smallest}"

    return check


def psda_margin_of_error_sample_size():
    n1, n2 = 120, 1080
    moe1, moe2 = Rational(5, 10), Rational(17, 100)

    def check(choices, idx):
        ratio_ok = n2 > n1 and abs(float(moe1 / sqrt(Rational(n2, n1)) - moe2)) < 0.01
        key_ok = "larger" in choices[idx]
        others = [i for i, ch in enumerate(choices) if "larger" in ch]
        return ratio_ok and key_ok and others == [idx], f"n2/n1 = {n2 // n1}; 0.5/sqrt(9) = {float(moe1/3):.3f} ~ {moe2}"

    return check


def psda_ratio_chained_split():
    indoor = 420 * Rational(3, 7)
    return indoor * Rational(4, 9)


def psda_unit_conversion_squared():
    return Rational(24, 10) * 60**2 / 1000


def psda_density_block_height():
    volume = Rational(2700) / Rational(75, 10)
    return volume / (8 * 6)


def geo_coterminal_radians():
    theta = Rational(83, 6) * pi
    while theta >= 2 * pi:
        theta -= 2 * pi
    assert 0 <= theta < 2 * pi
    return theta


def geo_similar_perimeter_to_area():
    return 24 * Rational(5, 2) ** 2


def geo_inscribed_angle_arc_x():
    return sp.solve(Eq(2 * x + 7, (6 * x - 10) / 2), x)[0]


def geo_parallel_proof_equation():
    a1, a2 = 3 * x + 10, 2 * x - 5
    condition = a1 + a2 - 180  # same-side interior angles supplementary

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            ratio = sp.simplify((lhs - rhs) / condition)
            if ratio.is_number and ratio != 0:
                matches.append(i)
        return matches == [idx], f"choices equivalent to {condition} = 0: {matches}"

    return check


def geo_polygon_angle_sum_n():
    hexagon = 180 * (6 - 2)
    return sp.solve(Eq(180 * (n - 2), 6 * hexagon), n)[0]


def geo_congruence_sufficiency():
    # Known: side AB and angle B. Each case adds one fact; decide with SSS/SAS/ASA/AAS.
    def sufficient(sides: set[frozenset], angles: set[str]) -> bool:
        if len(sides) == 3:
            return True
        if len(sides) == 2 and len(angles) >= 1:
            s1, s2 = sides
            included = s1 & s2
            return any(v in included for v in angles)  # SAS; SSA is not enough
        if len(angles) >= 2 and len(sides) >= 1:
            return True  # ASA or AAS
        return False

    base_sides, base_angles = {frozenset("AB")}, {"B"}
    cases = {
        "I": ({frozenset("BC")}, set()),
        "II": ({frozenset("AC")}, set()),
        "III": (set(), {"C"}),
    }
    good = [nm for nm, (sd, an) in cases.items() if sufficient(base_sides | sd, base_angles | an)]
    expected = {"I only": ["I"], "I and III only": ["I", "III"], "II and III only": ["II", "III"], "I, II, and III": ["I", "II", "III"]}

    def check(choices, idx):
        return expected.get(choices[idx]) == good, f"sufficient cases {good}"

    return check


CHECKS = {
    "sample-tangent-system": sample_tangent_system,
    "sample-positive-root": sample_positive_root,
    "sample-tilde-constants": sample_tilde_constants,
    "alg-no-solution-k": alg_no_solution_k,
    "alg-identity-sum": alg_identity_sum,
    "alg-print-shop-rate": alg_print_shop_rate,
    "alg-inequality-integer-a": alg_inequality_integer_a,
    "alg-perpendicular-x-intercept": alg_perpendicular_x_intercept,
    "alg-no-solution-one-var": alg_no_solution_one_var,
    "alg-decimal-system-difference": alg_decimal_system_difference,
    "adv-rational-remainder": adv_rational_remainder,
    "adv-symmetric-square": adv_symmetric_square,
    "adv-tangent-k": adv_tangent_k,
    "adv-parabola-line-y-product": adv_parabola_line_y_product,
    "adv-exponential-two-points": adv_exponential_two_points,
    "adv-vertex-evaluate": adv_vertex_evaluate,
    "adv-exponent-k": adv_exponent_k,
    "psda-mean-equals-median": psda_mean_equals_median,
    "psda-percent-return": psda_percent_return,
    "psda-conditional-table": psda_conditional_table,
    "psda-regression-line": psda_regression_line,
    "psda-growth-year": psda_growth_year,
    "geo-circle-point-k": geo_circle_point_k,
    "geo-tan-complement": geo_tan_complement,
    "geo-inscribed-square": geo_inscribed_square,
    "geo-sin-cos-degrees": geo_sin_cos_degrees,
    "geo-cylinder-sphere": geo_cylinder_sphere,
    # Batch 2
    "alg-which-equation-no-solution": alg_which_equation_no_solution,
    "alg-point-on-every-line-r": alg_point_on_every_line_r,
    "alg-sum-difference-trick": alg_sum_difference_trick,
    "alg-interpret-intercept": alg_interpret_intercept,
    "adv-discriminant-max-ac": adv_discriminant_max_ac,
    "adv-vieta-sum-to-product": adv_vieta_sum_to_product,
    "adv-vieta-other-root": adv_vieta_other_root,
    "adv-shift-from-table": adv_shift_from_table,
    "adv-composite-from-table": adv_composite_from_table,
    "adv-absolute-one-solution-k": adv_absolute_one_solution_k,
    "adv-absolute-no-solution-c": adv_absolute_no_solution_c,
    "adv-exponential-form-displays-value": adv_exponential_form_displays_value,
    "adv-decay-rate-interpretation": adv_decay_rate_interpretation,
    "adv-factor-theorem-constant": adv_factor_theorem_constant,
    "adv-sqrt-extraneous-root": adv_sqrt_extraneous_root,
    "psda-mixing-saline": psda_mixing_saline,
    "psda-weighted-mean-new-members": psda_weighted_mean_new_members,
    "psda-sd-frequency-smallest": psda_sd_frequency_smallest,
    "psda-margin-of-error-sample-size": psda_margin_of_error_sample_size,
    "psda-ratio-chained-split": psda_ratio_chained_split,
    "psda-unit-conversion-squared": psda_unit_conversion_squared,
    "psda-density-block-height": psda_density_block_height,
    "geo-coterminal-radians": geo_coterminal_radians,
    "geo-similar-perimeter-to-area": geo_similar_perimeter_to_area,
    "geo-inscribed-angle-arc-x": geo_inscribed_angle_arc_x,
    "geo-parallel-proof-equation": geo_parallel_proof_equation,
    "geo-polygon-angle-sum-n": geo_polygon_angle_sum_n,
    "geo-congruence-sufficiency": geo_congruence_sufficiency,
}


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def spr_fits_bluebook(value: Fraction) -> bool:
    """True if the reduced fraction, or a full-width decimal, fits the entry box."""
    limit = MAX_NEGATIVE_LENGTH if value < 0 else MAX_POSITIVE_LENGTH
    frac = f"{value.numerator}" if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if len(frac) <= limit:
        return True
    # A decimal needs the integer part plus at least one decimal digit to fit.
    whole = str(abs(value.numerator) // value.denominator)
    sign = 1 if value < 0 else 0
    return sign + len(whole) + 2 <= limit


def check_item(item: dict, compute) -> tuple[bool, str]:
    result = compute()
    if callable(result):
        return result(item["choices"], item["answerIndex"])

    expected = sp.nsimplify(result)
    if item["format"] == "mc":
        matches = []
        for i, ch in enumerate(item["choices"]):
            try:
                val = latex_to_sympy(ch)
            except Exception as e:  # noqa: BLE001
                return False, f"could not parse choice {i} {ch!r}: {e}"
            if sp.simplify(val - expected) == 0:
                matches.append(i)
        ok = matches == [item["answerIndex"]]
        return ok, f"expected {expected}; matching choices {matches}, key index {item['answerIndex']}"

    # SPR
    if not expected.is_Rational:
        return False, f"SPR key must be rational, got {expected}"
    exp_frac = Fraction(int(expected.p), int(expected.q))
    for ans in item["answers"]:
        if ans != exp_frac:
            return False, f"expected {exp_frac}, items.ts has {ans}"
        if not spr_fits_bluebook(ans):
            return False, f"{ans} does not fit the 5/6-character entry box"
    return True, f"expected {exp_frac}; {len(item['answers'])} key(s) match and fit"


def main() -> int:
    items = parse_items(ITEMS_TS.read_text(encoding="utf-8"))
    failures = 0
    print(f"{'id':34} {'dom':14} {'fmt':4} {'diff':6} {'route':15} status  detail")
    for item in items:
        compute = CHECKS.get(item["id"])
        if compute is None:
            ok, detail = False, "no SymPy check registered in verify_items.py"
        else:
            try:
                ok, detail = check_item(item, compute)
            except Exception as e:  # noqa: BLE001
                ok, detail = False, f"check raised {type(e).__name__}: {e}"
        failures += 0 if ok else 1
        print(f"{item['id']:34} {item['domain']:14} {item['format']:4} {item['difficulty']:6} {item['route']:15} "
              f"{'PASS' if ok else 'FAIL':6}  {detail}")

    unknown = sorted(set(CHECKS) - {i["id"] for i in items})
    if unknown:
        print(f"\nnote: checks with no matching item in items.ts: {unknown}")

    # Summary counts
    def tally(key):
        out: dict[str, int] = {}
        for it in items:
            out[it[key]] = out.get(it[key], 0) + 1
        return dict(sorted(out.items()))

    print(f"\n{len(items)} items; {failures} failing")
    print("by domain:    ", tally("domain"))
    print("by format:    ", tally("format"))
    print("by difficulty:", tally("difficulty"))
    print("by route:     ", tally("route"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
