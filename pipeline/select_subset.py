"""Choose a breadth-oriented extraction batch from the screened core papers (plan.md Phase 4).

Each selected paper carries the reasons it was picked:
  cited        highly cited (OpenAlex cited_by_count per year since publication)
  recent       2024 or later
  slice        quota per screening slice; slices the corpus barely covers get more
  cluster      TF-IDF k-means clusters over core abstracts, a few per cluster (breadth
               beyond the slice labels)
  lower_bound  screening reason or title/abstract says it proves lower bounds
  gap          named by gap triage (data/reports/triage.yaml) or cited-but-missing
  foundation   pre-2012 and listed in an expert bibliography
Only core papers with an arXiv id (LaTeX available) that are not already in the corpus.
Quotas are filled in that order of priority; overlaps count once; leftover capacity
goes to the least-represented clusters.

Writes corpus/batch-<name>.yaml (manifest-format entries plus `selected_for`) and prints
the composition by reason, slice, year and cluster.

Usage: uv run python pipeline/select_subset.py [--size 500] [--name 1] [--seed 0]
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import random
import re
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvest import get, norm_arxiv  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "corpus" / "harvest" / "citations.json"
LOW_COVERAGE_BOOST = 2.0  # quota multiplier for slices with few corpus papers
LB_RE = re.compile(r"lower bound|minimax (optimal|rate)|impossib|necessar(y|ily)|cannot be improved|tight", re.I)


def citation_counts(papers: list[dict]) -> dict[str, int]:
    """OpenAlex cited_by_count for papers with an arXiv id (cached)."""
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    todo = [p for p in papers if p["id"] not in cache and p.get("arxiv_id")]
    by_doi = {f"10.48550/arxiv.{p['arxiv_id'].lower()}": p["id"] for p in todo}
    keys = list(by_doi)
    for i in range(0, len(keys), 50):
        url = ("https://api.openalex.org/works?filter=doi:" + "|".join(keys[i:i + 50])
               + "&per-page=200&select=doi,cited_by_count")
        for w in json.loads(get(url))["results"]:
            d = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            if d in by_doi:
                cache[by_doi[d]] = w["cited_by_count"]
        time.sleep(0.2)
    for p in todo:
        cache.setdefault(p["id"], 0)
    CACHE.write_text(json.dumps(cache))
    return cache


def clusters(papers: list[dict], k: int, seed: int) -> dict[str, int]:
    """TF-IDF + k-means on title+abstract (pure numpy-free fallback via sklearn if present)."""
    try:
        from sklearn.cluster import MiniBatchKMeans
        from sklearn.feature_extraction.text import TfidfVectorizer
    except ImportError:
        return {p["id"]: hash(p.get("slice")) % k for p in papers}
    texts = [p["title"] + " " + (p.get("abstract") or "") for p in papers]
    X = TfidfVectorizer(max_features=20000, stop_words="english", ngram_range=(1, 2), min_df=3).fit_transform(texts)
    lab = MiniBatchKMeans(n_clusters=k, random_state=seed, n_init=5).fit_predict(X)
    return {p["id"]: int(c) for p, c in zip(papers, lab)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=500)
    ap.add_argument("--name", default="1")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--clusters", type=int, default=40)
    args = ap.parse_args()
    rnd = random.Random(args.seed)

    pool = {p["id"]: p for p in (json.loads(l) for l in (ROOT / "corpus" / "pool.jsonl").open(encoding="utf-8"))}
    scr = {}
    for line in (ROOT / "corpus" / "screening.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        scr[r["id"]] = r
    manifest = yaml.safe_load((ROOT / "corpus" / "manifest.yaml").read_text())["papers"]
    have = {p.get("arxiv_id") for p in manifest} | {p["id"] for p in manifest}
    core = [{**pool[i], "slice": r["slice"], "reason": r["reason"], "confidence": r["confidence"]}
            for i, r in scr.items() if r["label"] == "core" and i in pool]
    cand = [p for p in core if p.get("arxiv_id") and p["arxiv_id"] not in have and p["id"] not in have
            and p["confidence"] != "low"]
    print(f"{len(core)} core papers; {len(cand)} candidates (arXiv, not in corpus, not low-confidence)")

    cites = citation_counts(cand)
    year_now = dt.date.today().year
    rate = {p["id"]: cites.get(p["id"], 0) / max(1, year_now - (p["year"] or year_now) + 1) for p in cand}
    cl = clusters(cand, args.clusters, args.seed)

    # corpus coverage per slice (from the screening of corpus papers)
    corpus_slices = collections.Counter(scr[p["id"]]["slice"] for p in manifest if p["id"] in scr)
    slices = collections.Counter(p["slice"] for p in cand)
    quota_base = max(8, args.size // (3 * len(slices)))
    slice_quota = {s: int(quota_base * (LOW_COVERAGE_BOOST if corpus_slices[s] <= 2 else 1)) for s in slices}

    triage = yaml.safe_load((ROOT / "data" / "reports" / "triage.yaml").read_text()).get("triage", {})
    gap_arxiv = {norm_arxiv(pp.get("arxiv_id") or "") for v in triage.values() for pp in v.get("papers") or []} - {None}

    chosen: dict[str, set] = collections.defaultdict(set)

    def take(pids, reason, n):
        added = 0
        for pid in pids:
            if added >= n or len(chosen) >= args.size and pid not in chosen:
                break
            if reason not in chosen[pid]:
                if pid not in chosen or len(chosen[pid]) == 0:
                    added += 1
                chosen[pid].add(reason)
        return added

    by_id = {p["id"]: p for p in cand}
    # 1. gap-targeted (few, but direct tests of the system)
    take([p["id"] for p in cand if p["arxiv_id"] in gap_arxiv or "leads" in {s.split(":")[0] for s in p["sources"]}],
         "gap", 40)
    # 2. highly cited (by citations per year)
    take(sorted(rate, key=lambda i: -rate[i]), "cited", int(0.22 * args.size))
    # 3. foundations: pre-2012 and in an expert bibliography
    take(sorted([p["id"] for p in cand if (p["year"] or 3000) < 2012 and p["n_bibs"]], key=lambda i: -rate[i]),
         "foundation", int(0.06 * args.size))
    # 4. lower bounds
    lbs = [p["id"] for p in cand if LB_RE.search(p["reason"] + " " + p["title"])]
    rnd.shuffle(lbs)
    take(sorted(lbs, key=lambda i: -rate[i] * rnd.random()), "lower_bound", int(0.12 * args.size))
    # 5. recent (2024+), spread over slices
    recent = collections.defaultdict(list)
    for p in cand:
        if (p["year"] or 0) >= 2024:
            recent[p["slice"]].append(p["id"])
    for v in recent.values():
        rnd.shuffle(v)
    round_robin = [v[i] for i in range(max(map(len, recent.values()), default=0)) for v in recent.values() if i < len(v)]
    take(round_robin, "recent", int(0.18 * args.size))  # spread over slices, not alphabetical
    # 6. slice quotas (low-coverage slices boosted)
    for s, q in slice_quota.items():
        have_s = sum(1 for i in chosen if by_id[i]["slice"] == s)
        pids = [p["id"] for p in cand if p["slice"] == s and p["id"] not in chosen]
        rnd.shuffle(pids)
        take(sorted(pids, key=lambda i: -rate[i] * rnd.random()), "slice", max(0, q - have_s))
    # 7. clusters: at least 3 per cluster, then fill the least-represented clusters
    per = collections.Counter(cl[i] for i in chosen)
    for c in range(args.clusters):
        pids = [p["id"] for p in cand if cl[p["id"]] == c and p["id"] not in chosen]
        rnd.shuffle(pids)
        take(pids, "cluster", max(0, 3 - per[c]))
    remaining = collections.defaultdict(list)  # cluster -> candidates not yet chosen
    for p in cand:
        if p["id"] not in chosen:
            remaining[cl[p["id"]]].append(p["id"])
    for v in remaining.values():
        rnd.shuffle(v)
    per = collections.Counter(cl[i] for i in chosen)
    while len(chosen) < args.size and any(remaining.values()):
        c = min((c for c in remaining if remaining[c]), key=lambda c: per[c])  # least-represented non-empty cluster
        chosen[remaining[c].pop()].add("cluster")
        per[c] += 1

    sel = [by_id[i] for i in chosen]
    out = []
    for p in sorted(sel, key=lambda p: (p["slice"], -(p["year"] or 0))):
        out.append({"id": p["id"], "arxiv_id": p["arxiv_id"], "doi": p.get("doi"),
                    "url": f"https://arxiv.org/abs/{p['arxiv_id']}", "title": p["title"], "authors": p["authors"][:30],
                    "year": p["year"], "venue": "; ".join(p.get("venues") or []) or None, "slice": p["slice"],
                    "selected_for": sorted(chosen[p["id"]]), "citations": cites.get(p["id"], 0),
                    "cluster": cl[p["id"]], "screening_reason": p["reason"]})
    path = ROOT / "corpus" / f"batch-{args.name}.yaml"
    path.write_text(f"# Extraction batch {args.name}: {len(out)} core papers chosen for breadth by "
                    "pipeline/select_subset.py.\n" + yaml.safe_dump({"papers": out}, sort_keys=False, allow_unicode=True, width=110))
    print(f"selected {len(out)} -> {path}")
    print("by reason:", dict(collections.Counter(r for p in out for r in p["selected_for"]).most_common()))
    print("by slice: ", dict(collections.Counter(p["slice"] for p in out).most_common()))
    yrs = collections.Counter((p["year"] or 0) // 5 * 5 for p in out)
    print("by 5-year period:", dict(sorted(yrs.items())))
    print(f"clusters covered: {len({p['cluster'] for p in out})}/{args.clusters}; "
          f"median citations {sorted(p['citations'] for p in out)[len(out) // 2]}")


if __name__ == "__main__":
    main()
