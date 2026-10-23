"""Check the atlas against a textbook gold set (data/ground_truth/ls-book.yaml).

For each textbook result at setting B (an assumption vector over the ontology), with growth
rate r (pipeline/compare.py profile on the uniform-gap instance):

  recovered     the atlas has an extracted bound valid at B that is at least as strong:
                an upper bound <= r from B or a more general setting (upper bounds transfer to
                special cases), or a lower bound >= r from B or a special case;
                `exact` when the rates are equal, `stronger` when the atlas has a better one
  contradicted  an atlas bound valid at B is incompatible with the book: an upper bound below
                the book's lower bound, or a lower bound above the book's upper bound
                (rate-defining atlas bounds only: not restricted / algorithm-specific)
  not covered   neither: the corpus lacks the result at B and everything around it
  skipped       the book's expression has no rate (paper-specific symbols, no T)

Writes data/reports/goldcheck.md and .json.
Usage: uv run python pipeline/goldcheck.py [--gold data/ground_truth/ls-book.yaml]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402
import resolve  # noqa: E402
import schema  # noqa: E402
from order import Order  # noqa: E402

ROOT = schema.ROOT
CAN = ROOT / "data" / "canonical"
REG = ["T", "K", "d", "Delta"]


def prof(expr, nota, canonical):
    try:
        p = compare.profile(compare.instance_expr(expr, nota), canonical)
    except Exception:  # paper-specific expressions get no rate
        return None
    return p


def with_defaults(setting: dict, ont: dict) -> dict:
    """Gold entries list only the dimensions that matter; fill the rest as extractions do
    (context none, domain not_applicable, standard homoscedastic noise in stochastic settings)."""
    s = dict(setting)
    for dim, spec in ont["dimensions"].items():
        if dim in s or spec.get("multi"):
            continue
        for default in ("none", "not_applicable"):
            if default in spec["values"]:
                s[dim] = default
                break
    if str(s.get("environment", "")).startswith("stochastic") and "noise_detail" not in s:
        s["noise_detail"] = {"variance": "homoscedastic"}
    return s


def cmp_rates(p: dict, q: dict) -> int | None:
    """-1 if p grows strictly slower than q in some comparable variable and no faster in any,
    0 if equal on all comparable variables, 1 if strictly faster, None if incomparable."""
    vs = compare.comparable_vars(p, q)
    if not vs:
        return None
    a = [compare.path_exp(p, v) for v in vs]
    b = [compare.path_exp(q, v) for v in vs]
    if a == b:
        return 0
    if all(x <= y for x, y in zip(a, b)):
        return -1
    if all(x >= y for x, y in zip(a, b)):
        return 1
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", default=str(ROOT / "data" / "ground_truth" / "ls-book.yaml"))
    args = ap.parse_args()
    ont = schema.load_ontology()
    order = Order(ont)
    canonical = set(schema.load_variables()["variables"]) | {"Delta"}
    gold = yaml.safe_load(Path(args.gold).read_text())["results"]
    settings = {s["id"]: s for s in json.loads((CAN / "settings.json").read_text())}
    results = json.loads((CAN / "results.json").read_text())
    cmpd = json.loads((CAN / "comparison.json").read_text())
    profiles, rate_regime = cmpd["profiles"], cmpd.get("rate_regime", {})
    by_setting = collections.defaultdict(list)
    for r in results:
        by_setting[r["setting_id"]].append(r)

    def norm(p):
        if p is None:
            return None
        return {k: (tuple(v) if k != "_unknown" else set(v)) if isinstance(v, list) else v for k, v in p.items()}

    rows = []
    for g in gold:
        p = prof(g["expression"], g.get("notation"), canonical)
        if p is not None:  # variables the rate cannot be compared in (as compare.py does for the atlas)
            unknown = set(g.get("hidden_dependence") or [])
            if set(resolve.IDENT_RE.findall(g["expression"])) & compare.INSTANCE_TIED_PARAMS:
                unknown.add("Delta")  # e.g. eps < Delta_i in Theorem 8.1
            if unknown:
                p = {**p, "_unknown": unknown}
        fam, dep = compare.FAMILY.get(g["quantity"]), g["dependence"]
        rec = {"id": g["id"], "theorem": g["theorem"], "side": g["side"], "quantity": g["quantity"], "dependence": dep,
               "expression": g["expression"], "algorithm": g.get("algorithm"), "confidence": g.get("confidence", "high")}
        if p is None or fam is None or "T" not in p and g["quantity"] not in ("sample_complexity", "simple_regret", "error_probability"):
            rows.append({**rec, "verdict": "skipped"})
            continue
        key = resolve.setting_key(with_defaults(g["setting"], ont), ont)
        recovered, contradicted, n_rel = [], [], 0
        for sid, s in settings.items():
            same = s["key"] == key
            gen = same or bool(order.leq(key, s["key"]))   # S is more general than B: its upper bounds hold at B
            spe = same or bool(order.leq(s["key"], key))   # S is a special case: its lower bounds hold at B
            if not (gen or spe):
                continue
            n_rel += 1
            for r in by_setting.get(sid, []):
                if compare.FAMILY.get(r.get("quantity")) != fam or r.get("dependence") != dep:
                    continue
                q = norm(profiles.get(r["id"]))
                if q is None:
                    continue
                c = cmp_rates(q, p)
                if c is None:
                    continue
                in_rate = rate_regime.get(r["id"]) is not None
                hit = {"result": r["id"], "setting": sid, "label": s["label"], "expression": r["bound"]["expression"],
                       "relation": {-1: "slower", 0: "equal", 1: "faster"}[c]}
                if g["side"] == "upper":
                    if r["side"] == "upper" and gen and c <= 0:
                        recovered.append(hit)
                    if r["side"] == "lower" and spe and c > 0 and in_rate:
                        contradicted.append(hit)
                else:
                    if r["side"] == "lower" and spe and c >= 0:
                        recovered.append(hit)
                    if r["side"] == "upper" and gen and c < 0 and in_rate:
                        contradicted.append(hit)
        verdict = ("contradicted" if contradicted else
                   ("recovered" if recovered else "not covered"))
        exact = any(h["relation"] == "equal" for h in recovered)
        rows.append({**rec, "verdict": verdict, "exact": exact, "n_related_settings": n_rel,
                     "recovered_by": recovered[:5], "contradicted_by": contradicted[:5]})

    c = collections.Counter(r["verdict"] for r in rows)
    checked = [r for r in rows if r["verdict"] != "skipped"]
    n = len(checked)
    rec_n = sum(1 for r in checked if r["verdict"] == "recovered")
    out = ROOT / "data" / "reports"
    (out / "goldcheck.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    lines = ["# Textbook gold-set check", "",
             f"Generated by `pipeline/goldcheck.py` from `{Path(args.gold).relative_to(ROOT)}` "
             "(Lattimore & Szepesvári, *Bandit Algorithms*; LLM-transcribed with verbatim quotes, not human-verified).", "",
             f"- book results: {len(rows)}; checkable (with a growth rate): {n}",
             f"- **recovered**: {rec_n} ({rec_n / max(n, 1):.0%}) — the atlas has an equal "
             f"({sum(1 for r in checked if r.get('exact'))}) or stronger bound valid at the book's setting",
             f"- **contradicted**: {c['contradicted']} — an atlas bound valid there is incompatible with the book",
             f"- not covered: {c['not covered']}; skipped: {c['skipped']}", "",
             "Contradictions are the error signal: either an extraction is wrong, or a transfer rule is.", "",
             "## Contradictions", ""]
    for r in rows:
        if r["verdict"] == "contradicted":
            lines.append(f"- **{r['id']}** ({r['theorem']}, {r['side']}, {r['quantity']}, {r['dependence']}): "
                         f"`{r['expression']}`")
            for h in r["contradicted_by"][:3]:
                lines.append(f"  - atlas {h['result']} in *{h['label']}*: `{h['expression']}` ({h['relation']})")
    lines += ["", "## All results", "", "| id | side | verdict | atlas evidence |", "|---|---|---|---|"]
    for r in rows:
        ev = (r.get("recovered_by") or r.get("contradicted_by") or [{}])[0].get("result", "")
        lines.append(f"| {r['id']} | {r['side']} | {r['verdict']}{' (exact)' if r.get('exact') else ''} | {ev} |")
    (out / "goldcheck.md").write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} book results; checkable {n}: recovered {rec_n}, contradicted {c['contradicted']}, "
          f"not covered {c['not covered']}, skipped {c['skipped']}")


if __name__ == "__main__":
    main()
