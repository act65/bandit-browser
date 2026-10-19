"""Canonicalisation layer (desiderata D13): raw extractions -> stable-id records.

Reads data/extractions/*.json (left untouched) and writes data/canonical/:
  settings.json     canonical settings: id "S-<hash>", key, label, member settings per paper
  results.json      results with setting_id, algorithm_id, normalised expression
  algorithms.json   registry entries plus provisional ids for unregistered algorithms
  citations.json    per paper: cited_key -> manifest id / arXiv id / unresolved
  candidates.yaml   cited papers not in the corpus, ranked by citation count
  report.md         declared-symbol clusters (variable-registry proposals), unregistered
                    algorithms, unresolved citations

Usage: uv run python pipeline/resolve.py
"""

from __future__ import annotations

import collections
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

import sympy
import yaml
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema  # noqa: E402

ROOT = schema.ROOT
EXT = ROOT / "data" / "extractions"
OUT = ROOT / "data" / "canonical"
MANIFEST = ROOT / "corpus" / "manifest.yaml"

# Dimensions that define a node. learner_knows minus trivially known quantities is
# included because knowledge changes rates (e.g. bounded regret when mu_star is known).
TRIVIAL_KNOWLEDGE = {"T", "K", "d"}
DEFAULT_ACTION_SET = {"shape": "not_applicable", "time_varying": "not_applicable", "access": "not_applicable"}
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
FUNC_NAMES = {"log", "sqrt", "exp", "Min", "Max", "min", "max", "LambertW", "sum_subopt", "sum_arms", "kl"}


# ---------------------------------------------------------------- settings

def setting_key(s: dict, ont: dict) -> dict:
    """Canonical key: every dimension (lists sorted), node parameters and parameters."""
    key = {}
    for dim, spec in ont["dimensions"].items():
        v = s.get(dim)
        if spec.get("multi"):
            v = sorted(set(v or []))
            if dim == "learner_knows":
                v = [x for x in v if x not in TRIVIAL_KNOWLEDGE]
        key[dim] = v if v is not None else ("not_applicable" if dim == "domain" else None)
    key["action_set"] = {**DEFAULT_ACTION_SET, **(s.get("action_set") or {})}
    # access is computational only: it does not separate statistical settings
    key["action_set"] = {k: v for k, v in key["action_set"].items() if k != "access"}
    key["parameters"] = dict(sorted((s.get("parameters") or {}).items()))
    return key


def setting_id(key: dict) -> str:
    blob = json.dumps(key, sort_keys=True)
    return "S-" + hashlib.sha1(blob.encode()).hexdigest()[:8]


LABELS = {
    "stochastic_iid": "stochastic", "adversarial_oblivious": "adversarial (oblivious)",
    "adversarial_adaptive": "adversarial (adaptive)", "adversarial_unspecified": "adversarial",
    "stochastic_corrupted": "corrupted stochastic", "finite_K": "K-armed",
    "linear_finite": "linear (finite actions)", "linear_infinite": "linear",
    "bounded_01": "rewards in [0,1]", "gaussian_known_variance": "Gaussian",
}


def setting_label(key: dict) -> str:
    """Short human-readable name listing the informative dimension values."""
    parts = [LABELS.get(key["environment"], key["environment"]),
             LABELS.get(key["action_space"], key["action_space"])]
    if key["objective"] != "cumulative_regret":
        parts.insert(0, key["objective"])
    if key["feedback"] != "bandit":
        parts.append(key["feedback"] + " feedback")
    if key["context"] not in ("none", None):
        parts.append(key["context"].replace("_", " "))
    if key["function_class"]:
        parts.append("{" + ",".join(key["function_class"]) + "}")
    if key["noise"] not in ("not_applicable", None):
        parts.append(LABELS.get(key["noise"], key["noise"]))
    for dim in ("extras", "instance_assumptions", "learner_knows"):
        if key.get(dim):
            parts.append(("knows " if dim == "learner_knows" else "") + ", ".join(key[dim]))
    if key["action_set"].get("shape") not in ("not_applicable", "unspecified", None):
        parts.append(key["action_set"]["shape"].replace("_", " "))
    if key["parameters"]:
        parts.append(", ".join(f"{k}={v}" for k, v in key["parameters"].items()))
    return " · ".join(str(p) for p in parts)


# ---------------------------------------------------------------- expressions

def parse(expr: str):
    local = {}
    for m in IDENT_RE.finditer(expr):
        name = m.group(0)
        if name in local or name in FUNC_NAMES or name == "pi":
            continue
        local[name] = sympy.Function(name) if expr[m.end():m.end() + 1] == "(" else sympy.Symbol(name)
    funcs = {"log": sympy.log, "sqrt": sympy.sqrt, "exp": sympy.exp, "Min": sympy.Min, "Max": sympy.Max,
             "min": sympy.Min, "max": sympy.Max, "LambertW": sympy.LambertW, "pi": sympy.pi,
             "sum_subopt": sympy.Function("sum_subopt"), "sum_arms": sympy.Function("sum_arms"),
             "kl": sympy.Function("kl")}
    return parse_expr(expr, local_dict={**funcs, **local}, transformations=standard_transformations)


def conversion_applies(conv: dict, s: dict) -> bool:
    if conv.get("manual"):
        return False
    for field, want in (conv.get("when") or {}).items():
        have = s.get(field)
        if isinstance(want, dict):  # e.g. parameters: {K: "2"}
            if not all(str((have or {}).get(k)) == str(v) for k, v in want.items()):
                return False
        elif isinstance(want, list):
            if have not in want:
                return False
        elif have != want:
            return False
    return True


def normalise(expr: str, s: dict, conversions: list[dict]) -> tuple[str | None, list[str]]:
    """Apply registry conversions valid in setting s; return (expression, rules applied)."""
    try:
        e = parse(expr)
    except Exception:  # unparseable expressions are reported by validate.py
        return None, []
    applied = []
    for conv in conversions:
        if not conversion_applies(conv, s):
            continue
        lhs, rhs = (x.strip() for x in conv["rule"].split("="))
        sym = sympy.Symbol(lhs)
        if sym in e.free_symbols:
            e = e.subs(sym, parse(rhs))
            applied.append(conv["id"])
    return str(e), applied


# ---------------------------------------------------------------- citations

def norm_title(t: str | None) -> str:
    t = re.sub(r"\\[a-zA-Z]+|[{}$]", " ", t or "")
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def resolve_citation(c: dict, by_title: dict, by_arxiv: dict) -> str | None:
    if c.get("cited_arxiv_id") and c["cited_arxiv_id"] in by_arxiv:
        return by_arxiv[c["cited_arxiv_id"]]
    t = norm_title(c.get("cited_title"))
    if not t:
        return None
    if t in by_title:
        return by_title[t]
    best = difflib.get_close_matches(t, list(by_title), n=1, cutoff=0.9)
    return by_title[best[0]] if best else None


# ---------------------------------------------------------------- main

def main() -> None:
    ont = schema.load_ontology()
    var = schema.load_variables()
    registry = {a["id"]: a for a in schema.load_algorithms()}
    alias_to_id = {}
    for a in registry.values():
        for m in a.get("mentions", []):
            alias_to_id[(m["paper"], m["name"])] = a["id"]
    manifest = yaml.safe_load(MANIFEST.read_text())["papers"]
    by_title = {norm_title(t): p["id"] for p in manifest for t in [p["title"], *p.get("alt_titles", [])]}
    by_arxiv = {p["arxiv_id"]: p["id"] for p in manifest if p.get("arxiv_id")}
    canonical_vars = set(var["variables"])

    settings: dict[str, dict] = {}
    results, citations, candidates = [], {}, collections.Counter()
    candidate_info = {}
    algorithms = {k: {**v, "provisional": False} for k, v in registry.items()}
    declared = collections.defaultdict(list)
    unregistered = []

    for f in sorted(EXT.glob("*.json")):
        paper = f.stem
        o = json.loads(f.read_text())
        local_setting = {}
        for s in o["settings"]:
            if s.get("in_scope") is False:
                continue
            key = setting_key(s, ont)
            sid = setting_id(key)
            node = settings.setdefault(sid, {"id": sid, "label": setting_label(key), "key": key, "members": []})
            node["members"].append({"paper": paper, "local_id": s["id"], "name_in_paper": s.get("name_in_paper")})
            local_setting[s["id"]] = (sid, s)

        local_algo = {}
        for a in o["algorithms"]:
            aid = a.get("registry_id") or alias_to_id.get((paper, a["name"]))
            if not aid:
                aid = f"new:{paper}:{re.sub(r'[^a-z0-9]+', '_', a['name'].lower()).strip('_')[:40]}"
                algorithms.setdefault(aid, {"id": aid, "name": a["name"], "introduced_in": paper if a.get("is_new") else None,
                                            "techniques": a.get("techniques", []), "provisional": True})
                unregistered.append((paper, a["name"]))
            local_algo[a["id"]] = aid

        for r in o["results"]:
            if r["setting"] not in local_setting:
                continue
            sid, s = local_setting[r["setting"]]
            expr = r["bound"]["expression"]
            norm_expr, applied = normalise(expr, s, var.get("conversions", []))
            for name, meaning in (r.get("symbols") or {}).items():
                if name not in canonical_vars:
                    declared[name].append((paper, meaning))
            results.append({
                "id": f"{paper}:{r['id']}", "paper": paper, "setting_id": sid,
                "algorithm_id": local_algo.get(r.get("algorithm")),
                **{k: r.get(k) for k in ("side", "algorithm_class", "quantity", "dependence", "probability",
                                          "horizon", "comparator", "compute", "confidence", "notes",
                                          "extra_assumptions", "symbols", "is_new")},
                "bound": {**r["bound"], "expression_normalised": norm_expr, "conversions": applied},
                "source": r["source"],
            })

        cmap = {}
        for c in o.get("cited_results", []):
            target = resolve_citation(c, by_title, by_arxiv)
            entry = cmap.setdefault(c["cited_key"], {"paper_id": target, "title": c.get("cited_title"),
                                                     "arxiv_id": c.get("cited_arxiv_id"), "bounds": []})
            entry["bounds"].append({"side": c["side"], "algorithm_id": c.get("algorithm_registry_id"),
                                    "algorithm_name": c.get("algorithm_name"), "bound": c["bound"],
                                    "setting_description": c["setting_description"], "where": c["where"]})
            if not target and c.get("cited_title"):
                t = norm_title(c["cited_title"])
                candidates[t] += 1
                candidate_info.setdefault(t, {"title": c["cited_title"], "arxiv_id": c.get("cited_arxiv_id"),
                                              "cited_by": set()})["cited_by"].add(paper)
        citations[paper] = cmap

    OUT.mkdir(parents=True, exist_ok=True)
    dump = lambda name, obj: (OUT / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=sorted))
    dump("settings.json", sorted(settings.values(), key=lambda n: (-len(n["members"]), n["label"])))
    dump("results.json", results)
    dump("algorithms.json", sorted(algorithms.values(), key=lambda a: a["id"]))
    dump("citations.json", citations)
    cands = [{"title": candidate_info[t]["title"], "arxiv_id": candidate_info[t]["arxiv_id"], "times_cited": n,
              "cited_by": sorted(candidate_info[t]["cited_by"])} for t, n in candidates.most_common()]
    (OUT / "candidates.yaml").write_text(
        "# Cited papers not in corpus/manifest.yaml, ranked by how often corpus papers cite a bound from them.\n"
        + yaml.safe_dump({"candidates": cands}, sort_keys=False, allow_unicode=True, width=110))

    n_cites = sum(len(v) for v in citations.values())
    n_resolved = sum(1 for v in citations.values() for c in v.values() if c["paper_id"])
    recurring = sorted(((k, v) for k, v in declared.items() if len({p for p, _ in v}) >= 2),
                       key=lambda kv: -len({p for p, _ in kv[1]}))
    lines = ["# Canonicalisation report", "", "Generated by `pipeline/resolve.py`.", "",
             f"- canonical settings: {len(settings)} (from {sum(len(n['members']) for n in settings.values())} in-scope extracted settings)",
             f"- results: {len(results)}; with a registry algorithm: {sum(1 for r in results if r['algorithm_id'] and not r['algorithm_id'].startswith('new:'))}",
             f"- algorithms: {len(registry)} registered, {len(unregistered)} unregistered mentions (provisional ids)",
             f"- citations resolved to corpus papers: {n_resolved}/{n_cites}; {len(cands)} distinct candidate papers outside the corpus",
             f"- expressions changed by conversion rules: {sum(1 for r in results if r['bound']['conversions'])}",
             "", "## Declared symbols used by 2+ papers (variable-registry proposals)", ""]
    for name, uses in recurring:
        meanings = collections.Counter(m[:80] for _, m in uses).most_common(2)
        lines.append(f"- `{name}` ({len({p for p, _ in uses})} papers): " + " / ".join(m for m, _ in meanings))
    lines += ["", "## Unregistered algorithms", ""] + [f"- {p}: {n}" for p, n in unregistered]
    lines += ["", "## Top candidate papers outside the corpus", ""] + \
             [f"- ({c['times_cited']}×) {c['title']}" for c in cands[:25]]
    (OUT / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[4:10]))


if __name__ == "__main__":
    main()
