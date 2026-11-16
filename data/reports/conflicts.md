# Conflicts (review queue)

An upper bound grows more slowly than a lower bound in the same setting and regime. Usually an extraction error (a dropped term, a missing assumption in the setting) — occasionally a genuine contradiction.


## Vacuous upper bounds (regret growing at least linearly in T)

No better than the trivial bound. Usually an extraction error, an unoptimised tuning parameter, or a data-dependent quantity read at its worst case.

- `K**2*T**(2/M_batch) + sum_subopt(T**(1/M_batch)*log(K*T)/Delta_i) + K**2*T**(1/M_batch)*log(K)*log(log(K)/Delta_min)/Delta_min**2` (O; agarwal2022asymptotically Theorem 1.2)
- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 17)
- `T*d*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 18)
- `T*d**2*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 10)
- `T*eta/2 + d*log(2)/eta` (exact; audibert2011minimax Theorem 11)
- `9*T**(1/M_batch)*sum_subopt(1/Delta_i)*log(2*K*M_batch*T)` (exact; esfandiari2019regret Theorem 5.1)
- `T**(1/M_batch)*sqrt(T*d*log(K*T))` (O; esfandiari2019regret Theorem 6.2)
- `T**(1/M_batch)*d*sqrt(T*log(T))` (O; esfandiari2019regret Section 6.3 (Infinite Action Sets))
- `sqrt(T*(K + T/M_batch)*log(K))` (O; esfandiari2019regret Lemma 7.1)
- `sqrt(K)*T**(1/(2 - 2**(1 - M_batch)))*log(K)*sqrt(log(K*T))` (O; gao2019batched Theorem 4)
- `K*T**(1/M_batch)*log(K)*log(K*T)/Delta_min` (O; gao2019batched Theorem 4)
- `T**(1/(-eps_m*(eps_m/(eps_m + 1))**(M_batch - 1) + eps_m + 1))*v_mom**(1/(eps_m + 1))*(K*log(K*T))**(eps_m/(eps_m + 1))*log(K)` (O; guo2025batched Theorem 1)
- `K*T**(1/M_batch)*v_mom**(1/eps_m)*(1/Delta_min)**(1/eps_m)*log(K)*log(K*T)` (O; guo2025batched Theorem 1)
- `(sqrt(T*d) + T*d/M_batch)*log(T)*sqrt(log(K*T))` (O; han2020sequential Theorem 1)
- `C*T**(1/(M_batch + 3)) + T**(4/(M_batch + 3))*(sum_subopt(M_batch*log(K*T)/Delta_i) + K*log(1/Delta_min)*log(T)*log(K/Delta_min)/(Delta_min*M_batch))` (O; hu2025near Theorem 3)
- `T**(1/M_batch)*log(T)/Delta_min` (O; karpov2021batched Theorem 1)
- `T**(1/(2 - 2**(1 - M_batch)))*sqrt(log(T))` (O; karpov2021batched Theorem 7)
- `(K*T)**(eps_alg + 1/2)` (O; li2017beyond Theorem 4.13)
- `3*L_star*d*eta*m + 3*d*m**2*(-log(eta) + 2*log(d/m) + 1) + 3*d + m*(log(d/m) + 1)/eta` (exact; neu2015first Corollary (cor:nonadapt))
