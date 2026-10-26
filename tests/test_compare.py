"""Rate profiles and tightness (pipeline/compare.py).

Claims: profiles give the textbook exponents (derived by hand below, not from the code);
lower-order terms with large constants do not change a profile; instance-dependent sums use
the uniform-gap instance; asymptotic (lim inf) constants become log T rates but delta -> 0
limits do not; high-probability bounds yield a regret bound at delta = 1/T; cell status is
tight / log gap / poly gap / conflict by the best upper and lower fronts; bounds that do
not describe the setting's rate are kept out of it (instance- or algorithm-restricted,
small-T, model changes, fixed-parameter lower bounds), consistency classes excepted."""

from __future__ import annotations

import pytest
from conftest import CANONICAL, result

import compare

CAN = CANONICAL | {"Delta"}


def prof(expr: str, notation: str = "O") -> dict:
    p = compare.profile(compare.instance_expr(expr, notation), CAN)
    return {v: tuple(ab) for v, ab in p.items() if v != "_path"}


@pytest.mark.parametrize("expr, expected", [
    ("sqrt(K*T)", {"T": (0.5, 0), "K": (0.5, 0)}),
    ("sqrt(K*T*log(K))", {"T": (0.5, 0), "K": (0.5, 0.5)}),
    ("d*sqrt(T)*log(T)", {"T": (0.5, 1), "d": (1, 0)}),
    ("T**(2/3)*K**(1/3)*log(K)**(1/3)", {"T": (2 / 3, 0), "K": (1 / 3, 1 / 3)}),
    # 10^4 K^2 is lower order along T = K^4 (K^2 vs K^2.5); a profiler at moderate scales would see it
    ("10000*K**2 + sqrt(K*T)", {"T": (0.5, 0), "K": (0.5, 0)}),
    # uniform-gap instance: sum over K-1 suboptimal arms of log(T)/Delta
    ("sum_subopt(log(T)/Delta_i)", {"T": (0, 1), "K": (1, 0), "Delta": (1, 0)}),
    ("sqrt(d*T*log(T)) + d*log(T)**2", {"T": (0.5, 0.5), "d": (0.5, 0)}),
])
def test_profiles(expr, expected):
    assert prof(expr) == expected


def test_liminf_constant_is_log_T_rate():
    """'lim inf R_T / log T >= sum 1/KL' is stored as the constant; its rate is log T."""
    assert prof("sum_subopt(1/kl(mu_i, mu_star))", "liminf")["T"] == (0, 1)


def test_delta_limit_not_multiplied_by_log_T():
    """Fixed-confidence identification: 'lim E[tau]/log(1/delta) = T_star' is asymptotic in delta, not T;
    multiplying by log T would invent a T-dependence (the bug behind a BAI conflict, 2026-10-23)."""
    e = compare.instance_expr("T_star*log(1/delta)", "liminf")
    assert "T" not in {str(s) for s in e.free_symbols}


def test_opaque_or_foreign_symbols_not_profiled():
    assert compare.profile(compare.instance_expr("sqrt(T*zeta_paper)", "O"), CAN) is None


def cells(results: list[dict], inferred: list[dict] | None = None, **patches) -> dict:
    out = compare.compare({r["id"]: r for r in results}, inferred or [], CAN)
    return out["settings"].get("S", {})


def U(rid, expr, **kw):
    return result(f"p:{rid}", "S", "upper", expr, **kw)


def L(rid, expr, **kw):
    return result(f"p:{rid}", "S", "lower", expr, **kw)


@pytest.mark.parametrize("up, lo, status", [
    ("37*sqrt(K*T)", "sqrt(K*T)/20", "tight"),
    ("sqrt(K*T*log(K))", "sqrt(K*T)", "log_gap"),
    ("T**(2/3)*K**(1/3)", "sqrt(K*T)", "poly_gap"),
    ("sqrt(K*T)", "T**(2/3)", "conflict"),
])
def test_cell_status(up, lo, status):
    c = cells([U("u", up), L("l", lo)])["regret|worst_case"]
    assert c["status"] == status


def test_front_keeps_best_upper_only():
    """A dominated upper bound (extra log T) must not set the rate: tight, not log gap."""
    c = cells([U("u1", "sqrt(K*T*log(T))"), U("u2", "sqrt(K*T)"), L("l", "sqrt(K*T)")])["regret|worst_case"]
    assert c["status"] == "tight" and c["upper_front"] == ["p:u2"]


def test_high_probability_bound_gives_regret_at_delta_1_over_T():
    """A high-probability bound B(delta) yields expected regret B(1/T) + O(1): it enters the regret cell."""
    c = cells([U("u", "sqrt(K*T*log(1/delta))", quantity="high_probability_regret"),
               L("l", "sqrt(K*T)")])["regret|worst_case"]
    assert c["upper_front"] == ["p:u@delta=1/T"] and c["status"] == "log_gap"


def test_small_horizon_upper_bound_excluded():
    """An upper bound that holds only for T <= K^2 says nothing about the rate as T -> infinity."""
    c = cells([U("u", "sqrt(T)", conditions=["T <= K^2"]), L("l", "sqrt(K*T)")])
    assert "regret|worst_case" not in c or c["regret|worst_case"]["status"] == "no_upper"


def test_instance_restricted_upper_bound_excluded(monkeypatch):
    monkeypatch.setitem(compare.CONDITION_CLASSES, "all gaps equal", "instance_restriction")
    c = cells([U("u", "sqrt(T)", conditions=["all gaps equal"]), L("l", "sqrt(K*T)")])
    assert c.get("regret|worst_case", {}).get("status", "no_upper") == "no_upper"


def test_algorithm_restricted_lower_bound_excluded_but_consistency_kept(monkeypatch):
    """A lower bound for bounded-memory learners does not bound the setting's rate; a lower bound for
    consistent (uniformly good) learners does: it is the Lai-Robbins admissible class."""
    monkeypatch.setitem(compare.CONDITION_CLASSES, "learner stores at most M arms", "algorithm_restriction")
    monkeypatch.setitem(compare.CONDITION_CLASSES, "for consistent algorithms", "algorithm_restriction")
    c = cells([U("u", "sqrt(K*T)"), L("l", "T", conditions=["learner stores at most M arms"])])
    assert c["regret|worst_case"]["status"] == "no_lower"
    c = cells([U("u", "sqrt(K*T)"), L("l", "sqrt(K*T)", conditions=["for consistent algorithms"])])
    assert c["regret|worst_case"]["status"] == "tight"


def test_algorithm_specific_lower_bound_excluded():
    """A lower bound on UCB's regret is not a lower bound for the setting."""
    c = cells([U("u", "sqrt(K*T)"), L("l", "T", algorithm_class="specific_algorithm")])
    assert c["regret|worst_case"]["status"] == "no_lower"


def test_model_change_excluded_both_sides(monkeypatch):
    monkeypatch.setitem(compare.CONDITION_CLASSES, "quantum oracle access", "model_change")
    c = cells([U("u", "sqrt(K*T)"), L("l", "sqrt(K*T)"), U("q", "log(T)", conditions=["quantum oracle access"])])
    assert c["regret|worst_case"]["status"] == "tight" and "p:q" not in c["regret|worst_case"]["upper_front"]


def test_fixed_parameter_inherited_lower_bound_excluded():
    """An inherited lower bound proved for K = 2 only must not set a general-K rate."""
    src = result("q:l", "S2", "lower", "sqrt(T)")
    inh = {"id": "q:l>S", "setting_id": "S", "from_result": "q:l", "expression": "T**(2/3)",
           "caveats": ["holds for K = 2 only"], "rule": "lower_bound_to_generalisation"}
    c = compare.compare({"q:l": src, "p:u": U("u", "sqrt(K*T)")}, [inh], CAN)["settings"]["S"]
    assert c["regret|worst_case"]["status"] == "no_lower"


def test_instance_dependent_O_bound_without_gap_hides_constant():
    """An instance-dependent O(log T) bound that does not mention Delta hides a gap-dependent
    constant: its Delta exponent is unknown, not 0 (else it would 'beat' 1/Delta lower bounds)."""
    c = cells([U("u", "K*log(T)", dependence="instance_dependent"),
               L("l", "sum_subopt(log(T)/Delta_i)", dependence="instance_dependent")])
    pv = c["regret|instance_dependent"]["per_var"]
    assert "Delta" not in pv and pv["T"]["status"] == "tight"


def test_switching_comparator_is_its_own_family():
    """Inference audit 2026-10-26: a static-regret upper bound and a switching-regret lower bound in a
    switching setting were pooled in one 'regret' cell (false tight / conflict)."""
    c = cells([U("u", "sqrt(K*T)"), L("l", "sqrt(K*T*S_T)", comparator="best_switching_sequence")])
    assert c["regret|worst_case"]["status"] == "no_lower"
    assert c["switching_regret|worst_case"]["status"] == "no_upper"


def test_equal_rates_do_not_empty_the_front():
    """Regression (2026-10-26, present since the engine was written): sqrt(KT) and sqrt(KT) + sum Delta_i have the
    same rate but different profile dicts; non-strict dominance made each remove the other, leaving 49 cells
    (the core stochastic K-armed one among them) with no best upper bound."""
    c = cells([U("a", "sqrt(K*T)"), U("b", "sqrt(K*T) + sum_subopt(Delta_i)"), L("l", "sqrt(K*T)")])["regret|worst_case"]
    assert c["status"] == "tight" and set(c["upper_front"]) == {"p:a", "p:b"}
