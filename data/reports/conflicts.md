# Conflicts (review queue)

An upper bound grows more slowly than a lower bound in the same setting and regime. Usually an extraction error (a dropped term, a missing assumption in the setting) — occasionally a genuine contradiction.

- stochastic · K-armed · rewards in [0,1] · unique_optimal_arm (`S-6b5fd24d`, 2 papers), regret / instance_dependent, variable K: upper 0.5·log^-1 < lower 1
  - upper: `3*sqrt(K)/2 + 4*log(T) + 8` (exact; inherited from zimmert2021tsallisinf Theorem 1)
  - lower: `sum_subopt(Delta_i/(mu_i**2*log(mu_i/mu_star)/(mu_i**2 + sigma_i**2) + sigma_i**2*log(sigma_i**2/(Delta_i*mu_i + sigma_i**2))/(mu_i**2 + sigma_i**2)))` (liminf; ito2022variance Proposition 1)
- stochastic · K-armed · Gaussian · knows Delta, sigma · K=2, sigma_std=1 (`S-105752ee`, 2 papers), regret / instance_dependent, variable T: upper 0 < lower 0·log^1
  - upper: `1` (O; inherited from hao2020adaptive Theorem 3)
  - lower: `log(T)/(2*Delta_min)` (liminf; garivier2016etc Theorem 6)
- stochastic · K-armed · Gaussian · knows sigma · K=2, sigma_std=1 (`S-62cb34c0`, 1 papers), regret / instance_dependent, variable T: upper 0 < lower 0·log^1
  - upper: `1` (O; inherited from hao2020adaptive Theorem 3)
  - lower: `log(T)/(2*Delta_min)` (liminf; inherited from garivier2016etc Theorem 6)
- corrupted stochastic · K-armed · rewards in [0,1] · unique_optimal_arm (`S-0e1ac51c`, 2 papers), regret / instance_dependent, variable K: upper 0.5·log^-0.333333 < lower 1
  - upper: `3*sqrt(K)/2 + 2*sqrt(2)*sqrt(C*(sum_subopt((4*log(T) + 12)/Delta_i) + 2/Delta_min)) + 4*log(T) + 8` (exact; inherited from zimmert2021tsallisinf Theorem 1)
  - lower: `sum_subopt(Delta_i/(mu_i**2*log(mu_i/mu_star)/(mu_i**2 + sigma_i**2) + sigma_i**2*log(sigma_i**2/(Delta_i*mu_i + sigma_i**2))/(mu_i**2 + sigma_i**2)))` (liminf; inherited from ito2022variance Proposition 1)
- corrupted stochastic · K-armed · rewards in [0,1] · unique_optimal_arm (`S-0e1ac51c`, 2 papers), regret / instance_dependent, variable T: upper 0·log^0.833333 < lower 0·log^1
  - upper: `3*sqrt(K)/2 + 2*sqrt(2)*sqrt(C*(sum_subopt((4*log(T) + 12)/Delta_i) + 2/Delta_min)) + 4*log(T) + 8` (exact; inherited from zimmert2021tsallisinf Theorem 1)
  - lower: `sum_subopt(Delta_i/(mu_i**2*log(mu_i/mu_star)/(mu_i**2 + sigma_i**2) + sigma_i**2*log(sigma_i**2/(Delta_i*mu_i + sigma_i**2))/(mu_i**2 + sigma_i**2)))` (liminf; inherited from ito2022variance Proposition 1)
- stochastic · K-armed · Gaussian · sigma_std=1 (`S-c5d52449`, 1 papers), regret / instance_dependent, variable K: upper 0 < lower 1
  - upper: `1` (O; inherited from hao2020adaptive Theorem 3)
  - lower: `(K - 1)*log(Delta**2*T/(K - 1))/(4*Delta)` (exact; lattimore2015ocucb Theorem 3)
- stochastic · K-armed · Gaussian · sigma_std=1 (`S-c5d52449`, 1 papers), regret / instance_dependent, variable T: upper 0 < lower 0·log^1
  - upper: `1` (O; inherited from hao2020adaptive Theorem 3)
  - lower: `(K - 1)*log(Delta**2*T/(K - 1))/(4*Delta)` (exact; lattimore2015ocucb Theorem 3)
- adversarial_self_bounding · K-armed · rewards in [0,1] · unique_optimal_arm (`S-96e4adce`, 2 papers), regret / instance_dependent, variable K: upper 0.5·log^-0.378 < lower 1
  - upper: `3*sqrt(K)/2 + 2*sqrt(C_sb*(sum_subopt((4*log(T) + 12)/Delta_i) + 2/Delta_min)) + 4*log(T) + 8` (exact; zimmert2021tsallisinf Theorem 1)
  - lower: `sum_subopt(Delta_i/(mu_i**2*log(mu_i/mu_star)/(mu_i**2 + sigma_i**2) + sigma_i**2*log(sigma_i**2/(Delta_i*mu_i + sigma_i**2))/(mu_i**2 + sigma_i**2)))` (liminf; inherited from ito2022variance Proposition 1)
- adversarial_self_bounding · K-armed · rewards in [0,1] · unique_optimal_arm (`S-96e4adce`, 2 papers), regret / instance_dependent, variable T: upper 0·log^0.878 < lower 0·log^1
  - upper: `3*sqrt(K)/2 + 2*sqrt(C_sb*(sum_subopt((4*log(T) + 12)/Delta_i) + 2/Delta_min)) + 4*log(T) + 8` (exact; zimmert2021tsallisinf Theorem 1)
  - lower: `sum_subopt(Delta_i/(mu_i**2*log(mu_i/mu_star)/(mu_i**2 + sigma_i**2) + sigma_i**2*log(sigma_i**2/(Delta_i*mu_i + sigma_i**2))/(mu_i**2 + sigma_i**2)))` (liminf; inherited from ito2022variance Proposition 1)
