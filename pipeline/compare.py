"""Bound comparison (desiderata D2): asymptotic profiles, dominance, tightness.

Every bound (extracted and inferred) is reduced to a *profile*: for each scanned
variable v, the growth f ~ v^a (log v)^b. T is scanned alone (T -> infinity, others
fixed). K, d, 1/Delta and 1/epsilon are scanned in the regime "T large": along the path
T = v^4, and the bound's own T-profile is subtracted, so a separable bound such as
sqrt(K T) gets K-exponent 1/2. Comparisons use the raw path exponents, which is a valid
asymptotic comparison along that path even for non-separable bounds (Delta*T vs
log(T)/Delta). Profiles are estimated numerically (high-precision evaluation at very
large v), which is robust to the messy expressions papers produce.

Instance-dependent bounds are evaluated on a uniform-gap instance (sum over suboptimal
arms of g(Delta_i) -> (K-1) g(Delta); KL-type divergences ~ Delta^2; H_1 -> (K-1)/Delta^2).
Data-dependent quantities (L*_T, Q_T, Lambda_T) take their worst case ~T. Bounds that
contain paper-specific (non-canonical) symbols or opaque instance constants are not
profiled. An instance-dependent O-bound that does not mention Delta hides an
instance-dependent constant, so its Delta exponent is unknown and not compared.

Within a regime (quantity family x worst-case/instance-dependent):
  - the best upper bounds are the Pareto-minimal profiles, the best lower bounds the
    Pareto-maximal ones;
  - per variable: tight (same a and b), log gap (same a), poly gap, or conflict
    (best upper below best lower: an extraction error or a genuine contradiction);
  - setting status: no_upper | no_lower | tight | log_gap | poly_gap | conflict.
Constants are ignored: "tight" means tight up to constant factors in the scanned
variables.

Writes data/canonical/comparison.json and prints a summary.
Usage: uv run python pipeline/compare.py
"""

from __future__ import annotations

import collections
import json
import math
import re
import signal
import sys
from pathlib import Path

import mpmath
import sympy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve  # noqa: E402
import schema  # noqa: E402

OUT = schema.ROOT / "data" / "canonical"
mpmath.mp.dps = 80

# Scanned variables: name -> (base value, direction). "up": v -> infinity;
# "down": v -> 0, reported as the exponent of 1/v.
SCAN = {"T": (1e6, "up"), "K": (10, "up"), "d": (10, "up"), "Delta": (0.1, "down"), "epsilon": (0.1, "down")}
BASE = {"T": 10**6, "K": 10, "d": 10, "Delta": sympy.Rational(1, 10), "epsilon": sympy.Rational(1, 10),
        "delta": sympy.Rational(1, 100), "mu_star": sympy.Rational(1, 2), "N_exp": 10, "n_act": 10, "m": 3,
        "S": 1, "L_feat": 1, "sigma": 1, "sigma_std": 1, "lam": 1, "H": 10, "C": 1, "C_sb": 1}
# Instance quantities collapsed onto the scanned gap Delta (uniform-gap instance).
GAP_ALIASES = {"Delta_i": "Delta", "Delta_min": "Delta", "Delta_max": "Delta", "Delta_lin": "Delta"}
KL_LIKE = {"KL_i", "kl_i", "Kinf_i"}
WORST_CASE_T = {"L_star", "Q_T", "Lambda_T"}   # data-dependent, at most ~T
OPAQUE = {"C_lin"}                              # instance constants with unknown scaling
PATH_POWER = 4                                  # regime T = v^4 when scanning K, d, 1/Delta, 1/eps
INSTANCE_TIED_PARAMS = {"eps_alg"}              # free analysis parameters usually required to be < Delta

# Quantity families: bounds comparable for tightness. Upper bounds on expected regret
# (vs best in hindsight) imply upper bounds on pseudo-regret; lower bounds on
# pseudo-regret imply lower bounds on expected regret; we pool them as "regret".
FAMILY = {"pseudo_regret": "regret", "expected_regret": "regret", "regret_unspecified": "regret",
          "high_probability_regret": "hp_regret", "realized_regret": "hp_regret",
          "bayesian_regret": "bayesian_regret", "minimax_bayesian_regret": "bayesian_regret",
          "simple_regret": "simple_regret", "sample_complexity": "sample_complexity",
          "error_probability": "error_probability", "dynamic_regret": "dynamic_regret",
          "switching_regret": "switching_regret"}
MINIMAX_LOWER_CLASSES = {None, "all", "consistent", "uniformly_good"}
# A condition is a benign side condition if it only constrains the scanned problem sizes
# (e.g. "K >= 2", "T >= max{55, K}"); anything else restricts the instance class.
BENIGN_CONDITION = re.compile(r"^[\sTKdnN0-9δdelta()\[\]{}*+\-/^.,≥≤><=_maxinlogeqpwr]+$")


_CLASSES_FILE = schema.ROOT / "data" / "condition-classes.yaml"
CONDITION_CLASSES = ((__import__("yaml").safe_load(_CLASSES_FILE.read_text()) or {}).get("classes", {})
                     if _CLASSES_FILE.exists() else {})


def restricts_instances(conditions: list[str]) -> bool:
    """True if any condition restricts the instance class (classified by
    pipeline/classify_conditions.py; unclassified strings fall back to a regex)."""
    for c in conditions or []:
        cls = CONDITION_CLASSES.get(c)
        if cls in ("instance_restriction", "unclear") or CONSTRUCTED.search(c):
            return True
        if cls is None and not BENIGN_CONDITION.match(c.replace(" ", "")):
            return True
    return False


# "constructed class F ...": harmless on a lower bound (it describes the hard instance, and the
# classifier calls it a side condition), but an upper bound proved only there is restricted
CONSTRUCTED = re.compile(r"\bconstruct", re.I)
T_CAPPED = re.compile(r"^\s*(T|n)\s*(<|<=|≤)")  # a condition bounding the horizon from above
# consistency / uniform-goodness assumptions: the standard admissible class of asymptotic lower
# bounds (Lai & Robbins), handled through algorithm_class, not a restriction of the learner
CONSISTENCY = re.compile(r"o\(\s*[nT]\s*\^\s*\(?\s*a|for (every|all) a\s*>\s*0|uniformly (good|efficient|fast)|consisten"
                         r"|(delta|δ)[- ]?(correct|PAC)|\(\s*(epsilon|ε)\s*,\s*(delta|δ)\s*\)[- ]?PAC", re.I)
# ... and for fixed-confidence identification, delta-correct / (epsilon, delta)-PAC algorithms


def restricts_algorithms(conditions: list[str]) -> bool:
    """True if a condition restricts the learners (memory, batches, switching budget): a lower
    bound for such learners says nothing about the setting's minimax rate."""
    return any(CONDITION_CLASSES.get(c) == "algorithm_restriction" and not CONSISTENCY.search(c)
               for c in conditions or [])


def changes_model(conditions: list[str]) -> bool:
    """True if a condition puts the result in a modified protocol (quantum oracle, starved
    feedback, externalities): shown with the setting, but not evidence about its rate."""
    return any(CONDITION_CLASSES.get(c) == "model_change" for c in conditions or [])


def instance_expr(expr: str, notation: str | None):
    """Parse and specialise to the uniform-gap instance; returns a SymPy expression."""
    e = resolve.parse(expr)
    K, Delta = sympy.Symbol("K"), sympy.Symbol("Delta")
    rep = {sympy.Symbol(a): Delta for a in GAP_ALIASES}
    rep.update({sympy.Symbol(k): Delta**2 for k in KL_LIKE})
    rep.update({sympy.Symbol(k): sympy.Symbol("T") for k in WORST_CASE_T})
    rep[sympy.Symbol("H_1")] = (K - 1) / Delta**2
    rep[sympy.Symbol("T_star")] = (K - 1) / Delta**2  # BAI characteristic time: between H_1 and 2 H_1
    e = e.subs(rep)
    # sum over suboptimal arms -> (K-1) * summand; sum over all arms -> K * summand
    e = e.replace(lambda x: isinstance(x, sympy.Function) and x.func.__name__ == "sum_subopt",
                  lambda x: (K - 1) * x.args[0])
    e = e.replace(lambda x: isinstance(x, sympy.Function) and x.func.__name__ == "sum_arms",
                  lambda x: K * x.args[0])
    e = e.replace(lambda x: isinstance(x, sympy.Function) and x.func.__name__ == "kl",
                  lambda x: Delta**2)  # kl(mu_i, mu_star) on the uniform-gap instance
    if notation in ("liminf", "limsup") and not ({sympy.Symbol("T"), sympy.Symbol("delta")} & e.free_symbols):
        e = e * sympy.log(sympy.Symbol("T"))  # "lim R_T / log T <= c" written as c
    # an expression in delta (e.g. T_star * log(1/delta)) is asymptotic as delta -> 0, not in T
    return e


PROFILE_TIMEOUT_S = 10  # some paper expressions (e.g. factorials of T) never finish evaluating at T = 10^(10^10)


class _Timeout(BaseException):  # not caught by the broad `except Exception` handlers below
    pass


def _alarm(signum, frame):
    raise _Timeout


def _eval(f, point: dict):
    try:
        v = f(**point)
        v = mpmath.re(v) if isinstance(v, mpmath.mpc) and abs(mpmath.im(v)) < 1e-30 * abs(v) else v
        return v if isinstance(v, (mpmath.mpf, int, float)) and v > 0 and mpmath.isfinite(v) else None
    except Exception:  # evaluation of arbitrary paper expressions can fail many ways
        return None


def _fit(f, args: list, base: dict, path) -> tuple[float, float] | None:
    """Fit f ~ x^a (log x)^b along x -> infinity, with all arguments given by path(x)."""
    pts = []
    for k in (10**8, 10**9, 10**10):  # astronomically large scales: lower-order terms with big constants vanish
        x = mpmath.mpf(10) ** k
        val = _eval(f, {**base, **path(x)})
        if val is None:
            return None
        pts.append((mpmath.log(x), mpmath.log(val)))
    # solve y = a*l + b*log(l) + c exactly through the three points
    M = mpmath.matrix([[l, mpmath.log(l), 1] for l, _ in pts])
    a, b, _ = mpmath.lu_solve(M, mpmath.matrix([y for _, y in pts]))
    return _round(float(a)), _round(float(b))


def profile(e, canonical: set[str]) -> dict | None:
    """{var: (a, b)} for scanned variables in e, or None if e cannot be profiled.

    Values are display exponents (T-contribution subtracted); raw path exponents are
    stored under "_path".
    """
    syms = {str(s) for s in e.free_symbols}
    if syms & OPAQUE or syms - canonical - set(SCAN):
        return None
    args = sorted(syms)
    f = sympy.lambdify(args, e, modules="mpmath")
    base = {a: mpmath.mpf(str(sympy.N(sympy.sympify(BASE.get(a, 1)), 50))) for a in args}
    out, path_out = {}, {}
    T = "T" in syms
    if T:
        ab = _fit(f, args, base, lambda x: {"T": x})
        if ab is None:
            return None
        out["T"] = path_out["T"] = ab
    aT, bT = out.get("T", (0, 0))
    for v in SCAN:
        if v == "T" or v not in syms:
            continue
        up = SCAN[v][1] == "up"
        pt = (lambda x, v=v, up=up: {v: x if up else 1 / x, **({"T": x ** PATH_POWER} if T else {})})
        ab = _fit(f, args, base, pt)
        if ab is None:
            return None
        path_out[v] = ab
        out[v] = (_round(ab[0] - PATH_POWER * aT), _round(ab[1] - bT))
    out["_path"] = path_out
    return out


def _round(x: float) -> float:
    """Snap to simple fractions (halves, thirds, quarters, sixths)."""
    for den in (1, 2, 3, 4, 6):
        if abs(x * den - round(x * den)) < 0.02 * den:
            return round(x * den) / den
    return round(x, 3)


def path_exp(p: dict, v: str) -> tuple:
    """Exponent of p along the scan path of v. A bound that does not involve v still
    grows along the path through T = v^PATH_POWER (when it involves T)."""
    if v in p["_path"]:
        return tuple(p["_path"][v])
    aT, bT = p["_path"].get("T", (0, 0))
    return (_round(PATH_POWER * aT), bT) if v != "T" else (0, 0)


def comparable_vars(p: dict, q: dict) -> set:
    return (set(p["_path"]) | set(q["_path"])) - set(p.get("_unknown", ())) - set(q.get("_unknown", ()))


def leq(p: dict, q: dict) -> bool:
    """p grows no faster than q along every scanned path (lexicographic in (a, b)).
    Accepts profiles fresh from profile() or reloaded from JSON (lists)."""
    return all(path_exp(p, v) <= path_exp(q, v) for v in comparable_vars(p, q))


def fmt(ab) -> str:
    a, b = ab
    return f"{a:g}" + (f"·log^{b:g}" if b else "")


def main() -> None:
    results = {r["id"]: r for r in json.loads((OUT / "results.json").read_text())}
    inferred = json.loads((OUT / "inferred.json").read_text())
    entries = []  # (id, setting_id, side, quantity, dependence, algorithm_class, notation, expr, inherited, caveats)
    for r in results.values():
        entries.append((r["id"], r["setting_id"], r["side"], r.get("quantity"), r.get("dependence"),
                        r.get("algorithm_class"), r["bound"].get("notation"),
                        r["bound"].get("expression_normalised") or r["bound"]["expression"], False, []))
    for x in inferred:
        src = results[x["from_result"]]
        entries.append((x["id"], x["setting_id"], src["side"], x.get("quantity") or src.get("quantity"),
                        x.get("dependence") or src.get("dependence"),
                        src.get("algorithm_class"), src["bound"].get("notation"), x["expression"], True,
                        x["caveats"]))

    canonical = set(schema.load_variables()["variables"]) | {"Delta"}
    # A high-probability upper bound B(delta) gives an expected-regret bound B(1/T) + O(1)
    # (failure event of probability 1/T costs at most T * 1/T): add it to the regret family.
    for e in list(entries):
        eid, sid, side, q, dep, cls, nota, expr, inh, cav = e
        if side == "upper" and q == "high_probability_regret" and "delta" in resolve.IDENT_RE.findall(expr):
            entries.append((eid + "@delta=1/T", sid, side, "expected_regret", dep, cls, nota,
                            f"({expr}).subs(delta, 1/T)".replace("(", "(", 1) if False else
                            str(resolve.parse(expr).subs(sympy.Symbol("delta"), 1 / sympy.Symbol("T"))),
                            inh, cav + ["high-probability bound with delta = 1/T"]))
    profiles, failures = {}, collections.Counter()
    cache = {}
    for eid, sid, side, q, dep, cls, nota, expr, inh, cav in entries:
        key = (expr, nota)
        if key not in cache:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(PROFILE_TIMEOUT_S)
            try:
                cache[key] = profile(instance_expr(expr, nota), canonical)
            except _Timeout:
                print(f"profile timed out after {PROFILE_TIMEOUT_S}s, skipped: {expr[:150]}", flush=True)
                cache[key] = None
            except Exception:  # unparseable / unevaluable expressions get no profile
                cache[key] = None
            finally:
                signal.alarm(0)
        p = cache[key]
        if p is None:
            failures["no_profile"] += 1
        elif dep == "instance_dependent" and nota in ("O", "O_tilde", "Theta") and "Delta" not in p:
            p = {**p, "_unknown": {"Delta"}}  # hidden instance-dependent constant
        elif "Delta" in p and set(resolve.IDENT_RE.findall(expr)) & INSTANCE_TIED_PARAMS:
            p = {**p, "_unknown": {"Delta"}}  # tuning parameter constrained by the gap (e.g. eps < Delta)
        profiles[eid] = p

    inferred_by_id = {x["id"]: x for x in inferred}

    def conditions_of(eid: str) -> list[str]:
        eid = eid.partition("@")[0]
        r = results.get(eid) or results[inferred_by_id[eid]["from_result"]]
        return r.get("conditions") or []

    regimes = collections.defaultdict(lambda: {"upper": [], "lower": []})
    rate_regime = {}  # bound id -> "family|dependence" of the cell whose rate it takes part in
    for eid, sid, side, q, dep, cls, nota, expr, inh, cav in entries:
        fam = FAMILY.get(q)
        if set(resolve.IDENT_RE.findall(expr)) & WORST_CASE_T:
            dep = "data_dependent"  # small-loss / variation bounds: not comparable with gap-based ones
        p = profiles.get(eid)
        if fam is None or p is None:
            continue
        if changes_model(conditions_of(eid)):
            continue  # a different protocol (e.g. quantum oracle access): not this setting's rate
        if side == "upper" and restricts_instances(conditions_of(eid)):
            continue  # holds only on a restricted instance class: shown, but not the setting's rate
        if side == "upper" and any(T_CAPPED.match(c) for c in conditions_of(eid)):
            continue  # holds only for small horizons (e.g. T < (K log K)^2): says nothing about the rate
        if side == "lower" and cls == "other" and any(CONSISTENCY.search(c) for c in conditions_of(eid)):
            cls = "consistent"  # the admissible class of the lower bound (consistent, uniformly good, delta-correct)
        if side == "lower" and (cls not in MINIMAX_LOWER_CLASSES or any(c.startswith("holds for") for c in cav)
                                or (cls in (None, "all") and restricts_algorithms(conditions_of(eid)))):
            continue  # algorithm-specific or fixed-parameter lower bounds don't define the setting's rate
        if side == "lower" and inh and any("unspecified on one side" in c for c in cav) \
                and restricts_instances(conditions_of(eid)):
            continue  # hard instances may lie outside the target (e.g. non-observable graphs, observability unspecified)
        regimes[(sid, fam, dep)][side].append({"id": eid, "profile": p, "inherited": inh})
        rate_regime[eid] = f"{fam}|{dep}"

    settings_out, conflicts = collections.defaultdict(dict), []
    status_count = collections.Counter()
    for (sid, fam, dep), sides in regimes.items():
        ups = [u for u in sides["upper"]]
        los = [l for l in sides["lower"]]
        up_front = [u for u in ups if not any(leq(v["profile"], u["profile"]) and v["profile"] != u["profile"] for v in ups)]
        lo_front = [l for l in los if not any(leq(l["profile"], v["profile"]) and v["profile"] != l["profile"] for v in los)]
        vars_ = sorted({v for x in up_front + lo_front for v in x["profile"]["_path"]})
        per_var, status = {}, None
        if not up_front:
            status = "no_upper"
        elif not lo_front:
            status = "no_lower"
        else:
            worst = 0
            for v in vars_:
                us = [x for x in up_front if v not in x["profile"].get("_unknown", set())]
                ls = [x for x in lo_front if v not in x["profile"].get("_unknown", set())]
                if not us or not ls:
                    continue
                bu = min(path_exp(x["profile"], v) for x in us)
                bl = max(path_exp(x["profile"], v) for x in ls)
                du = min(tuple(x["profile"].get(v, (0, 0))) for x in us)
                dl = max(tuple(x["profile"].get(v, (0, 0))) for x in ls)
                if bu < bl:
                    s, lvl = "conflict", 3
                    conflicts.append({"setting_id": sid, "family": fam, "dependence": dep, "var": v,
                                      "upper": [x["id"] for x in us if path_exp(x["profile"], v) == bu],
                                      "lower": [x["id"] for x in ls if path_exp(x["profile"], v) == bl],
                                      "upper_rate": fmt(du), "lower_rate": fmt(dl)})
                elif bu == bl:
                    s, lvl = "tight", 0
                elif bu[0] == bl[0]:
                    s, lvl = "log_gap", 1
                else:
                    s, lvl = "poly_gap", 2
                per_var[v] = {"status": s, "upper": fmt(du), "lower": fmt(dl)}
                worst = max(worst, lvl)
            status = ["tight", "log_gap", "poly_gap", "conflict"][worst]
        status_count[status] += 1
        settings_out[sid][f"{fam}|{dep}"] = {
            "status": status, "per_var": per_var,
            "upper_front": [x["id"] for x in up_front], "lower_front": [x["id"] for x in lo_front],
            "relies_on_inherited": any(x["inherited"] for x in up_front + lo_front),
            "n_upper": len(ups), "n_lower": len(los)}

    (OUT / "comparison.json").write_text(json.dumps(
        {"profiles": {k: ({v: (sorted(ab) if v == "_unknown" else ab if v == "_path" else list(ab))
                            for v, ab in p.items()} if p is not None else None) for k, p in profiles.items()},
         "settings": settings_out, "conflicts": conflicts, "rate_regime": rate_regime}, indent=1, ensure_ascii=False))
    n_prof = sum(1 for p in profiles.values() if p is not None)
    print(f"{len(entries)} bounds; profiled {n_prof} ({n_prof / len(entries):.0%}); {failures['no_profile']} without profile")
    print(f"{len(regimes)} (setting, regime) cells: " + ", ".join(f"{k} {v}" for k, v in status_count.most_common()))
    print(f"{len(conflicts)} per-variable conflicts (upper below lower)")


if __name__ == "__main__":
    main()
