# Ontology review after batch 2 (ontology v0.5)

Input: the 6259 `unmapped` items in 1057 extractions, grouped into themes by one LLM pass with the ontology in context (`pipeline/review_unmapped.py`, opus). **Status: proposed, not applied.** 6234 of 6259 items were assigned to a theme.

| decision | themes | items | papers |
|---|---|---|---|
| ontology change | 9 | 884 | 218 |
| result field | 4 | 785 | 295 |
| already expressible | 20 | 3215 | 679 |
| out of scope | 7 | 1350 | 212 |

## Synthesis and recommendations for v0.6 (hand-written, 2026-11-09)

Inputs: the themes below (LLM grouping of 6,259 `unmapped` items), the conflict review after batch 2
(57 → 7 conflict cells; `data/corrections.yaml`, entries dated 2026-11-09), and the batch-2 audit
(`data/reports/audit-batch2.md`). **Nothing below is applied yet.** Ranked by how much they change the atlas:

1. **Scope leakage (no new vocabulary).** Settings that the v0.5 cut removes are still in the atlas when the extractor
   left `in_scope: true` and described the feature only in `unmapped`: state-dependent dynamics (72 papers),
   multi-agent (54), equilibrium objectives (25), multi-objective (24), quantum (17), offline data (13), attackers (8).
   Fix: a cached one-pass classifier over in-scope settings (like `classify_conditions.py`) that tags these, and a
   `resolve.py` rule that drops them. Reversible; no re-extraction.
2. **Combinatorial base-arm symbol.** 174 combinatorial bounds count base arms with `d`, 121 with `K`; bounds in the
   two conventions are compared as if `d` and `K` were different quantities (3 of the 7 remaining conflicts:
   chen2016pure vs rejwan2019combinatorial, xu2021simple vs kveton2014tight). Decide one convention (proposal: `d` =
   number of base arms, as in Audibert et al.; `K` only for unstructured arms), add it to the variable registry and
   prompt, and re-extract the ~80 combinatorial papers together with theme 1 below (`combinatorial.base_arm_dependence`).
3. **Fields the conflict review needed** (patched with corrections for now, each a `model_change` condition):
   - auctions: whether the valuation is seen *before* bidding (yanjun2020learning, √T) or only after
     (cesabianchi2024role, T/24); and the comparator policy class (Lipschitz vs monotone bidding functions);
   - an observation channel: losses observed through random flips (resler2018adversarial, T^{2/3} rates);
   - richer-than-bandit feedback (win-only / outcome-based, feng2017learning) and outcome-shared arms
     (song2025outcome);
   - dueling regret notions (`preference.regret_type`, theme 2 below; suk2024stationary's weighted regret).
4. **Kernel bounds are unprofiled.** `gamma_T` (information gain) grows with T at a kernel-dependent rate; it is
   now opaque in `compare.py` (54 results), which removed two false conflicts but also most kernel comparisons.
   A `kernel.family` field (SE, Matérn with ν, NTK) plus conversion rules γ_T(SE) = log^{d+1} T,
   γ_T(Matérn) = T^{d/(2ν+d)} log T would make them comparable again.
5. **The other new fields proposed below**, in order of items covered: `combinatorial.base_arm_dependence`
   (289 items), `preference.regret_type` + `stochastic_triangle_total_order` (182), `delay.observability/coupling` (128),
   `reward_model.kind: nested_model_selection` (82), extras `multi_task` (76), `function_class: dr_submodular` (71),
   `parameter_structure: disjoint_per_arm` (25), `combinatorial.reward: choice_mnl` (24), extras `cross_learning` (7).
   Each needs re-extraction of the affected papers only (estimated 150–250 papers, ~$100–150).
6. **Knowledge.** Batch 2 lists 0.49 knowledge items per setting in `unmapped` (batch 1: 0.17), as prompt rule 22 asks
   when no registry symbol fits; the audit still finds missing knowledge in ~20% of settings. Promote the recurring
   ones to `variables.yaml` (per-arm costs, corruption functions, graph spectra, margin exponents) so they become
   `learner_knows` values that block invalid lower-bound transfers.
7. **Fragmentation** is unchanged in kind: 1,907 of 2,037 canonical settings come from a single paper (batch 1:
   999 of 1,102). Inheritance leaves 23 settings without any bound. It is breadth, not one over-fine field.

## Ontology change

### Combinatorial reward structure: nonlinear/submodular rewards, approximation oracles, triggering, base-arm correlation, full-bandit feedback (289 items, 80 papers)

Add field combinatorial.base_arm_dependence {not_applicable, unspecified, independent, arbitrary} with order independent ⊑ arbitrary (rates under independence do not transfer to correlated outcomes). Approximation oracles stay alpha_regret + algorithm conditions; full-bandit feedback is feedback=bandit on combinatorial. Re-extract combinatorial settings.

Examples: `Exploration may play sets in I^{+1} (independent after deleting at most one element); exploitation and benchmark are mat` (aggarwal2026adversarial); `Mean reward is nonnegative submodular (possibly non-monotone); only the mean is submodular, not the realizations` (aggarwal2026adversarial); `Matroid is a unit-capacity partition matroid (at most one element per part)` (aggarwal2026adversarial); `Exploration may play sets in I^{+1}; exploitation and benchmark are feasible` (aggarwal2026adversarial)

### Dueling regret definitions and preference-model assumptions (182 items, 39 papers)

Add field preference.regret_type {not_applicable, unspecified, average, weak, strong, binary_weak, binary_strong} (must match, no order). Add preference.model value 'stochastic_triangle_total_order' ordered utility_link ⊑ strong_stochastic_transitivity ⊑ stochastic_triangle_total_order ⊑ general. Re-extract dueling settings.

Examples: `Stochastic triangle inequality (STI): eps_{i,k} <= eps_{i,j} + eps_{j,k} for b_i >= b_j >= b_k` (agarwal2022batched); `Stochastic triangle inequality (STI) holds` (agarwal2022batched); `Linear link function Pr[b_t=1|(u,v)] = (1+v-u)/2` (ailon2014reducing); `Regret measured on unobserved average utility (u_t+v_t)/2` (ailon2014reducing)

### Model selection, corralling and misspecification levels (82 items, 30 papers)

Add reward_model.kind value 'nested_model_selection' (realizable in an unknown member of nested classes), order realizable_general_class ⊑ nested_model_selection ⊑ misspecified; misspecification forms (uniform, gap-adjusted) go in conditions with eps_mis. Re-extract model-selection papers.

Examples: `Master algorithm combining M black-box base bandit algorithms; regret measured against the decision space Theta_i of a b` (agarwal2016corralling); `Master must pick among suggestions of two given (non-stable) base algorithms` (agarwal2016corralling); `Three nested policy classes Theta_4 ⊂ Theta_1 ⊂ Theta_3 used by different base algorithms; learner knows their sizes` (agarwal2016corralling); `Three nested policy classes used by different base algorithms; regret against the smallest class Theta_4` (agarwal2016corralling)

### Delay variants: censored/anonymous/composite feedback, loss-coupled delays, capacity limits, evolving observations (128 items, 23 papers)

Extend node delay with fields observability {not_applicable, unspecified, tagged, anonymous_aggregated, censored_window} (order tagged ⊑ anonymous_aggregated; censored must match) and coupling {not_applicable, unspecified, independent_of_loss, arm_dependent, loss_dependent} (order independent_of_loss ⊑ arm_dependent ⊑ loss_dependent); add delay.generation value 'adaptive'. Capacity/clairvoyance stay conditions. Re-extract settings with extras.delayed_feedback.

Examples: `an intermediate state S_t ~ P(.|A_t) from a finite state space is observed immediately; the loss is delivered after a fi` (baghi2026pooling); `an intermediate state S_t is observed immediately; loss delivered after fixed delay d` (baghi2026pooling); `Evolving observations: at each round the learner observes feedback losses ell_tau^(t) in [0,1]^K for all past rounds tau` (baron2024stochastic); `The learner knows an upper bound D_bar on the total feedback inaccuracy D (for the tuned corollary)` (baron2024stochastic)

### Meta-learning, multi-task, clustered users and shared representations (76 items, 21 papers)

Add extras value 'multi_task' (several bandit tasks, sequential or concurrent, sharing structure such as a prior, subspace or clusters; task count a variable n_tasks), not generalizing. Clusters of users served by one learner use it too. Re-extract.

Examples: `Multi-task / sequential transfer: J episodes of n steps; at each episode a latent task (model) is drawn i.i.d. from an u` (azar2013sequential); `Sequential multi-task (meta-learning) setting: m tasks of n rounds each; task parameters theta_s ~ N(mu_*, Sigma_0) i.i.` (basu2021regrets); `Learner knows meta-prior Q (mu_q, Sigma_q), task covariance Sigma_0 and noise sigma^2, but not mu_*` (basu2021regrets); `Regret is Bayes regret summed over all m tasks` (basu2021regrets)

### Disjoint per-arm parameters (separate theta_a per arm with shared or per-arm contexts) (25 items, 15 papers)

Add action_set.parameter_structure value 'disjoint_per_arm' (each of K arms has its own d-dim parameter; effective dimension K*d), order dense ⊑ disjoint_per_arm is wrong direction — instead treat as must-match, with a reduction to dense linear with d→K*d. Re-extract contextual linear papers mentioning per-arm parameters.

Examples: `Each of N arms has its own context x_{a,t} each round; reward mean f*(z_a, x_{a,t}) with f* in RKHS of product kernel k_` (deshmukh2017multi); `disjoint linear model: each of the K arms has its own unknown parameter theta_a in R^d, E[r_t(a)|x]=x^T theta_a` (dimakopoulou2017estimation); `disjoint linear model: each of the K arms has its own unknown parameter theta_a in R^d` (dimakopoulou2017estimation); `Each arm has its own unknown continuous path functional f_a; rewards are approximated by linear functionals of truncated` (guo2026signature)

### MNL / discrete-choice assortment feedback (24 items, 8 papers)

Add combinatorial.reward value 'choice_mnl' (single chosen item drawn from a multinomial-logit model over the offered set, revenue objective), order choice_mnl ⊑ nonlinear (no ⊑ to linear). Feedback stays semi_bandit-like as recorded; re-extract assortment papers.

Examples: `Feedback is a single choice (index of the chosen item or the no-purchase option) drawn from a Multinomial Logit choice m` (agrawal2017thompson); `Expected reward of a subset is the MNL revenue sum_i r_i v_i/(1+sum_j v_j), nonlinear in the unknown parameters v_i; ite` (agrawal2017thompson); `Multinomial logit (MNL) choice feedback: the learner observes which item (or no purchase) the customer chooses from the ` (chen2017note); `Reward is the expected revenue R_v(S) = sum r_i v_i / (1 + sum v_i), nonlinear in the assortment` (chen2017note)

### Cross-learning across contexts (7 items, 4 papers)

Add extras value 'cross_learning' (playing an action reveals its loss under every context), not generalizing; cross-learning results then do not transfer to plain contextual settings. Re-extract the few contextual papers that state it.

Examples: `Cross learning: playing an action reveals the rewards of the observed actions under all M contexts` (han2020optimal); `Cross learning across a finite set of M contexts` (han2020optimal); `Cross learning across a finite set of M contexts` (han2020optimal); `Cross-learning feedback: the learner observes the loss of the played arm under every context c in [C], not just the curr` (huang2024high)

### Continuous DR-submodular / up-concave reward functions (71 items, 4 papers)

Add function_class value 'dr_submodular' (continuous (weakly) DR-submodular / up-concave on a down-closed box subset; monotone or not in conditions; gamma weak-submodularity as variable) with quantity alpha_regret. Re-extract continuous submodular papers.

Examples: `reward functions are non-negative, non-monotone continuous DR-submodular (maximization) and L-smooth` (lu2026upper); `constraint set K subset of [0,1]^d is down-closed and contains the origin` (lu2026upper); `feedback: one stochastic unbiased gradient query (norm <= B_1) per round at a query point different from the played acti` (lu2026upper); `regret is 1/e-regret (alpha-regret against 1/e times the best fixed point)` (lu2026upper)

## Result field

### Miscellaneous instance and side conditions (gap/range assumptions, query geometry, continuous time, random horizons) (218 items, 118 papers)

These are result conditions (gap bounds, interior optima, query-outside-domain allowances, horizon definitions, constant-scaling regimes); record them in conditions, not unmapped.

Examples: `continuous time: signals dx_a = mu_a pi_a dt + sigma_a sqrt(pi_a) dW_a` (adusumilli2022sample); `continuous-time diffusion limit with fixed experiment duration tau=1 (corresponds to n observations)` (adusumilli2022sample); `local alternatives theta_0 + h/sqrt(n) with equal reference means; regret scaled by sqrt(n)` (adusumilli2022sample); `Allocations v_i >= 0 with sum_i v_i <= V^t, volumes V^t in {1..V}; learner knows the volume bound V` (agarwal2010optimal)

### Non-standard objectives and comparators (risk measures, quantiles, ratios, lenient regret, AoI, competitive ratio, estimation, stability, mixture benchmarks) (251 items, 105 papers)

Use quantity other (or competitive_ratio / policy_regret / alpha_regret) with the functional, benchmark and comparator described in conditions; comparator field takes the closest value.

Examples: `objective trades off expected total cost sum_t c_{i_t} against the error rate, compared with omniscient benchmarks (best` (abraham2013adaptive); `objective is minimax (max over means) expected regret = simple-regret-type loss of the implemented arm plus sampling cos` (adusumilli2022sample); `minimax (over means) simple regret criterion` (adusumilli2022sample); `learner chooses adaptive stopping time bounded by T` (adusumilli2022sample)

### Context-generation assumptions (diversity/eigenvalue, margin, smoothed or i.i.d. action sets, density bounds) (185 items, 92 papers)

Keep context ∈ {stochastic, adversarial} in the setting; diversity, minimum-eigenvalue, margin (alpha) and density conditions are result conditions; smoothed adversaries use environment adversarial_smoothed.

Examples: `contexts x_t(a) in [0,1]^d for each of K arms drawn i.i.d. jointly with rewards/consumptions from an unknown distributio` (agrawal2015linear); `Unknown fixed function f(x,c) with contexts c_t in [0,1]^p chosen by an adaptive adversary` (akhavan2024conversion); `Unknown fixed f(x,c), gamma-Hölder in the context c in [0,1]^p with constant L; contexts chosen by adaptive adversary` (akhavan2024conversion); `Unknown fixed f(x,c), gamma-Hölder in the context c in [0,1]^p with constant L; contexts chosen by adaptive adversary` (akhavan2024conversion)

### Auxiliary information: offline data, warm starts, predictions/hints, multi-fidelity queries, surrogates, priors and conversational feedback (131 items, 45 papers)

Per guidance, offline data/warm starts/predictor quality go in conditions with a parameter (n_offline, prediction error E, fidelity cost); prior specifics go in conditions with bayesian_prior.

Examples: `Learner knows a set of M candidate priors, one of which is the true prior (but not which one)` (agarwal2016corralling); `the learner additionally receives the stale action-loss vector m_t = c_{t-d} before acting` (baghi2026pooling); `the instance has drift E_2 = sum_t ||c_t - m_t||_inf^2 <= E (drift budget)` (baghi2026pooling); `learner has one historical sample per period from P_t (trace) before the horizon starts` (balseiro2023robust)

## Already expressible

### What the learner knows (constants, bounds, thresholds, structure) (477 items, 276 papers)

learner_knows is open over variables.yaml since v0.5; declare missing symbols in `symbols`. Guidance: list knowledge only via learner_knows, never as unmapped.

Examples: `learner knows the number of options n` (abraham2013adaptive); `arm variances sigma_1^2, sigma_0^2 are known; learner knows the cost c` (adusumilli2022sample); `learner knows score functions, information matrices I_a and mean derivatives (sigma_a^2 = mu_dot' I^-1 mu_dot) and the c` (adusumilli2022sample); `Learner knows the volume bound V` (agarwal2010optimal)

### Noise and corruption model details (moments, symmetry, adversarial/structured noise, corruption timing and measures) (319 items, 154 papers)

noise (heavy_tailed, general_model_class, conditionally_subgaussian, exponential_family), noise_detail.variance, and the corruption node cover these; exact moment orders, symmetry, and attacker information go in conditions.

Examples: `moment order epsilon may be any positive number (not restricted to (0,1]); the moment bound B is on the uncentred moment` (agrawal2021regret); `corruption distributions are arbitrary (possibly unbounded) and may vary over time` (agrawal2023crimed); `corruption distributions are arbitrary (possibly unbounded) and may vary over time` (agrawal2023crimed); `Additive measurement noise is adversarial: only E[xi_t^2] <= sigma^2, no zero-mean or independence across rounds require` (akhavan2020exploiting)

### Resource, cost, safety, conservative, fairness and ROI constraints (303 items, 72 papers)

extras knapsack_constraints / safety_constraints / fairness + node constraints {kind, violation}; comparator best_feasible_policy. Guidance: cost-subsidy, covering/minimum-quota and ruin constraints map to constraints.kind (long_term_average / per_round_high_prob / hard_budget) with details in conditions.

Examples: `known per-round crowd costs c_i` (abraham2013adaptive); `flow sampling cost c per unit time; learner chooses an adaptive stopping time tau and pays c*tau` (adusumilli2022sample); `per-observation sampling cost C = c/n^{3/2}, small-cost asymptotics n -> infinity` (adusumilli2022sample); `d-dimensional resource consumption vectors in [0,1]^d observed for chosen action; algorithm stops when any budget is exc` (agrawal2015efficient)

### Pure-exploration answer variants (closest-to-threshold, maximin, partition, clustering, max-sample, FDR, unverifiable, k-of-top-m) (221 items, 70 papers)

Use objective general_identification / thresholding / pac_epsilon_best / mean_estimation; the specific answer map, error criterion (FDR/FWER, unverifiable PAC) and known thresholds go in conditions.

Examples: `Each sample is a categorical observation over n options; goal is to identify the mode (most probable option) of the sing` (abraham2013adaptive); `Arms (crowds) yield categorical samples over n options; all crowds share the same unique mode x*, which must be output a` (abraham2013adaptive); `Objective is the estimation loss L_n^p = (sum_k ||M_hat^k - M^k||_F^{2p})^{1/p} after a fixed budget n of samples` (andrea2026active); `Loss parameter p chosen by the learner` (andrea2026active)

### Known structure over arms (unimodal graphs, low-rank, sparsity, clusters, trees, known parameter sets, ordered means) (200 items, 69 papers)

action_space=structured_general (or linear with parameter_structure sparse/low_rank/clustered, function_class unimodal); the specific structure goes in conditions.

Examples: `Arbitrary (possibly infinite) arm set X with structure exploited by a black-box MAB algorithm (SBM)` (ailon2014reducing); `Action set X arbitrary (possibly infinite); target f* lies in a known finite class F of arbitrary functions` (amin2011bandits); `Possibly infinite function class with a finite covering oracle C(eps) (sup-norm eps-cover) available to the learner` (amin2011bandits); `Actions and contexts are joint assignments to discrete variables; expected payoff F decomposes as a sum of unknown poten` (amin2012graphical)

### Policy classes, expert advice variants and computational oracles (178 items, 66 papers)

extras.expert_advice / reward_model with comparator best_expert/best_policy and N_exp, VC/Natarajan dimension as variables; ERM/regression/argmax oracles are algorithm conditions; transductive context knowledge in conditions.

Examples: `algorithm can efficiently construct the smallest Euclidean ball containing the compact convex set X` (agarwal2011stochastic); `policy class accessed only through a cost-sensitive classification (argmax) oracle` (agarwal2014taming); `Learner has access to an offline ERM oracle over the policy class` (agarwal2016corralling); `Learner has access to an offline ERM oracle over the policy class` (agarwal2016corralling)

### Auctions, posted pricing, bilateral trade, contracts and market application models (382 items, 52 papers)

Per existing guidance: map to the underlying structure (prices/bids as continuum_other or lipschitz_metric, finite bids finite_K; win/sale-only observation as partial_monitoring; budget-balance as constraints) and put the economic model (utility form, demand model, valuation model) in conditions.

Examples: `repeated first-price auction: bid b in [0,1], utility U(b)=(v-b)F(b)` (achddou2021fast); `censored feedback: value V_t observed only when the bid wins (M_t <= B_t)` (achddou2021fast); `the learner knows the CDF F of the opponents' maximal bid` (achddou2021fast); `repeated first-price auction: bid b in [0,1], utility U(b)=(v-b)F(b)` (achddou2021fast)

### Non-stationarity measures (path length, significant shifts, drift speed, GP-evolving functions) (128 items, 45 papers)

environment nonstationary_switching / nonstationary_drifting with the measure as a variable (declare path_length P_T, significant shifts, drift rate); learner_knows for knowledge; dynamic/switching regret quantities exist.

Examples: `requests drawn independently from unknown, time-varying (non-identical) distributions P_t` (balseiro2023robust); `requests drawn independently from unknown, time-varying distributions P_t` (balseiro2023robust); `Reward functions evolve by a Gaussian Markov model f_{t+1} = sqrt(1-eps) f_t + sqrt(eps) g_{t+1} with g_t i.i.d. GP(0,k)` (bogunovic2016time); `Learner knows the variation rate eps (TV-GP-UCB uses it as input) and kernel hyperparameters` (bogunovic2016time)

### Action-set and loss-set geometry (lp balls, spheres, hypercube vertices, star-convex, unbounded domains) (87 items, 41 papers)

action_set.shape / norm_bound / parameter_set / loss_set and domain=unconstrained; specific radii and containment balls go in conditions.

Examples: `losses bounded |<l_t,x>| <= M (M not necessarily 1)` (agarwal2017price); `actions are the n! vertices (permutations) of the n-permutahedron in R^n, d = n` (ailon2013bandit); `actions are vertices of the permutahedron rescaled into [-1,1]^n (Q_n = 2/(n-1) P_n), d = n` (ailon2013bandit); `Decision set D_0 is a convex body containing the origin in its interior` (amani2019linear)

### Censored, one-bit, win-only, apple-tasting and general partial-monitoring feedback details (173 items, 39 papers)

feedback=partial_monitoring with partial_monitoring.{observability,structure}; known loss/feedback matrices, non-degeneracy and specific feedback mechanisms go in conditions. Guidance: 'loss and signal matrices known' is the default and need not be listed.

Examples: `Censored feedback: per venue i the learner observes r_i = min(v_i, s_i), allowing a subgradient of the concave reward` (agarwal2010optimal); `Integer allocations u_i >= 0 with sum_i u_i <= V^t, V^t <= V; integer liquidities s_i; censored feedback min(u_i, s_i) p` (agarwal2010optimal); `Integer allocations u_i >= 0 with sum_i u_i <= V^t, V^t <= V; integer liquidities; censored feedback min(u_i, s_i) per v` (agarwal2010optimal); `two outcomes (M=2)` (antos2010toward)

### Lipschitz / metric / X-armed smoothness (dissimilarities, hierarchical partitions, local smoothness, near-optimality dimension) (91 items, 36 papers)

action_space=lipschitz_metric with function_class lipschitz/holder_smooth; weak/local smoothness, partitions and near-optimality/zooming dimensions go in conditions and variables.

Examples: `f is gamma-Hölder in the context with constant L (class F_gamma(L)); f(.,c) belongs to a generic class F' for which an i` (akhavan2024conversion); `Unknown fixed f(x,c), gamma-Hölder in context (gamma in [0,1], gamma=0 means bounded increments only) with constant L` (akhavan2024conversion); `Arm space is a general measurable space with a dissimilarity function (not necessarily a metric) and a given hierarchica` (azar2014online); `Local smoothness only w.r.t. the maximizer: f* - f(x) <= l(x*, x) (weaker than Lipschitz)` (azar2014online)

### GP / RKHS / neural (NTK) reward details (60 items, 36 papers)

action_space=kernel_rkhs (bayesian_prior for GP samples) or reward_model.kind=neural_ntk; kernel family, k(x,x) bounds, eigendecay and NTK Gram conditions go in conditions.

Examples: `Reward r = h(x) + noise with h an arbitrary unknown function; regret compares to max_i h(x_{t,i}) each round` (ban2021exploitation); `Kernel normalised so k(x,x) <= 1` (cai2021lenient); `kernel bounded: k(x,x) <= kappa^2 on all arms` (calandriello2019gaussian); `f is a sample path of a zero-mean GP with kernel k, k(x,x) <= 1` (contal2013gaussian)

### Batching, streaming memory, switching costs, communication/quantization and replicability (80 items, 35 papers)

extras batched / rare_policy_updates / streaming_bounded_memory / switching_cost; number of passes, memory bits, movement metric and replicability go in variables/conditions.

Examples: `Batch sizes may be chosen adaptively; the learner uses at most B (= M_batch) adaptive rounds and knows B` (agarwal2022batched); `Batch sizes may be chosen adaptively; at most a given number of batches` (agarwal2022batched); `Algorithm is allowed B_pass passes over the (possibly adversarially ordered, order may change across passes) stream of a` (agarwal2022sharp); `Arm can be played only while in memory; discarded arms are forgotten until re-encountered in a later pass` (agarwal2022sharp)

### Feedback-graph details (observability classes, revelation timing, random/hidden graphs, noisy side observations) (91 items, 34 papers)

feedback_graph {observability, time_varying, knowledge, self_loops, directedness, generation}; graph quantities (independence/domination numbers) are variables; noisy/weighted side observations go in conditions.

Examples: `for the tuned bound, the learner knows upper bounds m_t on mas(G_t) (their sum) to set eta` (alon2013from); `for the tuned bound, the learner knows upper bounds alpha_t on alpha(G_t) (their sum) to set eta` (alon2013from); `graphs drawn i.i.d. each round from Erdos-Renyi model with arc density r; for the tuned bound the learner knows r` (alon2013from); `the time-t graph G_t is disclosed at the beginning of round t, before prediction (not the whole sequence in advance)` (alon2013from)

### Differential privacy variants (local, joint, shuffle, federated, label DP) (64 items, 18 papers)

extras.differential_privacy (kept coarse by v0.5 decision); the privacy model (local/central/joint/shuffle, pure vs approximate, epsilon/delta) goes in the result's conditions.

Examples: `epsilon-differential privacy w.r.t. change of an entire loss vector (sequence of predictions must be private)` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price); `epsilon-differential privacy w.r.t. change of an entire loss vector` (agarwal2017price)

### Causal bandits (interventions on causal graphs, observing non-reward variables, instruments) (143 items, 18 papers)

extras.causal (kept coarse by v0.5); graph knowledge, identifiability, interventional distributions and observed side variables go in conditions.

Examples: `Action (query) affects reward only through a stochastic observed treatment embedding z_t ~ xi_{x,a}^{theta_1} supported ` (brooks2025generator); `Learner observes the treatment embedding z_t in addition to the reward` (brooks2025generator); `Learner has an offline empirical treatment model f_1^off with KL(f_1^off || f_1) <= eps for all (x,a), obtained via simu` (brooks2025generator); `Mean reward m_2(Z,x;theta_2) under Z ~ xi is sigma_1-subgaussian; reward noise eta is sigma_2-subgaussian` (brooks2025generator)

### Click models and ranking (cascade, position-based, dependent click) (70 items, 18 papers)

feedback=cascade or semi_bandit with combinatorial.family=ordered_list and reward=click_model; the specific click model and examination assumptions go in conditions.

Examples: `Generic click model rho(a,k): click probability depends on the whole recommendation and the position; assumed to satisfy` (gauthier2022uniranka); `Reward is the number of clicks (sum over positions)` (gauthier2022uniranka); `Cascading click model with item attraction probabilities theta_i` (gauthier2022uniranka); `Position-based click model with item attraction theta_i and unknown position observation probabilities kappa_k; position` (gauthier2022uniranka)

### Sleeping arms, available/blocked actions and adaptive action-set sequences (37 items, 17 papers)

extras sleeping_arms / time_varying_action_sets with action_set.time_varying; per-action regret uses comparator conditions.

Examples: `Blocking: playing arm i makes it unavailable for the next d_i - 1 rounds (fixed, known delays d_i, across all contexts)` (basu2020contextual); `Blocking with fixed known delays d_i` (basu2020contextual); `Loss Lipschitz in z w.r.t. ||.||_V; time-varying loss functions, models and action sets` (baumgrtner2026gray); `Loss Lipschitz in z w.r.t. ||.||_V; time-varying problems` (baumgrtner2026gray)

### Strategic arms, incentivized exploration and truthful mechanisms (79 items, 13 papers)

extras.strategic_arms; incentive/truthfulness requirements and compensation objectives go in conditions/quantity other.

Examples: `arms are strategic agents with private values-per-click v_i <= v_max reported as bids; reward of arm i is v_i times a Be` (babaioff2008characterizing); `mechanism must be (dominant-strategy) truthful and normalized, with payments computable only from observed clicks` (babaioff2008characterizing); `rewards are v_i * rho_i(t) with private values v_i in [0, v_max] reported as bids and clicks rho_i(t) in {0,1} chosen by` (babaioff2008characterizing); `mechanism must be weakly truthful (truthful in expectation over its random seed for every click realization) and normali` (babaioff2008characterizing)

### Infinitely many arms, arm reservoirs and many optimal arms (32 items, 9 papers)

extras.infinitely_many_arms; reservoir regularity exponent and proportion of optimal arms are variables / conditions.

Examples: `New arms are drawn from an arm reservoir distribution; the mean reservoir is beta-regular at its right end point: E~' ep` (carpentier2015simple); `Simple regret is measured against the right end point mu* of the mean reservoir, not the best sampled arm` (carpentier2015simple); `Arm reservoir with beta-regular mean reservoir at its end point` (carpentier2015simple); `Right end point of the mean reservoir is mu* = 1` (carpentier2015simple)

## Out of scope

### State-dependent dynamics: Markov/restless/rested arms, rising/rotting, queues, MDPs and episodic RL (386 items, 72 papers)

Covered by the v0.5 scope (markovian environment, restless/rotting_or_rising/mortal extras, MDP/RL). Guidance: map rested pull-count-dependent rewards, queue-state and history-dependent rewards to environment=markovian or extras.rotting_or_rising so resolve.py drops them.

Examples: `n arms are controlled Markov chains with finite state spaces and unknown transition matrices; m of n arms activated each` (akbarzadeh2022learning); `learner observes the full state of every arm (not only rewards)` (akbarzadeh2022learning); `reward functions r^i: S^i x {0,1} -> [0, R_max] known; all arms (active and passive) yield rewards` (akbarzadeh2022learning); `regret measured against the Whittle index policy of the true model (average-reward benchmark T*J(mu))` (akbarzadeh2022learning)

### Multi-agent, federated, multiplayer-collision, matching-market and decentralized settings (454 items, 54 papers)

Covered by the v0.5 cut (extras multi_player_collision / multi_agent_cooperative / federated). Extractors should set those extras so resolve.py drops them; matching markets and Byzantine/gossip networks belong here too. No new vocabulary.

Examples: `N agents communicate through a central server; communication cost (number of communicated real numbers / bits) is a seco` (amani2022distributed); `decision set of K feature vectors drawn i.i.d. from a known distribution D per agent per round` (amani2022distributed); `communication budget between agents: expected number of communicated bits less than dN/64` (amani2022distributed); `learner has access to a side-information message M with mutual information I(M; a_*) <= 1/16` (amani2022distributed)

### Game-theoretic equilibrium objectives (Nash/duality gap, maximin, Stackelberg, persuasion, learning in games) (185 items, 25 papers)

Already excluded by extractor_out_of_scope (learning in games with equilibrium objectives). Add a resolve.py rule keyed on objective/quantity mentioning equilibrium gap so such settings are dropped even when in_scope was left true.

Examples: `arms are entries of an m x n payoff matrix; learner picks mixed strategies (x_t, y_t) for both players and observes nois` (abe2026thompson); `performance measured by cumulative duality gap sum_t Gap(x_t,y_t)` (abe2026thompson); `payoff matrix assumed to have a unique Nash equilibrium` (abe2026thompson); `arms are entries of a payoff matrix; learner controls both players' mixed strategies` (abe2026thompson)

### Multi-objective / vector-valued rewards (Pareto sets, Pareto regret, lexicographic, hypervolume) (145 items, 24 papers)

Excluded by v0.5 (multi-objective vector rewards). Extractor should set in_scope=false; a fixed known scalarisation of a vector reward may instead be treated as a scalar reward.

Examples: `D-dimensional vector-valued cost feedback in [0,1]^D, components possibly dependent` (busafekete2017multi); `objective is the GGI (non-linear convex aggregation with known non-increasing weights w) of the average cost vector` (busafekete2017multi); `comparator is the best mixed strategy alpha* over arms (GGI of mu alpha*), not the best single arm` (busafekete2017multi); `learner knows the GGI weights w` (busafekete2017multi)

### Quantum oracle access (84 items, 17 papers)

Already excluded by v0.5 (quantum oracle access); add a resolve.py rule so settings with quantum feedback are dropped even when extractors left in_scope=true.

Examples: `Arms are two-qubit quantum states measured with a fixed known Witness Basis Measurement; the target quantity S_E(rho_i) ` (bharati2024batch); `Promise that exactly one arm lies below the threshold zeta = 0; the learner knows the threshold` (bharati2024batch); `The confidence width uses the sub-Gaussian scale sigma of the samples` (bharati2024batch); `Arms are two-qubit quantum states measured with a Witness Basis Measurement; target is a quadratic functional S_E(rho_i)` (bharati2024batch)

### Offline / logged data, policy evaluation and statistical inference without interaction (69 items, 13 papers)

Non-interactive problems (offline policy learning/evaluation, confounded logged data, passive estimation, inference CIs) are excluded by v0.5; set in_scope=false.

Examples: `offline logged data collected by a confounded behaviour policy` (chen2023unified); `unmeasured confounder U` (chen2023unified); `instrumental variable side observation` (chen2023unified); `contexts and side observations missing not at random` (chen2023unified)

### Attacker objectives (reward/context poisoning cost to force a target arm) (27 items, 8 papers)

Guarantees for an attacker rather than the learner are excluded by v0.5; extractor should set in_scope=false.

Examples: `attacker perturbs rewards observed by the learner after the arm is chosen; objective is forcing target-arm pulls at subl` (garcelon2020adversarial); `expected rewards <theta_a, x> in (0,1]` (garcelon2020adversarial); `attacker alters contexts seen by the learner before it acts; cost is ||x_t - x~_t||_2` (garcelon2020adversarial); `attacker knows a lower bound nu on target-arm rewards (Assumption 2)` (garcelon2020adversarial)
