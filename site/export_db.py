"""Write the site's SQLite database (_site/data/atlas.db.NNN + config.json).

The static site reads it in the browser with sql.js-httpvfs: HTTP range requests fetch only
the database pages a query touches, so the site stays static (GitHub Pages) while list pages
become queries. Tables:

  settings, papers, setting_papers      the corpus and canonical settings, with facet columns
  bounds                                every own and inherited bound (one row per bound)
  cells                                 setting x regime comparison: status, rates, best bounds
  triage                                gap-triage verdicts
  labels                                display labels for facet values
  docs                                  gzip-compressed HTML of setting and paper pages
  settings_fts, papers_fts              FTS5 indexes for text search
  meta                                  build information

The database is split into fixed-size chunks (GitHub limits files to 100 MB) named by a hash
of the content and described by config.json (the "chunked" server mode of sql.js-httpvfs).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import sqlite3
from pathlib import Path

PAGE_SIZE = 4096                 # also the request size: one database page per range request
CHUNK_BYTES = 10 * 1024 * 1024   # file chunk size on the server

SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE labels (dim TEXT, value TEXT, label TEXT, PRIMARY KEY (dim, value));
CREATE TABLE papers (
  id TEXT PRIMARY KEY, slug TEXT, cite TEXT, title TEXT, authors TEXT, year INTEGER, venue TEXT,
  arxiv_id TEXT, url TEXT, extracted INTEGER, n_settings INTEGER, n_results INTEGER, batch TEXT);
CREATE TABLE settings (
  id TEXT PRIMARY KEY, slug TEXT UNIQUE, name TEXT,
  objective TEXT, feedback TEXT, environment TEXT, action_space TEXT, context TEXT, noise TEXT,
  function_class TEXT, instance_assumptions TEXT, extras TEXT, learner_knows TEXT,
  n_papers INTEGER, n_upper INTEGER, n_lower INTEGER, n_inh_upper INTEGER, n_inh_lower INTEGER,
  up_src TEXT, lo_src TEXT, status TEXT, status_regime TEXT);
CREATE TABLE setting_papers (setting_id TEXT, paper_id TEXT, PRIMARY KEY (setting_id, paper_id));
CREATE TABLE bounds (
  id TEXT PRIMARY KEY, setting_id TEXT, side TEXT, regime TEXT, quantity TEXT, notation TEXT,
  inherited INTEGER, from_setting TEXT, paper_id TEXT, cite TEXT, year INTEGER, algorithm TEXT,
  algorithm_family TEXT, confidence TEXT, restricted INTEGER, in_rate INTEGER, tex TEXT, expr TEXT);
CREATE TABLE cells (
  setting_id TEXT, regime TEXT, status TEXT, n_upper INTEGER, n_lower INTEGER, relies_inherited INTEGER,
  per_var TEXT, up_tex TEXT, lo_tex TEXT, up_cite TEXT, lo_cite TEXT, triage TEXT,
  PRIMARY KEY (setting_id, regime));
CREATE TABLE triage (setting_id TEXT, regime TEXT, verdict TEXT, summary TEXT, papers TEXT, date TEXT,
  PRIMARY KEY (setting_id, regime));
CREATE TABLE docs (kind TEXT, key TEXT, title TEXT, html BLOB, PRIMARY KEY (kind, key));
CREATE VIRTUAL TABLE settings_fts USING fts5(slug UNINDEXED, name, facets);
CREATE VIRTUAL TABLE papers_fts USING fts5(slug UNINDEXED, title, authors, cite);
CREATE INDEX bounds_setting ON bounds (setting_id);
CREATE INDEX bounds_facets ON bounds (side, regime, inherited);
CREATE INDEX bounds_paper ON bounds (paper_id);
CREATE INDEX cells_status ON cells (status, regime);
CREATE INDEX setting_papers_paper ON setting_papers (paper_id);
"""

FACET_DIMS = ["objective", "feedback", "environment", "action_space", "context", "noise",
              "function_class", "instance_assumptions", "extras", "learner_knows"]


def _facet(v) -> str:
    """Multi-valued dims are stored space-separated (values are snake_case), queried with LIKE."""
    if isinstance(v, list):
        return " ".join(str(x) for x in v) or "none"
    return str(v) if v not in (None, "") else "none"


def export(site, A, docs: dict, out_dir: Path, value_label, regime_label, status_labels: dict, triage: dict) -> dict:
    """Build the database from the site model `site`, the analysis `A` and pre-rendered `docs`
    {(kind, key): (title, html)}; write chunks + config.json into out_dir. Returns stats."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / "atlas.build.db"
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    con.execute(f"PRAGMA page_size = {PAGE_SIZE}")
    con.execute("PRAGMA journal_mode = DELETE")
    con.executescript(SCHEMA)

    labels = {}
    def lab(dim, v):
        labels[(dim, v)] = value_label(dim, v) if v != "none" else "none"

    # settings
    rows, fts, sp = [], [], []
    for n in site.nodes.values():
        key = n["key"]
        raw = n.get("raw") or {}
        fac = {d: _facet(raw.get(d, key.get(d))) for d in FACET_DIMS}
        for d, s in fac.items():
            for v in s.split():
                lab(d, v)
        up, lo = site.counts(n)
        iu, il = site.counts(n, "inherited")
        inh_sides = {b["side"] for b in A.by_setting.get(n["id"]) or [] if b.get("inherited")}
        src = {s: ("own" if c else "inherited" if s in inh_sides else "none") for s, c in (("upper", up), ("lower", lo))}
        st, streg = A.setting_status(n["id"]) if A.ok else ("none", None)
        rows.append((n["id"], n["slug"], n["name"], *[fac[d] for d in FACET_DIMS], len(n["papers"]), up, lo, iu, il,
                     src["upper"], src["lower"], st, streg))
        fts.append((n["slug"], n["name"], " ".join(labels[(d, v)] for d in FACET_DIMS for v in fac[d].split())))
        sp += [(n["id"], p) for p in sorted(n["papers"])]
    con.executemany(f"INSERT INTO settings VALUES ({','.join('?' * 22)})", rows)
    con.executemany("INSERT INTO settings_fts VALUES (?,?,?)", fts)
    con.executemany("INSERT OR IGNORE INTO setting_papers VALUES (?,?)", sp)

    # papers
    n_set = {}
    for sid, p in sp:
        n_set[p] = n_set.get(p, 0) + 1
    prow, pfts = [], []
    for pid in site.paper_ids():
        info = site.paper_info(pid)
        ex = site.extractions.get(pid) or {}
        authors = info.get("authors") or (ex.get("paper") or {}).get("authors") or []
        authors = ", ".join(authors) if isinstance(authors, list) else str(authors)
        slug = site.slug_of_paper(pid)
        prow.append((pid, slug, site.cite(pid), site.title(pid), authors, info.get("year"), info.get("venue"),
                     info.get("arxiv_id"), info.get("url"), int(bool(ex)), n_set.get(pid, 0),
                     len(ex.get("results") or []), str(info.get("batch") or "")))
        pfts.append((slug, site.title(pid), authors, site.cite(pid)))
    con.executemany(f"INSERT INTO papers VALUES ({','.join('?' * 13)})", prow)
    con.executemany("INSERT INTO papers_fts VALUES (?,?,?,?)", pfts)

    # bounds (own and inherited, as in the analysis index)
    brow = []
    for b in A.bounds.values():
        tex, ok = A.tex(b)
        alg = (site.algorithms.get(b.get("algorithm_id") or "") or {}).get("name") or b.get("algorithm_id")
        reg = A.regime(b)
        brow.append((b["id"], b["setting_id"], b["side"], reg, b.get("quantity"), b.get("notation") or "exact",
                     int(bool(b.get("inherited"))), b.get("from_setting"), b.get("paper"), site.cite(b.get("paper")),
                     b.get("year"), alg, b.get("algorithm_family") or "none", b.get("confidence") or "unknown",
                     int(bool(b.get("restricted"))), int(b.get("rate_regime") == reg), tex if ok else None,
                     None if ok else b.get("expression")))
        labels[("regime", reg)] = regime_label(reg)
    con.executemany(f"INSERT OR REPLACE INTO bounds VALUES ({','.join('?' * 18)})", brow)

    # cells, with the best bound on each side rendered
    def best(ids):
        for bid in ids:
            b = A.bound(bid)
            if b:
                tex, ok = A.tex(b)
                return (tex if ok else b.get("expression")), site.cite(b.get("paper"))
        return None, None
    crow = []
    for c in A.cells:
        ut, uc = best(c.get("upper_front") or [])
        lt, lc = best(c.get("lower_front") or [])
        tri = triage.get(f"{c['setting_id']}|{c['regime']}")
        crow.append((c["setting_id"], c["regime"], c["status"], c["n_upper"], c["n_lower"],
                     int(bool(c.get("relies_on_inherited"))), json.dumps(c.get("per_var") or {}), ut, lt, uc, lc,
                     (tri or {}).get("verdict")))
        labels[("regime", c["regime"])] = regime_label(c["regime"])
    con.executemany(f"INSERT OR REPLACE INTO cells VALUES ({','.join('?' * 12)})", crow)
    con.executemany("INSERT OR REPLACE INTO triage VALUES (?,?,?,?,?,?)",
                    [(*k.split("|", 1), v.get("verdict"), v.get("summary"), json.dumps(v.get("papers") or []),
                      str(v.get("date") or "")) for k, v in triage.items() if k.split("|")[0] in site.nodes])
    for k, v in status_labels.items():
        labels[("status", k)] = v
    con.executemany("INSERT INTO labels VALUES (?,?,?)", [(d, v, l) for (d, v), l in labels.items()])

    # documents
    con.executemany("INSERT INTO docs VALUES (?,?,?,?)",
                    [(k, key, title, gzip.compress(html.encode("utf-8"), 9)) for (k, key), (title, html) in docs.items()])
    con.executemany("INSERT INTO meta VALUES (?,?)", [("built_with", "site/build.py"), ("n_settings", str(len(rows))),
                                                      ("n_papers", str(len(prow))), ("n_bounds", str(len(brow)))])
    con.execute("INSERT INTO settings_fts(settings_fts) VALUES ('optimize')")
    con.execute("INSERT INTO papers_fts(papers_fts) VALUES ('optimize')")
    con.commit()
    con.execute("VACUUM")
    con.close()

    # split into chunks for the static server
    for old in out_dir.glob("atlas*.db.*"):
        old.unlink()
    data = tmp.read_bytes()
    tmp.unlink()
    # content-addressed chunk names: a browser can never mix chunks of two builds
    version = hashlib.sha1(data).hexdigest()[:10]
    prefix = f"atlas-{version}.db."
    n_chunks = max(1, math.ceil(len(data) / CHUNK_BYTES))
    for i in range(n_chunks):
        (out_dir / f"{prefix}{i:03d}").write_bytes(data[i * CHUNK_BYTES:(i + 1) * CHUNK_BYTES])
    config = {"serverMode": "chunked", "requestChunkSize": PAGE_SIZE, "databaseLengthBytes": len(data),
              "serverChunkSize": CHUNK_BYTES, "urlPrefix": prefix, "suffixLength": 3}
    (out_dir / "config.json").write_text(json.dumps(config))
    return {"version": version, "bytes": len(data), "chunks": n_chunks, "settings": len(rows), "papers": len(prow), "bounds": len(brow),
            "cells": len(crow), "docs": len(docs)}
