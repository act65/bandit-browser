"""Gap triage: search for papers that resolve candidate gaps before calling them open.

For each candidate gap in data/canonical/comparison.json (log or polynomial gap, plus
missing lower bounds in well-studied settings with --missing), one `claude -p` call
with WebSearch/WebFetch only (it never sees paper text) looks for published results
that close the gap. Verdicts:
  closed      a paper outside the corpus matches the upper or lower bound (corpus gap)
  open_known  the literature states the gap is open (e.g. a COLT open problem)
  blank       nothing found either way: the system does not know
Searches that find nothing are logged too (negative evidence, D8).

Writes data/reports/triage.yaml (merged with earlier runs; use --force to redo). Setting ids
change whenever the ontology does; `--remap` moves verdicts to the renamed settings by key
(`--old-settings` gives keys for verdicts written before keys were stored).
Usage: uv run python pipeline/triage.py [--limit N] [--missing] [--force] [--remap [--old-settings F]]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_cli  # noqa: E402
import report  # noqa: E402
import schema  # noqa: E402

ROOT = schema.ROOT
CAN = ROOT / "data" / "canonical"
OUT = ROOT / "data" / "reports" / "triage.yaml"

SYSTEM = """You are a careful research assistant in theoretical machine learning (bandits).
You are given a problem setting and the best upper and lower bounds that our database of
a few hundred papers contains for it. Our database is incomplete. Search the literature (arXiv,
proceedings, surveys, the Lattimore-Szepesvari book) to determine whether the gap between
these bounds is already closed by some published result, is known to be open, or neither.
Only report a paper if you have seen its title and the relevant claim in a search result
or fetched page during this session; if your tools fail, say so in the summary and use
verdict "blank" rather than answering from memory. Prefer precise
citations (title, authors, year, arXiv id). Record the searches you ran."""

SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["verdict", "summary", "papers", "searches"],
    "properties": {
        "verdict": {"enum": ["closed", "open_known", "blank"]},
        "summary": {"type": "string"},
        "papers": {"type": "array", "items": {"type": "object", "additionalProperties": False,
                   "required": ["title", "year", "arxiv_id", "claim"],
                   "properties": {"title": {"type": "string"}, "year": {"type": ["integer", "null"]},
                                  "arxiv_id": {"type": ["string", "null"]}, "claim": {"type": "string"}}}},
        "searches": {"type": "array", "items": {"type": "string"}},
    },
}


def candidates(missing: bool) -> list[dict]:
    settings, results, inferred, cmp, _ = report.load()
    out = []
    for sid, regimes in cmp["settings"].items():
        for reg, c in regimes.items():
            want = c["status"] in ("log_gap", "poly_gap") or \
                (missing and c["status"] == "no_lower" and len(report.papers_of(sid, settings)) >= report.WELL_STUDIED)
            if not want:
                continue
            out.append({
                "id": f"{sid}|{reg}", "setting": settings[sid]["label"], "key": settings[sid]["key"],
                "regime": reg, "status": c["status"],
                "per_var": c["per_var"],
                "best_upper": [report.describe(e, results, inferred) for e in c["upper_front"][:3]],
                "best_lower": [report.describe(e, results, inferred) for e in c["lower_front"][:3]],
            })
    return out


def triage_one(c: dict) -> dict:
    user = json.dumps({k: c[k] for k in ("setting", "key", "regime", "status", "per_var", "best_upper", "best_lower")},
                      ensure_ascii=False, indent=1)
    out, env = claude_cli.call_structured(SYSTEM, user, SCHEMA, tools="WebSearch,WebFetch",
                                          label=f"triage:{c['id']}", timeout=1200)
    return {**out, "date": dt.date.today().isoformat(), "models": list((env.get("modelUsage") or {}).keys()),
            "setting": c["setting"], "key": c["key"], "regime": c["regime"], "status": c["status"]}


def key_matches(old: dict, new: dict) -> bool:
    """`new` agrees with `old` on every field `old` has; fields added to the ontology since
    (absent from `old`) are ignored, since the verdict's search did not depend on them."""
    for dim, v in old.items():
        if isinstance(v, dict):
            if any((new.get(dim) or {}).get(f, "not_applicable") != x for f, x in v.items()):
                return False
        elif new.get(dim) != v:
            return False
    return True


def remap(done: dict, old_settings: Path | None) -> int:
    """Re-attach verdicts whose setting id disappeared (ids hash the whole key, so every
    ontology change renames settings) to the current settings with a matching key."""
    settings = {s["id"]: s for s in json.loads((CAN / "settings.json").read_text())}
    cmp = json.loads((CAN / "comparison.json").read_text())["settings"]
    old_keys = ({s["id"]: s["key"] for s in json.loads(old_settings.read_text())} if old_settings else {})
    moved = 0
    for vid in [v for v in done if v.split("|")[0] not in settings]:
        sid, _, reg = vid.partition("|")
        key = done[vid].get("key") or old_keys.get(sid)
        if not key:
            continue
        for nid, s in settings.items():
            if key_matches(key, s["key"]) and reg in cmp.get(nid, {}) and f"{nid}|{reg}" not in done:
                done[f"{nid}|{reg}"] = {**done[vid], "key": s["key"], "remapped_from": vid,
                                        "status_now": cmp[nid][reg]["status"]}
                moved += 1
        del done[vid]
    return moved


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--missing", action="store_true", help="also triage missing lower bounds")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--remap", action="store_true", help="only re-attach stale verdicts to renamed settings")
    ap.add_argument("--old-settings", type=Path, default=None,
                    help="settings.json from before the rename (for verdicts written without a key)")
    args = ap.parse_args()
    done = yaml.safe_load(OUT.read_text())["triage"] if OUT.exists() else {}
    if args.remap:
        n = remap(done, args.old_settings)
        OUT.write_text("# Gap triage (pipeline/triage.py). Verdicts: closed | open_known | blank.\n"
                       + yaml.safe_dump({"triage": done}, sort_keys=False, allow_unicode=True, width=110))
        print(f"remapped {n} verdicts; {len(done)} kept")
        return
    todo = [c for c in candidates(args.missing) if args.force or c["id"] not in done][: args.limit]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(triage_one, c): c for c in todo}
        for f in as_completed(futs):
            c = futs[f]
            try:
                done[c["id"]] = f.result()
                print(f"{done[c['id']]['verdict']:10s} {c['setting'][:70]} ({c['regime']})", flush=True)
            except claude_cli.QuotaExhausted as e:
                print(f"QUOTA: {e}")
                break
            except Exception as e:
                print(f"FAIL {c['id']}: {e}", flush=True)
            OUT.write_text("# Gap triage (pipeline/triage.py). Verdicts: closed | open_known | blank.\n"
                           + yaml.safe_dump({"triage": done}, sort_keys=False, allow_unicode=True, width=110))


if __name__ == "__main__":
    main()
