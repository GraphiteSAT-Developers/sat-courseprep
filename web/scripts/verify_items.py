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


# ----- Batch batch3-geo -----
import sympy as sp
from sympy import Integer, Rational, pi, sqrt, sin, cos, tan, atan, asin, acos, Eq, symbols


x, y, s, w, c, theta, h = symbols("x y s w c theta h")


def _nearest(value, places: int):
    """Round an exact SymPy number to `places` decimals, asserting it is not a rounding tie."""
    scaled = value * 10**places
    assert abs(scaled - sp.floor(scaled) - Rational(1, 2)) > Rational(1, 100), "rounding tie"
    return Rational(int(sp.floor(scaled + Rational(1, 2))), 10**places)


# ----- Area and volume -----------------------------------------------------


def geo_prism_to_cube_edge():
    volume = 4 * 6 * 9
    edge = [v for v in sp.solve(Eq(s**3, volume), s) if v.is_real][0]
    return edge


def geo_rectangle_perimeter_to_area():
    sol = sp.solve([Eq(2 * w + 2 * (3 * w), 56)], [w])
    width = sol[w]
    return width * (3 * width)


def geo_scale_model_floor_area():
    k = Rational(25)  # warehouse length / model length
    return 18 * k**2


def geo_cylinder_tank_radius_decimal():
    r = [v for v in sp.solve(Eq(pi * s**2 * 8, 2000), s) if v > 0][0]
    assert abs(float(r) - 8.92) < 0.01
    return _nearest(r, 1)


def geo_prism_cubic_volume_s():
    sols = [v for v in sp.solve(Eq(s**2 * (s + 3), 200), s) if v.is_real and v > 0]
    assert len(sols) == 1
    return sols[0]


def geo_cone_cut_volume_ratio():
    k = Rational(4, 12)  # scale factor small cone : whole cone
    small = k**3
    rest = 1 - small
    return small / rest


# ----- Lines, angles, and triangles ----------------------------------------


def geo_parallel_obtuse_angle():
    acute = Integer(54)  # corresponding angles are congruent; obtuse is the supplement
    return 180 - acute


def geo_exterior_angle_x():
    A, B, ext = 2 * x, 3 * x - 12, 6 * x - 20
    xx = sp.solve(Eq(ext, A + B), x)[0]
    assert A.subs(x, xx) > 0 and B.subs(x, xx) > 0 and 0 < ext.subs(x, xx) < 180
    assert A.subs(x, xx) + B.subs(x, xx) + (180 - ext.subs(x, xx)) == 180
    return xx


def geo_similar_triangle_perimeter():
    k = Rational(6, 9)
    return k * (9 + 12 + 15)


def geo_triangle_between_parallels():
    angle_B = 180 - 38 - 64  # triangle angle sum
    # Alternate interior angles across transversal BC: angle ABC equals the angle between CB and line m.
    acute = angle_B if angle_B < 90 else 180 - angle_B
    return Integer(acute)


def geo_parallel_segment_trapezoid_area():
    k = Rational(6 + 4, 6)  # PQ / PS
    whole = 27 * k**2
    return whole - 27


# ----- Right triangles and trigonometry ------------------------------------


def geo_degrees_to_radians_150():
    return 150 * pi / 180


def geo_pole_wire_tangent_height():
    height = 15 * tan(40 * pi / 180)
    assert abs(float(height) - 12.586) < 0.001
    return _nearest(sp.nsimplify(round(float(height), 6)), 1)


def geo_ramp_angle_arctan():
    angle = atan(Rational(7, 24)) * 180 / pi
    assert abs(float(angle) - 16.26) < 0.01
    # Distractor sanity: arcsin and arccos of the same ratio round elsewhere.
    assert round(float(asin(Rational(7, 24)) * 180 / pi)) == 17
    assert round(float(acos(Rational(7, 24)) * 180 / pi)) == 73
    return Integer(round(float(angle)))


def geo_isosceles_right_area():
    leg = 10 * sin(pi / 4)
    return sp.simplify(Rational(1, 2) * leg * leg)


def geo_altitude_angle_sine():
    # C at the origin, A on the y-axis (AC = 6), B on the x-axis (BC = 8); D is the foot from C on AB.
    A, B, C = sp.Point(0, 6), sp.Point(8, 0), sp.Point(0, 0)
    D = sp.Line(A, B).projection(C)
    angle = sp.Segment(C, A).angle_between(sp.Segment(C, D))
    return sp.nsimplify(sp.simplify(sin(angle)))


def geo_quadrant_four_cosine():
    th = 2 * pi + asin(-Rational(5, 13))  # the angle in (3π/2, 2π) with that sine
    assert 3 * pi / 2 < th < 2 * pi
    return sp.simplify(cos(th))


# ----- Circles -------------------------------------------------------------


def geo_arc_length_100_degrees():
    return 2 * pi * 9 * Rational(100, 360)


def geo_circle_chord_on_line():
    pts = sp.solve([Eq(x**2 + y**2 - 2 * x + 4 * y - 20, 0), Eq(y, 2)], [x, y])
    assert len(pts) == 2
    (x1, y1), (x2, y2) = pts
    return sp.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def geo_sector_angle_garden():
    return sp.solve(Eq(theta / 360 * pi * 12**2, 30 * pi), theta)[0]


def geo_circle_radius_constant_c():
    # Complete the square: (x-3)^2 + (y+5)^2 = 34 - c; radius 7 means 34 - c = 49.
    expr = x**2 + y**2 - 6 * x + 10 * y + c
    cx, cy = Rational(6, 2), -Rational(10, 2)
    r2 = sp.expand(-(expr.subs({x: cx, y: cy})))  # 34 - c
    return sp.solve(Eq(r2, 49), c)[0]


def geo_circle_tangent_vertical_line():
    center, line_x = sp.Point(2, -3), 7

    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            lhs, rhs = (latex_to_sympy(t) for t in ch.strip("$").split("="))
            expr = sp.expand(lhs - rhs)
            poly = sp.Poly(expr, x, y)
            d, e, f = poly.coeff_monomial(x), poly.coeff_monomial(y), poly.coeff_monomial(1)
            h0, k0 = -d / 2, -e / 2
            r = sp.sqrt(h0**2 + k0**2 - f)
            if sp.Point(h0, k0) == center and r == abs(line_x - h0):
                good.append(i)
        return good == [idx], f"choices centered at (2, -3) and tangent to x = 7: {good}"

    return check


# ----- Batch batch3-algebra -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch3-algebra.ts (batch 3-algebra).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch3_algebra.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""


import re

import sympy as sp
from sympy import Eq, Integer, Rational, symbols


x, y, m, n, t, a, b, c, k, h = symbols("x y m n t a b c k h")


def _point(text: str):
    """'$(1, -2)$' -> (1, -2) as SymPy numbers."""
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip())


def _relational(text: str, var):
    """'$35n + 80 \\le 900$' -> SymPy relational in var."""
    s = text.strip().strip("$")
    for tok, rel in (("\\le", sp.Le), ("\\ge", sp.Ge), ("<", sp.Lt), (">", sp.Gt)):
        if tok in s:
            lhs, rhs = s.split(tok)
            return rel(latex_to_sympy(lhs), latex_to_sympy(rhs))
    raise ValueError(f"no inequality sign in {text!r}")


# ----- Linear equations in one variable -----


def alg_ride_fare_equation():
    miles = (Rational("19.70") - Rational("3.50")) / Rational("1.80")  # from the stem's givens

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            sol = sp.solve(Eq(lhs, rhs), m)
            if sol and sp.nsimplify(sol[0]) == miles:
                matches.append(i)
        return matches == [idx], f"m = {miles}; choices solved by it {matches}"

    return check


def alg_fraction_equation_solve():
    sols = sp.solve(Eq((2 * x - 5) / 3, (x + 4) / 2 - 1), x)
    assert len(sols) == 1
    return sols[0]


def alg_plumber_hours():
    return sp.solve(Eq(65 + 48 * h, 245), h)[0]


def alg_count_solutions_identity():
    diff = sp.expand(5 * (x - 2) - 3 * x - (2 * (x + 4) - 18))
    if diff == 0:
        word = "Infinitely many"
    elif diff.is_number:
        word = "Zero"
    else:
        word = "Exactly one"

    def check(choices, idx):
        return choices[idx] == word, f"lhs - rhs simplifies to {diff} -> '{word}'"

    return check


def alg_structure_x_plus_3():
    xx = sp.solve(Eq((2 * x + 6) / 5, 9), x)[0]
    return xx + 3


def alg_infinitely_many_c():
    poly = sp.Poly(sp.expand(c * (x + 2) - 4 - (6 * x + 8)), x)
    sols = sp.solve(poly.all_coeffs(), [c], dict=True)
    assert len(sols) == 1  # both coefficient conditions agree
    return sols[0][c]


# ----- Linear functions -----


def alg_evaluate_linear_f4():
    return (7 * x - 11).subs(x, 4)


def alg_drain_rate_interpretation():
    w = 420 - 15 * t
    slope, start, empty_at = sp.diff(w, t), w.subs(t, 0), sp.solve(Eq(w, 0), t)[0]

    def check(choices, idx):
        key_ok = "each minute" in choices[idx] and "decreases" in choices[idx] and slope == -15
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("when it starts" in ch and start != 15)
            or ("is empty" in ch and empty_at != 15)
            or ("every 15 minutes" in ch and 420 / Integer(15) != 15))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"slope={slope}, w(0)={start}, empty at t={empty_at}; contradicted distractors {wrong}"

    return check


def _line_through(points):
    (x1, y1), (x2, y2) = points[:2]
    slope = Rational(y2 - y1, x2 - x1)
    intercept = y1 - slope * x1
    for px, py in points[2:]:
        assert slope * px + intercept == py, "extra point must lie on the same line"
    return slope * x + intercept


def alg_table_to_rule_g():
    expected = _line_through([(2, 11), (5, 2), (9, -10)])

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if sp.expand(latex_to_sympy(ch.split("=")[1]) - expected) == 0]
        return matches == [idx], f"g(x) = {expected}; matching choices {matches}"

    return check


def alg_bird_count_model():
    f = _line_through([(2012, 860), (2020, 620)])
    return f.subs(x, 2029)


def alg_rule_from_point_and_rate():
    bb = sp.solve(Eq(4 * 3 + b, 10), b)[0]
    return (4 * x + bb).subs(x, -2)


def alg_linear_shift_rule():
    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            f = latex_to_sympy(ch.split("=")[1])
            shift_ok = sp.expand(f.subs(x, x + 3) - f - 12) == 0
            if shift_ok and f.subs(x, 2) == 1:
                matches.append(i)
        return matches == [idx], f"choices with f(x+3) - f(x) = 12 and f(2) = 1: {matches}"

    return check


def alg_rate_find_input():
    slope = Rational(6, 4)
    bb = sp.solve(Eq(slope * 10 + b, 20), b)[0]
    return sp.solve(Eq(slope * x + bb, 2), x)[0]


def alg_candle_height_time():
    f = _line_through([(12, Rational("22.6")), (40, Rational("15.6"))])
    return sp.solve(Eq(f, 10), x)[0]


# ----- Linear equations in two variables -----


def alg_slope_two_points():
    return Rational(-1 - 7, 6 - 2)


def alg_line_point_slope_equation():
    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = latex_to_sympy(ch.split("=")[1])
            if sp.diff(rhs, x) == -2 and rhs.subs(x, 6) == 1:
                matches.append(i)
        return matches == [idx], f"choices with slope -2 through (6, 1): {matches}"

    return check


def alg_snack_stand_pretzels():
    p, q = symbols("p q")
    return sp.solve(Eq(3 * p + 2 * q, 96).subs(q, 12), p)[0]


def alg_table_line_find_x():
    f = _line_through([(-3, 14), (1, 2), (6, -13)])
    return sp.solve(Eq(f, 50), x)[0]


def alg_line_constant_x_intercept():
    aa = sp.solve(Eq(a * (-6) + 4 * 2, 20), a)[0]
    return sp.solve(Eq(aa * x + 4 * 0, 20), x)[0]


def alg_budget_x_intercept_meaning():
    x_int = sp.solve(Eq(45 * x + 120 * 0, 900), x)[0]
    y_int = sp.solve(Eq(45 * 0 + 120 * y, 900), y)[0]
    ratio, pair_cost = Rational(120, 45), 45 + 120

    def check(choices, idx):
        key_ok = "chairs" in choices[idx] and "no desks" in choices[idx] and x_int == 20
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("no chairs" in ch and y_int != x_int)
            or ("for each desk" in ch and ratio != x_int)
            or ("cost" in ch and pair_cost != x_int))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"x-intercept {x_int}, y-intercept {y_int}, ratio {ratio}, pair cost {pair_cost}; contradicted {wrong}"

    return check


# ----- Systems of two linear equations in two variables -----


def alg_system_substitution_y():
    sol = sp.solve([Eq(y, 2 * x - 3), Eq(x + y, 9)], [x, y])
    return sol[y]


def alg_theater_child_tickets():
    sol = sp.solve([Eq(a + c, 380), Eq(12 * a + 7 * c, 3785)], [a, c])
    return sol[c]


def alg_system_product_xy():
    sol = sp.solve([Eq(x, 2 * y + 1), Eq(3 * x + 4 * y, 33)], [x, y])
    return sol[x] * sol[y]


def alg_infinite_solutions_c():
    # Infinitely many solutions: the second equation times a scalar equals the first.
    factor = Rational(6, -9)
    assert factor * 15 == -10
    cc = factor * 12
    assert sp.linsolve([6 * x - 10 * y - cc, -9 * x + 15 * y - 12], [x, y]) != sp.S.EmptySet
    assert sp.Matrix([[6, -10], [-9, 15]]).det() == 0
    return cc


def alg_system_k_on_line():
    sol = sp.solve([Eq(3 * x - 2 * y, 7), Eq(y, 2 * x)], [x, y])
    return (5 * x + 4 * y).subs(sol)


def alg_tanks_equal_volume():
    tt = sp.solve(Eq(300 + 12 * t, 540 - 8 * t), t)[0]
    return (300 + 12 * t).subs(t, tt)


# ----- Linear inequalities in one or two variables -----


def alg_point_satisfies_inequality():
    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if bool(sp.Gt(_point(ch)[1], 2 * _point(ch)[0] - 5))]
        return good == [idx], f"points satisfying y > 2x - 5: {good}"

    return check


def alg_elevator_crates_inequality():
    expected = sp.solve_univariate_inequality(sp.Le(80 + 35 * n, 900), n, relational=False)

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            got = sp.solve_univariate_inequality(_relational(ch, n), n, relational=False)
            if got == expected:
                matches.append(i)
        return matches == [idx], f"solution set {expected}; matching choices {matches}"

    return check


def alg_greatest_integer_inequality():
    sol = sp.solve_univariate_inequality(sp.Gt(7 - 2 * x, 3 * x - 8), x, relational=False)
    assert sol.right_open and sol.right == 3
    return sp.floor(sol.right) - 1  # strict, so the greatest integer is one below the endpoint


def alg_inequality_solution_set_c():
    # 3x + c > 5x - 9  <=>  x < (c + 9)/2; that bound must be 4.
    bound = sp.solve(sp.Gt(3 * x + c, 5 * x - 9), x)  # unused symbolic form guard
    cc = sp.solve(Eq((c + 9) / 2, 4), c)[0]
    sol = sp.solve_univariate_inequality(sp.Gt(3 * x + cc, 5 * x - 9), x, relational=False)
    assert sol == sp.Interval.open(-sp.oo, 4), (bound, sol)
    return cc


def alg_system_inequalities_point():
    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            px, py = _point(ch)
            if bool(sp.Ge(py, Rational(1, 2) * px - 3)) and bool(sp.Lt(2 * px + py, 6)):
                good.append(i)
        return good == [idx], f"points in the solution set: {good}"

    return check


def alg_count_integers_two_inequalities():
    s1 = sp.solve_univariate_inequality(sp.Gt(2 * x + 5, -9), x, relational=False)
    s2 = sp.solve_univariate_inequality(sp.Ge(4 - x, -3), x, relational=False)
    both = s1.intersect(s2)
    return Integer(len([i for i in range(-50, 51) if both.contains(i)]))


# ----- Batch batch3-psda -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch3-psda.ts (batch 3-psda).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch3_psda.py --only-extra

Each function derives the answer from the stem's givens, following the
conventions of verify_items.py: a numeric result for numeric keys, or a
callable (choices, answer_index) -> (ok, detail) for word-choice items, which
compute the underlying quantity and then match the choice text.
"""






x, m, n = symbols("x m n")


# ---------------------------------------------------------------------------
# Ratios, rates, proportional relationships, and units
# ---------------------------------------------------------------------------


def psda_scale_drawing_path():
    meters_per_cm = Rational(5, 2)
    return Rational(72, 10) * meters_per_cm


def psda_kilowatt_hours_heater():
    hours_per_day = Rational(25, 60)
    return Rational(3, 2) * hours_per_day * 12


def psda_density_neighbor_county():
    area1 = Rational(156000, 240)
    return 2 * area1 * 150


def psda_cyclist_speed_mps():
    meters = 27 * 1000
    seconds = (60 + 15) * 60
    return Rational(meters, seconds)


# ---------------------------------------------------------------------------
# Percentages
# ---------------------------------------------------------------------------


def psda_jacket_sale_price():
    return Rational(80) * (1 - Rational(35, 100))


def psda_percent_of_percent_music_art():
    both = Rational(45, 100) * Rational(60, 100)
    return both * 100


def psda_tax_tip_original_cost():
    total = Rational(6480, 100)
    return sp.solve(sp.Eq(m * Rational(108, 100) * Rational(120, 100), total), m)[0]


# ---------------------------------------------------------------------------
# One-variable data
# ---------------------------------------------------------------------------


def _median(values):
    vals = sorted(values)
    k = len(vals)
    return Rational(vals[k // 2]) if k % 2 else Rational(vals[k // 2 - 1] + vals[k // 2], 2)


def _mean(values):
    return Rational(sum(values), len(values))


def _sd(values, population=True):
    mu = _mean(values)
    denom = len(values) if population else len(values) - 1
    return sqrt(sum((v - mu) ** 2 for v in values) / denom)


def psda_books_frequency_mean():
    freq = {0: 4, 1: 6, 2: 3, 4: 2}
    data = [v for v, f in freq.items() for _ in range(f)]
    assert len(data) == 15
    return _mean(data)


def psda_remove_max_mean_median():
    before = [12, 15, 15, 18, 18, 20, 22, 70]
    after = [v for v in before if v != 70]
    assert len(after) == 7
    mean_word = "decreases" if _mean(after) < _mean(before) else ("remains the same" if _mean(after) == _mean(before) else "increases")
    med_word = "decreases" if _median(after) < _median(before) else ("remains the same" if _median(after) == _median(before) else "increases")
    expected = f"The mean {mean_word}, and the median {med_word}."

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if ch.strip() == expected]
        return matches == [idx], (f"mean {_mean(before)} -> {_mean(after)}, median {_median(before)} -> {_median(after)}; "
                                  f"matching choices {matches}")

    return check


def psda_combined_shifted_sets_sd():
    # Any A with mean 36 and SD 5 gives the same mean of C and var(C) = var(A) + 16 (population).
    A = [31] * 6 + [41] * 6
    assert _mean(A) == 36 and _sd(A) == 5
    B = [v - 8 for v in A]
    C = A + B
    mean_c = _mean(C)
    sd_pop, sd_samp = _sd(C), _sd(C, population=False)
    assert (sd_pop > 5) == (sd_samp > 5)
    word = "greater" if sd_pop > 5 else "less"

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if f"is {mean_c}," in ch and f"{word} than 5" in ch]
        return matches == [idx], f"mean(C) = {mean_c}, SD(C) = {float(sd_pop):.3f} (sample {float(sd_samp):.3f}); matching choices {matches}"

    return check


# ---------------------------------------------------------------------------
# Two-variable data
# ---------------------------------------------------------------------------


def psda_model_predict_customers():
    return (Rational(35, 10) * x + 12).subs(x, 8)


def psda_residual_from_model():
    predicted = (Rational(45, 10) * x + 2).subs(x, 6)
    return Integer(31) - predicted


def psda_cells_exponential_model():
    pts = [(0, 64), (1, 80), (2, 100), (3, 125)]

    def check(choices, idx):
        ssr = []
        for ch in choices:
            rhs = latex_to_sympy(ch.split("=")[1])
            ssr.append(sum((sp.nsimplify(rhs.subs(x, xv)) - yv) ** 2 for xv, yv in pts))
        exact = [i for i, v in enumerate(ssr) if sp.simplify(v) == 0]
        return exact == [idx], f"sum of squared residuals per choice {[float(v) for v in ssr]}; exact fits {exact}"

    return check


def psda_best_fit_predict_eight():
    xs = [1, 2, 3, 4, 5]
    ys = [Rational(32, 10), Rational(51, 10), Rational(66, 10), Rational(89, 10), Rational(107, 10)]
    xbar, ybar = Rational(sum(xs), 5), sum(ys) / 5
    slope = sum((xi - xbar) * (yi - ybar) for xi, yi in zip(xs, ys)) / sum((xi - xbar) ** 2 for xi in xs)
    intercept = ybar - slope * xbar
    return slope * 8 + intercept


# ---------------------------------------------------------------------------
# Probability and conditional probability
# ---------------------------------------------------------------------------


def psda_parking_lot_van():
    vans = 40 - 14 - 18
    return Rational(vans, 40)


def psda_club_members_given_probability():
    junior_share = 1 - Rational(5, 8)
    return sp.solve(sp.Eq(junior_share * n, 24), n)[0]


def psda_commuters_transit_conditional():
    transit = 200 - 120
    transit_long = 95 - 45
    return Rational(transit - transit_long, transit)


# ---------------------------------------------------------------------------
# Inference from sample statistics and margin of error
# ---------------------------------------------------------------------------


def psda_moe_streaming_interpretation():
    est, moe = Rational(26, 10), Rational(3, 10)
    lo, hi = est - moe, est + moe

    def check(choices, idx):
        interval = f"between {float(lo):g} and {float(hi):g}"
        matches = [i for i, ch in enumerate(choices)
                   if "mean" in ch and "all households in the city" in ch and interval in ch]
        return matches == [idx], f"interval {float(lo):g} to {float(hi):g}; choices stating the city mean lies plausibly in it: {matches}"

    return check


def psda_sample_proportion_employees():
    use_share = Rational(24, 60)
    return 1500 * (1 - use_share)


# ---------------------------------------------------------------------------
# Evaluating statistical claims
# ---------------------------------------------------------------------------


def _study_check(random_assignment: bool, random_selection: bool, population: str):
    """Map the two design flags to the (causal, generalizable-to) claims each choice makes."""
    causal_word = "likely caused" if random_assignment else "may not have caused"
    generalize = f"can be generalized to {population}" if random_selection else "cannot be generalized beyond"

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if causal_word in ch and generalize in ch]
        return matches == [idx], (f"random assignment={random_assignment} -> '{causal_word}'; "
                                  f"random selection={random_selection} -> '{generalize}'; matching choices {matches}")

    return check


def psda_fitness_stretching_experiment():
    return _study_check(random_assignment=True, random_selection=True, population="all members of the fitness center")


def psda_lavender_volunteers_generalize():
    return _study_check(random_assignment=True, random_selection=False, population="")


def psda_sampling_method_walk():
    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if "at random" in ch and "all students" in ch]
        return good == [idx], f"choices that are random and drawn from the whole population: {good}"

    return check


# ----- Batch batch3-advmath -----
#!/usr/bin/env python3
"""SymPy checks for batch 3-advmath (web/content/batches/batch3-advmath.ts).

Run from the repo root, against a temp items.ts that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch3_advmath.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""


import re

import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, sqrt, Eq


x, y, a, b, c, k, d, t = symbols("x y a b c k d t")


def latex_to_sympy_ext(text: str):
    """latex_to_sympy plus \\sqrt{..}, \\sqrt[n]{..} and \\% handling."""
    s = text.strip().strip("$").replace("\\%", "")
    # Innermost-first: rewrite \frac and \sqrt groups without nested braces until none remain.
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\[(\d+)\]\{([^{}]*)\}", r"((\2)**(1/\1))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    return latex_to_sympy(s)


def _rhs(choice: str):
    return latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1])


# ---------------------------------------------------------------- Equivalent expressions


def adv_poly_subtract_fluency():
    return sp.expand((3 * x**2 - 5 * x + 4) - (x**2 + 2 * x - 9))


def adv_difference_of_squares_factor():
    return 49 * x**2 - 36 * y**2


def adv_rational_combine_constants():
    num = sp.expand(5 * (x - 1) - 3 * (x + 2))
    sol = sp.solve(sp.Poly(num - (a * x + b), x).all_coeffs(), [a, b])
    assert sp.simplify(5 / (x + 2) - 3 / (x - 1) - (sol[a] * x + sol[b]) / ((x + 2) * (x - 1))) == 0
    return sol[a] + sol[b]


def adv_rational_exponent_simplify():
    xp = Symbol("x", positive=True)
    expr = sp.simplify(xp ** Rational(3, 4) * sqrt(xp) / xp ** Rational(1, 4))
    assert expr == xp
    return x  # same expression in the shared symbol


def adv_polynomial_product_constant_c():
    lhs = sp.expand((x**2 + k * x - 4) * (3 * x - 2))
    rhs = 3 * x**3 + 7 * x**2 + c * x + 8
    sol = sp.solve(sp.Poly(lhs - rhs, x).all_coeffs(), [c, k])
    return sol[c]


def adv_complete_square_equivalent():
    return x**2 - 10 * x + 7


def adv_rational_simplify_factor_cancel():
    return sp.cancel((x**2 - 9) / (x**2 + 5 * x + 6))


def adv_rational_structure_difference():
    return sp.cancel((4 * x**2 - 12 * x + 9) / (2 * x - 3) - (x**2 - 16) / (x + 4))


def adv_trinomial_factor_positive_ab():
    diff = sp.expand((a * x + 5) * (b * x - 4) - (6 * x**2 + 7 * x - 20))
    sols = sp.solve(sp.Poly(diff, x).all_coeffs(), [a, b], dict=True)
    assert len(sols) == 2  # the second pair is negative and excluded by the stem
    pos = [s for s in sols if s[a] > 0 and s[b] > 0]
    assert len(pos) == 1
    return pos[0][a] + pos[0][b]


def adv_exponential_rewrite_base():
    expected = 8 * 4**x
    for xv in (-2, 0, 1, Rational(3, 2), 5):
        assert sp.simplify((8**x / 2 ** (x - 3) - expected).subs(x, xv)) == 0
    return expected


# ------------------------------------------- Nonlinear equations and systems


def adv_absolute_value_positive_solution():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(sp.Abs(2 * xr - 7), 11), xr)
    assert len(sols) == 2
    return max(sols)


def adv_rational_equation_cross_multiply():
    sols = sp.solve(Eq(3 / (x - 2), 5 / (x + 4)), x)
    assert len(sols) == 1
    return sols[0]


def adv_garden_quadratic_perimeter():
    w = Symbol("w")
    ws = [v for v in sp.solve(Eq(w * (w + 4), 12), w) if v > 0]
    assert len(ws) == 1
    return 2 * (ws[0] + ws[0] + 4)


def adv_factored_cubic_sum_solutions():
    roots = sp.solve((x - 3) * (x + 5) * (2 * x - 1), x)
    assert len(roots) == 3
    return sum(roots)


def adv_two_solutions_k_condition():
    samples = [Rational(v, 2) for v in range(-20, 80)]
    two_real = {kv for kv in samples if sp.discriminant((2 * x**2 - 8 * x + k).subs(k, kv), x) > 0}

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            text = ch.strip("$")
            op = "<" if "<" in text else ">"
            lhs, rhs = (latex_to_sympy(s) for s in text.split(op))
            holds = {kv for kv in samples if bool((lhs < rhs if op == "<" else lhs > rhs).subs(k, kv))}
            if holds == two_real:
                matches.append(i)
        return matches == [idx], f"two-real-solution set on samples matches choices {matches}"

    return check


def adv_rational_equation_extraneous():
    cands = sp.solve(sp.together(x / (x - 3) + 2 / x - 3 / (x - 3)).as_numer_denom()[0], x)
    valid = [v for v in cands if v != 0 and v != 3]
    assert 3 in cands and valid == [-2]
    return valid[0]


def adv_quadratic_formula_radicand():
    roots = sp.solve(2 * x**2 - 8 * x + 3, x)
    big = max(roots, key=lambda r: float(r))
    kk = sp.simplify((2 * (big - 2)) ** 2)
    assert sp.simplify(min(roots, key=lambda r: float(r)) - (2 - sqrt(kk) / 2)) == 0
    return kk


def adv_parabola_line_tangent_c():
    disc = sp.discriminant((x**2 + 6 * x + c) - (2 * x + 3), x)
    sols = sp.solve(disc, c)
    assert len(sols) == 1
    return sols[0]


def adv_exponential_equation_common_base():
    xx = sp.solve(Eq(2 * (2 * x + 1), 3 * (x - 2)), x)[0]
    assert sp.simplify(4 ** (2 * xx + 1) - 8 ** (xx - 2)) == 0
    return xx


def adv_falling_object_solve_for_t():
    dp = Symbol("d", positive=True)
    expected = sqrt(dp / Rational(49, 10))

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = _rhs(ch).subs(d, dp)
            if all(abs(float((rhs - expected).subs(dp, dv))) < 1e-9 for dv in (Rational(49, 10), Rational(196, 10), 100)):
                matches.append(i)
        return matches == [idx], f"t = sqrt(d/4.9); matching choices {matches}"

    return check


def adv_absolute_value_sum_of_solutions():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(sp.Abs(3 * xr - 4), 2 * xr + 1), xr)
    assert len(sols) == 2
    return sum(sols)


# ---------------------------------------------------------- Nonlinear functions


def adv_exponential_model_evaluate_leaves():
    return (3 * 2**t + 1).subs(t, 3)


def adv_exponential_initial_value_club():
    N = 640 * Rational(108, 100) ** t
    n0, n1 = N.subs(t, 0), N.subs(t, 1)

    def check(choices, idx):
        key_ok = "when it was founded" in choices[idx] and n0 == 640
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("1 year after" in ch and n1 != 640)
            or ("first year" in ch and n1 - n0 != 640)
            or ("each year" in ch and sp.diff(N, t).free_symbols))]  # not a constant rate
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"N(0)={n0}, N(1)={n1}, N(1)-N(0)={n1 - n0}; contradicted distractors {wrong}"

    return check


def adv_vertex_form_displays_minimum():
    f = x**2 + 8 * x + 3
    xv = sp.solve(sp.diff(f, x), x)[0]
    fmin = f.subs(x, xv)

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = _rhs(ch)
            equivalent = sp.expand(rhs - f) == 0
            const = rhs.as_independent(x)[0]
            if equivalent and const == fmin:
                matches.append(i)
        return matches == [idx], f"minimum {fmin} at x={xv}; equivalent forms displaying it: {matches}"

    return check


def adv_algae_decay_every_two_days():
    target = 80 * Rational(64, 100) ** (x / 2)

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = _rhs(ch)
            if all(abs(float((rhs - target).subs(x, xv))) < 1e-9 for xv in (0, 1, 2, 3, 7)):
                matches.append(i)
        return matches == [idx], f"A = 80(0.64)^(x/2); matching choices {matches}"

    return check


def adv_quadratic_regression_shift_vertex():
    pts = {1: 2, 2: 7, 4: 29}
    f = a * x**2 + b * x + c
    sol = sp.solve([Eq(f.subs(x, xv), yv) for xv, yv in pts.items()], [a, b, c])
    g = f.subs(sol).subs(x, x - 2)
    return sp.solve(sp.diff(g, x), x)[0]


def adv_ball_vertex_form_interpret_max():
    h = -5 * (t - 3) ** 2 + 50
    tmax = sp.solve(sp.diff(h, t), t)[0]
    hmax, h0 = h.subs(t, tmax), h.subs(t, 0)

    def check(choices, idx):
        key_ok = "maximum height of the ball is 50" in choices[idx] and hmax == 50
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("launched from a height" in ch and h0 != 50)
            or ("50 seconds" in ch and tmax != 50)
            or ("each second" in ch and sp.diff(h, t).free_symbols))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"max {hmax} at t={tmax}, h(0)={h0}; contradicted distractors {wrong}"

    return check


def adv_factored_quadratic_y_intercept_a():
    f = a * (x - 3) * (x + 5)
    av = sp.solve(Eq(f.subs(x, 0), 45), a)[0]
    return f.subs(a, av).subs(x, -1)


def adv_parabola_symmetry_other_intercept():
    f = a * (x - 2) ** 2 - 9
    av = sp.solve(Eq(f.subs(x, 5), 0), a)[0]
    zeros = sp.solve(f.subs(a, av), x)
    assert 5 in zeros and len(zeros) == 2
    return [z for z in zeros if z != 5][0]


def adv_exponential_translation_y_intercept():
    g = 2 ** (x - 3) - 4
    return g.subs(x, 0)


def adv_shop_profit_max_price():
    P = -4 * x**2 + 96 * x - 200
    xv = sp.solve(sp.diff(P, x), x)[0]
    assert sp.diff(P, x, 2) < 0
    return xv


def adv_exponential_quarterly_annual_percent():
    factor = Rational(104, 100) ** 4
    pct = round(float((factor - 1) * 100))

    def check(choices, idx):
        vals = [int(latex_to_sympy_ext(ch)) for ch in choices]
        matches = [i for i, v in enumerate(vals) if v == pct]
        return matches == [idx], f"yearly factor {float(factor):.6f} -> {pct}%; matching choices {matches}"

    return check


# ----- Batch batch4-advmath -----
#!/usr/bin/env python3
"""SymPy checks for batch 4-advmath (web/content/batches/batch4-advmath.ts).

Run from the repo root, against a temp items.ts that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch4_advmath.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""


import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, sqrt, Eq


x, y, a, b, c, k, p, t, h = symbols("x y a b c k p t h")


def _b4_rhs(choice: str):
    """Right-hand side of an equation choice such as '$M(h) = 500(0.5)^{h/6}$'."""
    return latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1])


def _b4_expr_check(expected, samples, parse=latex_to_sympy_ext, label=""):
    """MC with expression choices: exactly the key equals `expected` at every sample point.

    samples: list of dicts {Symbol: value}. Comparing numerically at several points avoids
    simplification differences between radical, rational and exponential forms.
    """

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            try:
                expr = parse(ch)
            except Exception as e:  # noqa: BLE001
                return False, f"could not parse choice {i} {ch!r}: {e}"
            if all(abs(complex((expr - expected).subs(s).evalf())) < 1e-9 for s in samples):
                matches.append(i)
        return matches == [idx], f"{label or expected}; matching choices {matches}, key index {idx}"

    return check


_B4_X_SAMPLES = [{x: v} for v in (Rational(1, 3), Rational(3, 2), 3, 5, 7, 11)]
_B4_XY_SAMPLES = [{x: xv, y: yv} for xv, yv in ((1, 2), (3, Rational(-1, 2)), (Rational(2, 5), 4), (-3, 7))]


# ---------------------------------------------------------------- Equivalent expressions


def adv_common_factor_xy():
    return _b4_expr_check(12 * x**3 * y - 18 * x**2 * y**2, _B4_XY_SAMPLES, label="12x^3y - 18x^2y^2")


def adv_cube_root_power():
    xp = Symbol("x", positive=True)
    assert sp.simplify((27 * xp**6) ** Rational(1, 3) - 3 * xp**2) == 0
    return _b4_expr_check(3 * x**2, _B4_X_SAMPLES, label="(27x^6)^(1/3) = 3x^2 for x > 0")


def adv_complex_fraction_difference_squares():
    expr = sp.cancel((1 - 4 / x**2) / (1 + 2 / x))
    assert sp.simplify(expr - (x - 2) / x) == 0
    return _b4_expr_check(expr, _B4_X_SAMPLES, label=f"simplifies to {expr}")


def adv_tilde_square_minus_product_b():
    lhs = sp.expand((3 * x - 2) ** 2 - (x + 5) * (x - 1))
    sol = sp.solve(sp.Poly(lhs - (a * x**2 + b * x + c), x).all_coeffs(), [a, b, c])
    return sol[b]


def adv_rational_subtract_difference_squares():
    expr = sp.cancel(2 / (x**2 - 4) - 1 / (x - 2))
    assert sp.simplify(expr - (-x) / (x**2 - 4)) == 0
    return _b4_expr_check(expr, _B4_X_SAMPLES, label=f"simplifies to {expr}")


def adv_remainder_theorem_k():
    pk = x**3 + k * x**2 - 5 * x + 6
    kk = sp.solve(Eq(pk.subs(x, -2), 12), k)[0]
    _, rem = sp.div(pk.subs(k, kk), x + 2, x)
    assert rem == 12
    return kk


def adv_rational_divide_simplify():
    expr = sp.cancel((x**2 - 16) / (x**2 - 2 * x - 8) / ((x + 4) / (x - 1)))
    assert sp.simplify(expr - (x - 1) / (x + 2)) == 0
    return _b4_expr_check(expr, _B4_X_SAMPLES, label=f"simplifies to {expr}")


# ------------------------------------------- Nonlinear equations and systems


def adv_quadratic_negative_solution():
    sols = sp.solve(x**2 + 3 * x - 28, x)
    neg = [v for v in sols if v < 0]
    assert len(sols) == 2 and len(neg) == 1
    return neg[0]


def adv_radical_equation_coefficient():
    sols = sp.solve(Eq(2 * sqrt(x + 1), 6), x)
    assert sols == [8]
    return sols[0]


def adv_circle_line_positive_x():
    sols = sp.solve([Eq(x**2 + y**2, 20), Eq(y, 2 * x)], [x, y])
    pos = [sx for sx, _ in sols if sx > 0]
    assert len(sols) == 2 and len(pos) == 1
    return pos[0]


def adv_circle_tangent_line_c():
    disc = sp.discriminant((x**2 + (x + 4) ** 2 - c), x)
    sols = sp.solve(disc, c)
    assert len(sols) == 1 and sols[0] > 0
    # Cross-check: squared distance from the origin to the line y = x + 4.
    assert sols[0] == Rational(16, 2)
    return sols[0]


def adv_two_parabolas_x_difference():
    sols = sp.solve(Eq(x**2 - 4 * x + 1, -(x**2) + 2 * x + 9), x)
    assert len(sols) == 2
    return max(sols) - min(sols)


def adv_absolute_value_midpoint_c():
    xr, cr = symbols("x c", real=True)
    s1 = set(sp.solve(Eq(sp.Abs(2 * 1 - cr), 6), cr))
    s7 = set(sp.solve(Eq(sp.Abs(2 * 7 - cr), 6), cr))
    cvals = s1 & s7
    assert s1 == {-4, 8} and s7 == {8, 20} and cvals == {8}
    cv = cvals.pop()
    assert set(sp.solve(Eq(sp.Abs(2 * xr - cv), 6), xr)) == {1, 7}
    return cv


def adv_radical_constant_extraneous_sum():
    cv = sp.solve(Eq(sqrt(3 * 8 + c), 8 - 1), c)[0]
    assert cv == 25
    sols = sp.solve(Eq(sqrt(3 * x + cv), x - 1), x)  # sympy discards the extraneous root
    squared = sp.solve(Eq(3 * x + cv, (x - 1) ** 2), x)
    assert sols == [8] and set(squared) == {8, -3}
    return sum(sols)


def adv_one_solution_leading_k():
    sols = sp.solve(sp.discriminant(k * x**2 + 12 * x + 9, x), k)
    assert sols == [4]
    assert len(sp.solve((k * x**2 + 12 * x + 9).subs(k, sols[0]), x)) == 1
    return sols[0]


def adv_kinetic_energy_solve_v():
    # The parser reads a bare E as Euler's number, so the energy symbol is renamed W before parsing (Q is sympy.Q).
    W, m, v = symbols("W m v", positive=True)
    expected = sp.solve(Eq(W, Rational(1, 2) * m * v**2), v)
    assert len(expected) == 1
    target = expected[0].subs({W: Symbol("W"), m: Symbol("m")})
    samples = [{Symbol("W"): ev, Symbol("m"): mv} for ev, mv in ((9, 2), (Rational(1, 2), 1), (50, 4), (7, 3))]
    return _b4_expr_check(target, samples, parse=lambda ch: _b4_rhs(ch.replace("E", "W")), label="v = sqrt(2E/m)")


def adv_circle_line_no_solution():
    sols = sp.solve([Eq(x**2 + y**2, 9), Eq(y, x + 5)], [x, y], dict=True)
    count = len([s for s in sols if all(v.is_real for v in s.values())])
    words = {0: "Zero", 1: "Exactly one", 2: "Exactly two"}

    def check(choices, idx):
        return choices[idx] == words[count], f"{count} real solution(s) -> '{words[count]}'"

    return check


def adv_quadratic_in_disguise_sum():
    sols = sp.solve((x - 4) ** 2 - 3 * (x - 4) - 10, x)
    assert set(sols) == {2, 9}
    return sum(sols)


def adv_rational_equation_sum_solutions():
    num = sp.together(6 / x + x / (x + 1) - 2).as_numer_denom()[0]
    sols = sp.solve(num, x)
    valid = [v for v in sols if v != 0 and v != -1]
    assert len(valid) == 2
    return sp.simplify(sum(valid))


# ---------------------------------------------------------- Nonlinear functions


def adv_cubic_evaluate_negative():
    return (3 * x**3 - x**2 + 4).subs(x, -2)


def adv_van_decay_factor_interpretation():
    factor = Rational(85, 100)
    pct_decrease = (1 - factor) * 100  # 15
    V = 38000 * factor**t

    def check(choices, idx):
        key_ok = f"decreases by {pct_decrease}%" in choices[idx] and pct_decrease == 15
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("decreases by 85%" in ch and (1 - factor) * 100 != 85)
            or ("increases" in ch and factor >= 1)  # factor < 1 means decay, so this is false
            or ("85 dollars" in ch and sp.simplify(V.subs(t, 1) - V.subs(t, 0) + 85) != 0))]
        # 'increases' is a contradicted distractor exactly when factor < 1
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("decreases by 85%" in ch) or ("increases" in ch and factor < 1) or ("85 dollars" in ch))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"factor {factor} -> {pct_decrease}% decrease per year; contradicted distractors {wrong}"

    return check


def adv_medication_half_life_model():
    target = 500 * Rational(1, 2) ** (h / 6)
    samples = [{h: v} for v in (0, 1, 6, 12, 15)]
    assert target.subs(h, 6) == 250 and target.subs(h, 12) == 125
    return _b4_expr_check(target, samples, parse=_b4_rhs, label="M(h) = 500(0.5)^(h/6)")


def adv_arch_symmetry_distance():
    hx = -Rational(5, 100) * x**2 + 3 * x
    sols = sp.solve(Eq(hx, hx.subs(x, 10)), x)
    big = [v for v in sols if v > 10]
    assert set(sols) == {10, 50} and len(big) == 1
    return big[0]


def adv_factored_form_displays_intercepts():
    f = 3 * (x - 2) ** 2 - 27
    zeros = set(sp.solve(f, x))

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rhs = _b4_rhs(ch)
            equivalent = sp.expand(rhs - f) == 0
            shown = set()
            if rhs.is_Mul:
                for arg in rhs.args:
                    if arg.is_polynomial(x) and sp.Poly(arg, x).degree() == 1:
                        shown |= set(sp.solve(arg, x))
            if equivalent and shown == zeros:
                matches.append(i)
        return matches == [idx], f"zeros {zeros}; equivalent factored forms showing them: {matches}"

    return check


def adv_table_shift_minimum_value():
    f = a * x**2 + b * x + c
    sol = sp.solve([Eq(f.subs(x, 0), 5), Eq(f.subs(x, 1), 0), Eq(f.subs(x, 2), -3)], [a, b, c])
    g = f.subs(sol).subs(x, x - 2) + 3
    xv = sp.solve(sp.diff(g, x), x)[0]
    assert sp.diff(g, x, 2) > 0
    return g.subs(x, xv)


def adv_composition_positive_a():
    f = 2 * x + a
    g = x**2
    sols = sp.solve(Eq(g.subs(x, f.subs(x, 1)), 49), a)
    pos = [v for v in sols if v > 0]
    assert len(sols) == 2 and len(pos) == 1
    return pos[0]


def adv_insect_colony_doubling_time():
    sols = sp.solve(Eq(900 * 2 ** (t / 5), 7200), t)
    vals = {sp.nsimplify(sp.simplify(v)) for v in sols}
    assert vals == {15}
    return Integer(15)


def adv_fountain_stream_zero():
    zeros = sp.solve(-Rational(1, 2) * x**2 + 6 * x, x)
    pos = [v for v in zeros if v > 0]
    assert len(pos) == 1
    return pos[0]


def adv_vehicles_percent_per_year():
    r = sp.sqrt(Rational(144, 100))
    pct = (r - 1) * 100
    assert pct == 20

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        matches = [i for i, v in enumerate(vals) if sp.simplify(v - pct) == 0]
        return matches == [idx], f"yearly factor {r} -> {pct}%; matching choices {matches}"

    return check


def adv_horizontal_compression_intercepts():
    f = (x - 6) * (x + 2)
    g = f.subs(x, 2 * x)
    zeros = sp.solve(g, x)
    assert set(zeros) == {-1, 3}
    return sum(zeros)


def adv_cubic_y_intercept_a():
    f = (x - a) * (x**2 + 4)
    sols = sp.solve(Eq(f.subs(x, 0), -12), a)
    assert len(sols) == 1
    return sols[0]


def adv_barrel_percent_decrease():
    pr = Symbol("p", real=True)
    sols = sp.solve(Eq(250 * (1 - pr / 100) ** 3, 54), pr)
    real = [v for v in sols if v.is_real]
    assert real == [40]
    return real[0]


# ----- Batch batch4-algebra -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch4-algebra.ts (batch 4-algebra).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch4_algebra.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""


import sympy as sp
from sympy import Eq, Integer, Rational, symbols


x, y, a, b, c, k, m, s, p, q, h, w, t = symbols("x y a b c k m s p q h w t")


def _b4_rel(text: str):
    """'$3s + 5m \\le 400$' -> SymPy relational; a chain '$-2 < q - 3p < 4$' -> And of relationals."""
    body = text.strip().strip("$")
    for tok, rel in (("\\le", sp.Le), ("\\ge", sp.Ge), ("\\neq", sp.Ne), ("<", sp.Lt), (">", sp.Gt), ("=", sp.Eq)):
        if tok in body:
            exprs = [latex_to_sympy(part) for part in body.split(tok)]
            return sp.And(*[rel(lhs, rhs) for lhs, rhs in zip(exprs, exprs[1:])])
    raise ValueError(f"no relation symbol in {text!r}")


def _b4_system(text: str):
    """'$4s + 6b = 94$ and $s + 2b = 27$' -> list of SymPy equations."""
    return [Eq(*_split_equation(part)) for part in text.split(" and ")]


def _b4_line(points):
    """Linear expression in x through two points; extra points are checked to lie on it."""
    (x1, y1), (x2, y2) = points[:2]
    slope = Rational(y2 - y1, x2 - x1)
    intercept = y1 - slope * x1
    for px, py in points[2:]:
        assert slope * px + intercept == py
    return slope * x + intercept


# ----- Linear equations in one variable -----


def alg_trail_crew_solution_meaning():
    done, rate, target = 250, 18, 970
    ww = sp.solve(Eq(done + rate * w, target), w)[0]

    def check(choices, idx):
        key_ok = "weeks" in choices[idx] and "970 meters" in choices[idx] and done + rate * ww == target
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("each week" in ch and rate != ww)
            or ("add 250" in ch and Rational(done, rate) != ww)
            or ("970 weeks" in ch and done + rate * 970 != ww))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"w = {ww} weeks reaches {target} m; contradicted distractors {wrong}"

    return check


def alg_decimal_distribute_solve():
    sols = sp.solve(Eq(Rational("0.4") * (x - 5), Rational("1.2") * x + 3), x)
    assert len(sols) == 1
    return sols[0]


def alg_cord_three_pieces():
    first = x
    second = 2 * first
    third = second + 15
    return sp.solve(Eq(first + second + third, 180), x)[0]


def alg_unique_solution_k_condition():
    diff = sp.expand(k * x - 6 - (4 * (x - 3) + 2 * x))
    coeff, const = diff.coeff(x), diff.subs(x, 0)
    assert const != 0  # when the x-coefficient vanishes the equation has no solution, not infinitely many

    def unique(kv):
        return coeff.subs(k, kv) != 0

    tests = [-6, -1, 0, Rational(1, 2), 6, 7, 100]

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices)
                if all(bool(_b4_rel(ch).subs(k, kv)) == unique(kv) for kv in tests)]
        return good == [idx], f"({coeff})x = {const}; choices equivalent to 'exactly one solution': {good}"

    return check


def alg_fraction_identity_c_infinite():
    lhs = (5 * x - 2) / 3 - (x + 4) / 6
    rhs = (3 * x + 1) / 2 + c
    poly = sp.Poly(sp.expand(lhs - rhs), x)
    assert poly.degree() == 0  # the x-terms cancel identically, so only the constants must agree
    return sp.solve(poly.all_coeffs()[0], c)[0]


# ----- Linear functions -----


def alg_evaluate_fraction_input():
    return (x / 4 + 9).subs(x, -12)


def alg_vine_growth_rate_meaning():
    L = Rational("3.2") * t + 14
    rate, start = sp.diff(L, t), L.subs(t, 0)

    def check(choices, idx):
        key_ok = "each week" in choices[idx] and "3.2 centimeters" in choices[idx] and rate == Rational("3.2")
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("when it is planted" in ch and start != Rational("3.2"))
            or ("3.2 weeks after" in ch and L.subs(t, Rational("3.2")) != 14)
            or ("every 3.2 weeks" in ch and Rational(14) / Rational("3.2") != rate))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"rate={rate}, L(0)={start}, L(3.2)={L.subs(t, Rational('3.2'))}; contradicted distractors {wrong}"

    return check


def alg_two_outputs_evaluate_ten():
    f = _b4_line([(-2, 19), (6, -5)])
    return f.subs(x, 10)


def alg_cooling_liquid_model():
    expected = _b4_line([(3, 86), (8, 71)])

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices)
                   if sp.expand(latex_to_sympy(ch.split("=")[1]).subs(t, x) - expected) == 0]
        return matches == [idx], f"T(t) = {expected.subs(x, t)}; matching choices {matches}"

    return check


def alg_composite_linear_g4():
    f = 3 * x - 7
    g = f.subs(x, 2 * x) + 1
    return g.subs(x, 4)


def alg_linear_difference_shift_a():
    mm, bb = symbols("m_ b_")
    sol = sp.solve([Eq(mm * a + bb, 12), Eq(mm * (a + 4) + bb, 30)], [mm, bb])
    f = sol[mm] * x + sol[bb]
    return sp.simplify(f.subs(x, a + 10) - f.subs(x, a))


def alg_linear_through_origin_structure():
    f = m * x + b
    condition = sp.expand(f.subs(x, x + 1) - f - f.subs(x, 1))  # must vanish for every x
    bb = sp.solve(sp.Poly(condition, x).all_coeffs(), [b])[b]
    mm = sp.solve(Eq(f.subs({b: bb, x: 2}), 5), m)[0]
    return f.subs({b: bb, m: mm, x: 6})


# ----- Linear equations in two variables -----


def alg_standard_form_y_intercept():
    return sp.solve(Eq(3 * 0 - 5 * y, 30), y)[0]


def alg_kiln_time_equation():
    expected = Rational("0.25") * a + Rational("0.75") * b - 18

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            ratio = sp.simplify((lhs - rhs) / expected)
            if ratio.is_number and ratio != 0:
                matches.append(i)
        return matches == [idx], f"0.25a + 0.75b = 18; equivalent choices {matches}"

    return check


def alg_parallel_line_y_intercept():
    slope = sp.solve(Eq(2 * x + 3 * y, 12), y)[0].coeff(x)
    bb = sp.solve(Eq(slope * 6 + b, -1), b)[0]
    assert bb != sp.solve(Eq(2 * x + 3 * y, 12), y)[0].subs(x, 0)  # a distinct parallel line
    return bb


def alg_intercepts_to_constants():
    aa = sp.solve(Eq(a * 4 + b * 0, 24), a)[0]
    bb = sp.solve(Eq(a * 0 + b * (-3), 24), b)[0]
    return aa - bb


def alg_slope_two_points_with_k():
    sols = sp.solve(Eq((11 - k) / (k - 2), 2), k)
    assert len(sols) == 1 and sols[0] != 2
    return sols[0]


# ----- Systems of two linear equations in two variables -----


def alg_elimination_sum_x():
    sol = sp.solve([Eq(3 * x + y, 14), Eq(x - y, 2)], [x, y])
    return sol[x]


def alg_fraction_slope_system_y():
    sol = sp.solve([Eq(y, Rational(1, 2) * x - 4), Eq(y, -Rational(3, 4) * x + 1)], [x, y])
    return sol[y]


def alg_woodworking_shop_system():
    truth = sp.solve([Eq(4 * s + 6 * b, 94), Eq(s + 2 * b, 27)], [s, b])  # from the stem's givens

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            sol = sp.solve(_b4_system(ch), [s, b], dict=True)
            if sol and sol[0] == truth:
                matches.append(i)
        return matches == [idx], f"stools {truth[s]}, benches {truth[b]}; systems with that solution {matches}"

    return check


def alg_intersection_point_constants_sum():
    aa = sp.solve(Eq(9, 3 * 4 + a), a)[0]
    bb = sp.solve(Eq(9, -2 * 4 + b), b)[0]
    return aa + bb


def alg_system_k_two_places_infinite():
    parallel = sp.solve(sp.Matrix([[3, k], [k, 12]]).det(), k)
    infinite = [kv for kv in parallel if sp.linsolve([3 * x + kv * y - 11, kv * x + 12 * y - 22], [x, y]) != sp.S.EmptySet]
    assert len(parallel) == 2 and len(infinite) == 1
    return infinite[0]


def alg_proportional_system_a_plus_b():
    factor = Rational(5, 10)
    aa, bb = factor * 3, factor * (-4)
    assert sp.linsolve([3 * x - 4 * y - 10, aa * x + bb * y - 5], [x, y]) != sp.S.EmptySet
    assert sp.Matrix([[3, -4], [aa, bb]]).det() == 0
    return aa + bb


def alg_farm_stand_baskets_difference():
    sol = sp.solve([Eq(p + q, 21), Eq(8 * p + 5 * q, 138)], [p, q])
    return sol[p] - sol[q]


# ----- Linear inequalities in one or two variables -----


def alg_inequality_flip_sign_easy():
    expected = sp.solve_univariate_inequality(sp.Ge(-3 * x + 7, 1), x, relational=False)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices)
                   if sp.solve_univariate_inequality(_b4_rel(ch), x, relational=False) == expected]
        return matches == [idx], f"solution set {expected}; matching choices {matches}"

    return check


def alg_garden_club_budget_inequality():
    expected = sp.Le(3 * s + 5 * m, 400)
    grid = [(sv, mv) for sv in range(0, 141, 10) for mv in range(0, 141, 10)]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = _b4_rel(ch)
            if all(bool(rel.subs({s: sv, m: mv})) == bool(expected.subs({s: sv, m: mv})) for sv, mv in grid):
                matches.append(i)
        return matches == [idx], f"3s + 5m <= 400; choices agreeing on a 15x15 grid {matches}"

    return check


def alg_inequality_bound_c():
    sol = sp.solve_univariate_inequality(sp.Le((2 * x - 1) / 3 + 2, x / 2 + 4), x, relational=False)
    assert sol.left == -sp.oo and not sol.right_open
    return sol.right


def alg_point_x5_y_range():
    expected = sp.solve_univariate_inequality(sp.Lt(3 * 5 - 2 * y, 7), y, relational=False)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices)
                   if sp.solve_univariate_inequality(_b4_rel(ch), y, relational=False) == expected]
        return matches == [idx], f"solution set {expected}; matching choices {matches}"

    return check


def alg_inequality_coefficient_k_flip():
    # (k - 2)x < 15 with solution x > -3: the symbol reversed, so k - 2 < 0 and 15/(k - 2) = -3.
    kk = sp.solve(Eq(15 / (k - 2), -3), k)[0]
    assert kk - 2 < 0
    sol = sp.solve_univariate_inequality(sp.Lt(kk * x - 8, 2 * x + 7), x, relational=False)
    assert sol == sp.Interval.open(-3, sp.oo), sol
    return kk


def alg_parallel_strip_combination():
    system = sp.And(sp.Gt(q, 3 * p - 2), sp.Lt(q, 3 * p + 4))
    pts = [(pv, qv) for pv in range(-4, 5) for qv in [Rational(n_, 2) for n_ in range(-30, 31)]]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = _b4_rel(ch)
            if all(bool(rel.subs({p: pv, q: qv})) == bool(system.subs({p: pv, q: qv})) for pv, qv in pts):
                matches.append(i)
        return matches == [idx], f"choices equivalent to the strip -2 < q - 3p < 4 on {len(pts)} test points: {matches}"

    return check


def alg_two_jobs_least_hours():
    sol = sp.solve_univariate_inequality(sp.Ge(14 * (30 - h) + 20 * h, 480), h, relational=False)
    assert not sol.left_open and sol.right == sp.oo
    return sol.left


def alg_shelf_inequality_point_meaning():
    weight = 12 * 10 + 8 * 12
    limit = 240
    max_small_with_10_medium = sp.floor((limit - 12 * 10) / sp.Integer(8))

    def check(choices, idx):
        key_ok = "without exceeding" in choices[idx] and weight <= limit
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("at most 12" in ch and max_small_with_10_medium != 12)
            or ("exactly 240" in ch and weight != limit)
            or ("but not both" in ch and weight <= limit))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"12(10) + 8(12) = {weight} <= {limit}; max small boxes with 10 medium = {max_small_with_10_medium}; contradicted {wrong}"

    return check


# ----- Batch batch5-psda -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch5-psda.ts (batch 5-psda).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch5_psda.py --only-extra

Each function derives the answer from the stem's givens, following the
conventions of verify_items.py: a numeric result for numeric keys, or a
callable (choices, answer_index) -> (ok, detail) for items whose choices are
equations or sentences. Helpers are prefixed _b5p_ so they do not collide
with earlier batches after the merge.
"""



import sympy as sp
from sympy import Eq, Integer, Rational, sqrt, symbols


x, p, n = symbols("x p n")


def _b5p_mean(values):
    return Rational(sum(values), len(values))


def _b5p_median(values):
    vals = sorted(values)
    k = len(vals)
    return Rational(vals[k // 2]) if k % 2 else Rational(vals[k // 2 - 1] + vals[k // 2], 2)


def _b5p_sd(values):
    mu = _b5p_mean(values)
    return sqrt(sum((v - mu) ** 2 for v in values) / len(values))


# ---------------------------------------------------------------------------
# Ratios, rates, proportional relationships, and units
# ---------------------------------------------------------------------------


def psda_oven_loaves_two_hours():
    per_minute = Rational(36, 45)
    return per_minute * 2 * 60


def psda_sprinkler_lawn_minutes():
    liters = 18 * 10 * Rational(5, 2)
    seconds = liters / Rational(3, 4)
    return seconds / 60


# ---------------------------------------------------------------------------
# Percentages
# ---------------------------------------------------------------------------


def psda_scooter_fleet_percent_increase():
    return sp.solve(Eq(n * (1 + Rational(150, 100)), 1500), n)[0]


def psda_markup_discount_profit_p():
    regular, sale = 1 + Rational(60, 100), 1 + Rational(20, 100)
    return sp.solve(Eq(regular * (1 - p / 100), sale), p)[0]


# ---------------------------------------------------------------------------
# One-variable data
# ---------------------------------------------------------------------------


def psda_flaws_mean_minus_median():
    freq = {0: 6, 1: 9, 3: 5}
    data = [v for v, f in freq.items() for _ in range(f)]
    assert len(data) == 20
    return _b5p_mean(data) - _b5p_median(data)


def psda_scaled_shifted_data_set():
    # The rule (mean -> 3m - 5, SD -> 3s) holds for every list; check it on two lists with mean 14.
    for X in ([10, 12, 14, 16, 18], [14] * 10 + [4, 24, 9, 19, 14, 14, 14, 14, 14, 14]):
        assert _b5p_mean(X) == 14 and len(X) in (5, 20)
        Y = [3 * v - 5 for v in X]
        mean_y, ratio = _b5p_mean(Y), sp.simplify(_b5p_sd(Y) / _b5p_sd(X))
        assert ratio == 3
    expected_mean, expected_ratio = mean_y, ratio
    sd_phrase = f"is {expected_ratio} times the standard deviation" if expected_ratio != 1 else "is equal to the standard deviation"

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if f"is {expected_mean}," in ch and sd_phrase in ch]
        return matches == [idx], f"mean(Y) = {expected_mean}, SD(Y)/SD(X) = {expected_ratio}; matching choices {matches}"

    return check


# ---------------------------------------------------------------------------
# Two-variable data
# ---------------------------------------------------------------------------


def psda_tidal_pool_quadratic_fit():
    pts = [(0, 5), (1, 8), (2, 9), (3, 8), (4, 5)]

    def check(choices, idx):
        ssr = []
        for ch in choices:
            rhs = latex_to_sympy(ch.split("=")[1])
            ssr.append(sum((rhs.subs(x, xv) - yv) ** 2 for xv, yv in pts))
        exact = [i for i, v in enumerate(ssr) if sp.simplify(v) == 0]
        return exact == [idx], f"sum of squared residuals per choice {[int(v) for v in ssr]}; exact fits {exact}"

    return check


def psda_newsletter_linear_vs_exponential():
    y0, y2 = 250, 360
    slope = Rational(y2 - y0, 2)
    linear_4 = y0 + slope * 4
    b = [v for v in sp.solve(Eq(y0 * x**2, y2), x) if v > 0][0]
    exp_4 = y0 * b**4
    return sp.nsimplify(exp_4 - linear_4)


# ---------------------------------------------------------------------------
# Probability and conditional probability
# ---------------------------------------------------------------------------


def psda_tokens_not_red():
    return Rational(50 - 12, 50)


def psda_workshop_book_conditional():
    first_time_no_book = 90 - 28
    no_book = 150 - 40
    return Rational(first_time_no_book, no_book)


# ---------------------------------------------------------------------------
# Inference from sample statistics and margin of error
# ---------------------------------------------------------------------------


def psda_fish_mass_sample_mean():
    lo, hi = Rational(24, 10), Rational(32, 10)
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# Evaluating statistical claims
# ---------------------------------------------------------------------------


def psda_bicycle_survey_generalize():
    sampled_from = "residents of the apartment complex"

    def check(choices, idx):
        # The key names exactly the sampled population: no wider region, no subgroup.
        good = [i for i, ch in enumerate(choices)
                if ch.strip() == f"All {sampled_from}"]
        return good == [idx], f"sampled population '{sampled_from}'; choices naming exactly it: {good}"

    return check


# ----- Batch batch5-geo -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch5-geo.ts (batch 5-geo).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch5_geo.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers. Every value is kept exact (sqrt, pi)
until a stem asks for rounding.
"""

import sympy as sp
from sympy import Eq, Integer, Rational, pi, sqrt, sin, cos, symbols


x, y, s, h = symbols("x y s h")


def _b5g_nearest(value, places: int):
    """Round an exact SymPy number to `places` decimals, asserting it is not a rounding tie."""
    scaled = sp.nsimplify(value) * 10**places
    assert abs(scaled - sp.floor(scaled) - Rational(1, 2)) > Rational(1, 100), "rounding tie"
    return Rational(int(sp.floor(scaled + Rational(1, 2))), 10**places)


def _b5g_point(text: str):
    """'$(-4, 7)$' -> sympy Point(-4, 7)."""
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.Point(sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip()))


def _b5g_circle_from_general(expr):
    """x^2 + y^2 + Dx + Ey + F -> (center Point, radius) by completing the square."""
    poly = sp.Poly(sp.expand(expr), x, y)
    assert poly.coeff_monomial(x**2) == 1 and poly.coeff_monomial(y**2) == 1 and poly.coeff_monomial(x * y) == 0
    d, e, f = poly.coeff_monomial(x), poly.coeff_monomial(y), poly.coeff_monomial(1)
    h0, k0 = -d / 2, -e / 2
    r2 = h0**2 + k0**2 - f
    assert r2 > 0
    return sp.Point(h0, k0), sqrt(r2)


# ----- Area and volume -----------------------------------------------------


def geo_cone_radius_tripled_volume():
    r, hh = symbols("r hh", positive=True)
    v1 = Rational(1, 3) * pi * r**2 * hh
    v2 = Rational(1, 3) * pi * (3 * r) ** 2 * hh
    factor = sp.simplify(v2 / v1)
    assert factor == 9
    return 40 * factor


def geo_pyramid_bin_height_perimeter():
    side = Rational(24, 4)
    base_area = side**2
    return sp.solve(Eq(Rational(1, 3) * base_area * h, 84), h)[0]


def geo_cone_cup_to_cylinder_height():
    water = Rational(1, 3) * pi * 4**2 * 9
    height = sp.solve(Eq(pi * 3**2 * h, water), h)[0]
    assert height == Rational(16, 3)
    # Distractor sanity: 144/9 (no 1/3), 48/16 (cone radius reused), 16/9 (divided by 3 twice).
    assert [_b5g_nearest(v, 1) for v in (Rational(144, 9), Rational(48, 16), Rational(16, 9))] == [
        Integer(16), Integer(3), Rational(18, 10)]
    return _b5g_nearest(height, 1)


# ----- Lines, angles, and triangles ----------------------------------------


def geo_isosceles_vertex_to_base_angle():
    vertex = Integer(44)
    base = sp.solve(Eq(vertex + 2 * s, 180), s)[0]  # PQ = PR, so angles Q and R are equal
    return base


def geo_isosceles_nested_angle_dac():
    # Coordinates: B at the origin, C on the positive x-axis, AB = AC = 1, angle B = 50°.
    deg = pi / 180
    A = sp.Point(cos(50 * deg), sin(50 * deg))
    B = sp.Point(0, 0)
    C = sp.Point(2 * cos(50 * deg), 0)
    assert sp.simplify(A.distance(B) - A.distance(C)) == 0
    # D = (d, 0) on BC with AD = BD.
    d = symbols("d")
    dd = sp.solve(Eq((d - A.x) ** 2 + A.y**2, d**2), d)[0]
    D = sp.Point(dd, 0)
    assert 0 < float(dd) < float(C.x), "D must lie between B and C"
    assert abs(float(A.distance(D) - B.distance(D))) < 1e-12
    v1, v2 = D - A, C - A
    cos_dac = (v1.x * v2.x + v1.y * v2.y) / (A.distance(D) * A.distance(C))
    angle = sp.acos(cos_dac) / deg
    value = sp.nsimplify(round(float(angle), 9))
    assert value == 30
    return value


def geo_similar_triangles_solve_x_side():
    xx = sp.solve(Eq((x + 3) / (2 * x - 1), Rational(12, 20)), x)
    assert xx == [18]
    mn = (2 * x - 1).subs(x, xx[0])
    assert (x + 3).subs(x, xx[0]) / mn == Rational(12, 20)  # corresponding sides proportional
    return mn


# ----- Right triangles and trigonometry ------------------------------------


def geo_garden_diagonal_path_cosine():
    deg = pi / 180
    path = 30 / cos(28 * deg)
    assert abs(float(path) - 33.977) < 0.001
    # Distractor sanity: 30 cos 28°, 30 sin 28°, 30 / sin 28°.
    assert [round(float(v), 1) for v in (30 * cos(28 * deg), 30 * sin(28 * deg), 30 / sin(28 * deg))] == [26.5, 14.1, 63.9]
    return _b5g_nearest(sp.nsimplify(round(float(path), 6)), 1)


def geo_sin_4x_cos_x_complement():
    deg = pi / 180
    expr = sin(4 * x * deg) - cos(x * deg)
    # Exact root from the complementary-angle identity: 4x = 90 - x.
    root = sp.solve(Eq(4 * x, 90 - x), x)[0]
    assert sp.simplify(expr.subs(x, root)) == 0
    # The root is the only one in (0, 20): scan sign changes of the difference.
    grid = [Rational(2 * i + 1, 20) for i in range(0, 200)]  # 0.05, 0.15, ..., 19.95: never lands on the root itself
    vals = [float(expr.subs(x, g)) for g in grid]
    changes = sum(1 for p, q in zip(vals, vals[1:]) if p * q < 0)
    assert changes == 1, changes
    # ... and the same scan over (0, 90) finds the second solution, x = 30, outside the range.
    wide = [Rational(2 * i + 1, 20) for i in range(0, 900)]
    wvals = [float(expr.subs(x, g)) for g in wide]
    assert sum(1 for p, q in zip(wvals, wvals[1:]) if p * q < 0) == 2
    assert 0 < root < 20
    return root


def geo_30_60_90_area_hypotenuse():
    short = sp.Symbol("short", positive=True)
    area = Rational(1, 2) * short * (short * sqrt(3))
    ss = sp.solve(Eq(area, 18 * sqrt(3)), short)
    assert ss == [6]
    return 2 * ss[0]


# ----- Circles -------------------------------------------------------------


def geo_tangent_point_distance_center():
    return sqrt(8**2 + 15**2)  # radius ⟂ tangent, so OTP is a right triangle


def geo_sector_area_radians_diameter():
    radius = Rational(16, 2)
    theta = 3 * pi / 4
    area = Rational(1, 2) * radius**2 * theta
    assert sp.simplify(area - theta / (2 * pi) * pi * radius**2) == 0
    return area


def geo_circle_general_form_top_point():
    center, radius = _b5g_circle_from_general(x**2 + y**2 + 8 * x - 4 * y - 5)
    assert center == sp.Point(-4, 2) and radius == 5
    top = sp.Point(center.x, center.y + radius)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b5g_point(ch) == top]
        on_circle = [i for i, ch in enumerate(choices) if sp.simplify(_b5g_point(ch).distance(center) - radius) == 0]
        return matches == [idx], f"top point {top}; matching choices {matches}; choices on the circle {on_circle}"

    return check


# ----- Batch batch5-advmath -----
#!/usr/bin/env python3
"""SymPy checks for batch 5-advmath (web/content/batches/batch5-advmath.ts).

Run from the repo root, against a temp items.ts that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch5_advmath.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers. Helpers are prefixed _b5m_.
"""


import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, sqrt, Eq, pi



x, y, a, b, k, w, d, m, g, T = symbols("x y a b k w d m g T")


def _b5m_rhs(choice: str):
    """Right-hand side of an equation choice such as '$V(d) = 20(3)^{d - 1}$'."""
    return latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1])


def _b5m_expr_check(expected, samples, parse=latex_to_sympy_ext, label=""):
    """MC with expression choices: exactly the key equals `expected` at every sample point."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            try:
                expr = parse(ch)
            except Exception as e:  # noqa: BLE001
                return False, f"could not parse choice {i} {ch!r}: {e}"
            if all(abs(complex((expr - expected).subs(s).evalf())) < 1e-9 for s in samples):
                matches.append(i)
        return matches == [idx], f"{label or expected}; matching choices {matches}, key index {idx}"

    return check


_B5M_X_POS = [{x: v} for v in (Rational(1, 3), Rational(3, 2), 3, 5, 7, 11)]
_B5M_X_ALL = [{x: v} for v in (-3, Rational(-1, 2), Rational(1, 3), Rational(3, 2), 3, 5, 7)]


# ---------------------------------------------------------------- Equivalent expressions


def adv_radical_simplify_even_power():
    return _b5m_expr_check(sqrt(50 * x**6), _B5M_X_POS, label="sqrt(50x^6) for x > 0")


def adv_poly_multiply_binomial_trinomial():
    return _b5m_expr_check(sp.expand((2 * x - 5) * (x**2 + 3 * x - 1)), _B5M_X_ALL, label="(2x-5)(x^2+3x-1)")


def adv_rational_undefined_values_sum():
    zeros = sp.solve(2 * x**2 - 7 * x + 3, x)
    assert len(zeros) == 2 and all(z.is_real for z in zeros)
    assert (x + 4).subs(x, zeros[0]) != 0 and (x + 4).subs(x, zeros[1]) != 0  # genuinely undefined, not 0/0
    return sum(zeros)


def adv_long_division_quadratic_divisor():
    quotient, remainder = sp.div(x**3 + 2 * x**2 - 5 * x + 1, x**2 + 1, x)
    assert sp.expand(quotient) == x + 2
    return sp.Poly(remainder, x).coeff_monomial(x)


def adv_rational_subtract_factor_denominator():
    expected = x / (x - 2) - 4 / (x**2 - 2 * x)
    samples = [{x: v} for v in (-3, Rational(-1, 2), Rational(1, 3), Rational(3, 2), 5, 7)]  # avoid 0 and 2
    assert sp.simplify(expected - (x + 2) / x) == 0
    return _b5m_expr_check(expected, samples, label="x/(x-2) - 4/(x^2-2x)")


def adv_radical_product_rational_exponent():
    expected = x ** Rational(5, 4)
    assert abs((sp.root(x**3, 4) * sqrt(x) - expected).subs(x, 7).evalf()) < 1e-12
    return _b5m_expr_check(expected, _B5M_X_POS, label="x^(3/4) * x^(1/2)")


def adv_difference_squares_quartic_ab():
    expr = sp.expand((a * x**2 + 9) * (b * x + 3) * (b * x - 3) - (16 * x**4 - 81))
    sols = sp.solve(sp.Poly(expr, x).all_coeffs(), [a, b], dict=True)
    sol = [s for s in sols if s[a] > 0 and s[b] > 0]
    assert len(sol) == 1
    return sol[0][a] * sol[0][b]


# ------------------------------------------- Nonlinear equations and systems


def adv_square_equals_constant_greater_root():
    sols = sp.solve((x - 3) ** 2 - 25, x)
    assert len(sols) == 2
    return max(sols)


def adv_two_parabolas_no_common_point():
    sols = sp.solve([Eq(y, x**2 + 2 * x + 5), Eq(y, -(x**2) + 2 * x + 1)], [x, y], dict=True)
    count = len([s for s in sols if all(v.is_real for v in s.values())])
    words = {0: "Zero", 1: "Exactly one", 2: "Exactly two"}

    def check(choices, idx):
        return choices[idx] == words[count], f"{count} real common point(s) -> '{words[count]}'"

    return check


def adv_two_parabolas_tangent_y_coordinate():
    sols = sp.solve([Eq(y, 2 * x**2 - 3 * x + 1), Eq(y, x**2 + x - 3)], [x, y], dict=True)
    assert len(sols) == 1, sols  # tangent: exactly one common point
    return sols[0][y]


def adv_pendulum_solve_for_length():
    L = Symbol("L", positive=True)
    gg = Symbol("g", positive=True)
    TT = Symbol("T", positive=True)
    expected = sp.solve(Eq(TT, 2 * pi * sqrt(L / gg)), L)[0]
    samples = [{g: 9.8, T: 2}, {g: Rational(49, 5), T: Rational(7, 3)}, {g: 3, T: 5}]
    target = expected.subs({gg: g, TT: T})
    return _b5m_expr_check(target, samples, parse=_b5m_rhs, label=f"L = {target}")


def adv_two_real_solutions_least_integer_k():
    disc = sp.discriminant(x**2 - 2 * k * x + 5 * k - 6, x)
    ok = [kv for kv in range(1, 20) if disc.subs(k, kv) > 0]
    assert ok[:3] == [1, 4, 5], ok
    return Integer(min(ok))


def adv_two_parabolas_tangent_k():
    disc = sp.discriminant((x - 1) ** 2 + k - (-((x - 3) ** 2) + 5), x)
    sols = sp.solve(disc, k)
    assert len(sols) == 1
    return sols[0]


def adv_exponential_difference_common_factor():
    sols = sp.solve(2 ** (x + 3) - 2**x - 56, x)
    assert len(sols) == 1
    return sols[0]


# ---------------------------------------------------------- Nonlinear functions


def adv_message_board_posts_weeks():
    sols = sp.solve(4 * 2**w - 128, w)
    assert len(sols) == 1
    return sols[0]


def adv_video_views_exponential_model():
    data = {1: 20, 2: 60, 3: 180, 4: 540}

    def check(choices, idx):
        fits = []
        for i, ch in enumerate(choices):
            rhs = _b5m_rhs(ch)
            if all(sp.simplify(rhs.subs(d, dv) - vv) == 0 for dv, vv in data.items()):
                fits.append(i)
        return fits == [idx], f"choices fitting all four data points: {fits}"

    return check


def adv_distinct_intercepts_multiplicity():
    rts = sp.roots(sp.Poly(sp.expand(x * (x - 4) ** 2 * (x**2 + 1)), x))
    real = [r for r in rts if r.is_real]
    assert sum(rts.values()) == 5  # degree 5 counting multiplicity
    return Integer(len(real))


def adv_coin_value_monthly_function():
    yearly = Rational(106, 100)

    def check(choices, idx):
        fits = []
        for i, ch in enumerate(choices):
            rhs = _b5m_rhs(ch)
            good = True
            for months in (12, 24, 36):
                val = rhs.subs(m, months).evalf()
                target = (1200 * yearly ** Rational(months, 12)).evalf()
                if abs(val - target) > 1e-6:
                    good = False
            if good:
                fits.append(i)
        return fits == [idx], f"choices giving exactly 6% per year at 12, 24, 36 months: {fits}"

    return check


def adv_photo_frame_uniform_width():
    sols = sp.solve((8 + 2 * w) * (10 + 2 * w) - 168, w)
    pos = [s for s in sols if s > 0]
    assert len(pos) == 1
    return pos[0]


def adv_quartic_end_behavior_factored():
    f = (2 - x) * (x + 1) ** 2 * (x - 5)
    left = "decreases" if sp.limit(f, x, -sp.oo) == -sp.oo else "increases"
    right = "decreases" if sp.limit(f, x, sp.oo) == -sp.oo else "increases"

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            first, second = ch.split(", and ")
            if f"$f(x)$ {left} without bound" in first and f"$f(x)$ {right} without bound" in second:
                matches.append(i)
        return matches == [idx], f"left {left}, right {right}; matching choices {matches}"

    return check


# ----- Batch batch5-algebra -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch5-algebra.ts (batch 5-algebra).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch5_algebra.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""



import sympy as sp
from sympy import Eq, Integer, Rational, symbols



x, y, k, p, q, m, b, c, w, t, d, r = symbols("x y k p q m b c w t d r")


def _b5a_rel(text: str):
    """'$5r + 40d \\le 2,500$' -> SymPy relational; a chain '$-3 \\le x < 3.5$' -> And of relationals."""
    import re as _re
    body = text.strip().strip("$")
    ops = {"\\le": sp.Le, "\\ge": sp.Ge, "\\neq": sp.Ne, "<": sp.Lt, ">": sp.Gt, "=": sp.Eq}
    parts = _re.split(r"(\\le|\\ge|\\neq|<|>|=)", body)
    if len(parts) < 3:
        raise ValueError(f"no relation symbol in {text!r}")
    exprs = [latex_to_sympy(parts[i]) for i in range(0, len(parts), 2)]
    rels = [ops[parts[i]] for i in range(1, len(parts), 2)]
    return sp.And(*[rel(lhs, rhs) for rel, lhs, rhs in zip(rels, exprs, exprs[1:])])


def _b5a_condition(text: str):
    """'$p = 8$ and $q \\neq 2$' -> And of the two relationals."""
    return sp.And(*[_b5a_rel(part) for part in text.split(" and ")])


def _b5a_line(points):
    """Linear expression in x through two points."""
    (x1, y1), (x2, y2) = points
    slope = Rational(y2 - y1, x2 - x1)
    return slope * x + (y1 - slope * x1)


def _b5a_interpretation(key_phrases, contradictions):
    """MC check for sentence choices: the key contains every key phrase; each
    distractor is matched by one (phrase, claim_is_false) pair and that claim must be false."""

    def check(choices, idx):
        key_ok = all(ph in choices[idx] for ph in key_phrases)
        wrong = []
        for i, ch in enumerate(choices):
            if i == idx:
                continue
            for phrase, is_false in contradictions:
                if phrase in ch and is_false:
                    wrong.append(i)
                    break
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"key phrases {key_phrases} present={key_ok}; contradicted distractors {wrong}"

    return check


# ----- Linear equations in one variable -----


def alg_distribute_both_sides_solve():
    sols = sp.solve(Eq(3 * (x + 4), 5 * x - 2), x)
    assert len(sols) == 1
    return sols[0]


def alg_bookstore_split_copies():
    fewer = sp.solve(Eq(c + (c + 24), 150), c)[0]
    return fewer + 24


def alg_fraction_difference_solve_spr():
    sols = sp.solve(Eq((3 * x - 1) / 4 - x / 6, 2), x)
    assert len(sols) == 1
    return sols[0]


def alg_no_solution_two_constants_grid():
    diff = sp.expand(p * x + 8 - 4 * (2 * x + q))
    coeff, const = diff.coeff(x), diff.subs(x, 0)

    def no_solution(pv, qv):
        return coeff.subs(p, pv) == 0 and const.subs(q, qv) != 0

    grid = [(pv, qv) for pv in (7, 8, 9, Rational(17, 2)) for qv in (1, 2, 3, Rational(5, 2))]

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices)
                if all(bool(_b5a_condition(ch).subs({p: pv, q: qv})) == no_solution(pv, qv) for pv, qv in grid)]
        return good == [idx], f"({coeff})x = {-const}; choices equivalent to 'no solution': {good}"

    return check


def alg_constant_both_sides_known_solution():
    kk = sp.solve(Eq(k * (x - 2), 3 * x + 5 * k - 2).subs(x, 4), k)
    assert len(kk) == 1
    assert sp.solve(Eq(kk[0] * (x - 2), 3 * x + 5 * kk[0] - 2), x) == [4]
    return kk[0]


# ----- Linear functions -----


def alg_evaluate_negative_input():
    return (9 - 4 * x).subs(x, -3)


def alg_balloon_descent_initial_altitude():
    B = 520 - 65 * t
    start, rate, ground, at65 = B.subs(t, 0), sp.diff(B, t), sp.solve(B, t)[0], B.subs(t, 65)
    return _b5a_interpretation(
        ["520 meters when it begins descending"],
        [("each minute", rate != -520), ("reaches the ground", ground != 520), ("65 minutes after", at65 != 520)],
    ) if start == 520 else (lambda choices, idx: (False, "B(0) != 520"))


def alg_printer_page_count_input_spr():
    return sp.solve(Eq(28 * d + 190, 1170), d)[0]


def alg_linear_constant_from_one_output():
    cc = sp.solve(Eq(5 * 3 + c, 4), c)[0]
    return (5 * x + cc).subs(x, -1)


def alg_warehouse_pallets_pair_meaning():
    N = 36 + 9 * w
    return _b5a_interpretation(
        ["72 pallets in stock 4 weeks from now"],
        [("during the next 4 weeks", N.subs(w, 4) - N.subs(w, 0) != 72),
         ("4 pallets each week", sp.diff(N, w) != 4),
         ("72 weeks from now", N.subs(w, 72) != 4)],
    ) if N.subs(w, 4) == 72 else (lambda choices, idx: (False, "N(4) != 72"))


def alg_linear_constants_output_relation():
    f = m * x + b
    sol = sp.solve([Eq(f.subs(x, 3), 2 * f.subs(x, 1)), Eq(f.subs(x, 5), 18)], [m, b])
    return sol[b]


def alg_linear_k_scaled_inputs_spr():
    kp = sp.Symbol("k", positive=True)
    f = m * x + b
    sol = sp.solve([Eq(f.subs(x, kp), 3), Eq(f.subs(x, 2 * kp), 11), Eq(f.subs(x, 1), 5)], [m, b, kp], dict=True)
    assert len(sol) == 1
    return sol[0][kp]


# ----- Linear equations in two variables -----


def alg_point_on_standard_line_k():
    return sp.solve(Eq(2 * 4 + 3 * k, 23), k)[0]


def alg_recycling_coefficient_meaning():
    expr = Rational("0.8") * x + Rational("3.2") * c  # x stands for a, the aluminum
    coeff_c, coeff_a = expr.coeff(c), expr.coeff(x)
    return _b5a_interpretation(
        ["for each kilogram of copper"],
        [("for each kilogram of aluminum", coeff_a != Rational("3.2")),
         ("more for a kilogram of copper", coeff_c - coeff_a != Rational("3.2")),
         ("contains 3.2 kilograms", all(sp.solve(Eq(expr.subs(c, cv), 56), x) for cv in (Rational("3.2"), 5)))],
    ) if coeff_c == Rational("3.2") else (lambda choices, idx: (False, "coefficient of c != 3.2"))


def alg_two_points_x_axis_crossing_spr():
    line = _b5a_line([(-2, 9), (4, -3)])
    return sp.solve(line, x)[0]


def alg_perpendicular_line_equation():
    given_slope = sp.solve(Eq(x - 4 * y, 2), y)[0].coeff(x)
    perp = -1 / given_slope
    expected = perp * (x + 1) + 5

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            assert lhs == y
            if sp.expand(rhs - expected) == 0:
                matches.append(i)
        return matches == [idx], f"line: y = {expected}; matching choices {matches}"

    return check


def alg_intercepts_relation_k_spr():
    bb = sp.solve(Eq(k * 0 - 3 * y, 12), y)[0]
    aa = 2 * bb
    kk = sp.solve(Eq(k * aa - 3 * 0, 12), k)
    assert len(kk) == 1
    return kk[0]


# ----- Systems of two linear equations in two variables -----


def alg_system_sum_of_coordinates():
    sol = sp.solve([Eq(y, 2 * x + 1), Eq(y, -3 * x + 16)], [x, y])
    return sol[x] + sol[y]


def alg_hardware_bolts_containers():
    sol = sp.solve([Eq(b + c, 14), Eq(25 * b + 8 * c, 248)], [b, c])  # b boxes, c bags
    assert sol[b].is_integer and sol[c].is_integer and sol[b] > 0 and sol[c] > 0
    return sol[b]


def alg_system_count_solutions_coincident():
    sols = sp.linsolve([4 * x - 6 * y - 10, -6 * x + 9 * y + 15], [x, y])
    if sols == sp.S.EmptySet:
        word = "Zero"
    elif any(v.free_symbols for v in next(iter(sols))):
        word = "Infinitely many"
    else:
        word = "Exactly one"

    def check(choices, idx):
        return choices[idx] == word, f"linsolve -> {sols} -> '{word}'"

    return check


def alg_fraction_coefficient_system_x_spr():
    sol = sp.solve([Eq(x / 2 + y / 3, 5), Eq(x - y, 3)], [x, y])
    return sol[x]


def alg_parallel_unless_coincident_b():
    def has_solution(bv):
        return sp.linsolve([y - (2 * x + bv), 4 * x - 2 * y - 7], [x, y]) != sp.S.EmptySet

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if has_solution(latex_to_sympy(ch))]
        return good == [idx], f"choices for which the system has a solution: {good}"

    return check


def alg_artist_prints_total_spr():
    sol = sp.solve([Eq(x, 3 * y), Eq(15 * x + 40 * y, 1020)], [x, y])  # x small, y large
    assert sol[x].is_integer and sol[y].is_integer
    return sol[x] + sol[y]


# ----- Linear inequalities in one or two variables -----


def alg_greatest_value_simple_inequality():
    sol = sp.solve_univariate_inequality(sp.Le(2 * x + 7, 19), x, relational=False)
    assert sol.left == -sp.oo and not sol.right_open
    return sol.right


def alg_fundraiser_tickets_inequality():
    expected = sp.Ge(5 * r + 40 * d, 2500)
    grid = [(rv, dv) for rv in range(0, 601, 50) for dv in range(0, 81, 5)]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = _b5a_rel(ch)
            if all(bool(rel.subs({r: rv, d: dv})) == bool(expected.subs({r: rv, d: dv})) for rv, dv in grid):
                matches.append(i)
        return matches == [idx], f"5r + 40d >= 2500; choices agreeing on a {len(grid)}-point grid {matches}"

    return check


def alg_point_system_inequalities_count_k():
    system = sp.And(sp.Lt(y, 2 * x + 1), sp.Gt(y, -x + 2)).subs(x, 3)
    ints = [kv for kv in range(-50, 51) if bool(system.subs(y, kv))]
    assert ints == list(range(0, 7))
    return Integer(len(ints))


def alg_craft_fair_mugs_least():
    profit = 12 * x - Rational("4.5") * x - 350
    sol = sp.solve_univariate_inequality(sp.Ge(profit, 200), x, relational=False)
    assert sol.right == sp.oo
    least = sp.ceiling(sol.left)
    assert profit.subs(x, least) >= 200 and profit.subs(x, least - 1) < 200
    return least


def alg_compound_inequality_flip():
    truth = sp.And(sp.Lt(-4, 3 - 2 * x), sp.Le(3 - 2 * x, 9))
    tests = [Rational(v, 4) for v in range(-20, 21)]  # -5 .. 5 in quarter steps, including -3 and 3.5

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices)
                   if all(bool(_b5a_rel(ch).subs(x, tv)) == bool(truth.subs(x, tv)) for tv in tests)]
        sol = sp.reduce_inequalities([-4 < 3 - 2 * x, 3 - 2 * x <= 9], x)
        return matches == [idx], f"solution set {sol}; choices agreeing on {len(tests)} test points: {matches}"

    return check


def alg_scaled_inequality_max():
    target = 4 * x + 6 * y
    ratio = sp.simplify(target / (2 * x + 3 * y))
    assert ratio.is_number  # the target is a constant multiple of the constrained expression
    best = ratio * 12
    assert target.subs({x: 6, y: 0}) == best and (2 * x + 3 * y).subs({x: 6, y: 0}) <= 12
    return best


def alg_fraction_inequality_k_bound():
    # Clearing denominators: 3(x - k) > 2x + 6, so x > 3k + 6; the bound must be 15.
    lhs, rhs = (x - k) / 2, x / 3 + 1
    bound = sp.solve(Eq(lhs - rhs, 0), x)[0]
    assert sp.diff(lhs - rhs, x) > 0  # left side grows faster, so the solution set is x > bound
    kk = sp.solve(Eq(bound, 15), k)[0]
    assert sp.solve_univariate_inequality(sp.Gt(lhs.subs(k, kk), rhs), x, relational=False) == sp.Interval.open(15, sp.oo)
    return kk


# ----- Batch batch6-psdaA -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch6-psdaA.ts (batch batch6-psdaA).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch6_psdaA.py --only-extra

Each function derives the answer from the stem's givens, following the
conventions of verify_items.py. Helpers are prefixed _b6pa_ so they do not
collide with earlier batches after the merge.
"""


import sympy as sp
from sympy import Eq, Integer, Rational, symbols


_b6pa_x, _b6pa_k, _b6pa_g, _b6pa_m, _b6pa_p = symbols("_b6pa_x _b6pa_k _b6pa_g _b6pa_m _b6pa_p")


def _b6pa_dec(text):
    """Exact Rational from a decimal string, so 0.65 is 13/20, not a float."""
    return Rational(text)


def _b6pa_solve_positive(eq, var):
    sols = [s for s in sp.solve(eq, var) if s.is_real and s > 0]
    assert len(sols) == 1, sols
    return sols[0]


# ----- Ratios, rates, proportional relationships, and units -----


def psda_b6pa_coffee_beans_per_ounce():
    return _b6pa_dec("9.60") / 12


def psda_b6pa_road_map_towns_inches():
    return _b6pa_dec("4.2") * 15


def psda_b6pa_truck_fuel_route():
    return _b6pa_dec("0.12") * 245


def psda_b6pa_direct_proportion_y_x():
    k = Rational(30, 8)
    return k * 20


def psda_b6pa_map_scale_lakes_km():
    cm = _b6pa_dec("6.4") * 250000
    return cm / (100 * 1000)


def psda_b6pa_train_kmh_to_mps():
    return Rational(108 * 1000, 60 * 60)


def psda_b6pa_carpet_square_yards_cost():
    sq_ft = 42 * 3**2
    return sq_ft * _b6pa_dec("3.50")


def psda_b6pa_sandbox_cubic_yards():
    return _b6pa_dec("0.75") * 3**3


def psda_b6pa_wood_board_mass_kg():
    grams = 120 * 15 * 2 * _b6pa_dec("0.65")
    return grams / 1000


def psda_b6pa_trail_mix_almonds():
    grams = _b6pa_dec("1.5") * 1000
    return grams * Rational(5, 2 + 3 + 5)


def psda_b6pa_soup_calories_liters():
    ml = _b6pa_dec("0.4") * 1000
    return Rational(140, 250) * ml


def psda_b6pa_painting_crew_days():
    worker_days = 6 * 15
    return Rational(worker_days, 9)


def psda_b6pa_download_megabits_minutes():
    seconds = Rational(900 * 8, 60)
    return seconds / 60


def psda_b6pa_ratio_chain_a_over_c():
    a, b, c = symbols("a b c", nonzero=True)
    sol = sp.solve([Eq(2 * a, 5 * b), Eq(3 * b, 4 * c)], [a, b], dict=True)[0]
    return sp.simplify(sol[a] / c)


def psda_b6pa_club_juniors_ratio_change():
    k = _b6pa_k
    kval = sp.solve(Eq((4 * k + 12) / (5 * k), Rational(6, 5)), k)[0]
    return 4 * kval + 5 * kval


def psda_b6pa_fuel_efficiency_mpg():
    exact = 15 / _b6pa_dec("1.6") * _b6pa_dec("3.8")
    return Integer(sp.floor(exact + Rational(1, 2)))


def psda_b6pa_tank_two_hoses_hours():
    t = _b6pa_x
    liters = 54 * 1000
    both = sp.solve(Eq(180 * 60 + (180 + 120) * t, liters), t)[0]
    return (60 + both) / 60


def psda_b6pa_blueprint_parking_space_area():
    actual_cm2 = 120 * 50**2
    return Rational(actual_cm2, 100**2)


def psda_b6pa_faucet_drips_liters():
    minutes = 30 * 24 * 60
    ml = Rational(12 * minutes, 20)
    return ml / 1000


def psda_b6pa_three_part_ratio_sum():
    a, b, c = symbols("a b c", positive=True)
    sol = sp.solve([Eq(3 * a, 2 * b), Eq(5 * b, 4 * c), Eq(a + b + c, 105)], [a, b, c], dict=True)[0]
    return sol[c]


# ----- Percentages -----


def psda_b6pa_percent_of_number():
    return Rational(35, 100) * 840


def psda_b6pa_recycling_households_p():
    before = Rational(40, 100) * 2500
    after = Rational(50, 100) * 2800
    return (after - before) / before * 100


def psda_b6pa_grain_drying_original():
    m = _b6pa_m
    return sp.solve(Eq(m * (1 - Rational(12, 100)), 2640), m)[0]


def psda_b6pa_double_increase_44():
    p = _b6pa_p
    return _b6pa_solve_positive(Eq((1 + p / 100) ** 2, 1 + Rational(44, 100)), p)


def psda_b6pa_chess_club_girls():
    g = _b6pa_g
    return sp.solve(Eq(Rational(30, 100) * (1000 - g) + Rational(45, 100) * g, Rational(36, 100) * 1000), g)[0]


def psda_b6pa_monthly_sales_successive():
    jan = 2500
    feb = jan * (1 - Rational(8, 100))
    mar = feb * (1 + Rational(15, 100))
    return (mar - jan) / jan * 100


# ----- Batch batch6-lf1 -----
import sympy as sp
from sympy import Rational, Eq

_b6lf_x = sp.Symbol("x")
_b6lf_k = sp.Symbol("k")
_b6lf_t = sp.Symbol("t")


def _b6lf_line(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    m = (sp.nsimplify(y2) - sp.nsimplify(y1)) / (sp.nsimplify(x2) - sp.nsimplify(x1))
    return m * _b6lf_x + (sp.nsimplify(y1) - m * sp.nsimplify(x1))


def _b6lf_rhs_matches(expected, var=None):
    """MC check for equation choices 'f(x) = ...': exactly the key's right side equals expected."""
    var = var or _b6lf_x

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            rhs = ch.strip().strip("$").split("=", 1)[1]
            expr = sp.nsimplify(latex_to_sympy(rhs).subs(sp.Symbol(str(var)), _b6lf_x), rational=True)
            if sp.expand(expr - expected) == 0:
                hits.append(i)
        return hits == [idx], f"expected {expected}; matching choices {hits}"

    return check


def _b6lf_sentences(key_phrase, key_true, contradictions):
    """Sentence choices: key contains key_phrase and its claim is true; each distractor
    matches one (phrase, claim_is_false) pair whose claim is false."""

    def check(choices, idx):
        key_ok = key_phrase in choices[idx] and key_true
        wrong = []
        for i, ch in enumerate(choices):
            if i == idx:
                continue
            if any(ph in ch and is_false for ph, is_false in contradictions):
                wrong.append(i)
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"key ok={key_ok}; contradicted distractors {wrong}"

    return check


def alg_lf_eval_two_thirds_coefficient():
    return (6 - Rational(2, 3) * _b6lf_x).subs(_b6lf_x, 9)


def alg_lf_input_for_negative_output():
    sol = sp.solve(Eq(4 * _b6lf_x + 15, -9), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_slope_through_two_points():
    return sp.Poly(_b6lf_line((2, 9), (6, 1)), _b6lf_x).coeff_monomial(_b6lf_x)


def alg_lf_scaled_output_known_value():
    f4 = 11
    return 2 * f4 - 3


def alg_lf_campsite_temperature_rate():
    h = sp.Symbol("h")
    T = 62 - Rational(7, 2) * h
    rate = sp.diff(T, h)
    return _b6lf_sentences(
        "decreases by 3.5 degrees Fahrenheit each hour",
        rate == -Rational(7, 2),
        [("at sunset is 3.5", T.subs(h, 0) != Rational(7, 2)),
         ("reaches 0 degrees", T.subs(h, Rational(7, 2)) != 0),
         ("62 hours after sunset", T.subs(h, 62) != Rational(7, 2))],
    )


def alg_lf_rule_from_slope_and_intercept():
    return _b6lf_rhs_matches(4 * _b6lf_x - 3)


def alg_lf_combined_outputs_value():
    f = -5 * _b6lf_x + 8
    return 3 * f.subs(_b6lf_x, 2) - f.subs(_b6lf_x, -2)


def alg_lf_table_x_intercept_spr():
    pts = [(-3, 17), (1, 5), (6, -10)]
    h = _b6lf_line(pts[0], pts[1])
    assert h.subs(_b6lf_x, pts[2][0]) == pts[2][1]
    sol = sp.solve(Eq(h, 0), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_two_intercepts_evaluate():
    f = _b6lf_line((6, 0), (0, -4))
    return f.subs(_b6lf_x, 15)


def alg_lf_point_slope_form_intercept():
    return (5 * (_b6lf_x - 2) + 1).subs(_b6lf_x, 0)


def alg_lf_input_shift_rule():
    f = lambda v: 3 * v - 8  # noqa: E731
    return _b6lf_rhs_matches(sp.expand(f(_b6lf_x + 2)))


def alg_lf_table_y_intercept():
    pts = [(-4, 21), (2, 6), (6, -4)]
    f = _b6lf_line(pts[0], pts[1])
    assert f.subs(_b6lf_x, pts[2][0]) == pts[2][1]
    return f.subs(_b6lf_x, 0)


def alg_lf_sum_of_constants_two_points():
    a, b = sp.symbols("a b")
    sol = sp.solve([Eq(a * -1 + b, 11), Eq(a * 2 + b, 2)], [a, b])
    return sol[a] + sol[b]


def alg_lf_generator_fuel_factored():
    d = sp.Symbol("d")
    V = 25 * (32 - d)
    return _b6lf_sentences(
        "empty 32 days after",
        V.subs(d, 32) == 0,
        [("holds 32 liters of fuel when it is filled", V.subs(d, 0) != 32),
         ("uses 32 liters of fuel each day", -sp.diff(V, d) != 32),
         ("holds 25 liters of fuel 32 days", V.subs(d, 32) != 25)],
    )


def alg_lf_snow_depth_model():
    # S(2) = 25 and the depth falls 1.5 cm each hour.
    m = -Rational(3, 2)
    S = m * (_b6lf_x - 2) + 25
    return _b6lf_rhs_matches(sp.expand(S), var=sp.Symbol("h"))


def alg_lf_pool_depth_minutes():
    hours = sp.solve(Eq(Rational(4, 5) * _b6lf_t + Rational(7, 5), Rational(27, 5)), _b6lf_t)[0]
    return 60 * hours


def alg_lf_delivery_truck_point_meaning():
    f = _b6lf_line((0, 120), (8, 0))
    rate = sp.diff(f, _b6lf_x)
    return _b6lf_sentences(
        "75 packages left 3 hours",
        f.subs(_b6lf_x, 3) == 75,
        [("delivers 75 packages during the first 3 hours", f.subs(_b6lf_x, 0) - f.subs(_b6lf_x, 3) != 75),
         ("delivers 25 packages each hour", -rate != 25),
         ("3 packages left 75 hours", f.subs(_b6lf_x, 75) != 3)],
    )


def alg_lf_scaled_shifted_x_intercept():
    f = 4 * _b6lf_x - 6
    g = -2 * f + 5
    sol = sp.solve(Eq(g, 0), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_horizontal_shift_constant():
    f = lambda v: 6 * v - 5  # noqa: E731
    sol = sp.solve(Eq(f(4 - _b6lf_k), 1), _b6lf_k)
    assert len(sol) == 1
    return sol[0]


def alg_lf_intersection_y_coordinate():
    f = 3 * _b6lf_x + 7
    g = _b6lf_line((-1, 12), (3, 0))
    xs = sp.solve(Eq(f, g), _b6lf_x)
    assert len(xs) == 1
    return f.subs(_b6lf_x, xs[0])


def alg_lf_verbal_rates_double_output():
    f = 12 - 2 * _b6lf_x
    g = -3 + 3 * _b6lf_x
    sol = sp.solve(Eq(f, 2 * g), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_two_plants_height_gap():
    w = sp.Symbol("w")
    A = Rational(5, 2) * w + 18
    B = 9 + 4 * w
    sol = sp.solve(Eq(B - A, 3), w)
    assert len(sol) == 1
    return sol[0]


def alg_lf_sunflower_lagged_height():
    P = lambda v: Rational(9, 5) * v + 52  # noqa: E731
    return _b6lf_rhs_matches(sp.expand(P(_b6lf_x - 5)), var=_b6lf_t)


def alg_lf_tree_doubles_height():
    H = _b6lf_line((4, Rational(15, 2)), (10, 12))
    h0 = H.subs(_b6lf_x, 0)
    sol = sp.solve(Eq(H, 2 * h0), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_workshop_mugs_cheaper():
    A = 14 * _b6lf_x + 300
    B = _b6lf_line((10, 510), (30, 690))
    best = max(n for n in range(0, 1000) if A.subs(_b6lf_x, n) < B.subs(_b6lf_x, n))
    return sp.Integer(best)


def alg_lf_scaled_function_from_slope():
    f = _b6lf_line((2, 7), (6, 19))
    g = _b6lf_k * f
    kk = sp.solve(Eq(sp.diff(g, _b6lf_x), -6), _b6lf_k)[0]
    return g.subs({_b6lf_k: kk, _b6lf_x: 0})


def alg_lf_output_equals_input():
    f = _b6lf_line((-2, 9), (4, -3))
    sol = sp.solve(Eq(f, _b6lf_x), _b6lf_x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_vertical_shift_through_point():
    f = _b6lf_line((1, 3), (5, 11))
    sol = sp.solve(Eq(f.subs(_b6lf_x, 4) + _b6lf_k, 2), _b6lf_k)
    assert len(sol) == 1
    return sol[0]


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
    # batch batch3-geo
    "geo-prism-to-cube-edge": geo_prism_to_cube_edge,
    "geo-rectangle-perimeter-to-area": geo_rectangle_perimeter_to_area,
    "geo-scale-model-floor-area": geo_scale_model_floor_area,
    "geo-cylinder-tank-radius-decimal": geo_cylinder_tank_radius_decimal,
    "geo-prism-cubic-volume-s": geo_prism_cubic_volume_s,
    "geo-cone-cut-volume-ratio": geo_cone_cut_volume_ratio,
    "geo-parallel-obtuse-angle": geo_parallel_obtuse_angle,
    "geo-exterior-angle-x": geo_exterior_angle_x,
    "geo-similar-triangle-perimeter": geo_similar_triangle_perimeter,
    "geo-triangle-between-parallels": geo_triangle_between_parallels,
    "geo-parallel-segment-trapezoid-area": geo_parallel_segment_trapezoid_area,
    "geo-degrees-to-radians-150": geo_degrees_to_radians_150,
    "geo-pole-wire-tangent-height": geo_pole_wire_tangent_height,
    "geo-ramp-angle-arctan": geo_ramp_angle_arctan,
    "geo-isosceles-right-area": geo_isosceles_right_area,
    "geo-altitude-angle-sine": geo_altitude_angle_sine,
    "geo-quadrant-four-cosine": geo_quadrant_four_cosine,
    "geo-arc-length-100-degrees": geo_arc_length_100_degrees,
    "geo-circle-chord-on-line": geo_circle_chord_on_line,
    "geo-sector-angle-garden": geo_sector_angle_garden,
    "geo-circle-radius-constant-c": geo_circle_radius_constant_c,
    "geo-circle-tangent-vertical-line": geo_circle_tangent_vertical_line,
    # batch batch3-algebra
    "alg-ride-fare-equation": alg_ride_fare_equation,
    "alg-fraction-equation-solve": alg_fraction_equation_solve,
    "alg-plumber-hours": alg_plumber_hours,
    "alg-count-solutions-identity": alg_count_solutions_identity,
    "alg-structure-x-plus-3": alg_structure_x_plus_3,
    "alg-infinitely-many-c": alg_infinitely_many_c,
    "alg-evaluate-linear-f4": alg_evaluate_linear_f4,
    "alg-drain-rate-interpretation": alg_drain_rate_interpretation,
    "alg-table-to-rule-g": alg_table_to_rule_g,
    "alg-bird-count-model": alg_bird_count_model,
    "alg-rule-from-point-and-rate": alg_rule_from_point_and_rate,
    "alg-linear-shift-rule": alg_linear_shift_rule,
    "alg-rate-find-input": alg_rate_find_input,
    "alg-candle-height-time": alg_candle_height_time,
    "alg-slope-two-points": alg_slope_two_points,
    "alg-line-point-slope-equation": alg_line_point_slope_equation,
    "alg-snack-stand-pretzels": alg_snack_stand_pretzels,
    "alg-table-line-find-x": alg_table_line_find_x,
    "alg-line-constant-x-intercept": alg_line_constant_x_intercept,
    "alg-budget-x-intercept-meaning": alg_budget_x_intercept_meaning,
    "alg-system-substitution-y": alg_system_substitution_y,
    "alg-theater-child-tickets": alg_theater_child_tickets,
    "alg-system-product-xy": alg_system_product_xy,
    "alg-infinite-solutions-c": alg_infinite_solutions_c,
    "alg-system-k-on-line": alg_system_k_on_line,
    "alg-tanks-equal-volume": alg_tanks_equal_volume,
    "alg-point-satisfies-inequality": alg_point_satisfies_inequality,
    "alg-elevator-crates-inequality": alg_elevator_crates_inequality,
    "alg-greatest-integer-inequality": alg_greatest_integer_inequality,
    "alg-inequality-solution-set-c": alg_inequality_solution_set_c,
    "alg-system-inequalities-point": alg_system_inequalities_point,
    "alg-count-integers-two-inequalities": alg_count_integers_two_inequalities,
    # batch batch3-psda
    "psda-scale-drawing-path": psda_scale_drawing_path,
    "psda-kilowatt-hours-heater": psda_kilowatt_hours_heater,
    "psda-density-neighbor-county": psda_density_neighbor_county,
    "psda-cyclist-speed-mps": psda_cyclist_speed_mps,
    "psda-jacket-sale-price": psda_jacket_sale_price,
    "psda-percent-of-percent-music-art": psda_percent_of_percent_music_art,
    "psda-tax-tip-original-cost": psda_tax_tip_original_cost,
    "psda-books-frequency-mean": psda_books_frequency_mean,
    "psda-remove-max-mean-median": psda_remove_max_mean_median,
    "psda-combined-shifted-sets-sd": psda_combined_shifted_sets_sd,
    "psda-model-predict-customers": psda_model_predict_customers,
    "psda-residual-from-model": psda_residual_from_model,
    "psda-cells-exponential-model": psda_cells_exponential_model,
    "psda-best-fit-predict-eight": psda_best_fit_predict_eight,
    "psda-parking-lot-van": psda_parking_lot_van,
    "psda-club-members-given-probability": psda_club_members_given_probability,
    "psda-commuters-transit-conditional": psda_commuters_transit_conditional,
    "psda-moe-streaming-interpretation": psda_moe_streaming_interpretation,
    "psda-sample-proportion-employees": psda_sample_proportion_employees,
    "psda-fitness-stretching-experiment": psda_fitness_stretching_experiment,
    "psda-sampling-method-walk": psda_sampling_method_walk,
    "psda-lavender-volunteers-generalize": psda_lavender_volunteers_generalize,
    # batch batch3-advmath
    "adv-poly-subtract-fluency": adv_poly_subtract_fluency,
    "adv-difference-of-squares-factor": adv_difference_of_squares_factor,
    "adv-rational-combine-constants": adv_rational_combine_constants,
    "adv-rational-exponent-simplify": adv_rational_exponent_simplify,
    "adv-polynomial-product-constant-c": adv_polynomial_product_constant_c,
    "adv-complete-square-equivalent": adv_complete_square_equivalent,
    "adv-rational-simplify-factor-cancel": adv_rational_simplify_factor_cancel,
    "adv-rational-structure-difference": adv_rational_structure_difference,
    "adv-trinomial-factor-positive-ab": adv_trinomial_factor_positive_ab,
    "adv-exponential-rewrite-base": adv_exponential_rewrite_base,
    "adv-absolute-value-positive-solution": adv_absolute_value_positive_solution,
    "adv-rational-equation-cross-multiply": adv_rational_equation_cross_multiply,
    "adv-garden-quadratic-perimeter": adv_garden_quadratic_perimeter,
    "adv-factored-cubic-sum-solutions": adv_factored_cubic_sum_solutions,
    "adv-two-solutions-k-condition": adv_two_solutions_k_condition,
    "adv-rational-equation-extraneous": adv_rational_equation_extraneous,
    "adv-quadratic-formula-radicand": adv_quadratic_formula_radicand,
    "adv-parabola-line-tangent-c": adv_parabola_line_tangent_c,
    "adv-exponential-equation-common-base": adv_exponential_equation_common_base,
    "adv-falling-object-solve-for-t": adv_falling_object_solve_for_t,
    "adv-absolute-value-sum-of-solutions": adv_absolute_value_sum_of_solutions,
    "adv-exponential-model-evaluate-leaves": adv_exponential_model_evaluate_leaves,
    "adv-exponential-initial-value-club": adv_exponential_initial_value_club,
    "adv-vertex-form-displays-minimum": adv_vertex_form_displays_minimum,
    "adv-algae-decay-every-two-days": adv_algae_decay_every_two_days,
    "adv-quadratic-regression-shift-vertex": adv_quadratic_regression_shift_vertex,
    "adv-ball-vertex-form-interpret-max": adv_ball_vertex_form_interpret_max,
    "adv-factored-quadratic-y-intercept-a": adv_factored_quadratic_y_intercept_a,
    "adv-parabola-symmetry-other-intercept": adv_parabola_symmetry_other_intercept,
    "adv-exponential-translation-y-intercept": adv_exponential_translation_y_intercept,
    "adv-shop-profit-max-price": adv_shop_profit_max_price,
    "adv-exponential-quarterly-annual-percent": adv_exponential_quarterly_annual_percent,
    # batch batch4-advmath
    "adv-common-factor-xy": adv_common_factor_xy,
    "adv-cube-root-power": adv_cube_root_power,
    "adv-complex-fraction-difference-squares": adv_complex_fraction_difference_squares,
    "adv-tilde-square-minus-product-b": adv_tilde_square_minus_product_b,
    "adv-rational-subtract-difference-squares": adv_rational_subtract_difference_squares,
    "adv-remainder-theorem-k": adv_remainder_theorem_k,
    "adv-rational-divide-simplify": adv_rational_divide_simplify,
    "adv-quadratic-negative-solution": adv_quadratic_negative_solution,
    "adv-radical-equation-coefficient": adv_radical_equation_coefficient,
    "adv-circle-line-positive-x": adv_circle_line_positive_x,
    "adv-circle-tangent-line-c": adv_circle_tangent_line_c,
    "adv-two-parabolas-x-difference": adv_two_parabolas_x_difference,
    "adv-absolute-value-midpoint-c": adv_absolute_value_midpoint_c,
    "adv-radical-constant-extraneous-sum": adv_radical_constant_extraneous_sum,
    "adv-one-solution-leading-k": adv_one_solution_leading_k,
    "adv-kinetic-energy-solve-v": adv_kinetic_energy_solve_v,
    "adv-circle-line-no-solution": adv_circle_line_no_solution,
    "adv-quadratic-in-disguise-sum": adv_quadratic_in_disguise_sum,
    "adv-rational-equation-sum-solutions": adv_rational_equation_sum_solutions,
    "adv-cubic-evaluate-negative": adv_cubic_evaluate_negative,
    "adv-van-decay-factor-interpretation": adv_van_decay_factor_interpretation,
    "adv-medication-half-life-model": adv_medication_half_life_model,
    "adv-arch-symmetry-distance": adv_arch_symmetry_distance,
    "adv-factored-form-displays-intercepts": adv_factored_form_displays_intercepts,
    "adv-table-shift-minimum-value": adv_table_shift_minimum_value,
    "adv-composition-positive-a": adv_composition_positive_a,
    "adv-insect-colony-doubling-time": adv_insect_colony_doubling_time,
    "adv-fountain-stream-zero": adv_fountain_stream_zero,
    "adv-vehicles-percent-per-year": adv_vehicles_percent_per_year,
    "adv-horizontal-compression-intercepts": adv_horizontal_compression_intercepts,
    "adv-cubic-y-intercept-a": adv_cubic_y_intercept_a,
    "adv-barrel-percent-decrease": adv_barrel_percent_decrease,
    # batch batch4-algebra
    "alg-trail-crew-solution-meaning": alg_trail_crew_solution_meaning,
    "alg-decimal-distribute-solve": alg_decimal_distribute_solve,
    "alg-cord-three-pieces": alg_cord_three_pieces,
    "alg-unique-solution-k-condition": alg_unique_solution_k_condition,
    "alg-fraction-identity-c-infinite": alg_fraction_identity_c_infinite,
    "alg-evaluate-fraction-input": alg_evaluate_fraction_input,
    "alg-vine-growth-rate-meaning": alg_vine_growth_rate_meaning,
    "alg-two-outputs-evaluate-ten": alg_two_outputs_evaluate_ten,
    "alg-cooling-liquid-model": alg_cooling_liquid_model,
    "alg-composite-linear-g4": alg_composite_linear_g4,
    "alg-linear-difference-shift-a": alg_linear_difference_shift_a,
    "alg-linear-through-origin-structure": alg_linear_through_origin_structure,
    "alg-standard-form-y-intercept": alg_standard_form_y_intercept,
    "alg-kiln-time-equation": alg_kiln_time_equation,
    "alg-parallel-line-y-intercept": alg_parallel_line_y_intercept,
    "alg-intercepts-to-constants": alg_intercepts_to_constants,
    "alg-slope-two-points-with-k": alg_slope_two_points_with_k,
    "alg-elimination-sum-x": alg_elimination_sum_x,
    "alg-fraction-slope-system-y": alg_fraction_slope_system_y,
    "alg-woodworking-shop-system": alg_woodworking_shop_system,
    "alg-intersection-point-constants-sum": alg_intersection_point_constants_sum,
    "alg-system-k-two-places-infinite": alg_system_k_two_places_infinite,
    "alg-proportional-system-a-plus-b": alg_proportional_system_a_plus_b,
    "alg-farm-stand-baskets-difference": alg_farm_stand_baskets_difference,
    "alg-inequality-flip-sign-easy": alg_inequality_flip_sign_easy,
    "alg-garden-club-budget-inequality": alg_garden_club_budget_inequality,
    "alg-inequality-bound-c": alg_inequality_bound_c,
    "alg-point-x5-y-range": alg_point_x5_y_range,
    "alg-inequality-coefficient-k-flip": alg_inequality_coefficient_k_flip,
    "alg-parallel-strip-combination": alg_parallel_strip_combination,
    "alg-two-jobs-least-hours": alg_two_jobs_least_hours,
    "alg-shelf-inequality-point-meaning": alg_shelf_inequality_point_meaning,
    # batch batch5-psda
    "psda-oven-loaves-two-hours": psda_oven_loaves_two_hours,
    "psda-sprinkler-lawn-minutes": psda_sprinkler_lawn_minutes,
    "psda-scooter-fleet-percent-increase": psda_scooter_fleet_percent_increase,
    "psda-markup-discount-profit-p": psda_markup_discount_profit_p,
    "psda-flaws-mean-minus-median": psda_flaws_mean_minus_median,
    "psda-scaled-shifted-data-set": psda_scaled_shifted_data_set,
    "psda-tidal-pool-quadratic-fit": psda_tidal_pool_quadratic_fit,
    "psda-newsletter-linear-vs-exponential": psda_newsletter_linear_vs_exponential,
    "psda-tokens-not-red": psda_tokens_not_red,
    "psda-workshop-book-conditional": psda_workshop_book_conditional,
    "psda-fish-mass-sample-mean": psda_fish_mass_sample_mean,
    "psda-bicycle-survey-generalize": psda_bicycle_survey_generalize,
    # batch batch5-geo
    "geo-cone-radius-tripled-volume": geo_cone_radius_tripled_volume,
    "geo-pyramid-bin-height-perimeter": geo_pyramid_bin_height_perimeter,
    "geo-cone-cup-to-cylinder-height": geo_cone_cup_to_cylinder_height,
    "geo-isosceles-vertex-to-base-angle": geo_isosceles_vertex_to_base_angle,
    "geo-isosceles-nested-angle-dac": geo_isosceles_nested_angle_dac,
    "geo-similar-triangles-solve-x-side": geo_similar_triangles_solve_x_side,
    "geo-garden-diagonal-path-cosine": geo_garden_diagonal_path_cosine,
    "geo-sin-4x-cos-x-complement": geo_sin_4x_cos_x_complement,
    "geo-30-60-90-area-hypotenuse": geo_30_60_90_area_hypotenuse,
    "geo-tangent-point-distance-center": geo_tangent_point_distance_center,
    "geo-sector-area-radians-diameter": geo_sector_area_radians_diameter,
    "geo-circle-general-form-top-point": geo_circle_general_form_top_point,
    # batch batch5-advmath
    "adv-radical-simplify-even-power": adv_radical_simplify_even_power,
    "adv-poly-multiply-binomial-trinomial": adv_poly_multiply_binomial_trinomial,
    "adv-rational-undefined-values-sum": adv_rational_undefined_values_sum,
    "adv-long-division-quadratic-divisor": adv_long_division_quadratic_divisor,
    "adv-rational-subtract-factor-denominator": adv_rational_subtract_factor_denominator,
    "adv-radical-product-rational-exponent": adv_radical_product_rational_exponent,
    "adv-difference-squares-quartic-ab": adv_difference_squares_quartic_ab,
    "adv-square-equals-constant-greater-root": adv_square_equals_constant_greater_root,
    "adv-two-parabolas-no-common-point": adv_two_parabolas_no_common_point,
    "adv-two-parabolas-tangent-y-coordinate": adv_two_parabolas_tangent_y_coordinate,
    "adv-pendulum-solve-for-length": adv_pendulum_solve_for_length,
    "adv-two-real-solutions-least-integer-k": adv_two_real_solutions_least_integer_k,
    "adv-two-parabolas-tangent-k": adv_two_parabolas_tangent_k,
    "adv-exponential-difference-common-factor": adv_exponential_difference_common_factor,
    "adv-message-board-posts-weeks": adv_message_board_posts_weeks,
    "adv-video-views-exponential-model": adv_video_views_exponential_model,
    "adv-distinct-intercepts-multiplicity": adv_distinct_intercepts_multiplicity,
    "adv-coin-value-monthly-function": adv_coin_value_monthly_function,
    "adv-photo-frame-uniform-width": adv_photo_frame_uniform_width,
    "adv-quartic-end-behavior-factored": adv_quartic_end_behavior_factored,
    # batch batch5-algebra
    "alg-distribute-both-sides-solve": alg_distribute_both_sides_solve,
    "alg-bookstore-split-copies": alg_bookstore_split_copies,
    "alg-fraction-difference-solve-spr": alg_fraction_difference_solve_spr,
    "alg-no-solution-two-constants-grid": alg_no_solution_two_constants_grid,
    "alg-constant-both-sides-known-solution": alg_constant_both_sides_known_solution,
    "alg-evaluate-negative-input": alg_evaluate_negative_input,
    "alg-balloon-descent-initial-altitude": alg_balloon_descent_initial_altitude,
    "alg-printer-page-count-input-spr": alg_printer_page_count_input_spr,
    "alg-linear-constant-from-one-output": alg_linear_constant_from_one_output,
    "alg-warehouse-pallets-pair-meaning": alg_warehouse_pallets_pair_meaning,
    "alg-linear-constants-output-relation": alg_linear_constants_output_relation,
    "alg-linear-k-scaled-inputs-spr": alg_linear_k_scaled_inputs_spr,
    "alg-point-on-standard-line-k": alg_point_on_standard_line_k,
    "alg-recycling-coefficient-meaning": alg_recycling_coefficient_meaning,
    "alg-two-points-x-axis-crossing-spr": alg_two_points_x_axis_crossing_spr,
    "alg-perpendicular-line-equation": alg_perpendicular_line_equation,
    "alg-intercepts-relation-k-spr": alg_intercepts_relation_k_spr,
    "alg-system-sum-of-coordinates": alg_system_sum_of_coordinates,
    "alg-hardware-bolts-containers": alg_hardware_bolts_containers,
    "alg-system-count-solutions-coincident": alg_system_count_solutions_coincident,
    "alg-fraction-coefficient-system-x-spr": alg_fraction_coefficient_system_x_spr,
    "alg-parallel-unless-coincident-b": alg_parallel_unless_coincident_b,
    "alg-artist-prints-total-spr": alg_artist_prints_total_spr,
    "alg-greatest-value-simple-inequality": alg_greatest_value_simple_inequality,
    "alg-fundraiser-tickets-inequality": alg_fundraiser_tickets_inequality,
    "alg-point-system-inequalities-count-k": alg_point_system_inequalities_count_k,
    "alg-craft-fair-mugs-least": alg_craft_fair_mugs_least,
    "alg-compound-inequality-flip": alg_compound_inequality_flip,
    "alg-scaled-inequality-max": alg_scaled_inequality_max,
    "alg-fraction-inequality-k-bound": alg_fraction_inequality_k_bound,
    # batch batch6-psdaA
    "psda-coffee-beans-per-ounce": psda_b6pa_coffee_beans_per_ounce,
    "psda-road-map-towns-inches": psda_b6pa_road_map_towns_inches,
    "psda-truck-fuel-route": psda_b6pa_truck_fuel_route,
    "psda-direct-proportion-y-x": psda_b6pa_direct_proportion_y_x,
    "psda-map-scale-lakes-km": psda_b6pa_map_scale_lakes_km,
    "psda-train-kmh-to-mps": psda_b6pa_train_kmh_to_mps,
    "psda-carpet-square-yards-cost": psda_b6pa_carpet_square_yards_cost,
    "psda-sandbox-cubic-yards": psda_b6pa_sandbox_cubic_yards,
    "psda-wood-board-mass-kg": psda_b6pa_wood_board_mass_kg,
    "psda-trail-mix-almonds": psda_b6pa_trail_mix_almonds,
    "psda-soup-calories-liters": psda_b6pa_soup_calories_liters,
    "psda-painting-crew-days": psda_b6pa_painting_crew_days,
    "psda-download-megabits-minutes": psda_b6pa_download_megabits_minutes,
    "psda-ratio-chain-a-over-c": psda_b6pa_ratio_chain_a_over_c,
    "psda-club-juniors-ratio-change": psda_b6pa_club_juniors_ratio_change,
    "psda-fuel-efficiency-mpg": psda_b6pa_fuel_efficiency_mpg,
    "psda-tank-two-hoses-hours": psda_b6pa_tank_two_hoses_hours,
    "psda-blueprint-parking-space-area": psda_b6pa_blueprint_parking_space_area,
    "psda-faucet-drips-liters": psda_b6pa_faucet_drips_liters,
    "psda-three-part-ratio-sum": psda_b6pa_three_part_ratio_sum,
    "psda-percent-of-number": psda_b6pa_percent_of_number,
    "psda-recycling-households-p": psda_b6pa_recycling_households_p,
    "psda-grain-drying-original": psda_b6pa_grain_drying_original,
    "psda-double-increase-44": psda_b6pa_double_increase_44,
    "psda-chess-club-girls": psda_b6pa_chess_club_girls,
    "psda-monthly-sales-successive": psda_b6pa_monthly_sales_successive,
    # batch batch6-lf1
    "alg-lf-eval-two-thirds-coefficient": alg_lf_eval_two_thirds_coefficient,
    "alg-lf-input-for-negative-output": alg_lf_input_for_negative_output,
    "alg-lf-slope-through-two-points": alg_lf_slope_through_two_points,
    "alg-lf-scaled-output-known-value": alg_lf_scaled_output_known_value,
    "alg-lf-campsite-temperature-rate": alg_lf_campsite_temperature_rate,
    "alg-lf-rule-from-slope-and-intercept": alg_lf_rule_from_slope_and_intercept,
    "alg-lf-combined-outputs-value": alg_lf_combined_outputs_value,
    "alg-lf-table-x-intercept-spr": alg_lf_table_x_intercept_spr,
    "alg-lf-two-intercepts-evaluate": alg_lf_two_intercepts_evaluate,
    "alg-lf-point-slope-form-intercept": alg_lf_point_slope_form_intercept,
    "alg-lf-input-shift-rule": alg_lf_input_shift_rule,
    "alg-lf-table-y-intercept": alg_lf_table_y_intercept,
    "alg-lf-sum-of-constants-two-points": alg_lf_sum_of_constants_two_points,
    "alg-lf-generator-fuel-factored": alg_lf_generator_fuel_factored,
    "alg-lf-snow-depth-model": alg_lf_snow_depth_model,
    "alg-lf-pool-depth-minutes": alg_lf_pool_depth_minutes,
    "alg-lf-delivery-truck-point-meaning": alg_lf_delivery_truck_point_meaning,
    "alg-lf-scaled-shifted-x-intercept": alg_lf_scaled_shifted_x_intercept,
    "alg-lf-horizontal-shift-constant": alg_lf_horizontal_shift_constant,
    "alg-lf-intersection-y-coordinate": alg_lf_intersection_y_coordinate,
    "alg-lf-verbal-rates-double-output": alg_lf_verbal_rates_double_output,
    "alg-lf-two-plants-height-gap": alg_lf_two_plants_height_gap,
    "alg-lf-sunflower-lagged-height": alg_lf_sunflower_lagged_height,
    "alg-lf-tree-doubles-height": alg_lf_tree_doubles_height,
    "alg-lf-workshop-mugs-cheaper": alg_lf_workshop_mugs_cheaper,
    "alg-lf-scaled-function-from-slope": alg_lf_scaled_function_from_slope,
    "alg-lf-output-equals-input": alg_lf_output_equals_input,
    "alg-lf-vertical-shift-through-point": alg_lf_vertical_shift_through_point,
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
    import argparse, importlib.util
    ap = argparse.ArgumentParser(description="Recompute every item key with SymPy and compare with items.ts")
    ap.add_argument("--items", type=Path, default=ITEMS_TS, help="path to an items .ts file (default: web/content/items.ts)")
    ap.add_argument("--checks", type=Path, action="append", default=[],
                    help="extra Python module(s) defining CHECKS = {item_id: fn}; used by batch files before merge")
    ap.add_argument("--only-extra", action="store_true", help="verify only the ids registered in --checks modules")
    args = ap.parse_args()
    checks = dict(CHECKS)
    extra_ids: set[str] = set()
    for mod_path in args.checks:
        spec = importlib.util.spec_from_file_location(mod_path.stem, mod_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        checks.update(mod.CHECKS)
        extra_ids.update(mod.CHECKS)
    items = parse_items(args.items.read_text(encoding="utf-8"))
    if args.only_extra:
        items = [i for i in items if i["id"] in extra_ids]
    failures = 0
    print(f"{'id':34} {'dom':14} {'fmt':4} {'diff':6} {'route':15} status  detail")
    for item in items:
        compute = checks.get(item["id"])
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

    unknown = sorted(set(checks) - {i["id"] for i in items})
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
