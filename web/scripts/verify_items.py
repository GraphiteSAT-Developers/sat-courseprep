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


# ----- Batch batch6-ee1 -----
#!/usr/bin/env python3
"""SymPy checks for batch batch6-ee1 (web/content/batches/batch6-ee1.ts).

Run from the repo root, against a temp items.ts that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch6_ee1.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers. Every key is derived from the stem's
givens, not restated.
"""



import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, sqrt, Eq


x, y, a, b, c, d, h, k = symbols("x y a b c d h k")


def _b6ee_expr_check(expected, samples, label=""):
    """MC with expression choices: exactly the key equals `expected` at every sample point."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            try:
                expr = latex_to_sympy_ext(ch)
            except Exception as e:  # noqa: BLE001
                return False, f"could not parse choice {i} {ch!r}: {e}"
            if all(abs(complex((expr - expected).subs(s).evalf())) < 1e-9 for s in samples):
                matches.append(i)
        return matches == [idx], f"{label or expected}; matching choices {matches}, key index {idx}"

    return check


def _b6ee_coeffs(identity, unknowns):
    """Solve a polynomial identity in x (expression == 0 for all x) for the unknown constants."""
    eqs = sp.Poly(sp.expand(identity), x).all_coeffs()
    return sp.solve(eqs, unknowns, dict=True)


_B6EE_X = [{x: v} for v in (Rational(1, 3), Rational(3, 2), Rational(7, 2), 5, 7, 11)]
_B6EE_XPOS = [{x: v} for v in (Rational(1, 4), Rational(2, 3), 2, 5, 9)]
_B6EE_XY = [{x: xv, y: yv} for xv, yv in ((1, 2), (3, Rational(-1, 2)), (Rational(2, 5), 4), (-3, 7))]


# ---------------------------------------------------------------- easy


def adv_gcf_monomial_three_terms():
    expr = 15 * x**4 - 10 * x**3 + 5 * x**2
    g = sp.gcd_terms(expr)
    assert sp.expand(g - expr) == 0
    return _b6ee_expr_check(expr, _B6EE_X, label="15x^4 - 10x^3 + 5x^2")


def adv_poly_add_two_variable():
    expr = sp.expand((4 * x**2 - 3 * x * y + y**2) + (-(x**2) + 5 * x * y - 6 * y**2))
    return _b6ee_expr_check(expr, _B6EE_XY, label=str(expr))


def adv_power_of_monomial():
    expr = sp.expand((2 * x**3) ** 4)
    return _b6ee_expr_check(expr, _B6EE_X, label=str(expr))


def adv_rational_exponent_to_radical():
    xp = Symbol("x", positive=True)
    assert sp.simplify(xp ** Rational(2, 5) - sp.root(xp**2, 5)) == 0
    return _b6ee_expr_check(x ** Rational(2, 5), _B6EE_XPOS, label="x^(2/5) for x > 0")


def adv_mural_area_product():
    expr = sp.expand((2 * x + 3) * (x + 5))
    return _b6ee_expr_check(expr, _B6EE_X, label=f"area {expr}")


# ---------------------------------------------------------------- medium


def adv_gcf_then_difference_squares():
    expr = 3 * x**3 - 48 * x
    assert sp.factor(expr) == 3 * x * (x - 4) * (x + 4)
    return _b6ee_expr_check(expr, _B6EE_X, label="3x^3 - 48x")


def adv_trinomial_leading_ten():
    expr = 10 * x**2 - 11 * x - 6
    assert sp.factor(expr) == (5 * x + 2) * (2 * x - 3)
    return _b6ee_expr_check(expr, _B6EE_X, label="10x^2 - 11x - 6")


def adv_grouping_cubic_four_terms():
    expr = x**3 - 5 * x**2 - 4 * x + 20
    assert sp.factor(expr) == (x - 5) * (x - 2) * (x + 2)
    return _b6ee_expr_check(expr, _B6EE_X, label="x^3 - 5x^2 - 4x + 20")


def adv_complete_square_leading_two_k():
    sols = _b6ee_coeffs(2 * x**2 + 6 * x + 5 - (2 * (x + h) ** 2 + k), [h, k])
    assert len(sols) == 1
    return sols[0][k]


def adv_rational_add_unlike_denominators():
    expr = sp.together(3 / x + 2 / (x + 4))
    return _b6ee_expr_check(expr, _B6EE_X, label=f"sum {expr}")


def adv_rational_multiply_cancel_monomial():
    expr = sp.cancel((x**2 - 25) / (3 * x) * (6 * x**2) / (x + 5))
    assert sp.expand(expr - 2 * x * (x - 5)) == 0
    return _b6ee_expr_check(expr, _B6EE_X, label=f"product {expr}")


def adv_negative_exponent_quotient():
    expr = sp.simplify((3 * x**-2 * y**3) ** 2 / (x**-5 * y))
    assert sp.simplify(expr - 9 * x * y**5) == 0
    return _b6ee_expr_check(expr, _B6EE_XY, label=str(expr))


def adv_revenue_vertex_form():
    expr = -5 * x**2 + 150 * x
    vx = sp.solve(sp.diff(expr, x), x)[0]
    assert (vx, expr.subs(x, vx)) == (15, 1125)
    return _b6ee_expr_check(expr, _B6EE_X, label="-5x^2 + 150x")


def adv_cubic_product_coefficient_c():
    sols = _b6ee_coeffs((3 * x - 4) * (x**2 + 2 * x - 5) - (a * x**3 + b * x**2 + c * x + d), [a, b, c, d])
    return sols[0][c]


def adv_banner_perimeter_factor():
    length, rem = sp.div(6 * x**2 + 23 * x + 20, 2 * x + 5, x)
    assert rem == 0
    perim = sp.expand(2 * length + 2 * (2 * x + 5))
    return _b6ee_expr_check(perim, _B6EE_X, label=f"length {length}, perimeter {perim}")


# ---------------------------------------------------------------- hard


def adv_tilde_recentered_b():
    sols = _b6ee_coeffs(a * (x + 2) ** 2 + b * (x + 2) + c - (3 * x**2 + 5 * x - 1), [a, b, c])
    assert len(sols) == 1
    return sols[0][b]


def adv_rational_exponent_coefficient_quotient():
    xp = Symbol("x", positive=True)
    expr = sp.simplify((8 * xp**3) ** Rational(2, 3) / sqrt(16 * xp))
    assert sp.simplify(expr - xp ** Rational(3, 2)) == 0
    return _b6ee_expr_check(expr.subs(xp, x), _B6EE_XPOS, label=f"simplifies to {expr}")


def adv_complete_square_unknown_k():
    sols = _b6ee_coeffs(x**2 - 6 * k * x + 50 - ((x - h) ** 2 + 14), [h, k])
    pos = [s for s in sols if s[h] > 0 and s[k] > 0]
    assert len(sols) == 2 and len(pos) == 1
    return pos[0][k]


def adv_rational_binomial_ratio_difference():
    expr = sp.cancel((x + 1) / (x - 1) - (x - 1) / (x + 1))
    return _b6ee_expr_check(expr, _B6EE_X, label=f"difference {expr}")


def adv_quartic_quadratic_form_a():
    sols = _b6ee_coeffs(x**4 - 13 * x**2 + 36 - (x - a) * (x + a) * (x - b) * (x + b), [a, b])
    ok = [s for s in sols if s[a].is_real and s[b].is_real and s[a] > s[b] > 0]
    assert len(ok) == 1
    return ok[0][a]


def adv_patio_gravel_border_k():
    sols = _b6ee_coeffs((x + 2 * k) ** 2 - x**2 - (20 * x + 100), [k])
    pos = [s[k] for s in sols if s[k] > 0]
    assert len(pos) == 1
    return pos[0]


def adv_rational_product_four_factors():
    expr = sp.cancel((2 * x**2 + 5 * x - 3) / (x**2 - 9) * (x - 3) / (4 * x**2 - 1))
    assert sp.simplify(expr - 1 / (2 * x + 1)) == 0
    samples = [{x: v} for v in (Rational(7, 2), 4, 5, 9, 20)]  # stem restricts x > 3
    return _b6ee_expr_check(expr, samples, label=f"product {expr}")


def adv_exponent_difference_squares_a_minus_b():
    sols = sp.solve([Eq(a**2 - b**2, 32), Eq(a + b, 4)], [a, b], dict=True)
    assert len(sols) == 1
    xs = Symbol("xs", positive=True)
    s0 = sols[0]
    assert sp.simplify(xs ** (s0[a] ** 2) / xs ** (s0[b] ** 2) - xs**32) == 0
    return s0[a] - s0[b]


def adv_radical_perfect_square_negative_x():
    expr = sqrt(x**2 + 6 * x + 9)
    samples = [{x: v} for v in (-4, Rational(-9, 2), -5, Rational(-15, 2), -10)]  # stem restricts x < -3
    for s in samples:
        assert expr.subs(s) == -(s[x]) - 3
    return _b6ee_expr_check(expr, samples, label="sqrt((x+3)^2) = -x - 3 for x < -3")


# ----- Batch batch6-av -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch6-av.ts (batch batch6-av, Area and volume).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch6_av.py --only-extra

Each function derives the key from the stem's givens and returns it as an exact
SymPy object (or a callable for choices the base parser cannot read). Values stay
exact (pi, sqrt) until a stem asks for rounding.
"""



import sympy as sp
from sympy import Eq, Integer, Rational, pi, sqrt, symbols

_b6av_x, _b6av_h, _b6av_r, _b6av_w, _b6av_A = symbols("_b6av_x _b6av_h _b6av_r _b6av_w _b6av_A", positive=True)


def _b6av_pos_root(eq, var):
    sols = [v for v in sp.solve(eq, var) if v.is_real and v > 0]
    assert len(sols) == 1, sols
    return sols[0]


def _b6av_cone_volume(r, h):
    return Rational(1, 3) * pi * r**2 * h


def _b6av_cyl_volume(r, h):
    return pi * r**2 * h


def geo_trapezoid_parallel_sides_area():
    return Rational(1, 2) * (7 + 13) * 6


def geo_parallelogram_slanted_side_area():
    base, height = 15, 8  # the 9-unit side is slanted and unused
    return Integer(base * height)


def geo_triangle_altitude_from_area():
    return _b6av_pos_root(Eq(Rational(1, 2) * 12 * _b6av_h, 54), _b6av_h)


def geo_sphere_volume_from_diameter():
    r = Rational(6, 2)
    return Rational(4, 3) * pi * r**3


def geo_rectangular_pyramid_volume():
    return Rational(1, 3) * (5 * 8) * 9


def geo_cone_cylinder_equal_volume_height():
    return _b6av_pos_root(Eq(_b6av_cone_volume(_b6av_r, _b6av_h), _b6av_cyl_volume(_b6av_r, 5)), _b6av_h)


def geo_square_inscribed_circle_region():
    side = 10
    r = Rational(side, 2)
    return side**2 - pi * r**2


def geo_cylinder_total_surface_area():
    r, h = 3, 7
    return 2 * pi * r**2 + 2 * pi * r * h


def geo_cone_height_from_diameter_volume():
    return _b6av_pos_root(Eq(_b6av_cone_volume(Rational(12, 2), _b6av_h), 96 * pi), _b6av_h)


def geo_cone_half_radius_triple_height():
    new = _b6av_cone_volume(_b6av_r / 2, 3 * _b6av_h)
    return sp.simplify(new / _b6av_cone_volume(_b6av_r, _b6av_h))


def geo_cylinder_height_equals_diameter():
    r = _b6av_pos_root(Eq(_b6av_cyl_volume(_b6av_r, 2 * _b6av_r), 500), _b6av_r)
    assert abs(float(r) - 4.301) < 0.001
    return _nearest(r, 1)


def geo_square_corners_octagon_area():
    return Integer(12**2) - 4 * Rational(1, 2) * 4 * 4


def geo_hollow_tube_material_volume():
    return _b6av_cyl_volume(5, 10) - _b6av_cyl_volume(3, 10)


def geo_hemisphere_dome_volume():
    v = Rational(1, 2) * Rational(4, 3) * pi * 15**3
    return _nearest(v, 0)


def geo_tank_fill_time_minutes():
    v = _b6av_cyl_volume(Rational(3, 2), 4)
    return _nearest(v / Rational(1, 5), 0)


def geo_stage_area_square_centimeters():
    return Rational(45, 10) * 100 * 6 * 100


def geo_wall_paint_quarts():
    return Rational(14 * 9 - 5 * 3, 37)


def geo_channel_trapezoid_volume():
    return Rational(1, 2) * (3 + 1) * Rational(3, 2) * 50


def geo_cylinder_percent_volume_change():
    ratio = _b6av_cyl_volume(Rational(3, 2) * _b6av_r, Rational(4, 5) * _b6av_h) / _b6av_cyl_volume(_b6av_r, _b6av_h)
    return sp.simplify((ratio - 1) * 100)


def geo_equilateral_perimeter_area():
    side = Rational(18, 3)
    altitude = sqrt(side**2 - (side / 2) ** 2)
    expected = Rational(1, 2) * side * altitude

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        good = [i for i, v in enumerate(vals) if sp.simplify(v - expected) == 0]
        return good == [idx], f"expected {expected}; matching choices {good}"

    return check


def geo_square_pyramid_total_surface():
    side, height = 10, 12
    slant = sqrt(height**2 + Rational(side, 2) ** 2)
    return side**2 + 4 * Rational(1, 2) * side * slant


def geo_cylinder_volume_lateral_radius():
    sol = sp.solve([Eq(_b6av_cyl_volume(_b6av_r, _b6av_h), 245 * pi), Eq(2 * pi * _b6av_r * _b6av_h, 70 * pi)],
                   [_b6av_r, _b6av_h], dict=True)
    assert len(sol) == 1, sol
    return sol[0][_b6av_r]


def geo_cylinder_volume_27_surface_area():
    k = _b6av_pos_root(Eq(_b6av_x**3, 27), _b6av_x)
    return k**2 * 96 * pi


def geo_rectangle_scaled_area_difference():
    return _b6av_pos_root(Eq(Rational(3, 2) ** 2 * _b6av_A - _b6av_A, 54), _b6av_A)


def geo_triangle_two_altitudes_side():
    area = Rational(1, 2) * 15 * 8
    bc = _b6av_pos_root(Eq(Rational(1, 2) * _b6av_x * 12, area), _b6av_x)
    # The triangle exists: place A=(0,0), B=(15,0), C=(xc, 8) with BC = bc.
    xc = 15 - sqrt(bc**2 - 8**2)
    ac_line_dist = sp.Abs(8 * 0 - 8 * 15 + 0) / sqrt(8**2 + (xc - 15) ** 2)  # distance from A to line BC
    assert sp.simplify(ac_line_dist - 12) == 0
    return bc


def geo_open_box_greatest_volume():
    xx = sp.Symbol("_b6av_xx", real=True)
    v = xx * (16 - 2 * xx) * (10 - 2 * xx)
    crit = [c for c in sp.solve(sp.diff(v, xx), xx) if 0 < c < 5]
    candidates = [v.subs(xx, c) for c in crit]
    best = max(candidates)
    assert sp.factor(sp.expand(v - best)) == 4 * (xx - 2) ** 2 * (xx - 9)
    return best


def geo_salt_pile_cone_circumference():
    r = _b6av_pos_root(Eq(2 * pi * _b6av_r, 40), _b6av_r)
    return _nearest(_b6av_cone_volume(r, 6), 0)


def geo_garden_path_uniform_width():
    w = _b6av_pos_root(Eq(pi * (6 + _b6av_w) ** 2 - pi * 6**2, 40), _b6av_w)
    assert abs(float(w) - 0.981) < 0.001
    return _nearest(w, 1)


def geo_similar_candles_wax():
    k = _b6av_pos_root(Eq(_b6av_x**2, Rational(9, 4)), _b6av_x)
    return k**3 * 16


def geo_planter_soil_bags():
    vol_ft3 = 4 * Rational(30, 12) * Rational(18, 12)
    bags = vol_ft3 / Rational(5, 4)
    return sp.ceiling(bags)


# ----- Batch batch6-ne1 -----
import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, sqrt, Eq

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")

_B6NE_WORDS = {0: "Zero", 1: "Exactly one", 2: "Exactly two"}


def _b6ne_real_roots(expr, var=x):
    """Distinct real roots of an expression (polynomial or rational) in var."""
    vr = Symbol(str(var), real=True)
    return sorted(set(sp.solve(expr.subs(var, vr), vr)))


def _b6ne_count_check(count):
    def check(choices, idx):
        return choices[idx] == _B6NE_WORDS[count], f"{count} real solution(s) -> '{_B6NE_WORDS[count]}'"

    return check


def adv_trinomial_larger_root_factor():
    return max(_b6ne_real_roots(x**2 - 13 * x + 36))


def adv_square_isolate_positive_x():
    return [v for v in _b6ne_real_roots(3 * x**2 + 5 - 80) if v > 0][0]


def adv_factored_cubic_least_solution():
    return min(_b6ne_real_roots(x * (x + 6) * (3 * x - 2)))


def adv_exponential_power_of_two_easy():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(2 ** (xr - 1), 32), xr)
    assert len(sols) == 1
    return sols[0]


def adv_absolute_value_negative_zero_solutions():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(sp.Abs(2 * xr + 5) + 7, 3), xr)
    return _b6ne_count_check(len(sols))


def adv_rug_room_floor_strip():
    sols = [v for v in _b6ne_real_roots((x + 6) ** 2 - 324) if v > 0]
    assert len(sols) == 1
    return sols[0]


def adv_quadratic_formula_positive_radical():
    pos = [v for v in _b6ne_real_roots(x**2 + 4 * x - 6) if v > 0]
    assert len(pos) == 1

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        matches = [i for i, v in enumerate(vals) if sp.simplify(v - pos[0]) == 0]
        return matches == [idx], f"expected {pos[0]}; matching choices {matches}"

    return check


def adv_product_of_solutions_noninteger():
    roots = _b6ne_real_roots(3 * x**2 - 10 * x - 4)
    assert len(roots) == 2
    return sp.simplify(roots[0] * roots[1])


def adv_rational_common_denominator_extraneous():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq((xr**2 + 3 * xr) / (xr + 5), 10 / (xr + 5)), xr)
    sols = [v for v in sols if v != -5]
    assert len(sols) == 1
    return sols[0]


def adv_radical_equals_x_extraneous():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(sp.sqrt(5 * xr + 6), xr), xr)
    assert len(sols) == 1
    return sols[0]


def adv_line_parabola_y_difference():
    sols = sp.solve([Eq(y, 2 * x - 1), Eq(y, x**2 - 4 * x + 4)], [x, y], dict=True)
    assert len(sols) == 2
    sols.sort(key=lambda d: d[x])
    return sols[1][y] - sols[0][y]


def adv_exponential_product_same_base():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(3**xr * 9 ** (xr + 1), 3**11), xr)
    assert len(sols) == 1
    return sols[0]


def adv_circle_line_which_point():
    sols = sp.solve([Eq((x - 2) ** 2 + (y + 1) ** 2, 25), Eq(y, x - 2)], [x, y], dict=True)
    pts = {(d[x], d[y]) for d in sols}
    assert len(pts) == 2

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            inner = ch.strip().strip("$").strip("()")
            px, py = (latex_to_sympy(v) for v in inner.split(","))
            if (px, py) in pts:
                hits.append(i)
        return hits == [idx], f"intersection points {pts}; matching choices {hits}"

    return check


def adv_discriminant_zero_rearranged():
    expr = 4 * x**2 + 9 - 12 * x
    assert sp.discriminant(expr, x) == 0
    return _b6ne_count_check(len(_b6ne_real_roots(expr)))


def adv_biquadratic_real_solution_count():
    return Integer(len(_b6ne_real_roots(x**4 - 5 * x**2 - 36)))


def adv_tossed_ball_second_time():
    roots = _b6ne_real_roots(-5 * t**2 + 20 * t + Rational(18, 10) - Rational(168, 10), t)
    assert len(roots) == 2
    return max(roots)


def adv_raffle_price_revenue():
    roots = [v for v in _b6ne_real_roots(p * (200 - 10 * p) - 750, p) if v > 0 and 200 - 10 * v > 0]
    assert len(roots) == 2
    return max(roots)


def adv_horizon_distance_radical():
    hr = Symbol("h", nonnegative=True)
    sols = sp.solve(Eq(Rational(36, 10) * sp.sqrt(hr), 18), hr)
    assert len(sols) == 1
    return sols[0]


def adv_drone_distance_absolute_value():
    tr = Symbol("t", real=True)
    sols = [v for v in sp.solve(Eq(sp.Abs(3 * tr - 45), 15), tr) if 0 <= v <= 30]
    assert len(sols) == 2
    return max(sols)


def adv_two_machines_rational_time():
    roots = [v for v in _b6ne_real_roots(1 / x + 1 / (x + 3) - Rational(1, 2)) if v > 0]
    assert len(roots) == 1
    return roots[0]


def adv_stopping_distance_speed():
    v = Symbol("v", positive=True)
    sols = sp.solve(Eq(v**2 / 20 + v, 120), v)
    assert len(sols) == 1
    return sols[0]


def adv_two_parabolas_greatest_integer_k():
    good = []
    for kv in range(-50, 51):
        if len(_b6ne_real_roots(x**2 + kv - (-(x**2) + 6 * x))) == 2:
            good.append(kv)
    return Integer(max(good))


def adv_factored_cubic_two_distinct_c():
    good = []
    for cv in [Rational(i, 4) for i in range(-400, 401)]:
        if cv != 0 and len(_b6ne_real_roots(x * (x**2 - 6 * x + cv))) == 2:
            good.append(cv)
    assert len(good) == 1
    return good[0]


def adv_absolute_value_line_one_solution_c():
    xr = Symbol("x", real=True)

    def count(cv):
        return len(sp.solve(Eq(sp.Abs(xr - 3), xr / 2 + cv), xr))

    good = [cv for cv in [Rational(i, 4) for i in range(-40, 41)] if count(cv) == 1]
    assert len(good) == 1
    return good[0]


def adv_double_radical_equation():
    xr = Symbol("x", nonnegative=True)
    sols = sp.solve(Eq(sp.sqrt(xr + 7), sp.sqrt(xr) + 1), xr)
    assert len(sols) == 1
    return sols[0]


def adv_rational_all_extraneous_zero():
    expr = x / (x + 2) + 8 / (x**2 - 4) - 2 / (x - 2)
    cands = _b6ne_real_roots(sp.numer(sp.together(expr)))
    sols = [v for v in cands if v not in (2, -2)]
    return _b6ne_count_check(len(sols))


def adv_line_circle_tangent_intercept_b():
    bp = Symbol("b", positive=True)
    disc = sp.discriminant(sp.expand(x**2 + (3 * x + bp) ** 2 - 10), x)
    sols = sp.solve(disc, bp)
    assert len(sols) == 1
    return sols[0]


def adv_parabola_line_no_intersection_k():
    good = [kv for kv in range(-50, 51) if len(_b6ne_real_roots(x**2 - 5 * x + 2 - (x + kv))) == 0]
    return Integer(max(good))


def adv_root_twice_other_c():
    sol = sp.solve([Eq(r + 2 * r, 9), Eq(c, r * 2 * r)], [r, c], dict=True)
    assert len(sol) == 1
    cv = sol[0][c]
    roots = _b6ne_real_roots(x**2 - 9 * x + cv)
    assert len(roots) == 2 and roots[1] == 2 * roots[0]
    return cv


def adv_exponential_quadratic_in_two_power():
    xr = Symbol("x", real=True)
    sols = sp.solve(Eq(4**xr - 3 * 2 ** (xr + 1) + 8, 0), xr)
    assert len(sols) == 2
    return sum(sols)


def adv_absolute_value_steep_line_count():
    xr = Symbol("x", real=True)
    counts = set()
    for cv in [Rational(i, 3) for i in range(-90, 91)]:
        counts.add(len(sp.solve(Eq(sp.Abs(xr - 4), 2 * xr + cv), xr)))

    def check(choices, idx):
        ok = counts == {1} and "exactly one real solution for every value" in choices[idx]
        return ok, f"solution counts over sampled c: {counts}"

    return check


# ----- Batch batch7-psdaB -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch7-psdaB.ts (Percentages; One-variable data).

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch7_psdaB.py --only-extra

Each function derives the key from the stem's givens and returns it as an exact
SymPy object, or a callable (choices, idx) -> (ok, detail) for percent or
sentence choices.
"""

from itertools import combinations_with_replacement


import sympy as sp
from sympy import Eq, Integer, Rational, symbols, sqrt

_b7pb_x = symbols("_b7pb_x")


def _b7pb_mean(values):
    return Rational(sum(values), len(values))


def _b7pb_median(values):
    v = sorted(values)
    m = len(v)
    return Rational(v[m // 2]) if m % 2 else Rational(v[m // 2 - 1] + v[m // 2], 2)


def _b7pb_sd(values):
    mu = _b7pb_mean(values)
    return sqrt(sum((Rational(v) - mu) ** 2 for v in values) / len(values))


def _b7pb_expand(freq):
    return [v for v, f in freq for _ in range(f)]


def _b7pb_numeric(expected):
    """Choices may carry \\%; exactly the key choice must equal expected."""

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if sp.simplify(latex_to_sympy_ext(ch) - expected) == 0]
        return matches == [idx], f"expected {expected}; matching choices {matches}, key index {idx}"

    return check


def _b7pb_sentence(expected):
    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if ch.strip() == expected]
        return matches == [idx], f"expected '{expected}'; matching choices {matches}"

    return check


def _b7pb_pos_root(eq):
    sols = [v for v in sp.solve(eq, _b7pb_x) if v.is_real and v > 0]
    assert len(sols) == 1, sols
    return sols[0]


def _b7pb_change(before, after, word_same="remains the same"):
    if after > before:
        return "increases"
    if after < before:
        return "decreases"
    return word_same


# ----- Percentages ----------------------------------------------------------


def psda_orchard_young_apple_percent():
    return _b7pb_numeric(Rational(60, 400) * 100)


def psda_scale_reading_percent_error():
    return Rational(520 - 494, 520) * 100


def psda_helmet_price_before_tax():
    return _b7pb_pos_root(Eq(Rational(106, 100) * _b7pb_x, Rational(6360, 100)))


def psda_pond_fish_three_year_chain():
    return _b7pb_numeric(Rational(120, 100) * Rational(75, 100) * Rational(110, 100) * 100)


def psda_a_b_c_percent_chain():
    c = Integer(1)
    b = Rational(150, 100) * c
    a = Rational(40, 100) * b
    return a / c * 100


def psda_machine_value_depreciation():
    v = Integer(18000)
    for _ in range(3):
        v -= Rational(10, 100) * v
    return v


def psda_store_hardcover_fiction_share():
    fiction_hc = Rational(40, 100) * Rational(30, 100)
    nonfiction_hc = Rational(60, 100) * Rational(60, 100)
    return fiction_hc / (fiction_hc + nonfiction_hc) * 100


def psda_notebook_price_revenue():
    return (Rational(125, 100) * (1 - Rational(16, 100)) - 1) * 100


def psda_rug_prices_chain_difference():
    c = _b7pb_x
    b = (1 - Rational(20, 100)) * c
    a = (1 + Rational(30, 100)) * b
    return _b7pb_pos_root(Eq(a - c, Rational(240, 100)))


def psda_deposit_two_year_rate():
    return _b7pb_pos_root(Eq(5000 * (1 + _b7pb_x / 100) ** 2, 5832))


# ----- One-variable data -----------------------------------------------------


def psda_homework_minutes_median():
    return _b7pb_median([34, 18, 27, 45, 22, 30, 41, 25])


def psda_pets_dot_plot_range():
    data = _b7pb_expand([(0, 3), (1, 4), (2, 2), (3, 2), (6, 1)])
    assert len(data) == 12
    return max(data) - min(data)


def psda_missing_fifth_value_mean():
    return sp.solve(Eq((12 + 15 + 9 + 20 + _b7pb_x) / 5, 15), _b7pb_x)[0]


def psda_trips_frequency_median():
    data = _b7pb_expand([(1, 6), (2, 9), (3, 5), (4, 3), (5, 2)])
    assert len(data) == 25
    return _b7pb_median(data)


def psda_add_value_mean_median_amounts():
    before = [4, 7, 7, 9, 12, 15]
    after = before + [30]
    dm = _b7pb_mean(after) - _b7pb_mean(before)
    dmed = _b7pb_median(after) - _b7pb_median(before)
    med_text = "the median remains the same" if dmed == 0 else f"the median increases by {dmed}"
    return _b7pb_sentence(f"The mean increases by {dm}, and {med_text}.")


def psda_bakery_ovens_combined_mean():
    return _b7pb_mean([480] * 16 + [455] * 24)


def psda_race_time_recording_error():
    total = 10 * 52 - 61 + 47
    return Rational(total, 10)


def psda_fish_length_box_plot_iqr():
    q1, q3 = 24, 33
    return Integer(q3 - q1)


def psda_shifted_spread_sets_compare():
    A = _b7pb_expand([(10, 2), (11, 4), (12, 8), (13, 4), (14, 2)])
    B = _b7pb_expand([(20, 4), (21, 2), (22, 8), (23, 2), (24, 4)])
    assert len(A) == len(B) == 20
    mean_part = "The means are equal" if _b7pb_mean(A) == _b7pb_mean(B) else (
        "The mean of data set B is greater" if _b7pb_mean(B) > _b7pb_mean(A) else "The mean of data set A is greater")
    sa, sb = _b7pb_sd(A), _b7pb_sd(B)
    sd_part = "the standard deviations are equal" if sa == sb else (
        "the standard deviation of data set B is greater" if sb > sa else "the standard deviation of data set A is greater")
    return _b7pb_sentence(f"{mean_part}, and {sd_part}.")


def psda_mode_median_greatest_value():
    best = None
    # sorted 7-tuple of positive integers, sum 70, median 12, unique mode 14
    for low in combinations_with_replacement(range(1, 13), 3):
        for high in combinations_with_replacement(range(12, 71), 3):
            data = list(low) + [12] + list(high)
            if sum(data) != 70:
                continue
            counts = {v: data.count(v) for v in set(data)}
            top = max(counts.values())
            modes = [v for v, c in counts.items() if c == top]
            if modes != [14] or top < 2:
                continue
            best = max(best or 0, max(data))
    return Integer(best)


def psda_two_sections_size_from_mean():
    return _b7pb_pos_root(Eq(70 * (30 - _b7pb_x) + 85 * _b7pb_x, 76 * 30))


def psda_temperature_entry_error_effects():
    before = [82, 85, 86, 87, 88, 88, 90, 91, 93, 9]
    after = [82, 85, 86, 87, 88, 88, 90, 91, 93, 90]
    med = _b7pb_change(_b7pb_median(before), _b7pb_median(after))
    sd = _b7pb_change(_b7pb_sd(before), _b7pb_sd(after))
    return _b7pb_sentence(f"The median {med}, and the standard deviation {sd}.")


def psda_household_cars_added_mean():
    data = _b7pb_expand([(0, 5), (1, 14), (2, 13), (3, 6), (4, 2)])
    assert len(data) == 40
    return _b7pb_pos_root(Eq((sum(data) + 4 * _b7pb_x) / (40 + _b7pb_x), 2))


def psda_quiz_scores_correction_shift():
    # Any 11 distinct scores with median 74 behave the same; use a representative set.
    before = [50, 55, 60, 65, 70, 74, 78, 82, 86, 90, 95]
    after = sorted(before)
    after[-1] += 15
    after[0] -= 4
    assert _b7pb_median(before) == 74
    dm = _b7pb_mean(after) - _b7pb_mean(before)
    med_text = f"the median remains {_b7pb_median(after)}" if _b7pb_median(after) == 74 else f"the median increases by {_b7pb_median(after) - 74}"
    return _b7pb_sentence(f"The mean increases by {dm}, and {med_text}.")


def psda_rice_bags_added_at_mean():
    # Representative data: mean 500, population SD 4.
    before = [496] * 12 + [504] * 12
    assert _b7pb_mean(before) == 500 and _b7pb_sd(before) == 4
    after = before + [500, 500]
    mean = _b7pb_change(_b7pb_mean(before), _b7pb_mean(after))
    sd = _b7pb_change(_b7pb_sd(before), _b7pb_sd(after))
    return _b7pb_sentence(f"The mean {mean}, and the standard deviation {sd}.")


# ----- Batch batch7-ineq1 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch7-ineq1.ts (batch batch7-ineq1).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch7_ineq1.py --only-extra

Each function derives the answer from the stem's givens: a numeric result for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items
whose choices are inequalities, points or sentences.
"""

import re


import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")
m, f = symbols("m f")

_B7IQ_OPS = {"\\le": sp.Le, "\\ge": sp.Ge, "<": sp.Lt, ">": sp.Gt}


def _b7iq_rel(text: str):
    """'$3 \\le x < 6$' -> And(3 <= x, x < 6); '$y \\ge \\frac{3}{2}x - 2$' -> relational."""
    body = text.strip().strip("$")
    parts = re.split(r"(\\le|\\ge|<|>)", body)
    exprs = [latex_to_sympy(e) for e in parts[0::2]]
    ops = parts[1::2]
    rels = [_B7IQ_OPS[op](lhs, rhs) for op, lhs, rhs in zip(ops, exprs, exprs[1:])]
    return sp.And(*rels)


def _b7iq_point(text: str):
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip())


def _b7iq_same_set_1d(expected, var, grid):
    """Choices whose relation agrees with expected at every grid value of var."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = _b7iq_rel(ch)
            if all(bool(rel.subs(var, v)) == bool(expected.subs(var, v)) for v in grid):
                matches.append(i)
        return matches == [idx], f"expected {expected}; matching choices {matches}"

    return check


_B7IQ_GRID_1D = [Rational(i, 4) for i in range(-120, 121)]
_B7IQ_GRID_2D = [(Rational(i, 2), Rational(j, 2)) for i in range(-24, 25) for j in range(-24, 25)]


def _b7iq_count_ints(rel, var, lo=-200, hi=200):
    return Integer(sum(1 for i in range(lo, hi + 1) if bool(rel.subs(var, i))))


# ----- easy -----


def alg_ineq_collect_terms_easy():
    expected = sp.solve_univariate_inequality(sp.Lt(5 * x - 3, 2 * x + 9), x)
    return _b7iq_same_set_1d(expected, x, _B7IQ_GRID_1D)


def alg_ineq_which_value_solution():
    rel = sp.Gt(6 * x + 1, 4 * x + 11)

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if bool(rel.subs(x, latex_to_sympy(ch)))]
        return good == [idx], f"choices satisfying 6x + 1 > 4x + 11: {good}"

    return check


def alg_ineq_compound_middle_term():
    expected = sp.And(sp.Le(7, 4 * x - 5), sp.Lt(4 * x - 5, 19))
    return _b7iq_same_set_1d(expected, x, _B7IQ_GRID_1D)


def alg_ineq_point_standard_form():
    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            px, py = _b7iq_point(ch)
            if bool(sp.Ge(4 * px - 3 * py, 12)):
                good.append(i)
        return good == [idx], f"points satisfying 4x - 3y >= 12: {good}"

    return check


def alg_ineq_swimmer_weekly_distance():
    done, per, goal = 1200, 400, 3500
    expected = sp.Ge(done + per * p, goal)
    return _b7iq_same_set_1d(expected, p, list(range(0, 21)) + [Rational(i, 8) for i in range(0, 80)])


# ----- medium -----


def alg_ineq_least_integer_fraction_flip():
    sol = sp.solve_univariate_inequality(sp.Lt(5 - Rational(2, 3) * x, 1), x, relational=False)
    return Integer(min(i for i in range(-100, 101) if sol.contains(i)))


def alg_ineq_count_integers_chain():
    rel = sp.And(sp.Le(3 * (x - 2), 5 * x + 4), sp.Lt(5 * x + 4, 2 * x + 34))
    return _b7iq_count_ints(rel, x)


def alg_ineq_count_listed_points_system():
    pts = [(1, -5), (0, 3), (2, 2), (3, 2)]
    return Integer(sum(1 for px, py in pts if py > 3 * px - 8 and px + 2 * py < 7))


def alg_ineq_boundary_line_two_points():
    (x1, y1), (x2, y2) = (0, -2), (4, 4)
    slope = Rational(y2 - y1, x2 - x1)
    expected = sp.Ge(y, slope * (x - x1) + y1)  # on or above the line

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = _b7iq_rel(ch)
            if all(bool(rel.subs({x: u, y: v})) == bool(expected.subs({x: u, y: v})) for u, v in _B7IQ_GRID_2D):
                matches.append(i)
        return matches == [idx], f"expected {expected}; matching choices {matches}"

    return check


def alg_ineq_fractions_equivalent():
    expected = sp.solve_univariate_inequality(sp.Ge(x / 3 - 2, (x + 1) / 2), x)
    return _b7iq_same_set_1d(expected, x, _B7IQ_GRID_1D)


def alg_ineq_ferry_trucks():
    space, car, truck, cars = 136, 2, 5, 30
    sol = sp.solve_univariate_inequality(sp.Le(car * cars + truck * t, space), t, relational=False)
    return Integer(max(i for i in range(0, 200) if sol.contains(i)))


def alg_ineq_press_time_coefficient():
    coef_b, coef_f, limit = Rational(2, 5), Rational(1, 4), 8
    # 0.4 multiplies b (booklet batches) and the total is hours, so 0.4 is hours per booklet batch.

    def check(choices, idx):
        key = choices[idx]
        ok = "booklets uses 0.4 hour" in key and coef_b == Rational("0.4")
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("flyers uses 0.4" in ch and coef_f != Rational("0.4"))
            or ("0.4 batch of booklets per hour" in ch and 1 / coef_b != Rational("0.4"))
            or ("at most 0.4 hour" in ch and limit != Rational("0.4")))]
        return ok and len(wrong) == 3, f"coef of b = {coef_b} hours per batch; distractors contradicted {wrong}"

    return check


def alg_ineq_farm_stand_revenue_point():
    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            mv, bv = _b7iq_point(ch)
            if 6 * mv + 14 * bv >= 1800:
                good.append(i)
        return good == [idx], f"pairs with 6m + 14b >= 1800: {good}"

    return check


def alg_ineq_gym_plans_months():
    sol = sp.solve_univariate_inequality(sp.Lt(40 + 25 * t, 32 * t), t, relational=False)
    return Integer(min(i for i in range(0, 200) if sol.contains(i)))


def alg_ineq_rain_barrel_solution():
    sol = sp.solve_univariate_inequality(sp.Ge(480 - 15 * t, 120), t, relational=False)
    bound = sol.sup  # solution is t <= bound (t >= 0 in context)

    def check(choices, idx):
        nums = [Integer(re.search(r"first (\d+) minutes", ch).group(1)) for ch in choices]
        good = [i for i, v in enumerate(nums) if v == bound]
        return good == [idx], f"t <= {bound}; choice minutes {nums}"

    return check


# ----- hard -----


def alg_ineq_workshop_tables():
    best = None
    for tv in range(0, 50):
        for cv in range(0, 50):
            if 3 * cv + 7 * tv <= 120 and cv >= 2 * tv:
                best = tv if best is None else max(best, tv)
    return Integer(best)


def alg_ineq_candy_temperature_count():
    F = Symbol("F")
    celsius = Rational(5, 9) * (F - 32)
    rel = sp.And(sp.Le(112, celsius), sp.Le(celsius, 116))
    return Integer(sum(1 for i in range(0, 400) if bool(rel.subs(F, i))))


def alg_ineq_every_x_solution_k():
    # every x is a solution  <=>  the x-terms cancel and the constant comparison holds
    diff = sp.expand(3 * (2 * x - k) - (6 * x + 12))
    assert diff.coeff(x) == 0
    expected = sp.solve_univariate_inequality(sp.Le(diff, 0), k)
    return _b7iq_same_set_1d(expected, k, _B7IQ_GRID_1D)


def alg_ineq_no_solution_a():
    def no_solution(av):
        sol = sp.solve_univariate_inequality(sp.Lt(av * x + 5, 2 * (3 * x - 1)), x, relational=False)
        return sol == sp.EmptySet

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if no_solution(latex_to_sympy(ch))]
        return good == [idx], f"values of a giving no solution: {good}"

    return check


def alg_ineq_interval_all_satisfy_k():
    # x + k > 3x - 1  <=>  k > 2x - 1; must hold for every x in [2, 5]
    g = 2 * x - 1
    sup = sp.Max(*[g.subs(x, v) for v in (2, 5)])  # linear, so the max is at an endpoint
    return Integer(sp.floor(sup) + 1)


def alg_ineq_point_on_line_system_k():
    sol = sp.solve_univariate_inequality(sp.Gt(2 * k, -k + 9), k, relational=False).intersect(
        sp.solve_univariate_inequality(sp.Le(2 * k, k + 7), k, relational=False))
    assert not sol.right_open
    return sol.sup


def alg_ineq_wedge_greatest_x():
    sol = sp.solve_univariate_inequality(sp.Le(2 * x - 4, -Rational(1, 2) * x + 6), x, relational=False)
    assert not sol.right_open
    return sol.sup


def alg_ineq_difference_bounds():
    samples = [(3 + Rational(i, 2), -2 - Rational(j, 2)) for i in range(0, 20) for j in range(0, 20)]

    def check(choices, idx):
        implied = []
        for i, ch in enumerate(choices):
            rel = _b7iq_rel(ch)
            if all(bool(rel.subs({x: u, y: v})) for u, v in samples):
                implied.append(i)
        return implied == [idx], f"choices true for every x >= 3, y <= -2: {implied}"

    return check


def alg_ineq_lattice_points_count():
    return Integer(sum(1 for i in range(1, 30) for j in range(1, 30) if 3 * i + 4 * j <= 20))


# ----- Batch batch7-sys1 -----
import sympy as sp
from sympy import Rational, Eq

_b7sy_x, _b7sy_y = sp.symbols("x y")
_b7sy_k, _b7sy_a, _b7sy_b, _b7sy_c = sp.symbols("k a b c")


def _b7sy_solve(e1, e2):
    """Unique solution (x, y) of two equations given as SymPy Eq objects."""
    sol = sp.solve([e1, e2], [_b7sy_x, _b7sy_y], dict=True)
    assert len(sol) == 1 and not any(v.free_symbols for v in sol[0].values())
    return sol[0][_b7sy_x], sol[0][_b7sy_y]


def _b7sy_count(e1, e2):
    s = sp.linsolve([e1.lhs - e1.rhs, e2.lhs - e2.rhs], [_b7sy_x, _b7sy_y])
    if s == sp.S.EmptySet:
        return 0
    pt = next(iter(s))
    return "inf" if any(v.free_symbols for v in pt) else 1


def _b7sy_words(n):
    return {0: "Zero", 1: "Exactly one", "inf": "Infinitely many"}[n]


X, Y = _b7sy_x, _b7sy_y


def alg_sys_elim_subtract_y():
    return _b7sy_solve(Eq(4 * X + 3 * Y, 25), Eq(4 * X - Y, 1))[1]


def alg_sys_substitute_linear_y_x_spr():
    return _b7sy_solve(Eq(Y, 4 * X - 9), Eq(3 * X + 2 * Y, 37))[0]


def alg_sys_count_equal_slopes_zero():
    word = _b7sy_words(_b7sy_count(Eq(Y, 4 * X - 1), Eq(Y, 4 * X + 6)))

    def check(choices, idx):
        return choices[idx] == word, f"count -> {word}"

    return check


def alg_sys_intersection_standard_and_slope_form_x():
    return _b7sy_solve(Eq(2 * X + 5 * Y, 1), Eq(Y, X - 4))[0]


def alg_sys_add_equations_for_sum():
    sx, sy = _b7sy_solve(Eq(5 * X + 2 * Y, 31), Eq(3 * X + 6 * Y, 25))
    return sx + sy


def alg_sys_difference_gives_2x_minus_y_spr():
    sx, sy = _b7sy_solve(Eq(3 * X + Y, 17), Eq(X + 2 * Y, 9))
    return 2 * sx - sy


def alg_sys_decimal_coefficients_y_spr():
    R = Rational
    return _b7sy_solve(Eq(R(4, 10) * X + R(15, 10) * Y, R(73, 10)), Eq(R(12, 10) * X - R(5, 10) * Y, R(29, 10)))[1]


def alg_sys_fraction_coefficients_x_minus_y():
    R = Rational
    sx, sy = _b7sy_solve(Eq(R(1, 3) * X - R(1, 2) * Y, 1), Eq(R(3, 4) * X + R(1, 4) * Y, 5))
    return sx - sy


def _b7sy_line_through(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    m = Rational(y2 - y1, x2 - x1)
    return m * X + (y1 - m * x1)


def alg_sys_two_tables_intersection_b():
    f = _b7sy_line_through((1, 5), (3, 11))
    g = _b7sy_line_through((-1, 24), (2, 18))
    assert f.subs(X, 6) == 20 and g.subs(X, 5) == 12  # third table rows are consistent
    return _b7sy_solve(Eq(Y, f), Eq(Y, g))[1]


def alg_sys_verbal_lines_point_slope_x():
    return _b7sy_solve(Eq(Y - 3, 2 * (X - 1)), Eq(Y, -X + 9))[0]


def alg_sys_no_solution_fraction_slope_a():
    vals = [av for av in range(-20, 21)] + [Rational(2, 5), Rational(-2, 5)]
    none = [av for av in vals if _b7sy_count(Eq(Y, -Rational(2, 5) * X + 3), Eq(av * X + 5 * Y, 10)) == 0]
    assert len(none) == 1
    # Confirm algebraically: parallel condition.
    sol = sp.solve(Eq(-_b7sy_a / 5, -Rational(2, 5)), _b7sy_a)
    assert sol == none
    return sol[0]


def alg_sys_infinite_shifted_constants_ab_spr():
    a, b = _b7sy_a, _b7sy_b
    # Infinitely many: (a-1, 4, 10) proportional to (3, b+2, 15).
    sol = sp.solve([Eq((a - 1) * 15, 3 * 10), Eq(4 * 15, (b + 2) * 10)], [a, b], dict=True)[0]
    assert _b7sy_count(Eq((sol[a] - 1) * X + 4 * Y, 10), Eq(3 * X + (sol[b] + 2) * Y, 15)) == "inf"
    return sol[a] * sol[b]


def alg_sys_decimal_equation_infinite_partner():
    given = Eq(Rational(2, 5) * X - Rational(6, 5) * Y, 2)

    def check(choices, idx):
        inf = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            if _b7sy_count(given, Eq(lhs, rhs)) == "inf":
                inf.append(i)
        return inf == [idx], f"choices with infinitely many: {inf}"

    return check


def alg_sys_half_k_coefficient_no_solution_spr():
    k = _b7sy_k
    cand = sp.solve(sp.Matrix([[k / 2, -3], [5, 9]]).det(), k)
    none = [kv for kv in cand if _b7sy_count(Eq(kv / 2 * X - 3 * Y, 4), Eq(5 * X + 9 * Y, 2)) == 0]
    assert len(none) == 1
    return none[0]


def alg_sys_symmetric_coefficients_difference_of_squares():
    sx, sy = _b7sy_solve(Eq(13 * X + 7 * Y, 47), Eq(7 * X + 13 * Y, 13))
    return sp.expand(sx**2 - sy**2)


def alg_sys_slider_k_meet_on_x_axis():
    k = _b7sy_k
    xi = sp.solve(Eq(3 * X - 2 * 0, 8), X)[0]
    return sp.solve(Eq(0, k * xi + 2), k)[0]


def alg_sys_exactly_one_solution_condition():
    k, c = _b7sy_k, _b7sy_c
    bad_k = sp.solve(sp.Matrix([[4, -6], [6, k]]).det(), k)[0]  # -9
    samples = [(kv, cv) for kv in range(-15, 6) for cv in [Rational(9, 2), 0, 3, -7]]

    def unique(kv, cv):
        return _b7sy_count(Eq(4 * X - 6 * Y, 3), Eq(6 * X + kv * Y, cv)) == 1

    def holds(stmt, kv, cv):
        body = stmt.strip().strip("$")
        neq = "\\neq" in body
        lhs, rhs = body.split("\\neq") if neq else body.split("=")
        val = {"k": kv, "c": cv}[lhs.strip()]
        target = latex_to_sympy(rhs)
        return (val != target) if neq else (val == target)

    def check(choices, idx):
        must = []
        for i, ch in enumerate(choices):
            if all(holds(ch, kv, cv) for kv, cv in samples if unique(kv, cv)):
                must.append(i)
        # The key's statement is equivalent to uniqueness.
        equiv = all(holds(choices[idx], kv, cv) == unique(kv, cv) for kv, cv in samples)
        return must == [idx] and equiv, f"k bad at {bad_k}; must-be-true choices {must}; equivalent={equiv}"

    return check


def alg_sys_parallel_line_through_point():
    given = Eq(3 * X - 4 * Y, 12)

    def check(choices, idx):
        ok = []
        for i, ch in enumerate(choices):
            lhs, rhs = _split_equation(ch)
            through = (lhs - rhs).subs({X: 2, Y: 5}) == 0
            if through and _b7sy_count(given, Eq(lhs, rhs)) == 0:
                ok.append(i)
        return ok == [idx], f"choices through (2,5) with no solution: {ok}"

    return check


def alg_sys_functions_intersection_then_evaluate():
    f = lambda t: 3 * t - 7  # noqa: E731
    a = sp.solve(Eq(f(X), -Rational(1, 2) * X + 7), X)[0]
    return f(2 * a)


def alg_sys_line_through_intercepts_coordinate_sum():
    q = _b7sy_line_through((0, -2), (4, 0))
    sx, sy = _b7sy_solve(Eq(3 * X + 4 * Y, 20), Eq(Y, q))
    return sx + sy


def alg_sys_soap_sales_interpret_constant():
    sx, sy = _b7sy_solve(Eq(X + Y, 50), Eq(4 * X + 7 * Y, 275))
    quantities = {
        "total revenue": 4 * sx + 7 * sy,
        "total number of bars": sx + sy,
        "revenue, in dollars, from large": 7 * sy,
        "number of large bars": sy,
    }

    def check(choices, idx):
        true = []
        for i, ch in enumerate(choices):
            for phrase, val in quantities.items():
                if phrase in ch.lower():
                    if val == 275:
                        true.append(i)
                    break
        return true == [idx], f"quantities {quantities}; choices equal to 275: {true}"

    return check


def alg_sys_pottery_studio_equal_cost_hours():
    return _b7sy_solve(Eq(Y, 18 + 6 * X), Eq(Y, 30 + 4 * X))[0]


def alg_sys_coffee_blend_pricier_beans():
    return _b7sy_solve(Eq(X + Y, 40), Eq(12 * X + 20 * Y, 15 * 40))[1]


def alg_sys_cyclists_catch_up_distance_spr():
    R = Rational
    return _b7sy_solve(Eq(Y, 18 * X), Eq(Y, 24 * (X - R(1, 2))))[1]


def alg_sys_nursery_shrubs_trees_model():
    s, t = sp.symbols("s t")
    truth = sp.solve([Eq(s + t, 87), Eq(s, 2 * t + 12)], [s, t], dict=True)[0]

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            parts = [p.strip().strip("$") for p in ch.split(" and ")]
            eqs = []
            for p in parts:
                lhs, rhs = p.split("=")
                eqs.append(Eq(latex_to_sympy(lhs), latex_to_sympy(rhs)))
            sol = sp.solve(eqs, [s, t], dict=True)
            if sol and sol[0] == truth:
                hits.append(i)
        return hits == [idx], f"truth {truth}; matching systems {hits}"

    return check


def alg_sys_car_rental_six_dollars_less():
    m = sp.Symbol("m")
    R = Rational
    return sp.solve(Eq((30 + R(1, 4) * m) - (45 + R(1, 5) * m), 6), m)[0]


def alg_sys_bagels_juices_combined_price():
    R = Rational
    sx, sy = _b7sy_solve(Eq(3 * X + 2 * Y, R(27, 2)), Eq(5 * X + 4 * Y, R(49, 2)))
    return sx + sy


def alg_sys_two_clubs_members_table_weeks_spr():
    a = _b7sy_line_through((0, 54), (3, 63))
    b = _b7sy_line_through((0, 102), (3, 93))
    assert a.subs(X, 6) == 72 and b.subs(X, 6) == 84  # third table column is consistent
    return _b7sy_solve(Eq(Y, a), Eq(Y, b))[0]


def alg_sys_boat_current_speed():
    b, c = _b7sy_b, _b7sy_c
    sol = sp.solve([Eq(2 * (b + c), 36), Eq(3 * (b - c), 36)], [b, c], dict=True)[0]
    return sol[c]


# ----- Batch batch7-lat -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch7-lat.ts (batch batch7-lat, Lines, angles, and triangles).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch7_lat.py --only-extra

Each function derives the key from the stem's givens and returns it as an exact
SymPy object, or a callable (choices, answer_index) -> (ok, detail) for choices
the base parser cannot read (radicals, sentences).
"""



import re

import sympy as sp
from sympy import Eq, Integer, Rational, symbols

_b7lt_x = symbols("_b7lt_x")
_b7lt_a = symbols("_b7lt_a", positive=True)


def _b7lt_solve1(eq):
    sols = sp.solve(eq, _b7lt_x)
    assert len(sols) == 1, sols
    return sols[0]


def _b7lt_valid_roots(eq, exprs):
    """Real roots of eq for which every angle/length expression is positive."""
    out = []
    for v in sp.solve(eq, _b7lt_x):
        if v.is_real and all(e.subs(_b7lt_x, v) > 0 for e in exprs):
            out.append(v)
    assert len(out) == 1, out
    return out[0]


def geo_vertical_angles_expression_measure():
    X = _b7lt_x
    v = _b7lt_solve1(Eq(4 * X + 18, 6 * X - 12))  # vertical angles congruent
    return (4 * X + 18).subs(X, v)


def geo_complementary_expressions_x():
    X = _b7lt_x
    return _b7lt_solve1(Eq((3 * X + 7) + (2 * X - 2), 90))


def geo_linear_pair_ratio_four_to_one():
    a = sp.solve(Eq(_b7lt_a + 4 * _b7lt_a, 180), _b7lt_a)[0]
    return 4 * a


def geo_corresponding_angles_solve_x():
    X = _b7lt_x
    return _b7lt_solve1(Eq(5 * X - 14, 3 * X + 22))


def geo_equilateral_side_expressions_x():
    X = _b7lt_x
    v = _b7lt_solve1(Eq(2 * X + 5, 4 * X - 9))
    assert (2 * X + 5).subs(X, v) > 0
    return v


def geo_angle_ratio_largest_angle():
    a = sp.solve(Eq(2 * _b7lt_a + 3 * _b7lt_a + 7 * _b7lt_a, 180), _b7lt_a)[0]
    return 7 * a


def geo_alternate_interior_obtuse_angle():
    X = _b7lt_x
    v = _b7lt_solve1(Eq(7 * X - 30, 4 * X + 15))
    ang = (4 * X + 15).subs(X, v)
    return max(ang, 180 - ang)


def geo_isosceles_exterior_base_angle():
    B = sp.solve(Eq(2 * _b7lt_a, 112), _b7lt_a)[0]  # exterior angle = B + C, B = C
    assert (180 - 112) + 2 * B == 180
    return B


def geo_regular_polygon_sides_156():
    n = symbols("n", positive=True)
    return sp.solve(Eq(180 * (n - 2), 156 * n), n)[0]


def geo_side_splitter_parallel_length():
    AD, DB, DE = 4, 6, 5
    return Rational(DE * (AD + DB), AD)


def geo_dilation_angle_unchanged():
    Z = 180 - 38 - 64  # dilation preserves angles: N = Z
    return Integer(Z)


def geo_triangle_inequality_integer_count():
    return Integer(len([s for s in range(1, 100) if s < 7 + 12 and 12 < 7 + s and 7 < 12 + s]))


def geo_quadrilateral_diagonal_congruence():
    # Triangles ABC and CDA; correspondence A->C, B->D, C->A.
    corr = {"A": "C", "B": "D", "C": "A"}
    # Known congruent side pairs (as vertex sets in triangle ABC): AB<->CD and AC<->CA.
    known_sides = {frozenset("AB"), frozenset("AC")}

    def angle_vertex_in_ABC(name_abc, name_cda):
        """Return the ABC vertex if the stated pair corresponds, else None."""
        if set(name_abc) != set("ABC"):
            return None
        v1 = name_abc[1]
        # In triangle CDA the angle must use only C, D, A and sit at corr[v1].
        if set(name_cda) != set("CDA") or name_cda[1] != corr[v1]:
            return None
        return v1

    def sufficient(sides, angles):
        if len(sides) == 3:
            return True
        if len(angles) >= 2 and len(sides) >= 1:
            return True
        if len(sides) == 2 and angles:
            s1, s2 = sides
            return any(v in (s1 & s2) for v in angles)  # SAS needs the included angle
        return False

    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            names = re.findall(r"angle \$([A-Z]{3})\$", ch)
            assert len(names) == 2, ch
            v = angle_vertex_in_ABC(names[0], names[1])
            if v is not None and sufficient(known_sides, {v}):
                good.append(i)
        return good == [idx], f"sufficient choices {good}"

    return check


def geo_linear_pair_quadratic_angle():
    X = _b7lt_x
    v = _b7lt_valid_roots(Eq(X**2 + 6 * X - 7, 180), [X**2, 6 * X - 7])
    return (6 * X - 7).subs(X, v)


def geo_triangle_fraction_angle_expressions():
    X = _b7lt_x
    angles = [X / 3 + 20, X / 4 + 35, X / 6 + 17]
    v = _b7lt_solve1(Eq(sum(angles), 180))
    vals = [e.subs(X, v) for e in angles]
    assert all(val > 0 for val in vals)
    return max(vals)


def geo_exterior_angle_quadratic_interior():
    X = _b7lt_x
    A, B, ext = 3 * X + 4, 4 * X - 6, X**2 - 10
    v = _b7lt_valid_roots(Eq(ext, A + B), [A, B, ext, 180 - ext])
    return 180 - ext.subs(X, v)


def geo_side_splitter_quadratic_length():
    X = _b7lt_x
    FJ, JG, FK, KH = X - 2, 8, 5, X + 4
    v = _b7lt_valid_roots(Eq(FJ * KH, JG * FK), [FJ, KH])
    return FK + KH.subs(X, v)


def geo_pond_width_crossing_segments():
    AB, AC, CE = 18, 12, 30
    return Rational(AB * CE, AC)  # triangle ABC ~ triangle EDC


def geo_regular_frame_perimeter_140():
    n = sp.solve(Eq(180 * (symbols("n") - 2), 140 * symbols("n")), symbols("n"))[0]
    return 9 * n


def geo_welded_tubes_third_side():
    def check(choices, idx):
        vals = [latex_to_sympy_ext(c) for c in choices]
        good = [i for i, s in enumerate(vals) if s + 16 > 27 and s + 27 > 16 and 16 + 27 > s]
        return good == [idx], f"valid third sides at {good}"

    return check


def geo_mirror_beam_lamp_height():
    post_h, mirror_to_post, gap = Rational(12, 10), 2, 7
    mirror_to_wall = gap - mirror_to_post
    return post_h * mirror_to_wall / mirror_to_post


def geo_pentagon_flower_bed_fifth_angle():
    return Integer(180 * (5 - 2) - (100 + 115 + 108 + 120))


def geo_rail_lines_same_side_interior():
    X = _b7lt_x
    v = _b7lt_solve1(Eq((2 * X + 14) + (5 * X - 9), 180))
    vals = [(2 * X + 14).subs(X, v), (5 * X - 9).subs(X, v)]
    return min(vals)


def geo_equilateral_extension_angle_bad():
    acd = 180 - 60
    cad = Rational(180 - acd, 2)
    return 60 + cad


def geo_shared_angle_similar_side():
    AD, DC = 4, 5
    ab = symbols("ab", positive=True)
    return sp.solve(Eq(ab / (AD + DC), AD / ab), ab)[0]  # triangle ABD ~ triangle ACB: AB/AC = AD/AB


def geo_angle_bisectors_meet_bic():
    half_sum = Rational(180 - 52, 2)
    return 180 - half_sum


def geo_parallel_lines_bent_path_angle():
    # Coordinates: l is y = 1, m is y = 0, A = (0, 1), B = (0, 0), C and D on the +x side.
    import math
    pac, pbd = math.radians(38), math.radians(47)
    # P = A + t1*(cos pac, -sin pac) = B + t2*(cos pbd, sin pbd).
    t1 = 1 / (math.sin(pac) + math.cos(pac) * math.tan(pbd))
    px, py = t1 * math.cos(pac), 1 - t1 * math.sin(pac)
    assert 0 < py < 1 and px > 0  # P between the lines, same side of AB as C and D
    assert abs(math.degrees(math.atan2(py, px)) - 47) < 1e-9  # angle PBD really is 47
    ax, ay, bx, by = -px, 1 - py, -px, -py
    deg = math.degrees(math.acos((ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by))))
    assert abs(deg - (38 + 47)) < 1e-9, deg
    return Integer(round(deg))


# ----- Batch batch8-rtt -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch8-rtt.ts (batch batch8-rtt).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch8_rtt.py --only-extra

Each function derives the answer from the stem's givens: an exact SymPy number
for numeric keys, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices contain radicals (parsed with latex_to_sympy_ext).
"""



import sympy as sp
from sympy import Rational, Integer, symbols, sqrt, pi, sin, cos, tan, atan, asin, acos, Eq

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")

_B8RT_DEG = pi / 180


def _b8rt_nearest(value, places: int = 1):
    """Round an exact SymPy number to `places` decimals, asserting it is not a near tie."""
    v = sp.nsimplify(round(float(value), 9))
    scaled = v * 10**places
    assert abs(scaled - sp.floor(scaled) - Rational(1, 2)) > Rational(1, 100), "rounding tie"
    return Rational(int(sp.floor(scaled + Rational(1, 2))), 10**places)


def _b8rt_pick(expected):
    """Callable for MC items with radical choices: exactly the key choice equals `expected`."""
    expected = sp.nsimplify(expected)

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        matches = [i for i, v in enumerate(vals) if sp.simplify(v - expected) == 0]
        fl = [float(v) for v in vals]
        mono = all(u < w for u, w in zip(fl, fl[1:])) or all(u > w for u, w in zip(fl, fl[1:]))
        return matches == [idx] and mono, f"expected {expected}; matching choices {matches}; monotonic {mono}"

    return check


# ----- easy -------------------------------------------------------------------


def geo_ladder_wall_height_pythagorean():
    h = [v for v in sp.solve(Eq(x**2 + Rational(5, 2) ** 2, Rational(13, 2) ** 2), x) if v > 0][0]
    return h


def geo_legs_9_40_hypotenuse():
    return sqrt(9**2 + 40**2)


def geo_isosceles_right_leg_9_hypotenuse():
    # Angle Y = 180 - 45 - 45 = 90, so XZ is the hypotenuse; law of sines as an independent check.
    xz = 9 * sin(90 * _B8RT_DEG) / sin(45 * _B8RT_DEG)
    return _b8rt_pick(sp.simplify(xz))


def geo_tan_e_from_three_sides():
    de, ef, df = 29, 20, 21
    assert ef**2 + df**2 == de**2
    return Rational(df, ef)  # opposite E over adjacent E


def geo_sin_28_cos_x_complement():
    sols = [v for v in range(1, 90) if abs(float(sin(28 * _B8RT_DEG) - cos(v * _B8RT_DEG))) < 1e-12]
    assert sols == [62]
    return Integer(sols[0])


def geo_radians_7pi_12_to_degrees():
    return (7 * pi / 12) * 180 / pi


# ----- medium -----------------------------------------------------------------


def geo_post_shadow_sun_elevation():
    shadow = Rational(32, 10) / tan(35 * _B8RT_DEG)
    assert abs(float(shadow) - 4.570) < 0.001
    return _b8rt_nearest(shadow)


def geo_river_width_survey_tangent():
    ab = 80 * tan(58 * _B8RT_DEG)
    assert [float(_b8rt_nearest(v)) for v in (80 * cos(58 * _B8RT_DEG), 80 / tan(58 * _B8RT_DEG), 80 * sin(58 * _B8RT_DEG))] == [42.4, 50.0, 67.8]
    return _b8rt_nearest(ab)


def geo_truck_ramp_length_sine():
    L = Rational(12, 10) / sin(14 * _B8RT_DEG)
    assert [float(_b8rt_nearest(v)) for v in (Rational(12, 10) * tan(14 * _B8RT_DEG), Rational(12, 10) / sin(14), Rational(12, 10) / tan(14 * _B8RT_DEG))] == [0.3, 1.2, 4.8]
    return _b8rt_nearest(L)


def geo_escalator_horizontal_30_60_90():
    return _b8rt_pick(12 * cos(30 * _B8RT_DEG))


def geo_cliff_elevation_arccos():
    angle = acos(Rational(90, 150)) / _B8RT_DEG
    assert float(_b8rt_nearest(asin(Rational(90, 150)) / _B8RT_DEG)) == 36.9
    assert float(_b8rt_nearest(atan(Rational(150, 90)) / _B8RT_DEG)) == 59.0
    assert float(_b8rt_nearest(atan(Rational(90, 150)) / _B8RT_DEG)) == 31.0
    return _b8rt_nearest(angle)


def geo_30_60_90_longer_leg_hypotenuse():
    # R at the origin, S on the x-axis, angle R = 60°: ST = RS tan 60° (ST opposite R).
    rs = sp.solve(Eq(s * tan(60 * _B8RT_DEG), 8 * sqrt(3)), s)[0]
    return sp.simplify(rs / cos(60 * _B8RT_DEG))


def geo_cos_to_tan_nontriple():
    A = acos(Rational(3, 7))
    return _b8rt_pick(sp.simplify(tan(A)))


def geo_similar_triangle_tan_scaled():
    bc = sqrt(17**2 - 15**2)
    ac_d, bc_d = 3 * 15, 3 * bc  # triangle DEF: E corresponds to B; opposite E is DF (~AC), adjacent is EF (~BC)
    return sp.nsimplify(ac_d / bc_d)


def geo_triangle_angles_sin_cos_equal():
    A, B = 2 * x, x + 6
    valid = []
    for sol in sp.solve(Eq(A + B, 90), x) + sp.solve(Eq(A, B + 90), x):
        a_, b_ = A.subs(x, sol), B.subs(x, sol)
        if a_ > 0 and b_ > 0 and a_ + b_ < 180:
            assert sp.simplify(sin(a_ * _B8RT_DEG) - cos(b_ * _B8RT_DEG)) == 0
            valid.append(a_)
    assert len(valid) == 1
    return valid[0]


def geo_complementary_radians_k():
    B = pi / 2 - 3 * pi / 10
    return sp.simplify(B / pi)


def geo_tan_2pi_3_unit_circle():
    return _b8rt_pick(tan(2 * pi / 3))


# ----- hard -------------------------------------------------------------------


def geo_altitude_45_30_split_base():
    C = sp.Point(0, 6)
    D = sp.Point(0, 0)
    A = sp.Point(-6 / tan(45 * _B8RT_DEG), 0)
    B = sp.Point(6 / tan(30 * _B8RT_DEG), 0)
    # Angles at A and B are 45° and 30°.
    assert sp.simplify(sp.Segment(A, C).length - 6 * sqrt(2)) == 0
    assert sp.simplify(sp.Segment(B, C).length - 12) == 0
    return _b8rt_pick(sp.simplify(A.distance(B)))


def geo_parallel_segment_cos_complement():
    # P at the origin, R on the positive x-axis, S = (12, 0), T = (12, 5); Q is on ray PT above R.
    P, S, T = sp.Point(0, 0), sp.Point(12, 0), sp.Point(12, 5)
    R = sp.Point(30, 0)  # any R beyond S works; the angle at Q does not depend on it
    Q = sp.Point(30, 30 * Rational(5, 12))
    cos_q = (P - Q).dot(R - Q) / (P.distance(Q) * R.distance(Q))
    return sp.simplify(cos_q)


def geo_sin_x_squared_cos_x():
    f = sp.lambdify(x, sp.sin(x**2 * _B8RT_DEG) - sp.cos(x * _B8RT_DEG))
    roots = set()
    for i in range(1, 949):
        x0, x1 = i / 100, (i + 1) / 100
        if x1**2 >= 90:
            break
        if f(x0) == 0 or f(x0) * f(x1) < 0:
            roots.add(round(float(sp.nsolve(sp.sin(x**2 * _B8RT_DEG) - sp.cos(x * _B8RT_DEG), x, (x0 + x1) / 2)), 9))
    assert roots == {9.0}, roots
    assert sp.simplify(sin(81 * _B8RT_DEG) - cos(9 * _B8RT_DEG)) == 0
    return Integer(9)


def geo_isosceles_base_cosine():
    kl = 2 * 10 * cos(50 * _B8RT_DEG)
    assert [float(_b8rt_nearest(v)) for v in (10 * cos(50 * _B8RT_DEG), 10 * sin(50 * _B8RT_DEG), 20 * sin(50 * _B8RT_DEG))] == [6.4, 7.7, 15.3]
    return _b8rt_nearest(kl)


def geo_right_triangle_area_hypotenuse_angle():
    bc, ac = 15 * sin(64 * _B8RT_DEG), 15 * cos(64 * _B8RT_DEG)
    area = Rational(1, 2) * bc * ac
    assert [float(_b8rt_nearest(v)) for v in (Rational(1, 2) * 15 * ac, bc * ac, Rational(1, 2) * 15 * bc)] == [49.3, 88.7, 101.1]
    return _b8rt_nearest(area)


def geo_shadow_flagpole_hypotenuse():
    height = Rational(15, 10) / 2 * 14
    return sqrt(height**2 + 14**2)


def geo_lighthouse_two_elevations():
    h, d = symbols("h d", positive=True)
    sol = sp.solve([Eq(tan(45 * _B8RT_DEG), h / d), Eq(tan(30 * _B8RT_DEG), h / (d + 40))], [h, d], dict=True)
    assert len(sol) == 1
    height = sol[0][h]
    assert float(_b8rt_nearest(40 / (sqrt(3) + 1))) == 14.6
    assert float(_b8rt_nearest(height + 40)) == 94.6
    return _b8rt_nearest(height)


def geo_legs_differ_by_7_area():
    legs = [v for v in sp.solve(Eq(x**2 + (x + 7) ** 2, 17**2), x) if v > 0]
    assert legs == [8]
    return Rational(1, 2) * legs[0] * (legs[0] + 7)


def geo_sum_angles_sine_negative_root3():
    th = symbols("th")
    sols = sp.solveset(Eq(sin(th), -sqrt(3) / 2), th, sp.Interval.Ropen(0, 2 * pi))
    assert len(sols) == 2
    return sum(sols)


def geo_square_diagonal_2_more():
    side = [v for v in sp.solve(Eq(s * sqrt(2), s + 2), s) if v > 0][0]
    return _b8rt_pick(sp.radsimp(side))


def geo_sin_twice_cos_value():
    A = atan(2)  # sin A = 2 cos A  <=>  tan A = 2 for an acute angle A
    assert sp.simplify(sin(A) - 2 * cos(A)) == 0
    return _b8rt_pick(sp.simplify(cos(A)))


# ----- Batch batch8-psdaC -----
import math


import sympy as sp
from sympy import Rational, Eq

_b8pc_x = sp.symbols("x")
X = _b8pc_x


def _b8pc_lsq(pts):
    """Exact least-squares slope and intercept for a list of (x, y) pairs."""
    n = len(pts)
    xs = [sp.nsimplify(p[0]) for p in pts]
    ys = [sp.nsimplify(p[1]) for p in pts]
    xb, yb = sum(xs) / n, sum(ys) / n
    m = sum((xi - xb) * (yi - yb) for xi, yi in zip(xs, ys)) / sum((xi - xb) ** 2 for xi in xs)
    return m, yb - m * xb


def _b8pc_rhs(choice):
    return sp.nsimplify(latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1]), rational=True)


def _b8pc_pick_equation(expected):
    """Callable: exactly the key choice's right-hand side equals the expected expression."""
    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if sp.simplify(_b8pc_rhs(ch) - expected) == 0]
        return matches == [idx], f"expected y = {expected}; matching choices {matches}"
    return check


def _b8pc_pick_text(predicate, detail):
    """Callable: exactly the key choice satisfies the predicate on its text."""
    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if predicate(ch)]
        return matches == [idx], f"{detail}; matching choices {matches}"
    return check


# ---------------------------------------------------------------- Two-variable data


def psda_shipping_weight_rate_interpretation():
    # y = 2.4x + 15: the coefficient of x is the change in estimated cost per kilogram.
    model = Rational(24, 10) * X + 15
    rate = sp.diff(model, X)
    assert rate == Rational(12, 5)
    return _b8pc_pick_text(
        lambda ch: ch.startswith("For each additional kilogram") and "increases by 2.40 dollars" in ch,
        f"rate of change {rate} dollars per kilogram",
    )


def psda_bicycle_resale_intercept():
    model = -35 * X + 420
    at_zero = model.subs(X, 0)
    assert at_zero == 420
    return _b8pc_pick_text(
        lambda ch: "age 0 years" in ch and "is 420 dollars" in ch and "estimated" in ch,
        f"model value at x = 0 is {at_zero}",
    )


def psda_bamboo_shoot_prediction():
    return (Rational(9, 2) * X + 12).subs(X, 10)


def psda_iced_drinks_residual():
    predicted = (3 * X - 95).subs(X, 80)
    return 138 - predicted


def psda_candle_height_regression():
    pts = [(1, "18.6"), (2, "16.9"), (3, "15.5"), (4, "13.4"), (5, "12.1")]
    m, b = _b8pc_lsq(pts)
    return _b8pc_pick_equation(m * X + b)


def psda_spring_length_regression_prediction():
    m, b = _b8pc_lsq([(10, 52), (20, 57), (30, 61), (40, 66), (50, 69)])
    value = m * 60 + b
    # Exact value already has one decimal place, so "to the nearest tenth" is the value itself.
    assert (value * 10).is_integer
    return value


def psda_points_constant_ratio_relationship():
    pts = [(0, 400), (1, 300), (2, 225), (3, Rational(675, 4))]
    ratios = {Rational(pts[i + 1][1]) / pts[i][1] for i in range(3)}
    diffs = {Rational(pts[i + 1][1]) - pts[i][1] for i in range(3)}
    assert len(ratios) == 1 and len(diffs) > 1
    pct = (1 - ratios.pop()) * 100  # percent decrease per step
    return _b8pc_pick_text(
        lambda ch: ch.startswith("Exponential") and f"decreases by {pct}%" in ch,
        f"constant ratio, decrease {pct}% per step",
    )


def psda_ticket_price_revenue_quadratic():
    a, b, c = sp.symbols("a b c")
    pts = [(10, 1500), (15, 1875), (20, 2000), (25, 1875), (30, 1500)]
    q = a * X**2 + b * X + c
    sol = sp.solve([Eq(q.subs(X, px), py) for px, py in pts[:3]], [a, b, c], dict=True)[0]
    fitted = q.subs(sol)
    assert all(fitted.subs(X, px) == py for px, py in pts)  # quadratic fits all five exactly
    return fitted.subs(X, 35)


def psda_apartment_rent_association():
    # Described: points close to a line (strong, linear), y decreases as x increases (negative).
    return _b8pc_pick_text(
        lambda ch: ch.strip() == "A strong negative linear association",
        "strong, negative, linear",
    )


def psda_points_leveling_association():
    ys = [20, 31, 37, 40, 41, Rational(83, 2)]
    d = [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]
    assert all(v > 0 for v in d)  # increasing: positive
    assert len(set(d)) > 1 and all(d[i] > d[i + 1] for i in range(len(d) - 1))  # not constant: nonlinear
    return _b8pc_pick_text(
        lambda ch: ch.strip() == "A positive nonlinear association",
        f"first differences {d}: positive and shrinking",
    )


def psda_exhibit_visitors_models_compare():
    f = 1200 + 150 * X
    g = 1200 * Rational(11, 10) ** X
    week = next(w for w in range(0, 100) if w > 0 and g.subs(X, w) > f.subs(X, w))
    assert g.subs(X, week - 1) <= f.subs(X, week - 1)
    return sp.Integer(week)


def psda_tree_species_equal_height():
    return sp.solve(Eq(Rational(1, 2) * X + Rational(12, 5), Rational(7, 20) * X + Rational(21, 5)), X)[0]


def psda_printer_value_decay_interpretation():
    base = Rational(85, 100)
    pct = (1 - base) * 100
    return _b8pc_pick_text(
        lambda ch: f"decreases by {pct}% each year" in ch,
        f"decay factor {base}: {pct}% decrease each year",
    )


def psda_points_above_model_line():
    pts = [(1, 2), (2, 3), (3, 7), (4, 11), (5, 14), (6, 15)]
    return sp.Integer(sum(1 for px, py in pts if py > 3 * px - 2))


def psda_study_hours_intercept_from_means():
    pts = [(1, 58), (2, 66), (4, 75), (5, 81), (8, 90)]
    m, b = _b8pc_lsq(pts)
    assert m == Rational(9, 2)  # the slope stated in the stem
    return b


def psda_forum_members_exponential_fit():
    pts = [(0, 118), (1, 152), (2, 186), (3, 236), (4, 291)]
    # Log-linear least squares (what Desmos log mode fits), rounded as in the choices.
    lx = [p[0] for p in pts]
    ly = [math.log(p[1]) for p in pts]
    xb, yb = sum(lx) / 5, sum(ly) / 5
    m = sum((u - xb) * (v - yb) for u, v in zip(lx, ly)) / sum((u - xb) ** 2 for u in lx)
    a_fit, b_fit = round(math.exp(yb - m * xb), 1), round(math.exp(m), 2)

    def check(choices, idx):
        ssr = []
        for ch in choices:
            rhs = _b8pc_rhs(ch)
            ssr.append(float(sum((rhs.subs(X, px) - py) ** 2 for px, py in pts)))
        expected = sp.nsimplify(a_fit, rational=True) * sp.nsimplify(b_fit, rational=True) ** X
        matches = [i for i, ch in enumerate(choices) if sp.simplify(_b8pc_rhs(ch) - expected) == 0]
        best = min(range(4), key=lambda i: ssr[i])
        ok = matches == [idx] and best == idx
        return ok, f"log fit y = {a_fit}({b_fit})^x; matches {matches}; SSR {[round(v, 1) for v in ssr]}"

    return check


# ---------------------------------------------------------------- Probability


def psda_bulb_shipment_expected_defective():
    return Rational(4, 100) * 1250


def psda_fair_food_ride_joint():
    both, food_only, ride_only, neither = 120, 70, 50, 60
    total = both + food_only + ride_only + neither
    assert total == 300
    return Rational(both, total)


def psda_bean_plants_soil_given_flowered():
    a_yes, a_no, b_yes, b_no = 84, 36, 78, 52
    assert a_yes + a_no + b_yes + b_no == 250
    return Rational(b_yes, a_yes + b_yes)


def psda_game_club_neither():
    total, chess, checkers, both = 80, 30, 25, 10
    neither = total - (chess + checkers - both)
    return Rational(neither, total)


def psda_display_bin_red_apples():
    r = sp.symbols("r")
    return sp.solve(Eq(Rational(18) / (18 + r + 6), Rational(3, 8)), r)[0]


def psda_spanish_art_given_art():
    total = 400
    spanish = total * Rational(60, 100)
    spanish_art = spanish * Rational(25, 100)
    other_art = (total - spanish) * Rational(40, 100)
    return spanish_art / (spanish_art + other_art)


def psda_tiles_with_replacement_both_blue():
    return Rational(12, 30) ** 2


def psda_inspection_truck_given_failed():
    car_pass, car_fail, truck_pass, truck_fail = 198, 42, 84, 36
    assert car_pass + car_fail + truck_pass + truck_fail == 360
    return Rational(truck_fail, car_fail + truck_fail)


def psda_household_pets_at_least_two():
    freq = {0: 14, 1: 18, 2: 11, 3: 7}
    assert sum(freq.values()) == 50
    return Rational(sum(v for k_, v in freq.items() if k_ >= 2), 50)


def psda_two_lines_defective_source():
    a_def = 3000 * Rational(4, 100)
    b_def = 5000 * Rational(15, 1000)
    return a_def / (a_def + b_def)


# ----- Batch batch8-le1v1 -----
import sympy as sp
from sympy import Rational, Eq

_b8l1_x, _b8l1_k, _b8l1_a, _b8l1_b, _b8l1_c = sp.symbols("x k a b c")
_b8l1_m, _b8l1_n, _b8l1_p, _b8l1_g, _b8l1_C = sp.symbols("m n p g C")
_b8l1_R = Rational


def _b8l1_solve1(lhs, rhs, var=None):
    """Unique solution of a linear equation lhs = rhs in one variable."""
    var = var if var is not None else _b8l1_x
    sol = sp.solve(Eq(lhs, rhs), var)
    assert len(sol) == 1, sol
    return sol[0]


def _b8l1_count(lhs, rhs, var=None):
    """'Zero', 'Exactly one' or 'Infinitely many' for a linear equation."""
    var = var if var is not None else _b8l1_x
    d = sp.expand(lhs - rhs)
    coef, const = d.coeff(var, 1), d.coeff(var, 0)
    if coef != 0:
        return "Exactly one"
    return "Infinitely many" if const == 0 else "Zero"


def _b8l1_parse_eq(choice):
    s = choice.strip().strip("$")
    left, right = s.split("=")
    return latex_to_sympy(left), latex_to_sympy(right)


def _b8l1_rhs_matches(target_symbol, expected):
    """Choices are 'v = expr'; exactly the key's expr equals expected."""

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            left, right = _b8l1_parse_eq(ch)
            assert left == sp.Symbol(str(target_symbol)), left
            right = right.subs({sp.Symbol(str(s)): s for s in right.free_symbols})
            if sp.simplify(right - expected) == 0:
                hits.append(i)
        return hits == [idx], f"expected {expected}; matching choices {hits}"

    return check


def alg_decimal_quarter_coefficients_solve():
    return _b8l1_solve1(_b8l1_R(1, 4) * _b8l1_x + _b8l1_R(3, 2), _b8l1_R(3, 4) * _b8l1_x - _b8l1_R(5, 2))


def alg_distribute_negative_two_spr():
    return _b8l1_solve1(7 - 2 * (_b8l1_x - 3), 5)


def alg_flour_batches_equation():
    b = sp.Symbol("b")
    model = 40 - _b8l1_R(5, 2) * b - _b8l1_R(25, 2)  # flour left after b batches equals 12.5

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            left, right = _b8l1_parse_eq(ch)
            d = sp.nsimplify(sp.expand(left - right))
            ratio = sp.simplify(d / model)
            if ratio.is_number and ratio != 0:
                hits.append(i)
        return hits == [idx], f"choices equivalent to 40 - 2.5b = 12.5: {hits}"

    return check


def alg_submarine_depth_constant_meaning():
    m = sp.Symbol("m")
    msol = _b8l1_solve1(940 - 65 * m, 290, m)
    described = [940, 65, 940 - 65 * msol, 65 * msol]  # quantity each choice describes, in order

    def check(choices, idx):
        hits = [i for i, v in enumerate(described) if v == 290]
        return hits == [idx], f"m = {msol}; choices describing 290: {hits}"

    return check


def alg_literal_solve_m_three_terms():
    m, n, p = sp.symbols("m n p")
    return _b8l1_rhs_matches(m, sp.solve(Eq(3 * m + 2 * n, p), m)[0])


def alg_three_unit_fractions_of_x_solve():
    return _b8l1_solve1(_b8l1_x / 2 + _b8l1_x / 3, _b8l1_x / 4 + 7)


def alg_decimal_distribute_both_sides_spr():
    R = _b8l1_R
    return _b8l1_solve1(R(6, 5) * (3 * _b8l1_x - 5), R(4, 5) * (2 * _b8l1_x + 10) + R(2, 5))


def alg_value_3x_minus_5_from_12x():
    return 3 * _b8l1_solve1(12 * _b8l1_x - 20, 7) - 5


def alg_count_solutions_x_zero_trap():
    word = _b8l1_count(2 * (3 * _b8l1_x - 4), 6 * _b8l1_x - 8 + _b8l1_x)

    def check(choices, idx):
        return choices[idx] == word, f"count -> {word}"

    return check


def alg_parking_additional_hours():
    h = sp.Symbol("h")
    R = _b8l1_R
    return _b8l1_solve1(R(9, 2) + R(9, 4) * (h - 1), R(45, 2), h)


def alg_caterer_guests_literal():
    C, g = sp.symbols("C g")
    return _b8l1_rhs_matches(g, sp.solve(Eq(C, 18 * g + 250), g)[0])


def alg_common_factor_x_minus_2_spr():
    return _b8l1_solve1(5 * (_b8l1_x - 2) - 3 * (_b8l1_x - 2), 14) - 2


def alg_two_thirds_one_fourth_distribute():
    R = _b8l1_R
    return _b8l1_solve1(R(2, 3) * (_b8l1_x - 6), R(1, 4) * (_b8l1_x + 9) + 1)


def alg_silos_equal_grain():
    t = sp.Symbol("t")
    tsol = _b8l1_solve1(500 - 12 * t, 140 - 3 * t, t)
    assert 140 - 3 * tsol == 500 - 12 * tsol
    return 500 - 12 * tsol


def alg_strawberry_crews_rate_spr():
    r = sp.Symbol("r")
    return _b8l1_solve1(_b8l1_R(3, 2) * r * 8 + r * 6, 135, r)


def alg_value_3x_minus_2_structure_spr():
    xs = _b8l1_solve1((3 * _b8l1_x - 2) / 5, (3 * _b8l1_x - 2) / 2 - 6)
    return 3 * xs - 2


def alg_literal_x_two_fractions_abc():
    a, b, c = sp.symbols("a b c", positive=True)
    sol = sp.solve(Eq((_b8l1_x - a) / b, (_b8l1_x + a) / c), _b8l1_x)[0]

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            left, right = _b8l1_parse_eq(ch)
            right = right.subs({sp.Symbol("a"): a, sp.Symbol("b"): b, sp.Symbol("c"): c})
            if sp.simplify(right - sol) == 0:
                hits.append(i)
        return hits == [idx], f"x = {sol}; matching choices {hits}"

    return check


def alg_no_solution_fraction_k():
    k = sp.Symbol("k")
    d = sp.expand(6 * ((k * _b8l1_x + 2) / 3 - (_b8l1_x - 4) / 2))
    ks = sp.solve(Eq(d.coeff(_b8l1_x, 1), 0), k)
    ks = [kv for kv in ks if d.coeff(_b8l1_x, 0).subs(k, kv) != 0]
    assert len(ks) == 1
    return ks[0]


def alg_decimal_mixture_value_40_minus_x():
    R = _b8l1_R
    xs = _b8l1_solve1(R(3, 20) * (40 - _b8l1_x) + R(7, 20) * _b8l1_x, R(1, 4) * (_b8l1_x + 18))
    return 40 - xs


def alg_repeated_binomial_value_5x():
    R = _b8l1_R
    xs = _b8l1_solve1(R(13, 5) * (5 * _b8l1_x - 3) + R(21, 10), R(8, 5) * (5 * _b8l1_x - 3) + R(42, 5))
    return 5 * xs


def alg_pick_one_var_equation_no_solution():
    def check(choices, idx):
        counts = []
        for ch in choices:
            left, right = _b8l1_parse_eq(ch)
            counts.append(_b8l1_count(sp.nsimplify(left), sp.nsimplify(right)))
        hits = [i for i, w in enumerate(counts) if w == "Zero"]
        return hits == [idx], f"counts {counts}"

    return check


# ----- Batch batch8-nf1 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch8-nf1.ts (batch batch8-nf1).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch8_nf1.py --only-extra

Each function derives the answer from the stem's givens: a numeric result for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items
whose choices are points, equations, percents or sentences.
"""



import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq, sqrt

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")
m, d = symbols("m d")


def _b8nf_point(text: str):
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip())


def _b8nf_rhs(choice: str):
    return sp.nsimplify(latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1]))


def _b8nf_same_function(e1, e2, var=x, pts=(-2, -1, 0, Rational(1, 2), 1, 3)):
    return all(sp.simplify(e1.subs(var, v) - e2.subs(var, v)) == 0 for v in pts)


# ------------------------------------------------------------------ easy


def adv_nf_rational_evaluate_at_five():
    return ((2 * x + 10) / (x - 3)).subs(x, 5)


def adv_nf_cubic_x_intercept_point():
    f = (x + 4) * (x - 3) * (2 * x - 5)
    zeros = set(sp.solve(f, x))

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            px, py = _b8nf_point(ch)
            if py == 0 and px in zeros:
                hits.append(i)
        return hits == [idx], f"zeros {sorted(zeros)}; x-intercept choices {hits}"

    return check


def adv_nf_vertex_form_minimum_value():
    f = 4 * (x + 6) ** 2 - 11
    xv = sp.solve(sp.diff(f, x), x)[0]
    assert sp.diff(f, x, 2) > 0
    return f.subs(x, xv)


def adv_nf_channel_followers_weekly_percent():
    w = Symbol("w")
    F = 850 * Rational(106, 100) ** w
    pct = sp.simplify((F.subs(w, 1) - F.subs(w, 0)) / F.subs(w, 0)) * 100  # 6

    def check(choices, idx):
        vals = [sp.nsimplify(latex_to_sympy_ext(ch)) for ch in choices]
        hits = [i for i, v in enumerate(vals) if v == pct]
        return hits == [idx], f"weekly percent increase {pct}; matching choices {hits}"

    return check


def adv_nf_factored_vertex_x_coordinate():
    f = sp.expand((x - 4) * (x + 10))
    return sp.solve(sp.diff(f, x), x)[0]


def adv_nf_composition_quadratic_linear():
    f = sp.Lambda(x, x**2 - 3 * x)
    g = sp.Lambda(x, 2 * x + 1)
    return f(g(3))


# ------------------------------------------------------------------ medium


def adv_nf_radical_input_for_output():
    sols = sp.solve(Eq(2 * sqrt(a + 5) - 1, 11), a)
    sols = [v for v in sols if sp.simplify(2 * sqrt(v + 5) - 1 - 11) == 0]
    assert len(sols) == 1
    return sols[0]


def adv_nf_exponential_input_for_output():
    sols = sp.solve(Eq(5 * 3 ** (x - 2) + 4, 139), x)
    real = [v for v in sols if v.is_real]
    assert len(real) == 1
    return real[0]


def adv_nf_exponential_form_displays_y_intercept():
    f = 3 * 4 ** (x + 1)
    y0 = f.subs(x, 0)

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            rhs = _b8nf_rhs(ch)
            assert _b8nf_same_function(rhs, f), f"choice {i} is not equivalent"
            coeff, _ = rhs.as_independent(x, as_Add=False)
            if coeff == y0:
                hits.append(i)
        return hits == [idx], f"f(0) = {y0}; forms with that coefficient {hits}"

    return check


def adv_nf_hive_half_year_factor():
    bp = Symbol("bp", positive=True)
    sols = sp.solve(Eq(bp**2, Rational(121, 100)), bp)
    assert len(sols) == 1
    tt = Rational(7, 3)
    assert sp.simplify(2000 * Rational(121, 100) ** tt - 2000 * sols[0] ** (2 * tt)) == 0
    return sols[0]


def adv_nf_exponential_from_three_values():
    pts = {1: 6, 2: 18, 4: 162}

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            rhs = _b8nf_rhs(ch)
            if all(rhs.subs(x, xv) == yv for xv, yv in pts.items()):
                hits.append(i)
        return hits == [idx], f"choices through all three points {hits}"

    return check


def adv_nf_museum_visitors_point():
    V = -3 * d**2 + 90 * d
    assert V.subs(d, 10) == 600
    dmax = sp.solve(sp.diff(V, d), d)[0]
    vmax = V.subs(d, dmax)
    total10 = sum(V.subs(d, i) for i in range(1, 11))

    def check(choices, idx):
        key_ok = choices[idx].startswith("On the 10th day") and V.subs(d, 10) == 600
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("600th day" in ch and V.subs(d, 600) != 10)
            or ("greatest number" in ch and vmax != 600)
            or ("a total of 600" in ch and total10 != 600))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"V(10)=600, max {vmax} at d={dmax}, total over 10 days {total10}; contradicted {wrong}"

    return check


def adv_nf_wave_speed_depth():
    sols = sp.solve(Eq(sqrt(Rational(98, 10) * x), 7), x)
    assert len(sols) == 1
    return sols[0]


def adv_nf_rational_shift_x_intercept():
    f = sp.Lambda(x, 1 / x)
    g = f(x + 3) - 2
    sols = sp.solve(Eq(g, 0), x)
    assert len(sols) == 1
    return sols[0]


def adv_nf_island_rabbits_initial():
    ap_, bp_ = symbols("ap bp", positive=True)
    sol = sp.solve([Eq(ap_ * bp_**2, 900), Eq(ap_ * bp_**4, 1296)], [ap_, bp_], dict=True)
    assert len(sol) == 1
    return sol[0][ap_]


def adv_nf_table_shift_scale_evaluate():
    f = {-1: 7, 1: 2, 3: -4, 5: 9}
    return 2 * f[3 - 2] + 1


def adv_nf_quadratic_positive_input():
    sols = sp.solve(Eq(2 * x**2 - 8 * x - 1, 9), x)
    pos = [v for v in sols if v > 0]
    assert len(pos) == 1
    return pos[0]


# ------------------------------------------------------------------ hard


def adv_nf_regression_reflect_shift_max():
    q = a * x**2 + b * x + c
    sol = sp.solve([Eq(q.subs(x, -1), 15), Eq(q.subs(x, 1), 3), Eq(q.subs(x, 5), 27)], [a, b, c])
    f = sp.Lambda(x, q.subs(sol))
    h = 10 - f(x - 2)
    xc = sp.solve(sp.diff(h, x), x)[0]
    assert sp.diff(h, x, 2) < 0
    return h.subs(x, xc)


def adv_nf_exponential_doubling_period():
    f = sp.Lambda(x, 400 * 8 ** (x / 9))
    ratio = sp.simplify(f(x + k) / f(x))  # 8^(k/9), independent of x
    assert not ratio.has(x)
    sols = [v for v in sp.solve(Eq(ratio, 2), k) if v.is_real]
    assert len(sols) == 1
    assert sp.simplify(f(x + sols[0]) - 2 * f(x)) == 0
    return sols[0]


def adv_nf_tea_cooling_constant():
    T = 22 + 68 * Rational(9, 10) ** m
    t0, t1 = T.subs(m, 0), T.subs(m, 1)
    limit = sp.limit(T, m, sp.oo)

    def check(choices, idx):
        key_ok = "gets closer to 22" in choices[idx] and limit == 22
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("when it is poured is 22" in ch and t0 != 22)
            or ("decreases by 22 degrees" in ch and t0 - t1 != 22)
            or ("decreases by 22%" in ch and (t0 - t1) / t0 != Rational(22, 100)))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"T(0)={t0}, T(0)-T(1)={t0 - t1}, limit {limit}; contradicted {wrong}"

    return check


def adv_nf_shifted_exponential_two_points():
    ap_, bp_ = symbols("ap bp", positive=True)
    f = ap_ * bp_**x - 5
    sol = sp.solve([Eq(f.subs(x, 0), 11), Eq(f.subs(x, 2), 139)], [ap_, bp_], dict=True)
    assert len(sol) == 1
    fx = f.subs(sol[0])
    xs = [v for v in sp.solve(Eq(fx, 1291), x) if v.is_real]
    assert len(xs) == 1
    return xs[0]


def adv_nf_factored_plus_c_y_intercept():
    f = (x - 2) * (x - 8) + c
    xv = sp.solve(sp.diff(f, x), x)[0]
    cv = sp.solve(Eq(f.subs(x, xv), -7), c)[0]
    return f.subs(c, cv).subs(x, 0)


def adv_nf_composition_find_linear():
    comp = sp.expand((a * x + b) ** 2 + 1)
    sols = sp.solve(sp.Poly(comp - (4 * x**2 - 12 * x + 10), x).all_coeffs(), [a, b], dict=True)
    sols = [sd for sd in sols if sd[a] > 0]
    assert len(sols) == 1
    return (a * 5 + b).subs(sols[0])


def adv_nf_pen_wall_max_area():
    A = x * (120 - 2 * x)
    xc = sp.solve(sp.diff(A, x), x)[0]
    assert 0 < xc < 60 and sp.diff(A, x, 2) < 0
    return A.subs(x, xc)


def adv_nf_bridge_cable_length_below():
    h = Rational(2, 100) * x**2 - 4 * x + 210
    region = sp.solve_univariate_inequality(h <= 12, x, relational=False)
    region = region.intersect(sp.Interval(0, 200))  # between the towers: h(0) = h(200) = 210
    assert h.subs(x, 0) == h.subs(x, 200)
    return region.measure


def adv_nf_cubic_shift_up_intercept_count():
    g = sp.Poly(sp.expand((x - 1) * (x + 3) ** 2 + 4), x)
    return Integer(len(set(sp.real_roots(g))))


def adv_nf_exponential_input_scale_rewrite():
    f = sp.Lambda(x, 3 * 9**x)
    g = f(x / 2 + 1)
    av = sp.nsimplify(g.subs(x, 0))
    bv = sp.nsimplify(g.subs(x, 1) / g.subs(x, 0))
    assert _b8nf_same_function(g, av * bv**x)
    return av + bv


def adv_nf_quadratic_symmetric_values():
    q = a * x**2 + b * x + c
    sol = sp.solve([Eq(q.subs(x, -1), 12), Eq(q.subs(x, 2), -6), Eq(q.subs(x, 5), 12)], [a, b, c])
    return q.subs(sol).subs(x, 7)


# ----- Batch batch9-le2v1 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch9-le2v1.ts (batch batch9-le2v1).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch9_le2v1.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""

import re


import sympy as sp
from sympy import Eq, Rational, symbols

x, y, a, b, k, p, q = symbols("x y a b k p q")


# ----- helpers (prefix _b9l2_) -----


def _b9l2_line(pts):
    """y as an expression in x for the line through two points."""
    (x1, y1), (x2, y2) = [(sp.nsimplify(u), sp.nsimplify(v)) for u, v in pts]
    m = (y2 - y1) / (x2 - x1)
    return sp.expand(y1 + m * (x - x1))


def _b9l2_slope(expr):
    """Slope of the line expr = 0 (expr linear in x and y)."""
    return sp.solve(expr, y)[0].diff(x)


def _b9l2_eq(choice):
    """'$lhs = rhs$' -> lhs - rhs as a SymPy expression."""
    lhs, rhs = choice.strip().strip("$").split("=")
    return sp.expand(latex_to_sympy_ext(lhs) - latex_to_sympy_ext(rhs))


def _b9l2_point(choice):
    """'$(4, -1)$' or '$(p + 3, q - 4)$' -> tuple of SymPy expressions."""
    inner = choice.strip().strip("$").strip()
    assert inner.startswith("(") and inner.endswith(")"), inner
    parts = inner[1:-1].split(",")
    return tuple(latex_to_sympy(part) for part in parts)


def _b9l2_same_line(e1, e2):
    """True when two linear equations (as expr = 0) describe the same line."""
    s1, s2 = sp.solve(e1, y), sp.solve(e2, y)
    return len(s1) == 1 and len(s2) == 1 and sp.simplify(s1[0] - s2[0]) == 0


def _b9l2_unique(matches, idx, detail):
    return matches == [idx], f"{detail}; matching choices {matches}"


# ----- item checks -----


def alg_slope_standard_form_7x_2y():
    return _b9l2_slope(7 * x + 2 * y - 9)


def alg_point_on_line_5x_3y_17():
    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            px, py = _b9l2_point(ch)
            if 5 * px - 3 * py == 17:
                matches.append(i)
        return _b9l2_unique(matches, idx, "points on 5x - 3y = 17")

    return check


def alg_x_intercept_slope_intercept_form():
    return sp.solve(Eq(0, -4 * x + 10), x)[0]


def alg_slope_from_two_intercepts():
    line = _b9l2_line([(6, 0), (0, -4)])
    return line.diff(x)


def alg_hostel_pillows_term_meaning():
    pp, tt = symbols("p t")
    expr = 12 * pp + 5 * tt
    term = 12 * pp
    coeff, var = term.as_coeff_Mul()
    other = expr - term
    # Each choice names one object; map it to the expression it describes.
    meanings = {
        "number of pillows": var,
        "price, in dollars, of one pillow": coeff,
        "spent on towels": other,
        "spent on pillows": coeff * var,
    }

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            described = [v for key, v in meanings.items() if key in ch]
            assert len(described) == 1, ch
            if sp.simplify(described[0] - term) == 0:
                matches.append(i)
        return _b9l2_unique(matches, idx, "choice describing 12p")

    return check


def alg_two_points_standard_form_equation():
    pts = [(-4, 1), (2, 10)]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            e = _b9l2_eq(ch)
            if all(e.subs({x: px, y: py}) == 0 for px, py in pts):
                matches.append(i)
        return _b9l2_unique(matches, idx, "line through (-4, 1) and (2, 10)")

    return check


def alg_perpendicular_slope_standard_form():
    return -1 / _b9l2_slope(3 * x + 4 * y - 7)


def alg_rewrite_to_standard_form_c():
    # y = -2/5 x + 3  ->  (2/5) x + y = 3; scale so the x-coefficient is 2.
    rhs = -Rational(2, 5) * x + 3
    A, C = -rhs.coeff(x), rhs.subs(x, 0)
    scale = 2 / A
    return scale * C


def alg_intercepts_triangle_area():
    e = 5 * x + 2 * y - 20
    xi = sp.solve(e.subs(y, 0), x)[0]
    yi = sp.solve(e.subs(x, 0), y)[0]
    return Rational(1, 2) * abs(xi) * abs(yi)


def alg_point_slope_to_standard_form():
    given = y - 4 + Rational(3, 5) * (x + 10)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b9l2_same_line(_b9l2_eq(ch), given)]
        return _b9l2_unique(matches, idx, "same line as y - 4 = -3/5 (x + 10)")

    return check


def alg_moving_boxes_table_equation():
    pts = [(0, 12), (6, 8), (15, 2)]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            e = _b9l2_eq(ch)
            if all(e.subs({x: px, y: py}) == 0 for px, py in pts):
                matches.append(i)
        return _b9l2_unique(matches, idx, "equation through all three combinations")

    return check


def alg_club_hoodies_keychains_tradeoff():
    dk = symbols("dk")
    # 8(k + dk) + 20(h + 4) = 8k + 20h  ->  solve for the change in keychains
    change = sp.solve(Eq(8 * dk + 20 * 4, 0), dk)[0]
    return -change


def alg_yarn_twine_combination_spr():
    return _b9l2_line([(2, 12), (6, 6)]).subs(x, 8)


def alg_slope_constant_x_intercept_spr():
    kv = sp.solve(Eq(_b9l2_slope(k * x + 2 * y - 10), 3), k)[0]
    return sp.solve((kv * x + 2 * y - 10).subs(y, 0), x)[0]


def alg_perpendicular_shared_x_intercept():
    given = 3 * x - 4 * y - 12
    xi = sp.solve(given.subs(y, 0), x)[0]
    m = -1 / _b9l2_slope(given)
    target = y - m * (x - xi)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b9l2_same_line(_b9l2_eq(ch), target)]
        return _b9l2_unique(matches, idx, f"line y = {m}(x - {xi})")

    return check


def alg_point_shift_stays_on_line():
    q_of_p = sp.solve(Eq(4 * p - 3 * q, 10), q)[0]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            px, py = _b9l2_point(ch)
            if sp.simplify((4 * px - 3 * py - 10).subs(q, q_of_p)) == 0:
                matches.append(i)
        return _b9l2_unique(matches, idx, "points on 4x - 3y = 10 for every (p, q)")

    return check


def alg_shared_y_intercept_x_intercept_spr():
    yi = sp.solve((2 * x + 5 * y - 15).subs(x, 0), y)[0]
    line = _b9l2_line([(0, yi), (3, -2)])
    return sp.solve(line, x)[0]


def alg_barge_containers_slope_meaning():
    pat = re.compile(r"Adding (\d+) (small|large) containers? requires (adding|removing) (\d+) (small|large)")
    slope = _b9l2_slope(3 * x + 12 * y - 180)  # x = small, y = large

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            m = pat.search(ch)
            assert m, ch
            n1, kind1, verb, n2, kind2 = m.groups()
            d = {"small": 0, "large": 0}
            d[kind1] += int(n1)
            d[kind2] += int(n2) if verb == "adding" else -int(n2)
            # a change keeps the load full exactly when it moves along the line
            if d["small"] != 0 and sp.Rational(d["large"], d["small"]) == slope:
                matches.append(i)
        return _b9l2_unique(matches, idx, f"slope {slope}")

    return check


def alg_ribbon_pieces_unit_equation():
    # In meters: 0.3 a + 1.2 b = 45. Valid choices are proportional to this.
    target = [Rational(30, 100), Rational(12, 10), Rational(-45)]

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            e = _b9l2_eq(ch)
            vec = [e.coeff(a), e.coeff(b), e.subs({a: 0, b: 0})]
            ratio = vec[0] / target[0]
            if all(sp.simplify(v - ratio * t_) == 0 for v, t_ in zip(vec, target)):
                matches.append(i)
        return _b9l2_unique(matches, idx, "proportional to 0.3a + 1.2b = 45")

    return check


def alg_fudge_toffee_intercepts_difference():
    grams = 9 * 1000
    f_only = sp.solve(Eq(450 * x, grams), x)[0]
    t_only = sp.solve(Eq(300 * y, grams), y)[0]
    return t_only - f_only


def alg_parallel_through_point_which_point():
    m = _b9l2_slope(4 * x + 6 * y - 5)
    line = 7 + m * (x + 3)

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            px, py = _b9l2_point(ch)
            if line.subs(x, px) == py:
                matches.append(i)
        return _b9l2_unique(matches, idx, f"points on y = {sp.expand(line)}")

    return check


# ----- Batch batch9-psdaD -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch9-psdaD.ts (batch batch9-psdaD).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch9_psdaD.py --only-extra

Numeric items return the exact SymPy value. Items with sentence or interval
choices return a callable (choices, answer_index) -> (ok, detail) that derives
the decision (interval, overlap, design flags) from the stem's givens and then
checks that exactly the key choice states it.
"""



import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq, sqrt

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")


def _b9pd_pick(predicate, label):
    """Callable that accepts the item when exactly the key choice satisfies predicate."""

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices) if predicate(ch)]
        return hits == [idx], f"{label}; matching choices {hits}"

    return check


def _b9pd_interval(est, moe):
    return est - moe, est + moe


def _b9pd_fmt(v):
    """Format a whole number with thousands separators, as in the choice text."""
    return f"{int(v):,}"


# ----- Inference from sample statistics and margin of error -----


def _b9pd_library_overdue():
    return Integer(3600) * Rational(18, 120)


def _b9pd_bolts_not_defective():
    return Integer(12500) * (1 - Rational(6, 250))


def _b9pd_ev_upper_total():
    lo, hi = _b9pd_interval(Rational(30, 100), Rational(4, 100))
    return Integer(84000) * hi


def _b9pd_occupants_total():
    return Integer(3500) * Rational(24, 10)


def _b9pd_orchard_least_total():
    lo, hi = _b9pd_interval(Integer(42), Integer(3))
    return Integer(650) * lo


def _b9pd_plausible_proportion():
    lo, hi = _b9pd_interval(Rational(62, 100), Rational(4, 100))

    def check(choices, idx):
        vals = [sp.nsimplify(latex_to_sympy(ch)) for ch in choices]
        hits = [i for i, v in enumerate(vals) if lo <= v <= hi]
        return hits == [idx], f"interval [{lo}, {hi}]; choices inside {hits}"

    return check


def _b9pd_smaller_margin():
    import re

    n0 = 250

    def ok(ch):
        m = re.search(r"random sample of ([\d,]+) visitors", ch)
        return bool(m) and int(m.group(1).replace(",", "")) > n0

    return _b9pd_pick(ok, "larger random sample than 250 lowers the margin of error")


def _b9pd_commute_intervals():
    a_lo, a_hi = _b9pd_interval(Rational(245, 10), Rational(12, 10))
    b_lo, b_hi = _b9pd_interval(Rational(279, 10), Rational(15, 10))
    if b_lo > a_hi:
        phrase = "mean commute time of all adults in town B is greater"
    elif a_lo > b_hi:
        phrase = "mean commute time of all adults in town A is greater"
    else:
        phrase = "no convincing evidence"
    return _b9pd_pick(lambda ch: phrase in ch and "every adult" not in ch,
                      f"A [{a_lo}, {a_hi}], B [{b_lo}, {b_hi}] -> '{phrase}'")


def _b9pd_greenhouse_overlap():
    p_lo, p_hi = _b9pd_interval(Integer(48), Integer(3))
    q_lo, q_hi = _b9pd_interval(Integer(41), Integer(5))
    overlap = max(p_lo, q_lo) <= min(p_hi, q_hi)
    phrase = "no convincing evidence" if overlap else "greater percentage of all seeds planted in greenhouse P"
    return _b9pd_pick(lambda ch: phrase in ch,
                      f"P [{p_lo}, {p_hi}], Q [{q_lo}, {q_hi}], overlap={overlap} -> '{phrase}'")


def _b9pd_dog_park():
    lo, hi = _b9pd_interval(Integer(53), Integer(4))
    below_half_plausible = lo < 50

    def ok(ch):
        if "plausible that less than 50% of all residents" in ch:
            return below_half_plausible
        if "certainly" in ch:
            return lo > 50
        return False  # "exactly" and statements about the 600 surveyed are never supported

    return _b9pd_pick(ok, f"interval [{lo}, {hi}]; below 50 plausible={below_half_plausible}")


def _b9pd_garden_interval():
    lo, hi = _b9pd_interval(Rational(35, 100), Rational(3, 100))
    lo_n, hi_n = Integer(9200) * lo, Integer(9200) * hi
    target = f"From {_b9pd_fmt(lo_n)} to {_b9pd_fmt(hi_n)}"
    return _b9pd_pick(lambda ch: ch.strip() == target, f"plausible counts {target}")


def _b9pd_bus_delay():
    import re

    lo, hi = _b9pd_interval(Rational(48, 10), Rational(6, 10))

    def ok(ch):
        m = re.search(r"plausibly ([\d.]+) minutes", ch)
        if m:
            v = sp.nsimplify(m.group(1))
            return lo <= v <= hi
        return False  # "exactly" the sample mean, and claims about every trip, are not supported

    return _b9pd_pick(ok, f"interval [{lo}, {hi}]")


def _b9pd_books_larger_sample():
    return Rational(18, 10) * sqrt(Rational(400, 1600))


# ----- Evaluating statistical claims -----


def _b9pd_online_poll():
    self_selected = True
    return _b9pd_pick(lambda ch: self_selected and "selected themselves" in ch,
                      "respondents chose to respond -> voluntary response bias")


def _b9pd_plant_food_assignment():
    return _b9pd_pick(lambda ch: "attributed to the plant food" in ch,
                      "random assignment balances other variables so the effect is attributable to the treatment")


def _b9pd_study(random_selection: bool, random_assignment: bool, population: str):
    causal = "causes" if random_assignment else "is associated with"

    def ok(ch):
        if not ch.startswith("Daily walking " + causal):
            return False
        if random_selection:
            return population in ch and "all adults" not in ch
        return "all adults" not in ch and population not in ch

    return _b9pd_pick(ok, f"random selection={random_selection}, random assignment={random_assignment}")


def _b9pd_walking():
    return _b9pd_study(random_selection=True, random_assignment=False, population="adults in the county")


def _b9pd_green_tea_change():
    return _b9pd_pick(lambda ch: "Randomly assigning" in ch,
                      "only random assignment supports a causal conclusion")


def _b9pd_placebo():
    return _b9pd_pick(lambda ch: "effect of the ingredient from the effect of simply applying" in ch,
                      "placebo control isolates the active ingredient")


def _b9pd_weekday_shoppers():
    sampled = "All customers who shopped at the store on weekday mornings during that month"
    return _b9pd_pick(lambda ch: ch.strip() == sampled, "generalize to the sampled population only")


def _b9pd_fitness_bias():
    # Sample drawn where exercise is above average -> estimate biased upward.
    direction = "too high"
    return _b9pd_pick(lambda ch: direction in ch, f"convenience sample at a fitness center -> {direction}")


def _b9pd_screen_time():
    random_selection, random_assignment = False, False

    def ok(ch):
        claims_cause = "causes" in ch
        claims_general = "all people" in ch or "people like those" in ch
        return claims_cause == random_assignment and claims_general == random_selection

    return _b9pd_pick(ok, "no random selection, no random assignment")


def _b9pd_hens():
    population = 900
    return _b9pd_pick(lambda ch: f"All {population} hens on the farm" in ch,
                      "random selection from the farm's 900 hens + random assignment")


def _b9pd_practice_app():
    return _b9pd_pick(lambda ch: "chose to use the app may differ" in ch,
                      "self-selected treatment -> confounding")


# ----- Probability and conditional probability -----


def _b9pd_red_cards():
    return Rational(15, 40)


def _b9pd_seed_varieties():
    sprouted = symbols("sprouted", positive=True)
    total_sprouted = sp.solve(Eq(Rational(5, 8) * sprouted, 40), sprouted)[0]
    b_sprouted = total_sprouted - 40
    return Integer(40) - b_sprouted


def _b9pd_museum():
    no_tour = 300 - 180
    audio_no_tour = 110 - 65
    return Rational(audio_no_tour, no_tour)


def _b9pd_shelter():
    dogs = 120 - 45
    young_dogs = Rational(40, 100) * dogs
    u = symbols("u", positive=True)
    young_total = sp.solve(Eq(Rational(3, 5) * u, young_dogs), u)[0]
    return (young_total - young_dogs) / 45


# ----- Batch batch9-circ -----
import sympy as sp
from sympy import Rational, Eq, pi, sqrt, cos, sin

_b9ci_x, _b9ci_y, _b9ci_r, _b9ci_t, _b9ci_k, _b9ci_h = sp.symbols("x y r theta k h")
X, Y = _b9ci_x, _b9ci_y


# ----------------------------------------------------------------------------- helpers


def _b9ci_circle(expr):
    """x^2 + y^2 + Dx + Ey + F (any common leading coefficient) -> (center Point, r^2)."""
    poly = sp.Poly(sp.expand(expr), X, Y)
    lead = poly.coeff_monomial(X**2)
    assert lead != 0 and poly.coeff_monomial(Y**2) == lead and poly.coeff_monomial(X * Y) == 0
    d, e, f = (poly.coeff_monomial(m) / lead for m in (X, Y, 1))
    h0, k0 = -d / 2, -e / 2
    return sp.Point(h0, k0), h0**2 + k0**2 - f


def _b9ci_choice_circle(choice):
    lhs, rhs = _split_equation(choice)
    return _b9ci_circle(lhs - rhs)


def _b9ci_pick_circle(center, r2):
    """Callable: exactly the key choice is the circle with this center and r^2."""

    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            c0, rr = _b9ci_choice_circle(ch)
            if c0 == center and sp.simplify(rr - r2) == 0:
                good.append(i)
        return good == [idx], f"circle center {center}, r^2 = {r2}; matching choices {good}"

    return check


def _b9ci_point(text):
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.Point(sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip()))


# ----------------------------------------------------------------------------- easy


def geo_circ_equation_from_center_radius():
    return _b9ci_pick_circle(sp.Point(-3, 5), sp.Integer(6) ** 2)


def geo_circ_sector_radians_area_easy():
    return Rational(1, 2) * 10**2 * Rational(15, 10)


def geo_circ_skating_rink_arc():
    return sp.Integer(30) * Rational(12, 10)


def geo_circ_point_on_standard_form():
    expr = (X + 4) ** 2 + (Y - 3) ** 2 - 100

    def check(choices, idx):
        on = [i for i, ch in enumerate(choices) if expr.subs({X: _b9ci_point(ch).x, Y: _b9ci_point(ch).y}) == 0]
        return on == [idx], f"choices on the circle: {on}"

    return check


# ----------------------------------------------------------------------------- medium


def geo_circ_unit_circle_point_coordinates():
    ang = Rational(4, 3) * pi
    target = sp.Point(cos(ang), sin(ang))

    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            inner = ch.strip().strip("$").replace("\\left(", "").replace("\\right)", "")
            xs, ys = inner.split(",")
            pt = sp.Point(latex_to_sympy_ext(xs), latex_to_sympy_ext(ys))
            if sp.simplify(pt.distance(target)) == 0:
                good.append(i)
        return good == [idx], f"P = {target}; matching choices {good}"

    return check


def geo_circ_sprinkler_sector_radius():
    sols = sp.solve(Eq(Rational(80, 360) * pi * _b9ci_r**2, 32 * pi), _b9ci_r)
    return [s for s in sols if s > 0][0]


def geo_circ_line_through_center_greatest_y():
    sols = sp.solve([Eq(Y, X + 1), Eq((X - 3) ** 2 + (Y - 4) ** 2, 8)], [X, Y], dict=True)
    assert len(sols) == 2
    return max(s[Y] for s in sols)


def geo_circ_translate_left_up():
    c0, r2 = _b9ci_circle((X - 1) ** 2 + (Y + 6) ** 2 - 20)
    return _b9ci_pick_circle(sp.Point(c0.x - 4, c0.y + 3), r2)


def geo_circ_chord_distance_radius():
    return sqrt((Rational(30, 2)) ** 2 + 8**2)


def geo_circ_clock_minute_hand_arc():
    angle = sp.Integer(40) * 360 / 60
    return angle / 360 * 2 * pi * 9


def geo_circ_diameter_endpoints_equation():
    a, b = sp.Point(-3, 4), sp.Point(5, -2)
    return _b9ci_pick_circle(a.midpoint(b), (a.distance(b) / 2) ** 2)


def geo_circ_point_inside_expanded():
    expr = X**2 + Y**2 + 6 * X - 8 * Y

    def check(choices, idx):
        inside = [i for i, ch in enumerate(choices) if expr.subs({X: _b9ci_point(ch).x, Y: _b9ci_point(ch).y}) < 0]
        return inside == [idx], f"choices inside the circle: {inside}"

    return check


# ----------------------------------------------------------------------------- hard


def geo_circ_tangent_x_axis_constant():
    center, r2 = _b9ci_circle(X**2 + Y**2 + 10 * X - 6 * Y + _b9ci_k)
    kval = sp.solve(Eq(r2, center.y**2), _b9ci_k)[0]
    # Tangency: y = 0 meets the circle in a double root.
    roots = sp.roots(sp.Poly((X**2 + 10 * X + kval), X))
    assert len(roots) == 1 and list(roots.values())[0] == 2
    return kval


def geo_circ_leading_coefficient_radius():
    _, r2 = _b9ci_circle(2 * X**2 + 2 * Y**2 - 12 * X + 20 * Y + 18)
    return sqrt(r2)


def geo_circ_two_circles_common_chord():
    sols = sp.solve([Eq(X**2 + Y**2, 25), Eq((X - 9) ** 2 + Y**2, 52)], [X, Y], dict=True)
    assert len(sols) == 2
    p1, p2 = (sp.Point(s_[X], s_[Y]) for s_ in sols)
    return p1.distance(p2)


def geo_circ_sector_arc_area_radius():
    sols = sp.solve([Eq(_b9ci_r * _b9ci_t, 6 * pi), Eq(Rational(1, 2) * _b9ci_r**2 * _b9ci_t, 27 * pi)],
                    [_b9ci_r, _b9ci_t], dict=True)
    return [s[_b9ci_r] for s in sols if s[_b9ci_r] > 0][0]


def geo_circ_fountain_tangent_path():
    return sqrt(6**2 + 8**2) - 6


def geo_circ_wiper_blade_region():
    th = Rational(2, 3) * pi
    return Rational(1, 2) * 28**2 * th - Rational(1, 2) * 10**2 * th


def geo_circ_radian_central_inscribed():
    central_deg = Rational(5, 9) * pi * 180 / pi
    return central_deg / 2


def geo_circ_center_h_through_point():
    sols = sp.solve(Eq((1 - _b9ci_h) ** 2 + (7 - 3) ** 2, 25), _b9ci_h)
    return [s for s in sols if s > 0][0]


# ----- Batch batch9-ee2 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch9-ee2.ts (batch batch9-ee2).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch9_ee2.py --only-extra

Each function derives the answer from the stem's givens: a numeric result for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items
whose choices are expressions.
"""



import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq, sqrt

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")
d, w = symbols("d w")


def _b9e2_expr_check(expected, samples, label=""):
    """MC with expression choices: exactly the key equals `expected` at every sample point."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            try:
                expr = latex_to_sympy_ext(ch)
            except Exception as e:  # noqa: BLE001
                return False, f"could not parse choice {i} {ch!r}: {e}"
            if all(abs(complex((expr - expected).subs(sv).evalf(30))) < 1e-12 for sv in samples):
                matches.append(i)
        return matches == [idx], f"{label or expected}; matching choices {matches}, key index {idx}"

    return check


def _b9e2_coeffs(identity, unknowns):
    """Solve a polynomial identity in x (expression == 0 for all x) for the unknown constants."""
    return sp.solve(sp.Poly(sp.expand(identity), x).all_coeffs(), unknowns, dict=True)


# x samples avoid 0, -3, 3, -8 and other excluded values; all positive ones also serve x > 0 items.
_B9E2_X = [{x: v} for v in (Rational(1, 3), Rational(3, 2), Rational(7, 2), 5, 7, 11)]
_B9E2_XR = [{x: v} for v in (Rational(-5, 2), Rational(-1, 2), Rational(1, 3), Rational(3, 2), 5, 11)]
_B9E2_XY = [{x: xv, y: yv} for xv, yv in ((1, 2), (3, Rational(1, 2)), (Rational(2, 5), 4), (7, 3))]


# ------------------------------------------------------------------ easy


def adv_expand_monomial_two_binomials():
    expr = sp.expand(2 * x * (x + 3) * (x - 4))
    assert expr == 2 * x**3 - 2 * x**2 - 24 * x
    return _b9e2_expr_check(expr, _B9E2_XR, label=str(expr))


def adv_exponential_shift_coefficient():
    expr = 5 * 3 ** (x + 2)
    return _b9e2_expr_check(expr, _B9E2_XR, label="5*3^(x+2) = 45*3^x")


def adv_negative_exponents_product_two_variable():
    expr = sp.powsimp(x**-3 * y**2 * x**5 * y**-4)
    assert sp.simplify(expr - x**2 / y**2) == 0
    return _b9e2_expr_check(expr, _B9E2_XY, label=str(expr))


def adv_poly_sum_difference_coefficient_total():
    expr = sp.expand((3 * x**2 + 2 * x - 7) + (x**2 - 6 * x + 4) - (2 * x**2 - x - 1))
    co = sp.Poly(expr, x).all_coeffs()
    assert len(co) == 3
    return sum(co)


def adv_floor_tile_area_square_binomial():
    side = x + 4
    return _b9e2_expr_check(sp.expand(side**2), _B9E2_X, label="(x+4)^2")


# ---------------------------------------------------------------- medium


def adv_long_division_linear_negative_remainder():
    q, rem = sp.div(2 * x**2 + 5 * x - 4, x + 3, x)
    assert (q, rem) == (2 * x - 1, -1)
    expected = (2 * x**2 + 5 * x - 4) / (x + 3)
    return _b9e2_expr_check(expected, _B9E2_XR, label=f"quotient {q}, remainder {rem}")


def adv_rationalize_radical_difference_denominator():
    expected = 6 / (sqrt(x + 3) - sqrt(x))
    assert sp.simplify(sp.radsimp(expected) - (2 * sqrt(x + 3) + 2 * sqrt(x))) == 0
    return _b9e2_expr_check(expected, _B9E2_X, label="6/(sqrt(x+3)-sqrt(x))")


def adv_fractional_negative_exponent_power_two_variable():
    xp, yp = symbols("x y", positive=True)
    e = (xp ** Rational(1, 2) * yp**-3) ** -2 * xp**2 * yp**-4
    assert sp.simplify(e - xp * yp**2) == 0
    expected = e.subs({xp: x, yp: y})
    return _b9e2_expr_check(expected, _B9E2_XY, label="x*y^2")


def adv_exponential_difference_rewrite_coefficient():
    expected = 3 ** (x + 2) - 3**x
    return _b9e2_expr_check(expected, _B9E2_XR, label="3^(x+2) - 3^x")


def adv_perfect_square_identity_ab():
    sols = _b9e2_coeffs((a * x + b) ** 2 - (9 * x**2 - 24 * x + 16), [a, b])
    pos = [sv for sv in sols if sv[a] > 0]
    assert len(pos) == 1
    return pos[0][a] * pos[0][b]


def adv_difference_of_binomial_squares_factor():
    expected = (2 * x + 3) ** 2 - (x - 1) ** 2
    assert sp.factor(expected) == (x + 4) * (3 * x + 2)
    return _b9e2_expr_check(expected, _B9E2_XR, label=str(sp.factor(expected)))


def adv_complex_fraction_sum_numerator():
    expected = (2 / x + Rational(1, 4)) / ((x + 8) / 2)
    assert sp.simplify(expected - 1 / (2 * x)) == 0
    return _b9e2_expr_check(expected, _B9E2_XR, label="1/(2x)")


def adv_storage_bin_volume_three_binomials():
    volume = sp.expand((x + 3) * (x + 2) * (x - 1))
    return _b9e2_expr_check(volume, _B9E2_X, label=str(volume))


def adv_parallel_resistance_complex_fraction():
    expected = 1 / (1 / x + 1 / (x + 6))
    return _b9e2_expr_check(expected, _B9E2_X, label=str(sp.cancel(expected)))


# ---------------------------------------------------------------- hard


def adv_moss_area_exponential_rewrite_a():
    expr = 6 * Integer(4) ** ((w + 3) / 2)
    a_val = expr.subs(w, 0)
    b_val = sp.simplify(expr.subs(w, 1) / a_val)
    for wv in (0, 1, Rational(5, 2), 7):
        assert sp.simplify(expr.subs(w, wv) - a_val * b_val**wv) == 0
    assert b_val == 2
    return a_val


def adv_quartic_hidden_difference_squares():
    expected = x**4 + 2 * x**2 + 9
    return _b9e2_expr_check(expected, _B9E2_XR, label="(x^2+3)^2 - (2x)^2")


def adv_three_factor_coefficient_sum():
    co = sp.Poly(sp.expand((x - 2) * (x + 3) * (2 * x - 1)), x).all_coeffs()
    assert len(co) == 4
    return sum(co)


def adv_long_division_missing_term_cubic():
    q, rem = sp.div(x**3 - 8 * x + 5, x - 3, x)
    assert (q, rem) == (x**2 + 3 * x + 1, 8)
    expected = (x**3 - 8 * x + 5) / (x - 3)
    return _b9e2_expr_check(expected, _B9E2_XR, label=f"quotient {q}, remainder {rem}")


def adv_negative_exponent_complex_fraction_two_variable():
    expected = (x**-2 - y**-2) / (x**-1 - y**-1)
    assert sp.simplify(expected - (x + y) / (x * y)) == 0
    return _b9e2_expr_check(expected, _B9E2_XY, label="(x+y)/(xy)")


def adv_exponential_product_base_half():
    expected = 2 ** (2 * x + 3) * 8 ** (1 - x)
    return _b9e2_expr_check(expected, _B9E2_XR, label="2^(6-x)")


def adv_rationalize_conjugate_a_plus_b():
    val = sp.radsimp((sqrt(5) + 1) / (sqrt(5) - 1))
    val = sp.expand(val)
    b_val = val.coeff(sqrt(5))
    a_val = sp.expand(val - b_val * sqrt(5))
    assert a_val.is_Rational and b_val.is_Rational
    return a_val + b_val


def adv_quartic_product_identity_ab():
    sols = _b9e2_coeffs((x**2 + a * x + 2) * (x**2 + b * x + 2) - (x**4 - 5 * x**2 + 4), [a, b])
    prods = {sp.simplify(sv[a] * sv[b]) for sv in sols}
    assert len(prods) == 1
    return prods.pop()


def adv_radical_exponents_two_variable_a_minus_b():
    xp, yp = symbols("x y", positive=True)
    e = sp.root(xp**2 * yp, 3) * sqrt(xp * yp**3) / (xp ** Rational(-1, 3) * yp**2)
    e = sp.powsimp(sp.expand_power_base(e, force=True), force=True)
    # Read exponents directly from the simplified power product.
    powers = sp.Mul.make_args(e)
    exps = {}
    for f in powers:
        base, ex = f.as_base_exp()
        exps[base] = exps.get(base, 0) + ex
    a_val, b_val = exps[xp], exps[yp]
    assert sp.simplify(e - xp**a_val * yp**b_val) == 0
    return a_val - b_val


# ----- Batch batch10-lf2 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch10-lf2.ts (batch batch10-lf2).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch10_lf2.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""

import math


import sympy as sp
from sympy import Eq, Rational, symbols

x, y, t, k, a, b, c, p, q, n = symbols("x y t k a b c p q n")


# ----- helpers (prefix _b10lf_) -----


def _b10lf_line(p1, p2, var=x):
    """The linear expression in var through two points (exact)."""
    (x1, y1), (x2, y2) = [(sp.nsimplify(u), sp.nsimplify(v)) for u, v in (p1, p2)]
    m = (y2 - y1) / (x2 - x1)
    return sp.expand(y1 + m * (var - x1))


def _b10lf_slope(expr, var=x):
    return sp.Poly(sp.expand(expr), var).coeff_monomial(var)


def _b10lf_rhs(choice, var):
    """'$V(t) = 18,000 - 2,160t$' -> right side as SymPy, in terms of x."""
    rhs = choice.strip().strip("$").split("=", 1)[1]
    expr = latex_to_sympy(rhs)
    return sp.nsimplify(expr.subs(sp.Symbol(str(var)), x), rational=True)


def _b10lf_rhs_matches(expected, var=x):
    """MC check for 'F(v) = ...' choices: exactly the key's right side equals expected (in x)."""
    expected = sp.expand(expected.subs(var, x)) if var != x else sp.expand(expected)

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices) if sp.expand(_b10lf_rhs(ch, var) - expected) == 0]
        return hits == [idx], f"expected {expected}; matching choices {hits}"

    return check


def _b10lf_std_form_matches(line_expr):
    """MC check for 'Ax + By = C' choices: exactly the key describes y = line_expr."""

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            lhs, rhs = ch.strip().strip("$").split("=")
            eq = latex_to_sympy(lhs) - latex_to_sympy(rhs)
            sol = sp.solve(eq, y)
            if len(sol) == 1 and sp.expand(sol[0] - line_expr) == 0:
                hits.append(i)
        return hits == [idx], f"y = {line_expr}; matching choices {hits}"

    return check


def _b10lf_sentences(truth_by_phrase):
    """Sentence choices: each choice must contain exactly one known phrase; the key's
    claim is true and every distractor's claim is false (claims computed below)."""

    def check(choices, idx):
        verdicts = []
        for ch in choices:
            found = [truth for phrase, truth in truth_by_phrase.items() if phrase in ch]
            if len(found) != 1:
                return False, f"choice {ch!r} matched {len(found)} phrases"
            verdicts.append(bool(found[0]))
        true_idx = [i for i, v in enumerate(verdicts) if v]
        return true_idx == [idx], f"true claims at {true_idx}"

    return check


# ----- item checks -----


def alg_lf_uneven_table_slope():
    pts = [(-2, 13), (1, 4), (7, -14)]
    line = _b10lf_line(pts[0], pts[2])
    assert all(line.subs(x, px) == py for px, py in pts), "table is not linear"
    return _b10lf_slope(line)


def alg_lf_increase_between_inputs():
    f = 4 * x - 13
    return f.subs(x, 5) - f.subs(x, 2)


def alg_lf_table_scaled_shifted_value():
    pts = [(1, 10), (4, -2), (9, -22)]
    f = _b10lf_line(pts[0], pts[2])
    assert all(f.subs(x, px) == py for px, py in pts)
    g = 3 * f.subs(x, x - 1)
    return g.subs(x, 5)


def alg_lf_hiking_club_year_input():
    M = 35 * t + 1450
    return M.subs(t, 2018 - 2010)


def alg_lf_fraction_rule_input_spr():
    sol = sp.solve(Eq((3 * x - 8) / 2, 14), x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_decimal_rate_zero_input():
    sol = sp.solve(Eq(12 - Rational(2, 5) * x, 0), x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_table_missing_output_k():
    g = _b10lf_line((-3, 11), (6, -16))
    return g.subs(x, 1)


def alg_lf_scaled_shifted_rule():
    f = 2 * x - 5
    g = 3 * f.subs(x, x - 1)
    return _b10lf_rhs_matches(g)


def alg_lf_k_coefficient_and_term():
    f = k * x + 2 * k
    ks = sp.solve(Eq(f.subs(x, 3), 20), k)
    assert len(ks) == 1
    return f.subs({k: ks[0], x: 7})


def alg_lf_oven_percent_depreciation():
    price = 18000
    V = price - Rational(12, 100) * price * t
    return _b10lf_rhs_matches(V, var=t)


def alg_lf_table_standard_form_match():
    pts = [(-2, -1), (2, 5), (8, 14)]
    h = _b10lf_line(pts[0], pts[2])
    assert all(h.subs(x, px) == py for px, py in pts)
    return _b10lf_std_form_matches(h)


def alg_lf_charging_stations_since_2010():
    N = _b10lf_line((2012 - 2010, 40), (2020 - 2010, 112), var=t)
    return _b10lf_rhs_matches(N, var=t)


def alg_lf_compare_increase_interval():
    f = Rational(5, 2) * x - 4
    g = _b10lf_line((-1, 3), (5, 21))
    inc = lambda h: h.subs(x, 8) - h.subs(x, 0)  # noqa: E731
    return inc(g) - inc(f)


def alg_lf_tote_bags_budget_spr():
    C = Rational(11, 4) * x + 18
    bound = sp.solve(Eq(C, 100), x)[0]
    best = math.floor(bound)
    assert C.subs(x, best) <= 100 < C.subs(x, best + 1)
    return sp.Integer(best)


def alg_lf_calf_weight_shifted_input():
    W = Rational(12, 5) * (t - 5) + 86
    rate = sp.diff(W, t)
    return _b10lf_sentences({
        "at birth": W.subs(t, 0) == 86,
        "86 kilograms each week": rate == 86,
        "86 kilograms 5 weeks after birth": W.subs(t, 5) == 86,
        "in its first 5 weeks": W.subs(t, 5) - W.subs(t, 0) == 86,
    })


def alg_lf_transit_card_x_intercept():
    B = _b10lf_line((32, 0), (33, Rational(-9, 4)))  # slope -2.25 through (32, 0)
    rate = -_b10lf_slope(B)
    return _b10lf_sentences({
        "Each ride costs 32.00": rate == 32,
        "starting balance is 32.00": B.subs(x, 0) == 32,
        "balance is 2.25": B.subs(x, 32) == Rational(9, 4),
        "balance is 0 dollars": B.subs(x, 32) == 0,
    })


def alg_lf_decrease_over_interval_spr():
    f = _b10lf_line((-3, 7), (9, -2))
    return f.subs(x, 0) - f.subs(x, 20)


def alg_lf_constants_in_outputs_spr():
    f = a * x + b
    sol = sp.solve([Eq(f.subs(x, 1), 2 * a + 1), Eq(f.subs(x, 3), 21)], [a, b], dict=True)
    assert len(sol) == 1
    return f.subs(sol[0]).subs(x, 5)


def alg_lf_two_machines_equal_value():
    A = 24000 - Rational(10, 100) * 24000 * t
    B = 15000 - 1200 * t
    sol = sp.solve(Eq(A, B), t)
    assert len(sol) == 1 and A.subs(t, sol[0]) > 0
    return sol[0]


def alg_lf_seabird_shifted_base_year():
    P = Rational(18, 5) * t + 210
    Q = P.subs(t, x + (2015 - 2010))
    return _b10lf_rhs_matches(Q)


def alg_lf_shift_scale_from_two_values():
    f = _b10lf_line((2, 5), (6, -3))
    g = 3 * f.subs(x, x - 1)
    return g.subs(x, 0)


def alg_lf_two_intervals_intersection_spr():
    f = _b10lf_line((-2, 4), (6, 24))
    g = _b10lf_line((-2, 40), (6, 0))
    sol = sp.solve(Eq(f, g), x)
    assert len(sol) == 1
    return sol[0]


def alg_lf_shirts_profit_least_number():
    C = Rational(25, 2) * x + 450
    profit = 20 * x - C
    bound = sp.solve(Eq(profit, 200), x)[0]
    least = math.ceil(bound)
    assert profit.subs(x, least) >= 200 > profit.subs(x, least - 1)
    return sp.Integer(least)


def alg_lf_point_slope_equivalent():
    f = Rational(-3, 2) * (x + 4) + 10  # rate -3 per +2 in x, through (-4, 10)
    return _b10lf_rhs_matches(f)


def alg_lf_swapped_points_constant_c():
    m = sp.Symbol("m")
    f = m * x + 7  # f(0) = 7
    sols = sp.solve([Eq(f.subs(x, 2), c), Eq(f.subs(x, c), 2)], [m, c], dict=True)
    vals = {s[c] for s in sols if s[c] != 2}
    assert len(vals) == 1, vals
    return vals.pop()


def alg_lf_output_difference_input_gap():
    f = 5 - Rational(4, 5) * x
    d = sp.Symbol("d")
    diff = sp.expand(f.subs(x, p) - f.subs(x, q))
    sol = sp.solve(Eq(diff.subs(p, q + d), 6), d)
    assert len(sol) == 1
    return sol[0]


def alg_lf_table_two_unknown_outputs():
    m = sp.Symbol("m")
    r = 8 + m * (x + 1)  # passes through (-1, 8)
    av, bv = r.subs(x, -6), r.subs(x, 9)
    ms = sp.solve(Eq(bv - av, 30), m)
    assert len(ms) == 1
    return av.subs(m, ms[0])


def alg_lf_composed_integer_count():
    f = lambda u: 4 * u + 9  # noqa: E731
    g = sp.expand(f(2 * x - 3))
    count = sum(1 for nn in range(1, 1000) if g.subs(x, nn) < 100)
    return sp.Integer(count)


# ----- Batch batch10-ne2 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch10-ne2.ts (batch batch10-ne2).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch10_ne2.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers (radicals, words, points, equations).
"""

import re


import sympy as sp
from sympy import Eq, Rational, Symbol, sqrt, symbols

x, y, k, b, c, t = symbols("x y k b c t")


# ----- helpers (prefix _b10ne_) -----

_B10NE_COUNT_WORDS = {0: "Zero", 1: "Exactly one", 2: "Exactly two", 3: "Exactly three", 4: "Exactly four"}


def _b10ne_real_roots(expr, var=x):
    """Distinct real roots of a polynomial or rational expression in var."""
    vr = Symbol(str(var), real=True)
    return sorted(set(sp.solve(sp.together(expr).subs(var, vr), vr)))


def _b10ne_valid(expr, root, var=x):
    """True if root keeps every denominator nonzero and makes expr exactly 0."""
    num, den = sp.fraction(sp.together(expr))
    if sp.simplify(den.subs(var, root)) == 0:
        return False
    val = expr.subs(var, root)
    return val.is_real is not False and sp.simplify(val) == 0


def _b10ne_mc(expected):
    """Callable for numeric choices the base parser can't read (radicals)."""

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        matches = [i for i, v in enumerate(vals) if sp.simplify(v - expected) == 0]
        return matches == [idx], f"expected {expected}; matching choices {matches}"

    return check


def _b10ne_count(count):
    def check(choices, idx):
        word = _B10NE_COUNT_WORDS[count]
        return choices[idx] == word, f"{count} real solution(s) -> '{word}'"

    return check


def _b10ne_point(text):
    a_, b_ = text.strip().strip("$").strip("()").split(",")
    return latex_to_sympy(a_), latex_to_sympy(b_)


# ----- checks -----


def adv_ne2_quartic_isolate_positive():
    pos = [r for r in _b10ne_real_roots(2 * x**4 - 7 - 155) if r > 0]
    assert len(pos) == 1
    return pos[0]


def adv_ne2_factored_greatest_solution():
    return max(_b10ne_real_roots((2 * x - 9) * (x**2 - 16)))


def adv_ne2_square_equals_twelve_radical():
    pos = [r for r in _b10ne_real_roots((x + 2) ** 2 - 12) if r > 0]
    assert len(pos) == 1
    return _b10ne_mc(pos[0])


def adv_ne2_rod_length_tolerance():
    m = Symbol("L", real=True)
    sols = sp.solve(sp.Abs(m - 120) - Rational(2, 5), m)
    assert len(sols) == 2
    return max(sols)


def adv_ne2_rational_one_fraction_easy():
    expr = (x + 5) / (x - 1) - 3
    sols = [r for r in _b10ne_real_roots(expr) if _b10ne_valid(expr, r)]
    assert len(sols) == 1
    return sols[0]


def adv_ne2_line_parabola_which_point():
    sols = sp.solve([Eq(y, x**2), Eq(y, x + 6)], [x, y], dict=True)
    pts = {(s[x], s[y]) for s in sols}
    assert len(pts) == 2

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices) if _b10ne_point(ch) in pts]
        return hits == [idx], f"intersections {sorted(pts)}; matching choices {hits}"

    return check


def adv_ne2_irrational_negative_solution():
    neg = [r for r in _b10ne_real_roots(3 * x**2 - 6 * x - 2) if r < 0]
    assert len(neg) == 1
    return _b10ne_mc(neg[0])


def adv_ne2_complete_square_lesser():
    roots = _b10ne_real_roots(x**2 + 8 * x - 5)
    assert len(roots) == 2
    return _b10ne_mc(min(roots))


def adv_ne2_quartic_in_form_greatest():
    roots = _b10ne_real_roots(x**4 - 11 * x**2 + 18)
    assert len(roots) == 4
    return _b10ne_mc(max(roots))


def adv_ne2_rational_two_fractions_positive():
    expr = 2 / x + 3 / (x + 2) - 1
    pos = [r for r in _b10ne_real_roots(expr) if _b10ne_valid(expr, r) and r > 0]
    assert len(pos) == 1
    return pos[0]


def adv_ne2_two_radicals_quadratic_radicand():
    cands = _b10ne_real_roots(x**2 - 8 - 2 * x)
    good = [r for r in cands if r**2 - 8 >= 0 and 2 * r >= 0 and sp.simplify(sqrt(r**2 - 8) - sqrt(2 * r)) == 0]
    assert len(good) == 1
    return good[0]


def adv_ne2_difference_of_squares_system_y():
    sols = sp.solve([Eq(x**2 - y**2, 24), Eq(x + y, 8)], [x, y], dict=True)
    assert len(sols) == 1
    return sols[0][y]


def adv_ne2_exponential_line_count():
    g = lambda v: 3.0**v - v - 2  # noqa: E731
    # g is convex (g'' = 3^x ln(3)^2 > 0), so it has at most two zeros; count sign changes.
    grid = [i / 1000 for i in range(-50000, 50001)]
    changes = 0
    for u, v in zip(grid, grid[1:]):
        gu, gv = g(u), g(v)
        if gu == 0 or gu * gv < 0:
            changes += 1
    assert sp.Integer(3) ** 1 == 1 + 2  # exact root at x = 1
    return _b10ne_count(changes)


def adv_ne2_hyperbola_line_other_point():
    kv = sp.solve(Eq(2, k / 3), k)[0]
    cv = sp.solve(Eq(2, 3 + c), c)[0]
    others = [r for r in _b10ne_real_roots(kv / x - (x + cv)) if r != 3]
    assert len(others) == 1
    return others[0] + cv


def adv_ne2_cabin_rental_group_size():
    n = Symbol("n")
    expr = 360 / n - 360 / (n + 3) - 6
    pos = [r for r in _b10ne_real_roots(expr, n) if r > 0 and _b10ne_valid(expr, r, n)]
    assert len(pos) == 1
    return pos[0]


def adv_ne2_illuminance_solve_distance():
    E_, k_, d_ = symbols("q k d", positive=True)

    def check(choices, idx):
        good = []
        for i, ch in enumerate(choices):
            rhs = ch.strip().strip("$").split("=", 1)[1].replace("E", "q")
            dv = latex_to_sympy_ext(rhs).subs({Symbol("q"): E_, Symbol("k"): k_})
            if sp.simplify(k_ / dv**2 - E_) == 0:
                good.append(i)
        return good == [idx], f"choices solving E = k/d^2 for d: {good}"

    return check


def adv_ne2_catapult_balloon_height():
    ts = _b10ne_real_roots(-5 * t**2 + 25 * t - (5 * t + 15), t)
    assert len(ts) == 2
    return 5 * max(ts) + 15


def adv_ne2_library_collections_later_time():
    f = 1000 * sp.Float("1.1") ** t - 900 - 150 * t
    r1 = sp.nsolve(f, t, 2)
    r2 = sp.nsolve(f, t, 7)
    assert abs(r1 - r2) > 1
    later = max(r1, r2)
    return Rational(str(round(float(later), 1)))


def adv_ne2_cube_root_quadratic_form():
    u = Symbol("u", real=True)
    xs = [r**3 for r in sp.solve(u**2 - 5 * u + 4, u)]
    xp = Symbol("xp", positive=True)
    for v in xs:
        assert sp.simplify((xp ** Rational(2, 3) - 5 * xp ** Rational(1, 3) + 4).subs(xp, v)) == 0
    return sum(xs)


def adv_ne2_base_five_solution_count():
    u = Symbol("u", real=True)
    us = sp.solve(u**2 + 4 * u - 5, u)
    xs = [sp.log(v, 5) for v in us if v > 0]
    for v in xs:
        assert sp.simplify(5 ** (2 * v) + 4 * 5**v - 5) == 0
    return _b10ne_count(len(xs))


def adv_ne2_base_three_product_solutions():
    u = Symbol("u", real=True)
    us = sp.solve(3 * u**2 - 28 * u + 9, u)
    xs = [sp.simplify(sp.log(v, 3)) for v in us if v > 0]
    assert len(xs) == 2
    for v in xs:
        assert sp.simplify(3 ** (2 * v + 1) - 28 * 3**v + 9) == 0
    return sp.simplify(xs[0] * xs[1])


def adv_ne2_rational_restriction_extraneous():
    expr = x / (x - 2) - 3 / (x + 1) - 9 / (x**2 - x - 2)
    sols = [r for r in _b10ne_real_roots(expr) if _b10ne_valid(expr, r)]
    assert len(sols) == 1
    return sols[0]


def adv_ne2_two_radicals_sum_solutions():
    # Squaring twice gives (x + 1)^2 = 16(x - 2); keep candidates that satisfy the original.
    cands = _b10ne_real_roots((x + 1) ** 2 - 16 * (x - 2))
    good = [r for r in cands if 2 * r + 3 >= 0 and r - 2 >= 0
            and sp.simplify(sqrt(2 * r + 3) - sqrt(r - 2) - 2) == 0]
    assert len(good) == 2
    return sum(good)


def adv_ne2_two_radicals_no_solution():
    cands = _b10ne_real_roots(5 * x - 4 - 4 * (x - 1))
    good = [r for r in cands if 5 * r - 4 >= 0 and r - 1 >= 0
            and sp.simplify(sqrt(5 * r - 4) - 2 * sqrt(r - 1)) == 0]
    return _b10ne_count(len(good))


def adv_ne2_parabola_absolute_three_points():
    right = [r for r in _b10ne_real_roots(x**2 - 2 * x + 1 - (x - 1)) if r >= 1]
    left = [r for r in _b10ne_real_roots(x**2 - 2 * x + 1 - (1 - x)) if r < 1]
    return _b10ne_count(len(set(right + left)))


def adv_ne2_absolute_quadratic_three_solutions_k():
    f = x**2 - 6 * x + 5

    def count(kv):
        return len(set(_b10ne_real_roots(f - kv) + _b10ne_real_roots(f + kv)))

    vx = sp.solve(sp.diff(f, x), x)[0]
    kv = sp.Abs(f.subs(x, vx))
    assert count(kv) == 3 and count(kv - 1) == 4 and count(kv + 1) == 2
    return kv


def adv_ne2_k_at_both_ends_one_solution():
    kp = Symbol("kp", positive=True)
    sols = sp.solve(6**2 - 4 * kp * kp, kp)
    assert len(sols) == 1
    assert len(_b10ne_real_roots(sols[0] * x**2 + 6 * x + sols[0])) == 1
    return sols[0]


def adv_ne2_rational_tangent_positive_k():
    kp = Symbol("kp", positive=True)
    sols = sp.solve(kp**2 - 36, kp)
    assert len(sols) == 1
    expr = 9 / x - (sols[0] - x)
    assert len([r for r in _b10ne_real_roots(expr) if _b10ne_valid(expr, r)]) == 1
    return sols[0]


def adv_ne2_tangent_at_given_point_bc():
    quad = sp.expand(x**2 + b * x + c - (2 * x - 1))
    disc = sp.discriminant(quad, x)
    sols = sp.solve([quad.subs(x, 2), disc], [b, c], dict=True)
    assert len(sols) == 1
    s0 = sols[0]
    assert _b10ne_real_roots(quad.subs(s0)) == [2]
    return s0[b] * s0[c]


def adv_ne2_hiker_round_trip_speed():
    s_ = Symbol("s")
    expr = 12 / s_ + 12 / (s_ + 1) - 7
    pos = [r for r in _b10ne_real_roots(expr, s_) if r > 0 and _b10ne_valid(expr, r, s_)]
    assert len(pos) == 1
    return pos[0]


def adv_ne2_tabletop_diagonal_perimeter():
    lp, wp = symbols("l w", positive=True)
    sols = sp.solve([Eq(lp**2 + wp**2, 36), Eq(lp * wp, 14)], [lp, wp], dict=True)
    perims = {sp.simplify(2 * (s[lp] + s[wp])) for s in sols}
    assert len(perims) == 1
    return _b10ne_mc(perims.pop())


# ----- Batch batch10-sys2 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch10-sys2.ts (batch batch10-sys2).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch10_sys2.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""



import sympy as sp
from sympy import Eq, Rational

_b10sy_x, _b10sy_y = sp.symbols("x y")


# ----- helpers (prefix _b10sy_) -----


def _b10sy_solve(e1, e2, syms=None):
    """Unique solution of two linear equations, as a tuple in the order of syms."""
    syms = syms or [_b10sy_x, _b10sy_y]
    sol = sp.solve([e1, e2], syms, dict=True)
    assert len(sol) == 1 and len(sol[0]) == len(syms)
    assert not any(v.free_symbols for v in sol[0].values())
    return tuple(sol[0][v] for v in syms)


def _b10sy_parse_system(choice, syms):
    """Parse '$e1$ and $e2$' into a list of SymPy Eq objects in the given symbols."""
    eqs = []
    for part in choice.split(" and "):
        lhs, rhs = part.strip().strip("$").split("=")
        loc = {str(v): v for v in syms}
        eqs.append(Eq(sp.sympify(latex_to_sympy(lhs), locals=loc), sp.sympify(latex_to_sympy(rhs), locals=loc)))
    return eqs


def _b10sy_same_line(e1, e2):
    """True when two linear equations in x, y describe the same line."""
    f1 = sp.expand(e1.lhs - e1.rhs)
    f2 = sp.expand(e2.lhs - e2.rhs)
    X, Y = _b10sy_x, _b10sy_y
    v1 = [f1.coeff(X), f1.coeff(Y), f1.subs({X: 0, Y: 0})]
    v2 = [f2.coeff(X), f2.coeff(Y), f2.subs({X: 0, Y: 0})]
    return sp.Matrix([v1, v2]).rank() == 1


def _b10sy_system_matches(truth, syms):
    """Callable: exactly one choice is a system whose unique solution equals truth (dict)."""

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            eqs = _b10sy_parse_system(ch, syms)
            sol = sp.solve(eqs, syms, dict=True)
            if len(sol) == 1 and len(sol[0]) == len(syms) and all(sol[0][v] == truth[v] for v in syms):
                hits.append(i)
        return hits == [idx], f"truth {truth}; matching systems {hits}"

    return check


# ----- item checks -----


def alg_sys_combine_for_five_x_plus_seven_y():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(4 * X + 5 * Y, 23), Eq(X + 2 * Y, 8))
    return 5 * sx + 7 * sy


def alg_sys_scale_first_equation_seven_x_nine_y_spr():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(2 * X + 5 * Y, 13), Eq(3 * X - Y, 4))
    return 7 * sx + 9 * sy


def alg_sys_three_constants_solution_given_c_spr():
    a, b, c = sp.symbols("a b c")
    X, Y = 2, 5
    sol = sp.solve([Eq(a * X + 3 * Y, 19), Eq(4 * X - b * Y, c), Eq(b, 2 * a)], [a, b, c], dict=True)
    assert len(sol) == 1
    return sol[0][c]


def alg_sys_three_constants_p_plus_r():
    p, q, r = sp.symbols("p q r")
    X, Y = -1, 4
    sol = sp.solve([Eq(p * X + q * Y, 10), Eq(q * X + r * Y, 13), Eq(q, p + 1)], [p, q, r], dict=True)
    assert len(sol) == 1
    return sol[0][p] + sol[0][r]


def alg_sys_solution_x_twice_y_coefficient_k():
    X, Y = _b10sy_x, _b10sy_y
    k = sp.Symbol("k")
    sol = sp.solve([Eq(3 * X + k * Y, 26), Eq(X - 4 * Y, -2), Eq(X, 2 * Y)], [X, Y, k], dict=True)
    assert len(sol) == 1
    return sol[0][k]


def alg_sys_fractions_both_sides_x_spr():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq((X - 1) / 2, (Y + 3) / 4), Eq((X + 2 * Y) / 5, (X + 1) / 4))
    return sx


def alg_sys_parameter_ratio_x_over_y():
    X, Y = _b10sy_x, _b10sy_y
    k = sp.Symbol("k", nonzero=True)
    sol = sp.solve([Eq(2 * X + 3 * Y, 7 * k), Eq(5 * X - Y, 9 * k)], [X, Y], dict=True)
    assert len(sol) == 1
    ratio = sp.simplify(sol[0][X] / sol[0][Y])
    assert not ratio.free_symbols
    return ratio


def alg_sys_ratio_x_over_y_elimination():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(6 * X - 4 * Y, 18), Eq(3 * X + 5 * Y, 30))
    return sx / sy


def alg_sys_lines_described_standard_form():
    X, Y = _b10sy_x, _b10sy_y
    # line p: slope 3, y-intercept -2; line q through (0, 4) and (8, 0)
    mq = Rational(0 - 4, 8 - 0)
    p_line = Eq(Y, 3 * X - 2)
    q_line = Eq(Y, mq * X + 4)

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            e1, e2 = _b10sy_parse_system(ch, [X, Y])
            if (_b10sy_same_line(e1, p_line) and _b10sy_same_line(e2, q_line)) or (
                _b10sy_same_line(e1, q_line) and _b10sy_same_line(e2, p_line)
            ):
                hits.append(i)
        return hits == [idx], f"choices matching lines p and q: {hits}"

    return check


def alg_sys_which_ordered_pair_satisfies_both():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(2 * X + Y, 7), Eq(X - 3 * Y, 7))

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            u, v = latex_to_sympy(ch.strip("$").strip("()").split(",")[0]), latex_to_sympy(ch.strip("$").strip("()").split(",")[1])
            if (u, v) == (sx, sy):
                hits.append(i)
        return hits == [idx], f"solution ({sx}, {sy}); matching choices {hits}"

    return check


def alg_sys_horizontal_line_intersection_x():
    X, Y = _b10sy_x, _b10sy_y
    return _b10sy_solve(Eq(Y, 5), Eq(Y, 2 * X - 3))[0]


def alg_sys_solution_given_find_coefficient_a():
    a = sp.Symbol("a")
    X, Y = 2, -3
    assert X - Y == 5  # the pair satisfies the second equation
    return sp.solve(Eq(a * X + 3 * Y, 5), a)[0]


def alg_sys_sum_in_words_and_equation_x():
    X, Y = _b10sy_x, _b10sy_y
    return _b10sy_solve(Eq(X + Y, 12), Eq(3 * X - Y, 4))[0]


def alg_sys_infinite_solutions_y_at_given_x():
    X, Y = _b10sy_x, _b10sy_y
    a = sp.Symbol("a")
    # infinitely many solutions: coefficient vectors proportional
    a_val = sp.solve(Eq(a * 3, 6 * 2), a)[0]
    assert _b10sy_same_line(Eq(a_val * X + 6 * Y, 18), Eq(2 * X + 3 * Y, 9))
    return sp.solve(Eq(2 * 3 + 3 * Y, 9), Y)[0]


def alg_sys_which_system_has_given_solution():
    X, Y = _b10sy_x, _b10sy_y
    return _b10sy_system_matches({X: -2, Y: 3}, [X, Y])


def alg_sys_x_described_in_words_sum():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(X, 3 * Y - 4), Eq(2 * X + 5 * Y, 47))
    return sx + sy


def alg_sys_swapped_slope_intercept_y_spr():
    X, Y = _b10sy_x, _b10sy_y
    a = sp.Symbol("a")
    b = 9 - a
    sol = sp.solve([Eq(Y, a * X + b), Eq(Y, b * X + a)], [X, Y], dict=True)
    assert len(sol) == 1
    yv = sp.simplify(sol[0][Y])
    assert not yv.free_symbols  # independent of a (for a != b)
    return yv


def alg_sys_infinite_solutions_product_mc():
    X, Y = _b10sy_x, _b10sy_y
    m, c = sp.symbols("m c")
    # 4x - 6y = c  ->  y = (4x - c)/6 must equal mx + 1 for all x
    expr = sp.expand((4 * X - c) / 6 - (m * X + 1))
    sol = sp.solve([expr.coeff(X), expr.subs(X, 0)], [m, c], dict=True)
    assert len(sol) == 1
    return sol[0][m] * sol[0][c]


def alg_sys_fractions_both_sides_x_minus_y():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq((X + Y) / 2, (X - 5) / 4), Eq((2 * X - Y) / 5, (Y + 10) / 3))
    return sx - sy


def alg_sys_florist_bouquets_roses_spr():
    s, l = sp.symbols("s l")
    return _b10sy_solve(Eq(3 * s + 7 * l, 156), Eq(s, 2 * l), [s, l])[1]


def alg_sys_drones_altitude_interpret_y():
    X, Y = _b10sy_x, _b10sy_y
    sx, sy = _b10sy_solve(Eq(Y, 20 + 3 * X), Eq(Y, 140 - 5 * X))
    assert (sx, sy) == (15, 65)
    key = f"Both drones are at an altitude of {sy} meters {sx} seconds after the test begins."

    def check(choices, idx):
        return choices[idx] == key and choices.count(key) == 1, f"intersection ({sx}, {sy}); key text {key!r}"

    return check


def alg_sys_ice_sculptures_equal_height():
    t, h = sp.symbols("t h")
    R = Rational
    return _b10sy_solve(Eq(h, 30 - R(6, 5) * t), Eq(h, 22 - R(4, 5) * t), [t, h])[1]


def alg_sys_bowling_equal_cost_fee_spr():
    f = sp.Symbol("f")
    R = Rational
    games = 5
    return sp.solve(Eq(f + 6 * games, R(9, 2) + R(15, 2) * games), f)[0]


def alg_sys_hiker_flat_uphill_distance():
    f, u = sp.symbols("f u")
    sf, su = _b10sy_solve(Eq(5 * f + 3 * u, 21), Eq(f, u + 1), [f, u])
    return 3 * su


def alg_sys_bike_shop_repairs_model():
    t, b = sp.symbols("t b")
    truth = dict(zip([t, b], _b10sy_solve(Eq(t + b, 22), Eq(15 * t + 40 * b, 8 * 60), [t, b])))
    return _b10sy_system_matches(truth, [t, b])


def alg_sys_bridges_ages_future():
    a, b = sp.symbols("a b")
    R = Rational
    return _b10sy_solve(Eq(a, 4 * b), Eq(a + 12, R(5, 2) * (b + 12)), [a, b])[0]


def alg_sys_courier_van_unloaded_type_b_spr():
    a, b = sp.symbols("a b")
    sa, sb = _b10sy_solve(Eq(a + b, 20), Eq(900 - 60 * a - 25 * b, 120), [a, b])
    assert sa.is_integer and sb.is_integer and sa >= 0 and sb >= 0
    return 25 * sb


def alg_sys_puppies_weight_weeks_units():
    w, p = sp.symbols("w p")
    R = Rational
    return _b10sy_solve(Eq(p, 18 + 2 * w), Eq(p, 6 + R(1, 2) * 7 * w), [w, p])[0]


# ----- Batch batch11-le1v2 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch11-le1v2.ts (batch batch11-le1v2).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch11_le1v2.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers.
"""



import sympy as sp
from sympy import Eq, Rational, symbols

x, y, k, a, b, c, p, n, m, d = symbols("x y k a b c p n m d")


# ----- helpers (prefix _b11l1_) -----


def _b11l1_solve_one(eq, var=x):
    """The unique solution of a linear equation in var (asserts exactly one)."""
    sols = sp.solve(eq, var)
    assert len(sols) == 1, f"expected one solution, got {sols}"
    return sp.nsimplify(sols[0])


def _b11l1_identity_constants(lhs, rhs, unknowns, var=x):
    """Constants that make lhs = rhs an identity in var (asserts a unique choice)."""
    coeffs = sp.Poly(sp.expand(lhs - rhs), var).all_coeffs()
    sols = sp.solve(coeffs, unknowns, dict=True)
    assert len(sols) == 1, f"expected one set of constants, got {sols}"
    sol = sols[0]
    assert sp.expand((lhs - rhs).subs(sol)) == 0  # genuinely infinitely many solutions
    return sol


def _b11l1_split(text):
    lhs, rhs = text.strip().strip("$").split("=")
    return latex_to_sympy(lhs), latex_to_sympy(rhs)


# ----- items -----


def alg_le_x_fourths_sixths_sum():
    return _b11l1_solve_one(Eq(x / 4 + x / 6, 15))


def alg_le_proportion_two_numerators():
    return _b11l1_solve_one(Eq((x + 4) / 6, (2 * x - 1) / 9))


def alg_le_proportion_fraction_key_spr():
    return _b11l1_solve_one(Eq((5 - x) / 4, (x + 7) / 10))


def alg_le_proportion_k_from_solution():
    kk = _b11l1_solve_one(Eq((26 - 2 * k) / 3, (26 + k) / 5), k)
    # x = 26 is then the (only) solution of the equation in x
    assert _b11l1_solve_one(Eq((x - 2 * kk) / 3, (x + kk) / 5)) == 26
    return kk


def alg_le_shifted_constant_new_solution():
    kk = _b11l1_solve_one(Eq(3 * (2 * 15 - k), 5 * 15 + 2 * k), k)
    return _b11l1_solve_one(Eq(3 * (2 * x - kk), 5 * x + 2 * kk + 10))


def alg_le_nested_bracket_solve():
    return _b11l1_solve_one(Eq(2 * (3 - (x - 4)), x + 5))


def alg_le_nested_bracket_fraction_spr():
    return _b11l1_solve_one(Eq(4 - 3 * (2 * x - (5 - x)), 2 * (x + 1) - 6 * x))


def alg_le_value_x_plus_5():
    xx = _b11l1_solve_one(Eq(7 * (x + 5), 56))
    return xx + 5


def alg_le_value_6_minus_x():
    xx = _b11l1_solve_one(Eq((x - 6) / 4, 3))
    return 6 - xx


def alg_le_consecutive_twice_greatest():
    least = _b11l1_solve_one(Eq(2 * (n + 2), 3 * (n + (n + 1)) - 23), n)
    assert least.is_integer
    return least + 2


def alg_le_oak_maple_ages():
    return _b11l1_solve_one(Eq(4 * m + 18, 2 * (m + 18)), m)


def alg_le_ladder_discount_delivery():
    return _b11l1_solve_one(Eq(p * (1 - Rational(20, 100)) + Rational("9.00"), Rational("105.00")), p)


def alg_le_ticket_discount_service_fee_spr():
    discounted = p * (1 - Rational(25, 100))
    with_fee = discounted * (1 + Rational(8, 100))
    return _b11l1_solve_one(Eq(with_fee + Rational("4.50"), Rational("85.50")), p)


def alg_le_identity_two_constants_sum():
    sol = _b11l1_identity_constants(a * (2 * x - 3) + 4 * x, 10 * x + b, [a, b])
    return sol[a] + sol[b]


def alg_le_flower_shop_bouquets_equation():
    target = sp.expand(12 * b + 36 - 240)  # stems in bouquets + leftover = total

    def check(choices, idx):
        hits = []
        for i, ch in enumerate(choices):
            lhs, rhs = _b11l1_split(ch)
            diff = sp.expand(lhs - rhs)
            ratio = sp.simplify(diff / target)
            if ratio.is_number and ratio != 0:
                hits.append(i)
        return hits == [idx], f"equivalent to {target} = 0: choices {hits}"

    return check


def alg_le_greenhouse_term_meaning():
    # 1,260 - 90d = 450: 1,260 start, 90 per day, so 90d is the number shipped in d days.
    rate = sp.Integer(90)
    assert sp.solve(Eq(1260 - rate * d, 450), d) == [9]
    expected = "The number of seedlings shipped in $d$ days."

    def check(choices, idx):
        return choices[idx] == expected and choices.count(expected) == 1, f"expected {expected!r}"

    return check


def alg_le_club_mugs_profit_spr():
    profit = 14 * m - (150 + Rational("5.50") * m)
    return _b11l1_solve_one(Eq(profit, 445), m)


def alg_le_both_sides_easy_solve():
    return _b11l1_solve_one(Eq(8 - 3 * x, 2 * x - 17))


def alg_le_x_over_20_structure():
    xx = _b11l1_solve_one(Eq(x / 4 - x / 10, 9))
    return xx / 20


def alg_le_identity_coefficient_match_spr():
    sol = _b11l1_identity_constants(3 * (x - 2 * a) + b * x, 7 * x - 12, [a, b])
    return sol[a] + sol[b]


def alg_le_five_even_sum_greatest():
    terms = [n + 2 * i for i in range(5)]
    least = _b11l1_solve_one(Eq(sum(terms), 6 * n), n)
    assert least.is_integer and least % 2 == 0
    return terms[-1].subs(n, least)


# ----- Batch batch11-ineq2 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch11-ineq2.ts (batch batch11-ineq2).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch11_ineq2.py --only-extra

Each function derives the answer from the stem's givens: a numeric result for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items
whose choices are inequalities, systems, points or sentences.
"""

import re


import sympy as sp
from sympy import Rational, Integer, symbols

_b11iq_x, _b11iq_y = symbols("x y")
_b11iq_syms = {name: sp.Symbol(name) for name in "abcdghLpq"}

_B11IQ_OPS = {"\\le": sp.Le, "\\ge": sp.Ge, "<": sp.Lt, ">": sp.Gt}


def _b11iq_rel(text: str):
    """One math span ('$3 \\le x < 6$', '$y > \\frac{1}{2}x + 4$') -> SymPy relational (And for chains)."""
    body = text.strip().strip("$").replace("{,}", "")
    parts = re.split(r"(\\le|\\ge|<|>)", body)
    exprs = [latex_to_sympy(e) for e in parts[0::2]]
    ops = parts[1::2]
    rels = [_B11IQ_OPS[op](lhs, rhs) for op, lhs, rhs in zip(ops, exprs, exprs[1:])]
    return sp.And(*rels)


def _b11iq_system(text: str):
    """'$A$ and $B$' -> And(A, B)."""
    spans = re.findall(r"\$[^$]+\$", text)
    return sp.And(*[_b11iq_rel(sp_) for sp_ in spans])


def _b11iq_point(text: str):
    inner = text.strip().strip("$").strip().strip("()")
    xs, ys = inner.split(",")
    return sp.nsimplify(xs.strip()), sp.nsimplify(ys.strip())


def _b11iq_match(expected, parse, grid, var_list):
    """Callable: the choices whose parsed relation agrees with `expected` at every grid point."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            rel = parse(ch)
            if all(bool(rel.subs(dict(zip(var_list, pt)))) == bool(expected.subs(dict(zip(var_list, pt)))) for pt in grid):
                matches.append(i)
        return matches == [idx], f"expected {expected}; matching choices {matches}"

    return check


_B11IQ_GRID_1D = [(Rational(i, 4),) for i in range(-80, 81)]
_B11IQ_GRID_2D = [(Rational(i, 2), Rational(j, 2)) for i in range(-24, 25) for j in range(-24, 25)]


def _b11iq_corners(lines, feasible):
    """Corners of a region: pairwise intersections of boundary lines (a, b, c means a*x + b*y = c) that are feasible."""
    pts = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a1, b1, c1), (a2, b2, c2) = lines[i], lines[j]
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            px = Rational(c1 * b2 - c2 * b1, det)
            py = Rational(a1 * c2 - a2 * c1, det)
            if feasible(px, py):
                pts.append((px, py))
    return pts


# ----- easy -----


def alg_ineq_dashed_boundary_shaded_below():
    X, Y = _b11iq_x, _b11iq_y
    expected = sp.Lt(Y, 4 * X - 3)  # dashed -> strict; below -> less than
    return _b11iq_match(expected, _b11iq_rel, _B11IQ_GRID_2D, [X, Y])


def alg_ineq_describe_graph_solid_above():
    op = ">="  # y >= -3x + 6
    style = "solid" if op in ("<=", ">=") else "dashed"
    side = "above" if op in (">", ">=") else "below"
    target = f"The boundary line is {style}, and the region {side} it is shaded."

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if ch == target]
        return good == [idx], f"expected {target!r}; matching {good}"

    return check


def alg_ineq_pin_length_tolerance():
    L = _b11iq_syms["L"]
    center, tol = 12, Rational(3, 10)
    expected = sp.And(sp.Le(center - tol, L), sp.Le(L, center + tol))
    grid = [(Rational(i, 20),) for i in range(200, 300)]
    return _b11iq_match(expected, _b11iq_rel, grid, [L])


def alg_ineq_dashed_boundary_y_axis():
    X, Y = _b11iq_x, _b11iq_y
    yint = sp.solve(sp.Eq((3 * X - 4 * Y).subs(X, 0), 24), Y)[0]
    target = (Integer(0), yint)

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if _b11iq_point(ch) == target]
        return good == [idx], f"boundary meets y-axis at {target}; matching {good}"

    return check


def alg_ineq_data_plan_music_hours():
    m = sp.Symbol("m")
    sol = sp.solve_univariate_inequality(sp.Le(Rational(3, 2) * 4 + Rational(1, 10) * m, 8), m, relational=False)
    return sol.sup


# ----- medium -----


def alg_ineq_day_camp_staff_system():
    c, g = _b11iq_syms["c"], _b11iq_syms["g"]
    expected = sp.And(sp.Ge(c + g, 8), sp.Le(100 * c + 120 * g, 960))
    grid = [(i, j) for i in range(0, 15) for j in range(0, 15)]
    return _b11iq_match(expected, _b11iq_system, grid, [c, g])


def alg_ineq_recycling_credits_point_outside():
    a_pt, g_pt = 30, 15
    assert not (2 * a_pt + 5 * g_pt >= 150)  # the point really is outside

    def truth(ch):
        mt = re.match(r"Recycling (\d+) bags of cans and (\d+) bags of glass earns (fewer than|exactly|more than) (\d+) credits\.", ch)
        cans, glass, rel, val = int(mt.group(1)), int(mt.group(2)), mt.group(3), int(mt.group(4))
        total = 2 * cans + 5 * glass
        return {"fewer than": total < val, "exactly": total == val, "more than": total > val}[rel]

    def check(choices, idx):
        good = [i for i, ch in enumerate(choices) if truth(ch)]
        return good == [idx], f"true statements {good}"

    return check


def alg_ineq_tank_heater_hours():
    h = sp.Symbol("h")
    temp = 14 + 2 * h
    expected = sp.And(sp.Le(22, temp), sp.Le(temp, 28))
    grid = [(Rational(i, 4),) for i in range(0, 80)]
    return _b11iq_match(expected, _b11iq_rel, grid, [h])


def alg_ineq_shifted_compound_same_set():
    X = _b11iq_x
    expected = sp.And(sp.Le(-4, X), sp.Le(X, 10))
    return _b11iq_match(expected, _b11iq_rel, _B11IQ_GRID_1D, [X])


def alg_ineq_compound_two_constants_sum():
    X = _b11iq_x
    a_val = (3 * X - 6).subs(X, 2)  # 3x - 6 is increasing, so its least value on [2, 9] is at x = 2
    b_val = (3 * X - 6).subs(X, 9)
    sol = sp.solve_univariate_inequality(sp.Le(a_val, 3 * X - 6), X, relational=False).intersect(
        sp.solve_univariate_inequality(sp.Le(3 * X - 6, b_val), X, relational=False))
    assert sol == sp.Interval(2, 9)
    return a_val + b_val


def alg_ineq_region_greatest_y():
    X = _b11iq_x
    xv = sp.solve(sp.Eq(10 - X, 2 * X + 1), X)[0]
    best = 10 - xv
    # confirm: the bound min(10 - x, 2x + 1) never exceeds best on a fine grid
    assert all(min(10 - Rational(i, 8), 2 * Rational(i, 8) + 1) <= best for i in range(-200, 200))
    return best


def alg_ineq_intercepts_solid_above():
    X, Y = _b11iq_x, _b11iq_y
    slope = Rational(-4 - 0, 0 - 6)
    expected = sp.Ge(Y, slope * X - 4)  # solid -> inclusive; above
    return _b11iq_match(expected, _b11iq_rel, _B11IQ_GRID_2D, [X, Y])


def alg_ineq_table_boundary_least_k():
    pts = [(-1, 7), (2, 1), (4, -3)]
    m = Rational(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
    b = pts[0][1] - m * pts[0][0]
    assert all(py == m * px + b for px, py in pts)
    k = sp.Symbol("k")
    sol = sp.solve_univariate_inequality(sp.Gt(k, m * 0 + b), k, relational=False)
    return Integer(min(i for i in range(-50, 50) if sol.contains(i)))


def alg_ineq_function_values_compare():
    X = _b11iq_x
    expected = sp.Gt(3 * X - 8, 12 - X)
    return _b11iq_match(expected, _b11iq_rel, _B11IQ_GRID_1D, [X])


def alg_ineq_boundary_intercepts_constants():
    a_, b_ = _b11iq_syms["a"], _b11iq_syms["b"]
    sol = sp.solve([sp.Eq(a_ * 4 + b_ * 0, 12), sp.Eq(a_ * 0 + b_ * -3, 12)], [a_, b_], dict=True)[0]
    return sol[a_] + sol[b_]


# ----- hard -----


def alg_ineq_hike_distance_time_system():
    d, h = _b11iq_syms["d"], _b11iq_syms["h"]
    expected = sp.And(sp.Ge(d + h, 16), sp.Le(d / 4 + h / 2, 6))
    grid = [(Rational(i, 2), Rational(j, 2)) for i in range(0, 61) for j in range(0, 41)]
    return _b11iq_match(expected, _b11iq_system, grid, [d, h])


def alg_ineq_bakery_greatest_batches():
    best = max(i + j for i in range(0, 40) for j in range(0, 40) if 2 * i + 3 * j <= 30 and 4 * i + 3 * j <= 48)
    return Integer(best)


def alg_ineq_stable_feed_least_cost():
    # cost in cents: 30 per kg hay, 50 per kg oats; integer kilograms suffice (corners are integers)
    best = min(30 * hay + 50 * oats for hay in range(0, 351) for oats in range(200, 701) if hay + oats >= 600)
    return Rational(best, 100)


def alg_ineq_signs_of_constants():
    X = _b11iq_x
    target = sp.Interval.open(3, sp.oo)
    vals = [Rational(i, 2) for i in range(-12, 13) if i != 0]
    good_pq = [(pv, qv) for pv in vals for qv in vals
               if sp.solve_univariate_inequality(sp.Lt(pv * X + qv, 0), X, relational=False) == target]
    assert good_pq
    p_, q_ = _b11iq_syms["p"], _b11iq_syms["q"]

    def check(choices, idx):
        must = [i for i, ch in enumerate(choices)
                if all(bool(_b11iq_system(ch).subs({p_: pv, q_: qv})) for pv, qv in good_pq)]
        return must == [idx], f"(p, q) giving x > 3: {good_pq}; choices always true {must}"

    return check


def alg_ineq_four_constraints_greatest_sum():
    lines = [(1, 0, 0), (0, 1, 0), (3, 1, 18), (1, 2, 16)]

    def feasible(px, py):
        return px >= 0 and py >= 0 and 3 * px + py <= 18 and px + 2 * py <= 16

    return max(px + py for px, py in _b11iq_corners(lines, feasible))


def alg_ineq_point_not_in_system_c():
    c = _b11iq_syms["c"]
    px, py = 2, 1
    not_solution = sp.Not(sp.And(sp.Ge(py, 3 * px + c), sp.Le(py, -px + 4)))
    grid = [(Rational(i, 4),) for i in range(-60, 21)]
    return _b11iq_match(not_solution, _b11iq_rel, grid, [c])


def alg_ineq_two_inequalities_given_interval():
    X = _b11iq_x
    a_, b_ = _b11iq_syms["a"], _b11iq_syms["b"]
    # 5 - 2x >= a  <=>  x <= (5 - a)/2 (closed end 4); 3x + b > 0  <=>  x > -b/3 (open end -2)
    a_val = sp.solve(sp.Eq((5 - a_) / 2, 4), a_)[0]
    b_val = sp.solve(sp.Eq(-b_ / 3, -2), b_)[0]
    sol = sp.solve_univariate_inequality(sp.Ge(5 - 2 * X, a_val), X, relational=False).intersect(
        sp.solve_univariate_inequality(sp.Gt(3 * X + b_val, 0), X, relational=False))
    assert sol == sp.Interval.Lopen(-2, 4)
    return b_val - a_val


def alg_ineq_region_greatest_2x_plus_y():
    lines = [(1, 1, 8), (-1, 1, -2), (1, 0, 0)]  # y = 8 - x, y = x - 2, x = 0

    def feasible(px, py):
        return py <= 8 - px and py >= px - 2 and px >= 0

    return max(2 * px + py for px, py in _b11iq_corners(lines, feasible))


def alg_ineq_region_lines_through_points():
    X, Y = _b11iq_x, _b11iq_y
    m1 = Rational(4 - 0, 0 - (-2))
    m2 = Rational(1 - 4, 6 - 0)
    expected = sp.And(sp.Gt(Y, m1 * X + 4), sp.Le(Y, m2 * X + 4))
    return _b11iq_match(expected, _b11iq_system, _B11IQ_GRID_2D, [X, Y])


# ----- Batch batch11-nf2 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch11-nf2.ts (batch batch11-nf2).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch11_nf2.py --only-extra

Each function derives the answer from the stem's givens: a numeric result for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items
whose choices are equations, points, inequalities or sentences.
"""

import re


import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq, sqrt

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")
h = Symbol("h")


def _b11nf_rhs(choice):
    """'$y = ...$' or '$g(x) = ...$' -> the right side as a SymPy expression."""
    return latex_to_sympy_ext(choice.strip().strip("$").split("=", 1)[1])


def _b11nf_rhs_match(expected, samples, label=""):
    """MC with equation choices: exactly the key's right side equals `expected` at every sample x."""

    def check(choices, idx):
        matches = []
        for i, ch in enumerate(choices):
            expr = _b11nf_rhs(ch)
            if all(abs(complex((expr - expected).subs(x, v).evalf(30))) < 1e-12 for v in samples):
                matches.append(i)
        return matches == [idx], f"{label or expected}; matching choices {matches}, key index {idx}"

    return check


def _b11nf_point(text):
    m = re.fullmatch(r"\$?\((-?[\d.]+),\s*(-?[\d.]+)\)\$?", text.strip())
    assert m, text
    return sp.nsimplify(m.group(1)), sp.nsimplify(m.group(2))


def _b11nf_interval(text):
    """'$x < a$', '$x > a$' or '$a < x < b$' -> a SymPy set."""
    s_ = text.strip().strip("$").replace(" ", "")
    m = re.fullmatch(r"x<(-?\d+)", s_)
    if m:
        return sp.Interval.open(-sp.oo, int(m.group(1)))
    m = re.fullmatch(r"x>(-?\d+)", s_)
    if m:
        return sp.Interval.open(int(m.group(1)), sp.oo)
    m = re.fullmatch(r"(-?\d+)<x<(-?\d+)", s_)
    if m:
        return sp.Interval.open(int(m.group(1)), int(m.group(2)))
    raise ValueError(text)


# ------------------------------------------------------------------ easy


def adv_nf_remainder_cubic_divided_by_binomial():
    P = x**3 - 4 * x**2 + 2 * x + 9
    rem = sp.rem(P, x - 3, x)
    assert rem == P.subs(x, 3)
    return rem


def adv_nf_radical_evaluate_scaled_root():
    return (3 * sqrt(2 * x - 1) + 4).subs(x, 5)


def adv_nf_rational_undefined_input():
    sols = sp.solve(Eq(2 * x - 10, 0), x)
    assert len(sols) == 1 and (x + 6).subs(x, sols[0]) != 0
    return sols[0]


def adv_nf_parabola_shift_left_down_equation():
    expected = (x + 3) ** 2 - 2  # left 3: x -> x + 3; down 2: subtract 2
    return _b11nf_rhs_match(expected, [-5, Rational(1, 2), 2, 7])


def adv_nf_pool_chemical_half_life_amount():
    A = 96 * Rational(1, 2) ** (t / 4)
    return A.subs(t, 12)


# ------------------------------------------------------------------ medium


def adv_nf_repeated_factor_touch_point():
    f = -2 * x * (x - 5) ** 2 * (x + 4)
    roots = sp.roots(sp.Poly(f, x))
    touch = [rt for rt, mult in roots.items() if mult % 2 == 0]
    assert len(touch) == 1
    return touch[0]


def adv_nf_cubic_negative_between_zeros():
    f = (x + 2) * (x - 1) * (x - 4)

    def check(choices, idx):
        neg = [i for i, ch in enumerate(choices) if f.subs(x, latex_to_sympy(ch)) < 0]
        return neg == [idx], f"choices with f(a) < 0: {neg}"

    return check


def adv_nf_equal_remainders_coefficient():
    Q = 3 * x**2 + b * x - 7
    sols = sp.solve(Eq(sp.rem(Q, x - 2, x), sp.rem(Q, x + 1, x)), b)
    assert len(sols) == 1
    return sols[0]


def adv_nf_rational_input_for_output_five():
    sols = [v for v in sp.solve(Eq((3 * x + 1) / (x - 2), 5), x) if v != 2]
    assert len(sols) == 1
    return sols[0]


def adv_nf_poster_average_cost():
    sols = [v for v in sp.solve(Eq((1440 + 12 * n) / n, 20), n) if v > 0]
    assert len(sols) == 1
    return sols[0]


def adv_nf_radical_graph_endpoint():
    g = sqrt(12 - 3 * x) + 2
    xe = sp.solve(Eq(12 - 3 * x, 0), x)[0]
    # g is real only for x <= xe, so (xe, g(xe)) is the endpoint
    assert g.subs(x, xe + 1).is_real is False and g.subs(x, xe - 1).is_real
    end = (xe, g.subs(x, xe))

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices) if _b11nf_point(ch) == end]
        return hits == [idx], f"endpoint {end}; matching choices {hits}"

    return check


def adv_nf_laptop_half_life_period():
    hp = Symbol("hp", positive=True)
    sols = sp.solve(Eq(640 * Rational(1, 2) ** (6 / hp), 80), hp)
    assert len(sols) == 1
    return sols[0]


def adv_nf_caffeine_half_life_interpret():
    C = 200 * Rational(1, 2) ** (t / 5)
    c0, c1 = C.subs(t, 0), C.subs(t, 1)
    halves_every_5 = sp.simplify(C.subs(t, t + 5) / C) == Rational(1, 2)

    def check(choices, idx):
        key_ok = "half every 5 hours" in choices[idx] and halves_every_5
        wrong = [i for i, ch in enumerate(choices) if i != idx and (
            ("by 5 milligrams" in ch and sp.simplify(c0 - c1 - 5) != 0)
            or ("by 5%" in ch and sp.simplify(c1 / c0 - Rational(95, 100)) != 0)
            or ("one-fifth" in ch and sp.simplify(c1 / c0 - Rational(4, 5)) != 0))]
        ok = key_ok and sorted(wrong + [idx]) == [0, 1, 2, 3]
        return ok, f"C(0)={c0}, C(1)={sp.N(c1, 6)}; contradicted {wrong}"

    return check


def adv_nf_sqrt_reflect_translate_equation():
    expected = -sqrt(x) + 4  # reflect across x-axis, then up 4
    return _b11nf_rhs_match(expected, [Rational(1, 4), 1, 3, 9])


def adv_nf_shift_right_new_x_intercept():
    f = sp.Lambda(x, (x + 1) * (x - 5))
    g = f(x - 2)
    zeros = set(sp.solve(g, x))

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices)
                if _b11nf_point(ch)[1] == 0 and _b11nf_point(ch)[0] in zeros]
        return hits == [idx], f"zeros of g {sorted(zeros)}; x-intercept choices {hits}"

    return check


def adv_nf_rational_constant_from_value():
    f = (x + k) / (x - 3)
    ks = sp.solve(Eq(f.subs(x, 5), 4), k)
    assert len(ks) == 1
    return f.subs({k: ks[0], x: 1})


# ------------------------------------------------------------------ hard


def adv_nf_solar_panels_two_towns():
    A = 500 * Rational(12, 10) ** t
    B = 2000 * Rational(105, 100) ** t
    tt = 0
    while not A.subs(t, tt) > B.subs(t, tt):
        tt += 1
    # A stays ahead afterwards (ratio (8/7)^t is increasing)
    assert all(A.subs(t, v) > B.subs(t, v) for v in range(tt, tt + 20))
    return Integer(tt)


def adv_nf_cubic_negative_leading_sign_interval():
    f = -(x + 3) * (x - 2) ** 2
    xr = Symbol("xr", real=True)
    sol = sp.solve_univariate_inequality(f.subs(x, xr) > 0, xr, relational=False)

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices) if _b11nf_interval(ch) == sol]
        return hits == [idx], f"solution set {sol}; matching choices {hits}"

    return check


def adv_nf_cubic_touch_cross_evaluate():
    P = a * (x + 1) * (x - 2) ** 2  # odd multiplicity at -1, even at 2, degree 3
    av = sp.solve(Eq(P.subs(x, 0), 12), a)
    assert len(av) == 1
    return P.subs({a: av[0], x: 4})


def adv_nf_remainder_factor_of_shifted():
    # Every polynomial with p(-3) = 5 is (x + 3)q(x) + 5; test the choices against several q.
    qs = [Integer(1), x**2 + 7, 2 * x**3 - x + 4, x - 11]

    def check(choices, idx):
        must = []
        for i, ch in enumerate(choices):
            d = latex_to_sympy(ch)
            if all(sp.rem(sp.expand((x + 3) * q + 5 - 5), d, x) == 0 for q in qs):
                must.append(i)
        return must == [idx], f"choices dividing p(x) - 5 for every sample p: {must}"

    return check


def adv_nf_pendulum_longer_swing():
    Lp = Symbol("Lp", positive=True)
    L5 = sp.solve(Eq(2 * sqrt(Lp), 5), Lp)
    L4 = sp.solve(Eq(2 * sqrt(Lp), 4), Lp)
    assert len(L5) == len(L4) == 1
    return L5[0] - L4[0]


def adv_nf_two_samples_equal_mass():
    tp = Symbol("tp", real=True)
    A = 400 * Rational(1, 2) ** (tp / 3)
    B = 100 * Rational(1, 2) ** (tp / 6)
    sols = sp.solve(Eq(A, B), tp)
    assert len(sols) == 1
    return sols[0]


def adv_nf_shift_left_down_expanded():
    f = sp.Lambda(x, x**2 - 4 * x)
    expected = sp.expand(f(x + 2) - 5)
    return _b11nf_rhs_match(expected, [-3, Rational(1, 2), 2, 5])


def adv_nf_model_rocket_three_heights():
    H = a * t**2 + b * t + c
    sol = sp.solve([Eq(H.subs(t, 1), 38), Eq(H.subs(t, 2), 63), Eq(H.subs(t, 3), 78)], [a, b, c])
    Hm = H.subs(sol)
    assert sol[a] < 0
    tv = sp.solve(sp.diff(Hm, t), t)[0]
    return Hm.subs(t, tv)


def adv_nf_rational_point_undefined_input():
    f = 8 / (x - k) + 3
    ks = sp.solve(Eq(f.subs(x, 5), 7), k)
    assert len(ks) == 1
    return ks[0]  # f is undefined where x - k = 0


def adv_nf_half_life_ratio_constant():
    hp = Symbol("hp", positive=True)
    f = 500 * Rational(1, 2) ** (x / hp)
    sols = sp.solve(Eq(f.subs(x, 4), 2 * f.subs(x, 10)), hp)
    assert len(sols) == 1
    return sols[0]


def adv_nf_factored_cubic_remainder_constant():
    P = (x - a) * (x - 4) * (x + 2)
    sols = sp.solve(Eq(sp.rem(sp.expand(P), x - 1, x), 18), a)
    assert len(sols) == 1
    return sols[0]


# ----- Batch batch12-le2v2 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch12-le2v2.ts (batch batch12-le2v2).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch12_le2v2.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers (equations, points).
"""



import sympy as sp
from sympy import Eq, Rational, sqrt, symbols

x, y, k, p, t, n = symbols("x y k p t n")


# ----- helpers (prefix _b12l2_) -----


def _b12l2_line(pts):
    """y as an expression in x for the line through two points."""
    (x1, y1), (x2, y2) = [(sp.nsimplify(u), sp.nsimplify(v)) for u, v in pts]
    m = (y2 - y1) / (x2 - x1)
    return sp.expand(y1 + m * (x - x1))


def _b12l2_eq(choice):
    """'$lhs = rhs$' -> lhs - rhs as a SymPy expression ('{,}' thousands separators allowed)."""
    s = choice.strip().strip("$").replace("{,}", "")
    lhs, rhs = s.split("=")
    return sp.expand(latex_to_sympy_ext(lhs) - latex_to_sympy_ext(rhs))


def _b12l2_point(choice):
    inner = choice.strip().strip("$").strip().strip("()")
    u, v = inner.split(",")
    return latex_to_sympy_ext(u), latex_to_sympy_ext(v)


def _b12l2_unique(matches, idx, what):
    return matches == [idx], f"choices satisfying {what}: {matches}, key index {idx}"


def _b12l2_same_line(e1, e2):
    """True if e1 = 0 and e2 = 0 are the same line (proportional coefficients)."""
    v1 = [e1.coeff(x), e1.coeff(y), e1.subs({x: 0, y: 0})]
    v2 = [e2.coeff(x), e2.coeff(y), e2.subs({x: 0, y: 0})]
    return sp.Matrix([v1, v2]).rank() == 1


# ----- checks -----


def alg_vertical_line_shared_x_equation():
    pts = [(-3, 2), (-3, 9)]

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices)
                   if all(_b12l2_eq(ch).subs({x: px, y: py}) == 0 for px, py in pts)]
        return _b12l2_unique(matches, idx, "line through (-3, 2) and (-3, 9)")

    return check


def alg_perpendicular_to_vertical_y_crossing_spr():
    # x = 7 has direction (0, 1); a perpendicular line through (5, -2) has direction (1, 0).
    d_perp = sp.Matrix([1, 0])
    assert sp.Matrix([0, 1]).dot(d_perp) == 0
    s_ = symbols("s_")
    px, py = 5 + s_ * d_perp[0], -2 + s_ * d_perp[1]
    return sp.sympify(py).subs(s_, sp.solve(px, s_)[0])


def alg_collinear_point_k_and_k_plus_13():
    line = _b12l2_line([(-2, 5), (4, -7)])
    return sp.solve(Eq(line.subs(x, k), k + 13), k)[0]


def alg_table_missing_y_entry_spr():
    return _b12l2_line([(2, 7), (6, 17)]).subs(x, 11)


def alg_origin_line_missing_x_coordinate():
    line = _b12l2_line([(0, 0), (8, 6)])
    return sp.solve(Eq(line.subs(x, k), 15), k)[0]


def alg_origin_constant_slope():
    e = (k - 3) * x + 4 * y - (2 * k - 10)
    kv = sp.solve(e.subs({x: 0, y: 0}), k)[0]
    return sp.solve(e.subs(k, kv), y)[0].diff(x)


def alg_x_intercept_parallel_line_equation():
    given = 3 * x - 2 * y - 7
    m = sp.solve(given, y)[0].diff(x)
    target = y - m * (x + 4)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b12l2_same_line(_b12l2_eq(ch), target)]
        return _b12l2_unique(matches, idx, "line through (-4, 0) parallel to 3x - 2y = 7")

    return check


def alg_intercepts_ten_units_apart_k():
    kp = symbols("kp", positive=True)
    e = kp * x + 3 * y - 24
    xi = sp.solve(e.subs(y, 0), x)[0]
    yi = sp.solve(e.subs(x, 0), y)[0]
    sols = sp.solve(Eq(xi**2 + yi**2, 10**2), kp)
    assert len(sols) == 1
    return sols[0]


def alg_verbal_rate_x_axis_crossing():
    m = Rational(-2, 3)
    line = -1 + m * (x - 6)
    return sp.solve(line, x)[0]


def alg_collinear_equal_spacing_k_spr():
    pts = sp.Matrix([[0, k, 1], [3, 2 * k, 1], [6, 10, 1]])
    return sp.solve(pts.det(), k)[0]


def alg_table_entries_p_and_2p():
    line = _b12l2_line([(1, 5), (3, 11)])
    return sp.solve(Eq(line.subs(x, p), 2 * p), p)[0]


def alg_horizontal_vertical_intersection_point():
    sol = sp.solve([Eq(y, -9), Eq(x, 4)], [x, y])

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b12l2_point(ch) == (sol[x], sol[y])]
        return _b12l2_unique(matches, idx, f"intersection {(sol[x], sol[y])}")

    return check


def alg_undefined_slope_points_with_k():
    kv = sp.solve(Eq(k + 1, 3 * k - 7), k)[0]
    xv = kv + 1
    assert (3 * kv - 7) == xv

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b12l2_same_line(_b12l2_eq(ch), x - xv)]
        return _b12l2_unique(matches, idx, f"vertical line x = {xv}")

    return check


def alg_horizontal_line_constant_y_crossing():
    kv = sp.solve(2 * k - 6, k)[0]
    e = (2 * kv - 6) * x + (kv + 1) * y - 20
    assert e.coeff(x) == 0
    return sp.solve(e.subs(x, 0), y)[0]


def alg_patio_tiles_table_missing_count():
    # small tiles as a linear function of large tiles, through (40, 12) and (32, 36)
    small = _b12l2_line([(40, 12), (32, 36)])
    return small.subs(x, 17)


def alg_seed_packet_boxes_combination_count_spr():
    combos = [(s_, b_) for s_ in range(0, 61) for b_ in range(0, 61) if 4 * s_ + 6 * b_ == 60]
    return sp.Integer(len(combos))


def alg_catering_trays_verbal_rate_equation():
    m = Rational(-2, 3)
    target = y - 20 - m * (x - 6)

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b12l2_same_line(_b12l2_eq(ch), target)]
        return _b12l2_unique(matches, idx, "slope -2/3 through (6, 20)")

    return check


def alg_art_club_canvases_greatest_count():
    canv = [c_ for c_ in range(0, 15) for f_ in range(0, 15) if 6 * f_ + 15 * c_ == 84]
    return sp.Integer(max(canv))


def alg_dye_scarves_blankets_substitution():
    s_, b_ = symbols("s_ b_")
    return sp.solve(Eq(Rational(2, 5) * 60 + Rational(13, 20) * b_, 50), b_)[0]


def alg_concrete_sand_gravel_total_spr():
    s_, g_ = symbols("s_ g_")
    sol = sp.solve([Eq(5 * s_, 3 * g_), Eq(g_ - s_, 45)], [s_, g_])
    return sol[s_] + sol[g_]


def alg_tram_minutes_distance_equation():
    # distance = 30 * (x/60) + 12 * (y/60) = 48
    target = 30 * x / 60 + 12 * y / 60 - 48

    def check(choices, idx):
        matches = [i for i, ch in enumerate(choices) if _b12l2_same_line(_b12l2_eq(ch), target)]
        return _b12l2_unique(matches, idx, "30(x/60) + 12(y/60) = 48")

    return check


# ----- Batch batch12-ee3 -----
#!/usr/bin/env python3
"""SymPy key checks for web/content/batches/batch12-ee3.ts (batch batch12-ee3, Equivalent expressions).

Run from the repo root, against a temp items file that contains the batch:

    python3 web/scripts/verify_items.py --items <tmp items.ts> \
        --checks web/scripts/checks_batch12_ee3.py --only-extra

Each function derives the answer from the stem's givens: an exact SymPy value for
numeric keys, or a callable (choices, answer_index) -> (ok, detail) for items whose
choices are expressions.
"""



import sympy as sp
from sympy import Rational, Integer, Symbol, symbols, Eq, sqrt

x, y, k, a, b, c, p, s, r, n, t = symbols("x y k a b c p s r n t")
d, q, u = symbols("d q u")


def _b12e3_matches(choices, expected_fn, samples):
    """Indices of the choices that agree with expected_fn at every sample (dict of symbol values)."""
    out = []
    for i, ch in enumerate(choices):
        expr = latex_to_sympy_ext(ch)
        if all(abs(complex((expr.subs(sv) - expected_fn(sv)).evalf(30))) < 1e-12 for sv in samples):
            out.append(i)
    return out


def _b12e3_expr_check(expected, samples, label=""):
    """MC with expression choices: exactly the key equals `expected` at every sample point."""

    def check(choices, idx):
        try:
            m = _b12e3_matches(choices, lambda sv: expected.subs(sv), samples)
        except Exception as e:  # noqa: BLE001
            return False, f"could not parse a choice: {e}"
        return m == [idx], f"{label or expected}; matching choices {m}, key index {idx}"

    return check


def _b12e3_not_equiv_check(expected, samples, label=""):
    """MC 'NOT equivalent': exactly one choice (the key) disagrees with `expected`."""

    def check(choices, idx):
        try:
            m = _b12e3_matches(choices, lambda sv: expected.subs(sv), samples)
        except Exception as e:  # noqa: BLE001
            return False, f"could not parse a choice: {e}"
        odd = [i for i in range(len(choices)) if i not in m]
        return odd == [idx], f"{label}; non-equivalent choices {odd}, key index {idx}"

    return check


def _b12e3_coeffs(identity, unknowns, var=None):
    """Solve a polynomial identity (expression == 0 for all values of var) for the unknown constants."""
    return sp.solve(sp.Poly(sp.expand(identity), var if var is not None else x).all_coeffs(), unknowns, dict=True)


_B12E3_X = [{x: v} for v in (Rational(-7, 2), Rational(-1, 3), Rational(1, 3), Rational(3, 2), Rational(7, 2), 5, 11)]
_B12E3_XPOS = [{x: v} for v in (Rational(1, 4), Rational(2, 3), 2, 5, 9)]
_B12E3_XY = [{x: xv, y: yv} for xv, yv in ((1, 2), (3, Rational(1, 2)), (Rational(2, 5), 4), (-3, 7), (5, -2))]


# ------------------------------------------------------------------ easy


def adv_ee3_gcf_identify_two_variable():
    t1, t2 = 18 * x**5 * y**2, 24 * x**3 * y**4
    g = sp.gcd(t1, t2)
    assert sp.simplify(t1 / g).is_polynomial(x, y) and sp.simplify(t2 / g).is_polynomial(x, y)

    def check(choices, idx):
        m = [i for i, ch in enumerate(choices) if sp.expand(latex_to_sympy_ext(ch) - g) == 0]
        return m == [idx], f"gcd {g}; matching choices {m}, key index {idx}"

    return check


def adv_ee3_divide_trinomial_by_monomial():
    expr = sp.cancel((6 * x**3 + 9 * x**2 - 3 * x) / (3 * x))
    assert expr == 2 * x**2 + 3 * x - 1
    return _b12e3_expr_check(expr, _B12E3_X, label=str(expr))


def adv_ee3_difference_squares_fraction_coefficient():
    return _b12e3_expr_check(x**2 / 4 - 25, _B12E3_X, label="x^2/4 - 25")


def adv_ee3_trinomial_two_variable_factor():
    expr = x**2 - 3 * x * y - 28 * y**2
    assert sp.factor(expr) == (x - 7 * y) * (x + 4 * y)
    return _b12e3_expr_check(expr, _B12E3_XY, label=str(sp.factor(expr)))


def adv_ee3_store_shelves_cans_total():
    expr = sp.expand((x + 3) * (2 * x - 1) + 5)
    return _b12e3_expr_check(expr, _B12E3_X, label=str(expr))


# ------------------------------------------------------------------ medium


def adv_ee3_gcf_variable_exponent_n():
    expr = x ** (n + 4) - 9 * x ** (n + 2)
    samples = [{n: nv, x: xv} for nv in (1, 2, 3, 4) for xv in (Rational(1, 2), 2, 5, -3)]
    return _b12e3_expr_check(expr, samples, label="x^(n+2)(x-3)(x+3) for n = 1..4")


def adv_ee3_absolute_value_two_terms_negative():
    expr = sp.Abs(x - 3) - sp.Abs(x + 2) + x
    samples = [{x: v} for v in (Rational(-5, 2), -3, Rational(-9, 2), -7, -20)]  # stem restricts x < -2
    for sv in samples:
        assert expr.subs(sv) == sv[x] + 5
    return _b12e3_expr_check(expr, samples, label="x + 5 for x < -2")


def adv_ee3_factored_form_zero_p():
    sols = _b12e3_coeffs(3 * x**2 + 4 * x - 15 - 3 * (x - p) * (x - q), [p, q])
    ok = [sv for sv in sols if sv[p] > sv[q]]
    assert len(ok) == 1
    return ok[0][p]


def adv_ee3_not_equivalent_product_forms():
    return _b12e3_not_equiv_check(sp.expand((x - 4) * (x + 6)), _B12E3_X, label="(x - 4)(x + 6)")


def adv_ee3_substitution_u_shift():
    target = x**2 - 6 * x + 4
    in_u = sp.expand(target.subs(x, u + 3))
    assert in_u == u**2 - 5
    samples = [{u: v} for v in (-3, Rational(-1, 2), 0, Rational(2, 3), 4, 9)]
    # Each choice in u must equal the given expression at x = u + 3.
    return _b12e3_expr_check(target.subs(x, u + 3), samples, label=f"in terms of u: {in_u}")


def adv_ee3_cube_of_sum_k():
    sols = _b12e3_coeffs((x + 2) ** 3 - (x**3 + 8) - k * x * (x + 2), [k])
    assert len(sols) == 1
    return sols[0][k]


def adv_ee3_negative_rational_exponent_radical():
    xp = Symbol("xp", positive=True)
    val = xp ** Rational(-3, 2)
    assert sp.simplify(val - 1 / (xp * sqrt(xp))) == 0
    return _b12e3_expr_check(x ** Rational(-3, 2), _B12E3_XPOS, label="x^(-3/2) = 1/(x sqrt(x))")


def adv_ee3_theater_ticket_revenue_b():
    sols = _b12e3_coeffs((12 + x) * (300 - 15 * x) - (a * x**2 + b * x + c), [a, b, c])
    assert len(sols) == 1
    return sols[0][b]


def adv_ee3_solar_panels_area_difference():
    expr = sp.expand((x + 3) ** 2 - (x - 3) ** 2)
    samples = [{x: v} for v in (Rational(7, 2), 4, Rational(11, 2), 9, 20)]  # stem restricts x > 3
    return _b12e3_expr_check(expr, samples, label=f"difference {expr}")


# ------------------------------------------------------------------ hard


def adv_ee3_absolute_value_quotient_b():
    expr = (x**2 - 4) / sp.Abs(x - 2)
    samples = [{x: v} for v in (Rational(3, 2), 0, -1, Rational(-7, 3), -10)]  # stem restricts x < 2
    # Fit ax + b from two points, then confirm on the rest.
    sol = sp.solve([Eq(a * sv[x] + b, expr.subs(sv)) for sv in samples[:2]], [a, b], dict=True)[0]
    for sv in samples:
        assert expr.subs(sv) == sol[a] * sv[x] + sol[b]
    return sol[b]


def adv_ee3_substitution_quartic_u():
    target = x**4 + 5 * x**2 + 4
    # x^2 = u - 1, so substitute x = sqrt(u - 1) for u > 1.
    in_u = sp.expand(target.subs(x, sqrt(u - 1)))
    assert in_u == u**2 + 3 * u
    samples = [{u: v} for v in (Rational(3, 2), 2, Rational(7, 3), 5, 10)]
    return _b12e3_expr_check(in_u, samples, label=f"in terms of u: {in_u}")


def adv_ee3_four_factor_x2_coefficient():
    poly = sp.Poly(sp.expand((x - 1) * (x + 2) * (x + 3) * (x - 4)), x)
    return poly.coeff_monomial(x**2)


def adv_ee3_quartic_over_quadratic_polynomial():
    expr = sp.cancel((x**4 - 10 * x**2 + 9) / (x**2 + 2 * x - 3))
    assert expr == x**2 - 2 * x - 3
    return _b12e3_expr_check(expr, _B12E3_X, label=f"quotient {expr}")


def adv_ee3_ball_height_shifted_time_k():
    sols = _b12e3_coeffs(-5 * t**2 + 30 * t + 2 - (-5 * (t - 3) ** 2 + k), [k], var=t)
    assert len(sols) == 1
    return sols[0][k]


def adv_ee3_not_equivalent_difference_squares():
    return _b12e3_not_equiv_check(9 * x**2 - 1, _B12E3_X, label="9x^2 - 1")


def adv_ee3_gcf_then_trinomial_a_plus_b():
    lhs = 12 * x**5 * y**2 + 18 * x**4 * y**3 - 30 * x**3 * y**4
    diff = sp.expand(lhs - 6 * x**3 * y**2 * (a * x + b * y) * (x - y))
    sols = sp.solve(sp.Poly(diff, x, y).coeffs(), [a, b], dict=True)
    assert len(sols) == 1
    return sols[0][a] + sols[0][b]


def adv_ee3_equal_coefficients_k():
    poly = sp.Poly(sp.expand((x**2 + k * x + 2) * (x**2 - 3 * x + 5)), x)
    sols = sp.solve(Eq(poly.coeff_monomial(x**3), poly.coeff_monomial(x)), k)
    assert len(sols) == 1
    return sols[0]


def adv_ee3_exponential_sum_squared():
    expr = (2**x + 2 ** (-x)) ** 2
    return _b12e3_expr_check(expr, _B12E3_X, label="(2^x + 2^-x)^2 = 4^x + 2 + 4^-x")


# ----- Batch batch12-ne3 -----
#!/usr/bin/env python3
"""SymPy checks for web/content/batches/batch12-ne3.ts (batch batch12-ne3).

Run through the shared verifier, which loads this module's CHECKS:

    python3 web/scripts/verify_items.py --items <items file> \
        --checks web/scripts/checks_batch12_ne3.py --only-extra

Same conventions as verify_items.py: each function returns the exact answer as
a SymPy object, or a callable (choices, answer_index) -> (ok, detail) for MC
items whose choices are not plain numbers (radicals, words, +- expressions).
"""



import sympy as sp
from sympy import Eq, Rational, Symbol, sqrt, symbols

x, y, k, t = symbols("x y k t")


# ----- helpers (prefix _b12n3_) -----

_B12N3_COUNT_WORDS = {0: "Zero", 1: "Exactly one", 2: "Exactly two", 3: "Exactly three", 4: "Exactly four"}


def _b12n3_real_roots(expr, var=x):
    """Distinct real roots of a polynomial or rational expression in var."""
    vr = Symbol(str(var) + "_r", real=True)
    return sorted(set(sp.solve(sp.together(expr).subs(var, vr), vr)))


def _b12n3_real_points(eqs):
    """Distinct real solutions (x, y) of a system of polynomial equations."""
    sols = sp.solve(eqs, [x, y], dict=True)
    pts = set()
    for s0 in sols:
        xv, yv = sp.simplify(s0[x]), sp.simplify(s0[y])
        if xv.is_real and yv.is_real:
            pts.add((xv, yv))
    return pts


def _b12n3_mc(expected):
    """Callable for numeric choices the base parser can't read (radicals)."""

    def check(choices, idx):
        vals = [latex_to_sympy_ext(ch) for ch in choices]
        matches = [i for i, v in enumerate(vals) if sp.simplify(v - expected) == 0]
        return matches == [idx], f"expected {expected}; matching choices {matches}"

    return check


def _b12n3_count(count):
    def check(choices, idx):
        word = _B12N3_COUNT_WORDS[count]
        hits = [i for i, ch in enumerate(choices) if ch == word]
        return hits == [idx], f"{count} solution(s) -> '{word}'; matching choices {hits}"

    return check


def _b12n3_pm_set(text):
    """'$3 \\pm \\sqrt{5}$' -> {3 + sqrt(5), 3 - sqrt(5)}."""
    s = text.strip().strip("$")
    left, right = s.split("\\pm")
    a0 = latex_to_sympy_ext(left) if left.strip() else sp.Integer(0)
    b0 = latex_to_sympy_ext(right)
    return {sp.nsimplify(a0 + b0), sp.nsimplify(a0 - b0)}


# ----- checks -----


def adv_ne3_square_49_negative_root():
    neg = [r for r in _b12n3_real_roots(x**2 - 49) if r < 0]
    assert len(neg) == 1
    return neg[0]


def adv_ne3_five_times_power_two():
    sols = sp.solve(Eq(5 * 2**x, 160), x)
    assert len(sols) == 1
    return sp.nsimplify(sols[0])


def adv_ne3_sqrt_plus_five_easy():
    xp = Symbol("xp", nonnegative=True)
    sols = sp.solve(Eq(sqrt(xp) + 5, 11), xp)
    assert len(sols) == 1
    return sols[0]


def adv_ne3_heating_coil_voltage():
    vp = Symbol("V", positive=True)
    sols = sp.solve(Eq(vp**2 / 24, 150), vp)
    assert len(sols) == 1
    return sols[0]


def adv_ne3_product_xy_line_easy():
    pts = [p for p in _b12n3_real_points([Eq(x * y, 18), Eq(y, 2 * x)]) if p[0] > 0]
    assert len(pts) == 1
    return pts[0][0]


def adv_ne3_base_four_sixty_four():
    xr = Symbol("xr", real=True)
    sols = sp.solve(Eq(4 ** (xr + 1), 64), xr)
    assert len(sols) == 1
    return sp.nsimplify(sols[0])


def adv_ne3_factored_repeated_count():
    return _b12n3_count(len(_b12n3_real_roots((x - 5) ** 2 * (x**2 - 25))))


def adv_ne3_meeting_handshakes():
    pos = [r for r in _b12n3_real_roots(x * (x - 1) / 2 - 45) if r > 0]
    assert len(pos) == 1 and pos[0].is_integer
    return pos[0]


def adv_ne3_auditorium_rows_seats():
    pos = [r for r in _b12n3_real_roots(x * (x + 8) - 384) if r > 0]
    assert len(pos) == 1 and pos[0].is_integer
    return pos[0]


def adv_ne3_podcast_base_four_weeks():
    sols = sp.solve(Eq(25 * 4 ** (t / 2), 1600), t)
    real = [sp.nsimplify(v) for v in sols if v.is_real]
    assert len(real) == 1
    return real[0]


def adv_ne3_given_root_other_fraction():
    kv = sp.solve((3 * x**2 + k * x - 20).subs(x, -4), k)[0]
    others = [r for r in _b12n3_real_roots(3 * x**2 + kv * x - 20) if r != -4]
    assert len(others) == 1
    return others[0]


def adv_ne3_line_parabola_second_point_y():
    pts = _b12n3_real_points([Eq(y, x**2 - 2 * x + 3), Eq(y, 2 * x + 3)])
    assert (0, 3) in pts and len(pts) == 2
    other = [p for p in pts if p != (0, 3)][0]
    return other[1]


def adv_ne3_circles_external_tangent_count():
    return _b12n3_count(len(_b12n3_real_points([Eq(x**2 + y**2, 9), Eq((x - 5) ** 2 + y**2, 4)])))


def adv_ne3_f_equals_f_double_quadratic():
    f = lambda v: v**2 - 6 * v + 10  # noqa: E731
    nz = [r for r in _b12n3_real_roots(f(x) - f(2 * x)) if r != 0]
    assert len(nz) == 1
    return nz[0]


def adv_ne3_one_ninth_base_three():
    xr = Symbol("xr", real=True)
    sols = sp.solve(Eq(Rational(1, 9) ** xr, 3 ** (xr + 6)), xr)
    assert len(sols) == 1
    return sp.nsimplify(sols[0])


def adv_ne3_product_sum_squares():
    pts = _b12n3_real_points([Eq(x * y, 12), Eq(x + y, 7)])
    vals = {sp.simplify(p[0] ** 2 + p[1] ** 2) for p in pts}
    assert len(vals) == 1
    return vals.pop()


def adv_ne3_quadratic_formula_expression():
    roots = set(_b12n3_real_roots(x**2 - 6 * x + 4))

    def check(choices, idx):
        hits = [i for i, ch in enumerate(choices)
                if {sp.simplify(v) for v in _b12n3_pm_set(ch)} == {sp.simplify(v) for v in roots}]
        return hits == [idx], f"roots {roots}; matching choices {hits}"

    return check


def adv_ne3_absolute_quadratic_four_count():
    xr = Symbol("xr", real=True)
    sols = set(sp.solve(sp.Abs(xr**2 - 5) - 4, xr))
    return _b12n3_count(len(sols))


def adv_ne3_train_braking_domain():
    good = [r for r in _b12n3_real_roots(3 * (12 - t) ** 2 - 75, t) if 0 <= r <= 12]
    assert len(good) == 1
    return good[0]


def adv_ne3_circle_parabola_three_count():
    return _b12n3_count(len(_b12n3_real_points([Eq(x**2 + y**2, 16), Eq(y, x**2 - 4)])))


def adv_ne3_circles_other_point_b():
    pts = _b12n3_real_points([Eq(x**2 + y**2, 25), Eq((x - 7) ** 2 + (y - 1) ** 2, 25)])
    assert (3, 4) in pts and len(pts) == 2
    return [p for p in pts if p != (3, 4)][0][1]


def adv_ne3_sixteen_four_quadratic_exponent():
    # Exponents match on the common base 4; confirm on the original equation.
    pos = [r for r in _b12n3_real_roots(2 * x**2 - (x + 3)) if r > 0]
    assert len(pos) == 1
    assert sp.simplify(16 ** (pos[0] ** 2) - 4 ** (pos[0] + 3)) == 0
    return pos[0]


def adv_ne3_roots_differ_by_one_k():
    kp = Symbol("kp", positive=True)
    cands = []
    for kv in sp.solve((kp**2 - 48) - 1, kp):  # (difference of roots)^2 = discriminant
        rts = _b12n3_real_roots(x**2 + kv * x + 12)
        if len(rts) == 2 and abs(rts[1] - rts[0]) == 1:
            cands.append(kv)
    assert len(cands) == 1
    return cands[0]


def adv_ne3_v_graph_circle_count():
    right = [r for r in _b12n3_real_roots(x**2 + (x + 1) ** 2 - 25) if r >= 0]
    left = [r for r in _b12n3_real_roots(x**2 + (-x + 1) ** 2 - 25) if r < 0]
    return _b12n3_count(len(set(right + left)))


def adv_ne3_product_ellipse_x_plus_2y():
    pts = [p for p in _b12n3_real_points([Eq(x * y, 10), Eq(x**2 + 4 * y**2, 41)]) if p[0] > 0 and p[1] > 0]
    vals = {sp.simplify(p[0] + 2 * p[1]) for p in pts}
    assert len(pts) == 2 and len(vals) == 1
    return vals.pop()


def adv_ne3_robots_north_east():
    pos = [r for r in _b12n3_real_roots((2 * x) ** 2 + (2 * (x + 2)) ** 2 - 400) if r > 0]
    assert len(pos) == 1
    return pos[0]


def adv_ne3_dance_floor_enlarged_area():
    pos = [r for r in _b12n3_real_roots((x + 4) * (x + 6) - 2 * x**2) if r > 0]
    assert len(pos) == 1
    return (pos[0] + 4) * (pos[0] + 6)


def adv_ne3_f_equals_f_double_rational():
    f = lambda v: v + 12 / v  # noqa: E731
    pos = [r for r in _b12n3_real_roots(f(x) - f(2 * x)) if r > 0]
    assert len(pos) == 1
    return _b12n3_mc(pos[0])


def adv_ne3_quartic_substitution_product():
    roots = _b12n3_real_roots((x**2 - 3 * x) ** 2 - (x**2 - 3 * x) - 12)
    assert len(roots) == 2
    return sp.prod(roots)


def adv_ne3_root_difference_squared():
    rts = _b12n3_real_roots(2 * x**2 - 4 * x - 3)
    assert len(rts) == 2
    return sp.simplify((rts[0] - rts[1]) ** 2)


def adv_ne3_exponential_system_sum():
    xr, yr = symbols("xr yr", real=True)
    sols = sp.solve([Eq(3**xr * 9**yr, 81), Eq(9**xr / 3**yr, 27)], [xr, yr], dict=True)
    if not sols:  # fall back to the exponent system on base 3
        sols = sp.solve([Eq(xr + 2 * yr, 4), Eq(2 * xr - yr, 3)], [xr, yr], dict=True)
    assert len(sols) == 1
    s0 = sols[0]
    assert sp.simplify(3 ** s0[xr] * 9 ** s0[yr] - 81) == 0
    assert sp.simplify(9 ** s0[xr] / 3 ** s0[yr] - 27) == 0
    return s0[xr] + s0[yr]


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
    # batch batch6-ee1
    "adv-gcf-monomial-three-terms": adv_gcf_monomial_three_terms,
    "adv-poly-add-two-variable": adv_poly_add_two_variable,
    "adv-power-of-monomial": adv_power_of_monomial,
    "adv-rational-exponent-to-radical": adv_rational_exponent_to_radical,
    "adv-mural-area-product": adv_mural_area_product,
    "adv-gcf-then-difference-squares": adv_gcf_then_difference_squares,
    "adv-trinomial-leading-ten": adv_trinomial_leading_ten,
    "adv-grouping-cubic-four-terms": adv_grouping_cubic_four_terms,
    "adv-complete-square-leading-two-k": adv_complete_square_leading_two_k,
    "adv-rational-add-unlike-denominators": adv_rational_add_unlike_denominators,
    "adv-rational-multiply-cancel-monomial": adv_rational_multiply_cancel_monomial,
    "adv-negative-exponent-quotient": adv_negative_exponent_quotient,
    "adv-revenue-vertex-form": adv_revenue_vertex_form,
    "adv-cubic-product-coefficient-c": adv_cubic_product_coefficient_c,
    "adv-banner-perimeter-factor": adv_banner_perimeter_factor,
    "adv-tilde-recentered-b": adv_tilde_recentered_b,
    "adv-rational-exponent-coefficient-quotient": adv_rational_exponent_coefficient_quotient,
    "adv-complete-square-unknown-k": adv_complete_square_unknown_k,
    "adv-rational-binomial-ratio-difference": adv_rational_binomial_ratio_difference,
    "adv-quartic-quadratic-form-a": adv_quartic_quadratic_form_a,
    "adv-patio-gravel-border-k": adv_patio_gravel_border_k,
    "adv-rational-product-four-factors": adv_rational_product_four_factors,
    "adv-exponent-difference-squares-a-minus-b": adv_exponent_difference_squares_a_minus_b,
    "adv-radical-perfect-square-negative-x": adv_radical_perfect_square_negative_x,
    # batch batch6-av
    "geo-trapezoid-parallel-sides-area": geo_trapezoid_parallel_sides_area,
    "geo-parallelogram-slanted-side-area": geo_parallelogram_slanted_side_area,
    "geo-triangle-altitude-from-area": geo_triangle_altitude_from_area,
    "geo-sphere-volume-from-diameter": geo_sphere_volume_from_diameter,
    "geo-rectangular-pyramid-volume": geo_rectangular_pyramid_volume,
    "geo-cone-cylinder-equal-volume-height": geo_cone_cylinder_equal_volume_height,
    "geo-square-inscribed-circle-region": geo_square_inscribed_circle_region,
    "geo-cylinder-total-surface-area": geo_cylinder_total_surface_area,
    "geo-cone-height-from-diameter-volume": geo_cone_height_from_diameter_volume,
    "geo-cone-half-radius-triple-height": geo_cone_half_radius_triple_height,
    "geo-cylinder-height-equals-diameter": geo_cylinder_height_equals_diameter,
    "geo-square-corners-octagon-area": geo_square_corners_octagon_area,
    "geo-hollow-tube-material-volume": geo_hollow_tube_material_volume,
    "geo-hemisphere-dome-volume": geo_hemisphere_dome_volume,
    "geo-tank-fill-time-minutes": geo_tank_fill_time_minutes,
    "geo-stage-area-square-centimeters": geo_stage_area_square_centimeters,
    "geo-wall-paint-quarts": geo_wall_paint_quarts,
    "geo-channel-trapezoid-volume": geo_channel_trapezoid_volume,
    "geo-cylinder-percent-volume-change": geo_cylinder_percent_volume_change,
    "geo-equilateral-perimeter-area": geo_equilateral_perimeter_area,
    "geo-square-pyramid-total-surface": geo_square_pyramid_total_surface,
    "geo-cylinder-volume-lateral-radius": geo_cylinder_volume_lateral_radius,
    "geo-cylinder-volume-27-surface-area": geo_cylinder_volume_27_surface_area,
    "geo-rectangle-scaled-area-difference": geo_rectangle_scaled_area_difference,
    "geo-triangle-two-altitudes-side": geo_triangle_two_altitudes_side,
    "geo-open-box-greatest-volume": geo_open_box_greatest_volume,
    "geo-salt-pile-cone-circumference": geo_salt_pile_cone_circumference,
    "geo-garden-path-uniform-width": geo_garden_path_uniform_width,
    "geo-similar-candles-wax": geo_similar_candles_wax,
    "geo-planter-soil-bags": geo_planter_soil_bags,
    # batch batch6-ne1
    "adv-trinomial-larger-root-factor": adv_trinomial_larger_root_factor,
    "adv-square-isolate-positive-x": adv_square_isolate_positive_x,
    "adv-factored-cubic-least-solution": adv_factored_cubic_least_solution,
    "adv-exponential-power-of-two-easy": adv_exponential_power_of_two_easy,
    "adv-absolute-value-negative-zero-solutions": adv_absolute_value_negative_zero_solutions,
    "adv-rug-room-floor-strip": adv_rug_room_floor_strip,
    "adv-quadratic-formula-positive-radical": adv_quadratic_formula_positive_radical,
    "adv-product-of-solutions-noninteger": adv_product_of_solutions_noninteger,
    "adv-rational-common-denominator-extraneous": adv_rational_common_denominator_extraneous,
    "adv-radical-equals-x-extraneous": adv_radical_equals_x_extraneous,
    "adv-line-parabola-y-difference": adv_line_parabola_y_difference,
    "adv-exponential-product-same-base": adv_exponential_product_same_base,
    "adv-circle-line-which-point": adv_circle_line_which_point,
    "adv-discriminant-zero-rearranged": adv_discriminant_zero_rearranged,
    "adv-biquadratic-real-solution-count": adv_biquadratic_real_solution_count,
    "adv-tossed-ball-second-time": adv_tossed_ball_second_time,
    "adv-raffle-price-revenue": adv_raffle_price_revenue,
    "adv-horizon-distance-radical": adv_horizon_distance_radical,
    "adv-drone-distance-absolute-value": adv_drone_distance_absolute_value,
    "adv-two-machines-rational-time": adv_two_machines_rational_time,
    "adv-stopping-distance-speed": adv_stopping_distance_speed,
    "adv-two-parabolas-greatest-integer-k": adv_two_parabolas_greatest_integer_k,
    "adv-factored-cubic-two-distinct-c": adv_factored_cubic_two_distinct_c,
    "adv-absolute-value-line-one-solution-c": adv_absolute_value_line_one_solution_c,
    "adv-double-radical-equation": adv_double_radical_equation,
    "adv-rational-all-extraneous-zero": adv_rational_all_extraneous_zero,
    "adv-line-circle-tangent-intercept-b": adv_line_circle_tangent_intercept_b,
    "adv-parabola-line-no-intersection-k": adv_parabola_line_no_intersection_k,
    "adv-root-twice-other-c": adv_root_twice_other_c,
    "adv-exponential-quadratic-in-two-power": adv_exponential_quadratic_in_two_power,
    "adv-absolute-value-steep-line-count": adv_absolute_value_steep_line_count,
    # batch batch7-psdaB
    "psda-orchard-young-apple-percent": psda_orchard_young_apple_percent,
    "psda-scale-reading-percent-error": psda_scale_reading_percent_error,
    "psda-helmet-price-before-tax": psda_helmet_price_before_tax,
    "psda-pond-fish-three-year-chain": psda_pond_fish_three_year_chain,
    "psda-a-b-c-percent-chain": psda_a_b_c_percent_chain,
    "psda-machine-value-depreciation": psda_machine_value_depreciation,
    "psda-store-hardcover-fiction-share": psda_store_hardcover_fiction_share,
    "psda-notebook-price-revenue": psda_notebook_price_revenue,
    "psda-rug-prices-chain-difference": psda_rug_prices_chain_difference,
    "psda-deposit-two-year-rate": psda_deposit_two_year_rate,
    "psda-homework-minutes-median": psda_homework_minutes_median,
    "psda-pets-dot-plot-range": psda_pets_dot_plot_range,
    "psda-missing-fifth-value-mean": psda_missing_fifth_value_mean,
    "psda-trips-frequency-median": psda_trips_frequency_median,
    "psda-add-value-mean-median-amounts": psda_add_value_mean_median_amounts,
    "psda-bakery-ovens-combined-mean": psda_bakery_ovens_combined_mean,
    "psda-race-time-recording-error": psda_race_time_recording_error,
    "psda-fish-length-box-plot-iqr": psda_fish_length_box_plot_iqr,
    "psda-shifted-spread-sets-compare": psda_shifted_spread_sets_compare,
    "psda-mode-median-greatest-value": psda_mode_median_greatest_value,
    "psda-two-sections-size-from-mean": psda_two_sections_size_from_mean,
    "psda-temperature-entry-error-effects": psda_temperature_entry_error_effects,
    "psda-household-cars-added-mean": psda_household_cars_added_mean,
    "psda-quiz-scores-correction-shift": psda_quiz_scores_correction_shift,
    "psda-rice-bags-added-at-mean": psda_rice_bags_added_at_mean,
    # batch batch7-ineq1
    "alg-ineq-collect-terms-easy": alg_ineq_collect_terms_easy,
    "alg-ineq-which-value-solution": alg_ineq_which_value_solution,
    "alg-ineq-compound-middle-term": alg_ineq_compound_middle_term,
    "alg-ineq-point-standard-form": alg_ineq_point_standard_form,
    "alg-ineq-swimmer-weekly-distance": alg_ineq_swimmer_weekly_distance,
    "alg-ineq-least-integer-fraction-flip": alg_ineq_least_integer_fraction_flip,
    "alg-ineq-count-integers-chain": alg_ineq_count_integers_chain,
    "alg-ineq-count-listed-points-system": alg_ineq_count_listed_points_system,
    "alg-ineq-boundary-line-two-points": alg_ineq_boundary_line_two_points,
    "alg-ineq-fractions-equivalent": alg_ineq_fractions_equivalent,
    "alg-ineq-ferry-trucks": alg_ineq_ferry_trucks,
    "alg-ineq-press-time-coefficient": alg_ineq_press_time_coefficient,
    "alg-ineq-farm-stand-revenue-point": alg_ineq_farm_stand_revenue_point,
    "alg-ineq-gym-plans-months": alg_ineq_gym_plans_months,
    "alg-ineq-rain-barrel-solution": alg_ineq_rain_barrel_solution,
    "alg-ineq-workshop-tables": alg_ineq_workshop_tables,
    "alg-ineq-candy-temperature-count": alg_ineq_candy_temperature_count,
    "alg-ineq-every-x-solution-k": alg_ineq_every_x_solution_k,
    "alg-ineq-no-solution-a": alg_ineq_no_solution_a,
    "alg-ineq-interval-all-satisfy-k": alg_ineq_interval_all_satisfy_k,
    "alg-ineq-point-on-line-system-k": alg_ineq_point_on_line_system_k,
    "alg-ineq-wedge-greatest-x": alg_ineq_wedge_greatest_x,
    "alg-ineq-difference-bounds": alg_ineq_difference_bounds,
    "alg-ineq-lattice-points-count": alg_ineq_lattice_points_count,
    # batch batch7-sys1
    "alg-sys-elim-subtract-y": alg_sys_elim_subtract_y,
    "alg-sys-substitute-linear-y-x-spr": alg_sys_substitute_linear_y_x_spr,
    "alg-sys-count-equal-slopes-zero": alg_sys_count_equal_slopes_zero,
    "alg-sys-intersection-standard-and-slope-form-x": alg_sys_intersection_standard_and_slope_form_x,
    "alg-sys-add-equations-for-sum": alg_sys_add_equations_for_sum,
    "alg-sys-difference-gives-2x-minus-y-spr": alg_sys_difference_gives_2x_minus_y_spr,
    "alg-sys-decimal-coefficients-y-spr": alg_sys_decimal_coefficients_y_spr,
    "alg-sys-fraction-coefficients-x-minus-y": alg_sys_fraction_coefficients_x_minus_y,
    "alg-sys-two-tables-intersection-b": alg_sys_two_tables_intersection_b,
    "alg-sys-verbal-lines-point-slope-x": alg_sys_verbal_lines_point_slope_x,
    "alg-sys-no-solution-fraction-slope-a": alg_sys_no_solution_fraction_slope_a,
    "alg-sys-infinite-shifted-constants-ab-spr": alg_sys_infinite_shifted_constants_ab_spr,
    "alg-sys-decimal-equation-infinite-partner": alg_sys_decimal_equation_infinite_partner,
    "alg-sys-half-k-coefficient-no-solution-spr": alg_sys_half_k_coefficient_no_solution_spr,
    "alg-sys-symmetric-coefficients-difference-of-squares": alg_sys_symmetric_coefficients_difference_of_squares,
    "alg-sys-slider-k-meet-on-x-axis": alg_sys_slider_k_meet_on_x_axis,
    "alg-sys-exactly-one-solution-condition": alg_sys_exactly_one_solution_condition,
    "alg-sys-parallel-line-through-point": alg_sys_parallel_line_through_point,
    "alg-sys-functions-intersection-then-evaluate": alg_sys_functions_intersection_then_evaluate,
    "alg-sys-line-through-intercepts-coordinate-sum": alg_sys_line_through_intercepts_coordinate_sum,
    "alg-sys-soap-sales-interpret-constant": alg_sys_soap_sales_interpret_constant,
    "alg-sys-pottery-studio-equal-cost-hours": alg_sys_pottery_studio_equal_cost_hours,
    "alg-sys-coffee-blend-pricier-beans": alg_sys_coffee_blend_pricier_beans,
    "alg-sys-cyclists-catch-up-distance-spr": alg_sys_cyclists_catch_up_distance_spr,
    "alg-sys-nursery-shrubs-trees-model": alg_sys_nursery_shrubs_trees_model,
    "alg-sys-car-rental-six-dollars-less": alg_sys_car_rental_six_dollars_less,
    "alg-sys-bagels-juices-combined-price": alg_sys_bagels_juices_combined_price,
    "alg-sys-two-clubs-members-table-weeks-spr": alg_sys_two_clubs_members_table_weeks_spr,
    "alg-sys-boat-current-speed": alg_sys_boat_current_speed,
    # batch batch7-lat
    "geo-vertical-angles-expression-measure": geo_vertical_angles_expression_measure,
    "geo-complementary-expressions-x": geo_complementary_expressions_x,
    "geo-linear-pair-ratio-four-to-one": geo_linear_pair_ratio_four_to_one,
    "geo-corresponding-angles-solve-x": geo_corresponding_angles_solve_x,
    "geo-equilateral-side-expressions-x": geo_equilateral_side_expressions_x,
    "geo-angle-ratio-largest-angle": geo_angle_ratio_largest_angle,
    "geo-alternate-interior-obtuse-angle": geo_alternate_interior_obtuse_angle,
    "geo-isosceles-exterior-base-angle": geo_isosceles_exterior_base_angle,
    "geo-regular-polygon-sides-156": geo_regular_polygon_sides_156,
    "geo-side-splitter-parallel-length": geo_side_splitter_parallel_length,
    "geo-dilation-angle-unchanged": geo_dilation_angle_unchanged,
    "geo-triangle-inequality-integer-count": geo_triangle_inequality_integer_count,
    "geo-quadrilateral-diagonal-congruence": geo_quadrilateral_diagonal_congruence,
    "geo-linear-pair-quadratic-angle": geo_linear_pair_quadratic_angle,
    "geo-triangle-fraction-angle-expressions": geo_triangle_fraction_angle_expressions,
    "geo-exterior-angle-quadratic-interior": geo_exterior_angle_quadratic_interior,
    "geo-side-splitter-quadratic-length": geo_side_splitter_quadratic_length,
    "geo-pond-width-crossing-segments": geo_pond_width_crossing_segments,
    "geo-regular-frame-perimeter-140": geo_regular_frame_perimeter_140,
    "geo-welded-tubes-third-side": geo_welded_tubes_third_side,
    "geo-mirror-beam-lamp-height": geo_mirror_beam_lamp_height,
    "geo-pentagon-flower-bed-fifth-angle": geo_pentagon_flower_bed_fifth_angle,
    "geo-rail-lines-same-side-interior": geo_rail_lines_same_side_interior,
    "geo-equilateral-extension-angle-bad": geo_equilateral_extension_angle_bad,
    "geo-shared-angle-similar-side": geo_shared_angle_similar_side,
    "geo-angle-bisectors-meet-bic": geo_angle_bisectors_meet_bic,
    "geo-parallel-lines-bent-path-angle": geo_parallel_lines_bent_path_angle,
    # batch batch8-rtt
    "geo-ladder-wall-height-pythagorean": geo_ladder_wall_height_pythagorean,
    "geo-legs-9-40-hypotenuse": geo_legs_9_40_hypotenuse,
    "geo-isosceles-right-leg-9-hypotenuse": geo_isosceles_right_leg_9_hypotenuse,
    "geo-tan-e-from-three-sides": geo_tan_e_from_three_sides,
    "geo-sin-28-cos-x-complement": geo_sin_28_cos_x_complement,
    "geo-radians-7pi-12-to-degrees": geo_radians_7pi_12_to_degrees,
    "geo-post-shadow-sun-elevation": geo_post_shadow_sun_elevation,
    "geo-river-width-survey-tangent": geo_river_width_survey_tangent,
    "geo-truck-ramp-length-sine": geo_truck_ramp_length_sine,
    "geo-escalator-horizontal-30-60-90": geo_escalator_horizontal_30_60_90,
    "geo-cliff-elevation-arccos": geo_cliff_elevation_arccos,
    "geo-30-60-90-longer-leg-hypotenuse": geo_30_60_90_longer_leg_hypotenuse,
    "geo-cos-to-tan-nontriple": geo_cos_to_tan_nontriple,
    "geo-similar-triangle-tan-scaled": geo_similar_triangle_tan_scaled,
    "geo-triangle-angles-sin-cos-equal": geo_triangle_angles_sin_cos_equal,
    "geo-complementary-radians-k": geo_complementary_radians_k,
    "geo-tan-2pi-3-unit-circle": geo_tan_2pi_3_unit_circle,
    "geo-altitude-45-30-split-base": geo_altitude_45_30_split_base,
    "geo-parallel-segment-cos-complement": geo_parallel_segment_cos_complement,
    "geo-sin-x-squared-cos-x": geo_sin_x_squared_cos_x,
    "geo-isosceles-base-cosine": geo_isosceles_base_cosine,
    "geo-right-triangle-area-hypotenuse-angle": geo_right_triangle_area_hypotenuse_angle,
    "geo-shadow-flagpole-hypotenuse": geo_shadow_flagpole_hypotenuse,
    "geo-lighthouse-two-elevations": geo_lighthouse_two_elevations,
    "geo-legs-differ-by-7-area": geo_legs_differ_by_7_area,
    "geo-sum-angles-sine-negative-root3": geo_sum_angles_sine_negative_root3,
    "geo-square-diagonal-2-more": geo_square_diagonal_2_more,
    "geo-sin-twice-cos-value": geo_sin_twice_cos_value,
    # batch batch8-psdaC
    "psda-shipping-weight-rate-interpretation": psda_shipping_weight_rate_interpretation,
    "psda-bicycle-resale-intercept": psda_bicycle_resale_intercept,
    "psda-bamboo-shoot-prediction": psda_bamboo_shoot_prediction,
    "psda-iced-drinks-residual": psda_iced_drinks_residual,
    "psda-candle-height-regression": psda_candle_height_regression,
    "psda-spring-length-regression-prediction": psda_spring_length_regression_prediction,
    "psda-points-constant-ratio-relationship": psda_points_constant_ratio_relationship,
    "psda-ticket-price-revenue-quadratic": psda_ticket_price_revenue_quadratic,
    "psda-apartment-rent-association": psda_apartment_rent_association,
    "psda-points-leveling-association": psda_points_leveling_association,
    "psda-exhibit-visitors-models-compare": psda_exhibit_visitors_models_compare,
    "psda-tree-species-equal-height": psda_tree_species_equal_height,
    "psda-printer-value-decay-interpretation": psda_printer_value_decay_interpretation,
    "psda-points-above-model-line": psda_points_above_model_line,
    "psda-study-hours-intercept-from-means": psda_study_hours_intercept_from_means,
    "psda-forum-members-exponential-fit": psda_forum_members_exponential_fit,
    "psda-bulb-shipment-expected-defective": psda_bulb_shipment_expected_defective,
    "psda-fair-food-ride-joint": psda_fair_food_ride_joint,
    "psda-bean-plants-soil-given-flowered": psda_bean_plants_soil_given_flowered,
    "psda-game-club-neither": psda_game_club_neither,
    "psda-display-bin-red-apples": psda_display_bin_red_apples,
    "psda-spanish-art-given-art": psda_spanish_art_given_art,
    "psda-tiles-with-replacement-both-blue": psda_tiles_with_replacement_both_blue,
    "psda-inspection-truck-given-failed": psda_inspection_truck_given_failed,
    "psda-household-pets-at-least-two": psda_household_pets_at_least_two,
    "psda-two-lines-defective-source": psda_two_lines_defective_source,
    # batch batch8-le1v1
    "alg-decimal-quarter-coefficients-solve": alg_decimal_quarter_coefficients_solve,
    "alg-distribute-negative-two-spr": alg_distribute_negative_two_spr,
    "alg-flour-batches-equation": alg_flour_batches_equation,
    "alg-submarine-depth-constant-meaning": alg_submarine_depth_constant_meaning,
    "alg-literal-solve-m-three-terms": alg_literal_solve_m_three_terms,
    "alg-three-unit-fractions-of-x-solve": alg_three_unit_fractions_of_x_solve,
    "alg-decimal-distribute-both-sides-spr": alg_decimal_distribute_both_sides_spr,
    "alg-value-3x-minus-5-from-12x": alg_value_3x_minus_5_from_12x,
    "alg-count-solutions-x-zero-trap": alg_count_solutions_x_zero_trap,
    "alg-parking-additional-hours": alg_parking_additional_hours,
    "alg-caterer-guests-literal": alg_caterer_guests_literal,
    "alg-common-factor-x-minus-2-spr": alg_common_factor_x_minus_2_spr,
    "alg-two-thirds-one-fourth-distribute": alg_two_thirds_one_fourth_distribute,
    "alg-silos-equal-grain": alg_silos_equal_grain,
    "alg-strawberry-crews-rate-spr": alg_strawberry_crews_rate_spr,
    "alg-value-3x-minus-2-structure-spr": alg_value_3x_minus_2_structure_spr,
    "alg-literal-x-two-fractions-abc": alg_literal_x_two_fractions_abc,
    "alg-no-solution-fraction-k": alg_no_solution_fraction_k,
    "alg-decimal-mixture-value-40-minus-x": alg_decimal_mixture_value_40_minus_x,
    "alg-repeated-binomial-value-5x": alg_repeated_binomial_value_5x,
    "alg-pick-one-var-equation-no-solution": alg_pick_one_var_equation_no_solution,
    # batch batch8-nf1
    "adv-nf-rational-evaluate-at-five": adv_nf_rational_evaluate_at_five,
    "adv-nf-cubic-x-intercept-point": adv_nf_cubic_x_intercept_point,
    "adv-nf-vertex-form-minimum-value": adv_nf_vertex_form_minimum_value,
    "adv-nf-channel-followers-weekly-percent": adv_nf_channel_followers_weekly_percent,
    "adv-nf-factored-vertex-x-coordinate": adv_nf_factored_vertex_x_coordinate,
    "adv-nf-composition-quadratic-linear": adv_nf_composition_quadratic_linear,
    "adv-nf-radical-input-for-output": adv_nf_radical_input_for_output,
    "adv-nf-exponential-input-for-output": adv_nf_exponential_input_for_output,
    "adv-nf-exponential-form-displays-y-intercept": adv_nf_exponential_form_displays_y_intercept,
    "adv-nf-hive-half-year-factor": adv_nf_hive_half_year_factor,
    "adv-nf-exponential-from-three-values": adv_nf_exponential_from_three_values,
    "adv-nf-museum-visitors-point": adv_nf_museum_visitors_point,
    "adv-nf-wave-speed-depth": adv_nf_wave_speed_depth,
    "adv-nf-rational-shift-x-intercept": adv_nf_rational_shift_x_intercept,
    "adv-nf-island-rabbits-initial": adv_nf_island_rabbits_initial,
    "adv-nf-table-shift-scale-evaluate": adv_nf_table_shift_scale_evaluate,
    "adv-nf-quadratic-positive-input": adv_nf_quadratic_positive_input,
    "adv-nf-regression-reflect-shift-max": adv_nf_regression_reflect_shift_max,
    "adv-nf-exponential-doubling-period": adv_nf_exponential_doubling_period,
    "adv-nf-tea-cooling-constant": adv_nf_tea_cooling_constant,
    "adv-nf-shifted-exponential-two-points": adv_nf_shifted_exponential_two_points,
    "adv-nf-factored-plus-c-y-intercept": adv_nf_factored_plus_c_y_intercept,
    "adv-nf-composition-find-linear": adv_nf_composition_find_linear,
    "adv-nf-pen-wall-max-area": adv_nf_pen_wall_max_area,
    "adv-nf-bridge-cable-length-below": adv_nf_bridge_cable_length_below,
    "adv-nf-cubic-shift-up-intercept-count": adv_nf_cubic_shift_up_intercept_count,
    "adv-nf-exponential-input-scale-rewrite": adv_nf_exponential_input_scale_rewrite,
    "adv-nf-quadratic-symmetric-values": adv_nf_quadratic_symmetric_values,
    # batch batch9-le2v1
    "alg-slope-standard-form-7x-2y": alg_slope_standard_form_7x_2y,
    "alg-point-on-line-5x-3y-17": alg_point_on_line_5x_3y_17,
    "alg-x-intercept-slope-intercept-form": alg_x_intercept_slope_intercept_form,
    "alg-slope-from-two-intercepts": alg_slope_from_two_intercepts,
    "alg-hostel-pillows-term-meaning": alg_hostel_pillows_term_meaning,
    "alg-two-points-standard-form-equation": alg_two_points_standard_form_equation,
    "alg-perpendicular-slope-standard-form": alg_perpendicular_slope_standard_form,
    "alg-rewrite-to-standard-form-c": alg_rewrite_to_standard_form_c,
    "alg-intercepts-triangle-area": alg_intercepts_triangle_area,
    "alg-point-slope-to-standard-form": alg_point_slope_to_standard_form,
    "alg-moving-boxes-table-equation": alg_moving_boxes_table_equation,
    "alg-club-hoodies-keychains-tradeoff": alg_club_hoodies_keychains_tradeoff,
    "alg-yarn-twine-combination-spr": alg_yarn_twine_combination_spr,
    "alg-slope-constant-x-intercept-spr": alg_slope_constant_x_intercept_spr,
    "alg-perpendicular-shared-x-intercept": alg_perpendicular_shared_x_intercept,
    "alg-point-shift-stays-on-line": alg_point_shift_stays_on_line,
    "alg-shared-y-intercept-x-intercept-spr": alg_shared_y_intercept_x_intercept_spr,
    "alg-barge-containers-slope-meaning": alg_barge_containers_slope_meaning,
    "alg-ribbon-pieces-unit-equation": alg_ribbon_pieces_unit_equation,
    "alg-fudge-toffee-intercepts-difference": alg_fudge_toffee_intercepts_difference,
    "alg-parallel-through-point-which-point": alg_parallel_through_point_which_point,
    # batch batch9-psdaD
    "psda-infer-library-overdue-estimate": _b9pd_library_overdue,
    "psda-infer-bolts-not-defective-total": _b9pd_bolts_not_defective,
    "psda-infer-ev-households-upper-total": _b9pd_ev_upper_total,
    "psda-infer-apartment-occupants-total": _b9pd_occupants_total,
    "psda-infer-orchard-yield-least-total": _b9pd_orchard_least_total,
    "psda-infer-plausible-proportion-value": _b9pd_plausible_proportion,
    "psda-infer-park-visit-smaller-margin": _b9pd_smaller_margin,
    "psda-infer-two-towns-commute-intervals": _b9pd_commute_intervals,
    "psda-infer-greenhouse-sprout-overlap": _b9pd_greenhouse_overlap,
    "psda-infer-dog-park-majority": _b9pd_dog_park,
    "psda-infer-garden-households-interval": _b9pd_garden_interval,
    "psda-infer-bus-delay-plausible-mean": _b9pd_bus_delay,
    "psda-infer-books-read-larger-sample": _b9pd_books_larger_sample,
    "psda-claims-online-poll-self-selected": _b9pd_online_poll,
    "psda-claims-plant-food-random-assignment": _b9pd_plant_food_assignment,
    "psda-claims-walking-blood-pressure": _b9pd_walking,
    "psda-claims-green-tea-design-change": _b9pd_green_tea_change,
    "psda-claims-muscle-cream-placebo": _b9pd_placebo,
    "psda-claims-weekday-morning-shoppers": _b9pd_weekday_shoppers,
    "psda-claims-fitness-center-exercise-bias": _b9pd_fitness_bias,
    "psda-claims-screen-time-website": _b9pd_screen_time,
    "psda-claims-hens-supplement-extend": _b9pd_hens,
    "psda-claims-practice-app-self-chosen": _b9pd_practice_app,
    "psda-prob-red-cards-letter": _b9pd_red_cards,
    "psda-prob-seed-varieties-not-sprouted": _b9pd_seed_varieties,
    "psda-prob-museum-audio-no-tour": _b9pd_museum,
    "psda-prob-shelter-young-cats": _b9pd_shelter,
    # batch batch9-circ
    "geo-circ-equation-from-center-radius": geo_circ_equation_from_center_radius,
    "geo-circ-sector-radians-area-easy": geo_circ_sector_radians_area_easy,
    "geo-circ-skating-rink-arc": geo_circ_skating_rink_arc,
    "geo-circ-point-on-standard-form": geo_circ_point_on_standard_form,
    "geo-circ-unit-circle-point-coordinates": geo_circ_unit_circle_point_coordinates,
    "geo-circ-sprinkler-sector-radius": geo_circ_sprinkler_sector_radius,
    "geo-circ-line-through-center-greatest-y": geo_circ_line_through_center_greatest_y,
    "geo-circ-translate-left-up": geo_circ_translate_left_up,
    "geo-circ-chord-distance-radius": geo_circ_chord_distance_radius,
    "geo-circ-clock-minute-hand-arc": geo_circ_clock_minute_hand_arc,
    "geo-circ-diameter-endpoints-equation": geo_circ_diameter_endpoints_equation,
    "geo-circ-point-inside-expanded": geo_circ_point_inside_expanded,
    "geo-circ-tangent-x-axis-constant": geo_circ_tangent_x_axis_constant,
    "geo-circ-leading-coefficient-radius": geo_circ_leading_coefficient_radius,
    "geo-circ-two-circles-common-chord": geo_circ_two_circles_common_chord,
    "geo-circ-sector-arc-area-radius": geo_circ_sector_arc_area_radius,
    "geo-circ-fountain-tangent-path": geo_circ_fountain_tangent_path,
    "geo-circ-wiper-blade-region": geo_circ_wiper_blade_region,
    "geo-circ-radian-central-inscribed": geo_circ_radian_central_inscribed,
    "geo-circ-center-h-through-point": geo_circ_center_h_through_point,
    # batch batch9-ee2
    "adv-expand-monomial-two-binomials": adv_expand_monomial_two_binomials,
    "adv-exponential-shift-coefficient": adv_exponential_shift_coefficient,
    "adv-negative-exponents-product-two-variable": adv_negative_exponents_product_two_variable,
    "adv-poly-sum-difference-coefficient-total": adv_poly_sum_difference_coefficient_total,
    "adv-floor-tile-area-square-binomial": adv_floor_tile_area_square_binomial,
    "adv-long-division-linear-negative-remainder": adv_long_division_linear_negative_remainder,
    "adv-rationalize-radical-difference-denominator": adv_rationalize_radical_difference_denominator,
    "adv-fractional-negative-exponent-power-two-variable": adv_fractional_negative_exponent_power_two_variable,
    "adv-exponential-difference-rewrite-coefficient": adv_exponential_difference_rewrite_coefficient,
    "adv-perfect-square-identity-ab": adv_perfect_square_identity_ab,
    "adv-difference-of-binomial-squares-factor": adv_difference_of_binomial_squares_factor,
    "adv-complex-fraction-sum-numerator": adv_complex_fraction_sum_numerator,
    "adv-storage-bin-volume-three-binomials": adv_storage_bin_volume_three_binomials,
    "adv-parallel-resistance-complex-fraction": adv_parallel_resistance_complex_fraction,
    "adv-moss-area-exponential-rewrite-a": adv_moss_area_exponential_rewrite_a,
    "adv-quartic-hidden-difference-squares": adv_quartic_hidden_difference_squares,
    "adv-three-factor-coefficient-sum": adv_three_factor_coefficient_sum,
    "adv-long-division-missing-term-cubic": adv_long_division_missing_term_cubic,
    "adv-negative-exponent-complex-fraction-two-variable": adv_negative_exponent_complex_fraction_two_variable,
    "adv-exponential-product-base-half": adv_exponential_product_base_half,
    "adv-rationalize-conjugate-a-plus-b": adv_rationalize_conjugate_a_plus_b,
    "adv-quartic-product-identity-ab": adv_quartic_product_identity_ab,
    "adv-radical-exponents-two-variable-a-minus-b": adv_radical_exponents_two_variable_a_minus_b,
    # batch batch10-lf2
    "alg-lf-uneven-table-slope": alg_lf_uneven_table_slope,
    "alg-lf-increase-between-inputs": alg_lf_increase_between_inputs,
    "alg-lf-table-scaled-shifted-value": alg_lf_table_scaled_shifted_value,
    "alg-lf-hiking-club-year-input": alg_lf_hiking_club_year_input,
    "alg-lf-fraction-rule-input-spr": alg_lf_fraction_rule_input_spr,
    "alg-lf-decimal-rate-zero-input": alg_lf_decimal_rate_zero_input,
    "alg-lf-table-missing-output-k": alg_lf_table_missing_output_k,
    "alg-lf-scaled-shifted-rule": alg_lf_scaled_shifted_rule,
    "alg-lf-k-coefficient-and-term": alg_lf_k_coefficient_and_term,
    "alg-lf-oven-percent-depreciation": alg_lf_oven_percent_depreciation,
    "alg-lf-table-standard-form-match": alg_lf_table_standard_form_match,
    "alg-lf-charging-stations-since-2010": alg_lf_charging_stations_since_2010,
    "alg-lf-compare-increase-interval": alg_lf_compare_increase_interval,
    "alg-lf-tote-bags-budget-spr": alg_lf_tote_bags_budget_spr,
    "alg-lf-calf-weight-shifted-input": alg_lf_calf_weight_shifted_input,
    "alg-lf-transit-card-x-intercept": alg_lf_transit_card_x_intercept,
    "alg-lf-decrease-over-interval-spr": alg_lf_decrease_over_interval_spr,
    "alg-lf-constants-in-outputs-spr": alg_lf_constants_in_outputs_spr,
    "alg-lf-two-machines-equal-value": alg_lf_two_machines_equal_value,
    "alg-lf-seabird-shifted-base-year": alg_lf_seabird_shifted_base_year,
    "alg-lf-shift-scale-from-two-values": alg_lf_shift_scale_from_two_values,
    "alg-lf-two-intervals-intersection-spr": alg_lf_two_intervals_intersection_spr,
    "alg-lf-shirts-profit-least-number": alg_lf_shirts_profit_least_number,
    "alg-lf-point-slope-equivalent": alg_lf_point_slope_equivalent,
    "alg-lf-swapped-points-constant-c": alg_lf_swapped_points_constant_c,
    "alg-lf-output-difference-input-gap": alg_lf_output_difference_input_gap,
    "alg-lf-table-two-unknown-outputs": alg_lf_table_two_unknown_outputs,
    "alg-lf-composed-integer-count": alg_lf_composed_integer_count,
    # batch batch10-ne2
    "adv-ne2-quartic-isolate-positive": adv_ne2_quartic_isolate_positive,
    "adv-ne2-factored-greatest-solution": adv_ne2_factored_greatest_solution,
    "adv-ne2-square-equals-twelve-radical": adv_ne2_square_equals_twelve_radical,
    "adv-ne2-rod-length-tolerance": adv_ne2_rod_length_tolerance,
    "adv-ne2-rational-one-fraction-easy": adv_ne2_rational_one_fraction_easy,
    "adv-ne2-line-parabola-which-point": adv_ne2_line_parabola_which_point,
    "adv-ne2-irrational-negative-solution": adv_ne2_irrational_negative_solution,
    "adv-ne2-complete-square-lesser": adv_ne2_complete_square_lesser,
    "adv-ne2-quartic-in-form-greatest": adv_ne2_quartic_in_form_greatest,
    "adv-ne2-rational-two-fractions-positive": adv_ne2_rational_two_fractions_positive,
    "adv-ne2-two-radicals-quadratic-radicand": adv_ne2_two_radicals_quadratic_radicand,
    "adv-ne2-difference-of-squares-system-y": adv_ne2_difference_of_squares_system_y,
    "adv-ne2-exponential-line-count": adv_ne2_exponential_line_count,
    "adv-ne2-hyperbola-line-other-point": adv_ne2_hyperbola_line_other_point,
    "adv-ne2-cabin-rental-group-size": adv_ne2_cabin_rental_group_size,
    "adv-ne2-illuminance-solve-distance": adv_ne2_illuminance_solve_distance,
    "adv-ne2-catapult-balloon-height": adv_ne2_catapult_balloon_height,
    "adv-ne2-library-collections-later-time": adv_ne2_library_collections_later_time,
    "adv-ne2-cube-root-quadratic-form": adv_ne2_cube_root_quadratic_form,
    "adv-ne2-base-five-solution-count": adv_ne2_base_five_solution_count,
    "adv-ne2-base-three-product-solutions": adv_ne2_base_three_product_solutions,
    "adv-ne2-rational-restriction-extraneous": adv_ne2_rational_restriction_extraneous,
    "adv-ne2-two-radicals-sum-solutions": adv_ne2_two_radicals_sum_solutions,
    "adv-ne2-two-radicals-no-solution": adv_ne2_two_radicals_no_solution,
    "adv-ne2-parabola-absolute-three-points": adv_ne2_parabola_absolute_three_points,
    "adv-ne2-absolute-quadratic-three-solutions-k": adv_ne2_absolute_quadratic_three_solutions_k,
    "adv-ne2-k-at-both-ends-one-solution": adv_ne2_k_at_both_ends_one_solution,
    "adv-ne2-rational-tangent-positive-k": adv_ne2_rational_tangent_positive_k,
    "adv-ne2-tangent-at-given-point-bc": adv_ne2_tangent_at_given_point_bc,
    "adv-ne2-hiker-round-trip-speed": adv_ne2_hiker_round_trip_speed,
    "adv-ne2-tabletop-diagonal-perimeter": adv_ne2_tabletop_diagonal_perimeter,
    # batch batch10-sys2
    "alg-sys-combine-for-five-x-plus-seven-y": alg_sys_combine_for_five_x_plus_seven_y,
    "alg-sys-scale-first-equation-seven-x-nine-y-spr": alg_sys_scale_first_equation_seven_x_nine_y_spr,
    "alg-sys-three-constants-solution-given-c-spr": alg_sys_three_constants_solution_given_c_spr,
    "alg-sys-three-constants-p-plus-r": alg_sys_three_constants_p_plus_r,
    "alg-sys-solution-x-twice-y-coefficient-k": alg_sys_solution_x_twice_y_coefficient_k,
    "alg-sys-fractions-both-sides-x-spr": alg_sys_fractions_both_sides_x_spr,
    "alg-sys-parameter-ratio-x-over-y": alg_sys_parameter_ratio_x_over_y,
    "alg-sys-ratio-x-over-y-elimination": alg_sys_ratio_x_over_y_elimination,
    "alg-sys-lines-described-standard-form": alg_sys_lines_described_standard_form,
    "alg-sys-which-ordered-pair-satisfies-both": alg_sys_which_ordered_pair_satisfies_both,
    "alg-sys-horizontal-line-intersection-x": alg_sys_horizontal_line_intersection_x,
    "alg-sys-solution-given-find-coefficient-a": alg_sys_solution_given_find_coefficient_a,
    "alg-sys-sum-in-words-and-equation-x": alg_sys_sum_in_words_and_equation_x,
    "alg-sys-infinite-solutions-y-at-given-x": alg_sys_infinite_solutions_y_at_given_x,
    "alg-sys-which-system-has-given-solution": alg_sys_which_system_has_given_solution,
    "alg-sys-x-described-in-words-sum": alg_sys_x_described_in_words_sum,
    "alg-sys-swapped-slope-intercept-y-spr": alg_sys_swapped_slope_intercept_y_spr,
    "alg-sys-infinite-solutions-product-mc": alg_sys_infinite_solutions_product_mc,
    "alg-sys-fractions-both-sides-x-minus-y": alg_sys_fractions_both_sides_x_minus_y,
    "alg-sys-florist-bouquets-roses-spr": alg_sys_florist_bouquets_roses_spr,
    "alg-sys-drones-altitude-interpret-y": alg_sys_drones_altitude_interpret_y,
    "alg-sys-ice-sculptures-equal-height": alg_sys_ice_sculptures_equal_height,
    "alg-sys-bowling-equal-cost-fee-spr": alg_sys_bowling_equal_cost_fee_spr,
    "alg-sys-hiker-flat-uphill-distance": alg_sys_hiker_flat_uphill_distance,
    "alg-sys-bike-shop-repairs-model": alg_sys_bike_shop_repairs_model,
    "alg-sys-bridges-ages-future": alg_sys_bridges_ages_future,
    "alg-sys-courier-van-unloaded-type-b-spr": alg_sys_courier_van_unloaded_type_b_spr,
    "alg-sys-puppies-weight-weeks-units": alg_sys_puppies_weight_weeks_units,
    # batch batch11-le1v2
    "alg-le-x-fourths-sixths-sum": alg_le_x_fourths_sixths_sum,
    "alg-le-proportion-two-numerators": alg_le_proportion_two_numerators,
    "alg-le-proportion-fraction-key-spr": alg_le_proportion_fraction_key_spr,
    "alg-le-proportion-k-from-solution": alg_le_proportion_k_from_solution,
    "alg-le-shifted-constant-new-solution": alg_le_shifted_constant_new_solution,
    "alg-le-nested-bracket-solve": alg_le_nested_bracket_solve,
    "alg-le-nested-bracket-fraction-spr": alg_le_nested_bracket_fraction_spr,
    "alg-le-value-x-plus-5": alg_le_value_x_plus_5,
    "alg-le-value-6-minus-x": alg_le_value_6_minus_x,
    "alg-le-consecutive-twice-greatest": alg_le_consecutive_twice_greatest,
    "alg-le-oak-maple-ages": alg_le_oak_maple_ages,
    "alg-le-ladder-discount-delivery": alg_le_ladder_discount_delivery,
    "alg-le-ticket-discount-service-fee-spr": alg_le_ticket_discount_service_fee_spr,
    "alg-le-identity-two-constants-sum": alg_le_identity_two_constants_sum,
    "alg-le-flower-shop-bouquets-equation": alg_le_flower_shop_bouquets_equation,
    "alg-le-greenhouse-term-meaning": alg_le_greenhouse_term_meaning,
    "alg-le-club-mugs-profit-spr": alg_le_club_mugs_profit_spr,
    "alg-le-both-sides-easy-solve": alg_le_both_sides_easy_solve,
    "alg-le-x-over-20-structure": alg_le_x_over_20_structure,
    "alg-le-identity-coefficient-match-spr": alg_le_identity_coefficient_match_spr,
    "alg-le-five-even-sum-greatest": alg_le_five_even_sum_greatest,
    # batch batch11-ineq2
    "alg-ineq-dashed-boundary-shaded-below": alg_ineq_dashed_boundary_shaded_below,
    "alg-ineq-describe-graph-solid-above": alg_ineq_describe_graph_solid_above,
    "alg-ineq-pin-length-tolerance": alg_ineq_pin_length_tolerance,
    "alg-ineq-dashed-boundary-y-axis": alg_ineq_dashed_boundary_y_axis,
    "alg-ineq-data-plan-music-hours": alg_ineq_data_plan_music_hours,
    "alg-ineq-day-camp-staff-system": alg_ineq_day_camp_staff_system,
    "alg-ineq-recycling-credits-point-outside": alg_ineq_recycling_credits_point_outside,
    "alg-ineq-hike-distance-time-system": alg_ineq_hike_distance_time_system,
    "alg-ineq-tank-heater-hours": alg_ineq_tank_heater_hours,
    "alg-ineq-shifted-compound-same-set": alg_ineq_shifted_compound_same_set,
    "alg-ineq-compound-two-constants-sum": alg_ineq_compound_two_constants_sum,
    "alg-ineq-region-greatest-y": alg_ineq_region_greatest_y,
    "alg-ineq-intercepts-solid-above": alg_ineq_intercepts_solid_above,
    "alg-ineq-table-boundary-least-k": alg_ineq_table_boundary_least_k,
    "alg-ineq-function-values-compare": alg_ineq_function_values_compare,
    "alg-ineq-bakery-greatest-batches": alg_ineq_bakery_greatest_batches,
    "alg-ineq-stable-feed-least-cost": alg_ineq_stable_feed_least_cost,
    "alg-ineq-signs-of-constants": alg_ineq_signs_of_constants,
    "alg-ineq-four-constraints-greatest-sum": alg_ineq_four_constraints_greatest_sum,
    "alg-ineq-boundary-intercepts-constants": alg_ineq_boundary_intercepts_constants,
    "alg-ineq-point-not-in-system-c": alg_ineq_point_not_in_system_c,
    "alg-ineq-two-inequalities-given-interval": alg_ineq_two_inequalities_given_interval,
    "alg-ineq-region-greatest-2x-plus-y": alg_ineq_region_greatest_2x_plus_y,
    "alg-ineq-region-lines-through-points": alg_ineq_region_lines_through_points,
    # batch batch11-nf2
    "adv-nf-remainder-cubic-divided-by-binomial": adv_nf_remainder_cubic_divided_by_binomial,
    "adv-nf-radical-evaluate-scaled-root": adv_nf_radical_evaluate_scaled_root,
    "adv-nf-rational-undefined-input": adv_nf_rational_undefined_input,
    "adv-nf-parabola-shift-left-down-equation": adv_nf_parabola_shift_left_down_equation,
    "adv-nf-pool-chemical-half-life-amount": adv_nf_pool_chemical_half_life_amount,
    "adv-nf-repeated-factor-touch-point": adv_nf_repeated_factor_touch_point,
    "adv-nf-cubic-negative-between-zeros": adv_nf_cubic_negative_between_zeros,
    "adv-nf-equal-remainders-coefficient": adv_nf_equal_remainders_coefficient,
    "adv-nf-rational-input-for-output-five": adv_nf_rational_input_for_output_five,
    "adv-nf-poster-average-cost": adv_nf_poster_average_cost,
    "adv-nf-radical-graph-endpoint": adv_nf_radical_graph_endpoint,
    "adv-nf-laptop-half-life-period": adv_nf_laptop_half_life_period,
    "adv-nf-caffeine-half-life-interpret": adv_nf_caffeine_half_life_interpret,
    "adv-nf-sqrt-reflect-translate-equation": adv_nf_sqrt_reflect_translate_equation,
    "adv-nf-shift-right-new-x-intercept": adv_nf_shift_right_new_x_intercept,
    "adv-nf-rational-constant-from-value": adv_nf_rational_constant_from_value,
    "adv-nf-solar-panels-two-towns": adv_nf_solar_panels_two_towns,
    "adv-nf-cubic-negative-leading-sign-interval": adv_nf_cubic_negative_leading_sign_interval,
    "adv-nf-cubic-touch-cross-evaluate": adv_nf_cubic_touch_cross_evaluate,
    "adv-nf-remainder-factor-of-shifted": adv_nf_remainder_factor_of_shifted,
    "adv-nf-pendulum-longer-swing": adv_nf_pendulum_longer_swing,
    "adv-nf-two-samples-equal-mass": adv_nf_two_samples_equal_mass,
    "adv-nf-shift-left-down-expanded": adv_nf_shift_left_down_expanded,
    "adv-nf-model-rocket-three-heights": adv_nf_model_rocket_three_heights,
    "adv-nf-rational-point-undefined-input": adv_nf_rational_point_undefined_input,
    "adv-nf-half-life-ratio-constant": adv_nf_half_life_ratio_constant,
    "adv-nf-factored-cubic-remainder-constant": adv_nf_factored_cubic_remainder_constant,
    # batch batch12-le2v2
    "alg-vertical-line-shared-x-equation": alg_vertical_line_shared_x_equation,
    "alg-perpendicular-to-vertical-y-crossing-spr": alg_perpendicular_to_vertical_y_crossing_spr,
    "alg-collinear-point-k-and-k-plus-13": alg_collinear_point_k_and_k_plus_13,
    "alg-table-missing-y-entry-spr": alg_table_missing_y_entry_spr,
    "alg-origin-line-missing-x-coordinate": alg_origin_line_missing_x_coordinate,
    "alg-origin-constant-slope": alg_origin_constant_slope,
    "alg-x-intercept-parallel-line-equation": alg_x_intercept_parallel_line_equation,
    "alg-intercepts-ten-units-apart-k": alg_intercepts_ten_units_apart_k,
    "alg-verbal-rate-x-axis-crossing": alg_verbal_rate_x_axis_crossing,
    "alg-collinear-equal-spacing-k-spr": alg_collinear_equal_spacing_k_spr,
    "alg-table-entries-p-and-2p": alg_table_entries_p_and_2p,
    "alg-horizontal-vertical-intersection-point": alg_horizontal_vertical_intersection_point,
    "alg-undefined-slope-points-with-k": alg_undefined_slope_points_with_k,
    "alg-horizontal-line-constant-y-crossing": alg_horizontal_line_constant_y_crossing,
    "alg-patio-tiles-table-missing-count": alg_patio_tiles_table_missing_count,
    "alg-seed-packet-boxes-combination-count-spr": alg_seed_packet_boxes_combination_count_spr,
    "alg-catering-trays-verbal-rate-equation": alg_catering_trays_verbal_rate_equation,
    "alg-art-club-canvases-greatest-count": alg_art_club_canvases_greatest_count,
    "alg-dye-scarves-blankets-substitution": alg_dye_scarves_blankets_substitution,
    "alg-concrete-sand-gravel-total-spr": alg_concrete_sand_gravel_total_spr,
    "alg-tram-minutes-distance-equation": alg_tram_minutes_distance_equation,
    # batch batch12-ee3
    "adv-ee3-gcf-identify-two-variable": adv_ee3_gcf_identify_two_variable,
    "adv-ee3-divide-trinomial-by-monomial": adv_ee3_divide_trinomial_by_monomial,
    "adv-ee3-difference-squares-fraction-coefficient": adv_ee3_difference_squares_fraction_coefficient,
    "adv-ee3-trinomial-two-variable-factor": adv_ee3_trinomial_two_variable_factor,
    "adv-ee3-store-shelves-cans-total": adv_ee3_store_shelves_cans_total,
    "adv-ee3-gcf-variable-exponent-n": adv_ee3_gcf_variable_exponent_n,
    "adv-ee3-absolute-value-two-terms-negative": adv_ee3_absolute_value_two_terms_negative,
    "adv-ee3-factored-form-zero-p": adv_ee3_factored_form_zero_p,
    "adv-ee3-not-equivalent-product-forms": adv_ee3_not_equivalent_product_forms,
    "adv-ee3-substitution-u-shift": adv_ee3_substitution_u_shift,
    "adv-ee3-cube-of-sum-k": adv_ee3_cube_of_sum_k,
    "adv-ee3-negative-rational-exponent-radical": adv_ee3_negative_rational_exponent_radical,
    "adv-ee3-theater-ticket-revenue-b": adv_ee3_theater_ticket_revenue_b,
    "adv-ee3-solar-panels-area-difference": adv_ee3_solar_panels_area_difference,
    "adv-ee3-absolute-value-quotient-b": adv_ee3_absolute_value_quotient_b,
    "adv-ee3-substitution-quartic-u": adv_ee3_substitution_quartic_u,
    "adv-ee3-four-factor-x2-coefficient": adv_ee3_four_factor_x2_coefficient,
    "adv-ee3-quartic-over-quadratic-polynomial": adv_ee3_quartic_over_quadratic_polynomial,
    "adv-ee3-ball-height-shifted-time-k": adv_ee3_ball_height_shifted_time_k,
    "adv-ee3-not-equivalent-difference-squares": adv_ee3_not_equivalent_difference_squares,
    "adv-ee3-gcf-then-trinomial-a-plus-b": adv_ee3_gcf_then_trinomial_a_plus_b,
    "adv-ee3-equal-coefficients-k": adv_ee3_equal_coefficients_k,
    "adv-ee3-exponential-sum-squared": adv_ee3_exponential_sum_squared,
    # batch batch12-ne3
    "adv-ne3-square-49-negative-root": adv_ne3_square_49_negative_root,
    "adv-ne3-five-times-power-two": adv_ne3_five_times_power_two,
    "adv-ne3-sqrt-plus-five-easy": adv_ne3_sqrt_plus_five_easy,
    "adv-ne3-heating-coil-voltage": adv_ne3_heating_coil_voltage,
    "adv-ne3-product-xy-line-easy": adv_ne3_product_xy_line_easy,
    "adv-ne3-base-four-sixty-four": adv_ne3_base_four_sixty_four,
    "adv-ne3-factored-repeated-count": adv_ne3_factored_repeated_count,
    "adv-ne3-meeting-handshakes": adv_ne3_meeting_handshakes,
    "adv-ne3-auditorium-rows-seats": adv_ne3_auditorium_rows_seats,
    "adv-ne3-podcast-base-four-weeks": adv_ne3_podcast_base_four_weeks,
    "adv-ne3-given-root-other-fraction": adv_ne3_given_root_other_fraction,
    "adv-ne3-line-parabola-second-point-y": adv_ne3_line_parabola_second_point_y,
    "adv-ne3-circles-external-tangent-count": adv_ne3_circles_external_tangent_count,
    "adv-ne3-f-equals-f-double-quadratic": adv_ne3_f_equals_f_double_quadratic,
    "adv-ne3-one-ninth-base-three": adv_ne3_one_ninth_base_three,
    "adv-ne3-product-sum-squares": adv_ne3_product_sum_squares,
    "adv-ne3-quadratic-formula-expression": adv_ne3_quadratic_formula_expression,
    "adv-ne3-absolute-quadratic-four-count": adv_ne3_absolute_quadratic_four_count,
    "adv-ne3-train-braking-domain": adv_ne3_train_braking_domain,
    "adv-ne3-circle-parabola-three-count": adv_ne3_circle_parabola_three_count,
    "adv-ne3-circles-other-point-b": adv_ne3_circles_other_point_b,
    "adv-ne3-sixteen-four-quadratic-exponent": adv_ne3_sixteen_four_quadratic_exponent,
    "adv-ne3-roots-differ-by-one-k": adv_ne3_roots_differ_by_one_k,
    "adv-ne3-v-graph-circle-count": adv_ne3_v_graph_circle_count,
    "adv-ne3-product-ellipse-x-plus-2y": adv_ne3_product_ellipse_x_plus_2y,
    "adv-ne3-robots-north-east": adv_ne3_robots_north_east,
    "adv-ne3-dance-floor-enlarged-area": adv_ne3_dance_floor_enlarged_area,
    "adv-ne3-f-equals-f-double-rational": adv_ne3_f_equals_f_double_rational,
    "adv-ne3-quartic-substitution-product": adv_ne3_quartic_substitution_product,
    "adv-ne3-root-difference-squared": adv_ne3_root_difference_squared,
    "adv-ne3-exponential-system-sum": adv_ne3_exponential_system_sum,
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
