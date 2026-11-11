# Conflicts (review queue)

An upper bound grows more slowly than a lower bound in the same setting and regime. Usually an extraction error (a dropped term, a missing assumption in the setting) — occasionally a genuine contradiction.

- adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-0c139a66`, 1 papers), regret / worst_case, variable K: upper 0·log^0.5 < lower 0
  - upper: `1099511627776*Min(T, sqrt(T*log(K))*log(E*K*T)**2)` (exact; inherited from cesari2026action Theorem 2) — conditions: graph strongly revealing, known and fixed; oblivious losses in [0,1]^K
  - lower: `T**(2/3)/log(T)` (Omega; arora2019bandits Theorem 5.1)
- adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-0c139a66`, 1 papers), regret / worst_case, variable T: upper 0.5·log^2 < lower 0.666667·log^-1
  - upper: `1099511627776*Min(T, sqrt(T*log(K))*log(E*K*T)**2)` (exact; inherited from cesari2026action Theorem 2) — conditions: graph strongly revealing, known and fixed; oblivious losses in [0,1]^K
  - lower: `T**(2/3)/log(T)` (Omega; arora2019bandits Theorem 5.1)
- adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-6f1e943a`, 1 papers), regret / worst_case, variable K: upper 0·log^0.5 < lower 0
  - upper: `1099511627776*Min(T, sqrt(T*log(K))*log(E*K*T)**2)` (exact; cesari2026action Theorem 2) — conditions: graph strongly revealing, known and fixed; oblivious losses in [0,1]^K
  - lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
- adversarial (oblivious) · K-armed · graph_feedback feedback · rewards in [0,1] · switching_cost (`S-6f1e943a`, 1 papers), regret / worst_case, variable T: upper 0.5·log^2 < lower 0.666667·log^-1
  - upper: `1099511627776*Min(T, sqrt(T*log(K))*log(E*K*T)**2)` (exact; cesari2026action Theorem 2) — conditions: graph strongly revealing, known and fixed; oblivious losses in [0,1]^K
  - lower: `T**(2/3)/log(T)` (Omega; inherited from arora2019bandits Theorem 5.1)
- pac_epsilon_best · stochastic · combinatorial · rewards in [0,1] · knows m · finite (`S-e7a8db51`, 1 papers), sample_complexity / worst_case, variable d: upper 0 < lower 1
  - upper: `K*(log(1/delta) + log(m))/epsilon**2` (O; chen2016pure Theorem 1.7)
  - lower: `d/epsilon**2` (Omega; inherited from rejwan2019combinatorial Theorem 10)
- stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows m, reward_family · finite (`S-88bac412`, 1 papers), regret / instance_dependent, variable d: upper 0 < lower 1
  - upper: `K*m**2*log(T)**2/Delta_min` (O; inherited from xu2021simple Theorem 1.1)
  - lower: `m*(d - m)*log(T)/(4*Delta)` (liminf; inherited from kveton2014tight Proposition 1)
- pac_epsilon_best · stochastic · combinatorial · bernoulli · knows m, reward_family · finite (`S-70c3bd9a`, 1 papers), sample_complexity / worst_case, variable d: upper 0 < lower 1
  - upper: `K*(log(1/delta) + log(m))/epsilon**2` (O; inherited from chen2016pure Theorem 1.7)
  - lower: `d/epsilon**2` (Omega; rejwan2019combinatorial Theorem 10)
- stochastic · combinatorial · semi_bandit feedback · bernoulli · knows m · finite (`S-a06b480b`, 1 papers), regret / instance_dependent, variable d: upper 0 < lower 1
  - upper: `log(T)` (O; inherited from lai2007cognitive Lemma 11)
  - lower: `d*log(T)/(eps_gap*m)` (Omega; yang2021combinatorial Theorem 3)
- nonstationary_drifting · continuum_other · full_information feedback · adversarial contexts · {bounded} · bounded_pm1 · knows V_T (`S-540a698b`, 1 papers), dynamic_regret / worst_case, variable T: upper 0 < lower 1
  - upper: `Min(S_T, sqrt(T*V_T))` (O_tilde; inherited from zhou2025learning Theorem (thm:bobw)) — conditions: V_T = Omega(ln T)
  - lower: `T*c_1` (exact; zhou2025learning Proposition (prop:lb1))
- nonstationary_drifting · continuum_other · full_information feedback · adversarial contexts · {bounded} · bounded_pm1 (`S-6e75cd9f`, 1 papers), dynamic_regret / worst_case, variable T: upper 0 < lower 1
  - upper: `Min(S_T, sqrt(T*V_T))` (O_tilde; zhou2025learning Theorem (thm:bobw)) — conditions: V_T = Omega(ln T)
  - lower: `T*c_1` (exact; inherited from zhou2025learning Proposition (prop:lb1))
- nonstationary_switching · continuum_other · full_information feedback · adversarial contexts · {bounded} · bounded_pm1 (`S-a878f7d7`, 1 papers), dynamic_regret / worst_case, variable T: upper 0 < lower 1
  - upper: `S_T` (O_tilde; zhou2025learning Theorem (thm:full_lt1)) — conditions: L_T = o(T)
  - lower: `T*c_1**2` (exact; inherited from zhou2025learning Proposition (prop:lb1))
- nonstationary_switching · continuum_other · full_information feedback · adversarial contexts · {bounded} · bounded_pm1 · knows S_T (`S-469c2c8b`, 1 papers), dynamic_regret / worst_case, variable T: upper 0 < lower 1
  - upper: `S_T` (O_tilde; inherited from zhou2025learning Theorem (thm:full_lt1)) — conditions: L_T = o(T)
  - lower: `T*c_1**2` (exact; zhou2025learning Proposition (prop:lb1))
- stochastic · combinatorial · semi_bandit feedback · rewards in [0,1] · knows loss_range, m · finite (`S-8b4db714`, 1 papers), regret / instance_dependent, variable d: upper 0 < lower 1
  - upper: `sum_subopt(log(T)*log(K*T)/Delta_i) + K*m*log(1/Delta_min)*log(K/Delta_min)/Delta_min` (O; inherited from hu2025near Theorem 6)
  - lower: `d*log(T)/(eps_gap*m)` (Omega; inherited from yang2021combinatorial Theorem 3)

## Vacuous upper bounds (regret growing at least linearly in T)

No better than the trivial bound. Usually an extraction error, an unoptimised tuning parameter, or a data-dependent quantity read at its worst case.

- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 17)
- `T*d*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 18)
- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 10)
- `T*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 11)
- `sqrt(K)*T**(1/(2 - 2**(1 - M_batch)))*log(K)*sqrt(log(K*T))` (O; gao2019batched Theorem 4)
- `K*T**(1/M_batch)*log(K)*log(K*T)/Delta_min` (O; gao2019batched Theorem 4)
- `T**(1/(-eps_m*(eps_m/(eps_m + 1))**(M_batch - 1) + eps_m + 1))*v_mom**(1/(eps_m + 1))*(K*log(K*T))**(eps_m/(eps_m + 1))*log(K)` (O; guo2025batched Theorem 1)
- `K*T**(1/M_batch)*v_mom**(1/eps_m)*(1/Delta_min)**(1/eps_m)*log(K)*log(K*T)` (O; guo2025batched Theorem 1)
- `(sqrt(T*d) + T*d/M_batch)*log(T)*sqrt(log(K*T))` (O; han2020sequential Theorem 1)
- `C*T**(1/(M_batch + 3)) + T**(4/(M_batch + 3))*(sum_subopt(M_batch*log(K*T)/Delta_i) + K*log(1/Delta_min)*log(T)*log(K/Delta_min)/(Delta_min*M_batch))` (O; hu2025near Theorem 3)
- `T**(1/M_batch)*log(T)/Delta_min` (O; karpov2021batched Theorem 1)
- `T**(1/(2 - 2**(1 - M_batch)))*sqrt(log(T))` (O; karpov2021batched Theorem 7)
- `3*L_star*d*eta*m + 3*d*m**2*(-log(eta) + 2*log(d/m) + 1) + 3*d + m*(log(d/m) + 1)/eta` (exact; neu2015first Corollary (cor:nonadapt))
