"""Run resolve -> infer -> compare on a copy of the repo, optionally on a subset of papers or with rules switched off.

Shared by pipeline/saturation.py (subsets of the corpus) and pipeline/ablate.py (rules off). The copy lives in a
temporary directory, so the committed data is never touched. Returns the cell statuses and a few counts from the
copy's data/canonical/.
"""

from __future__ import annotations

import collections
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERDICT = ("tight", "log_gap", "poly_gap", "conflict")


def batches() -> dict[str, int]:
    """Paper id -> batch (0 = pilot) for every extracted, non-duplicate manifest paper."""
    import yaml
    man = yaml.safe_load((ROOT / "corpus" / "manifest.yaml").read_text())["papers"]
    have = {f.stem for f in (ROOT / "data" / "extractions").glob("*.json")}
    return {p["id"]: p.get("batch") or 0 for p in man if not p.get("duplicate_of") and p["id"] in have}


def run(papers: set[str] | None = None, ablate: tuple[str, ...] = (), keep: Path | None = None) -> dict:
    """Derive the comparison for `papers` (None: all) with the rules in `ablate` switched off."""
    tmp = Path(tempfile.mkdtemp(prefix="atlas-run-", dir=keep))
    try:
        for d in ("pipeline", "ontology"):
            shutil.copytree(ROOT / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__"))
        (tmp / "corpus").mkdir()
        shutil.copy(ROOT / "corpus" / "manifest.yaml", tmp / "corpus")
        shutil.copytree(ROOT / "data", tmp / "data", ignore=shutil.ignore_patterns("extractions", "extractions_verified",
                                                                                  "canonical", "reports"))
        (tmp / "data" / "canonical").mkdir()
        (tmp / "data" / "reports").mkdir()
        shutil.copy(ROOT / "data" / "reports" / "triage.yaml", tmp / "data" / "reports")
        (tmp / "data" / "extractions").mkdir()
        for f in (ROOT / "data" / "extractions").glob("*.json"):
            if papers is None or f.stem in papers:
                try:
                    os.link(f, tmp / "data" / "extractions" / f.name)
                except OSError:  # temporary directory on another device
                    shutil.copy(f, tmp / "data" / "extractions" / f.name)
        env = {**os.environ, "ATLAS_ABLATE": ",".join(ablate)}
        for step in ("resolve", "infer", "compare"):
            subprocess.run(["uv", "run", "--project", str(ROOT), "python", str(tmp / "pipeline" / f"{step}.py")],
                           cwd=tmp, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return summarise(tmp / "data" / "canonical")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def summarise(can: Path) -> dict:
    cmp = json.loads((can / "comparison.json").read_text())
    settings = json.loads((can / "settings.json").read_text())
    settings = settings["settings"] if isinstance(settings, dict) else settings
    results = json.loads((can / "results.json").read_text())
    cells = {f"{sid}|{reg}": c["status"] for sid, regs in cmp["settings"].items() for reg, c in regs.items()}
    st = collections.Counter(cells.values())
    multi = sum(1 for s in settings if len({m.get("paper") for m in s.get("members") or []}) > 1)
    return {"papers": len({r["paper"] for r in results}), "settings": len(settings),
            "settings_multi_paper": multi, "results": len(results), "cells": len(cells),
            "verdict_cells": sum(st[k] for k in VERDICT), **{k: st[k] for k in (*VERDICT, "no_lower", "no_upper")},
            "conflicts": sorted(f"{c['setting_id']}|{c['family']}|{c['dependence']}" for c in cmp["conflicts"]),
            "status": cells}
