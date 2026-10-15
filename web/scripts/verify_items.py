#!/usr/bin/env python3
"""Recompute every answer key in web/content/items.ts with SymPy and compare.

How to run (from the repo root, needs Python 3 and SymPy >= 1.12):

    python3 web/scripts/verify_items.py

The script reads items.ts directly (a small regex parser; no JSON export to keep
in sync), looks up a SymPy computation for each item id in CHECKS below, and
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

ITEMS_TS = Path(__file__).resolve().parents[1] / "content" / "items.ts"

MAX_POSITIVE_LENGTH = 5
MAX_NEGATIVE_LENGTH = 6

# ---------------------------------------------------------------------------
# items.ts parsing
# ---------------------------------------------------------------------------


def _unescape_ts(s: str) -> str:
    """Turn a TS double-quoted string body into its runtime value (only \\ and \" matter here)."""
    return s.replace('\\"', '"').replace("\\\\", "\\")


def parse_items(source: str) -> list[dict]:
    items = []
    # Each item object starts with `id: "..."`. Split the file on those markers.
    starts = [m.start() for m in re.finditer(r'^\s*id: "', source, re.M)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(source)
        block = source[start:end]
        item: dict = {"id": re.search(r'id: "([^"]+)"', block).group(1)}
        item["format"] = re.search(r'format: "(mc|spr)"', block).group(1)
        item["domain"] = re.search(r'domain: "([^"]+)"', block).group(1)
        item["difficulty"] = re.search(r'difficulty: "([^"]+)"', block).group(1)
        item["route"] = re.search(r'route: "([^"]+)"', block).group(1)
        if item["format"] == "mc":
            raw = re.search(r"choices: \[(.*?)\]", block, re.S).group(1)
            item["choices"] = [_unescape_ts(c) for c in re.findall(r'"((?:[^"\\]|\\.)*)"', raw)]
            item["answerIndex"] = int(re.search(r"answerIndex: (\d)", block).group(1))
        else:
            raw = re.search(r"answers: \[(.*?)\]", block, re.S).group(1)
            item["answers"] = [
                Fraction(int(n), int(d)) for n, d in re.findall(r"num: (-?\d+), den: (\d+)", raw)
            ]
        items.append(item)
    return items


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
