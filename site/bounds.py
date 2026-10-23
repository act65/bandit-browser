"""Render canonical bound expressions (SymPy strings, schema.md) as LaTeX.

The extraction stores two forms of every bound:
  * ``expression``        canonical, SymPy-parseable, over the canonical variables;
  * ``expression_latex``  the paper's own LaTeX (may use paper-private macros).

The site shows the canonical form (D13) and keeps the paper's LaTeX as provenance.
``bound_tex`` returns ``(tex, ok)``; ``ok`` is False when the canonical string could
not be parsed and the caller should fall back to the paper's LaTeX.
"""

from __future__ import annotations

import keyword
import re
from pathlib import Path

try:
    import sympy
    from sympy.core.function import AppliedUndef
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.printing.latex import LatexPrinter
except ImportError:  # the site still builds, with the paper's LaTeX only
    sympy = None

GREEK = {
    "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa",
    "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi",
    "omega", "vartheta", "varphi", "varepsilon", "varrho",
    "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
}
GREEK_ALIASES = {"eps": "varepsilon", "epsilon": "varepsilon", "lam": "lambda"}

# Canonical variables (schema.md) whose generic rendering would be wrong or ugly.
# ontology/variables.yaml, when present, takes precedence over this map.
SYMBOL_TEX = {
    "Delta_min": r"\Delta_{\min}",
    "Delta_max": r"\Delta_{\max}",
    "mu_star": r"\mu^*",
    "lam": r"\lambda",
    "L_feat": r"L_{\mathrm{feat}}",
    "L_lip": r"L_{\mathrm{Lip}}",
    "KL_i": r"\mathrm{KL}_i",
    "kl_i": r"\mathrm{kl}_i",
    "diam_K": r"\mathrm{diam}(\mathcal{K})",
    "gamma_T": r"\gamma_T",
    "S_T": "S_T",
    "V_T": "V_T",
    "E": "e",
}

FUNC_TEX = {"kl": r"\mathrm{kl}", "KL": r"\mathrm{KL}", "Phi": r"\Phi", "psi_star": r"\psi^*"}

NOTATION_WRAP = {
    "O": r"O",
    "O_tilde": r"\tilde{O}",
    "Theta": r"\Theta",
    "Theta_tilde": r"\tilde{\Theta}",
    "Omega": r"\Omega",
    "Omega_tilde": r"\tilde{\Omega}",
}
NOTATION_LABEL = {
    "exact": "exact", "O": "O", "O_tilde": "Õ", "Theta": "Θ", "Theta_tilde": "Θ̃",
    "Omega": "Ω", "Omega_tilde": "Ω̃", "liminf": "lim inf", "limsup": "lim sup",
}

# The symbol on the left of an "exact" or asymptotic bound, by result quantity.
QUANTITY_TEX = {
    "pseudo_regret": r"\bar{R}_T",
    "expected_regret": r"\mathbb{E}[R_T]",
    "high_probability_regret": r"R_T",
    "bayesian_regret": r"\mathrm{BR}_T",
    "minimax_bayesian_regret": r"\mathrm{BR}_T",
    "simple_regret": r"r_T",
    "sample_complexity": r"\mathbb{E}[\tau]",
    "error_probability": r"\mathbb{P}(\mathrm{error})",
    "dynamic_regret": r"R^{\mathrm{dyn}}_T",
    "switching_regret": r"R^{\mathrm{sw}}_T",
}

_variables: dict[str, str] = {}


def load_variables(path: Path) -> None:
    """Use ontology/variables.yaml (name -> {latex, ...}) if it exists."""
    import yaml

    _variables.clear()
    if not path.is_file():
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return
    for name, v in (data.get("variables") or {}).items():
        if isinstance(v, dict) and v.get("latex") and v.get("kind") != "function":
            _variables[str(name)] = str(v["latex"])


def _piece(s: str) -> str:
    if s in GREEK_ALIASES:
        return "\\" + GREEK_ALIASES[s]
    if s in GREEK:
        return "\\" + s
    if s in ("min", "max"):
        return "\\" + s
    if len(s) == 1 or s.isdigit():
        return s
    return r"\mathrm{" + s + "}"


def symbol_tex(name: str) -> str:
    """Canonical symbol name -> LaTeX: Delta_i -> \\Delta_i, w_star_i -> w^*_{i}."""
    if name in _variables:
        return _variables[name]
    if name in SYMBOL_TEX:
        return SYMBOL_TEX[name]
    base, *parts = name.rstrip("_").split("_")
    out = _piece(base) if base else name
    star = "star" in parts
    subs = [_piece(p) for p in parts if p and p != "star"]
    if star:
        out += "^*"
    if subs:
        out += "_{" + ",".join(subs) + "}"
    return out


if sympy is not None:

    class _Printer(LatexPrinter):
        def _print_Function(self, expr, exp=None):
            if isinstance(expr, AppliedUndef):
                name = expr.func.__name__
                args = [self._print(a) for a in expr.args]
                if name.startswith(("sum_subopt", "sum_arms")):
                    sub = r"i:\Delta_i>0" if name.startswith("sum_subopt") else "i"
                    body = args[0]
                    if isinstance(expr.args[0], sympy.Add):
                        body = r"\left(" + body + r"\right)"
                    tex = r"\sum_{" + sub + "} " + body
                    if name.endswith("_p") or exp:  # a factor of a product: bracket the whole sum
                        tex = r"\Bigl(" + tex + r"\Bigr)"
                    return tex + "^{" + exp + "}" if exp else tex
                if name == "BigO":
                    tex = r"O\left(" + args[0] + r"\right)"
                else:
                    fn = FUNC_TEX.get(name) or symbol_tex(name)
                    tex = fn + r"\left(" + ", ".join(args) + r"\right)"
                return tex + "^{" + exp + "}" if exp else tex
            return super()._print_Function(expr, exp)

        def _print_log(self, expr, exp=None):
            arg = expr.args[0]
            a = self._print(arg)
            head = r"\log" + ("^{" + exp + "}" if exp else "")
            if arg.is_Symbol or arg.is_Integer:
                return head + " " + a
            return head + r"\left(" + a + r"\right)"

    def _rebuild(e, args):
        try:
            return e.func(*args, evaluate=False)
        except TypeError:
            return e.func(*args)

    def _tidy(e, parent=None):
        """Drop the 1 in 1*x/y left by evaluate=False; mark sums used as factors."""
        if not e.args or e.is_Atom:
            return e
        args = [_tidy(a, e) for a in e.args]
        if e.is_Mul:
            args = [a for a in args if a != 1] or [sympy.S.One]
            if len(args) == 1:
                return args[0]
            # log factors last, so "\log T" never swallows the next factor
            args.sort(key=lambda a: isinstance(a, sympy.log) or (a.is_Pow and isinstance(a.base, sympy.log)))
            return sympy.Mul(*args, evaluate=False)
        if isinstance(e, AppliedUndef):
            name = e.func.__name__
            if name in ("sum_subopt", "sum_arms") and parent is not None and parent.is_Mul:
                return sympy.Function(name + "_p")(*args)
            return e.func(*args)
        return _rebuild(e, args)

    _KNOWN = {
        "sqrt": sympy.sqrt, "log": sympy.log, "exp": sympy.exp, "Min": sympy.Min, "Max": sympy.Max,
        "LambertW": sympy.LambertW, "Abs": sympy.Abs, "pi": sympy.pi,
        "floor": sympy.floor, "ceiling": sympy.ceiling,
    }
    _PRINTER_SETTINGS = {"order": "none", "mul_symbol": None, "fold_frac_powers": True}


def parse(expr: str):
    """Parse a canonical expression; every unknown identifier becomes a Symbol/Function."""
    if sympy is None:
        raise ValueError("sympy not installed")
    s = str(expr).strip()
    if not s:
        raise ValueError("empty")
    names: dict = {}
    orig = s
    for m in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", orig):
        name = m.group(0)
        is_call = orig[m.end():].lstrip().startswith("(")
        safe = name + "_" if keyword.iskeyword(name) else name
        if safe != name:
            s = re.sub(rf"\b{name}\b", safe, s)
        if name in _KNOWN:
            names[safe] = _KNOWN[name]
        elif is_call:
            names[safe] = sympy.Function("BigO" if name == "O" else name)
        else:
            names[safe] = sympy.Symbol(name)
    return parse_expr(s, local_dict=names, evaluate=False)


def expr_tex(expr: str) -> str:
    return to_tex(parse(expr))


def to_tex(e) -> str:
    e = _tidy(e)
    names = {s: symbol_tex(s.name) for s in e.free_symbols}
    return _Printer({**_PRINTER_SETTINGS, "symbol_names": names}).doprint(e)


def _has(e, sym) -> bool:
    return sym in e.free_symbols


def canonical_expr(bound: dict) -> str | None:
    """The normalised expression (data/canonical) if present, else the extracted one."""
    return bound.get("expression_normalised") or bound.get("expression")


def bound_tex(bound: dict, side: str | None, quantity: str | None) -> tuple[str, bool]:
    """Canonical bound -> (LaTeX with notation, parsed_ok)."""
    expr = canonical_expr(bound)
    notation = (bound.get("notation") or "exact").strip()
    if not expr or sympy is None:
        return "", False
    try:
        tex = expr_tex(expr)
    except Exception:  # noqa: BLE001 - any parse/print failure means "fall back"
        return "", False
    lhs = QUANTITY_TEX.get(quantity or "", "R_T")
    rel = r"\ge" if (side or "").lower() == "lower" else r"\le"
    if notation in NOTATION_WRAP:
        return NOTATION_WRAP[notation] + r"\left(" + tex + r"\right)", True
    if notation in ("liminf", "limsup"):
        op = r"\liminf_{T\to\infty}" if notation == "liminf" else r"\limsup_{T\to\infty}"
        try:
            e = parse(expr)
            T, dl = sympy.Symbol("T"), sympy.Symbol("delta")
            if _has(e, dl) and not _has(e, T):  # asymptotic in the confidence: delta -> 0 (fixed-confidence BAI)
                dop = r"\liminf_{\delta\to 0}" if notation == "liminf" else r"\limsup_{\delta\to 0}"
                ratio = sympy.simplify(e / sympy.log(1 / dl))
                if not _has(ratio, dl):
                    return dop + r"\frac{" + lhs + r"}{\log(1/\delta)} " + rel + " " + to_tex(ratio), True
                return dop + r"\frac{" + lhs + "}{" + tex + "} " + rel + " 1", True
            norm = sympy.simplify(e / sympy.log(T)) if _has(e, T) else e
            if _has(norm, T):  # not of the form c * log T: state the ratio to the whole bound
                return op + r"\frac{" + lhs + "}{" + tex + "} " + rel + " 1", True
            ntex = to_tex(norm)
            return op + r"\frac{" + lhs + r"}{\log T} " + rel + " " + ntex, True
        except Exception:  # noqa: BLE001
            return op + r"\frac{" + lhs + "}{" + tex + "} " + rel + " 1", True
    return lhs + " " + rel + " " + tex, True
