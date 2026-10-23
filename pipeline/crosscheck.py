"""Cross-check extractions against how other papers cite them (desiderata D5).

Every extraction records `cited_results`: bounds a paper attributes to earlier work (often from
its comparison table). resolve.py links them to corpus papers (data/canonical/citations.json).
For each cited bound we ask whether our own extraction of the cited paper contains a result on
the same side with the same growth rate (the profile of pipeline/compare.py, on the
uniform-gap instance):

  exact     same polynomial and logarithmic exponents in every variable
  poly      same polynomial exponents, different log factors (citations often drop logs)
  differs   the cited paper's results on that side all have other rates
  missing   we extracted no result on that side from the cited paper
  skipped   the cited bound has no profile (unparseable, paper-specific symbols)

A rate attributed to a paper by several independent citing papers that our extraction of the
paper lacks is the strongest error signal ("consensus disagreements"): either we missed or
mis-transcribed a result, or the community cites it in a different form.

Writes data/reports/crosscheck.json and data/reports/crosscheck.md.
Usage: uv run python pipeline/crosscheck.py
"""

from __future__ import annotations

import collections
import json
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402
import schema  # noqa: E402

ROOT = schema.ROOT
CAN = ROOT / "data" / "canonical"
OUT = ROOT / "data" / "reports"
VARS = ("T", "K", "d", "Delta")


def rate(expr: str, notation: str | None, canonical: set, cache: dict):
    key = (expr, notation)
    if key not in cache:
        signal.signal(signal.SIGALRM, compare._alarm)
        signal.alarm(compare.PROFILE_TIMEOUT_S)
        try:
            p = compare.profile(compare.instance_expr(expr, notation), canonical)
        except compare._Timeout:  # e.g. exponentials in d at T = 10^(10^10)
            p = None
        except Exception:  # unparseable paper expressions get no rate
            p = None
        finally:
            signal.alarm(0)
        cache[key] = None if p is None else {v: tuple(p[v]) for v in VARS if v in p}
    return cache[key]


def poly(r: dict) -> tuple:
    return tuple(round(r.get(v, (0, 0))[0], 3) for v in VARS)


def full(r: dict) -> tuple:
    return tuple((round(r.get(v, (0, 0))[0], 3), round(r.get(v, (0, 0))[1], 3)) for v in VARS)


def fmt(r: dict | None) -> str:
    if r is None:
        return "?"
    parts = []
    for v in VARS:
        a, b = r.get(v, (0, 0))
        if a or b:
            name = "1/Δ" if v == "Delta" else v
            parts.append(f"{name}^{a:g}" + (f"·log^{b:g}" if b else ""))
    return " ".join(parts) or "1"


def main() -> None:
    canonical = set(schema.load_variables()["variables"]) | {"Delta"}
    cits = json.loads((CAN / "citations.json").read_text())
    results = json.loads((CAN / "results.json").read_text())
    own = collections.defaultdict(list)  # paper -> its results
    for r in results:
        own[r["paper"]].append(r)
    cache = {}
    profiles = json.loads((CAN / "comparison.json").read_text())["profiles"]  # our own results, from compare.py
    own_rates = {}  # paper, side -> list of (rate, result id, expression)
    for p, rs in own.items():
        for r in rs:
            pr = profiles.get(r["id"])
            rr = None if pr is None else {v: tuple(pr[v]) for v in VARS if v in pr}
            if rr is not None:
                own_rates.setdefault((p, r["side"]), []).append((rr, r["id"], r["bound"]["expression"]))

    rows = []
    for citing, refs in cits.items():
        for key, ref in refs.items():
            pid = ref.get("paper_id")
            if not pid or pid == citing or pid not in own:
                continue
            for b in ref.get("bounds") or []:
                side, bd = b.get("side"), b.get("bound") or {}
                cr = rate(bd.get("expression") or "", bd.get("notation"), canonical, cache)
                mine = own_rates.get((pid, side), [])
                if cr is None:
                    verdict, match = "skipped", None
                elif not any(r["side"] == side for r in own[pid]):
                    verdict, match = "missing", None
                elif any(full(m[0]) == full(cr) for m in mine):
                    verdict, match = "exact", next(m[1] for m in mine if full(m[0]) == full(cr))
                elif any(poly(m[0]) == poly(cr) for m in mine):
                    verdict, match = "poly", next(m[1] for m in mine if poly(m[0]) == poly(cr))
                else:
                    verdict, match = "differs", None
                rows.append({"citing": citing, "cited": pid, "side": side, "algorithm": b.get("algorithm_name"),
                             "expression": bd.get("expression"), "notation": bd.get("notation"),
                             "setting": b.get("setting_description"), "rate": fmt(cr), "verdict": verdict,
                             "matched_result": match,
                             "own_rates": sorted({fmt(m[0]) for m in mine})})

    counts = collections.Counter(r["verdict"] for r in rows)
    checked = [r for r in rows if r["verdict"] != "skipped"]
    # consensus: same (cited paper, side, polynomial rate) from >= 2 distinct citing papers, not in our extraction
    groups = collections.defaultdict(lambda: {"citers": set(), "rows": []})
    for r in checked:
        if r["verdict"] in ("differs", "missing"):
            g = groups[(r["cited"], r["side"], r["rate"].split("·log")[0] if r["rate"] else r["rate"])]
            g["citers"].add(r["citing"])
            g["rows"].append(r)
    consensus = sorted(((k, g) for k, g in groups.items() if len(g["citers"]) >= 2),
                       key=lambda kg: (-len(kg[1]["citers"]), kg[0]))
    per_paper = collections.defaultdict(collections.Counter)
    for r in checked:
        per_paper[r["cited"]][r["verdict"]] += 1

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "crosscheck.json").write_text(json.dumps({"counts": counts, "rows": rows,
                                                    "consensus": [{"cited": k[0], "side": k[1], "rate": k[2],
                                                                   "citers": sorted(g["citers"]), "rows": g["rows"]}
                                                                  for k, g in consensus]},
                                                   indent=1, ensure_ascii=False, default=list))
    n = len(checked)
    agree = counts["exact"] + counts["poly"]
    lines = ["# Citation cross-check", "",
             "Generated by `pipeline/crosscheck.py`. Each bound that a corpus paper attributes to another corpus paper "
             "(`cited_results`) is compared with our own extraction of the cited paper by growth rate "
             "(exponents of T, K, d, 1/Δ on the uniform-gap instance).", "",
             f"- cited bounds pointing at corpus papers: {len(rows)} ({counts['skipped']} without a comparable rate)",
             f"- compared: {n}: **{agree} agree** ({agree / max(n, 1):.0%}; {counts['exact']} exactly, {counts['poly']} up to "
             f"log factors), {counts['differs']} differ, {counts['missing']} cite a side we extracted nothing for",
             f"- consensus disagreements (a rate cited by ≥ 2 papers that our extraction lacks): {len(consensus)}", "",
             "A disagreement is a lead, not an error: citing papers paraphrase, specialise (e.g. K = 2) or cite a "
             "different theorem of the same paper. Consensus disagreements are the ones to check first.", "",
             "## Consensus disagreements", "",
             "| cited paper | side | rate cited | cited by | our rates for that side |", "|---|---|---|---|---|"]
    for (pid, side, r), g in consensus[:60]:
        ours = sorted({x for row in g["rows"] for x in row["own_rates"]})
        lines.append(f"| {pid} | {side} | {r} | {len(g['citers'])}: {', '.join(sorted(g['citers'])[:4])}"
                     f"{'…' if len(g['citers']) > 4 else ''} | {'; '.join(ours[:4]) or '(none)'} |")
    lines += ["", "## Most-cited papers", "", "| paper | exact | poly | differs | missing |", "|---|---|---|---|---|"]
    for pid, c in sorted(per_paper.items(), key=lambda kv: -sum(kv[1].values()))[:30]:
        lines.append(f"| {pid} | {c['exact']} | {c['poly']} | {c['differs']} | {c['missing']} |")
    (OUT / "crosscheck.md").write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} cited bounds; compared {n}: exact {counts['exact']}, poly {counts['poly']}, "
          f"differs {counts['differs']}, missing {counts['missing']}, skipped {counts['skipped']}; "
          f"consensus disagreements {len(consensus)}")


if __name__ == "__main__":
    main()
