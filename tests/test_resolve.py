"""Setting keys, scope and corrections (pipeline/resolve.py), and the committed corrections file."""

from __future__ import annotations

import json

import yaml
from conftest import BASE, ONT, ROOT, key, result

import resolve


def test_key_independent_of_list_order_and_trivial_knowledge():
    """The same setting written two ways gets one id (list order; knowing T, K, d is trivial)."""
    a = key(learner_knows=["sigma", "T"], extras=["batched", "delayed_feedback"])
    b = key(learner_knows=["sigma"], extras=["delayed_feedback", "batched"])
    assert resolve.setting_id(a) == resolve.setting_id(b)


def test_implications_closed():
    """function_class implications are closed (linear => quadratic => smooth, convex): otherwise
    a linear setting is not below a convex one and bounds stop flowing."""
    k = key(function_class=["linear"])
    assert {"linear", "quadratic", "smooth", "convex"} <= set(k["function_class"])


def test_unspecified_variance_means_homoscedastic():
    """noise_detail.variance: unstated = homoscedastic (otherwise core K-armed cells split in two)."""
    assert key(noise_detail={"variance": "unspecified"}) == key(noise_detail={"variance": "homoscedastic"})


def test_out_of_scope_rules():
    assert resolve.out_of_scope(key(extras=["federated"]), ONT)
    assert resolve.out_of_scope(key(environment="markovian"), ONT)
    assert resolve.out_of_scope(key(), ONT) is None


def test_corrections_ops():
    r = result("p:r1", "S", "upper", "sqrt(K*T)")
    c = resolve.apply_corrections(r, [
        {"op": "multiply_expression_by", "factor": "T"},
        {"op": "add_condition", "value": "noiseless"},
        {"op": "set", "field": "bound.notation", "value": "Theta"}])
    assert c["bound"]["expression"] == "(T)*(sqrt(K*T))"
    assert c["conditions"] == ["noiseless"] and c["bound"]["notation"] == "Theta"
    assert r["bound"]["expression"] == "sqrt(K*T)" and not r["conditions"]  # the extraction is not edited
    assert len(c["corrections"]) == 3


def test_committed_corrections_target_existing_results():
    """Every entry in data/corrections.yaml targets an extracted result (or paper:* of an extracted
    paper), so a renumbered extraction cannot silently drop a correction."""
    corr = yaml.safe_load((ROOT / "data" / "corrections.yaml").read_text())["corrections"]
    ids = set()
    for f in (ROOT / "data" / "extractions").glob("*.json"):
        ids |= {f"{f.stem}:{r['id']}" for r in json.loads(f.read_text()).get("results") or []}
        ids.add(f"{f.stem}:*")
    missing = [c["target"] for c in corr if c["target"] not in ids]
    assert not missing, missing


def test_base_fixture_is_valid_vocabulary():
    for dim, v in BASE.items():
        vals = ONT["dimensions"][dim].get("values") or {}
        for x in v if isinstance(v, list) else [v]:
            assert x in vals, (dim, x)


def test_unstated_linear_parameter_structure_is_dense():
    """Inference audit round 2: an unstated parameter structure in a linear setting (not_applicable or
    unspecified) means no structure, i.e. dense; read as 'compatible', it let unrestricted lower bounds reach
    sparse settings. In a K-armed setting the field stays not_applicable."""
    lin = dict(action_space="linear_infinite", noise="subgaussian")
    assert key(**lin)["action_set"]["parameter_structure"] == "dense"
    assert key(**lin, action_set={"parameter_structure": "unspecified"})["action_set"]["parameter_structure"] == "dense"
    assert key(**lin, action_set={"parameter_structure": "sparse"})["action_set"]["parameter_structure"] == "sparse"
    assert key()["action_set"]["parameter_structure"] == "not_applicable"
