# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## other_pure_exploration · stochastic · K-armed · rewards in [0,1] (`S-dcec362a`, 4 papers): sample_complexity, worst_case — **poly gap**
- K: upper 2 vs lower 1 (poly_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K**2/epsilon**2` (O_tilde; inherited from bai2021sample Theorem 5)
- best lower: `K/epsilon**2` (Omega; inherited from li2023tight Lemma 4)
- relies on inherited bounds: True

## stochastic · K-armed · conditionally_subgaussian (`S-0fdbe7ba`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.75 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sigma*sqrt(K*T)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-f940b8b5`, 2 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-f940b8b5`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · bounded_pm1 (`S-bf5581cd`, 2 papers): hp_regret, worst_case — **poly gap**
- K: upper 2.5 vs lower 0.5 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K**3*vartheta*log(1/delta) + K**2*vartheta*sqrt(K*T*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-931a2431`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-3d6ed1f8`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-ac424177`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-008aa593`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] (`S-3bca81dd`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-d92bdbf2`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d` (O; ailon2013bandit Theorem 4)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## other_pure_exploration · stochastic · linear (finite actions) · subgaussian · finite (`S-0290f7b5`, 1 papers): sample_complexity, worst_case — **poly gap**
- d: upper 2 vs lower 1 (poly_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `d**2/epsilon**2` (O_tilde; bai2021sample Theorem 5)
- best lower: `d/epsilon**2` (Omega; bai2021sample Theorem 12); `d/epsilon**2` (Omega; inherited from li2023tight Lemma 4)
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · hypercube (`S-602b4890`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(T)*d*sqrt(log(2))` (exact; bubeck2012minimax Theorem 5)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · l1 ball (`S-73ea19d4`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-0051b7b0`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (limsup; inherited from baudry2023recipe Corollary 4); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · arbitrary compact (`S-b12c10a7`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:bandit_lower_linear), regret consequence)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · gap_bounded_below · knows Delta (`S-0f3a0af6`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `49*sqrt(K*T)` (exact; inherited from audibert2009moss Theorem 5); `K + 23*sqrt(K*T) - 1` (exact; inherited from garivier2018klucbswitch Theorem 1); `K + 44*sqrt(K*T) - 1` (exact; inherited from garivier2018klucbswitch Theorem 3)
- best lower: `Min(K/Delta, Delta*T)` (Omega; foster2021statistical Proposition (prop:bandit_gap_tabular), Eq. (eq:mab_gap))
- relies on inherited bounds: True

## stochastic · K-armed · Gaussian · knows mu_star, sigma · K=2 (`S-5feb16e3`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1·log^1 vs lower 1 (log_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0 vs lower 0 (tight)
- best upper: `sum_subopt(3*Delta_i + 36*log(17/Delta_i)/Delta_i)` (exact; inherited from garivier2019explore Theorem C.1)
- best lower: `Min(Delta_min*T/2, 2*Delta_min*log(2)/(Delta_min**2 + 2*log(4*T)/T))` (exact; garivier2019explore Theorem A.3)
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · full_information feedback · rewards in [0,1] · knows C, Delta (`S-a83ec7b7`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · rewards in [0,1] · knows C, Delta (`S-4ff3a80d`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `Min(sqrt(K*T), sqrt(C_sb*K/Delta) + K/Delta)` (Omega; ito2021optimal Theorem 6)
- relies on inherited bounds: True

## adversarial · K-armed · decoupled feedback · rewards in [0,1] (`S-fceb575a`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(K*T)` (O; jin2023improved Theorem 4)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · bernoulli · knows S · finite (`S-d369a55a`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (tight)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T)*d**(3/2)` (O; inherited from ailon2013bandit Theorem 1); `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d_eff)` (Omega; kock2026spectral Theorem 7)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · convex body (`S-50c79de8`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5·log^0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## other_pure_exploration · stochastic · K-armed · bernoulli (`S-a4e9a5e4`, 1 papers): sample_complexity, worst_case — **poly gap**
- K: upper 2 vs lower 1 (poly_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K**2/epsilon**2` (O_tilde; inherited from bai2021sample Theorem 5)
- best lower: `K/epsilon**2` (Omega; li2023tight Lemma 4)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · hypercube (`S-de893d80`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(3)*d*sqrt(T*log(T))/3 + 2` (exact; lvy2025self Theorem (thm:regret_scftpl_hypercube))
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · hypercube (`S-de893d80`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-ed5d97e9`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · K=2 (`S-6ae9fddd`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(3*Delta_i + 16*log(4/(Delta_i*delta))/Delta_i)` (exact; inherited from abbasi2011oful Theorem 6) [delta=1/T]
- best lower: `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6); `Min(LambertW(0.833333333333333*Delta_min**2*T)/(2*Delta_min), Delta_min*T/2)` (exact; inherited from garivier2019explore Theorem A.4); `log(Delta_min**2*T/2)/(4*Delta_min)` (exact; inherited from bubeck2013bounded Theorem 6)
- relies on inherited bounds: True

## other_pure_exploration · stochastic · K-armed · dueling feedback · general_model_class · unique_optimal_arm (`S-8552a515`, 1 papers): sample_complexity, worst_case — **poly gap**
- K: upper 1·log^1.16667 vs lower 1·log^1 (log_gap)
- epsilon: upper 2 vs lower 0 (poly_gap)
- best upper: `K*log(K)*log(log(K))**3/epsilon**2` (O; inherited from falahatgar2017maximum Corollary 14)
- best lower: `K*log(K)/log(m)` (Omega; ren2019sample Proposition (Proposition:HPC))
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · Gaussian · means_in_known_interval · knows alpha_G, reward_family, sigma (`S-d4a48bc7`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 0 (tight)
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 4); `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 1)
- best lower: `sigma*sqrt(T*alpha_G)/(8*sqrt(E))` (exact; wu2015online Remark 5)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · rewards in [0,1] · convex body (`S-e8f2ff3d`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · rewards in [0,1] · convex body (`S-e8f2ff3d`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5·log^0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · rewards in [0,1] · polytope (`S-2752d1c5`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · rewards in [0,1] · polytope (`S-2752d1c5`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5·log^0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-1c3b2b88`, 1 papers): hp_regret, worst_case — **poly gap**
- K: upper 2 vs lower 0.5 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K**2*vartheta*sqrt(T*log(1/delta)) + K**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-2385d0e3`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-2385d0e3`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2.5 vs lower 0.5 (poly_gap)
- best upper: `d**3*vartheta*log(1/delta) + d**2*vartheta*sqrt(T*d*log(1/delta))` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-80d1a45e`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-80d1a45e`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 2 vs lower 0.5 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · linear · rewards in [0,1] · arbitrary compact (`S-a530a961`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-029e9298`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-095e5b93`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · bounded_pm1 · knows alpha_G (`S-2563467b`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5·log^0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · bounded_pm1 · knows alpha_G (`S-fb1035f8`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5·log^0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-46c63d10`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · Gaussian · knows sigma · K=2 (`S-634ed2bf`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `C**2 + 2*sqrt(2)*C*log(T) + sqrt(2)*sqrt(T*log(2/delta))` (O_tilde; inherited from bogunovic2020stochastic Theorem 2) [delta=1/T]
- best lower: `log(T/139)/2` (exact; inherited from bubeck2013bounded Theorem 8)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-7f7e51bb`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (limsup; inherited from baudry2023recipe Corollary 4); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-5b549eb9`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (limsup; inherited from baudry2023recipe Corollary 4); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-2c4fc5d5`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (limsup; inherited from baudry2023recipe Corollary 4); `sum_subopt(Delta_i/kl_i)*log(T)` (limsup; inherited from garivier2011klucb Theorem 1)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · full_information feedback · rewards in [0,1] (`S-5b04976e`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · full_information feedback · bounded_pm1 · convex body (`S-b549b217`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0 (poly_gap)
- d: upper 2 vs lower 0·log^1 (poly_gap)
- best upper: `d**2*vartheta*sqrt(T*log(1/delta)) + d**2*vartheta*log(1/delta)` (O_tilde; inherited from lee2020biasnomore Theorem 3.1) [delta=1/T]
- best lower: `Min(sqrt(T*log(d)), sqrt(C_sb*log(d)/Delta) + log(d)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial · K-armed · full_information feedback · bounded_pm1 (`S-d50aade7`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial · K-armed · full_information feedback · rewards in [0,1] (`S-827d2f82`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · bounded_pm1 · gap_bounded_below (`S-92e39c08`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5·log^0.5 vs lower 1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `Min(K/Delta, Delta*T)` (Omega; inherited from foster2021statistical Proposition (prop:bandit_gap_tabular), Eq. (eq:mab_gap))
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · decoupled feedback · rewards in [0,1] (`S-05edf856`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(K*T)` (O; inherited from jin2023improved Theorem 4)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## adversarial_self_bounding · K-armed · full_information feedback · rewards in [0,1] (`S-71542444`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 1 (poly_gap)
- K: upper 0.5 vs lower 0·log^1 (poly_gap)
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `Min(sqrt(T*log(K)), sqrt(C_sb*log(K)/Delta) + log(K)/Delta)` (Omega; inherited from ito2021optimal Theorem 5)
- relies on inherited bounds: True

## other_pure_exploration · stochastic · K-armed · subgaussian (`S-89926bf4`, 1 papers): sample_complexity, worst_case — **poly gap**
- K: upper 2 vs lower 1 (poly_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K**2/epsilon**2` (O_tilde; inherited from bai2021sample Theorem 5)
- best lower: `K/epsilon**2` (Omega; inherited from li2023tight Lemma 4)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · Gaussian · means_in_known_interval · knows alpha_G, reward_family, sigma (`S-267351c7`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 0 (tight)
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 4); `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 1)
- best lower: `sigma*sqrt(T*alpha_G)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · Gaussian · means_in_known_interval · knows sigma (`S-ea721940`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 0 (tight)
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 4); `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 1)
- best lower: `sigma*sqrt(T*alpha_G)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · Gaussian · means_in_known_interval · knows sigma (`S-c8a31c22`, 1 papers): regret, worst_case — **poly gap**
- Delta: upper 0 vs lower 0 (tight)
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 4); `sqrt(K*T) + sum_subopt(Delta_i)` (O; inherited from jin2021mots Theorem 1)
- best lower: `sigma*sqrt(T*alpha_G)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · time_varying_action_sets · means_in_known_interval (`S-32db9420`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.75 vs lower 0.5 (poly_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sigma*sqrt(K*T)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-79bab957`, 10 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] (`S-f716f820`, 6 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `4*sqrt(K*T*log(K)) + (2*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-a56c4616`, 6 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp (`S-3fca3d75`, 5 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5·log^-0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; agarwal2014taming Theorem 2) [delta=1/T]; `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; dudik2011efficient Theorem 4) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `sqrt(K*T*log(N_exp)/log(K))` (Omega; inherited from agarwal2012contextual Theorem 5.1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-271b064a`, 4 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; mannor2011from Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · K=2 (`S-3ac7d199`, 3 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `49*sqrt(2)*sqrt(T)` (exact; inherited from audibert2009moss Theorem 5); `4*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from foster2021statistical Proposition (prop:posterior_mab), Eq. (eq:posterior_mab)); `23*sqrt(2)*sqrt(T) + 1` (exact; inherited from garivier2018klucbswitch Theorem 1)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows eps_m, moment_bound (`S-15d654c4`, 3 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K)*T**(1/(eps_m + 1))*log(K)**(eps_m/(eps_m + 1))` (O_tilde; inherited from tajdini2025improved Corollary 1)
- best lower: `0.01*K**(eps_m/(eps_m + 1))*T**(1/(eps_m + 1))` (exact; bubeck2013heavy Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian (`S-aa77d6a4`, 3 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(K/delta))` (O_tilde; inherited from bogunovic2020stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sigma*sqrt(K*T)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · K=2 (`S-8605788d`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · unit ball (`S-e471f293`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012minimax Theorem 6); `3*sqrt(T*d*log(T))` (exact; bubeck2012survey Theorem (th:ball))
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · adversarial contexts · rewards in [0,1] (`S-17e61c60`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; bubeck2012survey Theorem (th:context-simple)); `2.63*sqrt(K*M_ctx*T*log(K))` (exact; zhou2015survey Theorem 3.1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(K*T)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-1fb2c4ec`, 2 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `3*sqrt(K)/4 + 14*K*log(T) + sqrt(T)/2 + 2*sqrt(T*(K - 1)) + 15` (exact; inherited from masoudian2021improved Theorem 3); `4*sqrt(K*T) + 1` (exact; inherited from zimmert2021tsallisinf Theorem 1); `10*K*log(T) + 2*sqrt(K*T) + 16` (exact; inherited from zimmert2021tsallisinf Theorem 1)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · bounded_pm1 (`S-bf5581cd`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(K*T)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · expert_advice · knows N_exp (`S-9d79dacc`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5·log^-0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from agarwal2014taming Theorem 2) [delta=1/T]; `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; inherited from dudik2011efficient Theorem 4) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `sqrt(K*T*log(N_exp)/log(K))` (Omega; agarwal2012contextual Theorem 5.1)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · subgaussian · arms_span_Rd · finite (`S-a8b93b1e`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `C**2 + C*d**(3/2)*log(T) + sqrt(T*d*log(K/delta))` (O_tilde; bogunovic2020stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sigma*sqrt(T*d)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## simple_regret · stochastic · K-armed · rewards in [0,1] (`S-3fa94fee`, 1 papers): simple_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper -0.5 vs lower -0.5 (tight)
- best upper: `2*sqrt(K*log(K)/(K + T))` (exact; bubeck2008pure Corollary 3)
- best lower: `sqrt(K/T)/20` (exact; bubeck2008pure Remark (rk:origine))
- relies on inherited bounds: False

## stochastic · continuum_other · full_information feedback · bounded_pm1 (`S-a8a20803`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*log(T))*(2*sqrt(2) + 4)*(sqrt(2*E - 2) + 8) + 3` (exact; inherited from cesabianchi2024role Theorem 4)
- best lower: `sqrt(T)/2048` (exact; cesabianchi2024role Theorem 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-3e091fe6`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; inherited from jin2026nearly Corollary 18); `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Corollary 17); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2); `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] · fairness (`S-d5792589`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0·log^0.5 (tight)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*sqrt(T*log(K))/2 + sqrt(2)*sqrt(T*log(1/delta))/2` (exact; dai2022incentive Theorem (thm:regretexpweight)) [delta=1/T]; `sqrt(2)*sqrt(T*log(K)) + sqrt(2)*sqrt(T*log(1/delta))/2 + sqrt(2)*sqrt(log(K))/4` (exact; dai2022incentive Theorem (thm:nearoptimaldivergingT)) [delta=1/T]
- best lower: `sqrt(2)*sqrt(T*log(K))/2` (liminf; dai2022incentive Theorem (thm:lowerbd))
- relies on inherited bounds: False

## stochastic · linear · bounded_pm1 · bayesian_prior · knows prior · nonconvex (`S-220ed3c1`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## other_pure_exploration · stochastic · K-armed · dueling feedback · general_model_class (`S-87a90327`, 1 papers): sample_complexity, worst_case — **log gap**
- K: upper 1·log^1.16667 vs lower 1·log^1 (log_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K*log(K)*log(log(K))**3/epsilon**2` (O; falahatgar2017maximum Corollary 14)
- best lower: `K*log(K/delta)/epsilon**2` (Omega; falahatgar2017maximum Theorem 16)
- relies on inherited bounds: False

## stochastic · linear · bounded_pm1 · unit ball (`S-7696a1ff`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012survey Theorem (th:ball))
- best lower: `sqrt(T*d)` (Omega; foster2021statistical Proposition (prop:bandit_lower_linear), regret consequence); `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · bounded_pm1 · time_varying_action_sets · finite (`S-89b20099`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; jin2026nearly Corollary 18); `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Corollary 17); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sqrt(T*d)` (Omega; inherited from chu2011suplinucb Theorem 2)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-ed715bc2`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d*log(T)*log(K*T))` (O; kong2023bestofthree Theorem (thm:thmregret))
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(T*d)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · K=2 (`S-6ae9fddd`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `sqrt(T)` (O_tilde; pacchiano2020model Theorem 6.3)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · bayesian_prior · knows prior · arbitrary compact (`S-57b2aede`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## simple_regret · stochastic · linear (finite actions) · dueling feedback · bernoulli · batched · knows S · finite (`S-d35d23c1`, 1 papers): simple_regret, worst_case — **log gap**
- T: upper -0.5·log^0.5 vs lower -0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `30*sqrt(d/T)*(sqrt(d*log(d**(-1 + 1/d)*(4*T + 1)) + 2*log(1/delta)) + 1/sqrt(d))` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound)); `(30*d + 60)*sqrt(log(d**(-1 + 1/d)*(4*T + 1)))/sqrt(T) + 31/sqrt(T)` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound))
- best lower: `d*exp(-5)/(4*sqrt(T))` (exact; scheid2024optimal Theorem (theorem:lower_bound))
- relies on inherited bounds: False

## stochastic · linear (finite actions) · heavy_tailed · knows eps_m, moment_bound, reward_family · finite (`S-3acadb03`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0·log^0.5 (tight)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5·log^-0.5 (log_gap)
- best upper: `T**(1/(eps_m + 1))*sqrt(d)*log(K)**(eps_m/(eps_m + 1))` (O_tilde; inherited from tajdini2025improved Corollary 1)
- best lower: `T**(1/(eps_m + 1))*d**(eps_m/(eps_m + 1))*(log(K)/log(d))**(eps_m/(eps_m + 1))` (Omega; tajdini2025improved Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] (`S-56d98cb4`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · time_varying_action_sets (`S-5de067fa`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · adversarial contexts · rewards in [0,1] (`S-c8d14734`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:context-simple)); `2.63*sqrt(K*M_ctx*T*log(K))` (exact; inherited from zhou2015survey Theorem 3.1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(K*T)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-1c3b2b88`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(K*T*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(K*T*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `0.06*sqrt(K*T)` (exact; inherited from mannor2011from Theorem 4)
- relies on inherited bounds: True

## nonstationary_switching · linear · rewards in [0,1] (`S-588ba484`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012survey Theorem (th:ball)); `2*sqrt(3)*sqrt(T)*d*sqrt(log(2))` (exact; inherited from bubeck2012minimax Theorem 5)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · finite (`S-718ed54b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Corollary 17); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sigma*sqrt(T*d)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · stochastic contexts · subgaussian · finite (`S-a690e18e`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Corollary 17); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Proposition (prop:mab_lower), regret consequence); `sqrt(T*d)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax)); `sigma*sqrt(T*d)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · subgaussian · knows sigma (`S-3bd92399`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `C**2 + C*K**(3/2)*log(T) + sqrt(K*T*log(K/delta))` (O_tilde; inherited from bogunovic2020stochastic Theorem 2) [delta=1/T]
- best lower: `sigma*sqrt(K*T)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli (`S-ce0869da`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- best upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (O; inherited from jin2026nearly Corollary 18); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(K*T*log(1 + T/K))` (exact; inherited from jin2026nearly Corollary 17); `sqrt(K*T*log(K*T*log(T)/delta)**3)` (O; inherited from chu2011suplinucb Theorem 1) [delta=1/T]
- best lower: `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] · K=2 (`S-daac918b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `2*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3)); `sqrt(2)*sqrt(T)/sqrt(log(2)) + 5.15*sqrt(2)*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (Expected regret of Exp3.P))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · Gaussian · knows reward_family, sigma (`S-c001732c`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `C**2 + C*K**(3/2)*log(T) + sqrt(K*T*log(K/delta))` (O_tilde; inherited from bogunovic2020stochastic Theorem 2) [delta=1/T]
- best lower: `sigma*sqrt(K*T)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · K=2 (`S-4c2922a4`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^-1 (log_gap)
- best upper: `2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (O; inherited from jin2026nearly Corollary 18); `130*2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · K=2 (`S-26956d2c`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^-1 (log_gap)
- best upper: `2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (O; inherited from jin2026nearly Corollary 18); `130*2**(3/4)*sqrt(T*log(T/2 + 1))*log(4*T + 1)**(1/4)` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · stochastic contexts · subgaussian · knows sigma · finite (`S-8897dcb6`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.75 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Corollary 17); `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sigma*sqrt(T*d)/(8*sqrt(E))` (exact; inherited from wu2015online Remark 5)
- relies on inherited bounds: True

