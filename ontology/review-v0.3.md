# Ontology review after the schema-0.4 extraction (v0.3 → proposed v0.4)

Input: the 267 `unmapped` items in the schema-0.4 extractions (58 papers). They were clustered into 24 themes by one LLM pass, with the ontology in context (`claude -p`, no tools). Counts and decisions below are that pass's proposals, to be reviewed by hand. **Status: proposed, not applied**: applying v0.4 means re-extracting.

| decision | themes | items |
|---|---|---|
| ontology change | 9 | 113 |
| result field | 3 | 36 |
| already expressible | 10 | 98 |
| out of scope | 2 | 20 |

## Ontology changes (proposed for v0.4)

### Scale normalisation for linear/GLM settings: bounds on action norms, parameter norm or parameter set, and loss sets (dual/polar normalisation, l2/l1-ball losses) (45 items)

Papers: abbasi2011oful, abeille2017lints, agrawal2013lints, bubeck2012minimax, bubeck2012survey, chu2011suplinucb, dani2008stochastic, dann2023blackbox, hazan2016volumetric, kim2022varianceadaptive

Bounds in d, L and S are only comparable once the normalisation is known, so the normalisation should be a structured field rather than free text. Extend node_parameters.action_set with:
  norm_bound:
    values: [not_applicable, unspecified, unit_l2, bounded_L]   # bounded_L: ||x||_2 <= L (variable L)
    order: [[unit_l2, bounded_L], [unspecified, bounded_L]]
    value_maps: {unit_l2: {L: 1}}
  parameter_set:
    values: [not_applicable, unspecified, l2_ball, l1_ball, polytope, arbitrary_bounded, unbounded]   # ||theta|| <= S
    order: [[l2_ball, arbitrary_bounded], [l1_ball, arbitrary_bounded], [polytope, arbitrary_bounded], [unspecified, arbitrary_bounded], [arbitrary_bounded, unbounded]]
    note: "scale S lives in variables.yaml; learner_knows.S records whether it is known"
  loss_set:   # adversarial or stochastic loss-vector models
    values: [not_applicable, unspecified, bounded_mean_reward, polar_of_action_set, l2_ball, l1_ball, linf_box, binary_vectors]
    # bounded_mean_reward: |<theta,x>| <= 1 for all x in A; polar_of_action_set: |<x,l>| <= 1 for all x in A, l in Z
    order: [[bounded_mean_reward, polar_of_action_set], [unspecified, polar_of_action_set]]
    note: "l2_ball / l1_ball / linf_box are polar_of_action_set only for the matching dual action set; do not infer that order automatically"
Tail conditions on the loss vector (Shamir's sub-Gaussian dual-norm tails, a second moment of ||x||) go into noise (subgaussian / heavy_tailed) with loss_set = polar_of_action_set.

Examples: “abbasi2011oful: mean rewards theta^T x in [-1,1]; learner uses the bound L on ||x||” · “chu2011suplinucb: ||x_{t,a}|| <= 1 and ||theta*|| <= 1” · “bubeck2012minimax: loss set Z = cross-polytope / unit Euclidean ball”

### Learner knows quantities missing from learner_knows (action-norm bound L, moment order eps, number of experts N, independence number alpha_G, link constant c_mu, best loss L*, number of actions per round, psi function, inner/outer radii r and R of K) (17 items)

Papers: abbasi2011oful, abeille2017lints, bubeck2012survey, bubeck2013heavy, dann2023blackbox, lee2020biasnomore, li2019nearlyminimax, neu2015explore, rusmevichientong2010linear, tirinzoni2020primaldual

Extend learner_knows.values (the existing subset order rule applies unchanged):
  L: "bound on action / feature norms"
  eps_m: "moment order of the heavy-tail condition"
  N_exp: "number of experts / policies"
  alpha_G: "independence number (or a dominating set) of the feedback graph"
  c_mu: "lower bound on the link derivative"
  L_star: "cumulative loss of the best action"
  r_K: "radius of a ball contained in K" (diam_K already covers R)
Knowing the psi-function is moment_bound. The number of actions per round (n_act) is K. Related extractor errors: auer2002exp3's 'hardness S' is learner_knows.S_T, agrawal2013's R is sigma, and zimmert2021's gaps are Delta.

Examples: “bubeck2013heavy: learner knows eps” · “neu2015explore: learner knows alpha of the observation graph” · “abeille2017lints: learner uses c_mu to scale the confidence radius”

### Corruption model details (adaptive vs oblivious corruptor, per-path vs expected C, linear vs arbitrary corruption, whether regret is measured on corrupted or uncorrupted rewards) (16 items)

Papers: dann2023blackbox, gupta2019corruption, ito2022variance, kong2023bestofthree, lee2021instanceminimax, lykouris2018corruption, masoudian2021improved, zimmert2021tsallisinf

These choices change which bounds are comparable: regret on corrupted vs uncorrupted rewards differs by up to C, and an expected C differs from a per-path C. Add:
node_parameters:
  corruption:
    applies_to: "environment in {stochastic_corrupted, adversarial_self_bounding}; else not_applicable"
    fields:
      adversary: {values: [not_applicable, unspecified, oblivious, adaptive], order: [[oblivious, adaptive], [oblivious, unspecified], [unspecified, adaptive]]}
      budget_measure: {values: [not_applicable, unspecified, per_path, in_expectation], order: [[per_path, in_expectation]]}   # a per-path budget C implies E[C] <= C
      structure: {values: [not_applicable, unspecified, linear_in_action, arbitrary], order: [[linear_in_action, arbitrary]]}
      regret_reference: {values: [not_applicable, corrupted, uncorrupted]}   # must match exactly; no order
Knowledge of C stays in learner_knows.C. Masoudian's 'constraint only at time T' is a result condition. Zimmert's stochastically constrained + corrupted is adversarial_self_bounding (C_sb = 2C).

Examples: “lykouris2018corruption: adaptive corruptor, sum_t max_a |r - r_S| <= C on every sample path” · “ito2022variance: C = E[sum_t ||l' - l||_inf]; regret on corrupted losses” · “lee2021instanceminimax: linear corruption l_t = theta + c_t; regret w.r.t. uncorrupted theta”

### Action-set geometry details (subset of the unit ball, shifted ball, cylinder, product of circles, strongly convex / SBAR sets, explicit small hard sets) (11 items)

Papers: abeille2017lints, dani2008stochastic, hamidi2020lints, kim2022varianceadaptive, li2019nearlyminimax, rusmevichientong2010linear, shamir2015complexity

Most of these are already expressible with action_set.shape: arbitrary_compact (abeille, kim), convex_body (shamir's shifted ball and cylinder), nonconvex (dani's (S^1)^{n/2}), finite (hamidi), plus time_varying (li2019, kim). Conditions like 'contains {-mu,mu}^d' or 'bounded away from the origin' belong in result conditions. One value is missing, and it matters because the rates differ (sqrt(T) vs log T for strongly convex sets): add to action_set.shape
  strongly_convex: "strongly convex set / smooth best-arm response SBAR(J)"
  order: add [strongly_convex, convex_body]
'r known linearly independent arms with lambda_min >= lambda_0' maps to instance_assumptions.arms_span_Rd, with lambda_0 as a condition.

Examples: “rusmevichientong2010linear: arm set strongly convex / SBAR(J)” · “shamir2015complexity: cylinder [-1,1] x B^{d-1}” · “dani2008stochastic: product of n/2 unit circles”

### Bayesian prior details (learner knows the prior, prior-family conditions, arbitrary reward dependence, GP prior) (10 items)

Papers: hamidi2020lints, rusmevichientong2010linear, russo2014posterior

Mostly expressible as instance_assumptions.bayesian_prior + quantity bayesian_regret, with the prior conditions (E||Z|| <= M, gap density bounded) as result conditions. A GP prior is action_space = kernel_rkhs with bayesian_prior. One addition is needed, because prior-dependent and prior-independent bounds are not comparable: learner_knows gains
  prior: "the prior over the instance (Bayesian algorithm uses it)"
The subset order rule applies.

Examples: “russo2014posterior: learner knows the prior (4 settings)” · “rusmevichientong2010linear: prior N(0, I_r/r) known to the learner”

### Feedback-graph properties (strongly vs weakly observable, fixed vs time-varying, known vs unknown) (6 items)

Papers: dann2023blackbox, neu2015explore

Observability sets the rate (sqrt(T) vs T^{2/3}), so a graph_feedback bound is not comparable without it. Add:
node_parameters:
  feedback_graph:
    applies_to: "feedback = graph_feedback; else not_applicable"
    fields:
      observability: {values: [not_applicable, unspecified, strongly_observable, observable], order: [[strongly_observable, observable], [unspecified, observable]]}   # observable = strongly or weakly
      time_varying: {values: [not_applicable, fixed, oblivious_sequence, adaptive_sequence], order: [[fixed, oblivious_sequence], [oblivious_sequence, adaptive_sequence]]}
      knowledge: {values: [not_applicable, known_in_advance, revealed_after_action, never_revealed], order: [[known_in_advance, revealed_after_action], [revealed_after_action, never_revealed]]}
Weak-observability bounds should be recorded under observable.

Examples: “dann2023blackbox: feedback graph strongly observable and known” · “dann2023blackbox: weakly observable; learner knows a weakly dominating set” · “neu2015explore: fixed directed observation graph G”

### Computational access to the action set (barycentric spanner, self-concordant barrier) (3 items)

Papers: dani2008stochastic, lee2020biasnomore

Add to node_parameters.action_set.access.values: barycentric_spanner, self_concordant_barrier (a nu-barrier; nu is a variable). This is computational only, as the existing note says.

Examples: “dani2008stochastic: learner needs access to a barycentric spanner of D” · “lee2020biasnomore: learner is given a nu-self-concordant barrier for Omega”

### Gaussian rewards with unknown (arm-dependent) variances (3 items)

Papers: auer2002ucb1, baudry2023recipe

Add noise value gaussian_unknown_variance: "N(mu_i, sigma_i^2), both unknown". Order: [gaussian_known_variance, gaussian_unknown_variance] (an algorithm for unknown variances runs when they are known). Do not place it under subgaussian or heavy_tailed unless a variance bound is assumed; with a variance bound use instance_assumptions.bounded_variance. Known bounds on means or variances (baudry) map to means_in_known_interval and learner_knows.moment_bound.

Examples: “auer2002ucb1: Gaussian rewards with unknown means and unknown arm-dependent variances” · “baudry2023recipe: Gaussian with unknown variance (two-parameter family)”

### Decoupled exploration and exploitation feedback (observe a different arm from the one played) (2 items)

Papers: jin2023improved

Below the >= 3 threshold, but this is a distinct feedback model with different rates, and it cannot be expressed as bandit or graph feedback. Add to feedback.values:
  decoupled: "play one arm (suffer its loss), observe the loss of a separately chosen arm"
  order: add [full_information, decoupled]   # a full-information instance reveals the exploration arm's loss
Add no edge to bandit: the learner does not see the loss of the arm it played.

Examples: “jin2023improved: DEE-MAB, exploit arm i^t, observe exploration arm j^t”

## Belongs in a result field (conditions / tuning / regime), not the setting

### Lower-bound construction specifics and restricted algorithm classes (specific hard instances, random instances, bounds only against algorithms with log stochastic regret or only for LinTS, rescaled regret, bounds holding even with full information) (20 items)

Papers: auer2002exp3, auer2016nearly, bubeck2013bounded, bubeck2013heavy, dani2008stochastic, garivier2019explore, gupta2019corruption, hamidi2020lints, ito2022variance, lattimore2015ocucb

Record in the result fields: conditions (the specific instance family, Delta range, Dirac arm), regime (worst case over Delta, rescaled regret Delta*R_n), and an algorithm-class restriction ('algorithms with O(log^beta T) stochastic regret', 'LinTS without inflation'). Mis-specified priors (hamidi) also go in conditions. A lower bound that holds even under full information should be recorded with feedback = full_information, so that it transfers down the order.

Examples: “auer2016nearly: applies to players with pseudo-regret <= C (log n)^beta on stochastic problems” · “hamidi2020lints: holds only for LinTS without inflation” · “bubeck2013bounded: lower bound holds even with full information”

### Horizon / dimension side-conditions (n >= K >= 2, T >= max{55, K}, r >= 2) (9 items)

Papers: bubeck2012bobw, ito2022variance, jin2023improved, rusmevichientong2010linear

Record as result conditions on T, K and d.

Examples: “ito2022variance: T >= max{55, K}” · “rusmevichientong2010linear: r >= 2”

### Confidence parameter delta given to the algorithm (7 items)

Papers: chu2011suplinucb, lee2020biasnomore, lee2021instanceminimax

Record under result tuning (inputs: delta), with quantity high_probability_regret where it applies. It is not a property of the setting.

Examples: “chu2011suplinucb: learner also needs delta to set alpha” · “lee2021instanceminimax: learner needs confidence delta”

## Already expressible: extractor guidance needed

### Fixed numerical noise level (1-sub-Gaussian, standard Gaussian, R = 1) (18 items)

Papers: abbasi2011oful, hao2020adaptive, jin2020detc, kirschner2021ids, lattimore2015ocucb, lattimore2017endofoptimism, li2019nearlyminimax

Use noise = subgaussian or gaussian_known_variance. The value sigma = 1 (or sigma_std = 1) goes into the result's conditions or variable instantiation, not the setting. Arm-dependent noise under one common sigma is still subgaussian.

Examples: “jin2020detc: rewards are 1-subgaussian (7 settings)” · “lattimore2017endofoptimism: noise is standard Gaussian N(0,1)” · “hao2020adaptive: noise is standard Gaussian”

### Structured / parametric models (known Theta and reward map, unimodal 1-D losses with growth condition, GLM link regularity, eluder-dimension function classes, combinatorial sizes) (17 items)

Papers: abeille2017lints, bubeck2012minimax, bubeck2012survey, combes2017ossb, kong2023bestofthree, russo2014posterior, wei2018moreadaptive

OSSB-type models are action_space = structured_general, with noise bernoulli / gaussian_known_variance / general_model_class (finite arms are implied). Unimodal on [0,1] is continuum_other + function_class quasi_convex; the growth constant C_L is a condition. GLM link conditions are generalized_linear with k_mu and c_mu. A general class F with eluder dimension is structured_general, with the complexity measures as variables. The combinatorial max size K_0 is m. N actions -> K and |D| -> K are correct mappings.

Examples: “combes2017ossb: known compact Theta and reward map mu(x, theta)” · “bubeck2012survey: mean loss unimodal on [0,1]” · “wei2018moreadaptive: at most K_0 arms per action”

### General or non-parametric reward model classes (h-moment conditions, psi-condition, generic concentration assumption, all distributions on [0,1], finitely supported, exponential-family regularity) (16 items)

Papers: baudry2023recipe, bubeck2012survey, bubeck2013heavy, cappe2013klucb, garivier2011klucb, garivier2018klucbswitch, garivier2019explore, jin2022exptsfamily, menard2017klucbpp

All distributions on [0,1] is noise = bounded_01. Finitely supported on [0,1] is bounded_01 (the lower bound class is general_model_class). Canonical one-parameter exponential families, with their regularity conditions, are exponential_family. h-moment / psi-condition / Assumption 1 classes are heavy_tailed or general_model_class, with the specific condition as a result condition. Known support bound B, known mean lower bound and bounded variance V map to bounded_01 after rescaling, means_in_known_interval, bounded_variance and learner_knows.moment_bound.

Examples: “garivier2018klucbswitch: non-parametric model, all distributions over [0,1]” · “baudry2023recipe: E[h(|X|)] < B for a known convex h” · “menard2017klucbpp: variance of the family bounded by V; means in [mu^-, mu^+]”

### Contexts and per-round action sets (finite i.i.d. contexts with p(m) > 0, oblivious or adaptive context sequences, per-context action sets) (12 items)

Papers: agrawal2013lints, bubeck2012survey, chu2011suplinucb, hao2020adaptive, li2019nearlyminimax, russo2014posterior, tirinzoni2020primaldual, zhang2021varianceaware

Finite i.i.d. contexts are context = stochastic_contexts with M_ctx. p_min / rho_min are result conditions. Oblivious vs adaptive context sequences are context = adversarial_contexts plus action_set.time_varying in {oblivious_sequence, adaptive_sequence}; use extras.time_varying_action_sets. A generation process the paper does not specify should be recorded as adaptive_sequence, the conservative choice. Regret against the best arm in each round uses comparator best_action_per_round. Unique optimal arm per context is instance_assumptions.unique_optimal_arm.

Examples: “hao2020adaptive: M contexts i.i.d. with p(m) > 0, known action set per context” · “agrawal2013lints: contexts chosen by an adaptive adversary” · “li2019nearlyminimax: action sets chosen obliviously before execution”

### Regret notion / comparator details (realized regret, pseudo-regret against adaptive adversaries, empirical best arm, minimax game value, round complexity) (10 items)

Papers: auer2002exp3, jin2020detc, lee2020biasnomore, neu2015explore, wei2018moreadaptive, zimmert2021tsallisinf

Use quantity realized_regret, high_probability_regret, pseudo_regret or expected_regret with the matching comparator. The minimax game value is quantity other. Batch round complexity is a second result with quantity other, not a setting feature.

Examples: “lee2020biasnomore: realized regret against the best fixed action” · “zimmert2021tsallisinf: pseudo-regret even for adaptive adversaries” · “jin2020detc: number of policy updates also measured”

### Self-bounding / stochastically constrained variants (multiple optimal arms with excess term D, gap condition without i.i.d., constraint only at T) (8 items)

Papers: jin2023improved, masoudian2021improved, wei2018moreadaptive, zimmert2021tsallisinf

environment = adversarial_self_bounding. Omit unique_optimal_arm when multiple optimal arms are allowed. D goes into variables / result conditions. wei2018's conditional-gap environment is adversarial_self_bounding with C = 0. Zimmert's stochastically constrained adversary is adversarial_self_bounding with C_sb = 0.

Examples: “jin2023improved: multiple zero-gap arms; bound in D” · “wei2018moreadaptive: E[l_i - l_a* | past] >= Delta without i.i.d.”

### Policy-class / expert comparators (finite policy class, VC class, context-set classes, multiclass hinge-loss comparator, uniform expert in the class) (7 items)

Papers: auer2002exp3, bubeck2012survey, dann2023blackbox

Use extras.expert_advice and comparator best_policy / best_expert, with N_exp or the VC dimension as variables. 'Uniform expert included' and the hinge-loss comparator are result conditions. Bandit multiclass classification with a surrogate-loss comparator is borderline and can be flagged in_scope = false.

Examples: “dann2023blackbox: finite policy class of size N_exp” · “bubeck2012survey: policy class with VC dimension d” · “auer2002exp3: expert family must include the uniform expert”

### Martingale / time-varying conditional-variance noise with bounded rewards (variance-adaptive linear bandits) (4 items)

Papers: dani2008stochastic, kim2022varianceadaptive, kong2023bestofthree, zhang2021varianceaware

noise = conditionally_subgaussian; also set loss_set = bounded_mean_reward under the new action_set field. The dependence on sum_k sigma_k^2 is a result-side quantity (variables), not part of the setting.

Examples: “zhang2021varianceaware: martingale difference noise with unknown round-dependent variance; |r_k| <= 1” · “dani2008stochastic: E(c_t(x)|H_t) = mu.x, costs in [-1,1]”

### Losses vs rewards sign convention, and unstated adversary type (4 items)

Papers: abernethy2015fighting, dani2008stochastic, ito2022variance

Sign conventions are not a setting feature. Losses in [0,1] (or gains in [-1,0]) are noise = bounded_01; costs in [-1,1] are bounded_pm1. An unstated adversary is adversarial_unspecified.

Examples: “abernethy2015fighting: g_t in [-1,0]^N as negative gains; adversary not stated” · “dani2008stochastic: costs minimised rather than rewards”

### Utility-based dueling bandits (2 items)

Papers: zimmert2021tsallisinf

feedback = dueling, with environment stochastic_iid or adversarial_oblivious/unspecified. The utility-based link and the regret definition are result conditions.

Examples: “zimmert2021tsallisinf: P[W_t = I_t] = (1 + u_I - u_J)/2”

## Out of scope for the bandit graph (`in_scope: false`)

### Episodic MDPs / linear mixture MDPs (14 items)

Papers: dann2023blackbox, kim2022varianceadaptive, lee2020biasnomore, zhang2021varianceaware

Mark these settings in_scope = false. They are reinforcement-learning settings, not bandits.

Examples: “dann2023blackbox: tabular episodic MDP with unknown transitions” · “zhang2021varianceaware: linear mixture MDP with total reward bounded by 1”

### Repeated games (unknown N-person game, zero-sum matrix games with bandit feedback) (6 items)

Papers: auer2002exp3, wei2018moreadaptive

Mark in_scope = false, or, when the guarantee is plain regret, record as adversarial_adaptive bandit with feedback bandit. Guarantees relative to the game value are quantity other.

Examples: “auer2002exp3: repeated unknown zero-sum matrix game, guarantee vs minimax value” · “wei2018moreadaptive: two-player zero-sum game with bandit feedback”

