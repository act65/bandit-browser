"""Harvest candidate bandit papers from several sources (plan.md Phase 4).

Sources (subcommands):
  arxiv     arXiv API keyword search (abstract or title), all categories
  pmlr      PMLR proceedings: COLT, ALT, ICML, AISTATS volumes (title filter, then the
            paper page for the abstract)
  neurips   NeurIPS proceedings (papers.nips.cc), title filter, then the abstract page
  openalex  citation snowball from the current corpus: references of and works citing
            each manifest paper, keyword-filtered by OpenAlex's title/abstract search
  all       everything above

Output: corpus/harvest/<source>.jsonl, one record per line:
  {source, source_id, title, authors, year, venue, arxiv_id, doi, url, abstract}
Raw harvests are cached (gitignored); pipeline/dedupe.py merges them.

Requests carry a project user-agent and no personal contact details; arXiv is
queried at most once every 3 s, other sites about once per second.

Usage: uv run python pipeline/harvest.py {arxiv,pmlr,neurips,openalex,all} [--since YEAR]
"""

from __future__ import annotations

import argparse
import collections
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "harvest"
MANIFEST = ROOT / "corpus" / "manifest.yaml"
UA = "bandit-browser/0.1 (research corpus; https://github.com/act65/bandit-browser)"

# What counts as a bandit paper for harvesting (deliberately broad; screening comes later).
BANDIT_RE = re.compile(
    r"\bbandits?\b|best[- ]arm|\barms?\b.*\bregret\b|thompson sampling|partial monitoring|"
    r"pure exploration|\bUCB\b|upper confidence bound|\bExp3\b|dueling|combinatorial semi-bandit|"
    r"top-?k identification", re.I)
ARXIV_QUERIES = ['abs:bandit', 'ti:bandit', 'abs:"best arm identification"', 'abs:"partial monitoring"',
                 'abs:"thompson sampling"', 'abs:"pure exploration"', 'abs:"dueling bandit"']


OPENALEX_KEY = __import__("os").environ.get("OPENALEX_API_KEY", "")


def get(url: str, timeout: int = 60, retries: int = 6, accept: str | None = None) -> bytes:
    """GET with polite retries: rate limits (429/503) wait for Retry-After or minutes, not seconds."""
    if OPENALEX_KEY and "api.openalex.org" in url:
        url += ("&" if "?" in url else "?") + "api_key=" + OPENALEX_KEY
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **({"Accept": accept} if accept else {})})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (400, 401, 403, 404):
                raise  # bad request, out of budget, blocked or missing: retrying won't help
            if attempt == retries - 1:
                raise
            wait = int(e.headers.get("Retry-After") or 0) or (30 * 2 ** attempt if e.code in (429, 503) else 5 * 2 ** attempt)
            print(f"    HTTP {e.code}; waiting {wait}s", flush=True)
            time.sleep(min(wait, 600))
        except Exception:  # network errors
            if attempt == retries - 1:
                raise
            time.sleep(5 * 2 ** attempt)
    raise RuntimeError("unreachable")


def norm_arxiv(s: str | None) -> str | None:
    if not s:
        return None
    m = re.search(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})", s)
    return m.group(1) if m else None


def write(source: str, records: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{source}.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{source}: {len(records)} records -> {OUT / (source + '.jsonl')}")


# ---------------------------------------------------------------- arXiv

def harvest_arxiv(since: int) -> list[dict]:
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    seen: dict[str, dict] = {}
    for q in ARXIV_QUERIES:
        start, total = 0, None
        while total is None or start < total:
            url = ("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
                {"search_query": q, "start": start, "max_results": 200, "sortBy": "submittedDate",
                 "sortOrder": "ascending"}))
            cache = OUT / "cache" / f"arxiv_{re.sub(r'[^a-z]+', '_', q.lower())}_{start}.xml"
            if cache.exists():
                raw = cache.read_bytes()
            else:
                raw = get(url, timeout=120)
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_bytes(raw)
                time.sleep(3)
            root = ET.fromstring(raw)
            total = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
            entries = root.findall("a:entry", ns)
            for e in entries:
                aid = norm_arxiv(e.find("a:id", ns).text)
                year = int(e.find("a:published", ns).text[:4])
                if not aid or year < since:
                    continue
                doi = e.find("arxiv:doi", ns)
                jref = e.find("arxiv:journal_ref", ns)
                seen.setdefault(aid, {
                    "source": "arxiv", "source_id": aid, "arxiv_id": aid,
                    "title": " ".join(e.find("a:title", ns).text.split()),
                    "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
                    "year": year, "venue": jref.text if jref is not None else None,
                    "doi": doi.text if doi is not None else None,
                    "url": f"https://arxiv.org/abs/{aid}",
                    "abstract": " ".join(e.find("a:summary", ns).text.split()),
                    "categories": [c.get("term") for c in e.findall("a:category", ns)],
                })
            print(f"  arxiv {q}: {start + len(entries)}/{total}", flush=True)
            if not entries:
                break
            start += len(entries)
    return list(seen.values())


# ---------------------------------------------------------------- PMLR

PMLR_VENUES = {"COLT": "COLT", "ALT": "ALT", "ICML": "ICML", "AISTATS": "AISTATS"}


def pmlr_abstract(url: str) -> str | None:
    try:
        s = get(url).decode("utf-8", "replace")
    except Exception:  # missing page: keep the record without an abstract
        return None
    m = re.search(r'<div id="abstract" class="abstract">(.*?)</div>', s, re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()) if m else None


def harvest_pmlr(since: int) -> list[dict]:
    index = get("https://proceedings.mlr.press/").decode("utf-8", "replace")
    vols = re.findall(r'<a href="(v\d+)"><b>Volume \d+</b></a>\s*Proceedings of ([A-Za-z]+) (\d{4})', index)
    vols = [(v, conf, int(y)) for v, conf, y in vols if conf in PMLR_VENUES and int(y) >= since]
    print(f"  pmlr: {len(vols)} volumes ({', '.join(sorted({c for _, c, _ in vols}))})", flush=True)
    out = []
    for v, conf, year in vols:
        page = get(f"https://proceedings.mlr.press/{v}/").decode("utf-8", "replace")
        papers = []
        for chunk in page.split('<div class="paper">')[1:]:  # bounded per-paper chunks: no page-wide backtracking
            mt = re.search(r'<p class="title">([^<]*)</p>', chunk)
            ma = re.search(r'<span class="authors">([^<]*)</span>', chunk)
            mu = re.search(r'<a href="(https://proceedings\.mlr\.press/[^"]+\.html)">abs</a>', chunk)
            if mt and mu:
                papers.append((mt.group(1), ma.group(1) if ma else "", mu.group(1)))
        hits = 0
        for title, authors, url in papers:
            title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", title)).split())
            if not BANDIT_RE.search(title):
                continue
            hits += 1
            out.append({"source": "pmlr", "source_id": url.rsplit("/", 1)[-1][:-5], "title": title,
                        "authors": [a.strip() for a in html.unescape(authors).replace("\xa0", " ").split(",") if a.strip()],
                        "year": year, "venue": f"{PMLR_VENUES[conf]} {year}", "arxiv_id": None, "doi": None,
                        "url": url, "abstract": pmlr_abstract(url)})
            time.sleep(0.5)
        print(f"  pmlr {v} {conf} {year}: {hits}/{len(papers)} bandit titles", flush=True)
        time.sleep(1)
    return out


# ---------------------------------------------------------------- NeurIPS

def harvest_neurips(since: int) -> list[dict]:
    out = []
    for year in range(max(since, 1987), 2026):
        try:
            page = get(f"https://papers.nips.cc/paper_files/paper/{year}").decode("utf-8", "replace")
        except Exception as e:  # year not published yet
            print(f"  neurips {year}: {e}")
            continue
        items = []
        for m in re.finditer(r'<a title="paper title" href="(/paper_files/paper/\d{4}/hash/[^"]+)">([^<]*)</a>', page):
            ma = re.search(r'(?:<span class="paper-authors">|<i>)([^<]*)</(?:span|i)>',
                           page[m.end():m.end() + 600])  # authors follow within the item (layout varies by year)
            items.append((m.group(1), m.group(2), ma.group(1) if ma else ""))
        hits = 0
        for href, title, authors in items:
            title = " ".join(html.unescape(title).split())
            if not BANDIT_RE.search(title):
                continue
            hits += 1
            url = "https://papers.nips.cc" + href
            abstract = None
            try:
                ps = get(url).decode("utf-8", "replace")
                m = re.search(r"<h4>Abstract</h4>\s*(.*?)</div>", ps, re.S) or \
                    re.search(r'<p class="paper-abstract">(.*?)</p>', ps, re.S)
                if m:
                    abstract = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
            except Exception:  # keep the record without an abstract
                pass
            out.append({"source": "neurips", "source_id": href.rsplit("/", 1)[-1].split("-")[0], "title": title,
                        "authors": [a.strip() for a in html.unescape(authors).split(",") if a.strip()],
                        "year": year, "venue": f"NeurIPS {year}", "arxiv_id": None, "doi": None,
                        "url": url, "abstract": abstract})
            time.sleep(0.5)
        print(f"  neurips {year}: {hits}/{len(items)} bandit titles", flush=True)
        time.sleep(1)
    return out


# ---------------------------------------------------------------- OpenAlex

def oa_abstract(inv: dict | None) -> str | None:
    if not inv:
        return None
    pos = {i: w for w, idx in inv.items() for i in idx}
    return " ".join(pos[i] for i in sorted(pos))


def oa_record(w: dict) -> dict:
    ids = w.get("ids") or {}
    arxiv = None
    for loc in w.get("locations") or []:
        u = (loc.get("landing_page_url") or "") + " " + (loc.get("pdf_url") or "")
        if "arxiv.org" in u:
            arxiv = norm_arxiv(u)
            break
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
    return {"source": "openalex", "source_id": w["id"].rsplit("/", 1)[-1], "title": w.get("title") or "",
            "authors": [a["author"]["display_name"] for a in w.get("authorships") or []],
            "year": w.get("publication_year"), "venue": venue, "arxiv_id": arxiv,
            "doi": (ids.get("doi") or "").replace("https://doi.org/", "") or None,
            "url": w.get("doi") or w["id"], "abstract": oa_abstract(w.get("abstract_inverted_index"))}


def oa_works(filt: str, search: str | None = None, cap: int = 2000) -> list[dict]:
    out, cursor = [], "*"
    while cursor and len(out) < cap:
        params = {"filter": filt, "per-page": 200, "cursor": cursor}
        if search:
            params["search"] = search
        d = json.loads(get("https://api.openalex.org/works?" + urllib.parse.urlencode(params)))
        out += d["results"]
        cursor = d["meta"].get("next_cursor")
        time.sleep(0.3)
    return out


def harvest_openalex(since: int) -> list[dict]:
    papers = yaml.safe_load(MANIFEST.read_text())["papers"]
    seeds = []
    for p in papers:
        key = f"doi:{p['doi']}" if p.get("doi") else (f"arxiv:{p['arxiv_id']}" if p.get("arxiv_id") else None)
        try:
            if p.get("doi"):
                w = json.loads(get(f"https://api.openalex.org/works/doi:{p['doi']}"))
            else:
                q = urllib.parse.quote(p["title"][:200])
                d = json.loads(get(f"https://api.openalex.org/works?search={q}&per-page=1"))
                w = d["results"][0] if d["results"] else None
            if w:
                seeds.append(w)
        except Exception as e:  # unresolvable seed: skip it
            print(f"  openalex seed {key or p['id']}: {e}")
        time.sleep(0.2)
    print(f"  openalex: resolved {len(seeds)}/{len(papers)} seeds", flush=True)
    found: dict[str, dict] = {}
    for w in seeds:
        refs = [r.rsplit("/", 1)[-1] for r in w.get("referenced_works") or []]
        for i in range(0, len(refs), 50):  # references of the seed
            for r in oa_works("openalex:" + "|".join(refs[i:i + 50])):
                found[r["id"]] = r
        # works citing the seed that are about bandits
        for r in oa_works(f"cites:{w['id'].rsplit('/', 1)[-1]},from_publication_date:{since}-01-01", search="bandit"):
            found[r["id"]] = r
        print(f"  openalex: {w.get('title', '')[:60]} -> {len(found)} total", flush=True)
    out = []
    for r in found.values():
        rec = oa_record(r)
        if (rec["year"] or 0) >= since and BANDIT_RE.search(rec["title"] + " " + (rec["abstract"] or "")):
            out.append(rec)
    return out


# ---------------------------------------------------------------- OpenAlex topic and authors

BANDIT_TOPIC = "T12101"  # OpenAlex topic "Advanced Bandit Algorithms Research" (model-assigned, not keywords)


def harvest_topic(since: int) -> list[dict]:
    # primary topic only: works merely touching bandits (63k) would swamp the pool
    works = oa_works(f"primary_topic.id:{BANDIT_TOPIC},from_publication_date:{since}-01-01", cap=40000)
    print(f"  topic {BANDIT_TOPIC}: {len(works)} works", flush=True)
    return [{**oa_record(w), "source": "topic"} for w in works]


def harvest_authors(since: int, min_papers: int = 20) -> list[dict]:
    """Works of prolific bandit authors (>= min_papers keyword-matching papers in the current
    pool): their papers whose titles don't say 'bandit'. Restricted to computer science,
    mathematics and decision sciences (OpenAlex primary field). A threshold of 3 would mean
    ~3,000 authors; 20 gives ~150, the core community."""
    pool = [json.loads(line) for line in (ROOT / "corpus" / "pool.jsonl").open(encoding="utf-8")]
    counts = collections.Counter(a for p in pool if p["bandit_kw"] for a in p["authors"][:20] if a)
    names = [a for a, n in counts.most_common() if n >= min_papers]
    print(f"  authors: {len(names)} with >= {min_papers} bandit papers", flush=True)
    out = {}
    for name in names:
        d = json.loads(get("https://api.openalex.org/authors?" + urllib.parse.urlencode({"search": name, "per-page": 1})))
        if not d["results"]:
            continue
        aid = d["results"][0]["id"].rsplit("/", 1)[-1]
        for w in oa_works(f"authorships.author.id:{aid},from_publication_date:{since}-01-01,"
                          f"primary_topic.field.id:17|26|18", cap=600):
            out[w["id"]] = {**oa_record(w), "source": "authors", "via_author": name}
        time.sleep(0.2)
    return list(out.values())


# ---------------------------------------------------------------- curated bibliographies

# Expert-made reference lists: surveys and books. arXiv ones are parsed from their
# LaTeX .bib/.bbl; the Lattimore-Szepesvari book (not on arXiv) from its PDF.
BIB_ARXIV = {"1904.07272": "Slivkins, Introduction to Multi-Armed Bandits",
             "2402.06535": "Lattimore, Bandit Convex Optimisation",
             "1204.5721": "Bubeck & Cesa-Bianchi, Regret Analysis of Stochastic and Nonstochastic MAB",
             "2312.16730": "Foster & Rakhlin, Foundations of RL and Interactive Decision Making"}
BOOK_PDF = ("https://tor-lattimore.com/downloads/book/book.pdf", "Lattimore & Szepesvari, Bandit Algorithms")
TWO_LETTER_INITIAL = re.compile(r"\b(Cs|Th|Ch|Sz|Gy|Ph|Kh|Yu)\. ")


def bib_entries_bib(text: str) -> list[dict]:
    out = []
    for m in re.finditer(r"@\w+\s*\{[^,]*,(.*?)\n\s*\}", text, re.S):
        body = m.group(1)
        f = lambda k: (re.search(k + r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", body, re.S | re.I) or [None, None])[1]
        title = f("title")
        if title:
            out.append({"title": " ".join(re.sub(r"[{}\\]", "", title).split()), "authors": [f("author") or ""],
                        "year": int(y) if (y := f("year")) and y[:4].isdigit() else None,
                        "doi": f("doi"), "arxiv_id": norm_arxiv(f("eprint") or f("arxiv") or f("url") or "")})
    return out


def bib_entries_bbl(text: str) -> list[dict]:
    out = []
    for item in re.split(r"\\bibitem", text)[1:]:
        blocks = [" ".join(re.sub(r"\\[a-zA-Z]+|[{}~]", " ", b).split()) for b in item.split("\\newblock")]
        if len(blocks) >= 2:
            y = re.findall(r"\b(19\d\d|20\d\d)\b", item)
            out.append({"title": blocks[1].rstrip(" ."), "authors": [blocks[0][:200]], "year": int(y[-1]) if y else None,
                        "doi": None, "arxiv_id": norm_arxiv(item if "arxiv" in item.lower() else "")})
    return out


def book_bibliography(pdf_text: str) -> list[dict]:
    start = pdf_text.rfind("\nBibliography")
    body = pdf_text[start:]
    entries = re.split(r"\[\d[\d, ]*\]\s*\n", body)
    out = []
    for e in entries:
        e = " ".join(e.split())
        parts = re.split(r"(?<=[a-zéáóúíöüäñ'’}])\. ", TWO_LETTER_INITIAL.sub(r"\1_ ", e))
        if len(parts) < 2:
            continue
        y = re.findall(r"\b(19\d\d|20\d\d)[ab]?\b", e)
        out.append({"title": parts[1].replace("_ ", ". ").strip(), "authors": [parts[0].replace("_ ", ". ")[:200]],
                    "year": int(y[-1]) if y else None, "doi": None, "arxiv_id": norm_arxiv(e if "arXiv" in e else "")})
    return out


def harvest_bib(since: int) -> list[dict]:
    import subprocess
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fetch  # noqa: E402  (reuses the safe e-print unpacker)
    out = []
    for aid, name in BIB_ARXIV.items():
        d = OUT / "bib_src" / aid
        if not d.exists():
            fetch.unpack(get(f"https://arxiv.org/e-print/{aid}", timeout=180), d)
            time.sleep(3)
        entries = []
        for f in sorted(d.rglob("*.bib")):
            entries += bib_entries_bib(f.read_text(encoding="utf-8", errors="replace"))
        if not entries:
            for f in sorted(d.rglob("*.bbl")):
                entries += bib_entries_bbl(f.read_text(encoding="utf-8", errors="replace"))
        print(f"  bib {aid} ({name}): {len(entries)} entries", flush=True)
        out += [{"source": f"bib:{aid}", "source_id": f"{aid}#{i}", "venue": None, "url": None, "abstract": None,
                 "bibliography_of": name, **e} for i, e in enumerate(entries)]
    pdf = OUT / "bib_src" / "lattimore-szepesvari-book.pdf"
    if not pdf.exists():
        pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.write_bytes(get(BOOK_PDF[0], timeout=300))
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
    entries = book_bibliography(text)
    print(f"  bib book ({BOOK_PDF[1]}): {len(entries)} entries", flush=True)
    out += [{"source": "bib:lattimore-szepesvari", "source_id": f"ls#{i}", "venue": None, "url": None,
             "abstract": None, "bibliography_of": BOOK_PDF[1], **e} for i, e in enumerate(entries)]
    return out


# ---------------------------------------------------------------- leads already in the repo

def harvest_leads(since: int) -> list[dict]:
    """Cited-but-missing papers (data/canonical/candidates.yaml) and papers named by gap triage."""
    out = []
    cands = yaml.safe_load((ROOT / "data" / "canonical" / "candidates.yaml").read_text())["candidates"]
    for i, c in enumerate(cands):
        out.append({"source": "leads:cited", "source_id": f"cited#{i}", "title": c["title"], "authors": [],
                    "year": None, "venue": None, "arxiv_id": norm_arxiv(c.get("arxiv_id") or ""), "doi": None,
                    "url": None, "abstract": None, "times_cited": c["times_cited"]})
    tri = yaml.safe_load((ROOT / "data" / "reports" / "triage.yaml").read_text())["triage"]
    for k, v in tri.items():
        for j, pp in enumerate(v.get("papers") or []):
            out.append({"source": "leads:triage", "source_id": f"{k}#{j}", "title": pp["title"], "authors": [],
                        "year": pp.get("year"), "venue": None, "arxiv_id": norm_arxiv(pp.get("arxiv_id") or ""),
                        "doi": None, "url": None, "abstract": None, "claim": pp.get("claim")})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", choices=["arxiv", "pmlr", "neurips", "openalex", "topic", "authors", "bib", "leads", "all"])
    ap.add_argument("--since", type=int, default=1985)
    args = ap.parse_args()
    fns = {"arxiv": harvest_arxiv, "pmlr": harvest_pmlr, "neurips": harvest_neurips, "openalex": harvest_openalex,
           "bib": harvest_bib, "leads": harvest_leads, "topic": harvest_topic, "authors": harvest_authors}
    # "all" skips "authors", which reads the pool built by dedupe.py from the other sources
    for name in ([n for n in fns if n != "authors"] if args.source == "all" else [args.source]):
        write(name, fns[name](args.since))


if __name__ == "__main__":
    main()
