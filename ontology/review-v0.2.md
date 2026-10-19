# Ontology review after the first pilot extraction (v0.2 → proposed v0.3)

Input: the `unmapped` fields of the first pilot extraction (36 papers, 87 settings, 192 results, 148 unmapped items; `data/extractions/`). `unmapped` is the extractor's escape hatch (desiderata D3). Recurring items are the signal for the next ontology version. Each proposal below lists the evidence.

**Status: proposed, not applied.** Applying v0.3 means re-extracting the corpus (about an hour on the CLI backend), so it waits for review.

## Proposed changes

### 1. Node parameter `action_set` (unify with BCO's `constraint_set`)
**Evidence:** almost every linear paper (OFUL, LinTS ×3, Li et al. 2019, Kong et al. 2023, Shamir 2015 ×6, Bubeck et al. 2012 ×3, Hazan & Karnin 2016, Kim et al. 2022). The BCO notes asked for the same thing.
```yaml
action_set:
  shape: [arbitrary_compact, finite, unit_ball, sphere, hypercube, simplex, l1_ball, polytope, convex_body]
  time_varying: [fixed, oblivious_sequence, adaptive_sequence]   # A_t changes over rounds
  norm_bounds: {x_norm: L_feat, theta_norm: S}                   # as node parameters
  access: [explicit, membership_oracle, separation_oracle, linear_optimization_oracle]
```
Lower bounds are proved on specific shapes, so lower-bound transfer along `shape` must go specific → general only (BCO notes §3). This is the biggest gap in v0.2.

### 2. Extend `learner_knows`
**Evidence:** Bubeck et al. 2013 (bounded regret) ×5, Garivier et al. 2019 ×3, Garivier et al. 2016 (ETC), Bubeck et al. 2013 (heavy tails) ×3, Garivier & Cappé 2011, Cappé et al. 2013. Add `mu_star`, `Delta` (the exact gap; distinct from a lower bound on it), `Delta_lower_bound`, `moment_bound`, `reward_family` (e.g. a known exponential family) and `S_switches`. Knowledge changes rates qualitatively: bounded vs log T regret.

### 3. Vocabulary for common extra assumptions
**Evidence:** "unique optimal arm" appears in Combes et al. 2017, Gupta et al. 2019, Garivier et al. 2016, Lattimore 2015 and Jin et al. 2023. It is currently free text in `extra_assumptions`/`unmapped`, so it cannot be compared. Add an `instance_assumptions` multi-select: `unique_optimal_arm`, `gap_bounded_below`, `means_in_known_interval`, `bounded_variance`, `arms_span_Rd`. Keep free text as a fallback.

### 4. Loss/reward range for adversarial settings
**Evidence:** "losses in [0,1]" or "[-1,1]" appears in 10+ adversarial settings, all now `noise: not_applicable` plus unmapped text. Proposal: rename `noise` → `reward_model`, allowing `bounded_01` and `bounded_pm1` for adversarial losses, or add a small `loss_range` dimension.

### 5. Adversary refinements (`environment`)
**Evidence:** Masoudian & Seldin 2021, Zimmert & Seldin 2021, Gerchinovitz & Lattimore 2016, Wei & Luo 2018. Add:
- `adversarial_self_bounding`: the stochastically constrained adversary / (Δ, C, T) self-bounding regime, with order `stochastic_iid ⊑ adversarial_self_bounding ⊑ adversarial_oblivious`.
- `adversarial_restricted` (for example small-loss or bounded-variation loss sequences), with the restriction as a node parameter.

### 6. Comparator / regret notion
**Evidence:** Neu 2015 (switching comparator, expert advice, feedback graphs), Lykouris et al. 2018 (regret on corrupted rewards), Agrawal & Goyal 2013 (per-round best arm in contextual), Neu 2015 / Gerchinovitz & Lattimore 2016 (realised regret). Add quantity `realized_regret`, and an `extras` value `expert_advice`. Make the comparator explicit (best fixed arm / best arm per round / best switching sequence / best expert).

### 7. New action spaces and objectives
- `structured_general` (OSSB: known parametric structure, which covers linear, Lipschitz, unimodal, …).
- Objective `optimization_error` (Shamir 2015: expected error of a returned point; it is the simple-regret analogue for continuous sets).

### 8. Out-of-scope detection
Kim et al. 2022 contains an episodic RL result (linear mixture MDP), and Wei & Luo 2018 contains a game-theoretic self-play result. Add a setting-level flag `in_scope: false`, with a reason, so those settings are excluded from the bandit graph instead of being forced into bandit vocabulary.

## Not changing (and why)
- Variance-adaptive / data-dependent bounds (Zhang et al. 2021, Kim et al. 2022, Ito 2022) are properties of a *bound*, not of the setting; they are already expressible as expressions in `sum sigma_t^2` with `symbols`.
- Bayesian vs frequentist regret is already covered by `quantity: bayesian_regret`. Priors go in `extra_assumptions`.
