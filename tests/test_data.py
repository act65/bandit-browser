"""Regression checks on the committed derived data (data/canonical, reports).

CI also re-runs pipeline/derive.py and fails if the committed data differs from what the
code produces, so these checks hold for the code as well as for the files. Thresholds live in
tests/baseline.yaml; changing one is a deliberate, reviewed commit (say why in its message)."""

from __future__ import annotations

import json
import re

import pytest
import yaml
from conftest import ROOT

CAN = ROOT / "data" / "canonical"
BASE = yaml.safe_load((ROOT / "tests" / "baseline.yaml").read_text())


@pytest.fixture(scope="module")
def data():
    return {n: json.loads((CAN / f"{n}.json").read_text()) for n in ("settings", "results", "inferred", "comparison")}


def test_references_resolve(data):
    """Every result points at a setting, every inferred bound at a result and two settings, every
    front entry at a bound: a dangling id means a stale artefact or a renumbered extraction."""
    sids = {s["id"] for s in data["settings"]}
    rids = {r["id"] for r in data["results"]}
    assert all(r["setting_id"] in sids for r in data["results"])
    bad = [x["id"] for x in data["inferred"] if x["from_result"] not in rids
           or x["setting_id"] not in sids or x["from_setting"] not in sids]
    assert not bad, bad[:5]
    iids = {x["id"] for x in data["inferred"]}
    for sid, regs in data["comparison"]["settings"].items():
        assert sid in sids
        for c in regs.values():
            for b in c["upper_front"] + c["lower_front"]:
                assert b.split("@")[0] in rids | iids, b


def test_inference_never_reverses_direction(data):
    """Upper bounds are inherited from more general settings, lower bounds from special cases; a
    record whose source and target settings coincide is a self-loop."""
    for x in data["inferred"][:5000]:
        assert x["from_setting"] != x["setting_id"], x["id"]
        assert x["rule"] in ("upper_bound_to_special_case", "lower_bound_to_generalisation")


def test_cell_counts_within_baseline(data):
    status = [c["status"] for regs in data["comparison"]["settings"].values() for c in regs.values()]
    tight, conflict = status.count("tight"), status.count("conflict")
    assert conflict <= BASE["conflict_cells_max"], f"{conflict} conflict cells (baseline {BASE['conflict_cells_max']})"
    assert tight >= BASE["tight_cells_min"], f"{tight} tight cells (baseline {BASE['tight_cells_min']})"


def test_acceptance_no_regression():
    text = (ROOT / "data" / "acceptance-report.md").read_text()
    summary = dict((k, int(v)) for v, k in [m[::-1] for m in re.findall(r"(\w+) (\d+)", text.split("**Summary:**")[1].splitlines()[0])])
    assert summary.get("FAIL", 0) == 0, summary
    for k, n in BASE["acceptance_min"].items():
        assert summary.get(k, 0) >= n, f"acceptance {k}: {summary.get(k, 0)} < {n}"


def test_gold_set_not_contradicted():
    rows = json.loads((ROOT / "data" / "reports" / "goldcheck.json").read_text())
    bad = [r["id"] for r in rows if r.get("verdict") == "contradicted"]
    assert len(bad) <= BASE["gold_contradicted_max"], bad


def test_no_cell_has_bounds_but_an_empty_front(data):
    """A cell with upper (lower) bounds has a best upper (lower) bound; an empty front means the dominance
    relation removed every bound (the bug behind 49 cells reading 'no upper bound', fixed 2026-10-26)."""
    bad = [(s, r) for s, regs in data["comparison"]["settings"].items() for r, c in regs.items()
           if (c["n_upper"] and not c["upper_front"]) or (c["n_lower"] and not c["lower_front"])]
    assert not bad, bad[:5]
