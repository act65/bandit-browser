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
    dups = {p["id"] for p in manifest if p.get("duplicate_of")}
    exts = sorted(f for f in glob.glob(str(ROOT / "data" / "extractions" / "*.json")) if Path(f).stem not in dups)
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

    def onto_size(path: Path) -> tuple[int, int]:
        o = yaml.safe_load(path.read_text())
        fields = [fs for spec in (o.get("node_parameters") or {}).values() if isinstance(spec, dict)
                  for fs in (spec.get("fields", spec) or {}).values() if isinstance(fs, dict) and "values" in fs]
        values = sum(len(d.get("values") or []) for d in o["dimensions"].values() if isinstance(d, dict))
        return len(fields), values + sum(len(f["values"]) for f in fields)
    first_v = sorted((ROOT / "ontology").glob("bandits-0.5.yaml"))[0]
    N["OntoFieldsFirst"], N["OntoValuesFirst"] = map(str, onto_size(first_v))
    N["OntoFieldsLast"], N["OntoValuesLast"] = map(str, onto_size(onto_path))

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
    cond = [c for c in si["cells"] if c.get("conditional")]
    N["NTightConditional"] = str(sum(1 for c in cond if c["status"] == "tight"))
    N["NTightPlain"] = str(st["tight"] - sum(1 for c in cond if c["status"] == "tight"))
    N["NConditionalVerdicts"] = str(sum(1 for c in cond if c["status"] in ("tight", "log_gap", "poly_gap")))
    # settings by action space that reach a verdict (tight / gap / conflict) in some regime
    verdict = {c["setting_id"] for c in si["cells"] if c["status"] in ("tight", "log_gap", "poly_gap", "conflict")}
    kernel = [x["id"] for x in settings if (x.get("key") or {}).get("action_space") == "kernel_rkhs"]
    N["NKernelSettings"] = str(len(kernel))
    N["NKernelVerdicts"] = str(sum(1 for k in kernel if k in verdict))
    karmed = [x["id"] for x in settings if (x.get("key") or {}).get("action_space") == "finite_K"]
    N["PctKarmedVerdicts"] = str(round(100 * sum(1 for k in karmed if k in verdict) / len(karmed)))
    # convergence per batch: settings already populated by an earlier batch; ontology values first used
    batch_of = {p["id"]: p.get("batch") or 0 for p in manifest if p["id"] in have}
    first = {}
    for x in settings:
        bs = [batch_of[m["paper"]] for m in x.get("members") or [] if m.get("paper") in batch_of]
        if bs:
            first[x["id"]] = min(bs)

    def key_values(key: dict) -> set:
        out = set()
        for k, v in key.items():
            items = v.items() if isinstance(v, dict) else [(None, v)]
            for f, val in items:
                for y in (val if isinstance(val, list) else [val]):
                    if y not in ("not_applicable", "unspecified", None):
                        out.add((k, f, str(y)))
        return out
    seen: set = set()
    words = {0: "Pilot", 1: "One", 2: "Two", 3: "Three"}
    for b in sorted(words):
        members = [(x["id"], m) for x in settings for m in x.get("members") or [] if batch_of.get(m.get("paper")) == b]
        new_vals = set().union(*[key_values(x["key"]) for x in settings if first.get(x["id"]) == b]) - seen
        seen |= new_vals
        N[f"ValuesFirst{words[b]}"] = str(len(new_vals))
        if b:
            N[f"Reuse{words[b]}"] = str(round(100 * sum(1 for sid, _ in members if first[sid] < b) / len(members))) + r"\%"
            N[f"NewSettings{words[b]}"] = comma(sum(1 for sid in first if first[sid] == b))
    N["ValuesUsed"] = str(len(seen))
    unm = collections.Counter()
    for f in exts:
        b = batch_of.get(Path(f).stem)
        for x in json.loads(Path(f).read_text())["settings"]:
            if x.get("in_scope") is not False:
                unm[(b, "s")] += 1
                unm[(b, "u")] += len(x.get("unmapped") or [])
    for b in (1, 2, 3):
        N[f"Unmapped{words[b]}"] = f"{unm[(b, 'u')] / unm[(b, 's')]:.1f}"
    patches = yaml.safe_load((ROOT / "data" / "field-patches.yaml").read_text())["patches"]
    patched = {k for k, v in patches.items() if any(x != "keep" for x in v.values())}
    N["PctPatched"] = str(round(100 * len(patched) / sum(unm[(b, "s")] for b in (0, 1, 2, 3)))) + r"\%"
    syms = yaml.safe_load((ROOT / "data" / "symbol-classes.yaml").read_text())["classes"]
    N["NSymbolPairs"] = comma(len(syms))
    N["NTransfer"] = comma(len(si["transfer"]))
    N["NUnstudied"] = comma(len(si["unstudied"]))
    corr = yaml.safe_load((ROOT / "data" / "corrections.yaml").read_text())
    corr = corr.get("corrections", corr) if isinstance(corr, dict) else corr
    N["NCorrections"] = str(len(corr))

    # ---- validation (parsed from the generated reports)
    audits = [("One", "audit"), ("Two", "audit-batch2"), ("Three", "audit-batch3")]
    for tag, txt in [(t, (REP / f"{f}.md").read_text()) for t, f in audits]:
        row = re.search(r"\| \*\*overall\*\* \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \((\d+)%–(\d+)%\)", txt)
        N[f"Audit{tag}Major"] = row.group(4) + r"\%"
        N[f"Audit{tag}CI"] = f"{row.group(5)}--{row.group(6)}" + r"\%"
        graded = sum(int(row.group(i)) for i in (1, 2, 3))
        N[f"Audit{tag}Graded"] = str(graded)
        s = re.search(r"\| setting \| (\d+) \| (\d+) \| (\d+) \|", txt)
        N[f"Audit{tag}SettingMinor"] = str(round(100 * int(s.group(2)) / graded)) + r"\%"
        b = re.search(r"\| bound \| (\d+) \| (\d+) \| (\d+) \| (\d+)% \((\d+)%–(\d+)%\)", txt)
        N[f"Audit{tag}BoundMajor"] = b.group(4) + r"\%"
    # kinds of setting error (pipeline/audit_taxonomy.py), shares over all audits
    tax = json.loads((REP / "audit-taxonomy.json").read_text())["labels"]
    N["TaxItems"] = str(len(tax))
    for kind, name in [("knowledge", "Knowledge"), ("missing_assumption", "MissingAssumption"), ("noise", "Noise"),
                       ("protocol_feature", "Protocol"), ("environment", "Environment"), ("action_space", "Action")]:
        N[f"Tax{name}"] = str(round(100 * sum(kind in v for v in tax.values()) / len(tax))) + r"\%"
    N["NCorrectionsFromConflicts"] = str(sum(1 for c in corr if re.search(r"conflict", c.get("reason") or "", re.I)))

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

    # ---- saturation (pipeline/saturation.py) and ablations (pipeline/ablate.py)
    sat = json.loads((REP / "saturation.json").read_text())
    rows = sat["rows"]
    full = max(r["n"] for r in rows)
    mid = min({r["n"] for r in rows}, key=lambda n: abs(n - full / 2))  # the subset closest to half the corpus
    rand = [r for r in rows if r["order"].startswith("random")]
    t_mid = sum(r["tight"] for r in rand if r["n"] == mid) / len({r["order"] for r in rand})
    t_full = next(r["tight"] for r in rows if r["n"] == full)
    N["SatMidPapers"] = comma(mid)
    N["SatMidTight"] = str(round(t_mid))
    N["SatRateFirst"] = f"{100 * t_mid / mid:.0f}"
    N["SatRateSecond"] = f"{100 * (t_full - t_mid) / (full - mid):.0f}"
    pilot = next(r for r in rows if r["order"] == "batch" and r["n"] == min(x["n"] for x in rows))
    N["SatPilotTight"] = str(pilot["tight"])
    multi = {r["n"]: r["settings_multi_paper"] for r in rows if r["order"] == "batch"}
    N["SatMultiFull"] = str(multi[full])
    abl = json.loads((REP / "ablations.json").read_text())
    for r in abl["rules"]:
        name = "".join(w.capitalize() for w in r["rule"].split("_"))
        N[f"Abl{name}Conflict"] = comma(r["conflict"])
        N[f"Abl{name}Changed"] = comma(r["changed"])

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
