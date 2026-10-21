"""Build the site's analysis index (plan.md Phase 3b): data/canonical/site_index.json.

Contents:
  bounds     every bound (extracted and inherited) with metadata, its profile and a
             JavaScript function for plotting: the formula on the uniform-gap instance
             (as in compare.py), arguments = slider variables T, K, d, Delta, delta,
             epsilon; other symbols are fixed at compare.BASE values. O/Theta/Omega
             bounds are plotted with constant 1 (flag `shape_only`).
  cells      per setting and regime: tightness status, per-variable rates, best upper /
             lower fronts, and the gap-triage verdict if one exists.
  transfer   technique-transfer suggestions (motivation 3): for a setting with a gap or
             no upper bound, algorithm families that achieve the best upper bound in a
             neighbouring setting (one covering step in the poset, same regime) but do
             not appear among this setting's upper bounds.
  unstudied  unstudied neighbours (motivation 2), minus ill-posed combinations.
  redundant  results whose rate an earlier paper already implied (motivation 4).

Usage: uv run python pipeline/site_index.py   (run after derive.py)
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import sympy
import yaml
from sympy.printing.jscode import jscode

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402
import report  # noqa: E402
import resolve  # noqa: E402
import schema  # noqa: E402
from order import Order  # noqa: E402

ROOT = schema.ROOT
CAN = ROOT / "data" / "canonical"
SLIDERS = ["T", "K", "d", "Delta", "delta", "epsilon"]
SHAPE_ONLY = {"O", "O_tilde", "Theta", "Omega", "Omega_tilde"}
# Function classes that are not closed under addition: ill-posed against an adversary
# (BCO book: quasi-convex and PL classes "are not amenable to the adversarial setting").
NON_ADDITIVE = {"quasi_convex", "polyak_lojasiewicz"}
# Bounds stated before tuning (learning rate, free analysis constants) are not plotted:
# fixing eta = 1 or eps = 1 gives meaningless curves.
TUNING = {"eta", "eps_alg", "c_alg", "alpha_ts"}
CANONICAL = set(schema.load_variables()["variables"])


def js_function(expr: str, notation: str | None) -> dict | None:
    """{args, body} computing the bound on the uniform-gap instance, or None."""
    try:
        e = compare.instance_expr(expr, notation)
    except Exception:  # unparseable expressions are not plotted
        return None
    names = {str(s) for s in e.free_symbols}
    if names & TUNING or names - CANONICAL - set(SLIDERS):
        return None  # tuning-dependent, or paper-specific symbols with no sensible default
    fixed = {sympy.Symbol(n): sympy.sympify(compare.BASE.get(n, 1)) for n in names if n not in SLIDERS}
    try:
        e = e.subs(fixed)
    except (ValueError, TypeError, ZeroDivisionError):  # e.g. Min/Max of an undefined value
        return None
    if e.has(sympy.zoo, sympy.nan, sympy.I) or any(isinstance(f, sympy.core.function.AppliedUndef) for f in e.atoms(sympy.Function)) or e.has(sympy.LambertW):
        return None
    try:
        body = jscode(e)
    except Exception:  # printer has no JS form for some functions
        return None
    if "Not supported" in body or e.is_number and not e.is_positive:
        return None  # unprintable, or constant zero / negative after fixing non-slider symbols
    return {"args": sorted(str(s) for s in e.free_symbols), "body": body}


def main() -> None:
    settings, results, inferred, cmp, years = report.load()
    algos = {a["id"]: a for a in json.loads((CAN / "algorithms.json").read_text())}
    triage_path = ROOT / "data" / "reports" / "triage.yaml"
    triage = (yaml.safe_load(triage_path.read_text()) or {}).get("triage", {}) if triage_path.exists() else {}
    profiles = cmp["profiles"]

    def family(aid):
        a = algos.get(aid or "")
        return (a or {}).get("family") or ((a or {}).get("techniques") or [None])[0]

    bounds = []
    for eid, r in results.items():
        bounds.append((eid, r, r, False, r["bound"].get("expression_normalised") or r["bound"]["expression"]))
    for eid, x in inferred.items():
        src = results[x["from_result"]]
        bounds.append((eid, x, src, True, x["expression"]))
    out_bounds = []
    for eid, rec, src, inh, expr in bounds:
        nota = src["bound"].get("notation")
        q = rec.get("quantity") or src.get("quantity")
        out_bounds.append({
            "id": eid, "setting_id": rec["setting_id"], "side": src["side"], "quantity": q,
            "family": compare.FAMILY.get(q), "dependence": rec.get("dependence") or src.get("dependence"),
            "notation": nota, "inherited": inh, "from_setting": rec.get("from_setting"),
            "paper": src["paper"], "year": years.get(src["paper"]),
            "algorithm_id": src.get("algorithm_id"), "algorithm_family": family(src.get("algorithm_id")),
            "confidence": src.get("confidence"),
            "restricted": src["side"] == "upper" and compare.restricts_instances(src.get("conditions")),
            "rate_regime": cmp.get("rate_regime", {}).get(eid),  # None: shown, but not used for the rate
            "n_caveats": len(rec.get("caveats") or []), "expression": expr,
            "profile": {k: v for k, v in (profiles.get(eid) or {}).items() if not k.startswith("_")} or None,
            "js": js_function(expr, nota), "shape_only": nota in SHAPE_ONLY,
        })

    cells = []
    for sid, regimes in cmp["settings"].items():
        for reg, c in regimes.items():
            tri = triage.get(f"{sid}|{reg}")
            cells.append({"setting_id": sid, "regime": reg, **{k: c[k] for k in (
                "status", "per_var", "upper_front", "lower_front", "relies_on_inherited", "n_upper", "n_lower")},
                "triage": ({"verdict": tri["verdict"], "summary": tri["summary"],
                            "papers": tri.get("papers", [])} if tri else None)})

    # technique transfer: neighbours one covering step away, same regime
    cover = json.loads((CAN / "poset.json").read_text())
    nbrs = collections.defaultdict(set)
    for e in cover:
        nbrs[e["special"]].add(e["general"])
        nbrs[e["general"]].add(e["special"])
    bound_by_id = {b["id"]: b for b in out_bounds}
    fam_here = collections.defaultdict(set)
    for b in out_bounds:
        if b["side"] == "upper" and b["algorithm_family"]:
            fam_here[(b["setting_id"], f"{b['family']}|{b['dependence']}")].add(b["algorithm_family"])
    cell_of = {(c["setting_id"], c["regime"]): c for c in cells}
    transfer = []
    for c in cells:
        if c["status"] not in ("log_gap", "poly_gap", "no_upper"):
            continue
        sugg = collections.defaultdict(list)
        for n in nbrs.get(c["setting_id"], ()):
            nc = cell_of.get((n, c["regime"]))
            if not nc or nc["status"] not in ("tight", "log_gap"):
                continue
            for bid in nc["upper_front"]:
                fam = (bound_by_id.get(bid.partition("@")[0]) or {}).get("algorithm_family")
                if fam and fam not in fam_here[(c["setting_id"], c["regime"])]:
                    sugg[fam].append({"neighbour": n, "neighbour_status": nc["status"], "bound": bid})
        if sugg:
            transfer.append({"setting_id": c["setting_id"], "regime": c["regime"], "status": c["status"],
                             "families_here": sorted(fam_here[(c["setting_id"], c["regime"])]),
                             "suggestions": [{"family": f, "evidence": ev[:5]} for f, ev in sorted(sugg.items())]})

    order = Order(schema.load_ontology())
    unstudied = []
    for cand in report.unstudied(settings, order, schema.load_ontology()):
        k = cand["key"]
        if str(k.get("environment", "")).startswith("adversarial") and set(k.get("function_class") or []) & NON_ADDITIVE:
            continue
        unstudied.append({"label": resolve.setting_label(k), "key": k, "score": cand["score"],
                          "from": [{"setting_id": s, "dim": d, "from": f, "to": t, "direction": how}
                                   for s, d, f, t, how in cand["from"]]})

    red_md = (ROOT / "data" / "reports" / "redundant.md").read_text().splitlines()
    redundant = [ln[2:] for ln in red_md if ln.startswith("- ")]

    out = {"bounds": out_bounds, "cells": cells, "transfer": transfer, "unstudied": unstudied,
           "redundant": redundant, "sliders": SLIDERS,
           "slider_defaults": {k: float(sympy.sympify(compare.BASE.get(k, 1))) for k in SLIDERS}}
    (CAN / "site_index.json").write_text(json.dumps(out, ensure_ascii=False, default=list))
    n_js = sum(1 for b in out_bounds if b["js"])
    live = {f"{c['setting_id']}|{c['regime']}" for c in cells}
    stale = [k for k in triage if k not in live]
    if stale:
        print(f"warning: {len(stale)} triage verdicts refer to settings/regimes that no longer exist "
              "(setting ids change with the ontology); re-run pipeline/triage.py")
    print(f"{len(out_bounds)} bounds ({n_js} plottable), {len(cells)} cells, {len(transfer)} transfer suggestions, "
          f"{len(unstudied)} unstudied neighbours, {len(redundant)} redundant")


if __name__ == "__main__":
    main()
