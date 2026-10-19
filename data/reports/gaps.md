# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## adversarial (oblivious) · K-armed · rewards in [0,1] · K=2 (`S-6b2d1b44`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P)); `5*sqrt(T)/2 + 28*log(T) + 3*sqrt(2)/4 + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(2)*sqrt(T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `C` (Omega; inherited from gupta2019corruption Section 5.1 (A Lower bound))
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows moment_bound · K=2, u_mom=1 (`S-046cb977`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(5*Delta_i + 8*(4/Delta_i)**(1/eps_m)*log(T))` (exact; inherited from bubeck2013heavy Theorem 1); `sum_subopt(5*Delta_i + 32*(12*v_mom/Delta_i)**(1/eps_m)*log(T))` (exact; inherited from bubeck2013heavy Theorem 3)
- best lower: `0.4*log(T)/Delta_min**(1/eps_m)` (liminf; bubeck2013heavy Theorem 2)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · knows C · K=2 (`S-a664e052`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P)); `5*sqrt(T)/2 + 28*log(T) + 3*sqrt(2)/4 + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(2)*sqrt(T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `C` (Omega; gupta2019corruption Section 5.1 (A Lower bound))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] · K=2 (`S-5e72804b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P)); `5*sqrt(T)/2 + 28*log(T) + 3*sqrt(2)/4 + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(2)*sqrt(T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `C` (Omega; inherited from gupta2019corruption Section 5.1 (A Lower bound))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] (`S-6123da72`, 9 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] (`S-d7ebf661`, 4 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `4*sqrt(K*T*log(K)) + (2*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-acdb6735`, 3 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-7dbd870b`, 2 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-a945275c`, 2 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(T)*log(K*T))` (O; kong2023bestofthree Theorem (thm:thmregret))
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-9c1a3b69`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012survey Theorem (th:exp2john)); `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-b457bea9`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(K*T*log(T)/delta)**3)` (O; chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · arbitrary compact (`S-627ae3d0`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · bayesian_prior · knows reward_family · nonconvex (`S-b9f1e6cf`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · K-armed · Gaussian · knows mu_star, sigma · K=2, sigma=1 (`S-71037241`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0 vs lower 0 (tight)
- best upper: `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 2); `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 3); `Delta_min + log(Delta_min**2*T)/Delta_min` (O; inherited from jin2020detc Theorem 3)
- best lower: `Min(Delta_min*T/2, 2*Delta_min*log(2)/(Delta_min**2 + 2*log(4*T)/T))` (exact; garivier2019explore Theorem (th:LB-BPR))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · knows S, sigma · finite · L_feat=1, S=1, sigma=1 (`S-3a6823ff`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `d*sqrt(T*log(n_act))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_alg*log(T))` (Omega; li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · Gaussian · bayesian_prior · knows reward_family, sigma · sphere · sigma_std=1 (`S-94697c7a`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Proposition (prop:linear))
- best lower: `0.006*sqrt(T)*d` (exact; rusmevichientong2010linear Theorem 2.1)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · time_varying_action_sets · bayesian_prior · arbitrary compact (`S-fb82f905`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

