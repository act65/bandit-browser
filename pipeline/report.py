"""Gap and open-problem reports (desiderata D8) plus the poset artifact.

Writes:
  data/canonical/poset.json   covering edges (Hasse diagram) of the specialisation order,
                              each with changed dimensions and their justifications
  data/reports/gaps.md        log / polynomial gaps per setting and regime
  data/reports/missing-lower-bounds.md
  data/reports/conflicts.md   upper bound below a lower bound: extraction error or contradiction
  data/reports/unstudied-neighbours.md
                              settings one order step from a well-studied setting with no results
  data/reports/redundant.md   results whose rate was already implied by an earlier paper
All gaps are *candidates*: before calling one open, check for a resolving paper
outside the corpus (gap triage, plan.md Phase 3).

Usage: uv run python pipeline/report.py
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402
import schema  # noqa: E402
from order import Order  # noqa: E402

ROOT = schema.ROOT
CAN = ROOT / "data" / "canonical"
REP = ROOT / "data" / "reports"
MANIFEST = ROOT / "corpus" / "manifest.yaml"
WELL_STUDIED = 2  # papers


def load():
    settings = {s["id"]: s for s in json.loads((CAN / "settings.json").read_text())}
    results = {r["id"]: r for r in json.loads((CAN / "results.json").read_text())}
    inferred = {x["id"]: x for x in json.loads((CAN / "inferred.json").read_text())}
    cmp = json.loads((CAN / "comparison.json").read_text())
    years = {p["id"]: p.get("year") for p in yaml.safe_load(MANIFEST.read_text())["papers"]}
    return settings, results, inferred, cmp, years


def papers_of(sid, settings) -> set:
    return {m["paper"] for m in settings[sid]["members"]}


def describe(eid, results, inferred) -> str:
    eid, _, derived = eid.partition("@")  # e.g. "<id>@delta=1/T": high-probability bound read in expectation
    if derived:
        return describe(eid, results, inferred) + f" [{derived}]"
    if eid in results:
        r = results[eid]
        return f"`{r['bound'].get('expression_normalised') or r['bound']['expression']}` ({r['bound']['notation']}; {r['paper']} {r['source']['number']})"
    x = inferred[eid]
    r = results[x["from_result"]]
    return f"`{x['expression']}` ({r['bound']['notation']}; inherited from {r['paper']} {r['source']['number']})"


def conditions_of(eid, results, inferred) -> list[str]:
    eid = eid.partition("@")[0]
    r = results.get(eid) or results[inferred[eid]["from_result"]]
    return r.get("conditions") or []


def poset(settings, order: Order) -> list[dict]:
    pairs = {(a, b): ch for a, b, ch in order.comparable_pairs({k: v["key"] for k, v in settings.items()})}
    succ = collections.defaultdict(set)
    for a, b in pairs:
        succ[a].add(b)
    cover = []
    for (a, b), ch in pairs.items():
        if not any((c, b) in pairs for c in succ[a] if c != b):
            cover.append({"special": a, "general": b,
                          "changes": [{"dim": c.dim, "special": c.special, "general": c.general, "kind": c.kind,
                                       "justification": c.justification, "caveats": c.caveats,
                                       "param_map": c.param_map} for c in ch]})
    return cover


def unstudied(settings, order: Order, ont: dict) -> list[tuple]:
    """Keys one direct order step away (scalar dimensions) from well-studied settings."""
    existing = {json.dumps(s["key"], sort_keys=True) for s in settings.values()}
    cands = {}
    for sid, s in settings.items():
        n = len(papers_of(sid, settings))
        if n < WELL_STUDIED:
            continue
        for dim, spec in ont["dimensions"].items():
            if spec.get("multi"):
                continue
            v = s["key"].get(dim)
            for a, b in [tuple(p) for p in spec.get("order") or []]:
                for frm, to, direction in ((a, b, "generalise"), (b, a, "specialise")):
                    if v != frm:
                        continue
                    k = {**s["key"], dim: to}
                    blob = json.dumps(k, sort_keys=True)
                    if blob in existing:
                        continue
                    c = cands.setdefault(blob, {"key": k, "from": [], "score": 0})
                    c["from"].append((sid, dim, frm, to, direction))
                    c["score"] += n
    return sorted(cands.values(), key=lambda c: -c["score"])


def main() -> None:
    settings, results, inferred, cmp, years = load()
    ont = schema.load_ontology()
    order = Order(ont)
    REP.mkdir(parents=True, exist_ok=True)

    cover = poset(settings, order)
    (CAN / "poset.json").write_text(json.dumps(cover, indent=1, ensure_ascii=False, default=list))

    rows = []
    for sid, regimes in cmp["settings"].items():
        for reg, c in regimes.items():
            rows.append((sid, reg, c))
    label = lambda sid: f"{settings[sid]['label']} (`{sid}`, {len(papers_of(sid, settings))} papers)"

    # gaps
    gaps = [r for r in rows if r[2]["status"] in ("log_gap", "poly_gap")]
    gaps.sort(key=lambda r: (r[2]["status"] != "poly_gap", -len(papers_of(r[0], settings))))
    out = ["# Candidate gaps", "", "Settings whose best upper and lower bounds differ (polynomial gaps first). "
           "Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for "
           "resolving papers outside the corpus before calling a gap open.", ""]
    for sid, reg, c in gaps:
        out.append(f"## {label(sid)}: {reg.replace('|', ', ')} — **{c['status'].replace('_', ' ')}**")
        out += [f"- {v}: upper {pv['upper']} vs lower {pv['lower']} ({pv['status']})" for v, pv in c["per_var"].items()]
        out += ["- best upper: " + "; ".join(describe(e, results, inferred) for e in c["upper_front"][:3]),
                "- best lower: " + "; ".join(describe(e, results, inferred) for e in c["lower_front"][:3]),
                f"- relies on inherited bounds: {c['relies_on_inherited']}", ""]
    (REP / "gaps.md").write_text("\n".join(out) + "\n")

    # missing lower bounds
    miss = [r for r in rows if r[2]["status"] == "no_lower"]
    miss.sort(key=lambda r: (-len(papers_of(r[0], settings)), -r[2]["n_upper"]))
    out = ["# Settings with upper bounds but no lower bound", "",
           "Including inherited lower bounds. Sorted by number of papers.", "",
           "| setting | regime | papers | upper bounds | best upper |", "|---|---|---|---|---|"]
    for sid, reg, c in miss:
        best = describe(c["upper_front"][0], results, inferred) if c["upper_front"] else ""
        out.append(f"| {settings[sid]['label']} `{sid}` | {reg.replace('|', ', ')} | {len(papers_of(sid, settings))} | {c['n_upper']} | {best} |")
    (REP / "missing-lower-bounds.md").write_text("\n".join(out) + "\n")

    # conflicts
    out = ["# Conflicts (review queue)", "",
           "An upper bound grows more slowly than a lower bound in the same setting and regime. Usually an extraction "
           "error (a dropped term, a missing assumption in the setting) — occasionally a genuine contradiction.", ""]
    for cf in cmp["conflicts"]:
        out += [f"- {label(cf['setting_id'])}, {cf['family']} / {cf['dependence']}, variable {cf['var']}: "
                f"upper {cf['upper_rate']} < lower {cf['lower_rate']}",
                "  - upper: " + describe(cf["upper"][0], results, inferred)
                + (f" — conditions: {'; '.join(cond)}" if (cond := conditions_of(cf["upper"][0], results, inferred)) else ""),
                "  - lower: " + describe(cf["lower"][0], results, inferred)]
    # vacuous upper bounds: regret upper bounds growing at least linearly in T are no better
    # than the trivial bound T (rewards in [0,1]); usually an extraction error, an unoptimised
    # tuning parameter, or a data-dependent quantity read at its worst case
    vac = []
    canonical = set(schema.load_variables()["variables"]) | {"Delta"}
    for eid, r in results.items():
        if r["side"] != "upper" or compare.FAMILY.get(r.get("quantity")) != "regret" or r["bound"].get("regime"):
            continue  # case-split branches (e.g. Delta*T when T*Delta^2 is small) carry a regime
        expr = r["bound"].get("expression_normalised") or r["bound"]["expression"]
        try:
            e = compare.instance_expr(expr, r["bound"].get("notation"))
            e = e.subs(compare.sympy.Symbol("delta"), 1 / compare.sympy.Symbol("T"))  # delta = 1/T
            p = compare.profile(e, canonical) or {}
        except Exception:  # unprofilable expressions are reported by validate.py
            continue
        a, b = p.get("T", (0, 0))
        if a > 1 or (a == 1 and b >= 0):
            vac.append(eid)
    out += ["", "## Vacuous upper bounds (regret growing at least linearly in T)", "",
            "No better than the trivial bound. Usually an extraction error, an unoptimised tuning parameter, "
            "or a data-dependent quantity read at its worst case.", ""]
    out += [f"- {describe(e, results, inferred)}" for e in sorted(vac)]
    (REP / "conflicts.md").write_text("\n".join(out) + "\n")

    # unstudied neighbours
    cands = unstudied(settings, order, ont)
    out = ["# Unstudied neighbours", "",
           f"Settings one direct order step away from a setting studied by ≥ {WELL_STUDIED} papers, with no extracted "
           "results in the corpus. Ranked by how studied the neighbours are. Many will be studied in papers outside the "
           "corpus, or be uninteresting; this is a list of questions, not of open problems.", ""]
    for c in cands[:60]:
        steps = "; ".join(f"{settings[s]['label']} → {d}: {f} → {t} ({how})" for s, d, f, t, how in c["from"][:3])
        out.append(f"- score {c['score']}: {steps}")
    (REP / "unstudied-neighbours.md").write_text("\n".join(out) + "\n")

    # redundancy: own results whose rate is already implied by an earlier paper's result
    profiles = cmp["profiles"]
    by_cell = collections.defaultdict(list)
    for eid, r in results.items():
        by_cell[(r["setting_id"], compare.FAMILY.get(r.get("quantity")), r.get("dependence"), r["side"])].append(eid)
    for eid, x in inferred.items():
        r = results[x["from_result"]]
        by_cell[(x["setting_id"], compare.FAMILY.get(r.get("quantity")), r.get("dependence"), r["side"])].append(eid)
    def paper_of(e):
        e = e.partition("@")[0]
        return results[e]["paper"] if e in results else results[inferred[e]["from_result"]]["paper"]
    red = []
    for (sid, fam, dep, side), eids in by_cell.items():
        if fam is None or side != "upper":
            continue
        for e in eids:
            if e not in results or not profiles.get(e) or not results[e].get("is_new", True):
                continue
            y = years.get(paper_of(e)) or 9999
            for o in eids:
                po = profiles.get(o)
                if o == e or not po or (years.get(paper_of(o)) or 9999) >= y:
                    continue
                if compare.leq(po, profiles[e]):
                    red.append((sid, fam, dep, e, o))
                    break
    out = ["# Results whose rate was already known", "",
           "An extracted upper bound whose growth rate (ignoring constants) is matched or beaten by a result from an "
           "*earlier* paper, proved for this setting or inherited from a more general one. Constants and lower-order "
           "terms are ignored, so these are often genuine refinements; inherited matches are the interesting case "
           "(a special case of a known result).", ""]
    for sid, fam, dep, e, o in sorted(red, key=lambda x: (x[3] in results and o not in results, x[0])):
        out.append(f"- {settings[sid]['label']} ({fam}, {dep}): {describe(e, results, inferred)} "
                   f"— already implied by {describe(o, results, inferred)}")
    (REP / "redundant.md").write_text("\n".join(out) + "\n")

    print(f"poset: {len(cover)} covering edges; gaps {len(gaps)}; missing lower {len(miss)}; "
          f"conflicts {len(cmp['conflicts'])}; unstudied neighbours {len(cands)}; already-known results {len(red)}")


if __name__ == "__main__":
    main()
