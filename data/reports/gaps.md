# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## stochastic · K-armed · adversarial contexts · conditionally_subgaussian · knows S, sigma (`S-18e0a06d`, 2 papers): regret, worst_case — **poly gap**
- K: upper 1·log^0.5 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `K*sqrt(T*log(K))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · continuum_other · partial_monitoring feedback · {bounded} · rewards in [0,1] (`S-0e101ebf`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)` (O_tilde; jin2026tight Theorem 1)
- best lower: `sqrt(T)/32` (exact; weed2015online Lemma 2)
- relies on inherited bounds: False

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-1e748ff8`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-78ee1a6f`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-c4898137`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-87d5d366`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · knows vartheta · convex body (`S-4d5cecab`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp, function_class (`S-d6bb7e40`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; agarwal2014taming Theorem 2) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · permutahedron (`S-a2719807`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1.5 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d**(3/2)` (O; ailon2013bandit Theorem 1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · permutahedron (`S-70586456`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d` (O; ailon2013bandit Theorem 4)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · subgaussian · knows C, sigma · finite (`S-69d9d1e5`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.75 vs lower 0.5 (poly_gap)
- d: upper 0.5 vs lower 0.5 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; inherited from ding2021robust Remark 1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · hypercube (`S-602b4890`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(T)*d*sqrt(log(2))` (exact; bubeck2012minimax Theorem 5)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-80bc9063`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · general_model_class (`S-642138e9`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower -0.333333 (poly_gap)
- best upper: `sqrt(T*log(T))*(2*sqrt(2) + 4)*(sqrt(2*E - 2) + 8) + 3` (exact; cesabianchi2024role Theorem 4)
- best lower: `T**(2/3 - eps_alg)` (Omega; inherited from xu2022towards Theorem 7)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-fd2c947e`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.25 (poly_gap)
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 1 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; ding2021robust Remark 1)
- best lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-576993df`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.25 (poly_gap)
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 1 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; ding2021robust Remark 1)
- best lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp, context_distribution (`S-70f9e0be`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; dudik2011efficient Theorem 4) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp (`S-a29e9fb4`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · expert_advice · knows N_exp, context_distribution, function_class (`S-496d1f16`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]; `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; inherited from dudik2011efficient Theorem 4) [delta=1/T]; `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from agarwal2014taming Theorem 2) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; erez2024real Theorem 2)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-2385d0e3`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · structured_general · bernoulli · time_varying_action_sets · finite (`S-e64dd016`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.5 (poly_gap)
- T: upper 0.75·log^0.5 vs lower 0.5 (poly_gap)
- best upper: `T**(3/4)*sqrt(log(T))` (O; huang2024quantum Theorem 1)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · bounded_pm1 · time_varying_action_sets · finite (`S-0ab423a7`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.25 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; jin2026nearly Corollary 18)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bounded_pm1 · knows L_feat, S, sigma (`S-6cbbe972`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.75 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · knows d_eff, sigma · finite (`S-7e9d4915`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · knows S, sigma · finite (`S-eaaaaafd`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d**(3/2)*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]; `d*sqrt(T*log(K))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · hypercube (`S-ca7e2d63`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(3)*d*sqrt(T*log(T))/3 + 2` (exact; lvy2025self Theorem (thm:regret_scftpl_hypercube)); `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-2d3da471`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · K=2 (`S-f89b1b82`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(2/Delta_i)*log(T)` (limsup; inherited from jin2021mots Theorem 3)
- best lower: `4*log(T)/Delta_min` (liminf; inherited from garivier2016etc Theorem 4); `log(T)/Delta_min` (liminf; inherited from garivier2016etc Theorem 3); `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · {bounded} · bernoulli (`S-1870d1f6`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0·log^1 (poly_gap)
- best upper: `T**(2/3)` (O_tilde; inherited from jin2026tight Theorem 1)
- best lower: `log(T)` (Omega; weed2015online Theorem 3)
- relies on inherited bounds: True

## nonstationary_drifting · K-armed · rewards in [0,1] · knows Lambda_T, V_T (`S-f4898025`, 1 papers): dynamic_regret, data_dependent — **poly gap**
- K: upper 0.666667 vs lower 0 (poly_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `sqrt(K*T*V_T) + (K**2*Lambda_T*T*V_T)**(1/3)` (O_tilde; wei2017tracking Theorem 3.1)
- best lower: `sqrt(T*V_T) + (Lambda_T*T*V_T)**(1/3)` (Omega; wei2017tracking Theorem 4.3)
- relies on inherited bounds: False

## stochastic · continuum_other · partial_monitoring feedback · {unimodal} · general_model_class (`S-a957eb0d`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower -0.333333 (poly_gap)
- best upper: `sqrt(T*log(T))*(2*sqrt(2) + 4)*(sqrt(2*E - 2) + 8) + 3` (exact; inherited from cesabianchi2024role Theorem 4)
- best lower: `T**(2/3 - eps_alg)` (Omega; xu2022towards Theorem 7)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-e7825ea7`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · {bounded} · rewards in [0,1] (`S-4db9db5f`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0·log^1 (poly_gap)
- best upper: `T**(2/3)` (O_tilde; inherited from jin2026tight Theorem 1)
- best lower: `log(T)` (Omega; inherited from weed2015online Theorem 3)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-80d1a45e`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] (`S-86f54b23`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows C, sigma · finite (`S-90576d74`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.25 (poly_gap)
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 1 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; inherited from ding2021robust Remark 1)
- best lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows C, sigma · finite (`S-9bb2af03`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.25 (poly_gap)
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 1 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; inherited from ding2021robust Remark 1)
- best lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · conditionally_subgaussian · knows S, d_eff, sigma (`S-cd1e913b`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1·log^0.5 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `K*sqrt(T*log(K))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · conditionally_subgaussian · knows loss_range (`S-08243091`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(2)*sqrt(K*T*log(T)*Max(128*K*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-a8bd0c78`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-7477d51a`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-1f3f8126`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(2)*sqrt(T)*d` (exact; inherited from audibert2011minimax Theorem 12)
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-41449cf3`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(2)*sqrt(T)*d` (exact; inherited from audibert2011minimax Theorem 12)
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · finite (`S-70f62f23`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · knows L_feat, S, sigma · finite (`S-276b3658`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · subgaussian · knows L_feat, sigma · finite (`S-87eb7f98`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · subgaussian · knows S, sigma · finite (`S-ce9ba867`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · rewards in [0,1] · arbitrary compact (`S-dbe428ff`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · subgaussian · ellipsoid (`S-8eecdad2`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows S, sigma · unit ball (`S-914a4879`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows sigma · ellipsoid (`S-89411eb4`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · subgaussian · strongly convex (`S-fe3c6e35`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-79bab957`, 8 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] (`S-f716f820`, 5 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `4*sqrt(K*T*log(K)) + (2*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · K=2 (`S-8605788d`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-60f6f53d`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-c168a3ef`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*sqrt(E*T*d*log(E*d))` (exact; inherited from audibert2011minimax Theorem 16)
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · knows L_feat_sq, S, sigma (`S-57b28b5b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `4*sqrt(T*d*log(L_feat**2*T/d + lam))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat**2*T/(d*lam) + 1) + 2*log(1/delta)))` (exact; abbasi2011oful Theorem 13) [delta=1/T]; `4*sqrt(d*log(T/d)) + 4*sqrt(2)*sqrt(T*d*log(L_feat**2*T/d + lam))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat**2*T/(d*lam) + 1) + 2*log(1/delta)))` (exact; abbasi2011oful Theorem 14) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · knows S, sigma · arbitrary compact (`S-d41f9966`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows N_exp, context_distribution, function_class (`S-448da28f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · dueling feedback · rewards in [0,1] · convex body (`S-179848cd`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(T)**3)` (O; ailon2014reducing Corollary 3.2)
- best lower: `sqrt(T*d)` (Omega; inherited from gajane2015relative Theorem 2)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-b6b62510`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-d4798f10`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*sqrt(E*T*d*log(E*d))` (exact; audibert2011minimax Theorem 16)
- best lower: `0.05*sqrt(T*d)` (exact; audibert2011minimax Theorem 21)
- relies on inherited bounds: False

## stochastic · continuum_other · {bounded} · rewards in [0,1] · knapsack_constraints · knows B (`S-f8e3c06a`, 1 papers): regret, worst_case — **log gap**
- T: upper 0·log^0.666667 vs lower 0 (log_gap)
- best upper: `(B*log(T))**(2/3)` (O; babaioff2011dynamic Theorem 1.2)
- best lower: `B**(2/3)` (Omega; babaioff2011dynamic Theorem 6.1(a))
- relies on inherited bounds: False

## stochastic · linear · Gaussian · knows sigma · lp ball (`S-d3f10459`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(3)*sqrt(T)*d/48` (exact; banerjee2023minimax Theorem 1); `sqrt(T)*d` (Omega; inherited from bubeck2017sparsity Theorem 4)
- relies on inherited bounds: True

## simple_regret · stochastic · K-armed · rewards in [0,1] (`S-0128563c`, 1 papers): simple_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper -0.5 vs lower -0.5 (tight)
- best upper: `2*sqrt(K*log(K)/(K + T))` (exact; bubeck2008pure Corollary 3)
- best lower: `sqrt(K/T)/20` (exact; bubeck2008pure Remark (rk:origine))
- relies on inherited bounds: False

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-d30f3326`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012minimax Theorem 4)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · unit ball (`S-e471f293`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-ad3afe31`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; bubeck2012survey Theorem (th:context-simple))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-646fed35`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012survey Theorem (th:ball)); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · Gaussian · lp ball · p_norm=> 2 (`S-7c62f307`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d` (Omega; bubeck2017sparsity Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · delayed_feedback · knows D · N=1 (`S-7001015e`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `D + sqrt(T*(D + K)*log(K))` (O; cesabianchi2016delay Corollary (c:delayed))
- best lower: `sqrt(T*(D + K))` (Omega; cesabianchi2016delay Corollary (c:delayed))
- relies on inherited bounds: False

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-92b27f3b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; inherited from jin2026nearly Corollary 18); `sqrt(T*d*log(K*T*log(T)/delta)**3)` (O; chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2); `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · arbitrary compact (`S-f078e6d2`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1); `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1); `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-1447159b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K))` (O; dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## general_identification · stochastic · K-armed · dueling feedback · bernoulli (`S-fb1b31ee`, 1 papers): sample_complexity, worst_case — **log gap**
- K: upper 1·log^1.16667 vs lower 1·log^1 (log_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K*log(K)*log(log(K))**3/epsilon**2` (O; falahatgar2017maximum Corollary 14)
- best lower: `K*log(K/delta)/epsilon**2` (Omega; falahatgar2017maximum Theorem 16)
- relies on inherited bounds: False

## stochastic · linear · bounded_pm1 · unit ball (`S-d6a9cbee`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012survey Theorem (th:ball)); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear)); `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · gap_bounded_below · knows Delta_min (`S-121abc62`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `Min(K/Delta_min, Delta_min*T)` (Omega; foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_tabular))
- relies on inherited bounds: True

## stochastic · K-armed · dueling feedback · rewards in [0,1] (`S-00c2dc7b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(T)**3)` (O; inherited from ailon2014reducing Corollary 3.2)
- best lower: `sqrt(K*T)` (Omega; gajane2015relative Theorem 2)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · knows C · K=2 (`S-ac6095c1`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · bernoulli · knows d_eff · finite (`S-8dd7db57`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-b01170be`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*alpha_G*log(K))` (O; inherited from gennaro2025instance Section 4 (Strongly observable feedback graphs))
- best lower: `0.06*sqrt(T*alpha_G)` (exact; mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] · knows S_T (`S-239ed3e7`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-27f856f6`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-86b4f098`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `13*m*sqrt(T*d*(log(d/m) + 1)) + 9.49*m` (exact; neu2015first Theorem (unlabeled, adaptive FPL-TrIX))
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · full_information feedback · rewards in [0,1] · sleeping_arms, time_varying_action_sets · knows m · finite (`S-bb78d297`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(2)*m*sqrt(T*d*(log(d) + 1))` (exact; neu2026online Corollary 1)
- best lower: `sqrt(T*d)` (Omega; neu2026online Appendix D)
- relies on inherited bounds: False

## stochastic · K-armed · subgaussian · knows Delta_min (`S-3062cad4`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `sum_subopt(2/Delta_i)*log(T)` (limsup; inherited from jin2021mots Theorem 3)
- best lower: `Min(K/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_tabular))
- relies on inherited bounds: True

## stochastic · linear · Gaussian · knows sigma · sphere (`S-678a969e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `0.006*sqrt(T)*d` (exact; rusmevichientong2010linear Theorem 2.1); `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1)
- relies on inherited bounds: True

## simple_regret · stochastic · linear (finite actions) · dueling feedback · bernoulli · finite (`S-39964b81`, 1 papers): simple_regret, worst_case — **log gap**
- T: upper -0.5·log^0.5 vs lower -0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(d/T)*(20*eps_alg + 20)*(sqrt(lam) + sqrt(d*log(4*T/(d*lam**(1/d)) + lam**(1 - 1/d)) + 2*log(1/delta)))` (exact; scheid2024optimal Theorem (theorem:simple_regret_upper_bound)); `30*sqrt(d/T)*(sqrt(d*log(d**(-1 + 1/d)*(4*T + 1)) + 2*log(1/delta)) + 1/sqrt(d))` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound)); `(30*d + 60)*sqrt(log(d**(-1 + 1/d)*(4*T + 1)))/sqrt(T) + 31/sqrt(T)` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound))
- best lower: `d*exp(-5)/(4*sqrt(T))` (exact; scheid2024optimal Theorem (theorem:lower_bound))
- relies on inherited bounds: False

## stochastic · linear · subgaussian · convex body (`S-98bb5c5f`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*(d - 1)` (Omega; shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · hypercube (`S-435bc3c6`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*(d - 1)` (Omega; shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · continuum_other · semi_bandit feedback · {bounded,lipschitz} · rewards in [0,1] · knows L_lip · simplex (`S-a1471a3f`, 1 papers): regret, worst_case — **log gap**
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0.666667·log^0.333333 vs lower 0.666667 (log_gap)
- best upper: `K*T**(2/3)*log(T)**(1/3)` (O; tang2020bandit Theorem 4.2)
- best lower: `K*T**(2/3)` (Omega; tang2020bandit Theorem 6.1); `K*T**(2/3)` (Omega; tang2020bandit Theorem 6.1)
- relies on inherited bounds: False

## nonstationary_drifting · K-armed · full_information feedback · rewards in [0,1] (`S-9076fe31`, 1 papers): dynamic_regret, data_dependent — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `sqrt(T*V_T*log(K)) + (Lambda_T*T*V_T*log(K))**(1/3)` (O_tilde; wei2017tracking Theorem 3.5)
- best lower: `V_T + (Lambda_T*T*V_T)**(1/3)` (Omega; inherited from wei2017tracking Theorem 4.3)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · knows S_T (`S-acaa5b35`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-ad54edd0`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] · K=2 (`S-daac918b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-1c3b2b88`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · knows loss_range (`S-92c42c35`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-0ce959d9`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-3777668e`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · K-armed · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-08bbd034`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:context-simple))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · knows vartheta · finite (`S-6b8e9c55`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial_bounded_memory · K-armed · rewards in [0,1] (`S-1a96c540`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial_bounded_memory · K-armed · rewards in [0,1] · knows S_T (`S-f51983ee`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · K=2 (`S-9196292e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] · knows function_class (`S-b45210c0`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] · knows function_class (`S-4c531a0f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows M_ctx (`S-d8ffe5a0`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows function_class · K=2 (`S-0c1a5aaf`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^-1 (log_gap)
- best upper: `2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (O; inherited from jin2026nearly Corollary 18)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · K=2 (`S-b24676d6`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^-1 (log_gap)
- best upper: `2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (O; inherited from jin2026nearly Corollary 18)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx, context_distribution (`S-df6e3798`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp, context_distribution, function_class (`S-181d244f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows beta_holder (`S-e48bfa8f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-d7f713f3`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*sqrt(E*T*d*log(E*d))` (exact; inherited from audibert2011minimax Theorem 16)
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · subgaussian · time_varying_action_sets · knows n_act, sigma · finite (`S-51cb94de`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d**(3/2)*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]; `d*sqrt(T*log(K))*(sqrt(log(T)*log(1/delta)) + log(T))` (O; inherited from agrawal2013lints Theorem 1) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · rewards in [0,1] · finite (`S-202299c4`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows L_feat, sigma · arbitrary compact (`S-c7db52a2`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d` (Omega; inherited from bubeck2017sparsity Theorem 4); `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1); `sqrt(3)*sqrt(T)*d/48` (exact; inherited from banerjee2023minimax Theorem 1)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows S, sigma · arbitrary compact (`S-21ce1603`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

