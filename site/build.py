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

    data/canonical/inferred.json                         bounds propagated by pipeline/infer.py

Modules: ontology.py (dimensions, names), bounds.py (SymPy -> LaTeX), and
pipeline/order.py (the specialisation order; single source of truth for edges).
Display only: no bound comparison or inference happens here; inherited bounds are
read from inferred.json and shown separately from extracted ones (D1, D4).
"""

from __future__ import annotations

import argparse
import hashlib
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
sys.path.insert(1, str(REPO / "pipeline"))

import analysis  # noqa: E402
import bounds  # noqa: E402
from order import Order  # noqa: E402  (pipeline/order.py: the specialisation order, D1)
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


# Node-parameter fields shown in base names; the rest only appear when needed to tell
# two otherwise identically named settings apart (see Site._dedupe_names).
NAME_FIELDS = {"action_set.shape"}


def field_bit(d: str, v: str) -> str:
    return f"{value_label(d, v)} {d.split('.', 1)[1].replace('_', ' ')}"


def short_params(s: str, width: int = 48) -> str:
    """'K=2, restriction=L*_T / T <= alpha' -> 'K = 2, restriction: L*_T / T ≤ α' with long values cut."""
    out = []
    for part in s.split(", "):
        k, _, v = part.partition("=")
        v = v.replace("<=", "≤").replace(">=", "≥").replace("=>", "≥")
        if v.startswith(">") or v.startswith("<") or v.startswith("≥") or v.startswith("≤"):
            item = f"{k} {v}"
        elif len(v) > 12 or " " in v:
            item = f"{k}: {v}"
        else:
            item = f"{k} = {v}"
        out.append(item if len(item) <= width else item[: width - 1] + "…")
    return ", ".join(out)


def setting_name(key: dict[str, str]) -> str:
    order = [d for d in NAME_ORDER if d in key] + [d for d in key if d not in NAME_ORDER and d not in TRAILING
                                                    and ("." not in d or d in NAME_FIELDS)]
    bits = []
    for d in order:
        v = key[d]
        if is_default(d, v):
            continue
        if d in ("function_class", "instance_assumptions", "extras"):
            bits.append(value_label(d, v.split("+")))
        elif "." in d:  # node-parameter field, e.g. action_set.shape
            bits.append(field_bit(d, v))
        else:
            bits.append(value_label(d, v))
    if key.get("learner_knows"):
        bits.append("knows " + pretty_vars(", ".join(key["learner_knows"].split("+"))))
    if key.get("parameters"):
        bits.append(pretty_vars(short_params(key["parameters"])))
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
        for n in self.nodes.values():
            n["inherited"] = []
        self.n_inferred_raw = 0
        if self.canonical:
            self._load_inferred(canon)

    # -- canonical layer (preferred)
    def _load_canonical(self, canon: Path) -> None:
        for s in listify(load_json(canon / "settings.json"), "settings"):
            if s.get("in_scope") is False or not s.get("id"):
                continue
            key = flat_key(s.get("key") or {}, self.onto.dims, include=("learner_knows", "parameters"))
            members = [(m.get("paper"), m.get("local_id"), m.get("name_in_paper")) for m in listify(s, "members")]
            self.nodes[s["id"]] = {"id": s["id"], "slug": s["id"] if re.fullmatch(r"[A-Za-z0-9_.-]+", s["id"]) else slugify(s["id"]), "key": key, "label": s.get("label"),
                                   "raw": s.get("key") or {}, "members": members, "results": []}
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
                # learner_knows/parameters are not part of a raw-mode node's identity
                raw = {k: v for k, v in s.items() if k not in ("learner_knows", "parameters")}
                node = self.nodes.setdefault(nid, {"id": nid, "slug": nid, "key": key, "label": None, "raw": raw,
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
        """Settings sharing a base name get a short suffix listing only the node-parameter
        fields that differ between them (e.g. "corruption adversary: adaptive"); the id is a
        last resort."""
        seen: dict[str, list] = {}
        for n in self.nodes.values():
            seen.setdefault(n["name"], []).append(n)
        for name, ns in seen.items():
            if len(ns) < 2:
                continue
            fields = sorted({d for n in ns for d in n["key"] if "." in d and d not in NAME_FIELDS})
            differing = [d for d in fields if len({n["key"].get(d, "") for n in ns}) > 1]
            for n in ns:
                bits = [field_bit(d, n["key"][d]) for d in differing if not is_default(d, n["key"].get(d, ""))]
                n["name"] = f"{name} · {', '.join(bits)}" if bits else name
            again: dict[str, list] = {}
            for n in ns:
                again.setdefault(n["name"], []).append(n)
            for nm, group in again.items():
                if len(group) > 1:
                    for n in group:
                        n["name"] = f"{nm} [{n['id'][:10]}]"

    # -- neighbourhood structure
    def _edges(self) -> list[dict]:
        """Directed specialisation edges from pipeline/order.py (Order.leq), plus undirected
        "neighbour" edges between settings that differ in exactly one unordered dimension."""
        try:
            order = Order(self.onto.data) if self.onto.data.get("dimensions") else None
        except Exception as exc:  # noqa: BLE001 - a malformed ontology still yields a site
            warn(f"could not build the specialisation order: {exc}")
            order = None
        ids = sorted(self.nodes)
        out = []
        for i, a in enumerate(ids):
            na, ka = self.nodes[a], self.nodes[a]["key"]
            for b in ids[i + 1:]:
                nb, kb = self.nodes[b], self.nodes[b]["key"]
                ch, s, tg = None, a, b
                if order is not None:
                    ch = order.leq(na["raw"], nb["raw"])
                    if not ch:
                        ch, s, tg = order.leq(nb["raw"], na["raw"]), b, a
                if ch:
                    ks, kt = self.nodes[s]["key"], self.nodes[tg]["key"]
                    changes = [(c.dim, ks.get(c.dim, flat_value(c.special)), kt.get(c.dim, flat_value(c.general)))
                               for c in ch]
                    kind = "reduction" if any(c.kind == "reduction" for c in ch) else "order"
                    out.append({"source": s, "target": tg, "kind": kind, "dim": changes[0][0],
                                "from": changes[0][1], "to": changes[0][2], "changes": changes,
                                "maps": {k: v for c in ch for k, v in c.param_map.items()} if kind == "reduction" else {}})
                    continue
                diff = [d for d in dict.fromkeys(list(ka) + list(kb)) if ka.get(d, "") != kb.get(d, "")]
                if len(diff) == 1:
                    d = diff[0]
                    out.append({"source": a, "target": b, "kind": "neighbour", "dim": d,
                                "from": ka.get(d, ""), "to": kb.get(d, ""), "changes": [(d, ka.get(d, ""), kb.get(d, ""))]})
        return out

    # -- inherited bounds (pipeline/infer.py)
    def _load_inferred(self, canon: Path) -> None:
        recs = listify(load_json(canon / "inferred.json"), "inferred")
        self.n_inferred_raw = len(recs)
        by_id = {r["id"]: r for r in listify(load_json(canon / "results.json"), "results") if r.get("id")}
        dropped = {"own": 0, "dup": 0, "missing": 0}
        # Hops along covering (Hasse) edges, special -> general: 1 = an immediate cover.
        succ: dict[str, list] = {}
        for x in self.hasse():
            if x["kind"] != "neighbour":
                succ.setdefault(x["source"], []).append(x["target"])
        hops: dict[str, dict] = {}

        def hop(a: str, b: str) -> int:
            if a not in hops:
                dist, frontier = {a: 0}, [a]
                while frontier:
                    nxt = []
                    for y in frontier:
                        for z in succ.get(y, ()):
                            if z not in dist:
                                dist[z] = dist[y] + 1
                                nxt.append(z)
                    frontier = nxt
                hops[a] = dist
            return hops[a].get(b, 99)

        for rec in recs:
            n = self.nodes.get(rec.get("setting_id") or "")
            src = by_id.get(rec.get("from_result") or "")
            if n is None or src is None or rec.get("from_setting") not in self.nodes:
                dropped["missing"] += 1
                continue
            b = dict(src.get("bound") or {})
            orig = bounds.canonical_expr(b)
            b["expression_normalised"] = rec.get("expression") or bounds.canonical_expr(b)
            r = {**src, "bound": b}
            it = self._item(src.get("paper"), r, rec["from_setting"])
            it["inf"] = rec
            it["orig_expr"] = orig
            upper = str(rec.get("rule", "")).startswith("upper")
            special, general = (rec["setting_id"], rec["from_setting"]) if upper else (rec["from_setting"], rec["setting_id"])
            it["hops"] = hop(special, general)
            it["dist"] = (it["hops"], len(rec.get("changes") or []))
            n["inherited"].append(it)
        for n in self.nodes.values():
            # Already proved directly here by the same paper: not worth repeating.
            own = {self._sig(it) for it in n["results"]}
            seen: dict[tuple, dict] = {}
            for it in sorted(n["inherited"], key=lambda it: it["dist"]):
                sig = self._sig(it)
                if sig in own:
                    dropped["own"] += 1
                elif sig in seen:
                    seen[sig].setdefault("also", []).append(it)
                    dropped["dup"] += 1
                else:
                    seen[sig] = it
            n["inherited"] = list(seen.values())
        self.inferred_dropped = dropped

    @staticmethod
    def _sig(it: dict) -> tuple:
        """Identity of a bound for deduplication: same paper, side, quantity and canonical form."""
        r = it["r"]
        b = r.get("bound") or {}
        return (it["paper"], (r.get("side") or "").lower(), r.get("quantity"), r.get("dependence"),
                b.get("notation"), str(bounds.canonical_expr(b) or "").replace(" ", ""))

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

    def counts(self, n: dict, key: str = "results") -> tuple[int, int]:
        up = sum(1 for it in n[key] if (it["r"].get("side") or "").lower() == "upper")
        lo = sum(1 for it in n[key] if (it["r"].get("side") or "").lower() == "lower")
        return up, lo


# ---------------------------------------------------------------- page shell

NAV = [
    ("index.html", "Home", "home"),
    ("graph.html", "Graph", "graph"),
    ("settings/index.html", "Settings", "settings"),
    ("papers/index.html", "Papers", "papers"),
    ("gaps.html", "Gaps", "gaps"),
    ("search.html", "Search", "search"),
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
    if it.get("inf") and it.get("orig_expr") and str(it["orig_expr"]) != str(canon):
        pairs.append(("In source setting", f"<code>{e(str(it['orig_expr']))}</code>"))
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


def result_badges(r: dict, extra: str = "", lead: str = "") -> str:
    out = [lead] if lead else []
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


def alg_html(it: dict) -> str:
    r = it["r"]
    if it.get("alg"):
        full = it["alg"]
        tip = full + (f" (also: {', '.join(it['alg_aliases'][:4])})" if it.get("alg_aliases") else "")
        return f'<span class="alg" title="{e(tip, quote=True)}">{e(short(full))}</span>'
    if r.get("algorithm_class"):
        return f'<span class="muted" title="{e(str(r["algorithm_class"]), quote=True)}">{e(short("class: " + str(r["algorithm_class"])))}</span>'
    return '<span class="muted">any algorithm</span>' if (r.get("side") or "") == "lower" else NONE


def source_html(r: dict) -> str:
    src = r.get("source") or {}
    num = str(src.get("number") or src.get("label") or "source")
    if src.get("quote"):
        return (f'<details class="pop"><summary>{e(num)}</summary>'
                f'<blockquote>{e(str(src["quote"]))}</blockquote></details>')
    return e(num)


def paper_html(site: Site, pid: str, root: str) -> str:
    return f'<a href="{root}papers/{slugify(pid)}.html" title="{e(site.title(pid), quote=True)}">{e(site.cite(pid))}</a>'


def group_row(q, ncol: int) -> str:
    return f'<tr class="group"><th colspan="{ncol}">{e(QUANTITY_LABEL.get(q, label(q) or "Unspecified quantity"))}</th></tr>'


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
            body.append(group_row(q, ncol))
        alg, source = alg_html(it), source_html(r)
        cells = [bound_html(r) + result_badges(r, result_details(it)), alg, paper_html(site, pid, root), source]
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


# ---------------------------------------------------------------- inherited bounds (data/canonical/inferred.json)


def subst_html(rec: dict) -> str:
    """{d: K} -> d ↦ K for a reduction map (parameters fixed in the special case are listed as changes)."""
    fixed = {}
    for c in rec.get("changes") or []:
        if c.get("kind") == "parameter" and isinstance(c.get("special"), dict):
            fixed.update({str(k): str(v) for k, v in c["special"].items()})
    out = []
    for sym, val in (rec.get("substitutions") or {}).items():
        try:
            lhs, rhs = bounds.symbol_tex(sym), bounds.expr_tex(str(val))
        except Exception:  # noqa: BLE001
            lhs, rhs = sym, str(val)
        if fixed.get(sym) == str(val):
            continue  # a fixed parameter is already shown in the changed-dimension list
        out.append(math(f"{lhs} \\mapsto {rhs}"))
    return ", ".join(out)


def derivation_change(c: dict, upper: bool) -> str:
    """One changed dimension, written in the direction the bound travels (source → this setting)."""
    d, kind = c.get("dim", ""), c.get("kind")

    def v(x):
        if kind == "parameter":
            return pretty_vars(", ".join(f"{k} = {y}" for k, y in x.items())) if x else "any"
        if isinstance(x, list):
            return value_label(d, x) if x else "none"
        return value_label(d, x) if x not in (None, "") else "none"

    name = "fixed parameters" if kind == "parameter" else dim_label(d)
    if kind == "subset":  # multi-valued: the special case adds elements; show only the difference
        extra = [x for x in c.get("special") or [] if x not in (c.get("general") or [])]
        sign = "+" if upper else "drop"
        return f'<span class="dim">{e(name)}:</span> {sign} {e(value_label(d, extra) if d != "learner_knows" else pretty_vars(", ".join(extra)))}'
    src, dst = (c.get("general"), c.get("special")) if upper else (c.get("special"), c.get("general"))
    red = ' <span class="badge muted-badge" title="cross-value reduction with a parameter map">reduction</span>' if kind == "reduction" else ""
    return f'<span class="dim">{e(name)}:</span> {e(v(src))} <span class="arrow">→</span> {e(v(dst))}{red}'


def derivation_html(site: Site, it: dict, root: str) -> str:
    rec = it["inf"]
    upper = rec.get("rule", "").startswith("upper")
    src = site.nodes[rec["from_setting"]]
    rel = "more general" if upper else "special case"
    changes = rec.get("changes") or []
    # A reduction drags along action_set fields (e.g. finite shape -> not applicable): fold them away.
    folded = [c for c in changes if any(x.get("kind") == "reduction" for x in changes)
              and c.get("dim", "").startswith("action_set.")]
    via = "".join(f"<li>{derivation_change(c, upper)}</li>" for c in changes if c not in folded)
    h = it.get("hops", 99)
    steps = "immediate" if h == 1 else f"{h} steps {'up' if upper else 'down'}" if h < 99 else ""
    steps = f' <span class="hops" title="covering edges between the two settings">({steps})</span>' if steps else ""
    out = [f'<div class="from">from <a href="{root}settings/{src["slug"]}.html" title="{rel}">{e(src["name"])}</a>{steps}</div>',
           f'<ul class="via">{via}</ul>']
    subs = subst_html(rec)
    if subs:
        out.append(f'<div class="subs">substitute {subs}</div>')
    extra = []
    if rec.get("caveats"):
        extra.append(("Caveats", "<ul>" + "".join(f"<li>{e(str(c))}</li>" for c in rec["caveats"]) + "</ul>"))
    if it.get("also"):
        extra.append(("Also from", "<ul>" + "".join(
            f'<li><a href="{root}settings/{site.nodes[a["inf"]["from_setting"]]["slug"]}.html">'
            f'{e(site.nodes[a["inf"]["from_setting"]]["name"])}</a></li>' for a in it["also"]) + "</ul>"))
    if folded:
        extra.append(("Also changes", "<ul>" + "".join(f"<li>{derivation_change(c, upper)}</li>" for c in folded) + "</ul>"))
    extra.append(("Rule", e("upper bound on a generalisation holds on this special case" if upper
                            else "lower bound on a special case holds on this generalisation")))
    extra.append(("Derived id", f'<code>{e(str(rec.get("id")))}</code>'))
    n_cav = len(rec.get("caveats") or [])
    summ = f"caveats ({n_cav})" if n_cav else "derivation"
    out.append(f'<details class="more{" cav" if n_cav else ""}"><summary>{summ}</summary>{dl(extra, "kv")}</details>')
    return "".join(out)


def sort_inherited(site: Site, items: list[dict]) -> list[dict]:
    dep = {"worst_case": 0, "instance_dependent": 1}
    return sorted(items, key=lambda it: (quantity_rank(site, it["r"].get("quantity")),
                                         dep.get(it["r"].get("dependence"), 2),
                                         it["dist"], len(it["inf"].get("caveats") or []),
                                         str((it["r"].get("bound") or {}).get("notation")),
                                         -(site.paper_info(it["paper"]).get("year") or 0)))


PINNED = re.compile(r"^holds for (.+?=.+?) only$")


def pinned(it: dict) -> list[str]:
    """Parameter values the source bound was proved for only (caveat 'holds for K = 2 only'): valid here, but weak."""
    return [m.group(1) for c in it["inf"].get("caveats") or [] if (m := PINNED.match(str(c).strip()))]


def inherited_table(items: list[dict], site: Site, root: str, weak: bool = False) -> str:
    headers = ["Bound", "Derived from", "Algorithm", "Paper", "Source"]
    body, current = [], object()
    for it in sort_inherited(site, items):
        r = it["r"]
        q = r.get("quantity")
        if q != current:
            current = q
            body.append(group_row(q, len(headers)))
        tag = badge("inherited", "inh", "derived along the specialisation order; not proved for this setting directly")
        for pv in pinned(it):
            tag += badge(f"pinned {pretty_vars(pv)}", "pinned",
                         f"the source bound was proved only for {pv}; it holds here but says nothing about other values")
        cells = [bound_html(r) + result_badges(r, result_details(it), lead=tag), derivation_html(site, it, root),
                 alg_html(it), paper_html(site, it["paper"], root), source_html(r)]
        tds = "".join(f'<td class="c-{slugify(h)}" data-label="{h}">{c}</td>' for h, c in zip(headers, cells))
        body.append(f'<tr class="inh{" weak" if weak else ""}">{tds}</tr>')
    th = "".join(f'<th class="c-{slugify(h)}">{h}</th>' for h in headers)
    return (filter_box("Filter by algorithm, paper, source setting…") +
            f'<div class="scroll"><table class="results inherited filterable{" weak" if weak else ""}">'
            f'<thead><tr>{th}</tr></thead><tbody>\n' + "\n".join(body) + "\n</tbody></table></div>")


def inherited_section(site: Site, items: list[dict], side: str, anchor: str) -> str:
    if not items:
        return ""
    upper = side == "upper"
    title = "Inherited upper bounds" if upper else "Inherited lower bounds"
    whence = "from more general settings" if upper else "from special cases"
    hint = ("Upper bounds proved on a more general setting hold here too, after the parameter map and any fixed "
            "parameters are substituted." if upper else
            "Lower bounds proved on a special case hold here too (the hard instances are still available).")
    nsrc = len({it["inf"]["from_setting"] for it in items})
    strong = [it for it in items if not pinned(it)]
    weak = [it for it in items if pinned(it)]
    vals = sorted({pretty_vars(v) for it in weak for v in pinned(it)})
    nweak = f' <span class="weak-n">· {len(weak)} weak</span>' if weak else ""
    weak_html = f"""
<details class="weak-sec"{"" if strong else " open"}>
<summary>Weak transfers <span class="muted">({len(weak)}) · proved only for {e(", ".join(vals))}</span></summary>
<p class="hint">The source bound was proved for one pinned parameter value (e.g. a two-armed instance). It still holds
here, but it is usually far weaker than the bounds above and says nothing about how the bound scales with that parameter.</p>
{inherited_table(weak, site, "../", weak=True)}
</details>""" if weak else ""
    main = inherited_table(strong, site, "../") if strong else '<p class="muted">Only weak transfers (below).</p>'
    return f"""
<details class="inherited-sec" id="{anchor}">
<summary><h2>{title} <span class="muted">{whence}</span></h2><span class="count">{len(items)} from {nsrc} setting{"s" if nsrc != 1 else ""}{nweak}</span></summary>
<p class="hint">{hint} Derived automatically by <code>pipeline/infer.py</code> and <b>never proved for this setting
directly</b>; check the caveats. Closest sources (fewest changed assumptions) are listed first within each group.</p>
{main}{weak_html}
</details>"""


def split_sides(items):
    up = [i for i in items if (i["r"].get("side") or "").lower() == "upper"]
    lo = [i for i in items if (i["r"].get("side") or "").lower() == "lower"]
    other = [i for i in items if i not in up and i not in lo]
    return up, lo, other


# ---------------------------------------------------------------- pages


def home_page(site: Site) -> str:
    n_res = sum(len(n["results"]) for n in site.nodes.values())
    n_inh = sum(len(n["inherited"]) for n in site.nodes.values())
    iu = sum(site.counts(n, "inherited")[0] for n in site.nodes.values())
    n_ex = sum(1 for pid in site.paper_ids() if pid in site.extractions)
    n_dir = sum(1 for x in site.edges if x["kind"] != "neighbour")
    tiles = [
        ("papers/index.html", len(site.paper_ids()), "papers", f"{n_ex} extracted"),
        ("settings/index.html", len(site.nodes), "canonical settings", "assumption vectors"),
        ("settings/index.html", n_res, "results", "upper and lower bounds"),
        *([("settings/index.html", f"+{n_inh}", "inherited bounds", f"{iu} upper, {n_inh - iu} lower")] if n_inh else []),
        ("graph.html", n_dir, "specialisation edges", f"{len(site.edges) - n_dir} other neighbours"),
    ]
    tiles_html = "".join(f'<a class="tile" href="{h}"><b>{n}</b><span>{lbl}</span><small>{sub}</small></a>'
                         for h, n, lbl, sub in tiles)
    A = site.analysis
    if A.ok:
        from collections import Counter
        st = Counter(c["status"] for c in A.cells)
        n_sugg = sum(len(t["suggestions"]) for t in A.transfer)
        atiles = [
            ("gaps.html", st["poly_gap"] + st["log_gap"] + st["conflict"], "open-looking gaps",
             f'{st["poly_gap"]} poly · {st["log_gap"]} log' + (f' · {st["conflict"]} conflicts' if st["conflict"] else "")),
            ("gaps.html#status=no_lower", st["no_lower"] + st["no_upper"], "one-sided cells", f'{st["no_lower"]} no lower · {st["no_upper"]} no upper'),
            ("settings/index.html", st["tight"], "tight cells", f"of {len(A.cells)} setting × regime cells"),
            ("neighbours.html", len(A.unstudied), "unstudied neighbours", "one step from studied settings"),
            ("transfer.html", n_sugg, "technique transfers", f"suggested for {len(A.transfer)} cells"),
            ("redundant.html", len(A.redundant), "implied results", "rate already implied by earlier work"),
        ]
        tiles_html += ('</div><h2 class="tiles-h">Analysis <span class="muted small">(setting × regime cells, '
                       'compared by growth exponents)</span></h2><div class="tiles">'
                       + "".join(f'<a class="tile an" href="{h}"><b>{n}</b><span>{lbl}</span><small>{sub}</small></a>'
                                 for h, n, lbl, sub in atiles))
    analysis_cards = """
<a class="card" href="gaps.html"><h2>Gaps →</h2><p>Settings where the best upper and lower bounds don't match, with triage verdicts and transfer suggestions.</p></a>
<a class="card" href="search.html"><h2>Search →</h2><p>Faceted search over settings and bounds, with saved queries.</p></a>
<a class="card" href="neighbours.html"><h2>Unstudied neighbours →</h2><p>Settings one assumption away from well-studied ones, with no results yet.</p></a>
<a class="card" href="transfer.html"><h2>Technique transfer →</h2><p>Algorithm families that close the rate next door but are not tried here.</p></a>
<a class="card" href="redundant.html"><h2>Redundancy →</h2><p>Results whose rate an earlier, more general result already implied.</p></a>""" if A.ok else ""
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
<a class="card" href="papers/index.html"><h2>Papers →</h2><p>The corpus: what each paper proves, theorem by theorem.</p></a>
{analysis_cards}
<a class="card" href="ground-truth.html"><h2>Ground truth →</h2><p>Hand-curated bandit convex optimisation reference{"" if site.bco else " (not yet available)"},
and the pilot facts the graph should rediscover.</p></a>
</div>
<p class="muted small">Ontology {e(site.onto.version)}{" · canonical layer (data/canonical)" if site.canonical else " · grouped from raw extractions"}.
Bounds are shown in canonical notation; the paper's own LaTeX is under each result's <em>details</em>.
{"Inherited bounds are propagated along the specialisation order by <code>pipeline/infer.py</code> and shown separately, with their derivation." if n_inh else "No bounds are inferred yet."}
{"Bounds are compared by their growth exponents (<code>pipeline/compare.py</code>) for the gap analysis." if A.ok else "No bounds are compared yet."}</p>
"""
    return page("Home", body, "", "home")


PALETTE_SLOTS = 8


def colour_slots(values: list[str]) -> dict[str, int]:
    """Fixed categorical slot per value, ordered by frequency; overflow folds into 'other' (slot 0)."""
    from collections import Counter

    c = Counter(values)
    ranked = [v for v, _ in c.most_common()]
    return {v: (i + 1 if i < PALETTE_SLOTS else 0) for i, v in enumerate(ranked)}


def count_cell(own: int, inh: int) -> str:
    """'33 +12' with the inherited part muted; own count first."""
    o = str(own) if own else NONE
    return o + (f' <span class="inh-n" title="{inh} inherited along the specialisation order">+{inh}</span>' if inh else "")


def settings_index(site: Site) -> str:
    act_slots = colour_slots([n["key"].get("action_space", "") for n in site.nodes.values()])
    A = site.analysis
    rows = []
    for n in sorted(site.nodes.values(), key=lambda n: (-len(n["results"]), n["name"])):
        up, lo = site.counts(n)
        iu, il = site.counts(n, "inherited")
        k = n["key"]
        env, act = k.get("environment", ""), k.get("action_space", "")
        st, reg = A.setting_status(n["id"])
        st_cell = (f'<td data-label="Status">{analysis.status_badge(sys.modules[__name__], st, analysis.regime_label(reg) if reg else "")}</td>'
                   if A.ok else "")
        rows.append(
            f'<tr data-status="{st}" data-environment="{e(value_label("environment", env) if env else "unspecified")}" '
            f'data-action_space="{e(value_label("action_space", act) if act else "unspecified")}" data-n="{len(n["results"])}">'
            f'<td data-label="Setting"><span class="dot s{act_slots.get(act, 0)}" aria-hidden="true"></span>'
            f'<a href="{n["slug"]}.html">{e(n["name"])}</a></td>{st_cell}'
            f'<td class="num" data-label="Upper">{count_cell(up, iu)}</td><td class="num" data-label="Lower">{count_cell(lo, il)}</td>'
            f'<td class="num" data-label="Papers">{len(n["papers"])}</td></tr>'
        )
    status_select = ""
    if A.ok:
        from collections import Counter
        cnt = Counter(A.setting_status(n["id"])[0] for n in site.nodes.values())
        opts = "".join(f'<option value="{k}">{e(analysis.STATUS[k][0])} ({cnt[k]})</option>' for k in analysis.STATUS_RANK if cnt[k])
        status_select = (f'<label class="fsel"><span>Status</span><select id="status-filter" title="Status in the regret · '
                         f'worst-case regime, else the most relevant regime"><option value="">all</option>{opts}</select></label>')
    body = f"""
<h1>Settings</h1>
<p class="lede">{len(site.nodes)} canonical settings. A name lists only the assumptions that differ from the plain
stochastic-regret defaults (bandit feedback, no context, no extras). Also see the <a href="../graph.html">graph</a>.</p>
{'<p class="small muted">Counts are bounds extracted for the setting itself; <span class="inh-n">+n</span> are inherited along the specialisation order (upper bounds from more general settings, lower bounds from special cases).</p>' if site.canonical else ""}
<div class="toolbar">
{filter_box("Filter settings…")}
<div class="seg" role="group" aria-label="Group by">
<span>Group by</span>
<button type="button" data-group="action_space" aria-pressed="true">Action space</button>
<button type="button" data-group="environment" aria-pressed="false">Environment</button>
<button type="button" data-group="" aria-pressed="false">None</button>
</div>
{status_select}
</div>
<div class="scroll"><table class="settings filterable groupable">
<thead><tr><th>Setting</th>{'<th>Status</th>' if A.ok else ""}<th class="num">Upper</th><th class="num">Lower</th><th class="num">Papers</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>
{'<p class="small muted">Status: tightness in the regret · worst-case regime when the setting has one, else its most relevant regime; see <a href="../gaps.html">Gaps</a>.</p>' if A.ok else ""}
"""
    return page("Settings", body, "../", "settings", head='<script defer src="../static/analysis.js"></script>' if A.ok else "")


def change_html(x: dict) -> str:
    def one(d, fv, tv):
        v = lambda s: e(value_label(d, s) if s else "none")
        return f'<span class="dim">{e(dim_label(d))}</span> {v(fv)} <span class="arrow">→</span> {v(tv)}'

    def informative(d, fv, tv):
        lab = lambda s: value_label(d, s) if s else "none"
        if lab(fv) == lab(tv):
            return False  # e.g. "none -> none" after flattening
        if "." in d and "not_applicable" in (fv, tv):
            return False  # node field irrelevant on one side: implied by the governing dimension
        return True

    changes = x.get("changes") or [(x["dim"], x["from"], x["to"])]
    shown = [c for c in changes if informative(*c)] or changes[:1]
    return "<br>".join(one(*c) for c in shown)


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
            iu, il = site.counts(m, "inherited")
            inh = f' <span class="inh-n" title="inherited">(+{iu}↑ +{il}↓)</span>' if iu or il else ""
            kind = ' <span class="badge muted-badge" title="reduction (e.g. K-armed as linear with d = K)">reduction</span>' if x["kind"] == "reduction" else ""
            lis.append(f'<li><a href="{m["slug"]}.html">{e(m["name"])}</a>'
                       f'<div class="chg">{change_html(x)}{kind} <span class="cnt">{up}↑ {lo}↓{inh}</span></div></li>')
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
    iup, ilo, _ = split_sides(n.get("inherited") or [])
    inh = f' · inherited: <a href="#inherited-upper"><b>{len(iup)}</b> upper</a> · <a href="#inherited-lower"><b>{len(ilo)}</b> lower</a>' if iup or ilo else ""
    canon_id = f' / <code class="small">{e(n["id"])}</code>' if site.canonical else ""
    body = f"""
<p class="crumbs"><a href="index.html">Settings</a>{canon_id}</p>
<h1>{e(n["name"])}</h1>
<div class="chips">{"".join(chips)}</div>
<p class="summary"><b>{len(up)}</b> upper · <b>{len(lo)}</b> lower bounds from <b>{len(n["papers"])}</b> paper{"s" if len(n["papers"]) != 1 else ""}{inh}.</p>
<h2 id="neighbours">Neighbourhood</h2>{neighbourhood(site, n)}
{rates_section(site, n)}
<h2 id="upper">Upper bounds <span class="muted">({len(up)})</span></h2>{results_table(up, site, "../")}
<h2 id="lower">Lower bounds <span class="muted">({len(lo)})</span></h2>{results_table(lo, site, "../")}
{inherited_section(site, iup, "upper", "inherited-upper")}
{inherited_section(site, ilo, "lower", "inherited-lower")}
{f'<h2>Other <span class="muted">({len(other)})</span></h2>' + results_table(other, site, "../") if other else ""}
<h2 id="papers">As stated in papers</h2>{table(["Paper", "Name in paper", "Learner knows", "Unmapped"], inst_rows, "compact")}
"""
    head = '<script defer src="../static/plots.js"></script>' if site.analysis.by_setting.get(n["id"]) else ""
    return page(n["name"], body, "../", "settings", head=head)


def rates_section(site: Site, n: dict) -> str:
    """Status per regime, rate plot and rate plane (static/plots.js) from site_index.json."""
    A = site.analysis
    data = A.plot_data(n) if A.ok else None
    if not data:
        return ""
    h = sys.modules[__name__]
    pages = analysis.Pages(site, A, h)
    cells = sorted(A.cells_by_setting.get(n["id"]) or [], key=lambda c: (c["regime"] != "regret|worst_case", c["regime"]))
    rows = []
    for c in cells:
        tri = analysis.triage_badge(h, c.get("triage")) if c["status"] in analysis.GAP_STATUSES else ""
        rows.append(f'<li>{analysis.status_badge(h, c["status"])} <span class="reg-l">{e(analysis.regime_label(c["regime"]))}</span>'
                    f' {tri}{pages.per_var_html(c.get("per_var") or {})}</li>')
    strip = (f'<ul class="cellstrip">{"".join(rows)}</ul>' if rows else
             '<p class="muted small">No regime has bounds with a usable rate profile, so no tightness status.</p>')
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""
<h2 id="rates">Rates</h2>
<p class="hint muted small">Tightness per regime (quantity family × dependence) from the bounds' growth exponents;
↑ upper / ↓ lower exponent of each variable (1/Δ for the gap). <a href="../gaps.html">All gaps →</a></p>
{strip}
<div class="rateplot" id="rateplot"><noscript><p class="muted">The rate plot needs JavaScript.</p></noscript></div>
<script type="application/json" id="plot-data">{blob}</script>"""


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


# ---------------------------------------------------------------- ground truth (data/ground_truth/bco.yaml)

# The book's LaTeX macros (cvx.tex), so KaTeX can render its notation, compute column and quotes.
BCO_MACROS = {
    r"\cF": r"\mathcal{F}", r"\sF": r"\mathscr{F}", r"\pb": r"\mathtt{b}", r"\pl": r"\mathtt{l}",
    r"\psm": r"\mathtt{sm}", r"\psc": r"\mathtt{sc}", r"\plin": r"\mathtt{lin}", r"\pquad": r"\mathtt{quad}",
    r"\ps": r"\mathtt{s}", r"\pu": r"\mathtt{i}", r"\R": r"\mathbb{R}", r"\E": r"\mathbb{E}",
    r"\eps": r"\varepsilon", r"\ball": r"\mathbb{B}", r"\conv": r"\operatorname{conv}",
    r"\diam": r"\operatorname{diam}", r"\poly": r"\operatorname{poly}", r"\Reg": r"\mathrm{Reg}",
    r"\sReg": r"\mathrm{sReg}", r"\norm": r"\left\|#1\right\|", r"\ISO": r"\textsf{iso}", r"\iso": r"\textsf{iso}",
    r"\optsc": r"\textsf{optsc}", r"\svd": r"\textsf{svd}", r"\ellipsoid": r"\textsf{ellipsoid}",
    r"\cog": r"\textsf{cog}", r"\inscribed": r"\textsf{inscribed}", r"\low": r"\textsf{lowner}",
}
GT_DIMS = ["environment", "domain", "feedback", "dimension", "noise"]
GT_HORIZON = re.compile(r"(?<![A-Za-z_])n(?![A-Za-z_0-9])")  # the book's horizon n is canonical T
GT_WRAPPED = re.compile(r"^\s*(O_tilde|Omega_tilde|Theta_tilde|O|Omega|Theta)\((.*)\)\s*$")


def gt_n_to_t(expr) -> str:
    return GT_HORIZON.sub("T", str(expr))


def gt_bound(r: dict) -> str:
    """bound.expression (n -> T) via bounds.py; the book's expression_latex if that fails."""
    b = dict(r.get("bound") or {})
    if b.get("expression"):
        b["expression"] = gt_n_to_t(b["expression"])
    return bound_html({**r, "bound": b})


def gt_formula(s, side: str) -> str:
    """A free-form bound string from open_problems: 'Omega(d*sqrt(n))' -> formula, anything else -> text."""
    if s in (None, ""):
        return NONE
    m = GT_WRAPPED.match(str(s))
    if m:  # 'Omega(...) simple regret': the balanced wrapper is the bound, the rest a note
        depth, end = 0, None
        for i, ch in enumerate(s, start=0):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        inner, rest = s[s.index("(") + 1:end], s[end + 1:].strip() if end else ""
        tex, ok = bounds.bound_tex({"expression": gt_n_to_t(inner), "notation": m.group(1)}, side, None)
        if ok and end:
            note = f'<span class="muted small">{e(rest)}</span>' if rest else ""
            return f'<div class="formula">{math(tex)}</div>{note}'
    return f'<span class="small">{e(str(s))}</span>'


def gt_nota(s: dict) -> str:
    """The book's class notation, or the plain-text name when the LaTeX field is really prose."""
    tex = str(s.get("notation_latex") or "")
    if not tex or re.search(r"(?<![\\A-Za-z])[A-Za-z]{4,}", tex):
        return f'<span class="nota-plain">{e(str(s.get("notation_plain") or s.get("id")))}</span>'
    return math(tex)


def gt_setting_link(sid, sets: dict) -> str:
    s = sets.get(sid)
    if not s:
        return e(str(sid))
    return (f'<a class="gt-set" href="#s-{slugify(sid)}" title="{e(str(s.get("notation_plain") or sid), quote=True)}">'
            f'{gt_nota(s)}</a> <code class="small muted">{e(sid)}</code>')


def gt_chips(av: dict, params=None) -> str:
    chips = []
    fc = av.get("function_class")
    if isinstance(fc, dict):
        on = [label(k) for k, v in fc.items() if v is True and k != "convex"]
        chips.append(f'<span class="chip"><b>class</b> convex{", " + e(", ".join(on)) if on else ""}</span>')
    for d in GT_DIMS + [k for k in av if k not in GT_DIMS and k != "function_class"]:
        v = av.get(d)
        if v in (None, "", [], {}):
            continue
        shown = ", ".join(map(str, v)) if isinstance(v, list) else str(v)
        chips.append(f'<span class="chip"><b>{e(label(d))}</b> {e(label(shown))}</span>')
    if params:
        chips.append(f'<span class="chip"><b>parameters</b> {e(", ".join(map(str, as_list(params))))}</span>')
    return '<div class="chips">' + "".join(chips) + "</div>"


def gt_settings(settings: list[dict]) -> str:
    cards = []
    for s in settings:
        sid = str(s.get("id"))
        extra = []
        if s.get("definition_quote"):
            extra.append(("Definition", f'<blockquote>{e(str(s["definition_quote"]))}</blockquote>'))
        if isinstance(s.get("ontology_v0_1_mapping"), dict):
            extra.append(("Ontology v0.1", text(s["ontology_v0_1_mapping"])))
        if s.get("unmapped"):
            extra.append(("Unmapped", '<ul class="tight">' + "".join(f"<li>{e(str(u))}</li>" for u in as_list(s["unmapped"])) + "</ul>"))
        for k in ("definition_source", "notes"):
            if s.get(k):
                extra.append((label(k).capitalize(), text(s[k])))
        used = " ".join(f'<a href="#r-{slugify(u)}">{e(str(u))}</a>' for u in as_list(s.get("used_in")))
        conf = s.get("confidence")
        cards.append(f"""<article class="fact gt-setting" id="s-{slugify(sid)}">
<header><span class="gt-nota">{gt_nota(s)}</span> <code class="small muted">{e(sid)}</code>
{badge(f"{conf} confidence", f"conf-{conf}") if conf in ("low", "medium") else ""}
{badge("not in tables", "muted-badge") if s.get("in_tables") is False else ""}</header>
{f'<p class="small muted">{e(str(s["name_in_book"]))}</p>' if s.get("name_in_book") else ""}
{gt_chips(s.get("assumption_vector") or {}, s.get("parameters"))}
{f'<p class="small">Results: {used}</p>' if used else ""}
<details class="more"><summary>definition and mapping</summary>{dl(extra, "kv")}</details>
</article>""")
    return filter_box("Filter settings…") + '<div class="facts gt-open filterable-cards">' + "".join(cards) + "</div>"


def gt_citation(r: dict) -> str:
    c = r.get("original_citation") or {}
    authors = as_list(c.get("authors"))
    who = (surname(authors[0]) + (" et al." if len(authors) > 2 else f" and {surname(authors[1])}" if len(authors) == 2 else "")
           ) if authors else ""
    year = f" ({c['year']})" if c.get("year") else ""
    tip = e(str(c.get("title") or ""), quote=True)
    if not who:
        return f'<span class="muted small" title="{tip}">{e(short(str(c.get("title") or "–"), 40))}</span>'
    key = f'<code class="raw">{e(str(c["bib_key"]))}</code>' if c.get("bib_key") else ""
    return f'<span title="{tip}">{e(who)}{e(year)}</span>{key}'


def gt_book(r: dict) -> str:
    t = r.get("book_theorem")
    ch = f'<span class="muted small">Ch. {e(str(r["book_chapter"]))}</span>' if r.get("book_chapter") else ""
    if not isinstance(t, dict):
        return ch or NONE
    quote = "\n".join(x for x in (t.get("statement_summary"), f"Assumptions: {t['assumptions']}" if t.get("assumptions") else "") if x)
    num = e(str(t.get("number") or "theorem"))
    head = f'<details class="pop"><summary>{num}</summary><blockquote>{e(quote)}</blockquote></details>' if quote else num
    return head + ch


def gt_details(r: dict) -> str:
    b = r.get("bound") or {}
    pairs = []
    if b.get("regime"):
        pairs.append(("Regime", text(b["regime"])))
    if r.get("constraint_set"):
        pairs.append(("Constraint set", math(r["constraint_set"])))
    if r.get("extra_assumptions"):
        pairs.append(("Assumptions", '<ul class="tight">' + "".join(f"<li>{e(str(x))}</li>" for x in as_list(r["extra_assumptions"])) + "</ul>"))
    pairs.append(("Quantity", text(label(r.get("quantity")))))
    if r.get("probability"):
        pairs.append(("Probability", text(label(r["probability"]))))
    if b.get("expression"):
        pairs.append(("Canonical", f'<code>{e(str(b["expression"]))}</code> <span class="muted">(n = T)</span>'))
    if b.get("expression_latex"):
        pairs.append(("Book's LaTeX", math(b["expression_latex"], "paper") + f'<code class="raw">{e(str(b["expression_latex"]))}</code>'))
    if r.get("symbols"):
        pairs.append(("Symbols", '<ul class="tight">' + "".join(f"<li><code>{e(str(k))}</code>: {e(str(v))}</li>" for k, v in r["symbols"].items()) + "</ul>"))
    for k in ("erratum", "derivation", "notes"):
        if r.get(k):
            pairs.append((k.capitalize(), text(r[k])))
    for c in as_list(r.get("conflicts")):
        if isinstance(c, dict):
            pairs.append((f"Conflict ({c.get('where', '')})", f'<blockquote>{e(str(c.get("quote") or c))}</blockquote>'))
    return f'<details class="more"><summary>details</summary>{dl(pairs, "kv")}</details>'


def gt_results(results: list[dict], side: str, sets: dict) -> str:
    rows = [r for r in results if (r.get("side") or "").lower() == side]
    if not rows:
        return '<p class="muted">None.</p>'
    cols = ["Setting", "Bound", "Algorithm", "Original", "Compute", "Book", "Source"]
    if not any(r.get("compute") for r in rows):
        cols.remove("Compute")
    if not any(r.get("book_theorem") or r.get("book_chapter") for r in rows):
        cols.remove("Book")
    # Table rows first (book order), then bounds quoted from the text; grouped by quantity.
    qs = list(dict.fromkeys(r.get("quantity") for r in rows))
    body = []
    for q in qs:
        body.append(group_row(q, len(cols)) if q in QUANTITY_LABEL else
                    f'<tr class="group"><th colspan="{len(cols)}">{e(label(q).capitalize())}</th></tr>')
        for r in sorted((r for r in rows if r.get("quantity") == q), key=lambda r: r.get("in_tables") is False):
            extra = []
            if r.get("in_tables") is False:
                extra.append(badge("text, not table", "muted-badge", str((r.get("source") or {}).get("number") or "")))
            if r.get("non_constructive"):
                extra.append(badge("non-constructive", "muted-badge"))
            if r.get("erratum"):
                extra.append(badge("erratum", "conf-medium", str(r["erratum"])))
            if r.get("conflicts"):
                extra.append(badge("conflict", "conf-low"))
            if r.get("derived"):
                extra.append(badge("derived", "inh"))
            lead = badge(str(r.get("id")), "nota")
            alg = (f'<span class="alg" title="{e(str(r["algorithm"]), quote=True)}">{e(short(str(r["algorithm"]), 48))}</span>'
                   if r.get("algorithm") else alg_html({"r": r}))
            comp = r.get("compute")
            cells = {
                "Setting": gt_setting_link(r.get("setting"), sets),
                "Bound": gt_bound(r) + result_badges(r, "".join(extra) + gt_details(r), lead=lead),
                "Algorithm": alg,
                "Original": gt_citation(r),
                "Compute": ", ".join(math(x) for x in re.split(r",\s*(?![^()]*\))", str(comp))) if comp else NONE,
                "Book": gt_book(r),
                "Source": source_html(r),
            }
            tds = "".join(f'<td class="c-{slugify(h)}" data-label="{h}">{cells[h]}</td>' for h in cols)
            body.append(f'<tr id="r-{slugify(str(r.get("id")))}">{tds}</tr>')
    th = "".join(f'<th class="c-{slugify(h)}">{h}</th>' for h in cols)
    return (filter_box("Filter by setting, algorithm, citation…") +
            f'<div class="scroll"><table class="results gt filterable">'
            f'<thead><tr>{th}</tr></thead><tbody>\n' + "\n".join(body) + "\n</tbody></table></div>")


def gt_side_spec(v) -> str:
    if isinstance(v, dict):
        return ", ".join(f"{label(k)}: {', '.join(map(str, x)) if isinstance(x, list) else x}" for k, x in v.items())
    return "" if v is None else str(v)


def gt_rules(rules: list[dict]) -> str:
    shown = {"id", "kind", "from_setting", "to_setting", "transfers", "reverse_transfers", "statement", "quote",
             "supporting_quote", "quote_source", "section", "confidence", "order"}
    items = []
    for t in rules:
        tr = str(t.get("transfers") or "")
        head = tr.split(" ", 1)[0]
        cls = {"lower": "worst", "upper": "inst"}.get(head, "")
        pairs = [(label(k).capitalize(), text(v))
                 for k, v in t.items() if k not in shown and v not in (None, "")]
        if t.get("reverse_transfers"):
            pairs.insert(0, ("Reverse", text(t["reverse_transfers"])))
        if " " in tr:
            pairs.insert(0, ("Transfers", text(tr)))
        q = "".join(f'<p class="small muted">{e(lbl)}</p><blockquote>{e(str(t[k]))}</blockquote>'
                    for k, lbl in (("quote", "Quote"), ("supporting_quote", "Supporting quote")) if t.get(k))
        conf = t.get("confidence")
        items.append(f"""<li class="rule" id="t-{slugify(str(t.get("id")))}">
<div class="rule-head"><code>{e(str(t.get("id")))}</code> {badge(label(t.get("kind")))} {badge(head + " bounds" if head in ("lower", "upper", "both") else head, cls)}
{badge(f"{conf} confidence", f"conf-{conf}") if conf in ("low", "medium") else ""}
<span class="muted small">{e(str(t.get("section") or ""))}</span></div>
<div class="rule-ft"><span class="from">{e(gt_side_spec(t.get("from_setting")))}</span> <span class="arrow">→</span> <span class="to">{e(gt_side_spec(t.get("to_setting")))}</span>
{f'<span class="muted small">({e(str(t["order"]))})</span>' if t.get("order") else ""}</div>
<p>{e(str(t.get("statement") or ""))}</p>
{f'<details class="more"><summary>scope and parameters</summary>{dl(pairs, "kv")}</details>' if pairs else ""}
{f'<details class="more"><summary>quote{"s" if t.get("supporting_quote") else ""}</summary>{q}</details>' if q else ""}
</li>""")
    return filter_box("Filter rules…") + '<ul class="rules filterable-cards">' + "".join(items) + "</ul>"


def gt_known(v, side: str, sets: dict) -> str:
    if isinstance(v, dict):
        return "".join(f'<div class="kb"><a class="small" href="#s-{slugify(k)}">{gt_nota(sets[k]) if k in sets else e(k)}</a>'
                       f'{gt_formula(x, side)}</div>' for k, x in v.items())
    return gt_formula(v, side)


def gt_open(problems: list[dict], sets: dict) -> str:
    cards = []
    for o in problems:
        ss = o.get("settings")
        if ss == "all":
            slinks = '<span class="chip">all settings</span>'
        else:
            slinks = "".join(f'<a class="chip" href="#s-{slugify(s)}">{gt_nota(sets[s]) if s in sets else e(s)}</a>'
                             for s in as_list(ss))
        lo, up = o.get("known_lower_bound"), o.get("known_upper_bound")
        bnds = (f'<div class="ul2"><div><span class="side">Known lower</span>{gt_known(lo, "lower", sets)}</div>'
                f'<div><span class="side">Known upper</span>{gt_known(up, "upper", sets)}</div></div>') if lo or up else ""
        rel = " ".join(f'<a href="#r-{slugify(x)}">{e(str(x))}</a>' for x in as_list(o.get("related_results")))
        conf = o.get("confidence")
        quote = "".join(f'<blockquote>{e(str(o[k]))}</blockquote>' for k in ("context_quote", "quote") if o.get(k))
        cards.append(f"""<article class="fact" id="op-{slugify(str(o.get("id")))}">
<header><b>{e(str(o.get("id")))}</b> {badge(label(o.get("kind")), "status")}
{badge(f"{conf} confidence", f"conf-{conf}") if conf in ("low", "medium") else ""}
{f'<span class="muted small">{e(str(o["gap_label"]))}</span>' if o.get("gap_label") else ""}</header>
<p>{e(str(o.get("statement") or ""))}</p>
{f'<div class="chips">{slinks}</div>' if slinks else ""}
{bnds}
{f'<p class="small">Related: {rel}</p>' if rel else ""}
{f'<p class="small muted">{e(str(o["notes"]))}</p>' if o.get("notes") else ""}
{f'<details class="more"><summary>quote{" · " + e(str(o["section"])) if o.get("section") else ""}</summary>{quote}</details>' if quote else ""}
</article>""")
    return filter_box("Filter open problems…") + '<div class="facts gt-open filterable-cards">' + "".join(cards) + "</div>"


def gt_source(src: dict) -> str:
    pairs = []
    if src.get("title"):
        pairs.append(("Book", f'<em>{e(str(src["title"]))}</em>, {e(", ".join(map(str, as_list(src.get("authors")))))}'))
    if src.get("arxiv_id"):
        aid = str(src["arxiv_id"])
        pairs.append(("arXiv", f'<a href="https://arxiv.org/abs/{e(aid, quote=True)}{e(str(src.get("arxiv_version") or ""), quote=True)}">'
                               f'{e(aid)}{e(str(src.get("arxiv_version") or ""))}</a> <span class="muted">({e(str(src.get("arxiv_version_date") or ""))})</span>'))
    ex_ = src.get("extraction") or {}
    if ex_:
        pairs.append(("Extraction", f'{e(str(ex_.get("produced_by") or ""))} · status {e(str(ex_.get("status")))} · '
                                    f'human verified: {text(ex_.get("human_verified"))}'))
    conv = src.get("conventions") or {}
    cpairs = []
    for k, v in conv.items():
        if isinstance(v, dict):
            cpairs.append((label(k), dl([(label(a), text(b)) for a, b in v.items()], "kv")))
        elif k.endswith("_quote"):
            cpairs.append((label(k.removesuffix("_quote")), f"<blockquote>{e(str(v))}</blockquote>"))
        else:
            cpairs.append((label(k), text(v)))
    ga = "".join(f'<li><b>{e(str(a.get("number") or a.get("id")))}</b><blockquote>{e(str(a.get("quote") or ""))}</blockquote>'
                 + (f'<p class="small">{e(str(a["note"]))}</p>' if a.get("note") else "") + "</li>"
                 for a in as_list(src.get("global_assumptions")) if isinstance(a, dict))
    tc = src.get("table_conventions") or {}
    tcs = "".join(f'<p><b>{e(label(k))}</b>{": " + e(str(v.get("caption"))) if isinstance(v, dict) and v.get("caption") else ""}</p>'
                  + (f'<blockquote>{e(str(v.get("quote")))}</blockquote>' if isinstance(v, dict) else f"<p>{e(str(v))}</p>")
                  for k, v in tc.items())
    out = dl(pairs)
    if cpairs:
        out += f'<details class="more"><summary>conventions</summary>{dl(cpairs, "kv")}</details>'
    if ga:
        out += f'<details class="more"><summary>global assumptions</summary><ul class="tight gt-ga">{ga}</ul></details>'
    if tcs:
        out += f'<details class="more"><summary>table conventions</summary>{tcs}</details>'
    return out


def ground_truth_page(site: Site) -> str:
    bco = site.bco
    body = "<h1>Ground truth: bandit convex optimisation</h1>"
    if not isinstance(bco, dict):
        body += '<p class="notice">No ground-truth file yet (<code>data/ground_truth/bco.yaml</code>).</p>'
        return page("Ground truth", body, "", "gt")
    sets = {str(s.get("id")): s for s in listify(bco, "settings") if isinstance(s, dict)}
    results = [r for r in listify(bco, "results") if isinstance(r, dict)]
    rules = [t for t in listify(bco, "transfer_rules") if isinstance(t, dict)]
    probs = [o for o in listify(bco, "open_problems") if isinstance(o, dict)]
    nlo = sum(1 for r in results if r.get("side") == "lower")
    body += ('<p class="lede">Hand-curated reference data from Lattimore\'s <em>Bandit Convex Optimisation</em> '
             '(LLM-assisted, not yet human-verified). Bounds are rendered from the canonical expression with the '
             'book\'s horizon <i>n</i> written as <i>T</i>; the book\'s own LaTeX is under each row\'s <i>details</i>.</p>')
    toc = [("source", "Source"), ("settings", f"Settings ({len(sets)})"), ("lower", f"Lower bounds ({nlo})"),
           ("upper", f"Upper bounds ({len(results) - nlo})"), ("transfer-rules", f"Transfer rules ({len(rules)})"),
           ("open-problems", f"Open problems ({len(probs)})")]
    body += '<p class="crumbs">' + " · ".join(f'<a href="#{a}">{e(t)}</a>' for a, t in toc) + "</p>"
    if isinstance(bco.get("source"), dict):
        body += '<h2 id="source">Source</h2>' + gt_source(bco["source"])
    body += ('<h2 id="settings">Settings</h2><p class="hint muted small">Function classes of Definition 1.1 with '
             'their assumption vectors. Notation as in the book: superscript s = stochastic, i = improper.</p>' + gt_settings(list(sets.values())))
    body += ('<h2 id="lower">Lower bounds <span class="muted">(Table 2.1)</span></h2>' + gt_results(results, "lower", sets))
    body += ('<h2 id="upper">Upper bounds <span class="muted">(Table 2.2)</span></h2>'
             '<p class="muted small">Compute is the per-round complexity (∞ = non-constructive).</p>' + gt_results(results, "upper", sets))
    body += ('<h2 id="transfer-rules">Transfer rules</h2><p class="muted small">How bounds move between settings: '
             'from → to, and which side of the bound transfers.</p>' + gt_rules(rules))
    body += '<h2 id="open-problems">Open problems</h2>' + gt_open(probs, sets)
    head = f"<script>window.BB_MACROS = {json.dumps(BCO_MACROS)};</script>"
    return page("Ground truth", body, "", "gt", head=head, wide=True)


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
        iu, il = site.counts(n, "inherited")
        act, env = n["key"].get("action_space", ""), n["key"].get("environment", "")
        nodes.append({"id": n["id"], "url": f'settings/{n["slug"]}.html', "slug": n["slug"], "name": n["name"],
                      "up": up, "lo": lo, "iu": iu, "il": il, "papers": len(n["papers"]),
                      "action_space": value_label("action_space", act) if act else "unspecified",
                      "environment": value_label("environment", env) if env else "unspecified",
                      "sa": act_slots.get(act, 0), "se": env_slots.get(env, 0),
                      "st": site.analysis.setting_status(n["id"])[0] if site.analysis.ok else None,
                      "streg": analysis.regime_label(site.analysis.setting_status(n["id"])[1] or "") if site.analysis.ok else ""})
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

    # Overview: group settings by their main problem axes; one node per group, with
    # specialisation arrows between groups (transitively reduced). The full graph of 1000+
    # near-duplicate settings is unreadable as a first view; objective and feedback are left to
    # the group's members (adding them gives ~180 groups, too many to label).
    group_dims = ["environment", "action_space"]
    gid_of, groups = {}, {}
    for n in site.nodes.values():
        gk = tuple(n["key"].get(d, "") for d in group_dims)
        gid = "G" + hashlib.sha1("|".join(gk).encode()).hexdigest()[:8]
        gid_of[n["id"]] = gid
        g = groups.setdefault(gid, {"id": gid, "name": setting_name(dict(zip(group_dims, gk))), "members": [],
                                    "sa": act_slots.get(gk[1], 0), "se": env_slots.get(gk[0], 0), "results": 0})
        g["members"].append(n["id"])
        g["results"] += sum(site.counts(n))
    for x in nodes:
        x["g"] = gid_of[x["id"]]
    gpairs = {(gid_of[x["source"]], gid_of[x["target"]]) for x in site.hasse()
              if x["kind"] != "neighbour" and gid_of[x["source"]] != gid_of[x["target"]]}
    succ: dict[str, set] = {}
    for a, b in gpairs:
        succ.setdefault(a, set()).add(b)

    def reach(a, b, skip):
        stack, seen = [y for y in succ.get(a, ()) if (a, y) != skip], set()
        while stack:
            y = stack.pop()
            if y == b:
                return True
            if y not in seen:
                seen.add(y)
                stack += succ.get(y, ())
        return False
    gedges = [{"s": a, "t": b} for a, b in sorted(gpairs) if not reach(a, b, (a, b))]
    gnodes = [{**g, "n": len(g["members"])} for g in groups.values()]
    data = json.dumps({"nodes": nodes, "edges": edges, "groups": gnodes, "gedges": gedges},
                      ensure_ascii=False).replace("</", "<\\/")
    from collections import Counter
    stc = Counter(x["st"] for x in nodes)
    st_legend = "".join(f'<li><span class="dot st-{k}"></span>{e(analysis.STATUS[k][0])} <span class="muted">&nbsp;{stc[k]}</span></li>'
                        for k in analysis.STATUS_RANK if stc[k])
    st_legend += ('<li class="muted small">regret · worst-case regime, else the most relevant one</li>' if st_legend else "")
    n_dir = sum(1 for x in edges if x["kind"] != "neighbour")
    body = f"""
<div class="graph-head">
<div>
<h1>Settings graph</h1>
<p class="lede small"><b>Overview</b>: {len(gnodes)} groups of settings (environment × action space); click a
group to see its settings. <b>All settings</b>: {len(nodes)} settings. <b>Arrows</b> run from a special case to its generalisation
({n_dir} after removing transitive ones): upper bounds flow against the arrow, lower bounds along it.
<span class="faint-line"></span> faint lines join settings that differ in one unordered assumption.
Node size ∝ number of results. Click a node to open it.</p>
</div>
</div>
<div class="graph-controls">
<div class="seg" role="group" aria-label="View"><span>View</span>
<button type="button" data-view="overview" aria-pressed="true">Overview</button>
<button type="button" data-view="all" aria-pressed="false">All settings</button></div>
<div class="seg" role="group" aria-label="Colour by"><span>Colour</span>
<button type="button" data-colour="sa" aria-pressed="true">Action space</button>
<button type="button" data-colour="se" aria-pressed="false">Environment</button>
{'<button type="button" data-colour="st" aria-pressed="false">Status</button>' if site.analysis.ok else ""}</div>
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
<ul id="legend-st" hidden>{st_legend}</ul>
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


def bust_caches(out: Path) -> None:
    """Append ?v=<content hash> to every static/*.css|js reference in the generated pages, so
    browsers never combine new HTML with a cached old stylesheet or script (which broke the
    rate plots: unstyled SVG paths fill black)."""
    ref = re.compile(r'((?:\.\./)?static/([\w.-]+\.(?:css|js)))"')
    digest = {f.name: hashlib.sha1(f.read_bytes()).hexdigest()[:10] for f in (out / "static").iterdir() if f.is_file()}
    for page_file in out.rglob("*.html"):
        s = page_file.read_text(encoding="utf-8")
        s2 = ref.sub(lambda m: f'{m.group(1)}?v={digest[m.group(2)]}"' if m.group(2) in digest else m.group(0), s)
        if s2 != s:
            page_file.write_text(s2, encoding="utf-8")


def build(root: Path, out: Path) -> None:
    site = Site(root)
    site.analysis = analysis.Analysis(root, site)
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
    pages = analysis.Pages(site, site.analysis, sys.modules[__name__])
    w("gaps.html", pages.gaps_page())
    w("neighbours.html", pages.neighbours_page())
    w("transfer.html", pages.transfer_page())
    w("redundant.html", pages.redundant_page())
    w("search.html", pages.search_page())
    if site.analysis.ok:
        blob = json.dumps(site.analysis.search_data(), ensure_ascii=False, separators=(",", ":"))
        w("static/search-data.js", f"window.BB_SEARCH = {blob};\n")
    w("papers/index.html", papers_index(site))
    for pid in site.paper_ids():
        w(f"papers/{slugify(pid)}.html", paper_page(site, pid))
    n_res = sum(len(n["results"]) for n in site.nodes.values())
    bust_caches(out)
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
