# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## corrupted stochastic · K-armed · rewards in [0,1] · unique_optimal_arm (`S-0e1ac51c`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 2); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `C` (Omega; gupta2019corruption Section 5.1)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · bounded_pm1 · arms_span_Rd, unique_optimal_arm · finite (`S-2f7e7dff`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0·log^0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012survey Theorem 5.2)
- best lower: `C` (Omega; inherited from gupta2019corruption Section 5.1)
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · rewards in [0,1] · unique_optimal_arm (`S-96e4adce`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 2); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `C` (Omega; inherited from gupta2019corruption Section 5.1)
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows moment_bound · K=2, u_mom=1 (`S-046cb977`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(5*Delta_i + 8*(4/Delta_i)**(1/eps_m)*log(T))` (exact; inherited from bubeck2013heavy Theorem 1); `sum_subopt(5*Delta_i + 32*(12*v_mom/Delta_i)**(1/eps_m)*log(T))` (exact; inherited from bubeck2013heavy Theorem 3)
- best lower: `0.4*log(T)/Delta_min**(1/eps_m)` (liminf; bubeck2013heavy Theorem 2)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-7264b322`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)` (liminf; inherited from bubeck2012survey Theorem 2.2); `sum_subopt(1/Delta_i)*log(T)/2` (liminf; inherited from zimmert2021tsallisinf Appendix A (unnumbered))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] (`S-6123da72`, 9 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; bubeck2012survey Theorem 3.2); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; bubeck2012survey Theorem 3.2)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-acdb6735`, 3 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem 3.2); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem 3.2)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-a945275c`, 2 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(T)*log(K*T))` (O; kong2023bestofthree Theorem 1)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from garivier2019explore Theorem 6 (appendix), consequence); `sqrt(T*d)/20` (Omega; inherited from bubeck2012survey Theorem 3.4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · adversarial contexts · rewards in [0,1] (`S-fea93b33`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; bubeck2012survey Theorem 4.1)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from garivier2019explore Theorem 6 (appendix), consequence); `sqrt(K*T)/20` (Omega; inherited from bubeck2012survey Theorem 3.4); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-3048cfe8`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012survey Theorem 5.2)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from garivier2019explore Theorem 6 (appendix), consequence); `sqrt(T*d)/20` (Omega; inherited from bubeck2012survey Theorem 3.4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-b457bea9`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(K*T*log(T)/delta)**3)` (O; chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2); `Min(T, sqrt(T*d))/20` (exact; inherited from garivier2019explore Theorem 6 (appendix), consequence); `sqrt(T*d)/20` (Omega; inherited from bubeck2012survey Theorem 3.4)
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · arms_span_Rd · arbitrary compact (`S-bc618b70`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · subgaussian · time_varying_action_sets · knows sigma · finite · L_feat=1, S=1, sigma=1 (`S-41fd6c92`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `d*sqrt(T*log(n_act))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; li2019nearlyminimax Theorem 3); `d*sqrt(T*eps_alg*log(T))` (Omega; li2019nearlyminimax Theorem 4)
- relies on inherited bounds: True

## stochastic · linear · Gaussian · bayesian_prior · sphere · d=>=2 (`S-fb4f603e`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Proposition 3); `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Example (Linear Models, Section 7.2))
- best lower: `0.006*sqrt(T)*d` (exact; rusmevichientong2010linear Theorem 2.1)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · time_varying_action_sets · bayesian_prior · arbitrary compact (`S-fb82f905`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; russo2014posterior Proposition 3); `sqrt(T)*d*log(T)` (O; russo2014posterior Example (Linear Models, Section 7.2))
- best lower: `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1); `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-ebd2c4fd`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem 5.2)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from garivier2019explore Theorem 6 (appendix), consequence); `sqrt(K*T)/20` (Omega; inherited from bubeck2012survey Theorem 3.4); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · adversarial contexts · bernoulli (`S-98720fd6`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; inherited from bubeck2012survey Theorem 4.1)
- best lower: `sqrt(K*T)/20` (Omega; inherited from bubeck2012survey Theorem 3.4); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1)
- relies on inherited bounds: True

