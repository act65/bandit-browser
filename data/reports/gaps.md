# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## adversarial · linear · bounded_pm1 · hypercube (`S-fb75c747`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(T)*d*sqrt(log(2))` (exact; bubeck2012minimax Theorem 5)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · K-armed · Gaussian · knows mu_star, reward_family, sigma · K=2 (`S-0270b476`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1·log^1 vs lower 1 (log_gap)
- K: upper 1 vs lower 0 (poly_gap)
- best upper: `sum_subopt(3*Delta_i + 36*log(17/Delta_i)/Delta_i)` (exact; inherited from garivier2019explore Theorem C.1)
- best lower: `1/(4*Delta_min)` (exact; inherited from bubeck2013bounded Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-b2c205dc`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; hazan2016volumetric Corollary 7.1)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-b2c205dc`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-5d997e6a`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-5d997e6a`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · convex body (`S-6c77a35a`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · convex body (`S-6c77a35a`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-a05d66aa`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-bc8ef677`, 1 papers): hp_regret, worst_case — **poly gap**
- K: upper 2 vs lower 0.5 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K**2*vartheta*sqrt(T*log(1/delta)) + K**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] (`S-642244ca`, 8 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] (`S-c66bccd4`, 4 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `4*sqrt(K*T*log(K)) + (2*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-4a7d7ef8`, 3 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-32605594`, 3 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · unit ball (`S-f4a1ec30`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012minimax Theorem 6); `3*sqrt(T*d*log(T))` (exact; bubeck2012survey Theorem (th:ball))
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-a0beb0bf`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `d*sqrt(T*log(n_act))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_alg*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## adversarial · K-armed · adversarial contexts · rewards in [0,1] (`S-700023b9`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; bubeck2012survey Theorem (th:context-simple))
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-65c1bf79`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(K*T*log(T)/delta)**3)` (O; chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · arbitrary compact (`S-f11b1a7e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · bayesian_prior · knows prior · nonconvex (`S-df737978`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-a1767845`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(T)*log(K*T))` (O; kong2023bestofthree Theorem (thm:thmregret))
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · knows sigma · finite (`S-59ffe186`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `d*sqrt(T*log(n_act))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_alg*log(T))` (Omega; li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · bayesian_prior · knows prior · arbitrary compact (`S-a55c554b`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · adversarial contexts · rewards in [0,1] (`S-865565c2`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:context-simple))
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-bc8ef677`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(K - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · finite (`S-c97adc71`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5)
- relies on inherited bounds: True

