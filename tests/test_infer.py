"""Bound transfer along the order (pipeline/infer.py).

Claims: upper bounds go to special cases, lower bounds to generalisations, never the other
way; reductions translate symbols in the right direction (d = K down, K := d up); per-arm
lower bounds do not cross reductions; lower bounds hold for a learner with more class-level
(not instance) knowledge; fixed-parameter lower bounds are flagged; a bound's own regime
blocks transfers it excludes; Bayesian lower bounds become worst-case ones; graph lower bounds
are instantiated at the bandit graph only when stated in terms of the graph."""

from __future__ import annotations

from conftest import CANONICAL, LINEAR_FINITE, ONT, key, result

import infer


def run(settings: dict, results: list[dict]) -> dict:
    """Inferred bounds keyed by (source result, target setting)."""
    out, _ = infer.infer({k: {"key": v} for k, v in settings.items()}, results, ONT, CANONICAL)
    return {(x["from_result"], x["setting_id"]): x for x in out}


def test_directions():
    """Upper: general -> special only; lower: special -> general only (a swapped rule would send
    adversarial sqrt(KT) upper bounds nowhere and stochastic log T upper bounds to adversarial)."""
    S = {"sto": key(), "adv": key(environment="adversarial_oblivious")}
    R = [result("adv:u", "adv", "upper", "sqrt(K*T*log(K))"), result("sto:u", "sto", "upper", "K*log(T)/Delta",
                                                                      dependence="instance_dependent"),
         result("sto:l", "sto", "lower", "sqrt(K*T)"), result("adv:l", "adv", "lower", "sqrt(K*T)")]
    got = run(S, R)
    assert ("adv:u", "sto") in got and ("sto:l", "adv") in got
    assert ("sto:u", "adv") not in got and ("adv:l", "sto") not in got
    assert got[("adv:u", "sto")]["rule"] == "upper_bound_to_special_case"


def test_reduction_maps_symbols_both_ways():
    """Linear (finite actions) d*sqrt(T) upper -> K-armed K*sqrt(T); K-armed sqrt(K*T) lower ->
    linear sqrt(d*T). Forgetting either map leaves a foreign symbol and an unprofilable bound;
    mapping the wrong way would give sqrt(K*T) in a setting with no K."""
    S = {"k": key(), "lin": key(**LINEAR_FINITE)}
    R = [result("lin:u", "lin", "upper", "d*sqrt(T)*log(T)"), result("k:l", "k", "lower", "sqrt(K*T)")]
    got = run(S, R)
    assert got[("lin:u", "k")]["expression"].replace(" ", "") in ("K*sqrt(T)*log(T)",)
    assert got[("k:l", "lin")]["expression"].replace(" ", "") == "sqrt(T*d)"


def test_instance_dependent_lower_bound_not_through_reduction():
    """Per-arm (gap-dependent) lower bounds hold only on the embedded instances: they must not cross
    the K-armed -> linear reduction (a Lai-Robbins sum over K arms is not a linear-bandit rate)."""
    S = {"k": key(), "lin": key(**LINEAR_FINITE)}
    R = [result("k:l", "k", "lower", "sum_subopt(log(T)/Delta_i)", dependence="instance_dependent")]
    assert ("k:l", "lin") not in run(S, R)


def test_lower_bound_for_learner_with_class_knowledge_not_instance_knowledge():
    """A minimax lower bound over the class holds for a learner that knows sigma (class-level), but
    not for one that knows the gap Delta_min (instance-level): knowing the gap can beat it."""
    S = {"plain": key(noise="subgaussian"), "sig": key(noise="subgaussian", learner_knows=["sigma"]),
         "gap": key(noise="subgaussian", learner_knows=["Delta_min"])}
    R = [result("plain:l", "plain", "lower", "sqrt(K*T)")]
    got = run(S, R)
    assert ("plain:l", "sig") in got
    assert any("class-level" in c for c in got[("plain:l", "sig")]["caveats"])
    assert ("plain:l", "gap") not in got


def test_fixed_parameter_lower_bound_flagged():
    """A lower bound proved for K = 2 reaches general K only with 'holds for K = 2 only' (compare.py
    then keeps it out of the rate): unflagged, it would claim a K-free general-K lower bound."""
    S = {"two": key(parameters={"K": 2}), "any": key()}
    R = [result("two:l", "two", "lower", "sqrt(T)")]
    x = run(S, R)[("two:l", "any")]
    assert any(c.startswith("holds for K = 2 only") for c in x["caveats"])


def test_upper_bound_substitutes_fixed_parameter():
    """An upper bound for general K sent to K = 2 has K substituted."""
    S = {"two": key(parameters={"K": 2}), "any": key()}
    x = run(S, [result("any:u", "any", "upper", "sqrt(K*T)")])[("any:u", "two")]
    assert "K" not in x["expression"] and x["substitutions"] == {"K": "2"}


def test_regime_blocks_transfer():
    """regime_survives: a bound stated for C > R does not survive C = 0, and an unrelated regime does."""
    assert infer.regime_survives("C > R", {"C": 0}) is False
    assert infer.regime_survives("T >= K", {"d": "K"}) is True
    assert infer.regime_survives("T large enough", {"T": 5}) is None


def test_bayesian_lower_becomes_worst_case():
    """A Bayesian-regret lower bound sent to a setting without a prior is a worst-case bound
    (sup >= average); it must not stay 'bayesian_regret' there."""
    S = {"sto": key(), "adv": key(environment="adversarial_oblivious")}
    x = run(S, [result("sto:b", "sto", "lower", "sqrt(K*T)", quantity="bayesian_regret")])[("sto:b", "adv")]
    assert x["quantity"] == "pseudo_regret" and x["dependence"] == "worst_case"


def test_graph_lower_bound_instantiated_only_if_stated_in_alpha():
    """Regression: graph lower bounds reach the bandit setting with alpha_G = K only when stated in
    terms of alpha_G; an Omega(T) bound for non-observable graphs is not about every graph."""
    adv = dict(environment="adversarial_oblivious")
    S = {"graph": key(**adv, feedback="graph_feedback",
                      feedback_graph={"self_loops": "all", "observability": "strongly_observable"}),
         "bandit": key(**adv)}
    # the lower bound moves special -> general; bandit ⊑ graph? no: graph ⊑ bandit, so a lower bound
    # on the graph setting (special) goes up to bandit (general)
    R = [result("g:a", "graph", "lower", "sqrt(alpha_G*T)"), result("g:t", "graph", "lower", "T")]
    got = run(S, R)
    assert got[("g:a", "bandit")]["expression"].replace(" ", "") == "sqrt(K*T)"
    assert ("g:t", "bandit") not in got


def test_quantity_other_never_transfers():
    S = {"sto": key(), "adv": key(environment="adversarial_oblivious")}
    assert not run(S, [result("adv:o", "adv", "upper", "K*T", quantity="other")])


def test_comparator_scope_of_adversarial_to_stochastic():
    """The adversarial -> stochastic edge is valid for regret against the best fixed action only; a
    dynamic-regret (switching comparator) upper bound must not take it."""
    S = {"sto": key(), "adv": key(environment="adversarial_oblivious")}
    R = [result("adv:d", "adv", "upper", "sqrt(K*T)", comparator="best_switching_sequence")]
    assert ("adv:d", "sto") not in run(S, R)


def test_lower_bound_in_K_reaches_compact_sets_only_at_K_equals_d():
    """Inference audit 2026-10-26: a finite-menu lower bound in K sent to compact action sets (no K) kept K free,
    and with K -> infinity it exceeded the d*sqrt(T) upper bound. With 'K <= d' it is read at K = d; without an
    admissible value it is dropped."""
    from conftest import LINEAR_BALL
    compact = {**LINEAR_BALL, "action_set": {"shape": "arbitrary_compact", "time_varying": "fixed"}}
    S = {"menu": key(**LINEAR_FINITE), "compact": key(**compact)}
    R = [result("m:l", "menu", "lower", "sqrt(d*T*log(K))", conditions=["2 <= K <= d"]),
         result("m:x", "menu", "lower", "sqrt(d*T*log(K))")]
    got = run(S, R)
    assert got[("m:l", "compact")]["expression"].replace(" ", "") == "sqrt(T*d*log(d))"
    assert ("m:x", "compact") not in got
