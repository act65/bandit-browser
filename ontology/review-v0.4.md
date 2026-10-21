# Ontology review after batch 1 (ontology v0.4)

Input: the 3731 `unmapped` items in 558 extractions, grouped into themes by one LLM pass with the ontology in context (`pipeline/review_unmapped.py`, opus). **Status: proposed, not applied.** 3729 of 3731 items were assigned to a theme.

| decision | themes | items | papers |
|---|---|---|---|
| ontology change | 26 | 2497 | 472 |
| result field | 3 | 295 | 146 |
| already expressible | 7 | 742 | 275 |
| out of scope | 4 | 195 | 45 |

## Ontology change

### Learner knowledge of parameters outside the fixed vocabulary (198 items, 135 papers)

Make the learner_knows values open over the variables in variables.yaml (any declared symbol, e.g. B_rkhs, R_noise, M_range, beta_holder, tau_delay, d_max, Lambda_var), instead of a fixed list. Keep the order rule unchanged. Add the missing symbols to variables.yaml. Re-extract only learner_knows fields.

Examples: `T_0 requires knowledge of bar L and a kernel constant` (akhavan2020exploiting); `Choice of K in eq. (Kvalue) uses L, p, d, tau's` (akhavan2024conversion); `Tuned bound requires upper bounds m_t on mas(G_t) (sum known to tune eta)` (alon2014nonstochastic); `Tuned bound requires upper bounds alpha_t on alpha(G_t)` (alon2014nonstochastic)

### Noise models: heteroscedastic/revealed variance, adversarial noise, moment variants (201 items, 103 papers)

Add node parameter noise_detail. Fields: variance {homoscedastic, heteroscedastic_unknown, heteroscedastic_revealed}, ordered homoscedastic ⊑ heteroscedastic_revealed ⊑ heteroscedastic_unknown; dependence {iid, martingale, adversarial_bounded_moment}; moment_type {raw, central} for heavy_tailed. Distribution-family regularity (KL conditions, canonical exponential families, symmetric densities) goes in conditions. Re-extract the variance-aware papers.

Examples: `Noise is a martingale difference sequence, conditionally R-subgaussian (R plays the role of sigma)` (abeille2017lints); `value oracle error |f_hat(S)-f(S)| <= xi for all S, known radius xi` (aggarwal2026adversarial); `Noise conditionally R-sub-Gaussian (R = sigma)` (agrawal2013lints); `Single fixed function f; noise xi_t, xi'_t is adversarial: not necessarily zero-mean or independent across steps, only i` (akhavan2020exploiting)

### Action-set and domain geometry (141 items, 80 papers)

Add these action_set.shape values: lp_ball (p as a variable), ellipsoid, permutahedron and product_of_spheres, all ⊑ arbitrary_compact. Add the field positioning {none, rB⊆K⊆RB, isotropic}, with r_K and R_K as variables. Metric-space arms ([0,1]^d with l∞, doubling metric) record the metric in conditions. Queries outside K are domain = improper. Re-extraction is only needed where the shape was left unspecified.

Examples: `domain is [0,1]` (agarwal2011stochastic); `Action set is the vertex set of the (symmetrized) n-permutahedron, i.e. all permutations of (1..n) centred; d = n` (ailon2013bandit); `Actions are vertices of Q_n = (2/(n-1)) * symmetrized permutahedron, so ||pi||_inf <= 1; d = n` (ailon2013bandit); `Functions attain minimum over R^d inside the unit ball; gradient bounded by G > 2 alpha on the unit ball` (akhavan2020exploiting)

### Feedback structures beyond the current values (censored, cascade, triggered, first-order, limited advice, multi-query) (150 items, 75 papers)

Add these feedback values: censored (a one-bit or win-only observation), cascade (observe until the first click), triggered_semi_bandit (probabilistically triggered arms), first_order (a gradient at the played point), multi_point (k > 2 evaluations, generalising two_point), limited_advice (observe M of N experts), and outcome_side_information (an observation richer than the reward, e.g. a causal or outcome label). Orders: semi_bandit ⊑ triggered_semi_bandit; semi_bandit ⊑ cascade; cascade ⊑ bandit is not valid in general, so leave it out; full_information ⊑ multi_point ⊑ two_point; full_information ⊑ first_order (a statement for OCO only); full_information ⊑ limited_advice ⊑ bandit (with experts); outcome_side_information ⊑ bandit; bandit ⊑ censored is invalid, so add no order and route censored through partial_monitoring. Settings that were mapped to partial_monitoring or full_information as the closest value need re-extraction.

Examples: `Allocate volume V^t <= V among K venues; reward at venue i is min(v_i, s_i) (censored feedback: only the consumed amount` (agarwal2010optimal); `Learner knows the volume bound V` (agarwal2010optimal); `Comparator: best fixed assignment of each unit v in {1..V} to a venue` (agarwal2010optimal); `Reward is concave piecewise linear in allocations` (agarwal2010optimal)

### Reward model classes: realizability, general function classes, neural/NTK, misspecification, model selection (172 items, 74 papers)

Add dimension reward_model (multi: false; refines structured_general for contextual and structured settings). Values: {agnostic_policy_class, realizable_finite_class, realizable_general_class, linear_feature, glm, neural_ntk, holder_in_context, graph_unimodal, tree_smooth, misspecified_class, nested_model_selection}. Orders: realizable_finite_class ⊑ realizable_general_class; linear_feature ⊑ glm; realizable_* ⊑ misspecified_class. Complexity measures (eluder dimension, N, VC) are variables. Re-extract the contextual papers.

Examples: `Link function continuously differentiable, k_mu-Lipschitz, derivative lower bounded by c_mu > 0` (abeille2017lints); `Realizability: a known finite regressor class F (|F| = N) contains f* with E[r(a)|x] = f*(x,a); policy class is induced ` (agarwal2012contextual); `Learner knows the context distribution D(x) (removable via sample-based constraint, sketched in Section 7)` (agarwal2012contextual); `Learner knows the regressor class F` (agarwal2012contextual)

### Combinatorial action structure and nonlinear set rewards (176 items, 72 papers)

Add node parameter combinatorial (applies when action_space = combinatorial). Fields: family {m_set, at_most_m, matroid, paths, matchings, permutations, ordered_list, power_set, arbitrary_subset, assignment, load_allocation}; reward {linear, nonlinear_lipschitz_monotone, submodular, mnl_choice, click_model}; base_arm_dependence {independent, correlated}. Orders: m_set ⊑ matroid ⊑ arbitrary_subset; linear ⊑ nonlinear_lipschitz_monotone; independent ⊑ correlated. The full-bandit variant is feedback = bandit. Re-extract the combinatorial papers.

Examples: `matroid constraint of rank k with independence oracle` (aggarwal2026adversarial); `objective f:2^U->[0,1] nonnegative submodular, possibly non-monotone` (aggarwal2026adversarial); `actions are independent sets of a rank-k matroid on n base elements` (aggarwal2026adversarial); `mean reward f(S) is nonnegative submodular (monotone or non-monotone); realized rewards need not be submodular` (aggarwal2026adversarial)

### Identification and estimation targets beyond best arm (127 items, 46 papers)

Add node parameter identification_target (applies to the pure-exploration objectives). Field target: {best_arm, top_m, threshold_set, closest_to_threshold, first_above_threshold, mode, pareto_set, ranking, general_answer (set-valued i*), odd_arm, mean_estimation, hypothesis_test, information_gain}. Field transductive: {no, yes}. Also add the objective values estimation and hypothesis_testing. Remap results that used other_pure_exploration.

Examples: `single source of i.i.d. samples from a categorical distribution over n options; goal is to identify the mode (most proba` (abraham2013adaptive); `unique_optimal_arm here means the correct answer is the unique most probable option` (abraham2013adaptive); `the stopping rule uses the number of options n` (abraham2013adaptive); `arms are k crowds, each a categorical response distribution over n options; all crowds share the same unique most probab` (abraham2013adaptive)

### Multi-agent, multiplayer, distributed, federated and matching-market settings (268 items, 45 papers)

Add node parameter multi_agent (applies when extras contains multi_player_collision, multi_agent_cooperative or federated, or the new value matching_market). Fields: coordination {centralized, decentralized_no_comm, communication_graph, server_star, gossip}; collision_model {not_applicable, zero_reward, shared, arm_preference_resolved}; sensing {none, collision_indicator, full_matching_observed}; heterogeneity {homogeneous, player_dependent_means}; population {fixed_known, fixed_unknown, dynamic_entry_exit}; regret_aggregation {per_agent, group_sum, average}; byzantine {none, bounded_fraction}. Add the extras value matching_market and the comparator values stable_matching and max_weight_assignment. Order on coordination: centralized ⊑ communication_graph ⊑ decentralized_no_comm. Papers that use these extras need re-extraction.

Examples: `two-sided matching market with N users and K arms (N <= K), both sides have unknown preferences (two-sided uncertainty)` (basu2025competing); `action is a matching; each matched pair (user, arm) observes noisy rewards on both sides` (basu2025competing); `regret is pessimal stable regret / binary stable regret (rounds where matching is not stable)` (basu2025competing); `central platform forms the matching from reported partial ranks` (basu2025competing)

### Constraints: budgets, long-term and per-round safety, conservative, fairness (134 items, 37 papers)

Add node parameter constraints (applies when extras contains knapsack_constraints, safety_constraints or fairness). Fields: kind {hard_budget, long_term_average, per_round_high_prob, anytime_cumulative, conservative_baseline, fairness_rate, fairness_individual}; cost_observation {known, bandit, full}; violation_metric {none, cumulative_violation}; slack {slater_known, slater_unknown, safe_action_known}. Re-extract the constrained papers.

Examples: `K arms, each with a context x_t(a) in [0,1]^m drawn i.i.d. per round (tuple of contexts, rewards and consumption vectors` (agrawal2015linear); `Reward r_t(a) in [0,1] and consumption vector v_t(a) in [0,1]^{d_res}; E[r|x]=mu_*^T x, E[v|x]=W_*^T x with mu_* in [0,1` (agrawal2015linear); `Budget B for each of d_res resources, given to the algorithm as input; no-op arm available; algorithm stops when budget ` (agrawal2015linear); `Regret measured against OPT, the value of the optimal static context-dependent policy satisfying constraints in expectat` (agrawal2015linear)

### Corruption and contamination models (64 items, 29 papers)

Extend node parameter corruption. Add field model {budget, huber_probability, tv_distance, per_arm_budget, self_bounding_gap_definition}, so that Huber contamination maps to stochastic_corrupted with model = huber_probability rather than to a budget C. Add field target {rewards, contexts, feedback_and_costs}. Add the adversary value omniscient_sees_action. Make corruption apply to more settings (partial monitoring, combinatorial). Re-extract the Huber papers.

Examples: `Huber contamination: each observation is replaced with probability epsilon in (0,1/2) by a sample from an arbitrary (pos` (agrawal2023crimed); `corruption probability epsilon is known to the learner` (agrawal2023crimed); `regret measured on uncorrupted rewards` (agrawal2023crimed); `Huber contamination: each observation is replaced with probability epsilon in (0,1/2) by a sample from an arbitrary (pos` (agrawal2023crimed)

### Missing function_class values (convex, Hölder, DR-submodular, unimodal, nonconvex) (67 items, 26 papers)

Add these function_class values: convex (implied by linear, quadratic with A ⪰ 0, and strongly_convex), holder_smooth (order beta), dr_submodular / up_concave, unimodal, nonconvex_general, weak_lipschitz. Add the implications strongly_convex ⇒ convex, linear ⇒ convex and lipschitz ⇒ weak_lipschitz. Allow function_class on finite or metric arms. Re-extract the BCO papers that left convexity unmapped.

Examples: `mean cost function f is convex (no 'convex' function_class value)` (agarwal2011stochastic); `mean cost function f is convex (no 'convex' function_class value)` (agarwal2011stochastic); `Hölder smoothness of order beta >= 2 with constant L, plus Lipschitz gradient with constant bar L (Assumption 2.2)` (akhavan2020exploiting); `Gradient bounded by G on the compact convex set Theta` (akhavan2020exploiting)

### Adversary models: bounded memory, policy regret, smoothed and hybrid adversaries (74 items, 25 papers)

Add the environment values adversarial_bounded_memory (loss depends on the last m actions; adversarial_oblivious ⊑ adversarial_bounded_memory ⊑ adversarial_adaptive) and adversarial_smoothed (each round's distribution is sigma-smooth; stochastic_iid ⊑ adversarial_smoothed ⊑ adversarial_oblivious). Add the quantity policy_regret. Hybrid stochastic/adversarial models with an observable attack go in conditions. Re-extract arora2012, cesabianchi2013, malik2022, cesabianchi2024 and similar papers.

Examples: `Adversary knows player's strategy but not its random coins` (ailon2013bandit); `Nonoblivious adversary: losses and feedback sets may depend on past actions, but regret is against a fixed action assumi` (alon2014nonstochastic); `performance measured by policy regret: loss compared with the loss the learner would have suffered had it played the com` (arora2012online); `holds for any action set X (construction is generic)` (arora2012online)

### State-dependent reward dynamics (rested/restless Markov, rising/rotting, recovering, blocking, converging sequences) (76 items, 24 papers)

Add node parameter reward_dynamics (applies to environment = markovian or to the extras rotting_or_rising, restless, mortal_arms). Fields: driver {own_pull_count, time_since_last_pull, all_arms_time, graph_triggered, history_externality}; shape {monotone_increasing_concave, monotone_decreasing, arbitrary, converging_deterministic}; state_observed {pulled_arm_only, all_arms}; comparator_policy {best_fixed_arm, optimal_adaptive_policy}. Add the extras value blocking_arms. Re-extract the rested/restless papers.

Examples: `Playing arm i blocks it (across all contexts) for d_i rounds; delays d_i known to learner` (basu2020contextual); `Learner may skip rounds` (basu2020contextual); `Arm blocking for d_i rounds` (basu2020contextual); `Non-stochastic (hyperparameter-optimisation) model: assigning budget n to arm x returns a deterministic loss l(x,n) conv` (feng2023lipschitz)

### Preference / dueling model and winner notion (98 items, 23 papers)

Add node parameter preference_model (applies when feedback = dueling). Fields: winner {condorcet, copeland, borda, von_neumann, utility_best}; model {general, strong_stochastic_transitivity, relaxed_transitivity, utility_link (BTL/logistic/probit), plackett_luce}; comparison_size {pair, subset_winner, subset_top_m}; regret_form {average_pair, weak, strong}. Orders: plackett_luce ⊑ utility_link ⊑ strong_stochastic_transitivity ⊑ relaxed_transitivity ⊑ general; utility_best ⊑ condorcet ⊑ copeland. Re-extract the dueling papers.

Examples: `linear link function: P[b_t=1]=(1+v_t-u_t)/2` (ailon2014reducing); `regret measured on the unobserved average utility (u_t+v_t)/2 of the two played arms` (ailon2014reducing); `generic arm set X; guarantee is relative to the regret of a black-box MAB algorithm (SBM)` (ailon2014reducing); `linear link function` (ailon2014reducing)

### Non-stationarity measures (51 items, 21 papers)

Add node parameter nonstationarity (applies to the nonstationary_* environments). Fields: measure {switches_global, changes_per_arm, variation_sup, path_length_l2, tv_distance, lipschitz_drift_rate, gauss_markov_rate, best_arm_switches_only}; known {yes, no}; spacing_assumption {none, min_segment_length}. Add the environment value nonstationary_lipschitz_drift and the order nonstationary_switching ⊑ nonstationary_drifting with the caveat that V_T ≤ S_T·range. Re-extract the papers that used V_T for path length.

Examples: `Number of breakpoints Upsilon_T is NOT known to the learner` (besson2019efficient); `Breakpoints must be sufficiently spaced relative to change magnitudes (Assumption 4 / 11)` (besson2019efficient); `Learner knows the total number of changepoints C_T (sum over arms of per-arm changepoints)` (besson2019efficient); `Changepoints on each arm must be sufficiently spaced (Assumption 11)` (besson2019efficient)

### Parameter structure: sparsity, low rank, clusters, multi-task and meta-learning (48 items, 18 papers)

Add the field action_set.parameter_structure {none, sparse, low_rank, clustered, shared_representation} (none ⊑ any of them for upper bounds only when s and r are at their trivial values). Add the extras value multi_task_or_meta for sequences or populations of tasks (fields: tasks_concurrent / sequential, switch_times_known). Re-extract the sparse and meta papers.

Examples: `n users each recommended one item per step; m items (arms); each item can be recommended to a given user at most once` (bresler2014latent); `k latent user types, each user's type uniform over k; users of same type share preference vector p_u in [0,1]^m; ratings` (bresler2014latent); `objective: expected number of likable items (p_ui > 1/2) recommended, compared with an oracle recommending all likable i` (bresler2014latent); `A1: |p_ui - 1/2| >= Delta for all u,i (no Delta-ambiguous items); A2: gamma-incoherence between types` (bresler2014latent)

### Limited adaptivity, memory/streaming and switching/movement costs (41 items, 17 papers)

Add the extras values streaming_bounded_memory (arm memory M and pass count B as variables) and rare_policy_updates. Add a field to batched: grid {static, adaptive}, ordered static ⊑ adaptive for lower bounds. Add a field to switching_cost: cost {unit, metric_movement}. Re-extract the streaming and batched papers.

Examples: `Arms arrive in an arbitrarily (adversarially) ordered read-only stream; algorithm may store at most M < K arms (identiti` (agarwal2022sharp); `At most B passes over the stream; learner knows B and M` (agarwal2022sharp); `Stream order may change adversarially across passes (upper bound holds in that case)` (agarwal2022sharp); `Arms arrive in a read-only stream (fixed order across passes in the lower bound); algorithm may store at most M arms and` (agarwal2022sharp)

### Risk-aware and non-mean arm functionals (37 items, 16 papers)

Add dimension arm_functional (multi: false) with values {mean, cvar, mean_variance, quantile, sharpe, distortion_risk, kl_regularized, cost_ratio, general_risk}, default mean. Add no orders. Allocation-level objectives (mixture-based or non-additive) also get the quantity other. Re-extract the risk-aware papers.

Examples: `mean-covariance (risk-aware) utility f(w)=w^T theta* - rho w^T Sigma* w with known risk-aversion rho>0` (du2021continuous); `mean-covariance utility with risk-aversion rho` (du2021continuous); `mean-covariance utility with known risk-aversion rho` (du2021continuous); `mean-covariance utility with risk-aversion rho` (du2021continuous)

### Feedback graph details: self-loops, directedness, random or weighted graphs (55 items, 13 papers)

Extend node parameter feedback_graph with these fields: self_loops {all, optional} (all ⊑ optional); directedness {undirected, directed} (undirected ⊑ directed); generation {arbitrary, erdos_renyi, correlated_with_losses}; edge_type {exact, noisy_weighted, unbiased_estimate}. A bipartite base-arm graph should use outcome_side_information instead. No re-extraction is needed for observability; the new fields default to unspecified.

Examples: `Feedback graphs are undirected (symmetric feedback system)` (alon2014nonstochastic); `Feedback graphs G_t drawn i.i.d. from directed Erdos-Renyi model with density r` (alon2014nonstochastic); `Graph may be directed or undirected` (alon2014nonstochastic); `Feedback graph G_t disclosed before each action (informed); chosen adaptively by a nonoblivious adversary` (alon2014nonstochastic)

### Partial monitoring game specification (54 items, 11 papers)

Add node parameter partial_monitoring (applies when feedback = partial_monitoring). Fields: observability {unspecified, locally_observable, point_locally_observable, globally_observable, any_game}, ordered locally ⊑ point_locally ⊑ globally ⊑ any_game; structure {finite_outcomes, linear}; game_known {known, unknown}; non_degenerate {yes, unspecified}. This follows the feedback_graph node. Re-extract the partial-monitoring papers.

Examples: `M = 2 outcomes; loss matrix L and feedback matrix H known to the learner` (antos2010toward); `opponent deterministic and oblivious (fixed outcome sequence)` (antos2010toward); `non-degeneracy condition: no degenerate revealing action` (antos2010toward); `minimax regret over outcome sequences, classified by geometry of non-dominated actions (separation condition)` (antos2010toward)

### Privacy and replicability (34 items, 11 papers)

Add node parameter privacy (applies when extras contains differential_privacy). Fields: model {central, local, joint, shuffle, federated}; type {pure, approximate}; neighbouring {reward, loss_vector, context_and_reward, preference}. Add the extras value replicability. Orders: local ⊑ central for upper bounds is not valid, so add none. Re-extract the DP papers.

Examples: `algorithm must be epsilon-differentially private w.r.t. change of one entire loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. one loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. one loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. one loss vector` (agarwal2017price)

### Multi-objective (vector-valued) rewards (39 items, 10 papers)

Add dimension reward_dimension {scalar, vector}, with the number of objectives d_obj as a variable and an optional aggregation {pareto, weighted_known, lexicographic, hypervolume, hidden_preference}. Pareto regret goes under quantity other. Re-extract the multi-objective papers.

Examples: `multi-objective: each arm yields a D-dimensional reward vector in [0,1]^D, observed in full` (cao2025provably); `N users each with a stochastic preference vector c_t^n (||c||_1<=1, R-sub-Gaussian entries); scalar overall reward g = c` (cao2025provably); `regret is sum over users of preference-weighted mean gaps against each user's per-round best available arm` (cao2025provably); `per-coordinate reward variance bounded below by sigma_r_down^2 > 0` (cao2025provably)

### Delay models (76 items, 9 papers)

Add node parameter delay (applies when extras contains delayed_feedback). Fields: generation {fixed, stochastic_iid, adversarial}; arm_dependent {no, yes}; loss_dependent {no, yes}; observability {exact, censored_window, partial_aggregate}; clairvoyant {no, yes}; capacity_limit {none, hard, expectation}. Orders: fixed ⊑ stochastic_iid ⊑ adversarial; no ⊑ yes for both dependence fields. Re-extract the delay papers.

Examples: `Full-information feedback revealed with constant delay tau` (ayc2020group); `Feedback available at round t only up to round fb[t] with t - fb[t] <= B for a known constant B (batch size / delay boun` (desautels2012parallelizing); `Feedback delay/batch bound t - fb[t] <= B known` (desautels2012parallelizing); `Random delays tau_t independent of the forecaster's predictions (i.i.d. for the corollary)` (joulani2013online)

### Causal bandit structure (59 items, 8 papers)

Add node parameter causal (applies when extras contains causal). Fields: graph {known, essential_graph, unknown}; interventions {atomic_hard, soft, generalized_soft}; observation {reward_only, parents, all_nodes}; conditionals_known {none, parent_interventional, all_but_target}; scm_class {discrete, linear, polynomial, neural, rkhs}. Re-extract the causal papers.

Examples: `Known causal graph without latent confounders; arms are interventions from POMISs of the projected graph with non-manipu` (elahi2026information); `Learner observes reward and all non-intervened variables after each intervention (richer than bandit feedback)` (elahi2026information); `Unknown parameter is the set of CPTs with independent Dirichlet priors (parameter independence)` (elahi2026information); `Contexts are ancestrally closed, observed before action; need not be exogenous (may carry information about theta)` (elahi2026information)

### Offline data, warm starts, predictions and prior recommendations (35 items, 8 papers)

Add the extras value side_data with fields: kind {offline_samples, warm_start_supervised, causal_bounds, loss_predictions, surrogate_outcomes, optimal_action_samples}; shift {none, bounded_bias, similar_distribution}. Add no order. A setting with side_data is a separate setting. Re-extract the hybrid offline-online papers.

Examples: `unknown parameters in a known box [alpha_min,alpha_max]x[beta_min,beta_max] known to learner` (bu2019online); `pre-existing offline data: n samples all at a single historical price p_hat` (bu2019online); `optimal price assumed interior to [l,u]` (bu2019online); `instance quantity delta = |p_hat - p*| unknown to learner` (bu2019online)

### Quantum oracle access (22 items, 7 papers)

Add the feedback value quantum_oracle (the reward distribution is accessed through a unitary oracle and its inverse, with a per-round query count). Add no order to the classical values, since quantum results do not transfer. Re-extract the quantum papers.

Examples: `Quantum access model: the agent queries the environment in superposition via unitary oracles O_e (preparing sum_y sqrt(n` (casal2020quantum); `Choosing the number of rounds n ≈ (pi/4) sqrt(1/p) requires knowing p = sum_x |<x|A|0>|^2 a_x` (casal2020quantum); `Feedback is a quantum zeroth-order oracle Q_{f_t} that can be queried in superposition, O(1) (4) queries per round after` (he2020quantum); `Feedback is a quantum zeroth-order oracle queried in superposition, O(1) queries per round` (he2020quantum)

## Result field

### Comparator and regret-quantity variants (143 items, 82 papers)

Extend the comparator vocabulary with best_feasible_policy, best_fixed_mixture, oracle_policy_known_model, comparator_sequence_path_length, best_in_class_interval, stopping_time_benchmark. Extend the quantities with local_regret, inferior_sampling_time and stationarity_regret. Comparator-adaptive and dynamic-regret path-length dependence go in the result's conditions.

Examples: `Same analysis also covers optimization error of averaged iterate` (akhavan2020exploiting); `Contextual regret compares to per-round minimizer of f(.,c_t)` (akhavan2024conversion); `experts give probability vectors over actions; comparator is the best expert's expected return` (auer2002exp3); `bound depends on the hardness h(j^T) = 1 + number of switches of the comparator sequence` (auer2002exp3)

### Computational oracles and algorithm-side requirements (83 items, 53 papers)

ERM, regression, argmax, approximation, projection, self-concordant-barrier and approximate-posterior requirements go in the result's algorithm_class or conditions. They do not change the statistical setting; action_set.access stays computational_only.

Examples: `X is compact convex and specified so that the smallest enclosing Euclidean ball can be computed efficiently` (agarwal2011stochastic); `Policy class Pi is accessed only via a cost-sensitive classification (argmax) oracle AMO` (agarwal2014taming); `Learner uses a mu-self-concordant barrier on K` (akhavan2024conversion); `Learner needs a nu-self-concordant barrier of X` (ba2021doubly)

### Approximation regret and competitive ratios (69 items, 31 papers)

Add the quantities alpha_regret (regret against alpha·OPT; the variable alpha and the oracle (alpha,beta) go in conditions) and competitive_ratio (multiplicative). These describe the guarantee, not the setting.

Examples: `guarantee is an approximation ratio relative to OPT` (aggarwal2026adversarial); `regret is alpha-regret against alpha*OPT` (aggarwal2026adversarial); `alpha-regret` (aggarwal2026adversarial); `alpha-regret against an optimal clairvoyant (offline) policy, alpha = d_max/(2 d_max - 1)` (basu2020contextual)

## Already expressible

### Reward/loss ranges, scales and loss-set restrictions (161 items, 97 papers)

Guidance: a rescaled bounded range ([0,B], [-C,C], [0,R]) is bounded_01 or bounded_pm1, with the scale as a variable in the result's conditions. Norm restrictions on losses (‖l‖₁ ≤ 1, |⟨x,l⟩| ≤ 1) use action_set.loss_set. Small-loss or variation restrictions are adversarial_restricted. Unit-variance Gaussian is gaussian_known_variance with sigma = 1 in conditions.

Examples: `Action norm bound is on the squared norm: ||x||^2 <= L` (abbasi2011oful); `Losses are g_t in [-1,0]^N (negative gains, i.e. gains in [0,1]); the 'loss-only' non-positivity is used in the analysis` (abernethy2015fighting); `loss vectors in a bounded set Y with known norms ||Y||_p` (agarwal2017price); `|<l_t,x>| <= M with M known to tune eta` (agarwal2017price)

### Context and action-set generation details (127 items, 75 papers)

Guidance: i.i.d. contexts are stochastic_contexts, with diversity or eigenvalue conditions in conditions. Fixed, arbitrary or unspecified context sequences are adversarial_contexts plus action_set.time_varying (adaptive_sequence if unspecified). A known context distribution is a result condition. Finite context sets use M_ctx. Available-set sequences use extras.sleeping_arms or time_varying_action_sets.

Examples: `Context/reward-vector pairs drawn i.i.d. from a joint distribution D over X x [0,1]^A` (agarwal2014taming); `N arms each with a context vector b_i(t) chosen adaptively by an adversary each round; regret against the per-round best` (agrawal2013lints); `Fixed unknown function f(x,c); contexts c_t in [0,1]^p chosen by an adaptive adversary` (akhavan2024conversion); `Contexts adversarial in [0,1]^p; contextual regret against per-round minimizer` (akhavan2024conversion)

### Instance-class assumptions (uniqueness, distinct means, mean bounds, known ordering, permutation classes, priors, reservoirs) (120 items, 70 papers)

Guidance: use instance_assumptions (unique_optimal_arm, gap_bounded_below, means_in_known_interval, bayesian_prior) and learner_knows (Delta_lower_bound, mu_star). Infinite reservoirs use extras.infinitely_many_arms. Known orderings, permutation classes and other instance restrictions go in the result's conditions.

Examples: `Known lower bound mu^- on the means (used to clip estimates)` (baudry2023recipe); `Means bounded below by a known mu^-` (baudry2023recipe); `Gap Delta_bar_N = min over n of the per-round gap` (baumgrtner2026gray); `Instance is locally phi-sparse (||n||_2^2/n_1^2 <= phi on every window of size w >= sqrt(T))` (brukhim2026lookahead)

### Lower-bound construction specifics (56 items, 46 papers)

Guidance (existing line): hard-instance families, randomised permutations, algorithm-specific lower bounds and reductions go in the result's conditions or algorithm_class, not the setting.

Examples: `Contexts i.i.d. from specific distribution P_K (uniform on shrunken cells)` (akhavan2024conversion); `Lower bounds on families: uncorrupted Student distributions, or eps-corrupted Bernoulli distributions` (basu2022bandits); `Lower bound holds for some ordering (permutation) of the given set of distributions` (bubeck2008pure); `Supremum over all weakly Lipschitz environments F_{X,l}` (bubeck2010armed)

### Pricing, auctions, contracts, mechanism design and strategic agents (209 items, 36 papers)

Guidance: map the application to its underlying structure. Posted prices or bids are action_space continuum_other or lipschitz_metric (finite_K if discretised). Win-only or sale-only observation is the feedback value (see the feedback-structure theme). Strategic arms or buyers are extras.strategic_arms. Supply limits are knapsack_constraints. The application model (demand form, auction format, agent best response) goes in the result's conditions.

Examples: `Principal-agent contract design: actions are payment vectors f in [0,1]^m over m outcomes; agent of random type best-res` (ai2026minimax); `Feedback is the realized outcome category (one-hot vector over m outcomes), which is stronger than scalar bandit reward ` (ai2026minimax); `Stackelberg regret against the best fixed contract` (ai2026minimax); `Learner knows number of outcomes m and value vector v` (ai2026minimax)

### Gaussian process / RKHS specifics (56 items, 26 papers)

Guidance: action_space = kernel_rkhs. For a GP sample, add instance_assumptions.bayesian_prior. The RKHS norm bound is variable S (learner_knows.S if known). The kernel family (SE, Matern-nu) and k(x,x) ≤ 1 go in the result's conditions.

Examples: `Kernel k with k(x,x) <= 1 and tail conditions on sup|f| and its derivatives` (bogunovic2016time); `f has RKHS norm at most B for the SE or Matern-nu kernel (length-scale l)` (cai2020lower); `f has RKHS norm at most B for the SE or Matern-nu kernel` (cai2020lower); `f has RKHS norm at most B for the SE or Matern-nu kernel` (cai2020lower)

### Unknown, anytime or random horizon (13 items, 9 papers)

Guidance: an anytime or unknown horizon means T is absent from learner_knows. A random horizon and stopping-time definitions go in the result's conditions.

Examples: `Horizon unknown` (basu2020contextual); `Number of rounds n not necessarily known in advance (anytime); forecaster outputs a recommendation J_n each round` (bubeck2008pure); `horizon unknown to the learner` (durmann2026mean); `horizon unknown` (durmann2026mean)

## Out of scope

### Reinforcement learning / MDP and Markov-game settings (59 items, 16 papers)

Episodic MDPs, linear MDPs, factored MDPs and Markov games are RL problems, not bandit problems. Set in_scope=false for these settings and keep the bandit settings of the same papers.

Examples: `Episodic finite-horizon restless bandit: N arms, each a finite-state non-stationary MDP with unknown transition probabil` (akbarzadeh2024risk); `Learner observes the full state of all arms (state transitions of every arm), not just a scalar reward` (akbarzadeh2024risk); `Risk-aware objective: sum over arms of a non-decreasing Lipschitz utility of each arm's cumulative reward; history-depen` (akbarzadeh2024risk); `Rewards deterministic, known, in [r_min, r_max] with r_min >= 0` (akbarzadeh2024risk)

### Learning in games with equilibrium objectives (71 items, 13 papers)

Zero-sum and general-sum games, Stackelberg games, monotone games, potential games and self-play are about convergence to an equilibrium, not about one learner's regret. Mark these settings in_scope=false. A bandit-feedback regret result inside such a paper, against an arbitrary opponent sequence, should be extracted as adversarial_adaptive.

Examples: `Two-player zero-sum m x n matrix game; a single centralized learner picks mixed strategies x_t, y_t for both players and` (abe2026thompson); `Performance measure is the cumulative duality (Nash) gap sum_t Gap_{A*}(x_t,y_t), not standard regret` (abe2026thompson); `Payoff matrix A* assumed to have a unique Nash equilibrium` (abe2026thompson); `Two-player zero-sum m x m matrix game, centralized learner, cumulative duality gap` (abe2026thompson)

### Non-bandit problems and extraction artefacts (44 items, 11 papers)

Hopsets, Gittins-index approximation, fully offline confounded policy learning, passive kernel regression, online GLM prediction, concentration-boundary lower bounds and items whose source was missing are not interactive bandit problems. Set in_scope=false, or flag the item for re-parsing where the source was missing.

Examples: `Shortcut-edge sets (hopsets) for weighted graphs with a hop bound h; bounds are on hopset size and distance-query time. ` (besson2018what); `offline learning from a fixed logged dataset of T trials (no interaction)` (chen2023unified); `unmeasured confounder U affecting action, context and reward in the logging policy` (chen2023unified); `instrumental variable side observation Z` (chen2023unified)

### Attacker-side guarantees (21 items, 5 papers)

Results bound an attacker's cost of forcing a fixed victim algorithm onto a target arm. They are not guarantees for a bandit learner, so mark these settings in_scope=false.

Examples: `The guarantee is for an attacker (not the learner): the attacker perturbs contexts shown to LinUCB to force pulls of tar` (garcelon2020adversarial); `Disjoint per-arm linear model: reward <theta_a, x_t> + noise with K arm parameters` (garcelon2020adversarial); `Attacker knows a lower bound nu on the target-arm reward (Assumption 2) and has white-box access to LinUCB` (garcelon2020adversarial); `Expected rewards in (0,1] for all contexts and arms` (garcelon2020adversarial)
