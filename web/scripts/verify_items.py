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
