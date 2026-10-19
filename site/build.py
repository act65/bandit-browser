#!/usr/bin/env python3
"""Build the static bandit-browser site into _site/.

Usage:
    uv run python site/build.py              # real data
    uv run python site/build.py --fixtures   # site/fixtures/ test data
    ... [--out DIR]

Inputs (all optional; missing files/dirs are treated as empty):
    corpus/manifest.yaml
    data/canonical/{settings,results,algorithms}.json   canonical layer (pipeline/resolve.py);
                                                         if absent, settings are grouped from
    data/extractions/<paper_id>.json                     the raw extractions instead
    data/algorithms.yaml                                 algorithm registry (raw mode)
    data/ground_truth/{bco,pilot-facts}.yaml
    ontology/bandits-<highest version>.yaml, ontology/variables.yaml

Modules: ontology.py (dimensions, names, orders), bounds.py (SymPy -> LaTeX).
Display only: no bound comparison or inference happens here.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

import bounds  # noqa: E402
from ontology import (QUANTITY_LABEL, Ontology, dim_label, is_default, value_label)  # noqa: E402

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
CYTOSCAPE = "https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.30.2/cytoscape.min.js"
DAGRE = "https://cdnjs.cloudflare.com/ajax/libs/dagre/0.8.5/dagre.min.js"
CY_DAGRE = "https://cdn.jsdelivr.net/npm/cytoscape-dagre@2.5.0/cytoscape-dagre.min.js"
REPO_URL = "https://github.com/act65/bandit-browser"

# Order of dimensions in human-readable setting names (others follow in ontology order).
NAME_ORDER = ["objective", "environment", "action_space", "feedback", "context", "function_class", "domain",
              "noise", "instance_assumptions", "extras"]
TRAILING = ["learner_knows", "parameters"]  # always last in names

e = html.escape


# ---------------------------------------------------------------- loading


def warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


def load_yaml(path: Path):
    if not path.is_file():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        warn(f"could not parse {path}: {exc}")
        return None


def load_json(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        warn(f"could not parse {path}: {exc}")
        return None


def load_manifest(root: Path) -> list[dict]:
    data = load_yaml(root / "corpus" / "manifest.yaml") or {}
    papers = data.get("papers") if isinstance(data, dict) else None
    return [p for p in (papers or []) if isinstance(p, dict) and p.get("id")]


def load_extractions(root: Path) -> dict[str, dict]:
    out = {}
    d = root / "data" / "extractions"
    for f in sorted(d.glob("*.json")) if d.is_dir() else []:
        data = load_json(f)
        if isinstance(data, dict):
            out[f.stem] = data
    return out


def listify(data, key: str) -> list:
    if isinstance(data, dict):
        data = data.get(key)
    return [x for x in data or [] if isinstance(x, dict)] if isinstance(data, list) else []


# ---------------------------------------------------------------- small helpers


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", str(s).lower()).strip("-") or "x"


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


NONE = '<span class="muted">–</span>'


def text(v) -> str:
    if v is None or v == "" or v == [] or v == {}:
        return NONE
    if isinstance(v, list):
        return ", ".join(e(str(x)) for x in v) or NONE
    if isinstance(v, dict):
        return ", ".join(f"{e(str(k))}={e(str(x))}" for k, x in v.items())
    if isinstance(v, bool):
        return "yes" if v else "no"
    return e(str(v))


def math(tex, cls: str = "") -> str:
    """Span rendered client-side by KaTeX; shows the raw TeX if JS is off."""
    t = str(tex)
    return f'<span class="math {cls}" data-tex="{e(t, quote=True)}">{e(t)}</span>'


def label(s) -> str:
    return str(s or "").replace("_", " ")


def badge(txt: str, cls: str = "", title: str = "") -> str:
    t = f' title="{e(title, quote=True)}"' if title else ""
    return f'<span class="badge {cls}"{t}>{e(txt)}</span>'


def short(s: str, n: int = 30) -> str:
    s = re.split(r"\s+\(", s, maxsplit=1)[0].strip() or s
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def surname(author: str) -> str:
    a = str(author).strip()
    if "," in a:
        return a.split(",")[0].strip()
    parts = a.split()
    return parts[-1] if parts else a


# ---------------------------------------------------------------- setting keys


def flat_value(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return "+".join(sorted(map(str, v)))
    if isinstance(v, dict):
        return ", ".join(f"{k}={v[k]}" for k in sorted(v))
    return str(v)


def flat_key(raw: dict, dims: list[str], include: tuple = ()) -> dict[str, str]:
    """Assumption vector -> ordered {dimension: value-string}; node parameters split by field."""
    out = {d: flat_value(raw.get(d)) for d in dims}
    out["extras"] = flat_value(raw.get("extras"))
    for k, v in raw.items():
        if k in out or k in ("learner_knows", "parameters") and k not in include:
            continue
        if isinstance(v, dict) and k != "parameters":
            for f, x in v.items():
                out[f"{k}.{f}"] = flat_value(x)
        elif k in include or k in dims:
            out[k] = flat_value(v)
    for k in include:
        out.setdefault(k, flat_value(raw.get(k)))
    return out


GREEK_TEXT = {"sigma": "σ", "Delta": "Δ", "mu": "μ", "alpha": "α", "beta": "β", "gamma": "γ", "lam": "λ",
              "epsilon": "ε", "delta": "δ", "theta": "θ", "star": "*"}


def pretty_vars(s: str) -> str:
    """'Delta_min, sigma' -> 'Δ_min, σ' for names (plain text, not LaTeX)."""
    return re.sub(r"[A-Za-z]+", lambda m: GREEK_TEXT.get(m.group(0), m.group(0)), s).replace("_*", "*")


def setting_name(key: dict[str, str]) -> str:
    order = [d for d in NAME_ORDER if d in key] + [d for d in key if d not in NAME_ORDER and d not in TRAILING]
    bits = []
    for d in order:
        v = key[d]
        if is_default(d, v):
            continue
        if d in ("function_class", "instance_assumptions", "extras"):
            bits.append(value_label(d, v.split("+")))
        elif d.startswith("action_set."):
            bits.append(f"{value_label(d, v)} {d.split('.', 1)[1].replace('_', ' ')}")
        else:
            bits.append(value_label(d, v))
    if key.get("learner_knows"):
        bits.append("knows " + pretty_vars(", ".join(key["learner_knows"].split("+"))))
    if key.get("parameters"):
        bits.append(pretty_vars(key["parameters"].replace("=>=", " ≥ ").replace("=", " = ")))
    return " · ".join(bits) or "unspecified"


# ---------------------------------------------------------------- model


class Site:
    def __init__(self, root: Path):
        self.root = root
        self.onto = Ontology(root / "ontology", REPO / "ontology")
        var_file = root / "ontology" / "variables.yaml"
        bounds.load_variables(var_file if var_file.is_file() else REPO / "ontology" / "variables.yaml")
        self.manifest_list = load_manifest(root)
        self.manifest = {p["id"]: p for p in self.manifest_list}
        self.extractions = load_extractions(root)
        self.bco = load_yaml(root / "data" / "ground_truth" / "bco.yaml")
        self.facts = load_yaml(root / "data" / "ground_truth" / "pilot-facts.yaml")
        canon = root / "data" / "canonical"
        self.canonical = (canon / "settings.json").is_file() and (canon / "results.json").is_file()
        algs = listify(load_json(canon / "algorithms.json"), "algorithms") or \
            listify(load_yaml(root / "data" / "algorithms.yaml"), "algorithms")
        self.algorithms = {a["id"]: a for a in algs if a.get("id")}
        self.nodes: dict[str, dict] = {}
        self.local_to_node: dict[tuple[str, str], str] = {}
        if self.canonical:
            self._load_canonical(canon)
        else:
            self._load_raw()
        for n in self.nodes.values():
            n["name"] = setting_name(n["key"])
            n["papers"] = sorted({m[0] for m in n["members"]} | {it["paper"] for it in n["results"]})
        self._dedupe_names()
        self.edges = self._edges()

    # -- canonical layer (preferred)
    def _load_canonical(self, canon: Path) -> None:
        for s in listify(load_json(canon / "settings.json"), "settings"):
            if s.get("in_scope") is False or not s.get("id"):
                continue
            key = flat_key(s.get("key") or {}, self.onto.dims, include=("learner_knows", "parameters"))
            members = [(m.get("paper"), m.get("local_id"), m.get("name_in_paper")) for m in listify(s, "members")]
            self.nodes[s["id"]] = {"id": s["id"], "slug": s["id"] if re.fullmatch(r"[A-Za-z0-9_.-]+", s["id"]) else slugify(s["id"]), "key": key, "label": s.get("label"),
                                   "members": members, "results": []}
            for pid, lid, _ in members:
                self.local_to_node[(pid, lid)] = s["id"]
        for r in listify(load_json(canon / "results.json"), "results"):
            nid = r.get("setting_id")
            if nid not in self.nodes:
                continue
            self.nodes[nid]["results"].append(self._item(r.get("paper"), r, nid))

    # -- raw extractions (fixtures, or before pipeline/resolve.py has run)
    def _load_raw(self) -> None:
        for pid, ex in self.extractions.items():
            settings = {s.get("id"): s for s in listify(ex, "settings")}
            for sid, s in settings.items():
                if s.get("in_scope") is False:
                    continue
                key = flat_key(s, self.onto.dims)
                nid = slugify("--".join(v or "none" for v in key.values()))
                node = self.nodes.setdefault(nid, {"id": nid, "slug": nid, "key": key, "label": None,
                                                   "members": [], "results": []})
                node["members"].append((pid, sid, s.get("name_in_paper")))
                self.local_to_node[(pid, sid)] = nid
            for r in listify(ex, "results"):
                nid = self.local_to_node.get((pid, r.get("setting")))
                if nid is None:
                    if r.get("setting") in settings and settings[r.get("setting")].get("in_scope") is False:
                        continue
                    warn(f"{pid}: result {r.get('id')} references unknown setting {r.get('setting')}")
                    continue
                self.nodes[nid]["results"].append(self._item(pid, r, nid))

    def _item(self, pid: str, r: dict, nid: str | None) -> dict:
        ex = self.extractions.get(pid) or {}
        local_algs = {a.get("id"): a for a in listify(ex, "algorithms")}
        local_set = {s.get("id"): s for s in listify(ex, "settings")}
        reg = self.algorithms.get(r.get("algorithm_id") or "")
        loc = local_algs.get(r.get("algorithm"))
        full = (reg or {}).get("name") or (loc or {}).get("name") or (loc or {}).get("id")
        aliases = [a for a in as_list((reg or {}).get("aliases")) if a != full]
        knows = (local_set.get(r.get("setting")) or {}).get("learner_knows")
        if knows is None and nid in self.nodes:
            knows = [x for x in self.nodes[nid]["key"].get("learner_knows", "").split("+") if x]
        return {"paper": pid, "r": r, "node": nid, "alg": full, "alg_aliases": aliases, "knows": knows}

    def _dedupe_names(self) -> None:
        seen: dict[str, list] = {}
        for n in self.nodes.values():
            seen.setdefault(n["name"], []).append(n)
        for name, ns in seen.items():
            if len(ns) > 1:
                for n in ns:
                    n["name"] = f"{name} [{n['id'][:10]}]"

    # -- neighbourhood structure
    def _edges(self) -> list[dict]:
        ids = sorted(self.nodes)
        out = []
        for i, a in enumerate(ids):
            ka = self.nodes[a]["key"]
            for b in ids[i + 1:]:
                kb = self.nodes[b]["key"]
                diff = [d for d in dict.fromkeys(list(ka) + list(kb)) if ka.get(d, "") != kb.get(d, "")]
                if not diff:
                    continue
                rels = [self.onto.relation(d, ka.get(d, ""), kb.get(d, "")) for d in diff]
                if len(diff) == 1 and rels[0] is None:
                    d = diff[0]
                    out.append({"source": a, "target": b, "kind": "neighbour", "dim": d,
                                "from": ka.get(d, ""), "to": kb.get(d, ""), "changes": [(d, ka.get(d, ""), kb.get(d, ""))]})
                    continue
                # Product order (D1): a ⊑ b iff every differing dimension is ordered a ⊑ b.
                if any(r is None for r in rels) or len({r[1] for r in rels}) != 1:
                    continue
                a_le_b = rels[0][1]
                kind = "reduction" if any(r[0] == "reduction" for r in rels) else "order"
                s, tg, ks, kt = (a, b, ka, kb) if a_le_b else (b, a, kb, ka)
                changes = [(d, ks.get(d, ""), kt.get(d, "")) for d in diff]
                out.append({"source": s, "target": tg, "kind": kind, "dim": diff[0],
                            "from": changes[0][1], "to": changes[0][2], "changes": changes})
        return out

    def hasse(self) -> list[dict]:
        """Edges with transitive specialisation edges removed (for drawing). Cached."""
        if getattr(self, "_hasse", None) is None:
            self._hasse = self._compute_hasse()
        return self._hasse

    def _compute_hasse(self) -> list[dict]:
        directed = [x for x in self.edges if x["kind"] != "neighbour"]
        succ: dict[str, set] = {}
        for x in directed:
            succ.setdefault(x["source"], set()).add(x["target"])

        def reachable(s, t, skip):
            stack, seen = [y for y in succ.get(s, ()) if (s, y) != skip], set()
            while stack:
                y = stack.pop()
                if y == t:
                    return True
                if y not in seen:
                    seen.add(y)
                    stack += succ.get(y, ())
            return False

        keep = [x for x in directed if not reachable(x["source"], x["target"], (x["source"], x["target"]))]
        return keep + [x for x in self.edges if x["kind"] == "neighbour"]

    def paper_ids(self) -> list[str]:
        ids = [p["id"] for p in self.manifest_list]
        return ids + [pid for pid in self.extractions if pid not in self.manifest]

    def paper_info(self, pid: str) -> dict:
        p = (self.extractions.get(pid) or {}).get("paper") or {}
        m = self.manifest.get(pid, {})
        return {**{k: v for k, v in p.items() if v is not None}, **{k: v for k, v in m.items() if v is not None}}

    def cite(self, pid: str) -> str:
        info = self.paper_info(pid)
        authors = as_list(info.get("authors"))
        year = info.get("year") or ""
        if not authors:
            return pid
        first = surname(authors[0])
        who = first if len(authors) == 1 else f"{first} & {surname(authors[1])}" if len(authors) == 2 else f"{first} et al."
        return f"{who} {year}".strip()

    def title(self, pid: str) -> str:
        return self.paper_info(pid).get("title") or pid

    def counts(self, n: dict) -> tuple[int, int]:
        up = sum(1 for it in n["results"] if (it["r"].get("side") or "").lower() == "upper")
        lo = sum(1 for it in n["results"] if (it["r"].get("side") or "").lower() == "lower")
        return up, lo


# ---------------------------------------------------------------- page shell

NAV = [
    ("index.html", "Home", "home"),
    ("graph.html", "Graph", "graph"),
    ("settings/index.html", "Settings", "settings"),
    ("papers/index.html", "Papers", "papers"),
    ("ground-truth.html", "Ground truth", "gt"),
    ("pilot-facts.html", "Pilot facts", "facts"),
]


def page(title: str, body: str, root: str, active: str = "", head: str = "", wide: bool = False) -> str:
    links = "".join(
        f'<a href="{root}{href}"{" aria-current=page" if key == active else ""}>{lbl}</a>'
        for href, lbl, key in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · bandit-browser</title>
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<link rel="stylesheet" href="{root}static/style.css">
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{root}static/site.js"></script>
{head}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{root}index.html"><span class="logo" aria-hidden="true">◆</span> bandit-browser</a>
<nav>{links}</nav>
</div></header>
<main class="wrap{' wide' if wide else ''}">
{body}
</main>
<footer class="wrap">Generated from plain data files by <code>site/build.py</code>.
Results are extracted by an LLM and are not human-verified unless stated. ·
<a href="{REPO_URL}">Source and data</a></footer>
</body>
</html>
"""


def filter_box(placeholder: str = "Filter…") -> str:
    return f'<input class="filter" type="search" placeholder="{e(placeholder)}" aria-label="Filter rows">'


def table(headers: list[str], rows: list[list[str]], cls: str = "", filterable: bool = False) -> str:
    if not rows:
        return '<p class="muted">None.</p>'
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "\n".join(
        "<tr>" + "".join(f'<td data-label="{e(re.sub("<[^>]+>", "", h), quote=True)}">{c}</td>'
                         for h, c in zip(headers, r)) + "</tr>"
        for r in rows
    )
    tbl = f'<div class="scroll"><table class="{cls}{" filterable" if filterable else ""}"><thead><tr>{th}</tr></thead><tbody>\n{trs}\n</tbody></table></div>'
    return (filter_box() + tbl) if filterable else tbl


def dl(pairs: list[tuple[str, str]], cls: str = "") -> str:
    return f'<dl class="{cls}">' + "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in pairs) + "</dl>"


# ---------------------------------------------------------------- generic renderer (ground truth)


def flatten(d: dict, prefix: str = "") -> dict:
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def cell(key: str, v) -> str:
    if key.split(".")[-1].endswith("_latex") and isinstance(v, str):
        return math(v)
    if isinstance(v, list) and v and any(isinstance(x, (dict, list)) for x in v):
        return generic(v)
    if isinstance(v, str) and len(v) > 160:
        return f'<details class="clip"><summary>{e(v[:70])}…</summary><div>{e(v)}</div></details>'
    return text(v)


def generic(v) -> str:
    """Render arbitrary YAML: list of dicts -> table; dict -> dl; scalars -> text."""
    if isinstance(v, dict):
        if v and all(isinstance(x, dict) for x in v.values()):
            return generic([{"id": k, **x} for k, x in v.items()])
        return dl([(str(k), cell(str(k), x) if not isinstance(x, dict) else generic(x)) for k, x in v.items()])
    if isinstance(v, list):
        if v and all(isinstance(x, dict) for x in v):
            rows = [flatten(x) for x in v]
            cols: list[str] = []
            for r in rows:
                cols += [c for c in r if c not in cols]
            return table([e(c) for c in cols], [[cell(c, r.get(c)) for c in cols] for r in rows],
                         "generic", filterable=True)
        if all(not isinstance(x, (dict, list)) for x in v):
            return "<ul>" + "".join(f"<li>{e(str(x))}</li>" for x in v) + "</ul>"
        return "<ul>" + "".join(f"<li>{generic(x)}</li>" for x in v) + "</ul>"
    return text(v)


# ---------------------------------------------------------------- bounds and result tables

DEPENDENCE = {"instance_dependent": ("instance-dependent", "inst"), "worst_case": ("worst-case", "worst")}
PROBABILITY = {"high_probability": "w.h.p.", "expectation": "in expectation", "asymptotic": "asymptotic",
               "almost_sure": "a.s."}
HORIZON = {"anytime": "anytime", "known": "known T"}


def bound_html(r: dict) -> str:
    b = r.get("bound") or {}
    tex, ok = bounds.bound_tex(b, r.get("side"), r.get("quantity"))
    if ok:
        return f'<div class="formula">{math(tex)}</div>'
    if b.get("expression_latex"):
        return (f'<div class="formula fallback" title="Canonical expression could not be parsed; '
                f'showing the paper\'s LaTeX">{math(b["expression_latex"])}</div>')
    return f'<div class="formula"><code>{text(bounds.canonical_expr(b))}</code></div>'


def result_details(it: dict) -> str:
    r = it["r"]
    b = r.get("bound") or {}
    pairs = []
    if b.get("regime"):
        pairs.append(("Regime", text(b.get("regime"))))
    if r.get("extra_assumptions"):
        pairs.append(("Assumptions", "<ul>" + "".join(f"<li>{e(str(x))}</li>" for x in as_list(r["extra_assumptions"])) + "</ul>"))
    if it.get("knows"):
        pairs.append(("Learner knows", text(it["knows"])))
    if r.get("comparator"):
        pairs.append(("Comparator", text(label(r["comparator"]))))
    if r.get("symbols"):
        pairs.append(("Symbols", "<ul>" + "".join(f"<li><code>{e(str(k))}</code>: {e(str(v))}</li>" for k, v in r["symbols"].items()) + "</ul>"))
    canon = bounds.canonical_expr(b)
    if canon:
        pairs.append(("Canonical", f"<code>{e(str(canon))}</code>"))
    if b.get("expression_normalised") and b.get("expression") and b["expression"] != b["expression_normalised"]:
        pairs.append(("As extracted", f"<code>{e(str(b['expression']))}</code>"))
    if b.get("conversions"):
        pairs.append(("Conversions", text(b["conversions"])))
    if b.get("expression_latex"):
        pl = str(b["expression_latex"])
        prose = "$" in pl or re.search(r"[A-Za-z]{4,}\s+[A-Za-z]{3,}", re.sub(r"\\[A-Za-z]+", "", pl))
        pairs.append(("Paper's LaTeX", ("" if prose else math(pl, "paper")) + f'<code class="raw">{e(pl)}</code>'))
    if r.get("notes"):
        pairs.append(("Notes", text(r["notes"])))
    if r.get("compute") and r.get("compute") != "not_stated":
        pairs.append(("Compute", text(label(r["compute"]))))
    return f'<details class="more"><summary>details</summary>{dl(pairs, "kv")}</details>'


def result_badges(r: dict, extra: str = "") -> str:
    out = []
    dep = DEPENDENCE.get(r.get("dependence") or "")
    if dep:
        out.append(badge(dep[0], dep[1]))
    elif r.get("dependence"):
        out.append(badge(label(r["dependence"])))
    if r.get("probability") in PROBABILITY and r["probability"] != "expectation":
        out.append(badge(PROBABILITY[r["probability"]], "prob"))
    if r.get("horizon") in HORIZON:
        out.append(badge(HORIZON[r["horizon"]], "hor"))
    conf = r.get("confidence")
    if conf in ("low", "medium"):
        out.append(badge(f"{conf} confidence", f"conf-{conf}", str(r.get("notes") or "")))
    if r.get("is_new") is False:
        out.append(badge("restated", "muted-badge", "result restated from earlier work"))
    return '<div class="badges">' + "".join(out) + extra + "</div>"


def quantity_rank(site: Site, q) -> int:
    return site.onto.quantities.index(q) if q in site.onto.quantities else len(site.onto.quantities)


def sort_items(site: Site, items: list[dict]) -> list[dict]:
    dep = {"worst_case": 0, "instance_dependent": 1}
    return sorted(items, key=lambda it: (quantity_rank(site, it["r"].get("quantity")),
                                         dep.get(it["r"].get("dependence"), 2),
                                         str((it["r"].get("bound") or {}).get("notation")),
                                         site.paper_info(it["paper"]).get("year") or 0))


def results_table(items: list[dict], site: Site, root: str, show_setting: bool = False) -> str:
    if not items:
        return '<p class="muted">None extracted.</p>'
    # On a paper's own page (show_setting) the paper column would repeat itself.
    headers = ["Setting", "Bound", "Algorithm", "Source"] if show_setting else ["Bound", "Algorithm", "Paper", "Source"]
    ncol = len(headers)
    body = []
    current = object()
    for it in sort_items(site, items):
        r, pid = it["r"], it["paper"]
        q = r.get("quantity")
        if q != current:
            current = q
            body.append(f'<tr class="group"><th colspan="{ncol}">{e(QUANTITY_LABEL.get(q, label(q) or "Unspecified quantity"))}</th></tr>')
        if it.get("alg"):
            full = it["alg"]
            tip = full + (f" (also: {', '.join(it['alg_aliases'][:4])})" if it.get("alg_aliases") else "")
            alg = f'<span class="alg" title="{e(tip, quote=True)}">{e(short(full))}</span>'
        elif r.get("algorithm_class"):
            alg = f'<span class="muted" title="{e(str(r["algorithm_class"]), quote=True)}">{e(short("class: " + str(r["algorithm_class"])))}</span>'
        else:
            alg = '<span class="muted">any algorithm</span>' if (r.get("side") or "") == "lower" else NONE
        src = r.get("source") or {}
        num = str(src.get("number") or src.get("label") or "source")
        source = e(num)
        if src.get("quote"):
            source = (f'<details class="pop"><summary>{e(num)}</summary>'
                      f'<blockquote>{e(str(src["quote"]))}</blockquote></details>')
        paper = f'<a href="{root}papers/{slugify(pid)}.html" title="{e(site.title(pid), quote=True)}">{e(site.cite(pid))}</a>'
        cells = [bound_html(r) + result_badges(r, result_details(it)), alg, paper, source]
        if show_setting:
            n = site.nodes.get(it.get("node") or "")
            cells = [f'<a href="{root}settings/{n["slug"]}.html">{e(n["name"])}</a>' if n else text(r.get("setting")),
                     cells[0], alg, source]
        tds = "".join(f'<td class="c-{slugify(h)}" data-label="{h}">{c}</td>' for h, c in zip(headers, cells))
        body.append(f"<tr>{tds}</tr>")
    th = "".join(f'<th class="c-{slugify(h)}">{h}</th>' for h in headers)
    return (filter_box("Filter by algorithm, paper, quantity…") +
            f'<div class="scroll"><table class="results filterable{" with-setting" if show_setting else ""}">'
            f'<thead><tr>{th}</tr></thead><tbody>\n' + "\n".join(body) + "\n</tbody></table></div>")


def split_sides(items):
    up = [i for i in items if (i["r"].get("side") or "").lower() == "upper"]
    lo = [i for i in items if (i["r"].get("side") or "").lower() == "lower"]
    other = [i for i in items if i not in up and i not in lo]
    return up, lo, other


# ---------------------------------------------------------------- pages


def home_page(site: Site) -> str:
    n_res = sum(len(n["results"]) for n in site.nodes.values())
    n_ex = sum(1 for pid in site.paper_ids() if pid in site.extractions)
    n_dir = sum(1 for x in site.edges if x["kind"] != "neighbour")
    tiles = [
        ("papers/index.html", len(site.paper_ids()), "papers", f"{n_ex} extracted"),
        ("settings/index.html", len(site.nodes), "canonical settings", "assumption vectors"),
        ("settings/index.html", n_res, "results", "upper and lower bounds"),
        ("graph.html", n_dir, "specialisation edges", f"{len(site.edges) - n_dir} other neighbours"),
    ]
    tiles_html = "".join(f'<a class="tile" href="{h}"><b>{n}</b><span>{lbl}</span><small>{sub}</small></a>'
                         for h, n, lbl, sub in tiles)
    body = f"""
<section class="hero">
<h1>An atlas of theoretical bandit results</h1>
<p class="lede">Papers are parsed by an LLM into <em>settings</em> (assumption vectors over a fixed ontology) and
<em>results</em> (upper and lower bounds with provenance back to the theorem). Settings that differ in one assumption
are linked; where the ontology orders the two values, the link is a <em>specialisation</em> along which bounds transfer.</p>
</section>
<div class="tiles">{tiles_html}</div>
<div class="cards">
<a class="card" href="graph.html"><h2>Settings graph →</h2><p>Every canonical setting as a node, sized by number of results.
Arrows point from a special case to its generalisation.</p></a>
<a class="card" href="settings/index.html"><h2>Settings →</h2><p>Browse settings by environment or action space, with counts of upper and lower bounds.</p></a>
<a class="card" href="papers/index.html"><h2>Papers →</h2><p>The pilot corpus: what each paper proves, theorem by theorem.</p></a>
<a class="card" href="ground-truth.html"><h2>Ground truth →</h2><p>Hand-curated bandit convex optimisation reference{"" if site.bco else " (not yet available)"},
and the pilot facts the graph should rediscover.</p></a>
</div>
<p class="muted small">Ontology {e(site.onto.version)}{" · canonical layer (data/canonical)" if site.canonical else " · grouped from raw extractions"}.
Bounds are shown in canonical notation; the paper's own LaTeX is under each result's <em>details</em>. No bounds are compared or inferred yet.</p>
"""
    return page("Home", body, "", "home")


PALETTE_SLOTS = 8


def colour_slots(values: list[str]) -> dict[str, int]:
    """Fixed categorical slot per value, ordered by frequency; overflow folds into 'other' (slot 0)."""
    from collections import Counter

    c = Counter(values)
    ranked = [v for v, _ in c.most_common()]
    return {v: (i + 1 if i < PALETTE_SLOTS else 0) for i, v in enumerate(ranked)}


def settings_index(site: Site) -> str:
    act_slots = colour_slots([n["key"].get("action_space", "") for n in site.nodes.values()])
    rows = []
    for n in sorted(site.nodes.values(), key=lambda n: (-len(n["results"]), n["name"])):
        up, lo = site.counts(n)
        k = n["key"]
        env, act = k.get("environment", ""), k.get("action_space", "")
        rows.append(
            f'<tr data-environment="{e(value_label("environment", env) if env else "unspecified")}" '
            f'data-action_space="{e(value_label("action_space", act) if act else "unspecified")}" data-n="{len(n["results"])}">'
            f'<td data-label="Setting"><span class="dot s{act_slots.get(act, 0)}" aria-hidden="true"></span>'
            f'<a href="{n["slug"]}.html">{e(n["name"])}</a></td>'
            f'<td class="num" data-label="Upper">{up or NONE}</td><td class="num" data-label="Lower">{lo or NONE}</td>'
            f'<td class="num" data-label="Papers">{len(n["papers"])}</td></tr>'
        )
    body = f"""
<h1>Settings</h1>
<p class="lede">{len(site.nodes)} canonical settings. A name lists only the assumptions that differ from the plain
stochastic-regret defaults (bandit feedback, no context, no extras). Also see the <a href="../graph.html">graph</a>.</p>
<div class="toolbar">
{filter_box("Filter settings…")}
<div class="seg" role="group" aria-label="Group by">
<span>Group by</span>
<button type="button" data-group="action_space" aria-pressed="true">Action space</button>
<button type="button" data-group="environment" aria-pressed="false">Environment</button>
<button type="button" data-group="" aria-pressed="false">None</button>
</div>
</div>
<div class="scroll"><table class="settings filterable groupable">
<thead><tr><th>Setting</th><th class="num">Upper</th><th class="num">Lower</th><th class="num">Papers</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>
"""
    return page("Settings", body, "../", "settings")


def change_html(x: dict) -> str:
    def one(d, fv, tv):
        v = lambda s: e(value_label(d, s) if s else "none")
        return f'<span class="dim">{e(dim_label(d))}</span> {v(fv)} <span class="arrow">→</span> {v(tv)}'

    return "<br>".join(one(*c) for c in x.get("changes") or [(x["dim"], x["from"], x["to"])])


def flip(x: dict) -> dict:
    """The same edge described from its target's side."""
    return {**x, "from": x["to"], "to": x["from"],
            "changes": [(d, tv, fv) for d, fv, tv in x.get("changes") or [(x["dim"], x["from"], x["to"])]]}


def neighbourhood(site: Site, n: dict) -> str:
    nid = n["id"]
    general, special, other = [], [], []
    for x in site.hasse():  # immediate covers in the product order, plus unordered neighbours
        if nid not in (x["source"], x["target"]):
            continue
        if x["kind"] == "neighbour":
            o = x["target"] if x["source"] == nid else x["source"]
            other.append((o, x if x["source"] == nid else flip(x)))
        elif x["source"] == nid:
            general.append((x["target"], x))
        else:
            special.append((x["source"], flip(x)))

    def lst(items, empty):
        if not items:
            return f'<p class="muted small">{empty}</p>'
        lis = []
        for o, x in sorted(items, key=lambda t: (t[1]["dim"], -len(site.nodes[t[0]]["results"]))):
            m = site.nodes[o]
            up, lo = site.counts(m)
            kind = ' <span class="badge muted-badge" title="reduction (e.g. K-armed as linear with d = K)">reduction</span>' if x["kind"] == "reduction" else ""
            lis.append(f'<li><a href="{m["slug"]}.html">{e(m["name"])}</a>'
                       f'<div class="chg">{change_html(x)}{kind} <span class="cnt">{up}↑ {lo}↓</span></div></li>')
        return "<ul class=\"nb\">" + "".join(lis) + "</ul>"

    return f"""
<div class="nbhd">
<section><h3>More general <span class="muted">({len(general)})</span></h3>
<p class="hint">Their upper bounds also hold here.</p>{lst(general, "No more general extracted setting.")}</section>
<section><h3>Special cases <span class="muted">({len(special)})</span></h3>
<p class="hint">Their lower bounds also hold here.</p>{lst(special, "No extracted special case.")}</section>
<section><h3>Other neighbours <span class="muted">({len(other)})</span></h3>
<p class="hint">Differ in one unordered assumption.</p>{lst(other, "None.")}</section>
</div>
<p class="small"><a href="../graph.html?focus={e(n["slug"])}">Show in the graph →</a></p>"""


def setting_page(site: Site, n: dict) -> str:
    chips = []
    for d, v in n["key"].items():
        if not v or v in ("not_applicable", "none", "null"):
            continue
        desc = site.onto.describe(d, v)
        cls = "chip" + ("" if not is_default(d, v) else " dflt")
        shown = value_label(d, v.split("+")) if d in ("function_class", "instance_assumptions", "extras", "learner_knows") else value_label(d, v)
        chips.append(f'<span class="{cls}" title="{e(desc or v, quote=True)}"><b>{e(dim_label(d))}</b> {e(shown)}</span>')
    inst_rows = []
    for pid, lid, nm in n["members"]:
        s = next((x for x in listify(site.extractions.get(pid) or {}, "settings") if x.get("id") == lid), {})
        inst_rows.append([
            f'<a href="../papers/{slugify(pid)}.html" title="{e(site.title(pid), quote=True)}">{e(site.cite(pid))}</a>',
            text(nm or s.get("name_in_paper")),
            text(s.get("learner_knows")),
            ("<ul class=\"tight\">" + "".join(f"<li>{e(str(u))}</li>" for u in as_list(s.get("unmapped"))) + "</ul>") if s.get("unmapped") else NONE,
        ])
    up, lo, other = split_sides(n["results"])
    canon_id = f' / <code class="small">{e(n["id"])}</code>' if site.canonical else ""
    body = f"""
<p class="crumbs"><a href="index.html">Settings</a>{canon_id}</p>
<h1>{e(n["name"])}</h1>
<div class="chips">{"".join(chips)}</div>
<p class="summary"><b>{len(up)}</b> upper · <b>{len(lo)}</b> lower bounds from <b>{len(n["papers"])}</b> paper{"s" if len(n["papers"]) != 1 else ""}.</p>
<h2 id="neighbours">Neighbourhood</h2>{neighbourhood(site, n)}
<h2 id="upper">Upper bounds <span class="muted">({len(up)})</span></h2>{results_table(up, site, "../")}
<h2 id="lower">Lower bounds <span class="muted">({len(lo)})</span></h2>{results_table(lo, site, "../")}
{f'<h2>Other <span class="muted">({len(other)})</span></h2>' + results_table(other, site, "../") if other else ""}
<h2 id="papers">As stated in papers</h2>{table(["Paper", "Name in paper", "Learner knows", "Unmapped"], inst_rows, "compact")}
"""
    return page(n["name"], body, "../", "settings")


def papers_index(site: Site) -> str:
    rows = []
    for pid in site.paper_ids():
        info = site.paper_info(pid)
        ex = site.extractions.get(pid)
        nres = sum(1 for n in site.nodes.values() for it in n["results"] if it["paper"] == pid)
        status = f"{nres}" if ex else '<span class="muted">not extracted</span>'
        authors = as_list(info.get("authors"))
        auth = ", ".join(surname(a) for a in authors[:3]) + (" et al." if len(authors) > 3 else "")
        rows.append([
            f'<a href="{slugify(pid)}.html">{e(site.title(pid))}</a>',
            e(auth) or NONE, text(info.get("year")), e(label(info.get("slice"))) or NONE, status,
        ])
    body = (f'<h1>Papers</h1><p class="lede">{len(rows)} papers in the pilot corpus.</p>'
            + table(["Title", "Authors", "Year", "Slice", "Results"], rows, "papers", filterable=True))
    return page("Papers", body, "../", "papers")


def paper_page(site: Site, pid: str) -> str:
    info = site.paper_info(pid)
    ex = site.extractions.get(pid)
    url = info.get("url") or (f"https://arxiv.org/abs/{info['arxiv_id']}" if info.get("arxiv_id") else None)
    meta = [(k, text(info.get(k))) for k in ["authors", "year", "venue", "arxiv_id", "slice", "result_types"] if info.get(k) is not None]
    if url:
        meta.append(("link", f'<a href="{e(url, quote=True)}">{e(url)}</a>'))
    if info.get("why"):
        meta.append(("why in corpus", text(info.get("why"))))
    body = f'<p class="crumbs"><a href="index.html">Papers</a> / <code class="small">{e(pid)}</code></p><h1>{e(site.title(pid))}</h1>{dl(meta, "meta")}'
    items = [it for n in site.nodes.values() for it in n["results"] if it["paper"] == pid]
    if not ex and not items:
        body += '<p class="notice">Not yet extracted.</p>'
        return page(pid, body, "../", "papers")
    ex = ex or {}

    up, lo, other = split_sides(items)
    body += f'<h2>Upper bounds <span class="muted">({len(up)})</span></h2>' + results_table(up, site, "../", show_setting=True)
    body += f'<h2>Lower bounds <span class="muted">({len(lo)})</span></h2>' + results_table(lo, site, "../", show_setting=True)
    if other:
        body += f'<h2>Other <span class="muted">({len(other)})</span></h2>' + results_table(other, site, "../", show_setting=True)

    srows = []
    for s in listify(ex, "settings"):
        nid = site.local_to_node.get((pid, s.get("id")))
        n = site.nodes.get(nid or "")
        canon = f'<a href="../settings/{n["slug"]}.html">{e(n["name"])}</a>' if n else (
            '<span class="muted">out of scope</span>' if s.get("in_scope") is False else NONE)
        quote = s.get("definition_quote")
        srows.append([e(str(s.get("id", ""))), text(s.get("name_in_paper")), canon,
                      ("<ul class=\"tight\">" + "".join(f"<li>{e(str(u))}</li>" for u in as_list(s.get("unmapped"))) + "</ul>") if s.get("unmapped") else NONE,
                      f'<details class="pop"><summary>quote</summary><blockquote>{e(str(quote))}</blockquote></details>' if quote else NONE])
    body += "<h2>Settings</h2>" + table(["Id", "Name in paper", "Canonical setting", "Unmapped", "Definition"], srows, "compact")

    arows = [[text(a.get("id")), text(a.get("name")), text(a.get("is_new")), text(a.get("techniques")), text(a.get("requires_knowledge_of"))]
             for a in listify(ex, "algorithms")]
    body += "<h2>Algorithms</h2>" + table(["Id", "Name", "New", "Techniques", "Requires knowledge of"], arows, "compact")

    crows = []
    for c in listify(ex, "cited_results"):
        b = c.get("bound") or {}
        crows.append([text(c.get("cited_key")) + (f'<div class="muted small">{e(str(c["cited_title"]))}</div>' if c.get("cited_title") else ""),
                      text(c.get("algorithm_name")), text(c.get("side")), bound_html({"bound": b, "side": c.get("side")}),
                      text(c.get("setting_description"))])
    body += "<h2>Cited results</h2>" + table(["Cited", "Algorithm", "Side", "Bound", "Setting"], crows, "compact")

    run = ex.get("_run")
    if isinstance(run, dict):
        body += ('<details class="runinfo"><summary>Extraction run</summary>' + dl([(k, text(v)) for k, v in run.items()], "kv")
                 + f'<p class="muted small">schema {e(str(ex.get("schema_version")))}, ontology {e(str(ex.get("ontology_version")))}</p></details>')
    return page(pid, body, "../", "papers")


def ground_truth_page(site: Site) -> str:
    bco = site.bco
    body = "<h1>Ground truth: bandit convex optimisation</h1>"
    if not isinstance(bco, dict):
        body += '<p class="notice">No ground-truth file yet (<code>data/ground_truth/bco.yaml</code>).</p>'
        return page("Ground truth", body, "", "gt")
    body += '<p class="lede">Hand-curated reference data from Lattimore\'s <em>Bandit Convex Optimisation</em>, rendered as-is.</p>'
    order = ["source", "settings", "results", "transfer_rules", "open_problems"]
    keys = [k for k in order if k in bco] + [k for k in bco if k not in order]
    toc = " · ".join(f'<a href="#{slugify(k)}">{e(k.replace("_", " "))}</a>' for k in keys)
    body += f'<p class="crumbs">{toc}</p>'
    for k in keys:
        v = bco[k]
        inner = generic(v) if isinstance(v, (dict, list)) else f"<p>{text(v)}</p>"
        body += f'<h2 id="{slugify(k)}">{e(k.replace("_", " ").capitalize())}</h2>' + inner
    return page("Ground truth", body, "", "gt", wide=True)


def fact_bound(side: str, spec) -> str:
    if not isinstance(spec, dict):
        return text(spec)
    tex, ok = bounds.bound_tex({"expression": spec.get("bound"), "notation": spec.get("notation")}, side, None)
    f = math(tex) if ok else f"<code>{text(spec.get('bound'))}</code>"
    papers = " ".join(f'<a href="papers/{slugify(p)}.html">{e(p)}</a>' for p in as_list(spec.get("papers")))
    return f'<div class="formula">{f}</div><div class="muted small">{papers}</div>'


def facts_page(site: Site) -> str:
    facts = site.facts
    body = "<h1>Pilot acceptance facts</h1>"
    if not isinstance(facts, dict):
        body += '<p class="notice">No file yet (<code>data/ground_truth/pilot-facts.yaml</code>).</p>'
        return page("Pilot facts", body, "", "facts")
    body += ('<p class="lede">Known results in the K-armed and linear pilot slice that the graph should rediscover '
             "(plan.md Phase 3 acceptance tests). Written from domain knowledge; not yet verified line by line.</p>")
    by_key = {}
    for n in site.nodes.values():
        by_key.setdefault(tuple(n["key"].get(d, "") for d in site.onto.dims), n)
    cards = []
    for f in listify(facts, "facts"):
        s = f.get("setting") or {}
        n = by_key.get(tuple(flat_value(s.get(d)) for d in site.onto.dims)) if isinstance(s, dict) else None
        sname = setting_name(flat_key(s, site.onto.dims)) if isinstance(s, dict) else str(s)
        slink = f'<a href="settings/{n["slug"]}.html">{e(n["name"])}</a>' if n else f'{e(sname)} <span class="muted small">(no extracted node)</span>'
        tests = "".join(f"<li>{e(str(t))}</li>" for t in as_list(f.get("tests")))
        cards.append(f"""<article class="fact">
<header><b>{e(str(f.get("id", "")))}</b> {badge(label(f.get("status")), "status")} {badge(str(f.get("confidence", "")) + " confidence", "muted-badge")}</header>
<p class="small">{slink} · <span class="muted">{text(f.get("regime"))}</span></p>
<div class="ul2"><div><span class="side">Upper</span>{fact_bound("upper", f.get("upper"))}</div>
<div><span class="side">Lower</span>{fact_bound("lower", f.get("lower"))}</div></div>
{f'<p class="small">{e(str(f["history"]))}</p>' if f.get("history") else ""}
{f'<details class="more"><summary>tests</summary><ul class="tight">{tests}</ul></details>' if tests else ""}
</article>""")
    body += filter_box("Filter facts…") + '<div class="facts filterable-cards">' + "".join(cards) + "</div>"
    return page("Pilot facts", body, "", "facts")


def graph_page(site: Site) -> str:
    act_slots = colour_slots([n["key"].get("action_space", "") for n in site.nodes.values()])
    env_slots = colour_slots([n["key"].get("environment", "") for n in site.nodes.values()])
    nodes = []
    for n in site.nodes.values():
        up, lo = site.counts(n)
        act, env = n["key"].get("action_space", ""), n["key"].get("environment", "")
        nodes.append({"id": n["id"], "url": f'settings/{n["slug"]}.html', "slug": n["slug"], "name": n["name"],
                      "up": up, "lo": lo, "papers": len(n["papers"]),
                      "action_space": value_label("action_space", act) if act else "unspecified",
                      "environment": value_label("environment", env) if env else "unspecified",
                      "sa": act_slots.get(act, 0), "se": env_slots.get(env, 0)})
    def lbl(x, i):
        return "; ".join(value_label(d, c[i]) if c[i] else "none"
                         for c in x.get("changes") or [(x["dim"], x["from"], x["to"])] for d in [c[0]])

    edges = [{"s": x["source"], "t": x["target"], "kind": x["kind"],
              "dim": " + ".join(dim_label(c[0]) for c in x.get("changes") or [(x["dim"],)]),
              "from": lbl(x, 1), "to": lbl(x, 2)} for x in site.hasse()]

    def legend(slots, dim):
        items = sorted(((s, v) for v, s in slots.items()), key=lambda t: (t[0] == 0, t[0]))
        seen = set()
        out = []
        for s, v in items:
            lbl = "other" if s == 0 else (value_label(dim, v) if v else "unspecified")
            if lbl in seen:
                continue
            seen.add(lbl)
            out.append(f'<li><span class="dot s{s}"></span>{e(lbl)}</li>')
        return "".join(out)

    data = json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False).replace("</", "<\\/")
    n_dir = sum(1 for x in edges if x["kind"] != "neighbour")
    body = f"""
<div class="graph-head">
<div>
<h1>Settings graph</h1>
<p class="lede small">{len(nodes)} settings. <b>Arrows</b> run from a special case to its generalisation
({n_dir} after removing transitive ones): upper bounds flow against the arrow, lower bounds along it.
<span class="faint-line"></span> faint lines join settings that differ in one unordered assumption.
Node size ∝ number of results. Click a node to open it.</p>
</div>
</div>
<div class="graph-controls">
<div class="seg" role="group" aria-label="Colour by"><span>Colour</span>
<button type="button" data-colour="sa" aria-pressed="true">Action space</button>
<button type="button" data-colour="se" aria-pressed="false">Environment</button></div>
<div class="seg" role="group" aria-label="Layout"><span>Layout</span>
<button type="button" data-layout="dagre" aria-pressed="true">Hierarchy</button>
<button type="button" data-layout="cose" aria-pressed="false">Force</button></div>
<label class="check"><input type="checkbox" id="show-nb"> show other neighbours</label>
<input class="filter" id="graph-search" type="search" placeholder="Find a setting…" aria-label="Find a setting">
</div>
<div class="graph-wrap">
<div id="cy" role="img" aria-label="Graph of canonical settings"></div>
<aside class="legend">
<h3>Colour</h3>
<ul id="legend-sa">{legend(act_slots, "action_space")}</ul>
<ul id="legend-se" hidden>{legend(env_slots, "environment")}</ul>
<h3>Edges</h3>
<ul class="edge-key"><li><span class="ek order"></span>specialisation</li>
<li><span class="ek reduction"></span>reduction</li><li><span class="ek neighbour"></span>other neighbour</li></ul>
<p class="muted small">In the hierarchy, settings with no specialisation edge sit in the grid on the right.
Table view: <a href="settings/index.html">settings index</a>.</p>
</aside>
<div id="cy-tip" role="tooltip" hidden></div>
</div>
<script type="application/json" id="graph-data">{data}</script>
"""
    head = (f'<script defer src="{CYTOSCAPE}"></script>\n<script defer src="{DAGRE}"></script>\n'
            f'<script defer src="{CY_DAGRE}"></script>\n<script defer src="static/graph.js"></script>')
    return page("Graph", body, "", "graph", head=head, wide=True)


# ---------------------------------------------------------------- main


def build(root: Path, out: Path) -> None:
    site = Site(root)
    if out.exists():
        shutil.rmtree(out)
    (out / "settings").mkdir(parents=True)
    (out / "papers").mkdir()
    shutil.copytree(HERE / "static", out / "static")
    (out / ".nojekyll").write_text("")

    def w(rel: str, content: str) -> None:
        (out / rel).write_text(content, encoding="utf-8")

    w("index.html", home_page(site))
    w("graph.html", graph_page(site))
    w("ground-truth.html", ground_truth_page(site))
    w("pilot-facts.html", facts_page(site))
    w("settings/index.html", settings_index(site))
    for n in site.nodes.values():
        w(f"settings/{n['slug']}.html", setting_page(site, n))
    w("papers/index.html", papers_index(site))
    for pid in site.paper_ids():
        w(f"papers/{slugify(pid)}.html", paper_page(site, pid))
    n_res = sum(len(n["results"]) for n in site.nodes.values())
    print(f"built {out}: {len(site.paper_ids())} papers, {len(site.extractions)} extractions, "
          f"{len(site.nodes)} settings, {n_res} results, {len(site.edges)} edges, "
          f"{'canonical layer' if site.canonical else 'raw extractions'}, ontology {site.onto.version}, "
          f"ground truth {'yes' if site.bco else 'no'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixtures", action="store_true", help="read site/fixtures/ instead of the repo data")
    ap.add_argument("--out", type=Path, default=REPO / "_site")
    args = ap.parse_args()
    build(HERE / "fixtures" if args.fixtures else REPO, args.out)


if __name__ == "__main__":
    main()
