# Conflicts (review queue)

An upper bound grows more slowly than a lower bound in the same setting and regime. Usually an extraction error (a dropped term, a missing assumption in the setting) — occasionally a genuine contradiction.

- adversarial (oblivious) · linear · bounded_pm1 · l1 ball · p_norm=1 (`S-95105bc3`, 1 papers), regret / worst_case, variable T: upper 0.5·log^0.5 < lower 0.666667
  - upper: `d*sqrt(T*log(T))` (O; inherited from hazan2016volumetric Corollary 7.1) — conditions: K equipped with a membership oracle; losses satisfy |L^T x| <= 1 for all x in K
  - lower: `T**(2/3)*d**(1/3)/20` (exact; bubeck2017sparsity Theorem 5)
- stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · knows L_feat, S, sigma · finite (`S-e7387680`, 1 papers), regret / worst_case, variable K: upper 0 < lower 0.25
  - upper: `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; inherited from jin2026nearly Theorem 4) — conditions: K >= d >= 2; T >= d; noise N(0,1); ||theta||_2 <= 1, ||x_{t,i}||_2 <= 1
  - lower: `K**(1/4)*sqrt(T*d)` (Omega; jin2026nearly Theorem 1)
- stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · knows L_feat, S, sigma · finite (`S-e7387680`, 1 papers), regret / worst_case, variable d: upper 0.5 < lower 1
  - upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; inherited from jin2026nearly Theorem 3) — conditions: 2 <= K <= d <= T; noise N(0,1); ||theta||_2 <= 1, ||x_{t,i}||_2 <= 1
  - lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · finite (`S-7768e9b8`, 1 papers), regret / worst_case, variable K: upper 0 < lower 0.25
  - upper: `sqrt(T*d)*log(2*T*d)*Min(sqrt(d), (d*log(K))**(1/4))` (O; jin2026nearly Theorem 4) — conditions: K >= d >= 2; T >= d; noise N(0,1); ||theta||_2 <= 1, ||x_{t,i}||_2 <= 1
  - lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1)
- stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · finite (`S-7768e9b8`, 1 papers), regret / worst_case, variable d: upper 0.5 < lower 1
  - upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; jin2026nearly Theorem 3) — conditions: 2 <= K <= d <= T; noise N(0,1); ||theta||_2 <= 1, ||x_{t,i}||_2 <= 1
  - lower: `d*sqrt(T*log(T))` (Omega; inherited from li2019nearlyminimax Theorem 10)
- stochastic · linear (finite actions) · adversarial contexts · Gaussian · time_varying_action_sets · knows n_act, sigma · finite (`S-a4698ff8`, 1 papers), regret / worst_case, variable d: upper 0.5 < lower 1
  - upper: `(K*log(2*K*T + 1))**(1/4)*sqrt(T*d*log(T/d + 1))` (O; inherited from jin2026nearly Theorem 3) — conditions: 2 <= K <= d <= T; noise N(0,1); ||theta||_2 <= 1, ||x_{t,i}||_2 <= 1
  - lower: `d*sqrt(T*log(T))` (Omega; li2019nearlyminimax Theorem 10)
- stochastic · K-armed · rewards in [0,1] · knows m (`S-b9467e6d`, 1 papers), regret / worst_case, variable K: upper 0 < lower 0.5
  - upper: `sqrt(T*m*log(T))` (O; song2025outcome Theorem (thm:balanced-ucb-full)) — conditions: rewards in [0,1] with 1-sub-Gaussian noise; balanced partition s_o = K/m
  - lower: `Min(T, sqrt(K*T))/20` (exact; inherited from auer2002exp3 Theorem 5.1)
- stochastic · linear (finite actions) · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows sigma · finite (`S-f887286f`, 1 papers), regret / worst_case, variable K: upper 0 < lower 0.25
  - upper: `sqrt(T)*d**(3/2)*(sqrt(log(T)*log(1/delta)) + log(T))` (O; agrawal2013lints Theorem 1) [delta=1/T] — conditions: ||b_i(t)|| <= 1, ||mu|| <= 1, Delta_i(t) <= 1; noise conditionally R-sub-Gaussian (R = sigma)
  - lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1)
- stochastic · linear · adversarial contexts · conditionally_subgaussian · time_varying_action_sets · knows S, function_class, sigma · arbitrary compact (`S-22d6e1e6`, 1 papers), regret / worst_case, variable K: upper 0 < lower 0.25
  - upper: `2*sqrt(2)*sqrt(T*d*log(L_feat**2*T/(d*lam) + 1))*Max(1, sqrt(S**2*lam + d*sigma**2*log(L_feat**2*T/(d*lam) + 1) + 2*sigma**2*log(1/delta)))` (exact; baumgrtner2026gray Corollary 2) [delta=1/T] — conditions: V = 1, Lambda_0 = lambda_0 I, mu_0 = 0; ||theta*||_2 <= c_S (S); ||u||_2 <= c_L (L_feat); u^T theta* in [-1,1]; noise c_v-subgaussian (sigma = c_v)
  - lower: `K**(1/4)*sqrt(T*d)` (Omega; inherited from jin2026nearly Theorem 1)

## Vacuous upper bounds (regret growing at least linearly in T)

No better than the trivial bound. Usually an extraction error, an unoptimised tuning parameter, or a data-dependent quantity read at its worst case.

- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 17)
- `T*d*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 18)
- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 10)
- `T*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 11)
- `sqrt(K)*T**(1/(2 - 2**(1 - M_batch)))*log(K)*sqrt(log(K*T))` (O; gao2019batched Theorem 4)
- `K*T**(1/M_batch)*log(K)*log(K*T)/Delta_min` (O; gao2019batched Theorem 4)
- `3*L_star*d*eta*m + 3*d*m**2*(-log(eta) + 2*log(d/m) + 1) + 3*d + m*(log(d/m) + 1)/eta` (exact; neu2015first Corollary (cor:nonadapt))
