"""Merge harvested records into one deduplicated candidate pool (plan.md Phase 4).

Inputs: corpus/harvest/*.jsonl (pipeline/harvest.py) and corpus/manifest.yaml.
Records are linked when they share an arXiv id (version stripped), a DOI, or a
normalised title (lowercase alphanumerics; leading articles and a trailing
"(extended abstract)" etc. removed). Linked records are merged with union-find.

Each merged paper keeps: every source it was found in, all venues and links, the best
abstract (arXiv > PMLR > NeurIPS > OpenAlex), the earliest year, and signals for
screening and ranking:
  bandit_kw    the keyword filter matches the title or abstract
  n_bibs       number of curated bibliographies (books / surveys) that list it
  in_corpus    already in corpus/manifest.yaml
  sources      e.g. ["arxiv", "pmlr", "bib:1904.07272"]

Outputs:
  corpus/pool.jsonl   full records including abstracts (gitignored: abstracts are large)
  corpus/pool.csv     one row per paper without abstracts (committed)
  prints a summary by source and overlap.

Usage: uv run python pipeline/dedupe.py
"""

from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvest import BANDIT_RE, norm_arxiv  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HARVEST = ROOT / "corpus" / "harvest"
MANIFEST = ROOT / "corpus" / "manifest.yaml"
ABSTRACT_PRIORITY = ["arxiv", "pmlr", "neurips", "openalex"]


def norm_title(t: str | None) -> str:
    t = (t or "").lower()
    t = re.sub(r"\\[a-z]+|[{}$]", " ", t)
    t = re.sub(r"\((extended abstract|full version|preliminary version)\)", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return re.sub(r"^(the|a|an) ", "", t)


def load() -> list[dict]:
    recs = []
    for f in sorted(HARVEST.glob("*.jsonl")):
        recs += [json.loads(line) for line in f.open(encoding="utf-8")]
    for p in yaml.safe_load(MANIFEST.read_text())["papers"]:
        recs.append({"source": "manifest", "source_id": p["id"], "title": p["title"], "authors": p.get("authors", []),
                     "year": p.get("year"), "venue": p.get("venue"), "arxiv_id": p.get("arxiv_id"),
                     "doi": p.get("doi"), "url": p.get("url"), "abstract": None, "manifest_id": p["id"]})
        for alt in p.get("alt_titles") or []:
            recs.append({"source": "manifest", "source_id": p["id"] + "#alt", "title": alt, "authors": [],
                         "year": p.get("year"), "arxiv_id": p.get("arxiv_id"), "doi": p.get("doi"),
                         "manifest_id": p["id"]})
    return recs


def main() -> None:
    recs = load()
    parent = list(range(len(recs)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    keyed: dict[str, int] = {}
    for i, r in enumerate(recs):
        keys = []
        if (a := norm_arxiv(r.get("arxiv_id") or "")):
            keys.append("arxiv:" + a.split("v")[0])
        if r.get("doi"):
            keys.append("doi:" + r["doi"].lower().strip())
        if len(t := norm_title(r.get("title"))) >= 12:  # very short titles are ambiguous
            keys.append("title:" + t)
        for k in keys:
            if k in keyed:
                parent[find(i)] = find(keyed[k])
            else:
                keyed[k] = i

    groups = collections.defaultdict(list)
    for i, r in enumerate(recs):
        groups[find(i)].append(r)

    pool = []
    for members in groups.values():
        srcs = sorted({m["source"] for m in members})
        by_src = {m["source"]: m for m in members}
        best = next((by_src[s] for s in ["manifest", "arxiv", "pmlr", "neurips", "openalex"] if s in by_src), members[0])
        abstract = next((m["abstract"] for s in ABSTRACT_PRIORITY for m in members if m["source"] == s and m.get("abstract")), None)
        title = best["title"]
        years = [m["year"] for m in members if isinstance(m.get("year"), int)]
        arxiv = next((norm_arxiv(m["arxiv_id"]) for m in members if m.get("arxiv_id")), None)
        doi = next((m["doi"] for m in members if m.get("doi")), None)
        authors = next((m["authors"] for m in members if m.get("authors") and m["source"] in ("arxiv", "pmlr", "neurips", "openalex", "manifest")), members[0].get("authors") or [])
        first = (authors[0].split()[-1] if authors and authors[0] else "anon").lower()
        first = re.sub(r"[^a-z]", "", first) or "anon"
        year = min(years) if years else None
        word = next((w for w in norm_title(title).split() if len(w) > 3), "paper")
        pool.append({
            "id": next((m["manifest_id"] for m in members if m.get("manifest_id")), f"{first}{year or ''}{word}"),
            "title": title, "authors": authors, "year": year, "arxiv_id": arxiv, "doi": doi,
            "venues": sorted({m["venue"] for m in members if m.get("venue")}),
            "urls": sorted({m["url"] for m in members if m.get("url")}), "sources": srcs,
            "abstract": abstract,
            "bandit_kw": bool(BANDIT_RE.search(title + " " + (abstract or ""))),
            "n_bibs": len({m["source"] for m in members if m["source"].startswith("bib:")}),
            "in_corpus": "manifest" in srcs,
            "openalex_id": next((m["source_id"] for m in members if m["source"] == "openalex"), None),
        })

    # unique ids
    seen = collections.Counter()
    for p in pool:
        seen[p["id"]] += 1
        if seen[p["id"]] > 1:
            p["id"] += chr(ord("a") + seen[p["id"]] - 2)

    pool.sort(key=lambda p: (-(p["year"] or 0), p["id"]))
    with open(ROOT / "corpus" / "pool.jsonl", "w", encoding="utf-8") as f:
        for p in pool:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with open(ROOT / "corpus" / "pool.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "year", "title", "arxiv_id", "doi", "venues", "sources", "bandit_kw", "n_bibs", "in_corpus"])
        for p in pool:
            w.writerow([p["id"], p["year"], p["title"], p["arxiv_id"] or "", p["doi"] or "", "; ".join(p["venues"]),
                        "; ".join(p["sources"]), int(p["bandit_kw"]), p["n_bibs"], int(p["in_corpus"])])

    n = len(pool)
    by_src = collections.Counter(s for p in pool for s in p["sources"])
    print(f"{len(recs)} harvested records -> {n} distinct papers")
    print("papers per source:", dict(by_src.most_common()))
    print(f"with arXiv id: {sum(1 for p in pool if p['arxiv_id'])}; with abstract: {sum(1 for p in pool if p['abstract'])}; "
          f"keyword match: {sum(p['bandit_kw'] for p in pool)}; in >=1 bibliography: {sum(1 for p in pool if p['n_bibs'])}; "
          f"found by >=2 source types: {sum(1 for p in pool if len({s.split(':')[0] for s in p['sources']}) >= 2)}")
    missing = [p for p in pool if p["in_corpus"] and len(p["sources"]) == 1]
    print(f"corpus papers not found by any harvester (recall check): {len(missing)}: {[p['id'] for p in missing][:10]}")


if __name__ == "__main__":
    main()
