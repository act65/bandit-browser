"""Emit numbers.tex: every number the paper quotes, as LaTeX macros, from the committed data.

The paper (a separate repo) \\input{}s the result, so its numbers always match one state of this repo.
Counts come from data/canonical/ and the manifest; validation figures are parsed from the generated
reports in data/reports/ and data/acceptance-report.md (the scripts that wrote them are the source of
truth for their definitions).

Usage: uv run python pipeline/paper_numbers.py --out ../bandit-browser-paper/numbers.tex
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REP = ROOT / "data" / "reports"
CAN = ROOT / "data" / "canonical"


def grab(text: str, pattern: str, group: int = 1) -> str:
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"pattern not found: {pattern}")
    return m.group(group)


def comma(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "bandit-browser-paper" / "numbers.tex"))
    args = ap.parse_args()
    N: dict[str, str] = {}

    # ---- corpus and extraction
    manifest = yaml.safe_load((ROOT / "corpus" / "manifest.yaml").read_text())["papers"]
    exts = sorted(glob.glob(str(ROOT / "data" / "extractions" / "*.json")))
    runs = [json.loads(Path(f).read_text()).get("_run", {}) for f in exts]
    N["NPapers"] = comma(len(exts))
    have = {Path(f).stem for f in exts}
    by_batch = collections.Counter(p.get("batch") or 0 for p in manifest if p["id"] in have)
    N["NPilotPapers"] = str(by_batch[0])
    N["NBatchOnePapers"] = str(by_batch[1])
    N["NBatchTwoPapers"] = str(by_batch[2])
    N["NPool"] = comma(sum(1 for _ in open(ROOT / "corpus" / "pool.csv")) - 1)
    scr = collections.Counter(json.loads(x).get("label") for x in open(ROOT / "corpus" / "screening.jsonl"))
    N["NScreened"] = comma(sum(scr.values()))
    N["NCore"] = comma(scr["core"])
    cost = sum(r.get("cost_usd_equiv") or 0 for r in runs)
    N["CostTotal"] = comma(round(cost))
    N["CostPerPaper"] = f"{cost / len(runs):.2f}"
    N["TokensInPerPaper"] = comma(round(sum(r.get("input_tokens") or 0 for r in runs) / len(runs) / 1000)) + "k"
    N["TokensOutPerPaper"] = comma(round(sum(r.get("output_tokens") or 0 for r in runs) / len(runs) / 1000)) + "k"
    models = collections.Counter(m for r in runs for m in r.get("models") or [])
    mid = models.most_common(1)[0][0]  # e.g. claude-opus-5-5 -> Claude Opus 5.5
    parts = mid.split("-")
    N["ExtractModel"] = " ".join(w.capitalize() for w in parts[:2]) + " " + ".".join(parts[2:])

    # ---- ontology
    onto_path = sorted((ROOT / "ontology").glob("bandits-*.yaml"),
                       key=lambda p: [int(x) for x in p.stem.split("-")[1].split(".")])[-1]
    onto = yaml.safe_load(onto_path.read_text())
    N["OntologyVersion"] = onto_path.stem.split("-")[1]
    N["NDims"] = str(len(onto["dimensions"]))
    N["NNodeParams"] = str(len(onto.get("node_parameters") or {}))

    # ---- canonical layer
    settings = json.loads((CAN / "settings.json").read_text())
    settings = settings["settings"] if isinstance(settings, dict) else settings
    settings = [s for s in settings if s.get("in_scope") is not False]
    results = json.loads((CAN / "results.json").read_text())
    results = results["results"] if isinstance(results, dict) else results
    N["NSettings"] = comma(len(settings))
    N["NResults"] = comma(len(results))
    papers_per = [len({m.get("paper") for m in s.get("members") or []}) for s in settings]
    N["PctSingleSettings"] = str(round(100 * sum(1 for k in papers_per if k <= 1) / len(settings)))
    N["NCoverEdges"] = comma(len(json.loads((CAN / "poset.json").read_text())))
    si = json.loads((CAN / "site_index.json").read_text())
    N["NInherited"] = comma(sum(1 for b in si["bounds"] if b["inherited"]))
    own = [b for b in si["bounds"] if not b["inherited"]]
    # a growth profile in at least one variable; the rest use paper-specific symbols (or fail to evaluate)
    N["NProfiled"] = comma(sum(1 for b in own if b["profile"]))
    N["PctProfiled"] = str(round(100 * sum(1 for b in own if b["profile"]) / len(own)))
    st = collections.Counter(c["status"] for c in si["cells"])
    N["NCells"] = comma(len(si["cells"]))
    for k, name in [("tight", "NTight"), ("log_gap", "NLogGap"), ("poly_gap", "NPolyGap"), ("conflict", "NConflict"),
                    ("no_lower", "NNoLower"), ("no_upper", "NNoUpper")]:
        N[name] = comma(st[k])
    N["NGaps"] = comma(st["log_gap"] + st["poly_gap"])
    N["NTransfer"] = comma(len(si["transfer"]))
    N["NUnstudied"] = comma(len(si["unstudied"]))
    corr = yaml.safe_load((ROOT / "data" / "corrections.yaml").read_text())
    corr = corr.get("corrections", corr) if isinstance(corr, dict) else corr
    N["NCorrections"] = str(len(corr))

    # ---- validation (parsed from the generated reports)
    a1 = (REP / "audit.md").read_text()
    a2 = (REP / "audit-batch2.md").read_text()
    for tag, txt in [("One", a1), ("Two", a2)]:
        row = re.search(r"\| \*\*overall\*\* \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \((\d+)%–(\d+)%\)", txt)
        N[f"Audit{tag}Major"] = row.group(4) + r"\%"
        N[f"Audit{tag}CI"] = f"{row.group(5)}--{row.group(6)}" + r"\%"
        graded = sum(int(row.group(i)) for i in (1, 2, 3))
        N[f"Audit{tag}Graded"] = str(graded)
        s = re.search(r"\| setting \| (\d+) \| (\d+) \| (\d+) \|", txt)
        N[f"Audit{tag}SettingMinor"] = str(round(100 * int(s.group(2)) / graded)) + r"\%"
        b = re.search(r"\| bound \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \((\d+)%–(\d+)%\)", txt)
        N[f"Audit{tag}BoundMajor"] = b.group(4) + r"\%"
    q = (REP / "audit-quotes.md").read_text()
    N["NQuoteAudited"] = grab(q, r"(\d+) (?:in-scope )?results")
    g = (REP / "goldcheck.md").read_text()
    N["GoldBook"] = grab(g, r"book results: (\d+)")
    N["GoldCheckable"] = grab(g, r"checkable \(with a growth rate\): (\d+)")
    N["GoldRecovered"] = grab(g, r"\*\*recovered\*\*: (\d+)")
    N["GoldRecoveredPct"] = grab(g, r"\*\*recovered\*\*: \d+ \((\d+)%\)") + r"\%"
    N["GoldContradicted"] = grab(g, r"\*\*contradicted\*\*: (\d+)")
    x = (REP / "crosscheck.md").read_text()
    N["XCompared"] = comma(int(grab(x, r"compared: (\d+)")))
    N["XAgreePct"] = grab(x, r"agree\*\* \((\d+)%") + r"\%"
    N["XConsensus"] = grab(x, r"consensus disagreements[^:]*: (\d+)")
    inf = (REP / "audit-inference.md").read_text()
    N["InfJudged"] = str(sum(int(v) for v in re.findall(r"\| (?:lower|upper)/\w+ \| (\d+) \|", inf)))
    N["InfInvalidPct"] = grab(inf, r"\*\*invalid: \d+\*\* \((\d+)%") + r"\%"
    m = re.search(r"\*\*invalid: \d+\*\* \(\d+%, 95% CI (\d+)%–(\d+)%\)", inf)
    N["InfInvalidCI"] = f"{m.group(1)}--{m.group(2)}" + r"\%"
    N["InfCaveat"] = grab(inf, r"needs an unrecorded caveat: (\d+)")
    acc = (ROOT / "data" / "acceptance-report.md").read_text()
    summ = dict((k, int(v)) for v, k in [(v, k) for k, v in re.findall(r"(\w+) (\d+)", grab(acc, r"\*\*Summary:\*\* ([^\n]+)"))])
    N["NFacts"] = str(sum(summ.values()))
    for k in ("PASS", "PASS_STATUS", "PARTIAL", "MANUAL", "FAIL"):
        N["Facts" + k.title().replace("_", "")] = str(summ.get(k, 0))
    tri = yaml.safe_load((REP / "triage.yaml").read_text())["triage"]
    tv = collections.Counter(v.get("verdict") for v in tri.values())
    N["TriageCells"] = str(len(tri))
    N["TriageClosed"] = str(tv["closed"])
    N["TriageOpen"] = str(tv["open_known"])
    N["TriageBlank"] = str(tv["blank"])
    N["TriageClosedPct"] = str(round(100 * tv["closed"] / len(tri))) + r"\%"

    # ---- provenance
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    N["DataCommit"] = sha

    lines = [f"% Generated by bandit-browser/pipeline/paper_numbers.py at commit {sha}. Do not edit by hand."]
    lines += [f"\\newcommand{{\\{k}}}{{{v}\\xspace}}" for k, v in sorted(N.items())]
    Path(args.out).write_text("\n".join(lines) + "\n")
    print(f"{len(N)} macros -> {args.out}")
    for k, v in sorted(N.items()):
        print(f"  {k} = {v}")


if __name__ == "__main__":
    main()
