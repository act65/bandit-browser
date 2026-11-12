# Candidate gaps

Settings whose best upper and lower bounds differ (polynomial gaps first). Rates are growth exponents per variable; K, d, 1/Δ in the regime T large. *Candidates only*: check for resolving papers outside the corpus before calling a gap open.

## stochastic · K-armed · rewards in [0,1] · K=2 (`S-a242a6a8`, 7 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `log(T)/Delta_min` (O; lee2025revisiting Corollary 5.4); `46*sum_subopt(Max(1, log(Delta_i**2*T/2))/Delta_i)` (exact; inherited from audibert2009moss Theorem 6); `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1)
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · knows reward_family (`S-d1559e2c`, 7 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/KL_i)*log(T)` (liminf; lai1985asymptotically Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; saux2024mathematics Theorem 1.6); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3)
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows eps_m, u_mom (`S-ec20e2bf`, 5 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 2·log^-1 vs lower 1 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(Delta_i + (u**(eps_m + 1)/Delta_i)**(1/eps_m)*(C_1*log(T*(Delta_i/u)**((eps_m + 1)/eps_m)/(C_1*K)) + C_2*K))` (exact; wei2020minimax Theorem 8)
- best lower: `(K - 1)*log(Delta**2*T/(K - 1))/(4*Delta)` (exact; inherited from lattimore2015ocucb Theorem 19); `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-80bc9063`, 4 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2)
- best lower: `log(T)` (Omega; caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class (`S-59004b20`, 4 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3); `sum_subopt(Delta_i/KL_i)*log(T)` (liminf; inherited from lai1985asymptotically Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from saux2024mathematics Theorem 1.6)
- relies on inherited bounds: True

## stochastic · K-armed · bernoulli · K=2 (`S-f67b3e86`, 4 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `46*sum_subopt(Max(1, log(Delta_i**2*T/2))/Delta_i)` (exact; inherited from audibert2009moss Theorem 6); `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2)
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · delayed_feedback (`S-abbce210`, 4 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; inherited from schlisselberg2026near Theorem E.7); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl(mu_i/R_max, mu_star/R_max))*log(T)` (liminf; inherited from romano2022multi Theorem 1); `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-b0f3ec08`, 4 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-b0f3ec08`, 4 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 4*sqrt(log(3/delta)) + 1) + T**(1/3)*(2*sqrt(log(M_size)*log(3/delta)) + sqrt(log(M_size)) + 4*log(3/delta)) + 2*sqrt(log(M_size))*log(3/delta)` (exact; inherited from skalse2026online Theorem 3)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-60f6f53d`, 4 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-60f6f53d`, 4 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-1e748ff8`, 4 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `37*sqrt(K*T*q)/(1 - 1/q)` (exact; inherited from audibert2009moss Theorem 4); `sqrt(K*T)` (O; inherited from chen2025geometric Proposition 4); `A_u*sqrt(K)*M/c_alg + C_1*sqrt(K*T) + C_2*log(T + 1)` (exact; inherited from lee2024follow Theorem 4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-1e748ff8`, 4 papers): expected_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T)` (O; inherited from lee2025revisiting Corollary 4.2); `sqrt(pi)*sqrt(K)/(2*m_lr) + sqrt(K*T)*(60*sqrt(pi)*m_lr + 5.7/m_lr) + (E**2 + 2*K/27)*log(T + 1)` (exact; inherited from lee2025revisiting Theorem 4.3)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, sigma · arbitrary compact (`S-ae7355e1`, 3 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0 (poly_gap)
- d: upper 1 vs lower 1 (poly_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(dist_h*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; cella2020meta Lemma 1); `sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T))*sqrt(T*d*log(L_feat*T/(d*lam) + 1))` (O; cella2020meta Corollary 1)
- best lower: `Min(d/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_linear))
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-0d130cfb`, 3 papers): regret, worst_case — **poly gap**
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 0.5 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; ding2021robust Remark 1)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp (`S-a29e9fb4`, 3 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## bai_fixed_confidence · stochastic · K-armed · exponential_family · unique_optimal_arm · knows reward_family (`S-9bc788a0`, 3 papers): sample_complexity, instance_dependent — **poly gap**
- Delta: upper 2 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- best upper: `T_star*alpha_exp*log(1/delta)` (limsup; garivier2016optimal Proposition 5.1); `T_star*alpha_exp*log(1/delta)` (limsup; garivier2016optimal Theorem 5.2)
- best lower: `log(1/delta)` (Omega; inherited from yang2024best Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · continuum_other · partial_monitoring feedback · {bounded} · rewards in [0,1] (`S-0e101ebf`, 3 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)` (O_tilde; jin2026tight Theorem 1)
- best lower: `sqrt(T)/32` (exact; weed2015online Lemma 2)
- relies on inherited bounds: False

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-ad54edd0`, 3 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-ad54edd0`, 3 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-bc858c15`, 3 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-bc858c15`, 3 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 4*sqrt(log(3/delta)) + 1) + T**(1/3)*(2*sqrt(log(M_size)*log(3/delta)) + sqrt(log(M_size)) + 4*log(3/delta)) + 2*sqrt(log(M_size))*log(3/delta)` (exact; inherited from skalse2026online Theorem 3)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## bai_fixed_confidence · stochastic · K-armed · bernoulli · differential_privacy · unique_optimal_arm · knows eps_dp, reward_family (`S-a2e65f92`, 2 papers): sample_complexity, instance_dependent — **poly gap**
- Delta: upper 2·log^0.039 vs lower 1 (poly_gap)
- K: upper 1 vs lower 1 (tight)
- best upper: `sum_subopt(log(log(Delta_i**(-2))/delta)/(Delta_i**2*eps_dp**2))*log(1/delta_dp)` (O; inherited from zheng2020locally Theorem 12)
- best lower: `(sum_subopt(1/Delta_i) + 1/Delta_min)*log(0.416666666666667/delta)/eps_dp` (exact; azize2024differentially Corollary 3)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · general_model_class (`S-642138e9`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower -0.333333 (poly_gap)
- best upper: `sqrt(T*log(T))*(2*sqrt(2) + 4)*(sqrt(2*E - 2) + 8) + 3` (exact; cesabianchi2024role Theorem 4)
- best lower: `T**(2/3 - eps_alg)` (Omega; inherited from xu2022towards Theorem 7)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-1f3f8126`, 2 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-23c54b8a`, 2 papers): expected_regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `1.2*sqrt(T)*m*log(5/delta) + sqrt(T)*(2*sqrt(2)*sqrt(log(5/delta)) + 1.2) + 3*m*sqrt(T*d*(log(d/m) + 1)) + 2*sqrt(d*log(5/delta))*(sqrt(m) + m*sqrt(log(d/m) + 1)) + sqrt(T*d*m)*(log(5*d/delta) + 2) + sqrt(2)*sqrt(T*m*log(5/delta))*(sqrt(log(d/m) + 1) + 1)` (exact; inherited from neu2015importance Theorem 2) [delta=1/T]
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows C, sigma · finite (`S-e4290e12`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; inherited from ding2021robust Remark 1); `C*d*sqrt(d*log(T)*log(T/delta)) + d*sqrt(T*d*log(T)*log(T/delta))` (O; xu2026corruption Section 4 (discussion after Theorem 4.1)) [delta=1/T]
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp, context_distribution (`S-70f9e0be`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; dudik2011efficient Theorem 4) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-a8bd0c78`, 2 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-89c3b8ec`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `C_univ*log(T)**3/d**2 + sqrt(5)*d*sqrt(T*log(T)) + 2` (exact; lvy2025self Theorem (thm:regret_scftpl_ball)); `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-1df05581`, 2 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · Gaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-90b13adb`, 2 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.9·log^0.6 vs lower 0.7 (poly_gap)
- best upper: `S*sqrt(T*T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern))) + sqrt(T*T**(d/(d + 2*nu_matern))*(T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern)) + log(1/delta))*log(T)**(2*nu_matern/(d + 2*nu_matern)))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*(sigma**2*log(1/delta))**(nu_matern/(d + 2*nu_matern))` (Omega; inherited from cai2020lower Theorem 2)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-e7825ea7`, 2 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `37*sqrt(K*T*q)/(1 - 1/q)` (exact; inherited from audibert2009moss Theorem 4); `sqrt(K*T)` (O; inherited from chen2025geometric Proposition 4); `A_u*sqrt(K)*M/c_alg + C_1*sqrt(K*T) + C_2*log(T + 1)` (exact; inherited from lee2024follow Theorem 4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-e7825ea7`, 2 papers): expected_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T)` (O; inherited from lee2025revisiting Corollary 4.2); `sqrt(pi)*sqrt(K)/(2*m_lr) + sqrt(K*T)*(60*sqrt(pi)*m_lr + 5.7/m_lr) + (E**2 + 2*K/27)*log(T + 1)` (exact; inherited from lee2025revisiting Theorem 4.3)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · knows moment_bound (`S-f1811d29`, 2 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3); `sum_subopt(Delta_i/KL_i)*log(T)` (liminf; inherited from lai1985asymptotically Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from saux2024mathematics Theorem 1.6)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows function_class (`S-0cca6cb1`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-c168a3ef`, 2 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-78ee1a6f`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `4*rng*sqrt(K*T) + 2*rng` (exact; inherited from hadiji2020adaptation Theorem 23); `sqrt(2)*sqrt(K*T)` (exact; inherited from lattimore2020mirror Section 8 (Finite-armed bandits), via Lemma 19); `9.2*sqrt(K*T)` (limsup; inherited from pogodin2019first Corollary 4.4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-87d5d366`, 2 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `4*rng*sqrt(K*T) + 2*rng` (exact; inherited from hadiji2020adaptation Theorem 23); `sqrt(2)*sqrt(K*T)` (exact; inherited from lattimore2020mirror Section 8 (Finite-armed bandits), via Lemma 19); `9.2*sqrt(K*T)` (limsup; inherited from pogodin2019first Corollary 4.4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · knows vartheta · convex body (`S-984af66e`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] · knows function_class (`S-b45210c0`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · bernoulli · delayed_feedback (`S-3af0c4f2`, 2 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; inherited from schlisselberg2026near Theorem E.7); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · unique_optimal_arm · knows reward_family (`S-cf0b25f0`, 2 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows M_ctx (`S-d8ffe5a0`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows M_ctx (`S-d8ffe5a0`, 2 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-ee98f302`, 2 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-ee98f302`, 2 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows N_exp, context_distribution, function_class (`S-448da28f`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp, function_class (`S-d6bb7e40`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; agarwal2014taming Theorem 2) [delta=1/T]; `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · continuum_other · {bounded} · rewards in [0,1] (`S-e21441c0`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.666667 (unresolved)
- d: upper 1 vs lower 0 (poly_gap)
- best upper: `M**(3/2)*sqrt(B_size*T*log(B_size))` (O; inherited from galgana2023learning Theorem (thm:decoupled exp - bandit feedback)); `M*sqrt(B_size*T*log(B_size))` (O; inherited from galgana2023learning Theorem (thm: OMD)); `sqrt(T)*Max(1, L_z)*Max(d, sqrt(d*m_z))/sqrt(m_0)` (O_tilde; inherited from jagadeesan2022regret Theorem 4)
- best lower: `T**(2/3)` (Omega; balseiro2018contextual Theorem (thm:reduction))
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows B · finite (`S-d26d8f4f`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows B · finite (`S-4b87fd50`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · subgaussian · knows C, sigma · finite (`S-69d9d1e5`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T)*d*(C + C_prime) + sqrt(T)*d` (O_tilde; inherited from ding2021robust Theorem 1); `sqrt(log(K/delta)) + (C*log(T) + sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5)
- best lower: `C*d` (Omega; bogunovic2020stochastic Theorem 3)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · adversarial contexts · rewards in [0,1] (`S-8bb51c3a`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.333333·log^0.333333 vs lower 0.5 (poly_gap)
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(K*S_max*log(K))**(1/3)*sqrt(log(N_Theta))` (O; bubeck2012survey Theorem (th:theta-regret))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · K=2 (`S-b24676d6`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows eps_m, u_mom · K=2 (`S-e09b3568`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(Delta_i + (u**(eps_m + 1)/Delta_i)**(1/eps_m)*(C_1*log(T*(Delta_i/u)**((eps_m + 1)/eps_m)/(2*C_1)) + 2*C_2))` (exact; inherited from wei2020minimax Theorem 8)
- best lower: `0.4*log(T)/Delta_min**(1/eps_m)` (liminf; bubeck2013heavy Theorem 2); `log(T)/Delta_min` (liminf; inherited from garivier2016etc Theorem 3); `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · {bounded} · Gaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-3dca91d3`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.9·log^0.6 vs lower 0.7 (poly_gap)
- best upper: `S*sqrt(T*T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern))) + sqrt(T*T**(d/(d + 2*nu_matern))*(T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern)) + log(1/delta))*log(T)**(2*nu_matern/(d + 2*nu_matern)))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*(sigma**2*log(1/delta))**(nu_matern/(d + 2*nu_matern))` (Omega; cai2020lower Theorem 2)
- relies on inherited bounds: True

## stochastic · continuum_other · full_information feedback · general_model_class (`S-e4d78851`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1.66667 vs lower 0 (poly_gap)
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `K**(5/3)*T**(2/3)` (O_tilde; inherited from potfer2025comparing Theorem (theorem : explore then commit guarantee)); `K**(5/3)*T**(2/3)` (O_tilde; inherited from potfer2025comparing Theorem (theorem : instance dependant bounds uniform))
- best lower: `sqrt(T)/2048` (exact; cesabianchi2024role Theorem 5)
- relies on inherited bounds: True

## stochastic · K-armed · bounded_pm1 · K=2 (`S-d334c58a`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(2/(Delta_i*rho))*log(T)` (limsup; inherited from jin2021mots Theorem 2); `sum_subopt(2/Delta_i)*log(T)` (limsup; inherited from jin2021mots Theorem 3)
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows C, sigma · finite (`S-63acd113`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 0.5 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; inherited from ding2021robust Remark 1)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## corrupted stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-d697f9ce`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.75 vs lower 0.5·log^0.5 (poly_gap)
- d: upper 0.5 vs lower 0.5 (poly_gap)
- best upper: `C*T**(1/4)*d**(3/2) + T**(3/4)*sqrt(d)*(C + 1)` (O_tilde; ding2021robust Remark 1)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · expert_advice · knows N_exp, context_distribution, function_class (`S-496d1f16`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `K*log(K*N_exp/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from dudik2011efficient Theorem 5) [delta=1/T]; `16*sqrt(2)*sqrt(K*T*log(4*N_exp*T**2/delta))` (exact; inherited from dudik2011efficient Theorem 4) [delta=1/T]; `K*log(N_exp*T/delta) + sqrt(K*T*log(N_exp*T/delta))` (O; inherited from agarwal2014taming Theorem 2) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · expert_advice (`S-69a36924`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `tau*sqrt(K*T*d_N)*log(K*T/delta)` (O; foster2019model Proposition 14) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · expert_advice (`S-005637fa`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `tau*sqrt(K*T*d_N)*log(K*T/delta)` (O; inherited from foster2019model Proposition 14) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## adversarial · combinatorial · stochastic contexts · rewards in [0,1] · knows loss_range, m · finite (`S-b2032872`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*m**2*log(1/eps_bid)**(1/3)/eps_bid + m**4*log(1/eps_bid)/eps_bid**3` (O; golrezaei2026learning Theorem 3.4)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; inherited from cohen2017tight Theorem 2)
- relies on inherited bounds: True

## adversarial_restricted · linear (finite actions) · adversarial contexts · subgaussian · time_varying_action_sets · knows sigma · finite (`S-776e799f`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1.5 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d**(3/2)*sqrt(log(T*d)*log(T/delta))*(sqrt(log(1/delta)) + sqrt(log(T/d + 1)))` (O; inherited from kim2019contextual Theorem 4.1) [delta=1/T]
- best lower: `sqrt(T*(d - 1))/504` (exact; inherited from eldowa2026leveraging Proposition (prop:one-point-tree-lb)); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 5); `sqrt(T*(d - 1))/504` (exact; inherited from gerchinovitz2016refined Corollary 4)
- relies on inherited bounds: True

## adversarial · K-armed · adversarial contexts · bounded_pm1 · K=2 (`S-77b2b815`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*n_mask**(1/3)` (O_tilde; guo2022regreta Remark 4.2)
- best lower: `sqrt(T)/sqrt(pi)` (liminf; inherited from kobzar2022based Corollary 5)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · stochastic contexts · rewards in [0,1] · knows M_ctx (`S-67825cef`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, sigma · arbitrary compact (`S-e7970f1c`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d*log(T)` (O; hanna2021solving Lemma 1)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · convex body (`S-1b352b67`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T))` (O; hazan2016volumetric Corollary 7.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-0e594fcb`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-bdaf50ab`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## adversarial · structured_general · bernoulli · time_varying_action_sets · finite (`S-e64dd016`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.75·log^0.5 vs lower 0.5 (poly_gap)
- best upper: `T**(3/4)*sqrt(log(T))` (O; huang2024quantum Theorem 1)
- best lower: `sqrt(T*d_eff)` (Omega; inherited from kock2026spectral Theorem 7)
- relies on inherited bounds: True

## stochastic · continuum_other · {bounded} · subgaussian · arbitrary compact (`S-0d3c6e2b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.666667 (unresolved)
- d: upper 1 vs lower 0 (poly_gap)
- best upper: `sqrt(T)*Max(1, L_z)*Max(d, sqrt(d*m_z))/sqrt(m_0)` (O_tilde; jagadeesan2022regret Theorem 4)
- best lower: `T**(2/3)` (Omega; inherited from balseiro2018contextual Theorem (thm:reduction))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bounded_pm1 · knows L_feat, S, sigma (`S-6cbbe972`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · finite (`S-aca5b344`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · knows d_eff, sigma · finite (`S-4b1460fd`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; inherited from pacchiano2020model Theorem 6.1); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · nonconvex (`S-ccab9dec`, 1 papers): pseudo_regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1.5 vs lower 1 (poly_gap)
- best upper: `d**(3/2)*sqrt(T*log(T))` (O; kotowski2019bandit Corollary 4)
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-2a75b2d1`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1); `sqrt(2)*q*sqrt(T*d*m/(q - 1))` (exact; inherited from audibert2012regret Theorem 4); `2*sqrt(2)*sqrt(T*d*m)` (exact; inherited from audibert2012regret Theorem 4)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-2a75b2d1`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m, reward_family · finite (`S-6c89bfe3`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `(d - m)*log(T)/(4*Delta)` (liminf; kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m, reward_family · finite (`S-6c89bfe3`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1); `sqrt(2)*q*sqrt(T*d*m/(q - 1))` (exact; inherited from audibert2012regret Theorem 4); `2*sqrt(2)*sqrt(T*d*m)` (exact; inherited from audibert2012regret Theorem 4)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-569f7f9d`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; kveton2014tight Proposition 1)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-50792c5b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)` (O; inherited from chen2025note Theorem 1); `sqrt(T*d*m)` (O; inherited from chen2026further Theorem 3); `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · structured_general · subgaussian · knows function_class, sigma · K=2 (`S-c4411246`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `log(T)` (O; lattimore2014bounded Theorem 10); `4*Delta_max*(alpha_ucb - 1)/(alpha_ucb - 2) + sum_arms(Delta_i) + sum_subopt(8*alpha_ucb*sigma**2*log(T)/Delta_i)` (exact; inherited from lattimore2014bounded Theorem 2)
- best lower: `1/(8*theta_0)` (exact; inherited from lattimore2014bounded Theorem 8)
- relies on inherited bounds: True

## stochastic · structured_general · subgaussian · knows function_class, sigma · K=2 (`S-c4411246`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(T)/sqrt(pi)` (liminf; inherited from kobzar2022based Corollary 5)
- relies on inherited bounds: True

## stochastic · structured_general · semi_bandit feedback · bernoulli (`S-976b856c`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0 vs lower 0.5 (poly_gap)
- T: upper 0.75·log^0.5 vs lower 0.5 (poly_gap)
- best upper: `T**(3/4)*sqrt(log(T))` (O; inherited from huang2024quantum Theorem 1)
- best lower: `sqrt(2)*sqrt(K*T)/32` (exact; lattimore2014optimal Theorem 12)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp, function_class (`S-b4cf3653`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-2d3da471`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m, reward_family · finite (`S-88bac412`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · unique_optimal_arm · knows loss_range, reward_family (`S-8cf76adb`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; ng2026single Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · stochastic contexts · conditionally_subgaussian · time_varying_action_sets (`S-1b611262`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- d: upper 0.5 vs lower 1 (poly_gap)
- best upper: `sqrt(T)*d + T*sqrt(d)*eps_star` (O_tilde; pacchiano2020model Theorem 6.1)
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · finite (`S-70f62f23`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; pacchiano2020model Theorem 6.1)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · K=2 (`S-f89b1b82`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(2/(Delta_i*rho))*log(T)` (limsup; inherited from jin2021mots Theorem 2); `sum_subopt(2/Delta_i)*log(T)` (limsup; inherited from jin2021mots Theorem 3)
- best lower: `log(T)/Delta_min` (liminf; inherited from garivier2016etc Theorem 3); `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6); `log(Delta_min**2*T/2)/(4*Delta_min)` (exact; inherited from bubeck2013bounded Theorem 6)
- relies on inherited bounds: True

## stochastic · continuum_other · general_model_class (`S-c91556ec`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1.66667 vs lower 0 (poly_gap)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `K**(5/3)*T**(2/3)` (O_tilde; potfer2025comparing Theorem (theorem : explore then commit guarantee)); `K**(5/3)*T**(2/3)` (O_tilde; potfer2025comparing Theorem (theorem : instance dependant bounds uniform))
- best lower: `T**(2/3)` (Omega; potfer2025comparing Theorem (thm : uniform price auction lower bound regret)); `T**(2/3)` (Omega; potfer2025comparing Lemma (lemma : lower bound first price)); `T**(2/3)` (Omega; potfer2025comparing Lemma (par : delta separated))
- relies on inherited bounds: False

## stochastic · continuum_other · general_model_class · knows N (`S-1ebc0a58`, 1 papers): regret, worst_case — **poly gap**
- K: upper 1.66667 vs lower 0 (poly_gap)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `K**(5/3)*T**(2/3)` (O_tilde; inherited from potfer2025comparing Theorem (theorem : explore then commit guarantee)); `K**(5/3)*T**(2/3)` (O_tilde; inherited from potfer2025comparing Theorem (theorem : instance dependant bounds uniform))
- best lower: `T**(2/3)` (Omega; inherited from potfer2025comparing Theorem (thm : uniform price auction lower bound regret)); `T**(2/3)` (Omega; inherited from potfer2025comparing Lemma (lemma : lower bound first price)); `T**(2/3)` (Omega; inherited from potfer2025comparing Lemma (par : delta separated))
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · adversarial contexts · bernoulli · time_varying_action_sets · knows beta_holder · finite (`S-537136ad`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.8·log^1 vs lower 0.5 (poly_gap)
- best upper: `4*B*M_es*N_cl**2*T**((2*beta_holder + 2)/(3*beta_holder + 2))*log(T)/c_min` (O; qu2021context Theorem 2)
- best lower: `sqrt(K*T*m*log(N_exp))` (Omega_tilde; inherited from qin2026optimal Theorem (thm:lower-bound-ccsb)); `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## stochastic · K-armed · bounded_pm1 · delayed_feedback (`S-09dfe509`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; schlisselberg2026near Theorem E.7); `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl(mu_i/R_max, mu_star/R_max))*log(T)` (liminf; inherited from romano2022multi Theorem 1); `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · adversarial contexts · rewards in [0,1] (`S-3f20d599`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 4*sqrt(log(3/delta)) + 1) + T**(1/3)*(2*sqrt(log(M_size)*log(3/delta)) + sqrt(log(M_size)) + 4*log(3/delta)) + 2*sqrt(log(M_size))*log(3/delta)` (exact; skalse2026online Theorem 3)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · full_information feedback · adversarial contexts · rewards in [0,1] · knows N_exp, m · finite (`S-2e54646b`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `(d_ctx*m)**(1/4)*sqrt(K*T*log(N_exp))` (O; syrgkanis2016efficient Theorem 2)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · full_information feedback · adversarial contexts · rewards in [0,1] · knows N_exp, m · finite (`S-2e54646b`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `(d_ctx*m)**(1/4)*sqrt(K*T*log(N_exp))` (O; syrgkanis2016efficient Theorem 2)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · adversarial contexts · rewards in [0,1] · knows N_exp, m · finite (`S-6fd0a200`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `d_ctx**(1/4)*m**(3/4)*sqrt(K*T*log(N_exp))` (O; syrgkanis2016efficient Theorem 3)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · adversarial contexts · rewards in [0,1] · knows N_exp, m · finite (`S-6fd0a200`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `d_ctx**(1/4)*m**(3/4)*sqrt(K*T*log(N_exp))` (O; syrgkanis2016efficient Theorem 3)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## general_identification · stochastic · K-armed · subgaussian · knows Delta_lower_bound, sigma (`S-efd72228`, 1 papers): sample_complexity, worst_case — **poly gap**
- Delta: upper 2 vs lower 0 (poly_gap)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `K + log(n_groups/delta)/theta_bal + sigma**2*(K*log(K/delta) + sqrt(d)*log(n_groups)/theta_bal + sqrt(K*d*n_groups*log(K/delta)))/Delta_sep**2 + sigma**2*(sqrt(d) + log(log(K/delta)))*log(n_groups/delta)/(Delta_sep**2*theta_bal)` (O; thuot2024active Theorem 4.1)
- best lower: `K*sigma**2*kl(1 - delta, delta/K)/Delta_sep**2` (exact; thuot2024active Lemma B.1)
- relies on inherited bounds: False

## stochastic · K-armed · bernoulli · delayed_feedback · unique_optimal_arm · knows reward_family (`S-963c6a67`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; inherited from schlisselberg2026near Theorem E.7); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## nonstationary_drifting · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, Lambda_T, S, V_T, sigma · arbitrary compact (`S-caca0c43`, 1 papers): regret, data_dependent — **poly gap**
- T: upper 0.8 vs lower 0.666667 (poly_gap)
- d: upper 0.8 vs lower 0.666667 (poly_gap)
- best upper: `Lambda_T**(2/5)*T**(2/5)*V_T**(1/5)*d**(4/5) + T**(7/10)*d**(2/5) + T**(2/3)*V_T**(1/3)*d**(2/3)` (O_tilde; inherited from wang2024variance Theorem 12)
- best lower: `sqrt(T*V_T) + Min(Lambda_T, Lambda_T**(1/3)*T**(1/3)*V_T**(1/3)*d**(2/3))` (Omega; inherited from wang2025variance Theorem 4.1)
- relies on inherited bounds: True

## nonstationary_drifting · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, sigma · arbitrary compact (`S-c62b8c30`, 1 papers): regret, data_dependent — **poly gap**
- T: upper 0.8 vs lower 0.666667 (poly_gap)
- d: upper 0.8 vs lower 0.666667 (poly_gap)
- best upper: `Lambda_T**(2/5)*T**(2/5)*V_T**(1/5)*d**(4/5) + T**(7/10)*d**(2/5) + T**(2/3)*V_T**(1/3)*d**(2/3)` (O_tilde; wang2024variance Theorem 12)
- best lower: `sqrt(T*V_T) + Min(Lambda_T, Lambda_T**(1/3)*T**(1/3)*V_T**(1/3)*d**(2/3))` (Omega; inherited from wang2025variance Theorem 4.1)
- relies on inherited bounds: True

## nonstationary_drifting · linear · adversarial contexts · bounded_pm1 · time_varying_action_sets · knows L_feat, Lambda_T, S, V_T (`S-5ddc39eb`, 1 papers): regret, data_dependent — **poly gap**
- T: upper 0.8 vs lower 0.666667 (poly_gap)
- d: upper 0.8 vs lower 0.666667 (poly_gap)
- best upper: `Lambda_T**(2/5)*T**(2/5)*V_T**(1/5)*d**(4/5) + T**(7/10)*d**(2/5) + T**(2/3)*V_T**(1/3)*d**(2/3)` (O_tilde; inherited from wang2025variance Theorem A.1)
- best lower: `sqrt(T*V_T) + Min(Lambda_T, Lambda_T**(1/3)*T**(1/3)*V_T**(1/3)*d**(2/3))` (Omega; inherited from wang2025variance Theorem 4.1)
- relies on inherited bounds: True

## nonstationary_drifting · linear · adversarial contexts · bounded_pm1 · time_varying_action_sets · knows L_feat, S (`S-64862731`, 1 papers): regret, data_dependent — **poly gap**
- T: upper 0.8 vs lower 0.666667 (poly_gap)
- d: upper 0.8 vs lower 0.666667 (poly_gap)
- best upper: `Lambda_T**(2/5)*T**(2/5)*V_T**(1/5)*d**(4/5) + T**(7/10)*d**(2/5) + T**(2/3)*V_T**(1/3)*d**(2/3)` (O_tilde; wang2025variance Theorem A.1)
- best lower: `sqrt(T*V_T) + Min(Lambda_T, Lambda_T**(1/3)*T**(1/3)*V_T**(1/3)*d**(2/3))` (Omega; inherited from wang2025variance Theorem 4.1)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · {bounded} · bernoulli (`S-1870d1f6`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5)
- best lower: `log(T)` (Omega; weed2015online Theorem 3)
- relies on inherited bounds: True

## nonstationary_drifting · K-armed · rewards in [0,1] · knows Lambda_T, V_T (`S-f4898025`, 1 papers): dynamic_regret, data_dependent — **poly gap**
- K: upper 0.666667 vs lower 0 (poly_gap)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `sqrt(K*T*V_T) + (K**2*Lambda_T*T*V_T)**(1/3)` (O_tilde; wei2017tracking Theorem 3.1)
- best lower: `sqrt(T*V_T) + (Lambda_T*T*V_T)**(1/3)` (Omega; wei2017tracking Theorem 4.3)
- relies on inherited bounds: False

## adversarial (adaptive) · K-armed · stochastic contexts · rewards in [0,1] · expert_advice · knows N_exp, function_class (`S-973e68b6`, 1 papers): expected_regret, worst_case — **poly gap**
- T: upper 0.8 vs lower 0.5 (poly_gap)
- best upper: `T**(4/5)*(K**(2/3)*log(N_exp)**(1/3) + K*sqrt(log(K)))` (O; wu2024oracle Theorem 18)
- best lower: `sqrt(K*T)/18` (exact; inherited from eldowa2023information Theorem 8)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · subgaussian · time_varying_action_sets · knows sigma (`S-b552b282`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^2.5 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1.5 vs lower 0.5 (poly_gap)
- best upper: `d*sigma*sqrt(T*d*log(T/(d*lam) + 1)**3)*log(1/delta)` (O; xu2022langevin Theorem 4.2) [delta=1/T]
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · {unimodal} · general_model_class (`S-a957eb0d`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower -0.333333 (poly_gap)
- best upper: `sqrt(T*log(T))*(2*sqrt(2) + 4)*(sqrt(2*E - 2) + 8) + 3` (exact; inherited from cesabianchi2024role Theorem 4)
- best lower: `T**(2/3 - eps_alg)` (Omega; xu2022towards Theorem 7)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-2188ec6f`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · adversarial contexts · bernoulli · time_varying_action_sets · knows beta_holder · finite (`S-1bda0bfe`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.923·log^1 vs lower 0.5 (poly_gap)
- d: upper 0.308 vs lower 0 (poly_gap)
- best upper: `T**((D_ctx + 2*beta_holder)/(D_ctx + 3*beta_holder))*log(T)` (O; yang2019edge Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-a06b480b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)` (O; inherited from chen2025note Theorem 1); `sqrt(T*d*m)` (O; inherited from chen2026further Theorem 3); `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-a8abc741`, 1 papers): expected_regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `1.2*sqrt(T)*m*log(5/delta) + sqrt(T)*(2*sqrt(2)*sqrt(log(5/delta)) + 1.2) + 3*m*sqrt(T*d*(log(d/m) + 1)) + 2*sqrt(d*log(5/delta))*(sqrt(m) + m*sqrt(log(d/m) + 1)) + sqrt(T*d*m)*(log(5*d/delta) + 2) + sqrt(2)*sqrt(T*m*log(5/delta))*(sqrt(log(d/m) + 1) + 1)` (exact; inherited from neu2015importance Theorem 2) [delta=1/T]
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## bai_fixed_confidence · stochastic · K-armed · rewards in [0,1] · differential_privacy · knows eps_dp (`S-50fc8218`, 1 papers): sample_complexity, instance_dependent — **poly gap**
- Delta: upper 2·log^0.039 vs lower 1 (poly_gap)
- K: upper 1 vs lower 1 (tight)
- best upper: `sum_subopt(log(log(Delta_i**(-2))/delta)/(Delta_i**2*eps_dp**2))*log(1/delta_dp)` (O; zheng2020locally Theorem 12)
- best lower: `(sum_subopt(1/Delta_i) + 1/Delta_min)*log(0.416666666666667/delta)/eps_dp` (exact; inherited from azize2024differentially Corollary 3)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-6ae1e172`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)` (O; inherited from chen2025note Theorem 1); `sqrt(T*d*m)` (O; inherited from chen2026further Theorem 3); `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · arms_span_Rd · arbitrary compact (`S-f9aedae9`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5·log^0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T/delta))` (O; zimmert2022return Theorem 5)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · arms_span_Rd · arbitrary compact (`S-f9aedae9`, 1 papers): pseudo_regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T/delta))` (O; zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear · bounded_pm1 · arms_span_Rd · arbitrary compact (`S-f9aedae9`, 1 papers): expected_regret, worst_case — **poly gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `d*sqrt(T*log(T/delta))` (O; zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-d28e0dff`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-d28e0dff`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-cacaa1b7`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-cacaa1b7`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · stochastic contexts · bounded_pm1 · knows context_distribution · finite (`S-8f7ee09c`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5·log^0.5 (poly_gap)
- best upper: `sqrt(T)*d*log(T/delta)` (O; inherited from krishnamurthy2018semiparametric Theorem 4)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · stochastic contexts · bounded_pm1 · knows context_distribution · finite (`S-8f7ee09c`, 1 papers): pseudo_regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d*log(T/delta)` (O; inherited from krishnamurthy2018semiparametric Theorem 4) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · stochastic contexts · bounded_pm1 · knows context_distribution · finite (`S-8f7ee09c`, 1 papers): expected_regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d*log(T/delta)` (O; inherited from krishnamurthy2018semiparametric Theorem 4) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · bernoulli · delayed_feedback · unique_optimal_arm (`S-5adf431f`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; inherited from schlisselberg2026near Theorem E.7); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · knows moment_bound, reward_family (`S-723856d3`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3); `sum_subopt(Delta_i/KL_i)*log(T)` (liminf; inherited from lai1985asymptotically Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from saux2024mathematics Theorem 1.6)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-25ba82d1`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-25ba82d1`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp (`S-dc7bb219`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp (`S-dc7bb219`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows L_lip, sigma (`S-8ac5f37b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows M_ctx, sigma (`S-074ca0e1`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-519b84f3`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · {bounded} · rewards in [0,1] (`S-4db9db5f`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5)
- best lower: `log(T)` (Omega; inherited from weed2015online Theorem 3)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · conditionally_subgaussian · knows sigma · finite (`S-12cb3421`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; inherited from pacchiano2020model Theorem 6.1); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows L_feat, S, sigma · arbitrary compact (`S-5a59da3d`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0 (poly_gap)
- d: upper 1 vs lower 1 (poly_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(dist_h*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Lemma 1); `sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T))*sqrt(T*d*log(L_feat*T/(d*lam) + 1))` (O; inherited from cella2020meta Corollary 1)
- best lower: `Min(d/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_linear))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · adversarial contexts · bernoulli · knows S_T (`S-5c024cf6`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.333333·log^0.333333 vs lower 0.5 (poly_gap)
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(K*S_max*log(K))**(1/3)*sqrt(log(N_Theta))` (O; inherited from bubeck2012survey Theorem (th:theta-regret))
- best lower: `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30); `sqrt(K*T)/20` (exact; inherited from bubeck2012survey Theorem (th:LBminimax))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · adversarial contexts · rewards in [0,1] · knows function_class (`S-962bae9f`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.333333·log^0.333333 vs lower 0.5 (poly_gap)
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(K*S_max*log(K))**(1/3)*sqrt(log(N_Theta))` (O; inherited from bubeck2012survey Theorem (th:theta-regret))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · full_information feedback · adversarial contexts · rewards in [0,1] · knows N_exp, S_T, m · finite (`S-1b65beee`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `(d_ctx*m)**(1/4)*sqrt(K*T*log(N_exp))` (O; inherited from syrgkanis2016efficient Theorem 2)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · full_information feedback · adversarial contexts · rewards in [0,1] · knows N_exp, S_T, m · finite (`S-1b65beee`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `(d_ctx*m)**(1/4)*sqrt(K*T*log(N_exp))` (O; inherited from syrgkanis2016efficient Theorem 2)
- best lower: `0.05*sqrt(T*d)` (exact; inherited from audibert2011minimax Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-e9a0a033`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-e9a0a033`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-814688f7`, 1 papers): pseudo_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-814688f7`, 1 papers): expected_regret, worst_case — **poly gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `d*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · adversarial contexts · rewards in [0,1] (`S-aedf65f5`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 4*sqrt(log(3/delta)) + 1) + T**(1/3)*(2*sqrt(log(M_size)*log(3/delta)) + sqrt(log(M_size)) + 4*log(3/delta)) + 2*sqrt(log(M_size))*log(3/delta)` (exact; inherited from skalse2026online Theorem 3)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-0e99e49f`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `4*rng*sqrt(K*T) + 2*rng` (exact; inherited from hadiji2020adaptation Theorem 23); `sqrt(2)*sqrt(K*T)` (exact; inherited from lattimore2020mirror Section 8 (Finite-armed bandits), via Lemma 19); `9.2*sqrt(K*T)` (limsup; inherited from pogodin2019first Corollary 4.4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · rewards in [0,1] · K=2 (`S-3c249a16`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(T)/sqrt(pi)` (liminf; inherited from kobzar2022based Corollary 5)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] (`S-86f54b23`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `37*sqrt(K*T*q)/(1 - 1/q)` (exact; inherited from audibert2009moss Theorem 4); `sqrt(K*T)` (O; inherited from chen2025geometric Proposition 4); `A_u*sqrt(K)*M/c_alg + C_1*sqrt(K*T) + C_2*log(T + 1)` (exact; inherited from lee2024follow Theorem 4)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial · combinatorial · stochastic contexts · rewards in [0,1] · knows context_distribution, loss_range, m · finite (`S-f0bb1a37`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*m**2*log(1/eps_bid)**(1/3)/eps_bid + m**4*log(1/eps_bid)/eps_bid**3` (O; inherited from golrezaei2026learning Theorem 3.4)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; inherited from cohen2017tight Theorem 2)
- relies on inherited bounds: True

## bai_fixed_confidence · stochastic · K-armed · bernoulli · differential_privacy · unique_optimal_arm · knows eps_dp, loss_range (`S-06a9eb44`, 1 papers): sample_complexity, instance_dependent — **poly gap**
- Delta: upper 2·log^0.039 vs lower 1 (poly_gap)
- K: upper 1 vs lower 1 (tight)
- best upper: `sum_subopt(log(log(Delta_i**(-2))/delta)/(Delta_i**2*eps_dp**2))*log(1/delta_dp)` (O; inherited from zheng2020locally Theorem 12)
- best lower: `(sum_subopt(1/Delta_i) + 1/Delta_min)*log(0.416666666666667/delta)/eps_dp` (exact; inherited from azize2024differentially Corollary 3)
- relies on inherited bounds: True

## bai_fixed_confidence · stochastic · K-armed · rewards in [0,1] · differential_privacy · unique_optimal_arm · knows eps_dp, loss_range (`S-908bfa19`, 1 papers): sample_complexity, instance_dependent — **poly gap**
- Delta: upper 2·log^0.039 vs lower 1 (poly_gap)
- K: upper 1 vs lower 1 (tight)
- best upper: `sum_subopt(log(log(Delta_i**(-2))/delta)/(Delta_i**2*eps_dp**2))*log(1/delta_dp)` (O; inherited from zheng2020locally Theorem 12)
- best lower: `(sum_subopt(1/Delta_i) + 1/Delta_min)*log(0.416666666666667/delta)/eps_dp` (exact; inherited from azize2024differentially Corollary 3)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] (`S-e4378ff8`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 2 vs lower 1 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((C*K*log(K*T/delta) + log(T))*log(K*T/delta)/Delta_i)` (O; inherited from lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · K=2 (`S-9196292e`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `sum_subopt((2*C*log(2*T/delta) + log(T))*log(2*T/delta)/Delta_i)` (O; inherited from lykouris2018corruption Theorem 3) [delta=1/T]
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## nonstationary_switching · K-armed · stochastic contexts · rewards in [0,1] (`S-20b74903`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## nonstationary_switching · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx, N_exp (`S-ca2c184b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] (`S-ef4d3b68`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-a7370b75`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · adversarial contexts · rewards in [0,1] · knows function_class (`S-4c531a0f`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · gaussian_unknown_variance · knows reward_family · K=2 (`S-3fb4c8ef`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(8*log(T) + 1 + pi**2/2)*sum_arms(Delta_i) + 256*sum_subopt(sigma_i**2/Delta_i)*log(T)` (exact; inherited from auer2002ucb1 Theorem 4)
- best lower: `log(T)/Delta_min` (liminf; inherited from garivier2016etc Theorem 3); `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6); `log(Delta_min**2*T/2)/(4*Delta_min)` (exact; inherited from bubeck2013bounded Theorem 6)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · knows loss_range, reward_family (`S-993a402f`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3); `sum_subopt(Delta_i/KL_i)*log(T)` (liminf; inherited from lai1985asymptotically Theorem 1); `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from saux2024mathematics Theorem 1.6)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · unique_optimal_arm (`S-623502ef`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3)
- relies on inherited bounds: True

## stochastic · K-armed · general_model_class · unique_optimal_arm · knows loss_range (`S-65d77fef`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 1 vs lower 0·log^1 (poly_gap)
- best upper: `Min(T*mu_star, D_star*mu_star + T*eps_star + sqrt(D_star*T*mu_star))` (O; inherited from carpentier2026revealing Theorem 2)
- best lower: `sum_subopt(Delta_i/Kinf_i)*log(T)` (liminf; inherited from ng2026single Theorem 3)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · adversarial contexts · rewards in [0,1] · knows alpha_G, function_class (`S-22486edc`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `Min(T**(2/3), sqrt(K*T), sqrt(M_ctx*T*alpha_G))` (Omega; inherited from han2020optimal Theorem 6); `sqrt(T*Min(K, M_ctx, T**(1/3)))` (Omega_tilde; inherited from han2020optimal Corollary 2)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · adversarial contexts · rewards in [0,1] · knows alpha_G, m (`S-84fa54fe`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `Min(T**(2/3), sqrt(K*T), sqrt(M_ctx*T*alpha_G))` (Omega; inherited from han2020optimal Theorem 6); `sqrt(T*Min(K, M_ctx, T**(1/3)))` (Omega_tilde; inherited from han2020optimal Corollary 2)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · rewards in [0,1] (`S-7477d51a`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 0 (poly_gap)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2)
- best lower: `log(T)` (Omega; inherited from caron2012leveraging Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · heavy_tailed · knows eps_m, reward_family, u_mom (`S-52ee6e4b`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 2·log^-1 vs lower 1 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `sum_subopt(Delta_i + (u**(eps_m + 1)/Delta_i)**(1/eps_m)*(C_1*log(T*(Delta_i/u)**((eps_m + 1)/eps_m)/(C_1*K)) + C_2*K))` (exact; inherited from wei2020minimax Theorem 8)
- best lower: `(K - 1)*log(Delta**2*T/(K - 1))/(4*Delta)` (exact; inherited from lattimore2015ocucb Theorem 19); `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · adversarial contexts · rewards in [0,1] (`S-afcc9af4`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · adversarial contexts · rewards in [0,1] (`S-9fd5d878`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · adversarial contexts · rewards in [0,1] · knows function_class (`S-bcb436e0`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · adversarial contexts · rewards in [0,1] · knows function_class (`S-fe4975b0`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · rewards in [0,1] (`S-de400ecb`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · stochastic contexts · rewards in [0,1] · knows function_class (`S-f80fead2`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · partial_monitoring feedback · stochastic contexts · rewards in [0,1] · knows function_class (`S-04777523`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · delayed_feedback (`S-bbb63764`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `Ed_max*sqrt(K)*log(T) + K**(3/2)*log(T)**2*log(log(K)) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:lossDependGeneral)); `Ed_max*log(T) + sqrt(T*n_dim*log(K*T))` (O; inherited from schlisselberg2026near Theorem E.7); `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl(mu_i/R_max, mu_star/R_max))*log(T)` (liminf; inherited from romano2022multi Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · delayed_feedback (`S-267cbdaf`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl(mu_i/R_max, mu_star/R_max))*log(T)` (liminf; inherited from romano2022multi Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · delayed_feedback (`S-3abda525`, 1 papers): regret, instance_dependent — **poly gap**
- K: upper 0.5 vs lower 1 (poly_gap)
- T: upper 0.5·log^0.5 vs lower 0·log^1 (poly_gap)
- best upper: `sigma_max*log(sigma_max) + sqrt(K*T*log(K*T))` (O; inherited from schlisselberg2026near Theorem (thm:loss-independent-adv-delay))
- best lower: `sum_subopt(Delta_i/kl(mu_i/R_max, mu_star/R_max))*log(T)` (liminf; inherited from romano2022multi Theorem 1); `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from vernade2017stochastic Theorem 4)
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · knows loss_range · K=2 (`S-362db0d5`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `46*sum_subopt(Max(1, log(Delta_i**2*T/2))/Delta_i)` (exact; inherited from audibert2009moss Theorem 6); `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2)
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows L_feat, c_mu, function_class, k_mu (`S-020d373c`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows L_feat, c_mu, function_class, k_mu (`S-020d373c`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows M_ctx, context_distribution · K=2 (`S-a915e412`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows function_class (`S-0717833c`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows function_class (`S-0717833c`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows function_class · K=2 (`S-0c1a5aaf`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 6); `1/eps_gap` (liminf; inherited from kobzar2022based Theorem 11)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-bc588add`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] (`S-bc588add`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows L_lip (`S-def9ef8a`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows L_lip (`S-def9ef8a`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx (`S-9660c97b`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx (`S-9660c97b`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx, context_distribution (`S-df6e3798`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows M_ctx, context_distribution (`S-df6e3798`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp, context_distribution, function_class (`S-181d244f`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows beta_holder (`S-e48bfa8f`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.666667 vs lower 0.5 (poly_gap)
- best upper: `T**(2/3)*(2*sqrt(log(M_size)) + 1)` (exact; inherited from skalse2026online Theorem 1)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows beta_holder (`S-e48bfa8f`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0·log^1 (poly_gap)
- best upper: `C_R*d_star*sqrt(T*log(Max(E, T/delta)))*(M_b + d_star*sqrt(B_mis*log(Max(E, 11*log(T/delta))))) + 2*M_b + 8*c_u*d_star*sqrt(B_mis*T)*log(11*M_b*log(T)/delta)` (exact; inherited from pacchiano2020regret Theorem A.6) [delta=1/T]
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · expert_advice (`S-55763298`, 1 papers): regret, worst_case — **poly gap**
- K: upper 0.5 vs lower 0 (poly_gap)
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `tau*sqrt(K*T*d_N)*log(K*T/delta)` (O; inherited from foster2019model Proposition 14) [delta=1/T]
- best lower: `Min(sqrt(K*T), N_exp + sqrt(T))` (Omega_tilde; inherited from erez2024real Theorem 2)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows L_lip, sigma · K=2 (`S-9dfb9cc5`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.917 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `T**((d + 1)/(d + 2))` (Omega; inherited from suk2023tracking Proposition 16)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows M_ctx, S, sigma (`S-95e575f3`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows function_class, s_sparse, sigma (`S-4da69653`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows function_class, sigma (`S-86bdc338`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · subgaussian · knows sigma (`S-b3688a12`, 1 papers): regret, worst_case — **poly gap**
- T: upper 1 vs lower 0.5 (poly_gap)
- best upper: `T*delta_mis + 2*T*eps_mis + 3*n_S + 2*sqrt(6)*sigma*sqrt(T*n_S*log(T))` (exact; inherited from hong2020latent Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-a191695d`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-c63aca53`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows N, reward_family · finite (`S-4f25b674`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-41449cf3`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `d*log(T)/(eps_gap*m)` (Omega; inherited from yang2021combinatorial Theorem 3); `d*log(T)/eps_gap` (Omega; inherited from yang2021combinatorial Theorem 3)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-1e292a9d`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · finite (`S-1e292a9d`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows S, m · finite (`S-2bf57b09`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1); `(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014matroid Theorem 4)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows loss_range, m · finite (`S-8b4db714`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)` (O; inherited from chen2025note Theorem 1); `sqrt(T*d*m)` (O; inherited from chen2026further Theorem 3); `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows loss_range, m · finite (`S-8b4db714`, 1 papers): regret, instance_dependent — **poly gap**
- Delta: upper 1 vs lower 1 (tight)
- K: upper 1 vs lower 0 (poly_gap)
- T: upper 0·log^1 vs lower 0·log^1 (tight)
- best upper: `Delta_max*m_arms*(1 + pi**2/3) + sum_arms(12*L_size**2*a_max**2*log(T)/Delta_i_min)` (exact; inherited from chen2013combinatorial Section 4.3)
- best lower: `d*log(T)/(eps_gap*m)` (Omega; inherited from yang2021combinatorial Theorem 3); `d*log(T)/eps_gap` (Omega; inherited from yang2021combinatorial Theorem 3)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-de996aa8`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0 (poly_gap)
- best upper: `sqrt(T*d*m)` (O; inherited from chen2025note Theorem 1); `sqrt(T*d*m)` (O; inherited from chen2026further Theorem 3); `sqrt(T*d*m)/gamma_alg` (O; inherited from zimmert2019beating Theorem 1)
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · continuum_other · {bounded} · rewards in [0,1] · arbitrary compact (`S-e4da2d05`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5 vs lower 0.666667 (unresolved)
- d: upper 1 vs lower 0 (poly_gap)
- best upper: `sqrt(T)*Max(1, L_z)*Max(d, sqrt(d*m_z))/sqrt(m_0)` (O_tilde; inherited from jagadeesan2022regret Theorem 4)
- best lower: `T**(2/3)` (Omega; inherited from balseiro2018contextual Theorem (thm:reduction))
- relies on inherited bounds: True

## stochastic · kernel_rkhs · conditionally_subgaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-3667d919`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.9·log^0.6 vs lower 0.7 (poly_gap)
- best upper: `S*sqrt(T*T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern))) + sqrt(T*T**(d/(d + 2*nu_matern))*(T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern)) + log(1/delta))*log(T)**(2*nu_matern/(d + 2*nu_matern)))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*(sigma**2*log(1/delta))**(nu_matern/(d + 2*nu_matern))` (Omega; inherited from cai2020lower Theorem 2)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · conditionally_subgaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-3667d919`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.9·log^0.6 vs lower 0.7 (poly_gap)
- best upper: `S*sqrt(T*T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern))) + sqrt(T*T**(d/(d + 2*nu_matern))*(T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern)) + log(1/delta))*log(T)**(2*nu_matern/(d + 2*nu_matern)))` (O; inherited from chowdhury2017kernelized Theorem 3) [delta=1/T]
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*sigma**(2*nu_matern/(d + 2*nu_matern))` (Omega; inherited from scarlett2017lower Theorem 2)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · {bounded} · Gaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-d135bcb9`, 1 papers): hp_regret, worst_case — **poly gap**
- T: upper 0.9·log^0.6 vs lower 0.7 (poly_gap)
- best upper: `S*sqrt(T*T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern))) + sqrt(T*T**(d/(d + 2*nu_matern))*(T**(d/(d + 2*nu_matern))*log(T)**(2*nu_matern/(d + 2*nu_matern)) + log(1/delta))*log(T)**(2*nu_matern/(d + 2*nu_matern)))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*(sigma**2*log(1/delta))**(nu_matern/(d + 2*nu_matern))` (Omega; inherited from cai2020lower Theorem 2)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · bounded_pm1 · knows function_class · unit ball (`S-1b2708ae`, 1 papers): regret, worst_case — **poly gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 0.5 (poly_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, loss_range, sigma · arbitrary compact (`S-75780635`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0 (poly_gap)
- d: upper 1 vs lower 1 (poly_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(dist_h*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Lemma 1); `sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T))*sqrt(T*d*log(L_feat*T/(d*lam) + 1))` (O; inherited from cella2020meta Corollary 1)
- best lower: `Min(d/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_linear))
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, sigma · arbitrary compact (`S-f028e884`, 1 papers): regret, instance_dependent — **poly gap**
- T: upper 0.5·log^1 vs lower 0 (poly_gap)
- d: upper 1 vs lower 1 (poly_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(dist_h*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Lemma 1); `sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T))*sqrt(T*d*log(L_feat*T/(d*lam) + 1))` (O; inherited from cella2020meta Corollary 1)
- best lower: `Min(d/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_linear))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] (`S-79bab957`, 23 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(1/delta))` (O_tilde; inherited from huang2024high Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] (`S-f716f820`, 9 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `4*sqrt(K*T*log(K)) + (2*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; neu2015explore Theorem 1); `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P))
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · switching_cost (`S-9d381d4e`, 5 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0.333333 (unresolved)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; koren2017multi Theorem 7)
- best lower: `K**(1/3)*T**(2/3)` (Omega_tilde; cheng2023understanding Proposition 1); `K**(1/3)*T**(2/3)` (Omega_tilde; dekel2013bandits Theorem 1)
- relies on inherited bounds: False

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-c4898137`, 4 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K + 4*sqrt(T*alpha_tilde*log(K))` (exact; rouyer2022near Theorem 2)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-a0fd89ed`, 4 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `T**(2/3)*(delta_bar*log(K))**(1/3)` (O; inherited from chen2021understanding Corollary 25); `T**(2/3)*(delta_G*log(K))**(1/3)` (O; inherited from dann2023blackbox Corollary 19)
- best lower: `T**(2/3)/8` (exact; alon2015online Theorem 11)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, sigma · arbitrary compact (`S-ae7355e1`, 3 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; cella2020meta Corollary 1); `sqrt(T)*d*log(T)` (O; inherited from hanna2021solving Lemma 1)
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Corollary 23)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · bayesian_prior · knows prior (`S-9f6992e6`, 3 papers): bayesian_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*T*log(K))/2` (exact; tianhui2024active Proposition 1); `sqrt(2)*sqrt(K*T*log(K))` (exact; zimmert2019connections Example 8)
- best lower: `sqrt(K*T)` (Omega; inherited from shufaro2024bits Proposition C.1)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · rewards in [0,1] (`S-b546bb0a`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)*log(T)` (O; achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; achddou2020efficient Theorem 5)
- best lower: `sqrt(T)/64` (liminf; inherited from achddou2021fast Theorem (th:lower_bound_gen))
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · bernoulli (`S-9ec6fc56`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5)
- best lower: `sqrt(T)/64` (liminf; achddou2021fast Theorem (th:lower_bound_gen))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · full_information feedback · rewards in [0,1] · delayed_feedback · knows D (`S-e0d7fbf8`, 2 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0·log^0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*(D + 1))` (O_tilde; baron2024stochastic Corollary 6)
- best lower: `sqrt(T*(D + 1)*log(K))` (Omega; ryabchenko2025capacity Theorem D.5)
- relies on inherited bounds: False

## adversarial (oblivious) · K-armed · rewards in [0,1] · delayed_feedback · knows D (`S-243361f8`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `28*sqrt(K*T*(D + 1))` (exact; cesabianchi2018nonstochastic Corollary 7); `2*sqrt(2)*sqrt(K*T*(D + 1))` (exact; cesabianchi2018nonstochastic Corollary 7)
- best lower: `sqrt(K*T*(D + 1))` (Omega_tilde; cesabianchi2018nonstochastic Theorem 10)
- relies on inherited bounds: False

## corrupted stochastic · K-armed · rewards in [0,1] (`S-d6a2a630`, 2 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `C + sum_subopt(log(T)*log(K*T)/Delta_i) + K*log(1/Delta_min)*log(K/Delta_min)/Delta_min` (O; hu2025near Theorem 1)
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · stochastic contexts · rewards in [0,1] (`S-074b010a`, 2 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(1/delta))` (O_tilde; huang2024high Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · knows loss_range (`S-92c42c35`, 2 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(1/delta))` (O_tilde; inherited from huang2024high Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · rewards in [0,1] · K=2 (`S-daac918b`, 2 papers): pseudo_regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `sqrt(K*T)` (O; lee2025revisiting Corollary 5.4); `37*sqrt(2)*sqrt(T*q)/(1 - 1/q)` (exact; inherited from audibert2009moss Theorem 4); `2*sqrt(T)*sqrt(log(2))` (exact; inherited from bubeck2012survey Theorem (th:Exp3))
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · Gaussian · knows S, gamma_T, kernel, sigma · hypercube (`S-33988b87`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^3 vs lower 0.5·log^0.5 (log_gap)
- best upper: `sqrt(T)*log(T)**(d/2 + 5/2)` (O; inherited from vakili2020information Section 4); `S*sqrt(T*log(T)**(d + 1)) + sqrt(T*(log(T)**(d + 1) + log(1/delta))*log(T)**(d + 1))` (O; inherited from chowdhury2017kernelized Theorem 3) [delta=1/T]
- best lower: `sqrt(T*sigma**2*log(S**2*T/sigma**2)**(d/2))` (Omega; scarlett2017lower Theorem 2)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · Gaussian · knows S, gamma_T, kernel, sigma · hypercube (`S-33988b87`, 2 papers): hp_regret, worst_case — **log gap**
- T: upper 0.5·log^3 vs lower 0.5·log^0.5 (log_gap)
- best upper: `S*sqrt(T*log(T)**(d + 1)) + sqrt(T*(log(T)**(d + 1) + log(1/delta))*log(T)**(d + 1))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `sqrt(T*sigma**2*log(1/delta)*log(S**2*T/(sigma**2*log(1/delta)))**(d/2))` (Omega; inherited from cai2020lower Theorem 2)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · Gaussian · knows S, gamma_T, kernel, nu_matern, sigma · hypercube (`S-90b13adb`, 2 papers): regret, worst_case — **log gap**
- T: upper 0.7·log^2.3 vs lower 0.7 (log_gap)
- best upper: `T**(d*(1 + (d + 2*nu_matern)/d)/(2*(d + 2*nu_matern)))*log(T)**(-d/(2*(d + 2*nu_matern)) + 5/2)` (O; inherited from vakili2020information Section 4)
- best lower: `S**(d/(d + 2*nu_matern))*T**((d + nu_matern)/(d + 2*nu_matern))*sigma**(2*nu_matern/(d + 2*nu_matern))` (Omega; scarlett2017lower Theorem 2)
- relies on inherited bounds: True

## stochastic · combinatorial · cascade feedback · bernoulli · knows m · finite (`S-2587004b`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T)` (O_tilde; vial2022minimax Theorem 2); `sqrt(K*T)` (O_tilde; vial2022minimax Theorem 2)
- best lower: `sqrt(K*T)` (Omega; inherited from vial2022minimax Theorem 1)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · knows C (`S-c0839ca7`, 2 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `C_bar*K + K + sqrt(K*T*log(K))` (O; xu2024robust Theorem 4.1); `C*K + K + sqrt(K*T*log(K))` (O; xu2026corruption Theorem 3.1); `sqrt(K*T*log(K))` (O; xu2026corruption Section 3 (discussion after Theorem 3.1))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · bounded_pm1 (`S-2ec98009`, 2 papers): pseudo_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · bounded_pm1 (`S-2ec98009`, 2 papers): expected_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(K/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-8be4d43a`, 2 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*log(K)*Min(alpha_tilde, alpha_G*log(K)))` (O; inherited from dann2023blackbox Corollary 15)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial_bounded_memory · K-armed · rewards in [0,1] (`S-1a96c540`, 2 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · knows L_feat_sq, S, sigma (`S-543d4078`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `4*sqrt(T*d*log(L_feat**2*T/d + lam))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat**2*T/(d*lam) + 1) + 2*log(1/delta)))` (exact; abbasi2011oful Theorem 13) [delta=1/T]; `4*sqrt(d*log(T/d)) + 4*sqrt(2)*sqrt(T*d*log(L_feat**2*T/d + lam))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat**2*T/(d*lam) + 1) + 2*log(1/delta)))` (exact; abbasi2011oful Theorem 14) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · subgaussian · knows s_sparse · finite · s_sparse=1 (`S-58325da1`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; inherited from pacchiano2020model Theorem 6.1); `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]; `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; abbasiyadkori2012online Section 4.3 (text))
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · knows S, sigma · arbitrary compact (`S-d41f9966`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · bernoulli · knows N_exp, context_distribution, function_class (`S-448da28f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(N_exp/delta))` (O_tilde; inherited from levy2026optimal Theorem 3.1) [delta=1/T]
- best lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-f887286f`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-b6b62510`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K + 4*sqrt(T*alpha_tilde*log(K))` (exact; inherited from rouyer2022near Theorem 2); `sqrt(T*log(K)*Min(alpha_tilde, alpha_G*log(K)))` (O; inherited from dann2023blackbox Corollary 15)
- best lower: `sqrt(T*alpha_G)` (Omega; alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-84718472`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667·log^-1 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `T**(2/3)*alpha_G**(1/3)/(16*log(T))` (exact; arora2019bandits Theorem I.3); `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
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

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows S, sigma · finite (`S-16324bff`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows S, function_class, sigma · arbitrary compact (`S-22d6e1e6`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(L_feat**2*T/(d*lam) + 1))*Max(1, sqrt(S**2*lam + d*sigma**2*log(L_feat**2*T/(d*lam) + 1) + 2*sigma**2*log(1/delta)))` (exact; baumgrtner2026gray Corollary 2) [delta=1/T]
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Corollary 23)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-6b6e9521`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; bubeck2012minimax Theorem 4)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial · linear · bounded_pm1 · unit ball (`S-8f8244d1`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-ad3afe31`, 1 papers): pseudo_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(K*M_ctx*T*log(K))` (exact; bubeck2012survey Theorem (th:context-simple))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-f8d98c81`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(N_K))` (exact; bubeck2012survey Theorem (th:exp2john)); `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-f8d98c81`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · linear · bounded_pm1 · unit ball (`S-555d47bc`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; bubeck2012survey Theorem (th:ball)); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · linear · Gaussian · lp ball · p_norm=> 2 (`S-ca857d51`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*d` (Omega; bubeck2017sparsity Theorem 4)
- relies on inherited bounds: True

## stochastic · kernel_rkhs · {bounded} · Gaussian · knows S, gamma_T, kernel, sigma · hypercube (`S-3d4816ee`, 1 papers): hp_regret, worst_case — **log gap**
- T: upper 0.5·log^3 vs lower 0.5·log^0.5 (log_gap)
- best upper: `S*sqrt(T*log(T)**(d + 1)) + sqrt(T*(log(T)**(d + 1) + log(1/delta))*log(T)**(d + 1))` (O; inherited from chowdhury2017kernelized Theorem 3)
- best lower: `sqrt(T*sigma**2*log(1/delta)*log(S**2*T/(sigma**2*log(1/delta)))**(d/2))` (Omega; cai2020lower Theorem 2)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-40d2342c`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667·log^-1 (log_gap)
- best upper: `T**(2/3)*(D_obs*log(K))**(1/3)` (exact; cesari2026action Theorem 3); `Min(T, 5*T**(2/3)*(gamma_dom*log(K))**(1/3))` (exact; cesari2026action Theorem 1)
- best lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · time_varying_action_sets · finite (`S-92b27f3b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; chu2011suplinucb Theorem 2)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · switching_cost · m_delay=2 (`S-c8d99044`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0.333333 (unresolved)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `K**(1/3)*T**(2/3)` (Omega_tilde; coa2025learning Theorem 4.6)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · rewards in [0,1] · knows loss_range, m · finite (`S-a5c063ba`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Theorem 6); `2*sqrt(2)*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + 2*m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Proposition 1)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; cohen2017tight Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · rewards in [0,1] · knows loss_range, m · finite (`S-5c41c340`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Theorem 6); `2*sqrt(2)*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + 2*m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Proposition 1)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; cohen2017tight Theorem 2)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · rewards in [0,1] · knows loss_range, m · finite (`S-9819a1ec`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Theorem 6); `2*sqrt(2)*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + 2*m**(5/2)*log(1/mu_min)/lambda_low` (exact; inherited from combes2015combinatorial Proposition 1)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; cohen2017tight Theorem 3)
- relies on inherited bounds: True

## adversarial (oblivious) · combinatorial · rewards in [0,1] · knows m · finite (`S-48a6e274`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + m**(5/2)*log(1/mu_min)/lambda_low` (exact; combes2015combinatorial Theorem 6); `2*sqrt(2)*sqrt(T*m**3*(d + sqrt(m)/lambda_low)*log(1/mu_min)) + 2*m**(5/2)*log(1/mu_min)/lambda_low` (exact; combes2015combinatorial Proposition 1)
- best lower: `m**(3/2)*sqrt(T*d)` (Omega_tilde; inherited from cohen2017tight Theorem 1); `m**(3/2)*sqrt(T*d)` (Omega_tilde; inherited from cohen2017tight Theorem 2); `m**(3/2)*sqrt(T*d)` (Omega_tilde; inherited from cohen2017tight Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · arbitrary compact (`S-f078e6d2`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · finite (`S-49d4614d`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K))` (O; dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · bounded_pm1 · knows alpha_G (`S-e7e84b5a`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*log(K)*Min(alpha_tilde, alpha_G*log(K)))` (O; dann2023blackbox Corollary 15)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · bounded_pm1 (`S-8c66660d`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `T**(2/3)*(delta_G*log(K))**(1/3)` (O; dann2023blackbox Corollary 19)
- best lower: `T**(2/3)/8` (exact; inherited from alon2015online Theorem 11)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] · batched · knows M_batch (`S-9af086dd`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 1 vs lower 1 (tight)
- best upper: `sqrt(T*(K + T/M_batch)*log(K))` (O; esfandiari2019regret Lemma 7.1)
- best lower: `T/M_batch` (Omega; inherited from esfandiari2019regret Theorem 7.4)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · batched · knows M_batch (`S-6eed8cfa`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 1 vs lower 1 (tight)
- best upper: `sqrt(T*(K + T/M_batch)*log(K))` (O; inherited from esfandiari2019regret Lemma 7.1)
- best lower: `T/M_batch` (Omega; esfandiari2019regret Theorem 7.4)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · bounded_pm1 · finite (`S-9e778b6c`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## general_identification · stochastic · K-armed · dueling feedback · bernoulli (`S-fb1b31ee`, 1 papers): sample_complexity, worst_case — **log gap**
- K: upper 1·log^1.16667 vs lower 1·log^1 (log_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `K*log(K)*log(log(K))**3/epsilon**2` (O; falahatgar2017maximum Corollary 14)
- best lower: `K*log(K/delta)/epsilon**2` (Omega; falahatgar2017maximum Theorem 16)
- relies on inherited bounds: False

## stochastic · linear · adversarial contexts · bounded_pm1 · time_varying_action_sets · knows S · arbitrary compact (`S-67e5e13e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · bounded_pm1 · unit ball (`S-d6a9cbee`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012survey Theorem (th:ball)); `3*sqrt(T*d*log(T))` (exact; inherited from bubeck2012minimax Theorem 6)
- best lower: `sqrt(T*d)` (Omega; foster2021statistical Section 6.1.1 (text after Proposition prop:bandit_lower_linear))
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · gap_bounded_below · knows Delta_min (`S-121abc62`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `(1 + pi**2/3)*sum_arms(Delta_i) + 8*sum_subopt(log(T)/Delta_i)` (exact; inherited from auer2002ucb1 Theorem 1); `sum_subopt(c_alpha/Delta_i + (alpha_ucb2 + 1)*(4*alpha_ucb2 + 1)*log(2*Delta_i**2*E*T)/(2*Delta_i))` (exact; inherited from auer2002ucb1 Theorem 2); `Delta_max*K*(1 + pi**2/3) + sum_subopt(6*log(T)/Delta_i)` (exact; inherited from chen2014combinatorial Equation (eq:mabnew), Section 3.2)
- best lower: `Min(K/Delta_min, Delta_min*T)` (Omega; foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_tabular))
- relies on inherited bounds: True

## stochastic · K-armed · Gaussian · knows mu_star, sigma · K=2 (`S-40047484`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0 vs lower 0 (tight)
- best upper: `sum_subopt(3*Delta_i + 36*log(17/Delta_i)/Delta_i)` (exact; inherited from garivier2019explore Theorem (th:finiteRegret:mus:known)); `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 2); `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 3)
- best lower: `Min(Delta_min*T/2, 2*Delta_min*log(2)/(Delta_min**2 + 2*log(4*T)/T))` (exact; garivier2019explore Theorem (th:LB-BPR))
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · partial_monitoring feedback · bounded_pm1 (`S-a1c7df34`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T*log(K))/eps_obs` (O; gennaro2025instance Section 4 (Bandits with ill-conditioned observers))
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-955c8da1`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `18*d*rng*log(K) + 12*rng*sqrt(T*d*log(K))` (exact; hadiji2020adaptation Theorem 15); `2*sqrt(3)*sqrt(T*d*log(N_K))` (exact; inherited from bubeck2012survey Theorem (th:exp2john)); `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-955c8da1`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*(d - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · adversarial contexts · bounded_pm1 · knows M_ctx (`S-c9a184fb`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.666667·log^2 vs lower 0.666667 (log_gap)
- best upper: `T**(2/3)*log(T)**2` (O; han2020optimal Corollary 1)
- best lower: `T**(2/3)` (Omega_tilde; inherited from xu2022towards Corollary 9); `T**(2/3)` (Omega; inherited from lunghi2025online Remark 1)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-abe2ac6c`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*Min(beta_bar_M, mas_G))` (O_tilde; inherited from wen2024stochastic Theorem 3)
- best lower: `Min(T**(2/3), sqrt(K*T), sqrt(M_ctx*T*alpha_G))` (Omega; han2020optimal Theorem 6); `sqrt(T*Min(K, M_ctx, T**(1/3)))` (Omega_tilde; han2020optimal Corollary 2)
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · knows Delta_min, sigma (`S-eafb5403`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `K*sigma*log(1 + T/K)` (O; hanna2021solving Corollary 3); `sum_subopt(Max(Delta_i, sigma**2*(c_alg + 1)**2*log(sigma**2*(c_alg + 1)**2/(Delta_i**2*c_alg**2))/(Delta_i*c_alg**2)) + 2*sigma**2*(c_alg + 1)**2*log(Delta_i**2*T/sigma**2)/Delta_i)` (O; inherited from bian2022maillard Theorem 2); `sum_subopt(B_boost*sigma**2*(c_alg + 1)**2*log(log(Delta_i**2*T/(2*sigma**2)) + 1)/(Delta_i*c_alg**2) + Delta_i + 2*sigma**2*(c_alg + 1)**2*log(Delta_i**2*T*(log(Delta_i**2*T/(2*sigma**2) + 1) + 1)/(2*sigma**2))/Delta_i)` (O; inherited from bian2022maillard Theorem 4)
- best lower: `Min(K/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_tabular))
- relies on inherited bounds: True

## adversarial (oblivious) · linear (finite actions) · bounded_pm1 · knows s_sparse · finite · s_sparse=1 (`S-b3733bcc`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T/delta)` (O; inherited from krishnamurthy2018semiparametric Theorem 4) [delta=1/T]
- best lower: `sqrt(T)*d` (Omega; jang2026sparse Proposition 2.1)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · finite (`S-2b18387b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · bounded_pm1 · time_varying_action_sets · finite (`S-0ab423a7`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from chu2011suplinucb Theorem 2)
- relies on inherited bounds: True

## simple_regret · stochastic · K-armed · general_model_class (`S-eccda2d3`, 1 papers): simple_regret, worst_case — **log gap**
- K: upper 0.5·log^1 vs lower 0.5 (log_gap)
- T: upper -0.5 vs lower -0.5 (tight)
- best upper: `2*sqrt(sum_arms(sigma_i**2))*log(K)/sqrt(T)` (limsup; kato2023asymptotically Theorem 5.4)
- best lower: `sqrt(sum_arms(sigma_i**2))/(12*sqrt(T))` (liminf; kato2023asymptotically Corollary 3.6)
- relies on inherited bounds: False

## general_identification · stochastic · K-armed · bernoulli · knows reward_family · epsilon=0 (`S-ec1ff9c5`, 1 papers): sample_complexity, instance_dependent — **log gap**
- K: upper 1 vs lower 1 (log_gap)
- best upper: `K/C_min**2` (O_tilde; inherited from lindner2022interactively Theorem 2)
- best lower: `T_star*kl(delta, 1 - delta)` (exact; kaufmann2017monte Theorem 7)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · bernoulli · knows d_eff · finite (`S-9f8827f8`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sqrt(log(T/delta))/(2*p_c)) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## adversarial (adaptive) · structured_general · bounded_pm1 · knows loss_range · unit ball (`S-c33ee151`, 1 papers): expected_regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)` (O_tilde; kosoy2026computational Theorem 1)
- best lower: `sqrt(T)` (Omega; kosoy2026computational Theorem 3)
- relies on inherited bounds: False

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp, function_class (`S-b4cf3653`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(N_exp/delta))` (O_tilde; levy2026optimal Theorem 3.1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## nonstationary_drifting · K-armed · rewards in [0,1] · budgeted_exploration · knows B (`S-f4dc63b6`, 1 papers): dynamic_regret, worst_case — **log gap**
- T: upper 1 vs lower 1 (log_gap)
- best upper: `K**(1/3)*T*V_T**(1/3)/B**(1/3)` (O_tilde; li2025constrained Theorem 4.1)
- best lower: `K**(1/3)*T*V_T**(1/3)/B**(1/3)` (Omega; inherited from li2025constrained Theorem 5.1)
- relies on inherited bounds: True

## nonstationary_drifting · K-armed · rewards in [0,1] · budgeted_exploration · knows B, V_T (`S-58ec752b`, 1 papers): dynamic_regret, worst_case — **log gap**
- T: upper 1 vs lower 1 (log_gap)
- best upper: `K**(1/3)*T*V_T**(1/3)/B**(1/3)` (O_tilde; li2025constrained Theorem C.1); `K**(1/3)*T*V_T**(1/3)/B**(1/3)` (O_tilde; inherited from li2025constrained Theorem 4.1)
- best lower: `K**(1/3)*T*V_T**(1/3)/B**(1/3)` (Omega; li2025constrained Theorem 5.1)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows r_rank (`S-53cf90cb`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*r_rank)*(d_1 + d_2)**(3/2)*sqrt(log(1/delta))` (O_tilde; lu2020rank Theorem 1) [delta=1/T]
- best lower: `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows r_rank · unit ball · d_1=d, d_2=d (`S-485f33ec`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2); `2*sqrt(2)*d**(3/2)*sqrt(T*r_rank)*sqrt(log(1/delta))` (O_tilde; inherited from lu2020rank Theorem 1) [delta=1/T]
- best lower: `sqrt(T)*d*r_rank` (Omega; lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · lipschitz_metric · {bounded,lipschitz} · rewards in [0,1] · batched · knows M_batch · hypercube (`S-20cb2c78`, 1 papers): regret, worst_case — **log gap**
- T: upper 1·log^1 vs lower 1 (log_gap)
- best upper: `log(E*T)*Max(T**((d + 1)/(d + 2)), T**((d + 1)/((1 - 1/(d + 2)**M_batch)*(d + 2)))/M_batch**2, T**((d + 2)/(d + 3))/(W_mem*(M_batch - 1) + 1)**(1/(d*(d + 3))))` (O; lyu2026memory Theorem 3.1)
- best lower: `T**((d + 1)/((1 - 1/(d + 2)**M_batch)*(d + 2)))/M_batch**2` (Omega; lyu2026memory Lemma B.3)
- relies on inherited bounds: False

## pac_epsilon_best · stochastic · combinatorial · Gaussian · knows m · finite (`S-0b0a32c4`, 1 papers): sample_complexity, worst_case — **log gap**
- d: upper 1·log^1 vs lower 1 (log_gap)
- epsilon: upper 2 vs lower 2 (tight)
- best upper: `d*m*log(d/m)/epsilon**2 + d*log(1/delta)/epsilon**2` (O; maiti2026power Table 1)
- best lower: `d*m/epsilon**2 + d*log(1/delta)/epsilon**2` (Omega; maiti2026power Table 1); `m*(d - m + 1)/epsilon**2` (Omega; maiti2026power Theorem (appendix:thm-m-sets))
- relies on inherited bounds: False

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] (`S-b01170be`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `K + 4*sqrt(T*alpha_tilde*log(K))` (exact; inherited from rouyer2022near Theorem 2); `sqrt(T*alpha_G*log(K))` (O; inherited from gennaro2025instance Section 4 (Strongly observable feedback graphs)); `C_const*sqrt(T*alpha_bar*(log(K/alpha_bar) + 2)) + log(alpha_bar)/log(2)` (exact; inherited from eldowa2023minimax Theorem 3)
- best lower: `0.06*sqrt(T*alpha_G)` (exact; mannor2011from Theorem 4)
- relies on inherited bounds: True

## adversarial · K-armed · rewards in [0,1] · knows S_T (`S-239ed3e7`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `2*sqrt(2)*sqrt(K*T*log(K)) + (sqrt(2)*sqrt(K*T/log(K)) + 1)*log(2/delta)` (exact; inherited from neu2015explore Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-27f856f6`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*log(K)*Min(alpha_tilde, alpha_G*log(K)))` (O; inherited from dann2023blackbox Corollary 15)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-3c1ecab1`, 1 papers): expected_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `1.2*sqrt(T)*m*log(5/delta) + sqrt(T)*(2*sqrt(2)*sqrt(log(5/delta)) + 1.2) + 3*m*sqrt(T*d*(log(d/m) + 1)) + 2*sqrt(d*log(5/delta))*(sqrt(m) + m*sqrt(log(d/m) + 1)) + sqrt(T*d*m)*(log(5*d/delta) + 2) + sqrt(2)*sqrt(T*m*log(5/delta))*(sqrt(log(d/m) + 1) + 1)` (exact; neu2015importance Theorem 2) [delta=1/T]
- best lower: `0.008*sqrt(T)*d` (exact; inherited from audibert2011minimax Theorem 20); `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## nonstationary_drifting · lipschitz_metric · {bounded,lipschitz} · rewards in [0,1] · infinitely_many_arms · knows L_lip, V_T · d=1 (`S-8643cea7`, 1 papers): dynamic_regret, worst_case — **log gap**
- T: upper 0.75·log^2 vs lower 0.75 (log_gap)
- best upper: `(T**(3/4)*V_T**(1/4) + T**(2/3))*log(T)**2` (O; inherited from nguyen2025stationary Corollary 1)
- best lower: `T**(3/4)*V_T**(1/4) + T**(2/3)` (Omega; nguyen2025stationary Theorem 1)
- relies on inherited bounds: True

## nonstationary_drifting · lipschitz_metric · {bounded,lipschitz} · rewards in [0,1] · infinitely_many_arms · knows L_lip · d=1 (`S-c7851681`, 1 papers): dynamic_regret, worst_case — **log gap**
- T: upper 0.75·log^2 vs lower 0.75 (log_gap)
- best upper: `(T**(3/4)*V_T**(1/4) + T**(2/3))*log(T)**2` (O; nguyen2025stationary Corollary 1)
- best lower: `T**(3/4)*V_T**(1/4) + T**(2/3)` (Omega; inherited from nguyen2025stationary Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · subgaussian · knows Delta_min (`S-3062cad4`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `sum_subopt(2/(Delta_i*rho))*log(T)` (limsup; inherited from jin2021mots Theorem 2); `sum_subopt(2/Delta_i)*log(T)` (limsup; inherited from jin2021mots Theorem 3)
- best lower: `Min(K/Delta_min, Delta_min*T)` (Omega; inherited from foster2021statistical Section 6.1.5 (text after Proposition prop:bandit_gap_tabular))
- relies on inherited bounds: True

## stochastic · K-armed · rewards in [0,1] · time_varying_action_sets · bayesian_prior · knows prior (`S-8fdfb862`, 1 papers): bayesian_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `4*sqrt(K*T*(6*log(T) + 2)) + 2*Min(K, T)` (exact; russo2014posterior Proposition (prop:finite))
- best lower: `sqrt(K*T)` (Omega; inherited from shufaro2024bits Proposition C.1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · dueling feedback · bernoulli (`S-c683c228`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.333333·log^0.333333 vs lower 0.333333 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `6*T**(2/3)*(K*log(K))**(1/3)` (exact; saha2020adversarial Theorem 2)
- best lower: `K**(1/3)*T**(2/3)` (Omega; saha2020adversarial Theorem (thm:lb))
- relies on inherited bounds: False

## adversarial_restricted · K-armed · dueling feedback · bernoulli (`S-2cf35b3b`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 2 vs lower 2 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^1 vs lower 0 (log_gap)
- best upper: `64*K*log(2*K*T/delta)/Delta**2` (exact; saha2020adversarial Theorem (thm:ub_gap_whp)) [delta=1/T]
- best lower: `Min(K/Delta**2, Delta*T)` (Omega; saha2020adversarial Theorem (thm:lb_gap))
- relies on inherited bounds: False

## nonstationary_drifting · K-armed · dueling feedback · bernoulli · knows S_T, V_T (`S-4430346d`, 1 papers): dynamic_regret, worst_case — **log gap**
- K: upper 0.333333 vs lower 0.333333 (log_gap)
- T: upper 0.666667·log^1 vs lower 0.666667 (log_gap)
- best upper: `(4*K**(2/3)*T**(1/3)/V_T**(1/3) + K**(1/3)*T**(2/3)*V_T**(1/3))*log(K*T/delta)` (O; saha2021optimala Theorem (theorem:3s_boundcv))
- best lower: `T**(2/3)*(K*V_T)**(1/3)` (Omega; inherited from saha2021optimala Theorem (theorem:lower_bound_continuous))
- relies on inherited bounds: True

## simple_regret · stochastic · linear (finite actions) · dueling feedback · bernoulli · finite (`S-39964b81`, 1 papers): simple_regret, worst_case — **log gap**
- T: upper -0.5·log^0.5 vs lower -0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(d/T)*(20*eps_alg + 20)*(sqrt(lam) + sqrt(d*log(4*T/(d*lam**(1/d)) + lam**(1 - 1/d)) + 2*log(1/delta)))` (exact; scheid2024optimal Theorem (theorem:simple_regret_upper_bound)); `30*sqrt(d/T)*(sqrt(d*log(d**(-1 + 1/d)*(4*T + 1)) + 2*log(1/delta)) + 1/sqrt(d))` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound)); `(30*d + 60)*sqrt(log(d**(-1 + 1/d)*(4*T + 1)))/sqrt(T) + 31/sqrt(T)` (exact; scheid2024optimal Corollary (corollary:simple_regret_upper_bound))
- best lower: `d*exp(-5)/(4*sqrt(T))` (exact; scheid2024optimal Theorem (theorem:lower_bound))
- relies on inherited bounds: False

## stochastic · linear · subgaussian · convex body (`S-b6cbf2c3`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*(d - 1)` (Omega; shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6); `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · hypercube (`S-173a7f73`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*(d - 1)` (Omega; shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · rewards in [0,1] · bayesian_prior · knows prior · finite (`S-974a24a2`, 1 papers): bayesian_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(2)*sqrt(T*d*log(K))/2` (exact; inherited from russo2014information Proposition 5); `E_sqrt_l0*sqrt(T*d)` (O_tilde; inherited from russo2014posterior Proposition (prop:linear))
- best lower: `sqrt(T*d)` (Omega; shufaro2024bits Proposition C.2)
- relies on inherited bounds: True

## stochastic · lipschitz_metric · {lipschitz} · rewards in [0,1] · infinitely_many_arms · knows L_lip · d=1 (`S-9dfee86c`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.666667·log^0.333333 vs lower 0.666667 (log_gap)
- best upper: `L_lip**(1/3)*T**(2/3)*(c_ALG + 1)*log(T)**(1/3)` (exact; slivkins2019introduction Theorem 57)
- best lower: `L_lip**(1/3)*T**(2/3)` (Omega; slivkins2019introduction Theorem 58)
- relies on inherited bounds: False

## stochastic · linear · heavy_tailed · knows eps_m, v_mom · arbitrary compact (`S-212d8173`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `T**(1/(eps_m + 1))*d**((3*eps_m + 1)/(2*eps_m + 2))` (O_tilde; tajdini2025improved Corollary 1)
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `T**(1/(eps_m + 1))*d/192` (exact; inherited from shao2018almost Theorem 1); `T**(1/(eps_m + 1))*d**(2*eps_m/(eps_m + 1))` (Omega; inherited from tajdini2025improved Theorem 1)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · heavy_tailed · knows eps_m, v_mom · finite (`S-844d366e`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0·log^0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `T**(1/(eps_m + 1))*sqrt(d)*log(K)**(eps_m/(eps_m + 1))` (O_tilde; tajdini2025improved Corollary 1); `T**(1/(eps_m + 1))*d**((3*eps_m + 1)/(2*eps_m + 2))` (O_tilde; inherited from tajdini2025improved Corollary 1)
- best lower: `T**(1/(eps_m + 1))*d**(eps_m/(eps_m + 1))*(log(K)/log(d))**(eps_m/(eps_m + 1))` (Omega; tajdini2025improved Theorem 2); `T**(1/(eps_m + 1))*d**(eps_m/(eps_m + 1))*r_rank**(eps_m/(eps_m + 1))` (Omega; inherited from kang2024rank Theorem 5.1)
- relies on inherited bounds: True

## stochastic · linear · heavy_tailed · knows eps_m, v_mom · polytope (`S-cbe58259`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `T**(1/(eps_m + 1))*d**((3*eps_m + 1)/(2*eps_m + 2))` (O_tilde; inherited from tajdini2025improved Corollary 1)
- best lower: `T**(1/(eps_m + 1))*d**(2*eps_m/(eps_m + 1))` (Omega; tajdini2025improved Theorem 1); `T**(1/(eps_m + 1))*d/192` (exact; inherited from shao2018almost Theorem 1); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · heavy_tailed · knows eps_m, v_mom · unit ball (`S-86ea003b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `T**(1/(eps_m + 1))*d**((3*eps_m + 1)/(2*eps_m + 2))` (O_tilde; inherited from tajdini2025improved Corollary 1)
- best lower: `T**(1/(eps_m + 1))*d**(2*eps_m/(eps_m + 1))` (Omega; tajdini2025improved Theorem 4); `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · continuum_other · semi_bandit feedback · {bounded,lipschitz} · rewards in [0,1] · knows L_lip · simplex (`S-a1471a3f`, 1 papers): regret, worst_case — **log gap**
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0.5 vs lower 0.666667 (unresolved)
- d: upper 0 vs lower 0 (log_gap)
- best upper: `K*T**(2/3)*log(T)**(1/3)` (O; tang2020bandit Theorem 4.2); `sqrt(T)*Max(1, L_z)*Max(d, sqrt(d*m_z))/sqrt(m_0)` (O_tilde; inherited from jagadeesan2022regret Theorem 4)
- best lower: `K*T**(2/3)` (Omega; tang2020bandit Theorem 6.1); `K*T**(2/3)` (Omega; tang2020bandit Theorem 6.1)
- relies on inherited bounds: True

## stochastic · combinatorial · cascade feedback · bernoulli · knows m, reward_family · finite (`S-ffd83166`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T)` (O_tilde; inherited from vial2022minimax Theorem 2); `sqrt(K*T)` (O_tilde; inherited from vial2022minimax Theorem 2)
- best lower: `sqrt(K*T)` (Omega; vial2022minimax Theorem 1)
- relies on inherited bounds: True

## nonstationary_drifting · K-armed · full_information feedback · rewards in [0,1] (`S-9076fe31`, 1 papers): dynamic_regret, data_dependent — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `sqrt(T*V_T*log(K)) + (Lambda_T*T*V_T*log(K))**(1/3)` (O_tilde; wei2017tracking Theorem 3.5)
- best lower: `V_T + (Lambda_T*T*V_T)**(1/3)` (Omega; inherited from wei2017tracking Theorem 4.3)
- relies on inherited bounds: True

## stochastic · K-armed · graph_feedback feedback · adversarial contexts · rewards in [0,1] · knows M_ctx (`S-8250920e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*Min(beta_bar_M, mas_G))` (O_tilde; wen2024stochastic Theorem 3)
- best lower: `Min(T**(2/3), sqrt(K*T), sqrt(M_ctx*T*alpha_G))` (Omega; inherited from han2020optimal Theorem 6); `sqrt(T*Min(K, M_ctx, T**(1/3)))` (Omega_tilde; inherited from han2020optimal Corollary 2)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · graph_feedback feedback · rewards in [0,1] · knows alpha_G, m · finite (`S-2044575f`, 1 papers): expected_regret, worst_case — **log gap**
- K: upper 0 vs lower 0·log^0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)*m + sqrt(T*alpha_G*m)` (O_tilde; wen2025adversarial Theorem 1.1); `m*sqrt(T*alpha_G)` (O_tilde; inherited from wen2025adversarial Theorem 5.2); `Min(m*sqrt(T*alpha_G), sqrt(K*T*m))` (O_tilde; inherited from wen2025adversarial Theorem 5.2)
- best lower: `m*sqrt(T*log(K/m)) + sqrt(T*alpha_G*m)` (Omega; wen2025adversarial Theorem 1.3)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · graph_feedback feedback · rewards in [0,1] · knows alpha_G, m · finite (`S-a18f41c4`, 1 papers): expected_regret, worst_case — **log gap**
- K: upper 0 vs lower 0·log^0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `m*sqrt(T*alpha_G)` (O_tilde; wen2025adversarial Theorem 5.2); `Min(m*sqrt(T*alpha_G), sqrt(K*T*m))` (O_tilde; wen2025adversarial Theorem 5.2)
- best lower: `m*sqrt(T*log(K/m)) + sqrt(T*alpha_G*m)` (Omega; inherited from wen2025adversarial Theorem 1.3)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · graph_feedback feedback · rewards in [0,1] · knows alpha_G, m · finite (`S-a18f41c4`, 1 papers): pseudo_regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `m*sqrt(T*alpha_G)` (O_tilde; wen2025adversarial Theorem 5.2); `Min(m*sqrt(T*alpha_G), sqrt(K*T*m))` (O_tilde; wen2025adversarial Theorem 5.2)
- best lower: `0.008*sqrt(T)*d` (exact; inherited from audibert2011minimax Theorem 20)
- relies on inherited bounds: True

## corrupted stochastic · K-armed · rewards in [0,1] · knows m (`S-1d591128`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 1 vs lower 1 (log_gap)
- T: upper 0·log^2 vs lower 0·log^1 (log_gap)
- best upper: `C + sum_subopt(log(T)*log(K*T)/Delta_i)` (O; xu2021simple Theorem 1.2); `C + sum_subopt(log(T)*log(K*T)/Delta_i) + K*log(1/Delta_min)*log(K/Delta_min)/Delta_min` (O; inherited from hu2025near Theorem 1)
- best lower: `sum_subopt(Delta_i/kl_i)*log(T)` (liminf; inherited from bubeck2012survey Theorem (th:LR85))
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · heavy_tailed · time_varying_action_sets · knows eps_m, v_mom · finite (`S-cd4acbdc`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^1.5 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*T**(1/(eps_m + 1))*sqrt(d*log(2*K*T*log(T)/delta))*(120*(12*v_mom)**(1/(eps_m + 1)) + 120)*log(T) + 5*sqrt(2)*sqrt(T*log(2*K*T*log(T)/delta))` (exact; xue2020nearly Theorem 1) [delta=1/T]
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · heavy_tailed · time_varying_action_sets · knows eps_m, u_mom · finite (`S-293393b8`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^2 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T) + T**(1/(eps_m + 1))*sqrt(d)*(40*u_mom + 40*sqrt(2)*sqrt(u_mom*log(2*K*T*log(T)/delta)) + 80*log(2*K*T*log(T)/delta)/3)*log(T) + 40*sqrt(T*d)*log(T)` (exact; xue2020nearly Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · heavy_tailed · time_varying_action_sets · bayesian_prior · knows eps_m, u_mom · finite (`S-38914f9a`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^2 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `2*sqrt(T) + T**(1/(eps_m + 1))*sqrt(d)*(40*u_mom + 40*sqrt(2)*sqrt(u_mom*log(2*K*T*log(T)/delta)) + 80*log(2*K*T*log(T)/delta)/3)*log(T) + 40*sqrt(T*d)*log(T)` (exact; inherited from xue2020nearly Theorem 2) [delta=1/T]
- best lower: `T**(1/(eps_m + 1))*(d - 1)**(eps_m/(eps_m + 1))/32` (exact; xue2020nearly Theorem 3)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · bernoulli · d=1 (`S-36e0f30f`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5); `sqrt(T)*log(T)` (O; inherited from achddou2020efficient Theorem 5)
- best lower: `sqrt(T)` (Omega; yuxiao2025joint Theorem C.1)
- relies on inherited bounds: True

## adversarial · continuum_other · full_information feedback · adversarial contexts · rewards in [0,1] (`S-c0634911`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T)` (O_tilde; zhang2022leveraging Theorem 4)
- best lower: `sqrt(T)` (Omega_tilde; zhang2022leveraging Theorem 4)
- relies on inherited bounds: False

## stochastic · linear · Gaussian · bayesian_prior · knows prior, sigma (`S-50431437`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `L_feat*d*sqrt(tr_Sigma0) + sqrt(T)*d*sigma` (O_tilde; zhu2026prior Corollary 2)
- best lower: `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-d28e0dff`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; zimmert2022return Theorem 6)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-9c94036e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*log(T*m_attr**2*log(T))**3)` (O; inherited from hu2025interactive Appendix A (overall regret, unnumbered derivation))
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-cacaa1b7`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · knows S_T (`S-acaa5b35`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(1/delta))` (O_tilde; inherited from huang2024high Theorem 1)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · finite (`S-0d1a0c0c`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · stochastic contexts · bounded_pm1 · knows context_distribution · finite (`S-a6139bef`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · bounded_pm1 · time_varying_action_sets · arbitrary compact (`S-a5c1aa92`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows L_feat, S, sigma · arbitrary compact (`S-5a59da3d`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Corollary 1); `sqrt(T)*d*log(T)` (O; inherited from hanna2021solving Lemma 1)
- best lower: `sqrt(T)*d` (Omega; inherited from bubeck2017sparsity Theorem 4); `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · bounded_pm1 · K=2 (`S-fb44de26`, 1 papers): pseudo_regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5·log^-1 (log_gap)
- best upper: `sqrt(2)*sqrt(T*log(2/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `2*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T)/log(T)` (Omega; inherited from pacchiano2020model Theorem 5.2)
- relies on inherited bounds: True

## adversarial (adaptive) · K-armed · bounded_pm1 · K=2 (`S-fb44de26`, 1 papers): expected_regret, worst_case — **log gap**
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(2)*sqrt(T*log(2/delta))` (O; inherited from zimmert2022return Theorem 6) [delta=1/T]; `2*sqrt(T*log(T/delta))` (O; inherited from zimmert2022return Theorem 5) [delta=1/T]
- best lower: `sqrt(T)/sqrt(pi)` (liminf; inherited from kobzar2022based Corollary 5)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows S_T, m · finite (`S-df4a6ef0`, 1 papers): expected_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `1.2*sqrt(T)*m*log(5/delta) + sqrt(T)*(2*sqrt(2)*sqrt(log(5/delta)) + 1.2) + 3*m*sqrt(T*d*(log(d/m) + 1)) + 2*sqrt(d*log(5/delta))*(sqrt(m) + m*sqrt(log(d/m) + 1)) + sqrt(T*d*m)*(log(5*d/delta) + 2) + sqrt(2)*sqrt(T*m*log(5/delta))*(sqrt(log(d/m) + 1) + 1)` (exact; inherited from neu2015importance Theorem 2) [delta=1/T]
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## adversarial (adaptive) · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m · finite (`S-30953112`, 1 papers): expected_regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `1.2*sqrt(T)*m*log(5/delta) + sqrt(T)*(2*sqrt(2)*sqrt(log(5/delta)) + 1.2) + 3*m*sqrt(T*d*(log(d/m) + 1)) + 2*sqrt(d*log(5/delta))*(sqrt(m) + m*sqrt(log(d/m) + 1)) + sqrt(T*d*m)*(log(5*d/delta) + 2) + sqrt(2)*sqrt(T*m*log(5/delta))*(sqrt(log(d/m) + 1) + 1)` (exact; inherited from neu2015importance Theorem 2) [delta=1/T]
- best lower: `Min(T*m, sqrt(T*d*m))/20` (exact; inherited from kveton2014tight Proposition 2)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-e9a0a033`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (adaptive) · linear (finite actions) · bounded_pm1 · arms_span_Rd · finite (`S-814688f7`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*d*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*d*(log(d) + log(1/delta)))` (Omega; inherited from bacchiocchi2026efficient Corollary 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · bounded_pm1 (`S-1c3b2b88`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(K*T*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-081aac7b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `T**(2/3)*(delta_bar*log(K))**(1/3)` (O; inherited from chen2021understanding Corollary 25); `T**(2/3)*(delta_G*log(K))**(1/3)` (O; inherited from dann2023blackbox Corollary 19)
- best lower: `T**(2/3)/8` (exact; inherited from alon2015online Theorem 11)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-6c441bea`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667·log^-1 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1); `T**(2/3)*alpha_G**(1/3)/(16*log(T))` (exact; inherited from arora2019bandits Theorem I.3)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-774bbb26`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667·log^-1 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-bb2e3955`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667·log^-1 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
- relies on inherited bounds: True

## adversarial (oblivious) · K-armed · rewards in [0,1] · switching_cost · knows S_T (`S-ddaab066`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0.333333 (unresolved)
- T: upper 0.666667 vs lower 0.666667 (log_gap)
- best upper: `Max(C_c**(1/3)*T**(2/3), sqrt(K*T))` (O_tilde; inherited from koren2017multi Theorem 7)
- best lower: `K**(1/3)*T**(2/3)` (Omega_tilde; inherited from cheng2023understanding Proposition 1); `K**(1/3)*T**(2/3)` (Omega_tilde; inherited from dekel2013bandits Theorem 1)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] (`S-0ef35a4b`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.333333 vs lower 0 (log_gap)
- T: upper 0.666667 vs lower 0.666667 (tight)
- best upper: `T**(2/3)*(delta_G*log(K))**(1/3)` (O; inherited from dann2023blackbox Corollary 19)
- best lower: `T**(2/3)/8` (exact; inherited from alon2015online Theorem 11)
- relies on inherited bounds: True

## adversarial · K-armed · graph_feedback feedback · rewards in [0,1] · knows alpha_G (`S-5d662254`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `sqrt(T*log(K)*Min(alpha_tilde, alpha_G*log(K)))` (O; inherited from dann2023blackbox Corollary 15)
- best lower: `sqrt(T*alpha_G)` (Omega; inherited from alon2014nonstochastic Theorem 5)
- relies on inherited bounds: True

## adversarial · linear (finite actions) · bounded_pm1 · knows vartheta · finite (`S-4da500ba`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## adversarial_bounded_memory · K-armed · rewards in [0,1] · knows S_T (`S-f51983ee`, 1 papers): hp_regret, worst_case — **log gap**
- K: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- best upper: `5.15*sqrt(K*T*log(K/delta))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T/log(K))*log(1/delta) + 5.15*sqrt(K*T*log(K))` (exact; inherited from bubeck2012survey Theorem (th:exp3P)); `sqrt(K*T*log(K/delta))` (O; inherited from zimmert2022return Theorem 6)
- best lower: `sqrt(T*(K - 1)*log(1/(4*delta)))/27` (exact; inherited from gerchinovitz2016refined Theorem 1)
- relies on inherited bounds: True

## stochastic · K-armed · Gaussian · knows mu_star, reward_family, sigma · K=2 (`S-d66b7845`, 1 papers): regret, instance_dependent — **log gap**
- Delta: upper 1 vs lower 1 (log_gap)
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0 vs lower 0 (tight)
- best upper: `sum_subopt(3*Delta_i + 36*log(17/Delta_i)/Delta_i)` (exact; inherited from garivier2019explore Theorem (th:finiteRegret:mus:known)); `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 2); `2*log(T)/Delta_min` (limsup; inherited from jin2020detc Theorem 3)
- best lower: `Min(Delta_min*T/2, 2*Delta_min*log(2)/(Delta_min**2 + 2*log(4*T)/T))` (exact; inherited from garivier2019explore Theorem (th:LB-BPR))
- relies on inherited bounds: True

## stochastic · K-armed · conditionally_subgaussian · knows loss_range (`S-08243091`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `32*K**2*log(2*K*T**2/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · K-armed · stochastic contexts · rewards in [0,1] · knows N_exp, context_distribution, function_class (`S-181d244f`, 1 papers): regret, worst_case — **log gap**
- K: upper 0.5 vs lower 0.5 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(K*T*log(N_exp/delta))` (O_tilde; inherited from levy2026optimal Theorem 3.1) [delta=1/T]
- best lower: `sqrt(K*T)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(K*T)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · finite (`S-78b66b34`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*log(T*m_attr**2*log(T))**3)` (O; inherited from hu2025interactive Appendix A (overall regret, unnumbered derivation))
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m (`S-cbacda1d`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*log(T*m_attr**2*log(T))**3)` (O; inherited from hu2025interactive Appendix A (overall regret, unnumbered derivation))
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-60e36e74`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(T*log(T*m_attr**2*log(T))**3)` (O; inherited from hu2025interactive Appendix A (overall regret, unnumbered derivation))
- best lower: `sqrt(T)` (Omega; inherited from xu2025online Theorem 5)
- relies on inherited bounds: True

## stochastic · continuum_other · partial_monitoring feedback · stochastic contexts · bounded_pm1 · knows M_ctx (`S-789edca2`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.666667·log^2 vs lower 0.666667 (log_gap)
- best upper: `T**(2/3)*log(T)**2` (O; inherited from han2020optimal Corollary 1)
- best lower: `T**(2/3)` (Omega; inherited from lunghi2025online Remark 1); `T**(2/3)` (Omega_tilde; inherited from xu2022towards Corollary 9)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · bernoulli · time_varying_action_sets · finite (`S-256091df`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 30)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · finite (`S-42b57436`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · finite (`S-6da6e851`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows S · finite (`S-475a32f4`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.75 vs lower 0.5·log^0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `130*(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (exact; inherited from jin2026nearly Corollary 17)
- best lower: `sqrt(T*d*log(n_act)*log(T/d))` (Omega; inherited from li2019nearlyminimax Theorem 2); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · adversarial contexts · rewards in [0,1] · finite (`S-f27bda00`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · bounded_pm1 · finite (`S-54ca6a61`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0.5 vs lower 0.5 (tight)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12)
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · rewards in [0,1] · finite (`S-202299c4`, 1 papers): regret, worst_case — **log gap**
- K: upper 0·log^0.5 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (tight)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `2*sqrt(3)*sqrt(T*d*log(K))` (exact; inherited from bubeck2012minimax Theorem 4); `sqrt(T*d*log(K))` (O; inherited from dann2023blackbox Corollary 12); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sqrt(log(T/delta))/(2*p_c)) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · stochastic contexts · subgaussian · arms_span_Rd · finite (`S-8fef6755`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5·log^0.5 vs lower 0.5 (log_gap)
- d: upper 0.5 vs lower 0.5 (log_gap)
- best upper: `sqrt(log(K/delta)) + (sqrt(T*d*log(T*d/delta)) + log(T*d/delta))/lambda_0` (O; inherited from bogunovic2020stochastic Theorem 5) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · subgaussian · knows S, sigma · finite (`S-ce9ba867`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; inherited from pacchiano2020model Theorem 6.1); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]; `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear (finite actions) · subgaussian · knows sigma · finite (`S-7ee304a4`, 1 papers): regret, worst_case — **log gap**
- K: upper 0 vs lower 0 (log_gap)
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 0 vs lower 0.5 (unresolved)
- best upper: `Min(K*sqrt(T)/d, sqrt(T)*d + T*sqrt(d)*eps_star)` (O_tilde; inherited from pacchiano2020model Theorem 6.1); `32*K**2*log(2*T**2*d/delta)/(1 - p_c)**2 + 4*sqrt(T)/(K - 1) + 4*delta + 8*sqrt(K*T)*(1 + sigma*sqrt(log(T/delta))/p_c) + 2*sqrt(2)*sqrt(T*log(2/delta))` (exact; inherited from kim2025linear Theorem 5) [delta=1/T]; `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T*d)` (Omega; inherited from foster2021statistical Section 5.1.3 (Regret lower bound paragraph, via Proposition prop:mab_lower and Theorem thm:lower_main_expectation)); `Min(T, sqrt(T*d))/20` (exact; inherited from auer2002exp3 Theorem 5.1); `sqrt(T*d)` (Omega; inherited from slivkins2019introduction Theorem 21)
- relies on inherited bounds: True

## stochastic · linear · Gaussian · bayesian_prior · knows L_feat, prior, sigma · sphere (`S-7dbf9d67`, 1 papers): bayesian_regret, worst_case — **log gap**
- T: upper 0.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `L_feat*d*sqrt(tr_Sigma0) + sqrt(T)*d*sigma` (O_tilde; inherited from zhu2026prior Corollary 2)
- best lower: `0.006*sqrt(T)*d` (exact; inherited from rusmevichientong2010linear Theorem 2.1)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, loss_range, sigma · arbitrary compact (`S-75780635`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Corollary 1); `sqrt(T)*d*log(T)` (O; inherited from hanna2021solving Lemma 1)
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Corollary 23)
- relies on inherited bounds: True

## stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows L_feat, S, sigma · arbitrary compact (`S-f028e884`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5·log^0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T*d*log(L_feat*T/(d*lam) + 1))*(S*sqrt(lam) + sigma*sqrt(d*log(L_feat*T**2/(d*lam) + T)))` (O; inherited from cella2020meta Corollary 1); `sqrt(T)*d*log(T)` (O; inherited from hanna2021solving Lemma 1)
- best lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10); `d*sqrt(T*eps_c*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 21); `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Corollary 23)
- relies on inherited bounds: True

## stochastic · linear · conditionally_subgaussian · knows S, sigma (`S-5caaac72`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d/10` (exact; inherited from dani2008stochastic Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 3); `sqrt(T)*(d - 1)` (Omega; inherited from shamir2015complexity Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · arbitrary compact (`S-6b07c33e`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · ellipsoid (`S-8eecdad2`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1.5 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `2*sqrt(2)*sqrt(T*d*log(T)*Max(128*d*log(T)*log(T**2/delta), 64*log(T**2/delta)**2/9))` (exact; inherited from dani2008stochastic Theorem 2) [delta=1/T]
- best lower: `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · ellipsoid (`S-bef7dd7c`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^0.55 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*delta + d*sqrt(T*log(T)*log(1/delta))*log(log(T/delta))` (O; inherited from li2019tight Theorem 2)
- best lower: `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

## stochastic · linear · subgaussian · knows L_feat, r_rank, sigma (`S-718a134b`, 1 papers): regret, worst_case — **log gap**
- T: upper 0.5·log^1 vs lower 0.5 (log_gap)
- d: upper 1 vs lower 1 (log_gap)
- best upper: `sqrt(T)*d*log(T)` (O; inherited from hanna2021solving Lemma 1)
- best lower: `sqrt(T)*d*r_rank` (Omega; inherited from lu2020rank Theorem 6)
- relies on inherited bounds: True

