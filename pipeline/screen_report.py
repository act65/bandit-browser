"""Summarise the screening (corpus/screening.jsonl) of the candidate pool.

Writes corpus/screened.csv: one row per screened paper (id, label, slice, confidence,
year, title, arXiv id, DOI, sources), core papers first. Prints label counts overall,
by source and by slice, the recall on corpus/manifest.yaml papers, and how many core
papers have an arXiv id (i.e. LaTeX source available for extraction).

Usage: uv run python pipeline/screen_report.py
"""

from __future__ import annotations

import collections
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = {"core": 0, "adjacent": 1, "applied": 2, "off_topic": 3}


def main() -> None:
    pool = {p["id"]: p for p in (json.loads(line) for line in (ROOT / "corpus" / "pool.jsonl").open(encoding="utf-8"))}
    key_to_id = {p["key"]: i for i, p in pool.items() if p.get("key")}  # screening records carry stable keys
    scr = {}
    for line in (ROOT / "corpus" / "screening.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        scr[key_to_id.get(r.get("key"), r["id"])] = {**r, "id": key_to_id.get(r.get("key"), r["id"])}  # last verdict wins
    rows = sorted((r for r in scr.values() if r["id"] in pool),
                  key=lambda r: (ORDER[r["label"]], -(pool[r["id"]]["year"] or 0)))
    with open(ROOT / "corpus" / "screened.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "label", "slice", "confidence", "title_only", "year", "title", "arxiv_id", "doi", "sources", "reason"])
        for r in rows:
            p = pool[r["id"]]
            w.writerow([r["id"], r["label"], r["slice"], r["confidence"], int(r.get("title_only", False)), p["year"],
                        p["title"], p["arxiv_id"] or "", p["doi"] or "", "; ".join(p["sources"]), r["reason"]])
    labels = collections.Counter(r["label"] for r in rows)
    print(f"screened {len(rows)} of {len(pool)} pool papers: {dict(labels)}")
    core = [r for r in rows if r["label"] == "core"]
    print(f"core: {len(core)}; with arXiv id (LaTeX available): {sum(1 for r in core if pool[r['id']]['arxiv_id'])}; "
          f"title-only verdicts: {sum(1 for r in core if r.get('title_only'))}; low confidence: "
          f"{sum(1 for r in core if r['confidence'] == 'low')}")
    corpus = [p for p in pool.values() if p["in_corpus"]]
    got = collections.Counter(scr[p["id"]]["label"] if p["id"] in scr else "unscreened" for p in corpus)
    print(f"recall on the current corpus: {dict(got)}")
    print("core by slice:", dict(collections.Counter(r["slice"] for r in core).most_common()))
    by_src = collections.defaultdict(collections.Counter)
    for r in rows:
        for s in {x.split(":")[0] for x in pool[r["id"]]["sources"]}:
            by_src[s][r["label"]] += 1
    print("core rate by source:")
    for s, c in sorted(by_src.items(), key=lambda kv: -kv[1]["core"]):
        n = sum(c.values())
        print(f"  {s:10s} {c['core']:6d} core / {n:6d} screened ({c['core'] / n:.0%})")
    only = collections.Counter()
    for r in core:
        kinds = {x.split(":")[0] for x in pool[r["id"]]["sources"]}
        if len(kinds) == 1:
            only[next(iter(kinds))] += 1
    print("core papers found by only one source type:", dict(only.most_common()))


if __name__ == "__main__":
    main()
