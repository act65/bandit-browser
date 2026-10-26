"""The specialisation order (pipeline/order.py): S ⊑ S' iff S is a special case of S'.

Claims: the order goes the right way on each dimension; it is a partial order (no two
distinct settings below each other); edges with requirements (graph feedback ⊑ bandit,
bandit ⊑ partial monitoring) enforce them; reductions carry their parameter maps; the
K-armed embedding reaches only action sets that contain it. Most fixtures are past bugs."""

from __future__ import annotations

import itertools

import pytest
from conftest import LINEAR_BALL, LINEAR_FINITE, ONT, key

from order import Order

O = Order(ONT)


def leq(a: dict, b: dict) -> bool:
    return O.leq(a, b) is not None


def test_stochastic_below_adversarial_not_reverse():
    """Upper bounds flow from adversarial to stochastic, never back (a swapped pair in the
    closure would send stochastic log T rates to adversarial settings)."""
    sto, adv = key(), key(environment="adversarial_oblivious")
    assert leq(sto, adv) and not leq(adv, sto)


def test_more_knowledge_is_special_case():
    """learner_knows: knowing more is a special case (subset rule), not the reverse."""
    knows, not_ = key(learner_knows=["sigma"]), key()
    assert leq(knows, not_) and not leq(not_, knows)


def test_noise_order_direction():
    """Bernoulli ⊑ [0,1] ⊑ sub-Gaussian ⊑ heavy-tailed."""
    chain = [key(noise=n) for n in ("bernoulli", "bounded_01", "subgaussian", "heavy_tailed")]
    for a, b in itertools.combinations(chain, 2):
        assert leq(a, b) and not leq(b, a)


def test_k_armed_embeds_in_finite_linear_with_map():
    """K-armed ⊑ linear with finitely many actions via d = K (the parameter map must be recorded,
    or linear bounds in d reach K-armed settings with d unbound)."""
    ch = O.leq(key(), key(**LINEAR_FINITE))
    assert ch is not None
    red = [c for c in ch if c.dim == "action_space"]
    assert red and red[0].kind == "reduction" and red[0].param_map.get("d") == "K"


def test_k_armed_not_below_unit_ball():
    """Regression (inference audit 2026-10-26): the basis-vector action set of a K-armed bandit is not
    a unit ball, so K-armed ⋢ linear on the unit ball. Before the fix, action_set.shape =
    not_applicable deferred and sqrt(KT) lower bounds reached unit-ball settings."""
    assert not leq(key(), key(**LINEAR_BALL))


def test_k_armed_below_arbitrary_compact_linear():
    """... but it is a special case of linear bandits on arbitrary compact action sets."""
    assert leq(key(), key(**{**LINEAR_BALL, "action_set": {"shape": "arbitrary_compact", "time_varying": "fixed"}}))


def test_graph_feedback_below_bandit_needs_self_loops():
    """Regression: graph feedback ⊑ bandit only if every action observes its own loss
    (self_loops = all). Without self-loops a bandit algorithm cannot run on the graph problem."""
    graph = dict(feedback="graph_feedback", environment="adversarial_oblivious")
    adv_bandit = key(environment="adversarial_oblivious")
    with_loops = key(**graph, feedback_graph={"self_loops": "all", "observability": "strongly_observable"})
    without = key(**graph, feedback_graph={"self_loops": "optional", "observability": "observable"})
    unspec = key(**graph, feedback_graph={"self_loops": "unspecified", "observability": "strongly_observable"})
    assert leq(with_loops, adv_bandit)
    assert not leq(without, adv_bandit)
    ch = O.leq(unspec, adv_bandit)  # unstated: allowed with a caveat
    assert ch is not None and any("self_loops" in cv for c in ch for cv in c.caveats)


def test_unspecified_observability_not_below_observable():
    """Regression (v0.4.1): unspecified ⊑ observable let Omega(T) bounds for non-observable graphs
    reach observable ones; unspecified is compatible with a caveat only, never ordered below."""
    pairs = O.orders["feedback_graph.observability"]
    assert ("unspecified", "observable") not in pairs and ("strongly_observable", "observable") in pairs


def test_partial_monitoring_requires_a_class_of_games():
    """bandit ⊑ partial monitoring only for a class of games (requires_general, strict): a specific
    mechanism (unspecified) is not a generalisation of the bandit problem."""
    bandit = key(environment="adversarial_oblivious")
    pm = dict(feedback="partial_monitoring", environment="adversarial_oblivious")
    assert leq(bandit, key(**pm, partial_monitoring={"observability": "locally_observable"}))
    assert not leq(bandit, key(**pm, partial_monitoring={"observability": "unspecified"}))


def test_fixed_parameter_is_special_case():
    """Fixing K = 2 is a special case; the Change records the fixed value."""
    ch = O.leq(key(parameters={"K": 2}), key())
    assert ch is not None and ch[-1].kind == "parameter" and ch[-1].param_map == {"K": 2}
    assert not leq(key(), key(parameters={"K": 2}))


def test_scalar_orders_are_antisymmetric():
    """The closure of every scalar order is a strict partial order: no cycles (a cycle would make two
    different settings each a special case of the other, and bounds would flow both ways)."""
    for dim, rel in O.orders.items():
        cyc = [(a, b) for a, b in rel if (b, a) in rel]
        assert not cyc, f"{dim}: cycle {cyc[:3]}"


def test_leq_is_strict_and_antisymmetric_on_real_settings():
    """On the canonical settings: S ⋢ S, and S ⊑ S' ⊑ S for distinct keys only through
    caveated `unspecified` steps (an unstated value is treated as compatible both ways, by design)."""
    import json

    from conftest import ROOT
    settings = json.loads((ROOT / "data" / "canonical" / "settings.json").read_text())[:400]
    keys = [s["key"] for s in settings]
    for k in keys:
        assert O.leq(k, k) is None
    below = {(i, j): O.leq(keys[i], keys[j]) for i, j in itertools.permutations(range(len(keys)), 2)}
    below = {p: ch for p, ch in below.items() if ch}
    bad = [(settings[i]["id"], settings[j]["id"]) for (i, j), ch in below.items() if (j, i) in below
           and not all("unspecified" in (c.special, c.general) and c.caveats for c in ch)]
    assert not bad, bad[:3]


def test_top_value_not_below_unspecified():
    """Regression (2026-10-26): a field's most general value (any_game, any_graph) was 'compatible'
    with unspecified both ways, so a lower bound proved over all games reached a setting with one
    unstated game. unspecified ⊑ top is fine (with a caveat); top ⊑ unspecified is not."""
    pm = dict(feedback="partial_monitoring", environment="adversarial_oblivious")
    anyg = key(**pm, partial_monitoring={"observability": "any_game"})
    unsp = key(**pm, partial_monitoring={"observability": "unspecified"})
    assert leq(unsp, anyg) and not leq(anyg, unsp)


@pytest.mark.parametrize("env", ["stochastic_corrupted", "adversarial_self_bounding", "adversarial_adaptive"])
def test_iid_below_environment_generalisations(env):
    assert leq(key(), key(environment=env))


def test_corrupted_regret_reference_must_match():
    """Inference audit 2026-10-26: adversarial bounds are on the realised (corrupted) rewards; regret against the
    uncorrupted means differs by up to C, so uncorrupted-reference settings are not special cases."""
    adv = key(environment="adversarial_oblivious")
    real = key(environment="stochastic_corrupted", corruption={"regret_reference": "corrupted"})
    clean = key(environment="stochastic_corrupted", corruption={"regret_reference": "uncorrupted"})
    assert leq(real, adv) and not leq(clean, adv)


def test_k_armed_to_linear_only_without_contexts():
    """Inference audit 2026-10-26: d = K embeds the non-contextual K-armed bandit; with M_ctx contexts the
    linear dimension is K * M_ctx (or the problem is not linear), so the reduction must not apply."""
    ctx = dict(context="stochastic_contexts")
    assert leq(key(), key(**LINEAR_FINITE))
    assert not leq(key(**ctx), key(**ctx, **LINEAR_FINITE))


def test_k_armed_embedding_is_dense_box_parameters():
    """Inference audit round 2: the K-armed embedding has theta = the mean vector in [0,1]^K, which is dense and
    not in an l2 ball, so K-armed ⋢ sparse linear and ⋢ linear with an l2-ball parameter set."""
    lin = dict(action_space="linear_finite", noise="subgaussian")
    fin = {"shape": "finite", "time_varying": "fixed"}
    assert leq(key(), key(**lin, action_set={**fin, "parameter_structure": "dense"}))
    assert not leq(key(), key(**lin, action_set={**fin, "parameter_structure": "sparse"}))
    assert not leq(key(), key(**lin, action_set={**fin, "parameter_set": "l2_ball"}))
    assert leq(key(), key(**lin, action_set={**fin, "parameter_set": "arbitrary_bounded"}))
