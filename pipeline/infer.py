"""Propagate bounds along the specialisation order (desiderata D1).

Rules, for every pair S ⊑ S' (S a special case of S'):
  - an upper bound proved on S' holds on S. Reduction maps are applied (e.g. a
    linear bound in d becomes a K-armed bound with d = K), and parameters fixed in S
    are substituted (e.g. K = 2);
  - a lower bound proved on S holds on S'. Reduction maps are inverted (a K-armed
    Omega(sqrt(KT)) becomes Omega(sqrt(dT)) on linear); for a parameter fixed in S
    the bound holds for that parameter value.
Only extracted results are propagated (one hop over the transitively closed order),
so derivations never chain through other inferred results.

Writes data/canonical/inferred.json: one record per (result, target setting) with the
source result, the changed dimensions, substitutions and caveats. Inferred results
are never mixed into results.json.

Usage: uv run python pipeline/infer.py
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import sympy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import resolve  # noqa: E402
import schema  # noqa: E402
from order import CAVEATS, Order  # noqa: E402

OUT = schema.ROOT / "data" / "canonical"

# Results that must not propagate: pull-count and other non-performance quantities,
# and realised-regret lower bounds (they hold only with constant probability).
SKIP_QUANTITIES = {"other"}
SKIP_LOWER_QUANTITIES = {"realized_regret"}


def transferable(r: dict, target_key: dict) -> bool:
    if r.get("quantity") in SKIP_QUANTITIES:
        return False
    if r["side"] == "lower" and r.get("quantity") in SKIP_LOWER_QUANTITIES:
        return False
    if r.get("quantity") == "bayesian_regret" and "bayesian_prior" not in (target_key.get("instance_assumptions") or []):
        return False  # Bayesian regret is undefined without a prior
    return True


def foreign_symbols(expr: str | None, canonical: set[str]) -> list[str]:
    """Symbols defined only in the source paper (declared, not canonical)."""
    if not expr:
        return []
    names = set(resolve.IDENT_RE.findall(expr)) - resolve.FUNC_NAMES - {"pi"}
    return sorted(n for n in names if n not in canonical)


def substitute(expr: str | None, mapping: dict) -> tuple[str | None, dict]:
    """Substitute symbols in an expression; returns (new expression, substitutions used)."""
    if not expr or not mapping:
        return expr, {}
    try:
        e = resolve.parse(expr)
    except Exception:  # unparseable expressions are left as-is and flagged by validate.py
        return expr, {}
    used = {}
    for sym, val in mapping.items():
        s = sympy.Symbol(sym)
        if s in e.free_symbols:
            try:
                v = resolve.parse(str(val))
            except Exception:  # a constraint such as ">=2", not a value: leave the symbol
                continue
            e = e.subs(s, v)
            used[sym] = str(val)
    return str(e), used


def main() -> None:
    ont = schema.load_ontology()
    order = Order(ont)
    canonical = set(schema.load_variables()["variables"])
    settings = {s["id"]: s for s in json.loads((OUT / "settings.json").read_text())}
    results = json.loads((OUT / "results.json").read_text())
    by_setting = collections.defaultdict(list)
    for r in results:
        by_setting[r["setting_id"]].append(r)

    pairs = list(order.comparable_pairs({k: v["key"] for k, v in settings.items()}))
    inferred = []
    for special, general, changes in pairs:
        down_map, up_map, fixed, caveats = {}, {}, {}, []
        for ch in changes:
            if ch.kind in ("reduction", "order") and ch.param_map:
                down_map.update(ch.param_map)  # reduction maps and value maps (e.g. M_ctx = 1)
            if ch.kind == "reduction":
                # invert plain-symbol maps for lower bounds (K-armed -> linear: K := d)
                up_map.update({v: k for k, v in ch.param_map.items() if isinstance(v, str) and v.isidentifier()})
            if ch.kind == "parameter":
                fixed.update(ch.param_map)
            if ch.dim in CAVEATS and CAVEATS[ch.dim] not in caveats:
                caveats.append(CAVEATS[ch.dim])
        change_list = [{"dim": c.dim, "special": c.special, "general": c.general, "kind": c.kind} for c in changes]

        for r in by_setting.get(general, []):
            if r["side"] != "upper" or not transferable(r, settings[special]["key"]):
                continue
            expr, subs = substitute(r["bound"].get("expression_normalised") or r["bound"]["expression"],
                                    {**down_map, **fixed})
            foreign = foreign_symbols(expr, canonical)
            inferred.append({"id": f"{r['id']}>{special}", "rule": "upper_bound_to_special_case",
                             "setting_id": special, "from_setting": general, "from_result": r["id"],
                             "expression": expr, "substitutions": subs, "changes": change_list,
                             "caveats": caveats + ([f"uses symbols defined only in the source setting: {', '.join(foreign)}"] if foreign else [])})
        for r in by_setting.get(special, []):
            if r["side"] != "lower" or not transferable(r, settings[general]["key"]):
                continue
            expr, subs = substitute(r["bound"].get("expression_normalised") or r["bound"]["expression"], up_map)
            foreign = foreign_symbols(expr, canonical)
            note = [f"holds for {k} = {v} only" for k, v in fixed.items()]
            note += [f"uses symbols defined only in the source setting: {', '.join(foreign)}"] if foreign else []
            inferred.append({"id": f"{r['id']}>{general}", "rule": "lower_bound_to_generalisation",
                             "setting_id": general, "from_setting": special, "from_result": r["id"],
                             "expression": expr, "substitutions": subs, "changes": change_list,
                             "caveats": caveats + note})

    (OUT / "inferred.json").write_text(json.dumps(inferred, indent=1, ensure_ascii=False))
    got = collections.Counter(x["setting_id"] for x in inferred)
    own = {k: len(v) for k, v in by_setting.items()}
    empty_before = sum(1 for s in settings if not own.get(s))
    empty_after = sum(1 for s in settings if not own.get(s) and not got.get(s))
    print(f"{len(pairs)} ordered pairs; {len(inferred)} inferred results "
          f"({sum(x['rule'].startswith('upper') for x in inferred)} upper, "
          f"{sum(x['rule'].startswith('lower') for x in inferred)} lower)")
    print(f"settings with any lower bound: own {sum(1 for s in settings if any(r['side'] == 'lower' for r in by_setting.get(s, [])))}"
          f" -> with inherited {len({x['setting_id'] for x in inferred if x['rule'].startswith('lower')} | {s for s in settings if any(r['side'] == 'lower' for r in by_setting.get(s, []))})}"
          f" of {len(settings)}")
    print(f"settings with no results: {empty_before} -> {empty_after}")


if __name__ == "__main__":
    main()
