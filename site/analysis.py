"""Analysis pages (plan.md Phase 3b): rate plots, gaps, unstudied neighbours, technique
transfer, redundancy and faceted search.

Display only. Everything is read from data/canonical/site_index.json, written by
pipeline/site_index.py (bound profiles, per-cell tightness status, fronts, triage verdicts,
transfer suggestions, unstudied neighbours, redundancy). When the file is missing (e.g.
``--fixtures``) every page still builds and says there is no data.

The page helpers (``page``, ``badge``, ``math`` …) live in build.py and are passed in as
``h`` so this module has no import cycle with it.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import bounds
from ontology import QUANTITY_LABEL, dim_label, value_label

STATUS = {  # key -> (label, short help)
    "conflict": ("conflict", "an upper bound grows more slowly than a lower bound: extraction error or contradiction"),
    "poly_gap": ("poly gap", "best upper and lower bounds differ by a polynomial factor"),
    "log_gap": ("log gap", "best upper and lower bounds differ by logarithmic factors only"),
    "no_lower": ("no lower bound", "upper bounds but no comparable lower bound"),
    "no_upper": ("no upper bound", "lower bounds but no comparable upper bound"),
    "tight": ("tight", "best upper and lower bounds match up to constants"),
    "none": ("no comparable bounds", "no bound in this setting has a usable rate profile"),
}
GAP_STATUSES = ["conflict", "poly_gap", "log_gap", "no_lower", "no_upper"]
# Most relevant first: what a setting's colour on the graph shows when it has several regimes.
STATUS_RANK = {s: i for i, s in enumerate(["conflict", "poly_gap", "log_gap", "no_lower", "no_upper", "tight", "none"])}
TRIAGE = {"closed": "closed by prior work", "open_known": "known open problem", "blank": "blank (no literature found)"}
FAMILY_LABEL = {"regret": "regret", "hp_regret": "high-prob. regret", "bayesian_regret": "Bayesian regret",
                "simple_regret": "simple regret", "switching_regret": "switching regret",
                "sample_complexity": "sample complexity", "error_probability": "error probability",
                "dynamic_regret": "dynamic regret"}
DEP_LABEL = {"worst_case": "worst-case", "instance_dependent": "instance-dependent", "data_dependent": "data-dependent"}
# As in pipeline/compare.py: small-loss / variation bounds form their own regime.
DATA_DEPENDENT = re.compile(r"\b(L_star|Q_T|Lambda_T)\b")
SEARCH_DIMS = ["environment", "action_space", "feedback", "context", "noise", "objective", "function_class",
               "instance_assumptions", "extras"]


def regime_label(reg: str) -> str:
    fam, _, dep = reg.partition("|")
    return f"{FAMILY_LABEL.get(fam, QUANTITY_LABEL.get(fam, fam.replace('_', ' ')))} · {DEP_LABEL.get(dep, dep.replace('_', ' '))}"


def strip_id(bid: str) -> str:
    return bid.partition("@")[0]


def rate_str(s) -> str:
    """'0.5' -> 'T^0.5'-style exponent text used in per-variable rates; '0·log^1' -> 'log¹'."""
    s = str(s)
    a, _, b = s.partition("·log^")
    try:
        a_f = float(a)
    except ValueError:
        return s
    a_txt = "" if a_f == 0 and b else (f"{a_f:g}")
    sup = str.maketrans("0123456789.-", "⁰¹²³⁴⁵⁶⁷⁸⁹·⁻")
    log = f"log{b.translate(sup)}" if b and b not in ("0",) else ""
    return " ".join(x for x in (a_txt, log) if x) or "0"


class Analysis:
    def __init__(self, root: Path, site):
        path = root / "data" / "canonical" / "site_index.json"
        data = {}
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = {}
        self.site = site
        self.ok = bool(data.get("bounds") or data.get("cells"))
        nodes = site.nodes
        self.bounds = {b["id"]: b for b in data.get("bounds") or [] if b.get("setting_id") in nodes}
        self.by_setting: dict[str, list] = collections.defaultdict(list)
        for b in self.bounds.values():
            self.by_setting[b["setting_id"]].append(b)
        self.cells = [c for c in data.get("cells") or [] if c.get("setting_id") in nodes]
        self.cells_by_setting: dict[str, list] = collections.defaultdict(list)
        for c in self.cells:
            self.cells_by_setting[c["setting_id"]].append(c)
        self.cell_of = {(c["setting_id"], c["regime"]): c for c in self.cells}
        self.transfer = [t for t in data.get("transfer") or [] if t.get("setting_id") in nodes]
        self.transfer_of = {(t["setting_id"], t["regime"]): t for t in self.transfer}
        self.unstudied = data.get("unstudied") or []
        self.redundant = data.get("redundant") or []
        self.sliders = data.get("sliders") or ["T", "K", "d", "Delta", "delta", "epsilon"]
        self.defaults = data.get("slider_defaults") or {}
        self._tex: dict = {}

    # -- small lookups
    def bound(self, bid: str) -> dict | None:
        return self.bounds.get(strip_id(bid))

    @staticmethod
    def regime(b: dict) -> str:
        fam = b.get("family") or b.get("quantity") or "unknown"
        dep = "data_dependent" if DATA_DEPENDENT.search(str(b.get("expression") or "")) else (b.get("dependence") or "unknown")
        return f"{fam}|{dep}"

    def tex(self, b: dict) -> tuple[str, bool]:
        key = (b.get("expression"), b.get("notation"), b.get("side"), b.get("quantity"))
        if key not in self._tex:
            self._tex[key] = bounds.bound_tex({"expression": b.get("expression"), "notation": b.get("notation")},
                                              b.get("side"), b.get("quantity"))
        return self._tex[key]

    def setting_status(self, sid: str) -> tuple[str, str | None]:
        """Status shown for a setting: its best-populated regime (both sides present first, then
        most bounds; ties prefer regret|worst_case), so a setting with many instance-dependent upper
        bounds is not labelled "no upper bound" because its worst-case regime has only lower bounds."""
        cells = self.cells_by_setting.get(sid) or []
        if not cells:
            return "none", None
        c = min(cells, key=lambda c: (not (c["n_upper"] and c["n_lower"]), -(c["n_upper"] + c["n_lower"]),
                                      c["regime"] != "regret|worst_case", c["regime"]))
        return c["status"], c["regime"]

    # -- per-setting plot data (embedded in the setting page)
    def plot_data(self, n: dict) -> dict | None:
        bs = self.by_setting.get(n["id"]) or []
        if not bs:
            return None
        site = self.site
        cells = {c["regime"]: c for c in self.cells_by_setting.get(n["id"]) or []}
        fronts = {reg: set(c["upper_front"]) | set(c["lower_front"]) for reg, c in cells.items()}

        def entry(b: dict, reg: str, full_id: str, dsub: bool) -> dict:
            tex, ok = self.tex(b)
            src = site.nodes.get(b.get("from_setting") or "")
            alg = (site.algorithms.get(b.get("algorithm_id") or "") or {}).get("name") or b.get("algorithm_id")
            return {"id": full_id, "side": b["side"], "reg": reg, "nota": b.get("notation"),
                    "shape": bool(b.get("shape_only")), "inh": bool(b.get("inherited")),
                    "from": src["name"] if src else None, "fromSlug": src["slug"] if src else None,
                    "paper": b.get("paper"), "cite": site.cite(b.get("paper")), "year": b.get("year"),
                    "alg": alg, "js": b.get("js"), "tex": tex if ok else None, "expr": b.get("expression"),
                    "prof": b.get("profile"), "front": full_id in fronts.get(reg, ()), "dsub": dsub,
                    "restricted": bool(b.get("restricted")), "conf": b.get("confidence")}

        out = [entry(b, self.regime(b), b["id"], False) for b in bs]
        # High-probability bounds read in expectation with delta = 1/T (front ids "...@delta=1/T").
        for reg, c in cells.items():
            for bid in c["upper_front"] + c["lower_front"]:
                if "@" in bid and self.bound(bid):
                    out.append(entry(self.bound(bid), reg, bid, True))
        regs = collections.Counter(x["reg"] for x in out)
        order = sorted(regs, key=lambda r: (r != "regret|worst_case", r not in cells, -regs[r], r))
        return {
            "sliders": self.sliders, "defaults": self.defaults,
            "regimes": [{"key": r, "label": regime_label(r), "status": (cells.get(r) or {}).get("status"),
                         "statusLabel": STATUS.get((cells.get(r) or {}).get("status") or "", ("",))[0],
                         "perVar": (cells.get(r) or {}).get("per_var") or {}} for r in order],
            "bounds": out,
        }

    # -- search index (static/search-data.js)
    def search_data(self) -> dict:
        site = self.site
        settings, idx, labels = [], {}, {}
        for i, n in enumerate(sorted(site.nodes.values(), key=lambda n: (-len(n["papers"]), n["name"]))):
            idx[n["id"]] = i
            raw = n.get("raw") or {}
            facets = {}
            for d in SEARCH_DIMS:
                v = raw.get(d, n["key"].get(d))
                vals = [x for x in (v if isinstance(v, list) else [v]) if x not in (None, "")]
                facets[d] = [str(x) for x in vals] or ["none"]
                for x in facets[d]:
                    labels.setdefault(d, {})[x] = value_label(d, x)
            own = collections.Counter((it["r"].get("side") or "").lower() for it in n["results"])
            inh = {b["side"] for b in self.by_setting.get(n["id"]) or [] if b.get("inherited")}
            src = {s: ("own" if own.get(s) else "inherited" if s in inh else "none") for s in ("upper", "lower")}
            settings.append({"id": n["id"], "slug": n["slug"], "name": n["name"], "papers": len(n["papers"]),
                             "f": facets, "cells": {c["regime"]: c["status"] for c in self.cells_by_setting.get(n["id"]) or []},
                             "upSrc": src["upper"], "loSrc": src["lower"]})
        out_b = []
        for b in self.bounds.values():
            tex, ok = self.tex(b)
            alg = (site.algorithms.get(b.get("algorithm_id") or "") or {}).get("name") or b.get("algorithm_id")
            out_b.append({"s": idx[b["setting_id"]], "id": b["id"], "side": b["side"], "reg": self.regime(b),
                          "nota": b.get("notation") or "exact", "inh": bool(b.get("inherited")),
                          "p": b.get("paper"), "c": site.cite(b.get("paper")), "y": b.get("year"),
                          "af": b.get("algorithm_family") or "none", "a": alg, "conf": b.get("confidence") or "unknown",
                          "rs": bool(b.get("restricted")), "t": tex if ok else None, "e": None if ok else b.get("expression")})
        out_b.sort(key=lambda x: (x["s"], x["reg"], x["side"] != "upper", x["inh"], x["c"]))
        return {"settings": settings, "bounds": out_b, "labels": labels,
                "regimes": {r: regime_label(r) for r in sorted({x["reg"] for x in out_b} | {c["regime"] for c in self.cells})},
                "status": {k: v[0] for k, v in STATUS.items()}}


# ---------------------------------------------------------------- shared html


def status_badge(h, st: str | None, title: str = "") -> str:
    st = st or "none"
    lbl, hlp = STATUS.get(st, (st, ""))
    return h.badge(lbl, f"st st-{st}", title or hlp)


def triage_badge(h, tri: dict | None) -> str:
    if not tri:
        return h.badge("untriaged", "muted-badge", "no gap-triage verdict for this cell yet")
    v = tri.get("verdict") or "?"
    return h.badge(v.replace("_", " "), f"tri tri-{v}", TRIAGE.get(v, ""))


ANALYSIS_TABS = [("gaps.html", "Gaps", "gaps"), ("neighbours.html", "Unstudied neighbours", "neighbours"),
                 ("transfer.html", "Technique transfer", "transfer"), ("redundant.html", "Redundancy", "redundant"),
                 ("search.html", "Search", "search")]


def tabs(active: str) -> str:
    return ('<nav class="subnav" aria-label="Analysis">' + "".join(
        f'<a href="{href}"{" aria-current=page" if key == active else ""}>{lbl}</a>' for href, lbl, key in ANALYSIS_TABS)
        + "</nav>")


def no_data(h, title: str, active: str, nav: str) -> str:
    body = (f"{tabs(active)}<h1>{h.e(title)}</h1><p class=\"notice\">No analysis data yet: "
            "<code>data/canonical/site_index.json</code> is missing (run <code>pipeline/site_index.py</code>).</p>")
    return h.page(title, body, "", nav)


class Pages:
    def __init__(self, site, A: Analysis, h):
        self.site, self.A, self.h = site, A, h

    def setting_link(self, sid: str, root: str = "") -> str:
        n = self.site.nodes.get(sid)
        if not n:
            return f"<code>{self.h.e(sid)}</code>"
        return f'<a href="{root}settings/{n["slug"]}.html">{self.h.e(n["name"])}</a>'

    def bound_line(self, bid: str, root: str = "", show_from: bool = True) -> str:
        h, b = self.h, self.A.bound(bid)
        if not b:
            return f"<code>{h.e(bid)}</code>"
        tex, ok = self.A.tex(b)
        f = f'<div class="formula">{h.math(tex)}</div>' if ok else f'<div class="formula"><code>{h.e(str(b.get("expression")))}</code></div>'
        bits = [h.paper_html(self.site, b["paper"], root)]
        alg = (self.site.algorithms.get(b.get("algorithm_id") or "") or {}).get("name")
        if alg:
            bits.append(f'<span class="alg">{h.e(h.short(alg))}</span>')
        if "@" in bid:
            bits.append(h.badge("w.h.p., δ = 1/T", "prob", "high-probability bound read in expectation with δ = 1/T"))
        if b.get("inherited") and show_from and b.get("from_setting") in self.site.nodes:
            src = self.site.nodes[b["from_setting"]]
            nm = src["name"] if len(src["name"]) <= 60 else src["name"][:59].rstrip() + "…"
            bits.append(f'<span class="muted">inherited from <a href="{root}settings/{src["slug"]}.html" '
                        f'title="{h.e(src["name"], quote=True)}">{h.e(nm)}</a></span>')
        return f'<div class="bl">{f}<div class="small bl-meta">{" · ".join(bits)}</div></div>'

    def front_html(self, ids: list[str], root: str = "", keep: int = 2) -> str:
        if not ids:
            return '<span class="muted small">none</span>'
        # One line per distinct (paper, expression): fronts often list the same bound via several sources.
        seen, uniq = set(), []
        for bid in ids:
            b = self.A.bound(bid) or {}
            k = (b.get("paper"), b.get("expression"), "@" in bid)
            if k not in seen:
                seen.add(k)
                uniq.append(bid)
        head = "".join(self.bound_line(x, root) for x in uniq[:keep])
        if len(uniq) > keep:
            head += f'<div class="small muted">+{len(uniq) - keep} more with the same rate (see the setting page)</div>'
        return head

    def per_var_html(self, per_var: dict) -> str:
        h = self.h
        if not per_var:
            return ""
        out = []
        for v, x in per_var.items():
            st = x.get("status") or ""
            sym = {"Delta": "1/Δ", "delta": "1/δ", "epsilon": "1/ε"}.get(v, v)
            out.append(f'<span class="pv pv-{h.e(st)}" title="{h.e(STATUS.get(st, (st,))[0], quote=True)}">'
                       f'<b>{h.e(sym)}</b> ↑{h.e(rate_str(x.get("upper")))} ↓{h.e(rate_str(x.get("lower")))}</span>')
        return '<div class="pvs">' + "".join(out) + "</div>"

    # ------------------------------------------------------------ gaps.html
    def gaps_page(self) -> str:
        h, A, site = self.h, self.A, self.site
        if not A.ok:
            return no_data(h, "Gaps", "gaps", "gaps")
        cells = [c for c in A.cells if c["status"] in GAP_STATUSES]
        sev = {"conflict": 0, "poly_gap": 1, "log_gap": 2, "no_lower": 3, "no_upper": 4}
        # default: real gaps first (poly, log, conflicts), then missing bounds; papers break ties
        cells.sort(key=lambda c: (sev[c["status"]], -len(site.nodes[c["setting_id"]]["papers"]), c["regime"]))
        counts = collections.Counter(c["status"] for c in cells)
        regimes = collections.Counter(c["regime"] for c in cells)
        acts = collections.Counter(self._dimval(c["setting_id"], "action_space") for c in cells)
        envs = collections.Counter(self._dimval(c["setting_id"], "environment") for c in cells)
        tris = collections.Counter(((c.get("triage") or {}).get("verdict") or "untriaged") for c in cells)

        def sel(name, label, counter, labels=None):
            opts = "".join(f'<option value="{h.e(k, quote=True)}">{h.e((labels or {}).get(k, k))} ({v})</option>'
                           for k, v in sorted(counter.items(), key=lambda t: -t[1]))
            return (f'<label class="fsel"><span>{h.e(label)}</span><select data-facet="{name}">'
                    f'<option value="">all</option>{opts}</select></label>')

        cards = []
        for c in cells:
            sid, n = c["setting_id"], site.nodes[c["setting_id"]]
            tri = c.get("triage")
            tr = A.transfer_of.get((sid, c["regime"]))
            tr_html = ""
            if tr:
                items = []
                for s in tr["suggestions"]:
                    ev = s["evidence"][0]
                    more = f' <span class="muted">+{len(s["evidence"]) - 1}</span>' if len(s["evidence"]) > 1 else ""
                    items.append(f'<li><b>{h.e(h.label(s["family"]))}</b> <span class="muted">reaches the best upper bound in</span> '
                                 f'{self.setting_link(ev["neighbour"])} {status_badge(h, ev["neighbour_status"])}{more}</li>')
                tr_html = f'<div class="tr"><span class="side">Try (technique transfer)</span><ul class="tight">{"".join(items)}</ul></div>'
            tri_html = ""
            if tri:
                papers = "".join(
                    f'<li><b>{h.e(str(p.get("title") or ""))}</b> ({h.e(str(p.get("year") or ""))})'
                    + (f' <a href="https://arxiv.org/abs/{h.e(str(p["arxiv_id"]), quote=True)}">arXiv:{h.e(str(p["arxiv_id"]))}</a>' if p.get("arxiv_id") else "")
                    + (f'<div class="small muted">{h.e(str(p.get("claim") or ""))}</div>' if p.get("claim") else "") + "</li>"
                    for p in tri.get("papers") or [])
                tri_html = (f'<details class="more tri-d"><summary>triage: {h.e(TRIAGE.get(tri.get("verdict"), ""))}</summary>'
                            f'<p class="small">{h.e(str(tri.get("summary") or ""))}</p>'
                            + (f'<ul class="tight small">{papers}</ul>' if papers else "") + "</details>")
            inh = h.badge("relies on inherited", "inh", "a best bound here is inherited, not proved for this setting") if c.get("relies_on_inherited") else ""
            cards.append(f"""<article class="gap" data-status="{c['status']}" data-papers="{len(n['papers'])}" data-sev="{sev[c['status']]}" data-regime="{h.e(c['regime'], quote=True)}"
 data-action="{h.e(self._dimval(sid, 'action_space'), quote=True)}" data-env="{h.e(self._dimval(sid, 'environment'), quote=True)}"
 data-triage="{h.e((tri or {}).get('verdict') or 'untriaged', quote=True)}">
<header>{status_badge(h, c['status'])} {h.badge(regime_label(c['regime']), 'reg')} {triage_badge(h, tri)} {inh}
<span class="muted small gap-n">{len(n['papers'])} paper{'s' if len(n['papers']) != 1 else ''} · {c['n_upper']}↑ {c['n_lower']}↓</span></header>
<h3><a href="settings/{n['slug']}.html#rates">{h.e(n['name'])}</a></h3>
{self.per_var_html(c.get('per_var') or {})}
<div class="ul2"><div><span class="side">Best upper</span>{self.front_html(c['upper_front'])}</div>
<div><span class="side">Best lower</span>{self.front_html(c['lower_front'])}</div></div>
{tr_html}{tri_html}
</article>""")
        chips = " ".join(f'<button type="button" class="stchip" data-set-facet="status" data-value="{s}">{status_badge(h, s)} {counts[s]}</button>'
                         for s in GAP_STATUSES if counts[s])
        n_tri = sum(1 for c in cells if c.get("triage"))
        body = f"""{tabs("gaps")}
<h1>Gaps</h1>
<p class="lede">Per setting and regime (quantity family × dependence), the best upper and best lower bounds are compared by
their growth exponents in T, K, d and 1/Δ (<code>pipeline/compare.py</code>). Cells that are not tight are listed here,
most-studied settings first, then by gap size. <b>Rates</b> read ↑ upper / ↓ lower exponent, so <i>T</i> ↑0.5 ↓0.5 is √T
on both sides. A gap is only called open after gap triage; {n_tri} of {len(cells)} cells have a verdict.</p>
<p class="stchips">{chips} <button type="button" class="stchip" data-set-facet="status" data-value="">show all</button></p>
<div class="facetbar" data-target="gap-list">
{sel("status", "Status", counts, {k: v[0] for k, v in STATUS.items()})}
{sel("regime", "Regime", regimes, {k: regime_label(k) for k in regimes})}
{sel("action", "Action space", acts)}
{sel("env", "Environment", envs)}
{sel("triage", "Triage", tris)}
<label class="fsel"><span>Sort</span><select data-sort><option value="sev">gap size, then papers</option>
<option value="papers">papers, then gap size</option></select></label>
<input class="filter" type="search" data-facet-text placeholder="Filter by setting, paper…" aria-label="Filter">
<span class="muted small" data-count></span>
</div>
<div class="gaps" id="gap-list">{"".join(cards)}</div>"""
        return h.page("Gaps", body, "", "gaps", head='<script defer src="static/analysis.js"></script>', wide=True)

    def _dimval(self, sid: str, dim: str) -> str:
        v = self.site.nodes[sid]["key"].get(dim, "")
        return value_label(dim, v) if v else "unspecified"

    # ------------------------------------------------------------ neighbours.html
    def neighbours_page(self) -> str:
        h, A = self.h, self.A
        if not A.ok:
            return no_data(h, "Unstudied neighbours", "neighbours", "analysis")
        rows = []
        for u in sorted(A.unstudied, key=lambda u: (-u.get("score", 0), u.get("label", ""))):
            src = []
            for f in u.get("from") or []:
                d = f.get("dim", "")
                arrow = "generalises" if f.get("direction") == "generalise" else "specialises" if f.get("direction") == "specialise" else h.e(str(f.get("direction") or ""))
                src.append(f'<li>{self.setting_link(f["setting_id"])}<div class="chg"><span class="dim">{h.e(dim_label(d))}</span> '
                           f'{h.e(value_label(d, f.get("from")) if f.get("from") else "none")} <span class="arrow">→</span> '
                           f'{h.e(value_label(d, f.get("to")) if f.get("to") else "none")} <span class="muted">({arrow})</span></div></li>')
            rows.append([f'<b>{h.e(self._pretty_label(u))}</b>', f'<span class="num">{h.e(str(u.get("score", "")))}</span>',
                         f'<ul class="nb">{"".join(src)}</ul>'])
        body = (f'{tabs("neighbours")}<h1>Unstudied neighbours</h1>'
                f'<p class="lede">{len(rows)} assumption vectors one order step away from an extracted setting (one dimension '
                'moved to an adjacent value) with no extracted results. <b>Score</b> ranks them by how well studied their '
                'neighbours are; combinations flagged ill-posed are skipped. Each is a candidate research question '
                '(motivation 2): a result here would also transfer to the neighbours.</p>'
                + h.table(["Unstudied setting", "Score", "Next to (studied)"], rows, "neigh", filterable=True))
        return h.page("Unstudied neighbours", body, "", "analysis")

    def _pretty_label(self, u: dict) -> str:
        key = u.get("key")
        if isinstance(key, dict):
            try:
                return self.h.setting_name(self.h.flat_key(key, self.site.onto.dims, include=("learner_knows", "parameters")))
            except Exception:  # noqa: BLE001
                pass
        return str(u.get("label") or "")

    # ------------------------------------------------------------ transfer.html
    def transfer_page(self) -> str:
        h, A = self.h, self.A
        if not A.ok:
            return no_data(h, "Technique transfer", "transfer", "analysis")
        by_fam: dict[str, list] = collections.defaultdict(list)
        for t in A.transfer:
            for s in t["suggestions"]:
                by_fam[s["family"]].append((t, s))
        secs = []
        for fam, items in sorted(by_fam.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            lis = []
            for t, s in sorted(items, key=lambda ts: (GAP_STATUSES.index(ts[0]["status"]) if ts[0]["status"] in GAP_STATUSES else 9,
                                                      -len(self.site.nodes[ts[0]["setting_id"]]["papers"]))):
                ev = "".join(f'<li>{self.setting_link(x["neighbour"])} {status_badge(h, x["neighbour_status"])}'
                             f'{self.bound_line(x["bound"], show_from=False)}</li>' for x in s["evidence"])
                here = ", ".join(h.label(f) for f in t.get("families_here") or []) or "none"
                lis.append(f"""<article class="gap">
<header>{status_badge(h, t['status'])} {h.badge(regime_label(t['regime']), 'reg')}</header>
<h3><a href="settings/{self.site.nodes[t['setting_id']]['slug']}.html#rates">{h.e(self.site.nodes[t['setting_id']]['name'])}</a></h3>
<p class="small muted">Families with an upper bound here: {h.e(here)}</p>
<span class="side">Evidence: best upper bound in a neighbouring setting (same regime)</span><ul class="ev">{ev}</ul>
</article>""")
            secs.append(f'<section class="fam" id="fam-{h.slugify(fam)}"><h2>{h.e(h.label(fam))} '
                        f'<span class="muted">({len(items)} setting{"s" if len(items) != 1 else ""})</span></h2>'
                        f'<div class="gaps">{"".join(lis)}</div></section>')
        toc = " · ".join(f'<a href="#fam-{h.slugify(f)}">{h.e(h.label(f))}</a> ({len(v)})'
                         for f, v in sorted(by_fam.items(), key=lambda kv: (-len(kv[1]), kv[0])))
        body = (f'{tabs("transfer")}<h1>Technique transfer</h1>'
                '<p class="lede">For a setting with a gap or no upper bound: algorithm families that achieve the best upper '
                'bound in a neighbouring setting (one covering step, same regime, tight or log gap there) but do not appear '
                'among this setting\'s upper bounds (motivation 3). Grouped by family.</p>'
                + (f'<p class="crumbs">{toc}</p>' if toc else "") + ("".join(secs) or '<p class="muted">No suggestions.</p>'))
        return h.page("Technique transfer", body, "", "analysis", wide=True)

    # ------------------------------------------------------------ redundant.html
    def redundant_page(self) -> str:
        h, A = self.h, self.A
        if not A.ok:
            return no_data(h, "Redundancy", "redundant", "analysis")
        by_label = {}
        for n in self.site.nodes.values():
            by_label[str(n.get("label") or "")] = n
        papers = set(self.site.paper_ids()) | {b["paper"] for b in A.bounds.values()}
        items = []
        for md in A.redundant:
            items.append(f"<li>{self._md(md, by_label, papers)}</li>")
        body = (f'{tabs("redundant")}<h1>Redundancy</h1>'
                f'<p class="lede">{len(items)} extracted results whose rate an <em>earlier</em> paper already implied, via a bound '
                'inherited along the specialisation order (motivation 4). Not necessarily redundant work: the later result may '
                'have better constants, a simpler algorithm or weaker assumptions; but the rate was not new.</p>'
                + h.filter_box("Filter…") + f'<ul class="redund filterable-cards">{"".join(items)}</ul>')
        return h.page("Redundancy", body, "", "analysis")

    def _md(self, md: str, by_label: dict, papers: set) -> str:
        h = self.h
        out = []
        # setting labels can contain " (" themselves: take the longest label the line starts with
        head = max((lb for lb in by_label if lb and md.startswith(lb + " (")), key=len, default=None)
        if head:
            n = by_label[head]
            out.append(f'<a href="settings/{n["slug"]}.html">{h.e(n["name"])}</a> (')
            md = md[len(head) + 2:]
        for i, part in enumerate(md.split("`")):
            if i % 2:
                try:
                    out.append(h.math(bounds.expr_tex(part)))
                except Exception:  # noqa: BLE001
                    out.append(f"<code>{h.e(part)}</code>")
            else:
                t = h.e(part)
                t = re.sub(r"\b([a-z][a-z0-9]*\d{4}[a-z0-9]*)\b",
                           lambda m: f'<a href="papers/{h.slugify(m.group(1))}.html">{m.group(1)}</a>' if m.group(1) in papers else m.group(1), t)
                t = t.replace(" — already implied by ", '<br><span class="muted">already implied by</span> ')
                out.append(t)
        return "".join(out)

    # ------------------------------------------------------------ search.html
    def search_page(self) -> str:
        h, A = self.h, self.A
        if not A.ok:
            return no_data(h, "Search", "search", "search")
        saved = [
            ("Adversarial settings with no lower bound",
             "mode=settings&environment=adversarial_unspecified,adversarial_oblivious,adversarial_adaptive,"
             "adversarial_self_bounding,adversarial_restricted&cell=no_lower&regime=regret|worst_case"),
            ("Tight results", "mode=settings&cell=tight"),
            ("Log gaps in linear bandits", "mode=settings&cell=log_gap&action_space=linear_finite,linear_infinite,generalized_linear"),
            ("Settings whose lower bounds are all inherited", "mode=settings&loSrc=inherited"),
            ("Inherited lower bounds", "mode=bounds&side=lower&origin=inherited"),
            ("Low-confidence own upper bounds", "mode=bounds&side=upper&origin=own&conf=low"),
            ("Thompson sampling, since 2015", "mode=bounds&af=thompson_sampling&ymin=2015"),
        ]
        links = "".join(f'<li><a href="#{q}">{h.e(t)}</a></li>' for t, q in saved)
        body = f"""{tabs("search")}
<h1>Search</h1>
<p class="lede small">Faceted search over settings (assumption dimensions, per-regime status) and bounds (side, regime,
notation, algorithm family, paper, year, own/inherited, confidence). Facets combine with AND, values within a facet with OR;
the query lives in the URL, so it can be shared.</p>
<div class="saved"><span class="muted small">Saved queries:</span><ul>{links}</ul></div>
<div class="search" id="search"><p class="muted">Loading…</p></div>"""
        head = '<script defer src="static/search-data.js"></script>\n<script defer src="static/search.js"></script>'
        return h.page("Search", body, "", "search", head=head, wide=True)
