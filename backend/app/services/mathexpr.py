"""A tiny, safe math expression reader for lesson steps where students type an equation.

It understands numbers, x, + - * / ^, parentheses, implicit multiplication (2x, 3(x + 1), (x + 1)(x - 2)),
sqrt(), abs(), pi, and a leading "y =" or "f(x) =". It never uses eval. website/src/lesson-kit.js has the same
reader in JavaScript so the preview grades the same way; tests/test_lesson_formats.py checks they agree.
"""
import math
import re

MAX_LEN = 60
SAMPLES = (-3.7, -2.2, -1.3, -0.4, 0.6, 1.9, 2.8, 4.1, 5.3)
_FUNCS = {"sqrt": math.sqrt, "abs": abs}


class ExprError(ValueError):
    pass


def clean(text):
    s = str(text or "").strip().lower()
    s = (s.replace("−", "-").replace("–", "-").replace("·", "*").replace("×", "*")
          .replace("²", "^2").replace("³", "^3").replace("√", "sqrt").replace("π", "pi"))
    s = re.sub(r"^\s*(y|f\s*\(\s*x\s*\))\s*=", "", s)
    return s.replace(" ", "")


def _tokens(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isdigit() or (c == "." and i + 1 < len(s) and s[i + 1].isdigit()):
            m = re.match(r"\d*\.?\d+|\d+\.?", s[i:])
            out.append(("num", float(m.group(0))))
            i += len(m.group(0))
        elif c.isalpha():
            m = re.match(r"sqrt|abs|pi|[a-z]", s[i:])
            out.append(("id", m.group(0)))
            i += len(m.group(0))
        elif c in "+-*/^()":
            out.append(("op", c))
            i += 1
        else:
            raise ExprError(f"Desmos would read that differently: {c}")
    # implicit multiplication: 2x, 2(x), x(x), )(, )x, x2 is not allowed
    res = []
    for t in out:
        if res:
            p = res[-1]
            left = p[0] == "num" or (p[0] == "id" and p[1] not in _FUNCS) or p == ("op", ")")
            right = t[0] == "id" or t == ("op", "(")
            if left and right:
                res.append(("op", "*"))
        res.append(t)
    return res


class _Parser:
    def __init__(self, toks, names):
        self.t, self.i, self.names = toks, 0, names

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, op=None):
        tok = self.peek()
        if op is not None and tok != ("op", op):
            raise ExprError("Check your brackets.")
        self.i += 1
        return tok

    def expr(self):
        node = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            rhs = self.term()
            node = ("+" if op == "+" else "-", node, rhs)
        return node

    def term(self):
        node = self.unary()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.take()[1]
            node = (op, node, self.unary())
        return node

    def unary(self):
        if self.peek() == ("op", "-"):
            self.take()
            return ("neg", self.unary())
        if self.peek() == ("op", "+"):
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == ("op", "^"):
            self.take()
            return ("^", base, self.unary())
        return base

    def atom(self):
        kind, val = self.peek()
        if kind == "num":
            self.take()
            return ("num", val)
        if kind == "id":
            self.take()
            if val in _FUNCS:
                self.take("(")
                arg = self.expr()
                self.take(")")
                return ("fn", val, arg)
            if val == "pi":
                return ("num", math.pi)
            if val not in self.names:
                raise ExprError(f"Use x for the variable, not {val}.")
            return ("var", val)
        if (kind, val) == ("op", "("):
            self.take()
            node = self.expr()
            self.take(")")
            return node
        raise ExprError("That isn't a complete expression yet.")


def parse(text, names=("x",)):
    s = clean(text)
    if not s or len(s) > MAX_LEN:
        raise ExprError("Type an expression.")
    p = _Parser(_tokens(s), set(names))
    node = p.expr()
    if p.i != len(p.t):
        raise ExprError("Check your brackets.")
    return node


def evaluate(node, env):
    k = node[0]
    if k == "num":
        return node[1]
    if k == "var":
        return env[node[1]]
    if k == "neg":
        return -evaluate(node[1], env)
    if k == "fn":
        return _FUNCS[node[1]](evaluate(node[2], env))
    a, b = evaluate(node[1], env), evaluate(node[2], env)
    if k == "+":
        return a + b
    if k == "-":
        return a - b
    if k == "*":
        return a * b
    if k == "/":
        return a / b
    r = a ** b
    if isinstance(r, complex):
        raise ValueError("complex")
    return r


def value(text, x, **env):
    """The value of an expression at x (and any parameters), or None where it's undefined."""
    try:
        node = parse(text, ("x",) + tuple(env))
        v = evaluate(node, dict(env, x=x))
        return v if math.isfinite(v) else None
    except (ExprError, ValueError, ZeroDivisionError, OverflowError, TypeError):
        return None


def _at(node, x):
    try:
        v = evaluate(node, {"x": x})
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return None
    return v if math.isfinite(v) else None


def same(a, b):
    """True when two expressions in x agree everywhere we sample them (and are defined at enough points)."""
    try:
        na, nb = parse(a), parse(b)
    except ExprError:
        return False
    agree = 0
    for x in SAMPLES:
        va, vb = _at(na, x), _at(nb, x)
        if va is None or vb is None:
            if (va is None) != (vb is None):
                return False
            continue
        if abs(va - vb) > 1e-6 * max(1.0, abs(va), abs(vb)):
            return False
        agree += 1
    return agree >= 3
