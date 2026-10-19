#!/usr/bin/env python3
"""Build the static bandit-browser site into _site/.

Usage:
    uv run --with pyyaml python site/build.py              # real data
    uv run --with pyyaml python site/build.py --fixtures   # site/fixtures/ test data
    ... [--out DIR]

Inputs (all optional; missing files/dirs are treated as empty):
    corpus/manifest.yaml
    data/extractions/<paper_id>.json
    data/ground_truth/bco.yaml

Display only: no bound comparison or inference happens here.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
DIMS = ["objective", "feedback", "environment", "action_space", "function_class", "domain",
        "context", "noise"]  # ontology v0.2
KEY_DIMS = DIMS + ["extras"]  # learner_knows deliberately excluded

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


def load_manifest(root: Path) -> list[dict]:
    data = load_yaml(root / "corpus" / "manifest.yaml") or {}
    papers = data.get("papers") if isinstance(data, dict) else None
    return [p for p in (papers or []) if isinstance(p, dict) and p.get("id")]


def load_extractions(root: Path) -> dict[str, dict]:
    out = {}
    d = root / "data" / "extractions"
    if not d.is_dir():
        return out
    for f in sorted(d.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            warn(f"could not parse {f}: {exc}")
            continue
        if isinstance(data, dict):
            out[f.stem] = data
    return out


# ---------------------------------------------------------------- helpers


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", str(s).lower()).strip("-") or "x"


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def text(v) -> str:
    """Plain escaped text for a scalar or list."""
    if v is None or v == "" or v == []:
        return '<span class="muted">–</span>'
    if isinstance(v, list):
        return ", ".join(e(str(x)) for x in v) or '<span class="muted">–</span>'
    if isinstance(v, bool):
        return "yes" if v else "no"
    return e(str(v))


def math(tex, fallback=None) -> str:
    """Span rendered client-side by KaTeX; shows raw text if JS is off."""
    if not tex:
        return text(fallback)
    t = str(tex)
    return f'<span class="math" data-tex="{e(t, quote=True)}">{e(t)}</span>'


def setting_key(s: dict) -> tuple:
    def dimval(v):
        if isinstance(v, list):  # multi-select dimensions, e.g. function_class
            return "+".join(sorted(map(str, v))) or "none"
        return str(v) if v is not None else "null"

    vals = tuple(dimval(s.get(d)) for d in DIMS)
    extras = tuple(sorted(str(x) for x in as_list(s.get("extras"))))
    return vals + (extras,)


def key_slug(k: tuple) -> str:
    parts = list(k[:-1]) + ["-".join(k[-1]) or "no-extras"]
    return slugify("--".join(parts))


def key_dict(k: tuple) -> dict:
    d = dict(zip(DIMS, k[:-1]))
    d["extras"] = list(k[-1])
    return d


def key_label(k: tuple) -> str:
    d = key_dict(k)
    bits = [d["objective"], d["feedback"], d["environment"], d["action_space"]]
    if d["context"] not in ("none", "null"):
        bits.append(d["context"])
    bits.append(d["noise"])
    bits += d["extras"]
    return " · ".join(bits)


def paper_title(pid: str, manifest: dict, extractions: dict) -> str:
    if pid in manifest and manifest[pid].get("title"):
        return manifest[pid]["title"]
    p = (extractions.get(pid) or {}).get("paper") or {}
    return p.get("title") or pid


def arxiv_url(p: dict) -> str | None:
    if p.get("url"):
        return p["url"]
    if p.get("arxiv_id"):
        return f"https://arxiv.org/abs/{p['arxiv_id']}"
    return None


# ---------------------------------------------------------------- page shell


def page(title: str, body: str, root: str, active: str = "") -> str:
    nav = [
        ("index.html", "Home", "home"),
        ("settings/index.html", "Settings", "settings"),
        ("papers/index.html", "Papers", "papers"),
        ("ground-truth.html", "Ground truth (BCO)", "gt"),
        ("pilot-facts.html", "Pilot facts", "facts"),
    ]
    links = " ".join(
        f'<a href="{root}{href}"{" class=active" if key == active else ""}>{label}</a>'
        for href, label, key in nav
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
</head>
<body>
<header><nav><strong><a href="{root}index.html">bandit-browser</a></strong> {links}</nav></header>
<main>
{body}
</main>
<footer>Generated from plain data files by <code>site/build.py</code>. Extracted by LLMs; not human-verified unless stated.</footer>
</body>
</html>
"""


FILTER = '<input class="filter" type="search" placeholder="Filter…" aria-label="Filter rows">'


def table(headers: list[str], rows: list[list[str]], cls: str = "") -> str:
    if not rows:
        return '<p class="muted">None.</p>'
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="scroll"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>\n{trs}\n</tbody></table></div>'


def dl(pairs: list[tuple[str, str]]) -> str:
    return "<dl>" + "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in pairs) + "</dl>"


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
    if "latex" in key.lower() and isinstance(v, str):
        return math(v)
    if isinstance(v, list) and v and any(isinstance(x, (dict, list)) for x in v):
        return generic(v)
    if isinstance(v, str) and len(v) > 200:
        return f"<details><summary>{e(v[:80])}…</summary>{e(v)}</details>"
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
            return FILTER + table(
                [e(c) for c in cols],
                [[cell(c, r.get(c)) for c in cols] for r in rows],
                "filterable",
            )
        if all(not isinstance(x, (dict, list)) for x in v):
            return "<ul>" + "".join(f"<li>{e(str(x))}</li>" for x in v) + "</ul>"
        return "<ul>" + "".join(f"<li>{generic(x)}</li>" for x in v) + "</ul>"
    return text(v)


# ---------------------------------------------------------------- model


class Site:
    def __init__(self, root: Path):
        self.root = root
        self.manifest_list = load_manifest(root)
        self.manifest = {p["id"]: p for p in self.manifest_list}
        self.extractions = load_extractions(root)
        self.bco = load_yaml(root / "data" / "ground_truth" / "bco.yaml")
        self.facts = load_yaml(root / "data" / "ground_truth" / "pilot-facts.yaml")
        # canonical settings
        self.nodes: dict[tuple, dict] = {}
        self.local_to_key: dict[tuple[str, str], tuple] = {}
        for pid, ex in self.extractions.items():
            algs = {a.get("id"): a for a in as_list(ex.get("algorithms")) if isinstance(a, dict)}
            settings = {s.get("id"): s for s in as_list(ex.get("settings")) if isinstance(s, dict)}
            for sid, s in settings.items():
                k = setting_key(s)
                self.local_to_key[(pid, sid)] = k
                node = self.nodes.setdefault(k, {"instances": [], "results": []})
                node["instances"].append((pid, s))
            for r in as_list(ex.get("results")):
                if not isinstance(r, dict):
                    continue
                k = self.local_to_key.get((pid, r.get("setting")))
                if k is None:
                    warn(f"{pid}: result {r.get('id')} references unknown setting {r.get('setting')}")
                    continue
                self.nodes[k]["results"].append(
                    {"paper": pid, "r": r, "alg": algs.get(r.get("algorithm")), "setting": settings.get(r.get("setting"))}
                )

    def paper_ids(self) -> list[str]:
        ids = [p["id"] for p in self.manifest_list]
        return ids + [pid for pid in self.extractions if pid not in self.manifest]

    def neighbours(self, k: tuple) -> list[tuple[tuple, str, str, str]]:
        out = []
        for other in self.nodes:
            diffs = [i for i in range(len(KEY_DIMS)) if other[i] != k[i]]
            if len(diffs) == 1:
                i = diffs[0]
                fmt = (lambda x: ", ".join(x) or "none") if KEY_DIMS[i] == "extras" else str
                out.append((other, KEY_DIMS[i], fmt(k[i]), fmt(other[i])))
        return sorted(out, key=lambda t: (t[1], t[3]))


# ---------------------------------------------------------------- result tables


def results_table(items: list[dict], site: Site, root: str, show_setting: bool = False) -> str:
    headers = ["Bound", "Notation", "Quantity", "Dependence", "Probability", "Horizon", "Algorithm",
               "Learner knows", "Extra assumptions", "Regime", "Paper", "Theorem", "Confidence"]
    if show_setting:
        headers.insert(0, "Setting")
    rows = []
    for it in items:
        r, pid = it["r"], it["paper"]
        b = r.get("bound") or {}
        alg = it.get("alg")
        if alg:
            alg_html = e(alg.get("name") or alg.get("id") or "")
        elif r.get("algorithm_class"):
            alg_html = f'<span class="muted">class: {e(str(r["algorithm_class"]))}</span>'
        else:
            alg_html = text(r.get("algorithm"))
        src = r.get("source") or {}
        thm = text(src.get("number"))
        if src.get("quote"):
            thm = f'<details><summary>{thm}</summary><blockquote>{e(str(src["quote"]))}</blockquote></details>'
        notes = r.get("notes")
        conf = text(r.get("confidence"))
        if notes:
            conf = f'<span class="conf-{e(str(r.get("confidence")))}" title="{e(str(notes), quote=True)}">{conf}</span>'
        s = it.get("setting") or {}
        row = [
            math(b.get("expression_latex"), b.get("expression")),
            text(b.get("notation")),
            text(r.get("quantity")),
            text(r.get("dependence")),
            text(r.get("probability")),
            text(r.get("horizon")),
            alg_html,
            text(s.get("learner_knows")),
            text(r.get("extra_assumptions")),
            text(b.get("regime")),
            f'<a href="{root}papers/{slugify(pid)}.html">{e(pid)}</a>',
            thm,
            conf,
        ]
        if show_setting:
            k = site.local_to_key.get((pid, r.get("setting")))
            row.insert(0, f'<a href="{root}settings/{key_slug(k)}.html">{e(str(r.get("setting")))}</a>' if k else text(r.get("setting")))
        rows.append(row)
    return FILTER + table(headers, rows, "filterable results")


def split_sides(items):
    up = [i for i in items if (i["r"].get("side") or "").lower() == "upper"]
    lo = [i for i in items if (i["r"].get("side") or "").lower() == "lower"]
    other = [i for i in items if i not in up and i not in lo]
    return up, lo, other


# ---------------------------------------------------------------- pages


def home_page(site: Site) -> str:
    n_res = sum(len(n["results"]) for n in site.nodes.values())
    n_ex = sum(1 for pid in site.paper_ids() if pid in site.extractions)
    body = f"""
<h1>bandit-browser</h1>
<p>A machine-readable atlas of theoretical results on bandit problems. Papers are parsed by an LLM into
<em>settings</em> (assumption vectors over a fixed ontology) and <em>results</em> (upper and lower bounds with provenance).
This site is a plain browser over that data; no bounds are compared or inferred yet.</p>
<ul class="stats">
<li><a href="papers/index.html"><b>{len(site.paper_ids())}</b> papers</a> ({n_ex} extracted)</li>
<li><a href="settings/index.html"><b>{len(site.nodes)}</b> canonical settings</a></li>
<li><b>{n_res}</b> extracted results</li>
<li><a href="ground-truth.html">Ground truth: bandit convex optimisation</a>{"" if site.bco else " (not yet available)"}</li>
<li><a href="pilot-facts.html">Pilot acceptance facts</a> (known results the graph should rediscover)</li>
</ul>
<p>Canonical setting = objective | feedback | environment | action space | function class | domain | context | noise | extras.
What the learner knows (e.g. <code>T</code>) is shown per result, not used to group settings.</p>
<p>Source and data: <a href="https://github.com/act65/bandit-browser">github.com/act65/bandit-browser</a>.</p>
"""
    return page("Home", body, "", "home")


def settings_index(site: Site) -> str:
    rows = []
    for k in sorted(site.nodes):
        n = site.nodes[k]
        up, lo, _ = split_sides(n["results"])
        papers = {pid for pid, _ in n["instances"]}
        d = key_dict(k)
        rows.append(
            [f'<a href="{key_slug(k)}.html">{e(d["objective"])}</a>']
            + [e(d[x]) for x in DIMS[1:]]
            + [text(d["extras"]), str(len(up)), str(len(lo)), str(len(papers))]
        )
    headers = [x.replace("_", " ") for x in DIMS] + ["extras", "upper", "lower", "papers"]
    body = f"<h1>Settings</h1><p>{len(site.nodes)} canonical settings from extracted papers.</p>{FILTER}{table(headers, rows, 'filterable')}"
    return page("Settings", body, "../", "settings")


def setting_page(site: Site, k: tuple) -> str:
    n = site.nodes[k]
    d = key_dict(k)
    vec = dl([(x, text(d[x])) for x in KEY_DIMS])
    inst_rows = []
    for pid, s in n["instances"]:
        inst_rows.append([
            f'<a href="../papers/{slugify(pid)}.html">{e(pid)}</a>',
            e(str(s.get("id", ""))),
            text(s.get("name_in_paper")),
            text(s.get("learner_knows")),
            text(s.get("unmapped")),
        ])
    up, lo, other = split_sides(n["results"])
    nb = site.neighbours(k)
    nb_html = (
        "<ul>" + "".join(
            f'<li><a href="{key_slug(o)}.html"><code>{e(dim)}</code>: {e(a)} → <b>{e(b)}</b></a></li>'
            for o, dim, a, b in nb
        ) + "</ul>"
    ) if nb else '<p class="muted">No extracted setting differs in exactly one dimension.</p>'
    body = f"""
<p class="crumbs"><a href="index.html">Settings</a></p>
<h1>{e(key_label(k))}</h1>
<h2>Assumption vector</h2>{vec}
<h2>Upper bounds ({len(up)})</h2>{results_table(up, site, "../")}
<h2>Lower bounds ({len(lo)})</h2>{results_table(lo, site, "../")}
{f"<h2>Other ({len(other)})</h2>" + results_table(other, site, "../") if other else ""}
<h2>Neighbours</h2>{nb_html}
<h2>As stated in papers</h2>{table(["Paper", "Local id", "Name in paper", "Learner knows", "Unmapped"], inst_rows)}
"""
    return page(key_label(k), body, "../", "settings")


def papers_index(site: Site) -> str:
    rows = []
    for pid in site.paper_ids():
        m = site.manifest.get(pid, {})
        ex = site.extractions.get(pid)
        status = f'{len(as_list(ex.get("results")))} results' if ex else '<span class="muted">not yet extracted</span>'
        authors = m.get("authors") or ((ex or {}).get("paper") or {}).get("authors")
        year = m.get("year") or ((ex or {}).get("paper") or {}).get("year")
        rows.append([
            f'<a href="{slugify(pid)}.html">{e(paper_title(pid, site.manifest, site.extractions))}</a>',
            text(authors), text(year), text(m.get("slice")), status,
        ])
    body = f"<h1>Papers</h1><p>{len(rows)} papers.</p>{FILTER}{table(['Title', 'Authors', 'Year', 'Slice', 'Extraction'], rows, 'filterable')}"
    return page("Papers", body, "../", "papers")


def paper_page(site: Site, pid: str) -> str:
    m = site.manifest.get(pid, {})
    ex = site.extractions.get(pid)
    p = (ex or {}).get("paper") or {}
    info = {**{k: v for k, v in p.items() if v is not None}, **{k: v for k, v in m.items() if v is not None}}
    url = arxiv_url(info)
    meta = [(k, text(info.get(k))) for k in ["id", "authors", "year", "venue", "arxiv_id", "slice", "result_types", "why"] if info.get(k) is not None]
    if url:
        meta.append(("link", f'<a href="{e(url, quote=True)}">{e(url)}</a>'))
    body = f'<p class="crumbs"><a href="index.html">Papers</a></p><h1>{e(paper_title(pid, site.manifest, site.extractions))}</h1>{dl(meta)}'
    if not ex:
        body += '<p class="notice">Not yet extracted.</p>'
        return page(pid, body, "../", "papers")

    run = ex.get("_run")
    if isinstance(run, dict):
        body += "<h2>Extraction run</h2>" + dl([(k, text(v)) for k, v in run.items()])
    body += f'<p class="muted">schema {e(str(ex.get("schema_version")))}, ontology {e(str(ex.get("ontology_version")))}</p>'

    srows = []
    for s in as_list(ex.get("settings")):
        if not isinstance(s, dict):
            continue
        k = site.local_to_key.get((pid, s.get("id")))
        link = f'<a href="../settings/{key_slug(k)}.html">{e(str(s.get("id")))}</a>' if k else text(s.get("id"))
        quote = s.get("definition_quote")
        srows.append([link, text(s.get("name_in_paper"))] + [text(s.get(x)) for x in DIMS + ["extras", "learner_knows", "unmapped"]]
                     + [f"<details><summary>quote</summary><blockquote>{e(str(quote))}</blockquote></details>" if quote else text(None)])
    body += "<h2>Settings</h2>" + table(["Id", "Name in paper"] + [x.replace("_", " ") for x in DIMS] + ["extras", "learner knows", "unmapped", "definition"], srows)

    arows = [[text(a.get("id")), text(a.get("name")), text(a.get("is_new")), text(a.get("techniques")), text(a.get("requires_knowledge_of"))]
             for a in as_list(ex.get("algorithms")) if isinstance(a, dict)]
    body += "<h2>Algorithms</h2>" + table(["Id", "Name", "New", "Techniques", "Requires knowledge of"], arows)

    algs = {a.get("id"): a for a in as_list(ex.get("algorithms")) if isinstance(a, dict)}
    settings = {s.get("id"): s for s in as_list(ex.get("settings")) if isinstance(s, dict)}
    items = [{"paper": pid, "r": r, "alg": algs.get(r.get("algorithm")), "setting": settings.get(r.get("setting"))}
             for r in as_list(ex.get("results")) if isinstance(r, dict)]
    up, lo, other = split_sides(items)
    body += f"<h2>Upper bounds ({len(up)})</h2>" + results_table(up, site, "../", show_setting=True)
    body += f"<h2>Lower bounds ({len(lo)})</h2>" + results_table(lo, site, "../", show_setting=True)
    if other:
        body += f"<h2>Other ({len(other)})</h2>" + results_table(other, site, "../", show_setting=True)

    crows = []
    for c in as_list(ex.get("cited_results")):
        if not isinstance(c, dict):
            continue
        b = c.get("bound") or {}
        crows.append([text(c.get("cited_key")), text(c.get("cited_title")), text(c.get("algorithm_name")), text(c.get("side")),
                      text(c.get("setting_description")), math(b.get("expression_latex"), b.get("expression")),
                      text(b.get("notation")), text(b.get("regime")), text(c.get("where"))])
    body += "<h2>Cited results</h2>" + table(["Cited key", "Title", "Algorithm", "Side", "Setting", "Bound", "Notation", "Regime", "Where"], crows)
    return page(pid, body, "../", "papers")


def ground_truth_page(site: Site) -> str:
    bco = site.bco
    body = "<h1>Ground truth: bandit convex optimisation</h1>"
    if not isinstance(bco, dict):
        body += '<p class="notice">No ground-truth file yet (<code>data/ground_truth/bco.yaml</code>).</p>'
        return page("Ground truth (BCO)", body, "", "gt")
    body += "<p>Hand-curated reference data, rendered as-is.</p>"
    order = ["source", "settings", "results", "transfer_rules", "open_problems"]
    keys = [k for k in order if k in bco] + [k for k in bco if k not in order]
    toc = " · ".join(f'<a href="#{slugify(k)}">{e(k.replace("_", " "))}</a>' for k in keys)
    body += f'<p class="crumbs">{toc}</p>'
    for k in keys:
        v = bco[k]
        inner = generic(v) if isinstance(v, (dict, list)) else f"<p>{text(v)}</p>"
        body += f'<h2 id="{slugify(k)}">{e(k.replace("_", " ").capitalize())}</h2>' + inner
    return page("Ground truth (BCO)", body, "", "gt")


def facts_page(site: Site) -> str:
    facts = site.facts
    body = "<h1>Pilot acceptance facts</h1>"
    if not isinstance(facts, dict):
        body += '<p class="notice">No file yet (<code>data/ground_truth/pilot-facts.yaml</code>).</p>'
        return page("Pilot facts", body, "", "facts")
    body += ("<p>Known results in the K-armed and linear pilot slice that the graph should rediscover "
             "(plan.md Phase 3 acceptance tests). Written from domain knowledge; not yet verified line by line.</p>")
    body += generic(facts.get("facts", []))
    return page("Pilot facts", body, "", "facts")


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
    w("ground-truth.html", ground_truth_page(site))
    w("pilot-facts.html", facts_page(site))
    w("settings/index.html", settings_index(site))
    for k in site.nodes:
        w(f"settings/{key_slug(k)}.html", setting_page(site, k))
    w("papers/index.html", papers_index(site))
    for pid in site.paper_ids():
        w(f"papers/{slugify(pid)}.html", paper_page(site, pid))
    print(f"built {out}: {len(site.paper_ids())} papers, {len(site.extractions)} extractions, "
          f"{len(site.nodes)} settings, ground truth {'yes' if site.bco else 'no'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixtures", action="store_true", help="read site/fixtures/ instead of the repo data")
    ap.add_argument("--out", type=Path, default=REPO / "_site")
    args = ap.parse_args()
    build(HERE / "fixtures" if args.fixtures else REPO, args.out)


if __name__ == "__main__":
    main()
