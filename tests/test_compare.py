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
import sympy
from conftest import CANONICAL, result

import compare
import resolve

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


def test_side_condition_blocks_scan_of_the_bounded_variable():
    """Regression (batch 2): a lower bound stated for 2 <= K <= d (jin2026nearly) or under a coupling such as
    n_act = 2^(d/2) (li2019nearlyminimax) says nothing about K (resp. d) -> infinity with the other fixed; read as
    a rate it 'beat' sqrt(d T log K) upper bounds. The other variables keep their exponents."""
    c = cells([U("u", "sqrt(d*T*log(K))"), L("l", "K**(1/4)*sqrt(d*T)", conditions=["2 <= K <= d"])])
    cell = c["regret|worst_case"]
    assert cell["status"] != "conflict" and "K" not in cell["per_var"] and cell["per_var"]["d"]["status"] == "tight"
    c = cells([U("u", "sqrt(d*T*log(K))"), L("l", "d*sqrt(T)", conditions=["n_act = 2^(d/2)"])])
    assert c["regret|worst_case"]["status"] != "conflict"
    # the same bounds without the condition are a conflict: the condition, not the expression, decides
    assert cells([U("u", "sqrt(d*T*log(K))"), L("l", "K**(1/4)*sqrt(d*T)")])["regret|worst_case"]["status"] == "conflict"


def test_side_conditions_parsed_conservatively():
    can = CAN | {"m", "N_exp", "n_act"}
    assert compare.side_condition_unknowns(["2 <= K <= d"], can) == {"K"}
    assert compare.side_condition_unknowns(["d >= K"], can) == {"K"}
    assert compare.side_condition_unknowns(["m = d/2"], can) == {"d"}
    assert compare.side_condition_unknowns(["T >= d^2", "K >= 2", "n >= d", "losses in [0,1]"], can) == set()


def test_O_tilde_upper_hides_logs_not_rates():
    """O~(sqrt(alpha T)) against Omega(sqrt(T log K)) differs only in a log factor the O~ hides: a log gap, not a
    conflict (wen2025adversarial). A polynomial difference stays a conflict."""
    c = cells([U("u", "sqrt(T)", notation="O_tilde"), L("l", "sqrt(T*log(K))")])
    assert c["regret|worst_case"]["status"] == "log_gap"
    assert cells([U("u", "sqrt(T)", notation="O_tilde"), L("l", "T**(2/3)")])["regret|worst_case"]["status"] == "conflict"


def test_O_tilde_upper_cannot_make_a_cell_tight():
    """Regression (batch 2, pilot fact F06): O~(sqrt(KT log(1/delta))) at delta = 1/T matched an Omega(sqrt(KT))
    lower bound and the cell read 'tight', though the O~ hides log factors. A plain O bound with the same rate is tight."""
    assert cells([U("u", "sqrt(K*T)", notation="O_tilde"), L("l", "sqrt(K*T)")])["regret|worst_case"]["status"] == "log_gap"
    assert cells([U("u", "sqrt(K*T)"), L("l", "sqrt(K*T)")])["regret|worst_case"]["status"] == "tight"


def test_runaway_exponents_are_skipped_deterministically():
    """Exponents that grow with a scanned variable are refused up front (they used to hit a wall-clock
    timeout, which made the derived data depend on machine speed); bounded exponents still profile."""
    P = resolve.parse
    for expr in ["log(T)**(d + 1)", "2**d", "exp(-10*Delta**2*T/K)/4", "epsilon**(2 - d)",
                 "sqrt(T)*log(T)**(d + 1)", "K*exp((K - T)/(144*sigma**2))"]:
        assert compare.runaway_exponent(P(expr)), expr
    for expr in ["T**((d + 1)/(d + 2))", "sqrt(K*T*log(K))", "T**(K/(K + 1))*log(T)**(1/(K + 1))",
                 "Lambda_T**(nu_matern/(d + 2*nu_matern))*T**(d/(d + 2*nu_matern))", "d*sqrt(T)*log(T)**2"]:
        assert not compare.runaway_exponent(P(expr)), expr


def test_paper_symbols_held_fixed_substituted_or_blocked():
    """notes/comparability.md: instance constants are held fixed (and reported), aliases become their canonical
    variable, and anything that scales, sits in an exponent, or is unclassified blocks the profile."""
    P = resolve.parse
    can = {"T", "K", "d", "Delta", "delta"}
    cls = {"p|kappa": "instance_constant", "p|n_r": "alias:T", "p|C_1": "constant", "p|P_T": "scales",
           "p|d_z": "instance_constant"}
    e, held, cond = compare.hold_symbols(P("kappa*d*sqrt(T)"), "p", can, cls)
    assert held == ["kappa"] and cond == ["kappa"]
    e, held, cond = compare.hold_symbols(P("C_1*sqrt(K*n_r)"), "p", can, cls)
    assert e == P("sqrt(K*T)") * sympy.Symbol("C_1") and held == ["C_1"] and cond == []
    assert compare.hold_symbols(P("sqrt(T*P_T)"), "p", can, cls) is None          # grows with T
    assert compare.hold_symbols(P("T**((d_z + 1)/(d_z + 2))"), "p", can, cls) is None  # rate depends on its value
    assert compare.hold_symbols(P("sqrt(T*rho)"), "p", can, cls) is None          # unclassified
    assert compare.hold_symbols(P("sqrt(T*kappa)"), "q", can, cls) is None        # classes are per paper


def test_held_parameter_makes_the_cell_conditional(monkeypatch):
    """A cell whose best upper bound needs a held instance parameter is tight only 'up to instance parameters'."""
    monkeypatch.setattr(compare, "SYMBOL_CLASSES", {"pa|kappa": "instance_constant"})
    up = result("pa:r1", "S1", "upper", "kappa*d*sqrt(T)", quantity="expected_regret", dependence="worst_case")
    lo = result("pb:r1", "S1", "lower", "d*sqrt(T)", quantity="expected_regret", dependence="worst_case")
    out = compare.compare({r["id"]: r for r in (up, lo)}, [], CAN)
    cell = out["settings"]["S1"]["regret|worst_case"]
    assert cell["status"] == "tight" and cell["conditional"] == ["kappa"]


def test_lower_bounds_hold_only_numerical_constants():
    """A lower bound's free parameters are usually construction parameters chosen with T and K
    (carpentier2026revealing: min(T r, D r + T eps + sqrt(D T r))); holding them fixed overstates the rate."""
    P = resolve.parse
    cls = {"p|r": "instance_constant", "p|C_1": "constant"}
    assert compare.hold_symbols(P("Min(T*r, sqrt(T*r))"), "p", {"T"}, cls, side="lower") is None
    assert compare.hold_symbols(P("C_1*sqrt(T)"), "p", {"T"}, cls, side="lower")[1] == ["C_1"]
    assert compare.hold_symbols(P("Min(T*r, sqrt(T*r))"), "p", {"T"}, cls, side="upper")[1] == ["r"]


def test_held_parameter_cannot_stand_in_for_a_missing_variable(monkeypatch):
    """gong2023efficient: sigma*sqrt(K_star*T log T) with K_star <= K held fixed must not read as K-free and
    'beat' a sqrt(KT) lower bound; its K-exponent is unknown, so the cell is not a conflict in K."""
    monkeypatch.setattr(compare, "SYMBOL_CLASSES", {"pa|K_star": "instance_constant"})
    up = result("pa:r1", "S1", "upper", "sqrt(K_star*T*log(T))", quantity="expected_regret", notation="O")
    lo = result("pb:r1", "S1", "lower", "sqrt(K*T)", quantity="expected_regret")
    cell = compare.compare({r["id"]: r for r in (up, lo)}, [], CAN)["settings"]["S1"]["regret|worst_case"]
    assert cell["status"] != "conflict" and "K" not in cell["per_var"]


def test_held_parameters_cannot_create_a_conflict(monkeypatch):
    """skalse2026online: T^(2/3) with a held class size M (which may grow with d) against a T^((d+1)/(d+2))
    lower bound is not evidence of an error; the variable is left unresolved instead of a conflict."""
    monkeypatch.setattr(compare, "SYMBOL_CLASSES", {"pa|M_size": "instance_constant"})
    up = result("pa:r1", "S1", "upper", "T**(2/3)*sqrt(log(M_size))", quantity="expected_regret", notation="O")
    lo = result("pb:r1", "S1", "lower", "T**((d + 1)/(d + 2))", quantity="expected_regret")
    cell = compare.compare({r["id"]: r for r in (up, lo)}, [], CAN)["settings"]["S1"]["regret|worst_case"]
    assert cell["status"] != "conflict" and cell["per_var"]["T"]["status"] == "unresolved"


def test_log_log_factors_do_not_make_a_conflict():
    """chen2015optimal: (log(1/delta) + log log(1/Delta))/Delta^2 against log log(1/Delta)/Delta^2 is one rate."""
    up = result("pa:r1", "S1", "upper", "(log(1/delta) + log(log(1/Delta)))/Delta**2", quantity="sample_complexity",
                dependence="instance_dependent", notation="O")
    lo = result("pb:r1", "S1", "lower", "log(log(1/Delta))/Delta**2", quantity="sample_complexity",
                dependence="instance_dependent")
    cell = compare.compare({r["id"]: r for r in (up, lo)}, [], CAN)["settings"]["S1"]["sample_complexity|instance_dependent"]
    assert cell["status"] != "conflict"


def test_cell_is_not_conditional_when_an_ordinary_bound_reaches_the_rate(monkeypatch):
    monkeypatch.setattr(compare, "SYMBOL_CLASSES", {"pa|kappa": "instance_constant"})
    rs = [result("pa:r1", "S1", "upper", "kappa*sqrt(K*T)", quantity="expected_regret", notation="O"),
          result("pc:r1", "S1", "upper", "2*sqrt(K*T)", quantity="expected_regret", notation="O"),
          result("pb:r1", "S1", "lower", "sqrt(K*T)", quantity="expected_regret")]
    cell = compare.compare({r["id"]: r for r in rs}, [], CAN)["settings"]["S1"]["regret|worst_case"]
    assert cell["status"] == "tight" and cell["conditional"] == []


def test_adaptive_adversary_splits_pseudo_and_expected_regret():
    """Author correspondence (2026-11-11): against an adaptive adversary pseudo-regret <= expected regret and the two
    differ, so they get separate cells. Expected upper bounds and pseudo lower bounds count in both; a pseudo upper
    bound must not make the expected-regret cell tight, nor an expected lower bound the pseudo cell."""
    rs = [result("pa:r1", "SA", "upper", "sqrt(K*T)", quantity="pseudo_regret", notation="O"),
          result("pb:r1", "SA", "lower", "sqrt(K*T)", quantity="pseudo_regret"),
          result("pc:r1", "SA", "upper", "T**(2/3)", quantity="expected_regret", notation="O"),
          result("pd:r1", "SA", "lower", "T**(2/3)", quantity="expected_regret")]
    out = compare.compare({r["id"]: r for r in rs}, [], CAN, adaptive={"SA"})["settings"]["SA"]
    assert set(out) == {"pseudo_regret|worst_case", "expected_regret|worst_case"}
    ps, ex = out["pseudo_regret|worst_case"], out["expected_regret|worst_case"]
    assert ps["status"] == "tight" and "pa:r1" in ps["upper_front"] and "pd:r1" not in ps["lower_front"]
    assert ex["status"] == "tight" and "pc:r1" in ex["upper_front"] and "pa:r1" not in ex["upper_front"]
    assert ex["n_lower"] == 2 and "pb:r1" not in ex["lower_front"]  # counted, but dominated by T^(2/3)
    assert "pc:r1" in ps["upper_front"] or ps["n_upper"] == 2
    # without the split (oblivious / stochastic) they pool into one regret cell
    pooled = compare.compare({r["id"]: r for r in rs}, [], CAN)["settings"]["SA"]
    assert set(pooled) == {"regret|worst_case"}


def test_fixed_dimension_cells_compare_T_rates_over_a_grid():
    """Kernel / Lipschitz settings fix d (and nu): Matern T^((nu+d)/(2nu+d)) is a T-rate per (d, nu), not a runaway
    exponent in d. An extra log T is a log gap at every grid point; a d-dependent polynomial difference is a poly gap."""
    up = result("pa:r1", "SK", "upper", "T**((nu_matern + d)/(2*nu_matern + d))*log(T)", quantity="expected_regret", notation="O")
    lo = result("pb:r1", "SK", "lower", "T**((nu_matern + d)/(2*nu_matern + d))", quantity="expected_regret")
    cell = compare.compare({r["id"]: r for r in (up, lo)}, [], CAN, fixed_dim={"SK"})["settings"]["SK"]["regret|worst_case"]
    assert cell["status"] == "log_gap" and set(cell["per_var"]) == {"T"} and len(cell["per_var"]["T"]["grid"]) == 9
    up2 = result("pc:r1", "SK", "upper", "T**((nu_matern + 2*d)/(2*nu_matern + 2*d))", quantity="expected_regret", notation="O")
    cell = compare.compare({r["id"]: r for r in (up2, lo)}, [], CAN, fixed_dim={"SK"})["settings"]["SK"]["regret|worst_case"]
    assert cell["status"] == "poly_gap"


def test_squared_exponential_rates_profile_only_at_fixed_dimension():
    """sqrt(T) log^(d/2) T (squared exponential lower bound) has d in an exponent: a runaway exponent when d is
    scanned, a plain T-rate when d is fixed."""
    lo = result("pb:r1", "SK", "lower", "sqrt(T)*log(T)**(d/2)", quantity="expected_regret")
    up = result("pa:r1", "SK", "upper", "sqrt(T)*log(T)**(d/2 + 1)", quantity="expected_regret", notation="O")
    rs = {r["id"]: r for r in (up, lo)}
    assert compare.compare(rs, [], CAN)["profiles"]["pb:r1"] is None
    cell = compare.compare(rs, [], CAN, fixed_dim={"SK"})["settings"]["SK"]["regret|worst_case"]
    assert cell["status"] == "log_gap"


def test_condition_satisfied_by_the_setting_does_not_exclude_the_bound():
    """A polynomial-eigendecay upper bound is instance-restricted for 'any kernel', but a Matern kernel has polynomial
    eigendecay: in a Matern setting the bound counts (ontology kernel.family satisfies)."""
    import re
    up = result("pa:r1", "SM", "upper", "T**(3/4)", quantity="expected_regret", notation="O",
                conditions=["polynomial eigendecay with exponent beta_p > 1"])
    lo = result("pb:r1", "SM", "lower", "T**(3/4)", quantity="expected_regret")
    rs = {r["id"]: r for r in (up, lo)}
    assert compare.compare(rs, [], CAN)["settings"]["SM"]["regret|worst_case"]["status"] == "no_upper"
    sat = {"SM": [re.compile(r, re.I) for r in compare.schema.load_ontology()["node_parameters"]["kernel"]["fields"]
                  ["family"]["satisfies"]["matern"]]}
    assert compare.compare(rs, [], CAN, satisfied=sat)["settings"]["SM"]["regret|worst_case"]["status"] == "tight"
