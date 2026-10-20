"""Iterative citation snowballing over the candidate pool (plan.md Phase 4).

A work cited by many pool papers is almost certainly relevant, whatever its title says
(e.g. Lai & Robbins, "Asymptotically efficient adaptive allocation rules"). Each round:
  1. resolve pool papers to OpenAlex works (DOI, arXiv DOI 10.48550/arXiv.<id>, or id);
  2. fetch their referenced_works and count, for every referenced work, how many pool
     papers cite it;
  3. add works cited by >= --min-cites pool papers that are not in the pool yet.
Rounds repeat until no new work crosses the threshold (or --rounds is reached).

Only keyword-matching pool papers (bandit_kw) or ones already in the corpus count as
citers, and works added by the snowball become citers only if they match the bandit
keywords themselves, so general references (textbooks, concentration inequalities)
don't steer it.

Needs OpenAlex (set OPENALEX_API_KEY for a usable daily budget).
Output: corpus/harvest/snowball.jsonl (merged by dedupe.py like any other harvest).

Usage: uv run python pipeline/snowball.py [--min-cites 5] [--rounds 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harvest import BANDIT_RE, OUT, ROOT, get, oa_abstract, oa_record  # noqa: E402

SELECT = "id,doi,title,referenced_works"


def batch_works(filter_key: str, values: list[str], select: str | None = SELECT) -> list[dict]:
    out = []
    for i in range(0, len(values), 50):
        chunk = "|".join(values[i:i + 50])
        url = f"https://api.openalex.org/works?filter={filter_key}:{chunk}&per-page=200" + (f"&select={select}" if select else "")
        out += json.loads(get(url))["results"]
        time.sleep(0.2)
    return out


def resolve(pool: list[dict]) -> dict[str, dict]:
    """pool id -> OpenAlex work (with referenced_works)."""
    by_doi = {p["doi"].lower(): p["id"] for p in pool if p.get("doi")}
    by_doi.update({f"10.48550/arxiv.{p['arxiv_id']}": p["id"] for p in pool if p.get("arxiv_id") and not p.get("doi")})
    found = {}
    for w in batch_works("doi", list(by_doi)):
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        if doi in by_doi:
            found[by_doi[doi]] = w
    rest = {p["openalex_id"]: p["id"] for p in pool if p.get("openalex_id") and p["id"] not in found}
    for w in batch_works("openalex", list(rest)):
        found[rest[w["id"].rsplit("/", 1)[-1]]] = w
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-cites", type=int, default=5)
    ap.add_argument("--rounds", type=int, default=3)
    args = ap.parse_args()
    pool = [json.loads(line) for line in (ROOT / "corpus" / "pool.jsonl").open(encoding="utf-8")]
    citers = [p for p in pool if p["bandit_kw"] or p["in_corpus"]]
    works = resolve(citers)
    print(f"resolved {len(works)}/{len(citers)} citing papers in OpenAlex", flush=True)
    known = {w["id"] for w in works.values()} | {f"https://openalex.org/{p['openalex_id']}" for p in pool if p.get("openalex_id")}
    added: dict[str, dict] = {}
    frontier = list(works.values())
    for rnd in range(1, args.rounds + 1):
        counts = collections.Counter(r for w in frontier for r in set(w.get("referenced_works") or []))
        new = [r for r, n in counts.items() if n >= args.min_cites and r not in known]
        print(f"round {rnd}: {len(counts)} referenced works, {len(new)} new with >= {args.min_cites} pool citations", flush=True)
        if not new:
            break
        full = batch_works("openalex", [r.rsplit("/", 1)[-1] for r in new], select=None)
        for w in full:
            rec = oa_record(w)
            rec.update(source="snowball", pool_citations=counts[w["id"]], round=rnd)
            added[w["id"]] = rec
            known.add(w["id"])
        # newly added works only become citers if they are bandit papers themselves; otherwise
        # general references (textbooks, concentration inequalities) drag in their own references
        frontier = frontier + [w for w in full if BANDIT_RE.search((w.get("title") or "") + " "
                                                                   + (oa_abstract(w.get("abstract_inverted_index")) or ""))]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "snowball.jsonl", "w", encoding="utf-8") as f:
        for r in sorted(added.values(), key=lambda r: -r["pool_citations"]):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"snowball: {len(added)} works -> {OUT / 'snowball.jsonl'}")
    for r in sorted(added.values(), key=lambda r: -r["pool_citations"])[:15]:
        print(f"  {r['pool_citations']:4d}  {r['year']}  {r['title'][:90]}")


if __name__ == "__main__":
    main()
