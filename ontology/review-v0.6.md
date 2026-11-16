# Ontology review after batch 3 (ontology v0.6)

Input: the 9643 `unmapped` items in 1555 extractions, grouped into themes by one LLM pass with the ontology in context (`pipeline/review_unmapped.py`, opus). **Status: proposed, not applied.** 9629 of 9643 items were assigned to a theme.

| decision | themes | items | papers |
|---|---|---|---|
| ontology change | 19 | 4575 | 761 |
| result field | 2 | 346 | 107 |
| already expressible | 13 | 2830 | 489 |
| out of scope | 6 | 1884 | 294 |

## Synthesis and recommendations for v0.7 (hand-written, 2026-11-16)

Inputs: the themes below (LLM grouping of 9,643 `unmapped` items), the conflict review after batch 3 (85 → 9 conflict
cells; `data/corrections.yaml`, entries dated 2026-11-12), the batch-3 audit (`data/reports/audit-batch3.md`) and the
citation cross-check (`data/reports/crosscheck.md`). **Status (2026-11-16): items 1-3 applied in v0.7 and the ontology-change themes below in v0.8** (fields filled from the extracted text by `pipeline/fill_fields.py`, no re-extraction). v0.6 added only the kernel
family; items 1–2 of the v0.5 synthesis are still open and come first. Ranked by how much they change the atlas:

1. **Scope leakage (open since v0.5, larger now).** The out-of-scope themes below hold 1,884 items from 294 papers:
   state-dependent dynamics (107 papers), multi-agent (71), games / strategic agents / attacks (55), multi-objective
   (33), quantum (18). The extractor keeps `in_scope: true` and puts the feature in `unmapped`, so resolve.py's cut does
   not see it. Fix as proposed for v0.5: a cached one-pass classifier over in-scope settings that tags these features,
   and a resolve.py drop rule. No re-extraction.
2. **Combinatorial base-arm symbol (open since v0.5).** Three of the 9 remaining conflict cells are `d` vs `K` for base
   arms (chen2016pure vs rejwan2019combinatorial, lai2007cognitive vs yang2021combinatorial). Same proposal: `d` = base
   arms, `K` only for unstructured arms; re-extract the combinatorial papers (theme "Combinatorial structure", 99 papers).
3. **Fields the batch-3 conflict review needed** (patched with `model_change` / `instance_restriction` conditions):
   - **mechanism** for market settings: first/second-price bidding, posted prices, bilateral trade. The theme below calls
     auctions "already expressible" by mapping to continuum_other / partial_monitoring, but that mapping is what put
     bilateral trade (T/4, T^{2/3} lower bounds) in the same cells as auction bidding (√T upper bounds): 9 conflict
     cells. Needs a node parameter (`market.mechanism`, `market.value_timing` from v0.5 item 3), not guidance.
   - **dueling `regret_type`** {average, weak, strong, fixed_arm} next to `winner` (theme below): weak regret
     (hilgendorf2018duelling) and fixed-arm regret (saha2022versatile, saha2021optimala) sat in Borda cells.
   - **shape constraints on the means** (monotone, concave, unimodal) as `function_class` values over the arm index:
     cheshire2020influence's shape-constrained thresholding rates reached unstructured cells.
   - **linear structure of combinatorial / cascade items** (zhong2018thompson): `action_set` fields on combinatorial
     settings, or `function_class: linear` allowed there.
   - **comparator**: foresight regret (liu2022stationary) and ex-post benchmarks (balseiro2018contextual) are comparator
     values, not conditions (theme "Regret and comparator notions").
4. **The other ontology-change themes**, by papers: constraints / knapsacks / safety (85 papers), noise models (84),
   linear model details (82), feedback-graph and partial-monitoring structure (64), model selection / meta-learning (48),
   auxiliary observations (43), X-armed structure (37), risk functionals (34). Most are already in the vocabulary as
   coarse extras; the proposals refine them. Re-extract only the affected papers.
5. **Extraction quality.** Batch-3 audit (200 results): major errors 2% (1%–4%), as in batch 2; minor setting errors
   down from 36% to 25% (50 of 199). The minor errors are still missing knowledge (tuning inputs the algorithm uses),
   over-general noise models and a defining feature left in `unmapped`. The cross-check agrees 66% (62% after
   batch 2); its 83 consensus disagreements are mostly citations of a corollary (UCB1's √(KT log T)) or of a rate with
   Δ dropped, and a few papers without the cited side extracted (zoghi2013relative, wang2018thompson, zhou2019neural,
   zhang2020neural): a re-extraction queue.
6. **Fragmentation** is unchanged in kind: 93% of canonical settings come from a single paper.

## Ontology change

### Combinatorial structure: nonlinear/bottleneck/max rewards, full-bandit feedback, correlated base arms, triggering smoothness, approximation oracles (589 items, 99 papers)

Add combinatorial.outcome_dependence {independent, arbitrary_correlated} (independent ⊑ arbitrary_correlated). Add combinatorial.reward values max_or_bottleneck and general_smooth (linear ⊑ nonlinear_monotone_lipschitz ⊑ general_smooth). Full-bandit feedback on a combinatorial action is feedback=bandit (guidance). Approximation oracles go in the result's alpha_regret/conditions. Re-extract combinatorial papers.

Examples: `Censored feedback: per venue i the learner observes r_i = min(v_i, s_i), allowing a subgradient of the concave reward` (agarwal2010optimal); `Allocations v_i >= 0 with sum_i v_i <= V^t, volumes V^t in {1..V}; learner knows the volume bound V` (agarwal2010optimal); `Reward is sum_i min(v_i, s_i) (concave in allocations); comparator is best fixed unit-to-venue assignment opt in {1..K}^` (agarwal2010optimal); `Integer allocations u_i >= 0 with sum_i u_i <= V^t, V^t <= V; integer liquidities s_i; censored feedback min(u_i, s_i) p` (agarwal2010optimal)

### Constraints: knapsacks/BwK, safety, conservative baselines, fairness, long-term costs (594 items, 85 papers)

Keep node parameter constraints; extend kind with exposure_fairness (merit-proportional), quota_or_min_rate, envy_free_or_proportional, false_discovery_rate, return_on_spend; add field known_baseline {known_value, unknown_value, not_applicable} (known ⊑ unknown); add field signal {expected_only, observed_noisy, unobservable}. Benchmark (best fixed/LP/fluid feasible policy) stays on the result comparator best_feasible_policy. Re-extract settings with knapsack/safety/fairness extras.

Examples: `stage-wise conservative constraint: expected reward at every round >= (1-alpha) times known baseline reward r_{b,t}; lea` (afsharrad2025multi); `Diversity constraint: empirical item distribution must have entropy at least c (H_c)` (agarwal2022diversified); `Benchmark is the best item distribution in H_c intersected with EIRD(M), the everywhere-instantaneously-realizable set` (agarwal2022diversified); `Benchmarks: best item distribution in IRD of the uniform vector, or best menu distribution` (agarwal2022diversified)

### Noise models (raw vs central moments, symmetric/undefined-mean noise, location-dependent variance, parameter noise, sub-Weibull, Fisher-type KL conditions, time-varying variance) (262 items, 84 papers)

Add noise_detail field moment {central, raw} (relevant for heavy_tailed). Add a noise value symmetric_location (symmetric about the location, moments may not exist), ordered heavy_tailed ⊑ symmetric_location only under symmetry, with no general order. Extend noise_detail.variance with action_dependent (parameter noise, variance a^T Σ a), placed between homoscedastic and heteroscedastic_unknown. Other constants (Fisher-information KL bounds, sub-Weibull exponents, unknown range [m,M]) go in result conditions. Re-extract heavy-tailed settings.

Examples: `Arm distributions are light-tailed (sub-exponential) and continuous with strictly increasing CDF (C1)` (a2019concentration); `Light-tailed (sub-exponential) distribution, continuous with strictly increasing CDF` (a2019concentration); `Raw p-th moment bound E|X|^p < u with p in (1,2] (eps_m = p-1); estimator uses p, u and delta for truncation` (a2019concentration); `Continuous distribution with strictly increasing CDF (C1)` (a2019concentration)

### Linear/parametric model details (per-arm parameters, misspecification, geometry and norms, links, known structure sets) (311 items, 82 papers)

Add action_set field parameter_sharing {shared, per_arm_disjoint, hybrid}. per_arm_disjoint is not ordered with shared; it is a different model. Misspecification uses reward_model.kind = misspecified with eps as a variable. Norms, shapes, links (logistic) and parameter sets use the existing action_set and generalized_linear fields plus conditions. Re-extract linear contextual papers.

Examples: `mean rewards bounded |<x,theta*>| <= G (G may exceed 1)` (abbasiyadkori2012online); `mean rewards bounded |<x,theta*>| <= G` (abbasiyadkori2012online); `mean rewards x^T theta_global in [0,1]` (afsharrad2025multi); `losses bounded |<l_t,x>| <= M (M not necessarily 1)` (agarwal2017price)

### Feedback-graph and partial-monitoring structure (graph timing, probabilistic edges, weighted/noisy side observations, cross-learning across contexts, game matrices) (372 items, 64 papers)

Add feedback value cross_learning: playing an arm reveals its reward under other contexts. Order full_information ⊑ cross_learning ⊑ bandit, valid only when contexts are present. Extend feedback_graph.generation with random_edge_probabilities. Extend feedback_graph.knowledge with revealed_before_action, placed between known_in_advance and revealed_after_action. Add field side_observation_quality {exact, noisy_or_weighted}, with exact ⊑ noisy_or_weighted. Partial-monitoring game specifics (known L and H matrices, non-degeneracy) are result conditions. Re-extract graph-feedback settings.

Examples: `for the tuned bound, the learner knows upper bounds m_t on mas(G_t) (their sum) to set eta` (alon2013from); `for the tuned bound, the learner knows upper bounds alpha_t on alpha(G_t) (their sum) to set eta` (alon2013from); `graphs drawn i.i.d. each round from Erdos-Renyi model with arc density r; for the tuned bound the learner knows r` (alon2013from); `the time-t graph G_t is disclosed at the beginning of round t, before prediction (not the whole sequence in advance)` (alon2013from)

### Dueling / preference / subset-choice specifics (transitivity, STI, weak/strong regret, winners, battling) (317 items, 54 papers)

Extend node parameter preference: model gains total_order and sst_and_sti (utility_link ⊑ sst_and_sti ⊑ strong_stochastic_transitivity ⊑ total_order ⊑ general), plus condorcet_exists as a separate field; add field regret_type {average, weak, strong, binary_weak, binary_strong} with no order; winner gains weighted_borda. Feedback for subset play (battling, winner-of-subset, top-m ranking) uses comparison=subset plus a variable for the subset size. Re-extract dueling settings.

Examples: `Existence of a Condorcet winner a* with p_{a*,j} > 1/2 for all j; Delta_j := p_{a*,j} - 1/2; regret per step (Delta_{i_t` (agarwal2022asymptotically); `Stochastic triangle inequality (STI): eps_{i,k} <= eps_{i,j} + eps_{j,k} for b_i >= b_j >= b_k` (agarwal2022batched); `Stochastic triangle inequality (STI) holds` (agarwal2022batched); `Arbitrary (possibly infinite) arm set X with structure exploited by a black-box MAB algorithm (SBM)` (ailon2014reducing)

### Model selection, corralling, meta-learning, multi-task and shared representations (259 items, 48 papers)

Add extras multi_task: several tasks played sequentially or in parallel, with regret summed over tasks and a task-distribution or shared-representation variable. Add reward_model field selection {single_class, nested_classes_unknown_index, base_algorithm_corralling}, with single_class ⊑ nested_classes_unknown_index. The learner's hyper-prior knowledge goes in learner_knows.prior. Re-extract the affected papers.

Examples: `Model selection over M black-box base bandit algorithms; regret compared to the best base algorithm` (abbasiyadkori2020regret); `The learner knows a high-probability (possibly data-dependent) upper bound U on the regret of the optimal base algorithm` (abbasiyadkori2020regret); `Model selection over log(T) epsilon-greedy base algorithms with exploration rates 2^i/t` (abbasiyadkori2020regret); `Model selection over M RL base algorithms / candidate feature maps for a linear MDP` (abbasiyadkori2020regret)

### Extra, paid, budgeted or auxiliary observations (free peeks, query budgets, label-efficient, hints/predictions, surrogate signals, conversational queries) (206 items, 43 papers)

Add feedback value free_or_paid_observations: the learner may observe additional arms (free, at a cost, or under a budget), with bandit ⊑ free_or_paid_observations ⊑ full_information. Add extras loss_predictions (hints / optimistic predictors; the prediction error is a declared variable). Add extras auxiliary_signals (surrogate/proxy/intermediate observations, conversational key-terms). Observation budgets and costs are variables. Re-extract the affected papers.

Examples: `user-triggered supervision: on uncontrolled rounds the learner observes r_t=0 and the user's best action abar(x_t), with` (agarwal2023leveraging); `revealing action a_0 always reveals abar(x) (Assumption 1)` (agarwal2023leveraging); `revealing action a_0 (Assumption 1)` (agarwal2023leveraging); `user-triggered supervision with surrogate loss Delta and fidelity constraint` (agarwal2023leveraging)

### Metric/X-armed structure (dissimilarities, hierarchical partitions, local smoothness at the optimum, near-optimality dimension, unimodality graphs) (154 items, 37 papers)

Add function_class value local_smoothness_at_optimum (weak Lipschitz w.r.t. a semi-metric or partition), with lipschitz ⊑ local_smoothness_at_optimum under the order_rule. Near-optimality dimension and covering dimension are variables, and a given partition tree goes in learner_knows. Re-extract lipschitz_metric settings.

Examples: `Arm space is a general measurable space with a dissimilarity function (not necessarily a metric) and a given hierarchica` (azar2014online); `Local smoothness only w.r.t. the maximizer: f* - f(x) <= l(x*, x) (weaker than Lipschitz)` (azar2014online); `Complexity measured by near-optimality dimension d_near with constant C_cov` (azar2014online); `The learner knows the smoothness parameters nu_1 and rho of the covering tree` (azar2014online)

### Risk / distributional functional objectives (CVaR, quantile, mean-variance, median, max, general functional of the arm law) (221 items, 34 papers)

Add node parameter target_functional {field kind: mean (default, unspecified_means: mean), quantile, cvar, mean_variance, sharpe, expectile_or_elicitable, max_or_support_end, lipschitz_functional_of_cdf, other}; no order between kinds; level (alpha, rho) as variables; learner_knows the level. Every result now filed under quantity=other with a risk functional should be re-extracted; regret then measured in that functional.

Examples: `Best arm is defined as the arm with lowest CVaR at a fixed level alpha (risk-aware objective), not highest mean` (a2019concentration); `The learner knows the CVaR level alpha` (a2019concentration); `Target is CVaR at level alpha, not the mean` (a2019concentration); `Target is CVaR at level alpha, not the mean` (a2019concentration)

### Online/zeroth-order optimisation details (DR-submodular and up-concave, saddle points, biased gradient oracles, query points off the played point, unbounded domains) (293 items, 32 papers)

Add function_class values dr_submodular_or_up_concave (alpha-regret results) and convex_concave_saddle. Add a feedback order note: zeroth-order queries at points other than the played point are multi_point/two_point with a caveat. Biased or noisy gradient oracles use first_order with conditions. Re-extract BCO/OCO settings with these features.

Examples: `Losses also assumed L-Lipschitz (BGD base algorithm is also run)` (agarwal2016corralling); `Observed loss phi_t in [0,1] is a noisy evaluation with E[phi_t] = f_t(y_t), f_t G-Lipschitz linear` (agarwal2022diversified); `Bounded gradient norm G on the compact set Theta` (akhavan2020exploiting); `Bounded gradient norm G on Theta` (akhavan2020exploiting)

### Differential privacy and replicability constraints (180 items, 31 papers)

Replace the coarse extras.differential_privacy with node parameter privacy {model: not_applicable, central_global, joint, shuffle, local, replicable; protected: rewards, contexts_and_rewards, full_transcript, messages; type: pure, approximate, zcdp}. Order: central_global ⊑ joint is not valid in general, so no order except pure ⊑ approximate (a pure-DP algorithm is approximate-DP). Privacy levels eps/delta/rho stay variables; learner_knows them. Re-extract every setting with extras.differential_privacy.

Examples: `epsilon-differential privacy w.r.t. change of an entire loss vector (sequence of predictions must be private)` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price)

### Delayed feedback details (censoring, delay knowledge, reward-coupled delays, composite/anonymous, capacity-limited tracking) (217 items, 31 papers)

Extend node parameter delay with fields: knowledge {known_at_play (clairvoyant), revealed_on_arrival, never_revealed} ordered known_at_play ⊑ revealed_on_arrival ⊑ never_revealed; observability {full, windowed_censored, composite_anonymous, evolving}; coupling {independent, arm_dependent, reward_dependent} ordered independent ⊑ arm_dependent ⊑ reward_dependent; tracking_capacity as a variable C_cap. Re-extract settings with extras.delayed_feedback.

Examples: `an intermediate state S_t ~ P(.|A_t) from a finite state space is observed immediately; the loss is delivered after a fi` (baghi2026pooling); `state-sufficiency: E[X_t | past, A_t, S_t] = theta_t(S_t), with oblivious state-loss means theta_t in [0,1]^|S| and stoc` (baghi2026pooling); `an intermediate state S_t is observed immediately; loss delivered after fixed delay d` (baghi2026pooling); `Evolving observations: at each round the learner observes feedback losses ell_tau^(t) in [0,1]^K for all past rounds tau` (baron2024stochastic)

### Corruption and contamination specifics (strong adversary seeing action/realization, feedback-bit corruption, Huber probability, imprecise models) (99 items, 31 papers)

Extend corruption.adversary with strong_after_action, which sees the action and the realised reward before corrupting. Order: oblivious ⊑ adaptive ⊑ strong_after_action. Add corruption.target value binary_feedback. Budget normalisations (sum of sup-norms, per-node or per-arm budgets) are result conditions. Re-extract corrupted settings whose adversary was left unspecified.

Examples: `Played action is perturbed by unobserved adversarial vectors xi_t with norm <= eps` (agarwal2022diversified); `Persistent adversarial oracle error bounded by xi, xi known to the algorithm` (aggarwal2026adversarial); `corruption probability epsilon in (0,1/2) is known to the learner` (agrawal2023crimed); `corruption distributions are arbitrary (possibly unbounded) and may vary over time` (agrawal2023crimed)

### Batching, streaming, memory and communication-bounded learners (93 items, 27 papers)

Add node parameter batched.grid {static, adaptive}, with static ⊑ adaptive. Passes over a stream (P_pass) and memory bits are variables under extras.streaming_bounded_memory. Re-extract settings with extras.batched.

Examples: `Batch sizes may be chosen adaptively; the learner uses at most B (= M_batch) adaptive rounds and knows B` (agarwal2022batched); `Batch sizes may be chosen adaptively; at most a given number of batches` (agarwal2022batched); `Algorithm is allowed B_pass passes over the (possibly adversarially ordered, order may change across passes) stream of a` (agarwal2022sharp); `Arm can be played only while in memory; discarded arms are forgotten until re-encountered in a later pass` (agarwal2022sharp)

### Nonparametric contextual bandits (rewards smooth/Hölder in the context, neural/NTK reward models) (134 items, 24 papers)

Add reward_model.kind value nonparametric_smooth_in_context: rewards are (beta,L)-Hölder or Lipschitz in the context, with beta_holder as a variable, ordered realizable_general_class ⊑ nonparametric_smooth_in_context. Margin and density conditions are result conditions; neural_ntk already exists. Re-extract contextual papers that left this unmapped.

Examples: `Unknown fixed function f(x,c) with contexts c_t in [0,1]^p chosen by an adaptive adversary` (akhavan2024conversion); `f is gamma-Hölder in the context with constant L (class F_gamma(L)); f(.,c) belongs to a generic class F' for which an i` (akhavan2024conversion); `contextual regret compares to per-context minimizer` (akhavan2024conversion); `Unknown fixed f(x,c), gamma-Hölder in the context c in [0,1]^p with constant L; contexts chosen by adaptive adversary` (akhavan2024conversion)

### Multinomial-logit choice feedback for assortments (133 items, 18 papers)

Add feedback value choice ('one item chosen from the offered set, or none'). It is a special case of partial_monitoring, with no order to semi_bandit. Add combinatorial.reward value mnl_revenue. Record utilities (linear/contextual) via action_space and kappa as a variable; learner_knows revenues. Re-extract assortment papers.

Examples: `Multinomial logit (MNL) choice model: offering assortment S, the customer purchases product i in S with probability v_i/` (agrawal2017bandit); `Expected revenue R(S,v) = sum_{i in S} r_i v_i/(1+sum_{j in S} v_j) is nonlinear in the parameters` (agrawal2017bandit); `No-purchase most likely: v_i <= v_0 = 1 for all products (Assumption 4.1)` (agrawal2017bandit); `Feasible assortments given by totally unimodular constraints A x(S) <= b and downward closed` (agrawal2017bandit)

### Cost-aware sampling (arm-dependent query costs, multi-fidelity evaluations, sampling-cost objectives, random-latency/ratio objectives) (103 items, 15 papers)

Add node parameter query_cost {kind: unit, arm_dependent_known, random_unknown, multi_fidelity; budget_type: horizon, total_cost}. Fidelity bias zeta and cost lambda are variables. Order: unit ⊑ arm_dependent_known ⊑ random_unknown. Re-extract settings marked extras.budgeted_exploration.

Examples: `known per-round crowd costs c_i` (abraham2013adaptive); `flow sampling cost c per unit time; learner chooses an adaptive stopping time tau and pays c*tau` (adusumilli2022sample); `learner chooses adaptive stopping time bounded by T` (adusumilli2022sample); `Each decision is a (group, deadline) pair from [K] x a finite deadline set of size L; task occupies random completion ti` (ayc2020group)

### Limits on arm use (blocking/cool-down, pull-at-most-once/B times, no-repetition, monotone arm sequences, shareable capacities) (38 items, 7 papers)

Add extras arm_pull_limits: deterministic per-arm limits on how often or when an arm may be played (blocking delays, at most B pulls, no repetition, monotone sequences, capacities). Delays and capacities are variables. Unlike rested or rotting dynamics, these do not make rewards state-dependent. Re-extract blocking-bandit and capacity papers.

Examples: `no-repetition constraint: an item cannot be recommended twice to the same user` (ariu2020regret); `random user arrivals among m users with no-repetition constraint; regime m >= n, T = o(mn)` (ariu2020regret); `random user arrivals with no-repetition constraint; regime m >= n, T = o(mn)` (ariu2020regret); `Each arm i is deterministically blocked (unavailable) for D_i - 1 rounds after each play; the set of available arms depe` (basu2019blocking)

## Result field

### Context/action-set generation and regularity conditions (diversity, eigenvalue, margin, smoothed contexts, i.i.d. action sets, gap assumptions) (216 items, 72 papers)

These are conditions under which a result holds (minimum eigenvalue, margin exponent, diversity, symmetric densities, gap bounds, smoothed perturbations): put them in the result's conditions. The generation process itself is already context = stochastic/adversarial plus action_set.time_varying.

Examples: `mu_{*,t} must be constant over time (i.i.d. contexts)` (abbasiyadkori2020regret); `gaps Delta_i(t) <= 1 assumed` (agrawal2013lints); `contexts x_t(a) in [0,1]^d for each of K arms drawn i.i.d. jointly with rewards/consumptions from an unknown distributio` (agrawal2015linear); `contexts i.i.d. from a specific distribution P_K` (akhavan2024conversion)

### Regret and comparator notions (policy/smoothed/lenient/satisficing/KL-regularised/sampling regret, stopping-time regret, competitive ratio, information-theoretic quantities) (130 items, 37 papers)

These describe the guarantee, not the problem. Use the result's quantity, comparator and conditions (add quantity values satisficing_regret and smoothed_regret only if they recur). The setting is unchanged.

Examples: `objective trades off expected total cost sum_t c_{i_t} against the error rate, compared with omniscient benchmarks (best` (abraham2013adaptive); `objective is minimax (max over means) expected regret = simple-regret-type loss of the implemented arm plus sampling cos` (adusumilli2022sample); `minimax (over means) simple regret criterion` (adusumilli2022sample); `policy regret against constant action sequences (counterfactual losses under adversary's reaction)` (arora2012online)

## Already expressible

### Pure-exploration answer types (thresholds, good-arm, clustering, ranking, maximin, transductive, unverifiable/anytime, PAC variants) (597 items, 117 papers)

Guidance: thresholding, general_identification (Pareto/ranking/clustering/maximin/partition/transductive Z ≠ X), mean_estimation and top_m_identification cover the answer; the error criterion (epsilon-good, FDR/FWER, unverifiable or anytime, cost-weighted misclassification) goes in the result's quantity/conditions, and known thresholds go in learner_knows.

Examples: `Each sample is a categorical observation over n options; goal is to identify the mode (most probable option) of the sing` (abraham2013adaptive); `Arms (crowds) yield categorical samples over n options; all crowds share the same unique mode x*, which must be output a` (abraham2013adaptive); `Goal is estimating the minimum value min_x f(x) (not the minimizer)` (akhavan2020exploiting); `Objective: query complexity = expected first round at which a query hits a maximum of f* (the algorithm need not identif` (amin2011bandits)

### Auctions, posted prices, bilateral trade and market mechanisms (766 items, 72 papers)

Guidance: map to the underlying structure (posted price on [0,1] = continuum_other/lipschitz_metric; win-only, sale-only or one/two-bit trade outcomes = partial_monitoring; transparent HOB = graph_feedback or full_information), budget balance to constraints, and the application model (GFT, first/second price, valuation model) to result conditions.

Examples: `Repeated second-price auction: bid B_t in [0,1]; utility (V_t - M_t)1{B_t >= M_t}; i.i.d. values V_t in [0,1] with mean ` (achddou2020efficient); `The value V_t is observed only when the auction is won (action-dependent censoring)` (achddou2020efficient); `Repeated second-price auction with i.i.d. values in [0,1] and i.i.d. opponent maximal bids with cdf F` (achddou2020efficient); `The value V_t is observed only when the auction is won (action-dependent censoring)` (achddou2020efficient)

### What the learner knows (constants, thresholds, model structure, priors, scale bounds) (109 items, 63 papers)

Guidance: any known constant, threshold, structure or prior goes in learner_knows (open vocabulary over variables.yaml plus named items); declare a symbol only if the registry has none, and never list it as unmapped.

Examples: `sparsity level ||theta*||_0 not known to the learner` (abbasiyadkori2012online); `learner knows the number of options n` (abraham2013adaptive); `arm variances sigma_1^2, sigma_0^2 are known; learner knows the cost c` (adusumilli2022sample); `learner knows score functions, information matrices I_a and mean derivatives (sigma_a^2 = mu_dot' I^-1 mu_dot) and the c` (adusumilli2022sample)

### Non-stationarity measures (path length, significant shifts, RKHS/TV variation, drift speed, GP-evolving functions, periodic, change-point structure) (198 items, 43 papers)

Guidance: switching → nonstationary_switching with S_T (including significant-shift counts as a declared variable); budgets of any norm (l2 path length, RKHS norm, total variation of distributions, per-round drift speed) → nonstationary_drifting with a declared variable naming the norm; whether the learner knows it → learner_knows.

Examples: `S here is the number of epochs of the comparator sequence (S-1 switches)` (avner2012decoupling); `the instance has drift E_2 = sum_t ||c_t - m_t||_inf^2 <= E (drift budget)` (baghi2026pooling); `Reward function evolves by Markov model f_{t+1} = sqrt(1-eps) f_t + sqrt(eps) g_{t+1}, g_t i.i.d. GP(0,k); eps is the va` (bogunovic2016time); `The learner knows the variation rate eps and kernel hyperparameters` (bogunovic2016time)

### Expert advice, policy classes and online classification structure (213 items, 37 papers)

Use extras.expert_advice with comparator best_expert/best_policy. N_exp, VC or Natarajan dimension are variables, and limited_advice covers querying M experts. Multiclass 0/1 or margin structure goes in conditions.

Examples: `finite policy class Pi of size N_exp; comparator is the solution of the constrained problem` (agarwal2023leveraging); `finite policy class Pi accessed through an arg-max oracle (AMO); comparator is best mixed policy over Pi feasible in exp` (agrawal2015efficient); `finite policy class Pi accessed through an arg-max oracle; comparator is best mixed policy over Pi` (agrawal2015efficient); `experts give arbitrary probability-vector advice xi_t^e in the simplex each round` (allenzhu2018make)

### Low-rank, matrix/tensor and latent-cluster structure (users × items, rank-r parameters, unknown clusters) (198 items, 32 papers)

Use action_set.parameter_structure = low_rank or clustered, with rank r_rank and the cluster count as variables. Incoherence, condition number and cluster separation go in conditions. A user population sampled each round is context = stochastic_contexts.

Examples: `Each 'arm' k is a d_k x d_k matrix of unknown rank r_k; pulling arm k reveals a noisy observation of a uniformly random ` (andrea2026active); `Objective is the estimation loss L_n^p = (sum_k ||M_hat^k - M^k||_F^{2p})^{1/p} after a fixed budget n of samples` (andrea2026active); `Learner knows the dimensions d_k and the bound A on entries and observations, but not ranks or noise variance` (andrea2026active); `Loss parameter p chosen by the learner` (andrea2026active)

### Kernel / GP specifics (GP sample paths, NTK and other named kernels, domain, eigendecay, misspecified RKHS) (151 items, 28 papers)

Use kernel_rkhs with kernel.family (NTK and gamma-exponential are family = other). A GP sample path is instance_assumptions.bayesian_prior. The domain (sphere, [0,r]^d), eigendecay, k(x,x) <= 1 and RKHS misspecification eps (reward_model.kind = misspecified) go in conditions.

Examples: `true function f* is only epsilon-uniformly approximated (sup norm) by an RKHS function of norm <= B` (bogunovic2021misspecified); `true function f* is only epsilon-uniformly approximated (sup norm) by an RKHS function of norm <= B; epsilon unknown to ` (bogunovic2021misspecified); `action sets D_t subset of D drawn i.i.d. each round` (bogunovic2021misspecified); `f* : D -> [0,1], epsilon-uniformly approximated by RKHS function of norm <= B; epsilon unknown, assumed in [0,1)` (bogunovic2021misspecified)

### Offline data, warm starts, logged/confounded data and transfer bounds (128 items, 26 papers)

Guidance (v0.5): offline data or warm starts go in conditions and make the setting its own via a variable such as n_offline. Purely offline policy learning or evaluation, with no interaction, is in_scope=false.

Examples: `learner has access to tau_1 offline samples from the same instance, collected by an unknown adaptive offline policy; tau` (agrawal2023optimal); `delta-correctness is with respect to the joint distribution of offline and online data; sample complexity counts online ` (agrawal2023optimal); `conditional delta-correctness (given each offline history) variant discussed in Appendix B (Theorem B.2, Bernoulli arms)` (agrawal2023optimal); `learner has access to offline samples N^o_a(T) collected by an independent adaptive policy; regret counts online pulls o` (agrawal2023optimal)

### Computational oracles (ERM/argmax/regression, projection, membership, LO oracles, approximate posteriors, policy parametrisation) (63 items, 25 papers)

Existing guidance already applies: oracles are algorithm requirements and belong in the algorithm's conditions/tuning (or action_set.access), never in the setting.

Examples: `algorithm can efficiently construct the smallest Euclidean ball containing the compact convex set X` (agarwal2011stochastic); `policy class accessed only through a cost-sensitive classification (argmax) oracle` (agarwal2014taming); `Learner has access to an offline ERM oracle over the policy class` (agarwal2016corralling); `Learner has access to an offline ERM oracle over the policy class` (agarwal2016corralling)

### Arm availability and arm generation (sleeping/available sets, reservoirs, many-armed regimes) (99 items, 23 papers)

Use extras.sleeping_arms / time_varying_action_sets with action_set.time_varying (i.i.d., oblivious, adaptive), and extras.infinitely_many_arms for reservoirs. The reservoir regularity beta and the fraction of good arms are variables; per-action regret is a comparator/quantity.

Examples: `Decision sets are nested (contracting) K_{t+1} subset of K_t; regret measured against the final set K_T` (agarwal2022diversified); `Decision sets are nested (contracting); regret against the final set K_T` (agarwal2022diversified); `large reservoir of n items whose success rates are drawn i.i.d. from unknown absolutely continuous distribution zeta on ` (ariu2020regret); `satisficing regret relative to the (1-epsilon)-quantile mu_{1-epsilon}` (ariu2020regret)

### Click models and ranked lists (102 items, 22 papers)

Guidance: ranked lists are combinatorial with family=ordered_list and reward=click_model (feedback=cascade for cascade clicks); name the click model (DCM, PBM, generic examination assumptions) and known examination probabilities in conditions/learner_knows.

Examples: `Learner outputs a score vector in R^m over m documents (side information X_t in R^{m x d}); only relevances of the top-k` (chaudhuri2016online); `Comparator is the best linear scoring function w with ||w||_2 <= U; learner knows U and R_D (feature norm bound)` (chaudhuri2016online); `Relevance vectors in {0,...,n}^m, chosen by oblivious adversary` (chaudhuri2016online); `Learner outputs score vectors ranking m documents; only relevance of the top-ranked document is revealed; loss is any ND` (chaudhuri2016online)

### Causal bandits (interventions, known/unknown graphs, observed node values) (166 items, 21 papers)

Use extras.causal (v0.5 kept causal structure coarse). Graph knowledge, observed variables and identifiability gaps go in learner_knows and conditions.

Examples: `Arms are hard interventions do(W=w) on subsets of n discrete variables with domain size K_dom; (K_dom+1)^n arms` (elahi2024partial); `Unknown semi-Markovian causal graph with latent confounders; all observed variables are observed after each intervention` (elahi2024partial); `Interventional faithfulness and gap assumptions (epsilon for ancestrality, gamma for latent confounders, eta lower bound` (elahi2024partial); `The learner knows the gap constants epsilon, gamma, eta, the max degree bound d_max, the number of nodes n and domain si` (elahi2024partial)

### Switching and movement costs (40 items, 13 papers)

Use extras.switching_cost with the per-switch cost (or a metric movement cost) as a variable, and learner_knows for whether it is known.

Examples: `regret includes a switching cost lambda per switch (lambda_sw); the learner knows lambda_sw` (amir2022better); `regret includes a switching cost lambda per switch (lambda_sw); the learner knows lambda_sw` (amir2022better); `unit switching cost (lambda = 1) added to the regret` (amir2022better); `unit switching cost (lambda = 1) added to the regret` (amir2022better)

## Out of scope

### State-dependent reward dynamics, MDPs/RL, queueing, control, rested/rising/rotting and history-dependent arms (642 items, 107 papers)

Covered by the scope rules (environment markovian; extras restless/rotting_or_rising/mortal_arms) and extractor guidance on MDP/RL: state-dependent dynamics and planning are close to RL and are cut. Extractor should set those values so resolve.py drops them.

Examples: `Recommender shows a menu of k out of n items (K=n, m=k); the agent picks one item with probability proportional to prefe` (agarwal2022diversified); `Agent choice probabilities depend on its memory vector of past choices through a preference model` (agarwal2022diversified); `Learner knows the preference model exactly (univariate linear score functions)` (agarwal2022diversified); `n arms are controlled Markov chains with finite state spaces and unknown transition matrices; m of n arms activated each` (akbarzadeh2022learning)

### Multi-agent, federated, decentralized, multiplayer-collision and matching-market settings (560 items, 71 papers)

Covered by scope rule extras {multi_player_collision, multi_agent_cooperative, federated}: multi-agent/distributed learning is cut (v0.5 user decision). Extractor should set those extras so resolve.py drops them; no new vocabulary.

Examples: `N agents on an undirected connected network communicate only with neighbours via a doubly stochastic matrix W; each comm` (afsharrad2025multi); `each agent observes local reward with its own parameter theta^i; regret measured w.r.t. the global (average) parameter` (afsharrad2025multi); `the learner knows the network's second largest eigenvalue magnitude |lambda_2| and the weight matrix W` (afsharrad2025multi); `N agents communicate through a central server; communication cost (number of communicated real numbers / bits) is a seco` (amani2022distributed)

### Games, equilibria, Stackelberg/persuasion, principal-agent, strategic agents and attacks on learners (344 items, 55 papers)

Equilibrium objectives, two-sided control of a game, mechanism design for strategic agents and guarantees for an attacker are excluded by extractor_out_of_scope. Keep the single-learner adversarial_adaptive regret results (already allowed) and extras.strategic_arms for strategic arms.

Examples: `arms are entries of an m x n payoff matrix; learner picks mixed strategies (x_t, y_t) for both players and observes nois` (abe2026thompson); `performance measured by cumulative duality gap sum_t Gap(x_t,y_t)` (abe2026thompson); `payoff matrix assumed to have a unique Nash equilibrium` (abe2026thompson); `arms are entries of a payoff matrix; learner controls both players' mixed strategies` (abe2026thompson)

### Multi-objective / vector-valued rewards (Pareto, lexicographic, hypervolume) (192 items, 33 papers)

Multi-objective rewards were cut in v0.5; the extractor should set in_scope = false. The exception is a known scalarisation into one reward, which should map to the scalar problem with the scalariser in the conditions.

Examples: `multiple objectives (vector-valued rewards), Pareto regret / effective Pareto fairness` (ann2026blessings); `no distributional assumptions on the contexts` (ann2026blessings); `multiple good arms condition inducing implicit exploration` (ann2026blessings); `Each arm returns a D-dimensional reward vector with independent Bernoulli coordinates; regret is Pareto regret (distance` (balef2023piecewise)

### Quantum oracle access (86 items, 18 papers)

Quantum oracles were cut in v0.5 (extractor_out_of_scope); the extractor should set in_scope = false.

Examples: `Arms are two-qubit quantum states measured with a fixed known Witness Basis Measurement; the target quantity S_E(rho_i) ` (bharati2024batch); `Promise that exactly one arm lies below the threshold zeta = 0; the learner knows the threshold` (bharati2024batch); `The confidence width uses the sub-Gaussian scale sigma of the samples` (bharati2024batch); `Arms are two-qubit quantum states measured with a Witness Basis Measurement; target is a quadratic functional S_E(rho_i)` (bharati2024batch)

### Non-interactive estimation, inference and asymptotic diffusion analyses (60 items, 13 papers)

These are not interactive bandit guarantees: passive estimation of an optimal value, off-policy evaluation, CLT and stability of pull counts, diffusion limits, confidence boundaries and Gittins-index properties. Set in_scope=false, or file them as result conditions only when a regret result is also given.

Examples: `continuous time: signals dx_a = mu_a pi_a dt + sigma_a sqrt(pi_a) dW_a` (adusumilli2022sample); `continuous-time diffusion limit with fixed experiment duration tau=1 (corresponds to n observations)` (adusumilli2022sample); `per-observation sampling cost C = c/n^{3/2}, small-cost asymptotics n -> infinity` (adusumilli2022sample); `local alternatives theta_0 + h/sqrt(n) with equal reference means; regret scaled by sqrt(n)` (adusumilli2022sample)
