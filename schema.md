# Extraction schema and prompt (draft v0.1, bandits ontology)

This file has three parts:

1. **The prompt**: the system prompt given to the LLM extractor, verbatim (everything inside the `PROMPT` fence).
2. **Controlled vocabulary**: the bandits ontology v0.1, which is pasted into the prompt.
3. **Design notes**: why the schema looks the way it does, and open questions.

The core of the schema (`paper`, `results`, `bound`, provenance) is domain-agnostic ([desiderata.md](desiderata.md) D3). Only the `setting` dimensions and the variable vocabulary are bandit-specific.

---

## 1. Prompt

````text PROMPT
You are an expert in theoretical machine learning extracting structured results from a research paper. You will be given the LaTeX source of one paper. Your job is to record every formal result about performance guarantees (upper bounds and lower bounds) that the paper states, mapped onto a fixed ontology. Precision matters more than coverage: a wrong record is worse than a missing one.

## What to extract

For each theorem, corollary, proposition or lemma that states a performance guarantee (regret, sample complexity, error probability, …) for a problem setting, produce one entry in `results`. Skip purely technical lemmas (concentration inequalities, algebraic facts) unless they are themselves a performance guarantee for a setting.

Also extract:
- `settings`: each distinct problem setting the paper studies, mapped to the controlled vocabulary.
- `algorithms`: each algorithm the paper proposes or analyses.
- `cited_results`: bounds that the paper attributes to *other* papers, typically in comparison tables or related-work sections. These are used for cross-checking, so record them as the paper states them, with the citation key.

## Rules

1. **Use only the controlled vocabulary** for setting dimensions. If a feature of the setting cannot be expressed with the vocabulary, describe it in `unmapped` in plain words. Never stretch a vocabulary term to cover something it doesn't mean.
2. **Do not infer or strengthen.** Record exactly what the theorem states. If the theorem says "with probability at least 1−δ", the bound is high-probability; do not convert it to expectation. If constants are given, keep them. If the paper writes Õ, record Õ.
3. **Hidden assumptions matter.** Assumptions stated anywhere that the theorem depends on (in the theorem, in a referenced "Assumption 2", in the setting section, in footnotes) go into the setting or into `extra_assumptions`. Common ones: known horizon T, rewards in [0,1], sub-Gaussian noise with known σ, unique optimal arm, bounded parameter norm ‖θ‖ ≤ S, a finite or bounded action set.
4. **Expressions** must be SymPy-parseable strings using the canonical variables below. If the bound uses a quantity not in the vocabulary, define it in `symbols` with a one-line meaning, and use that symbol. Use the conventions below for sums over arms.
5. **One result per formal statement and per bound.** If one theorem gives both a gap-dependent and a minimax bound, produce two results with the same `source.label`.
6. **Provenance is mandatory.** Every result gets the LaTeX label (if any), the number as printed (e.g. "Theorem 3.2"), and a verbatim quote of the statement (the LaTeX is fine, truncated to ~600 characters if needed).
7. **Novelty**: set `is_new` to false for results the paper restates from prior work (e.g. "Theorem 1 (Lai & Robbins)"); put those in `cited_results` instead of `results`.
8. **Confidence**: for each result, give `confidence` in {high, medium, low} and a short `notes` field explaining anything you were unsure about.
9. If a field is not stated in the paper, use `null`. Do not guess.
10. Output a single JSON object matching the schema below, and nothing else.

## Canonical variables

| symbol      | meaning |
|-------------|---------|
| T           | horizon (number of rounds) |
| K           | number of arms / actions (finite) |
| d           | dimension (linear, contextual, kernel features) |
| Delta_i     | gap of arm i: mu_star - mu_i |
| Delta_min   | smallest positive gap |
| Delta_max   | largest gap |
| mu_star     | optimal mean reward |
| sigma       | noise scale (sub-Gaussian parameter or standard deviation) |
| delta       | failure probability (high-probability bounds; fixed-confidence BAI) |
| epsilon     | accuracy (PAC / epsilon-best arm) |
| S           | norm bound on the unknown parameter, ‖theta‖ ≤ S |
| L           | bound on the action/feature norm, or Lipschitz constant (state which in `symbols`) |
| m           | size of a combinatorial action (number of base arms selected) |
| C           | total corruption budget |
| S_T         | number of switches / changes of the environment (non-stationary) |
| V_T         | total variation budget (non-stationary) |
| D           | delay (fixed), or D_total for total delay |
| B           | budget (knapsacks / constrained) |
| N           | number of agents/players |
| H           | episode length (if an episodic structure appears) |
| gamma_T     | maximum information gain (kernel / GP bandits) |
| KL_i        | KL divergence used in instance-dependent lower bounds for arm i |

Sum over suboptimal arms: write `sum_subopt(<expr in Delta_i, KL_i>)`, e.g. `sum_subopt(log(T)/Delta_i)`.
Sum over all arms: `sum_arms(<expr>)`. Polylog factors kept explicitly: use `log(...)`.

## Output schema (JSON)

{
  "schema_version": "0.1",
  "ontology_version": "bandits-0.1",
  "paper": {
    "title": str,
    "arxiv_id": str | null,
    "arxiv_version": str | null,
    "year": int | null,
    "authors": [str]
  },
  "settings": [
    {
      "id": "s1",                       // local id, referenced by results
      "name_in_paper": str,             // what the paper calls it
      "objective": <vocab>,
      "feedback": <vocab>,
      "environment": <vocab>,
      "action_space": <vocab>,
      "context": <vocab>,
      "noise": <vocab>,
      "learner_knows": [<vocab>],       // e.g. ["T", "sigma"]
      "extras": [<vocab>],              // e.g. ["delayed_feedback"]
      "unmapped": [str],                // plain-language features not covered by the vocabulary
      "definition_quote": str           // verbatim quote of the setting definition
    }
  ],
  "algorithms": [
    {
      "id": "a1",
      "name": str,                      // as named in the paper, e.g. "UCB-V"
      "is_new": bool,                   // proposed in this paper?
      "techniques": [<vocab>],          // e.g. ["optimism", "elimination"]
      "requires_knowledge_of": [str]    // inputs the algorithm needs, e.g. ["T", "Delta_min"]
    }
  ],
  "results": [
    {
      "id": "r1",
      "setting": "s1",
      "side": "upper" | "lower",
      "algorithm": "a1" | null,         // upper bounds: the algorithm; lower bounds: null
      "algorithm_class": "all" | "consistent" | "uniformly_good" | "other" | null,  // lower bounds only
      "quantity": <vocab>,              // e.g. "pseudo_regret"
      "dependence": "worst_case" | "instance_dependent",
      "probability": "expectation" | "high_probability" | "almost_sure" | "asymptotic",
      "horizon": "known" | "anytime" | "not_applicable",
      "bound": {
        "notation": "exact" | "O" | "O_tilde" | "Theta" | "Omega" | "Omega_tilde" | "liminf" | "limsup",
        "expression": str,              // SymPy-parseable, canonical variables
        "expression_latex": str,        // as written in the paper
        "regime": str | null            // conditions such as "T >= K", "d <= K", "for T large enough"
      },
      "symbols": { str: str },          // any symbol used that is not in the canonical table
      "extra_assumptions": [str],       // beyond the setting, e.g. "unique optimal arm"
      "is_new": true,
      "source": {
        "label": str | null,            // LaTeX \label, e.g. "thm:main"
        "number": str,                  // e.g. "Theorem 3.2"
        "quote": str
      },
      "confidence": "high" | "medium" | "low",
      "notes": str
    }
  ],
  "cited_results": [
    {
      "cited_key": str,                 // bib key as in the LaTeX
      "cited_title": str | null,        // from the .bib / .bbl if available
      "algorithm_name": str | null,
      "side": "upper" | "lower",
      "setting_description": str,       // free text; may be mapped later
      "bound": { "notation": ..., "expression": str, "expression_latex": str, "regime": str | null },
      "where": str                      // e.g. "Table 1", "Section 2"
    }
  ]
}

## Controlled vocabulary

{{ONTOLOGY}}

## Example (illustrative)

Input excerpt:
  \begin{theorem}\label{thm:ucb1} For all K>1, if policy UCB1 is run on K machines having arbitrary reward distributions P_1,...,P_K with support in [0,1], then its expected regret after any number n of plays is at most
  \[ 8 \sum_{i:\mu_i<\mu^*} \frac{\ln n}{\Delta_i} + \Big(1+\frac{\pi^2}{3}\Big)\sum_{j=1}^K \Delta_j . \]
  \end{theorem}

Output result:
  {
    "id": "r1", "setting": "s1", "side": "upper", "algorithm": "a1", "algorithm_class": null,
    "quantity": "pseudo_regret", "dependence": "instance_dependent",
    "probability": "expectation", "horizon": "anytime",
    "bound": {
      "notation": "exact",
      "expression": "8*sum_subopt(log(T)/Delta_i) + (1 + pi**2/3)*sum_arms(Delta_i)",
      "expression_latex": "8 \\sum_{i:\\mu_i<\\mu^*} \\frac{\\ln n}{\\Delta_i} + (1+\\frac{\\pi^2}{3})\\sum_{j=1}^K \\Delta_j",
      "regime": null
    },
    "symbols": {},
    "extra_assumptions": [],
    "is_new": true,
    "source": {"label": "thm:ucb1", "number": "Theorem 1", "quote": "For all K>1, if policy UCB1 is run on K machines ..."},
    "confidence": "high",
    "notes": "Paper's n is the horizon T. 'Expected regret' here is defined via expected pull counts, i.e. pseudo-regret. Bound holds for any n, so anytime."
  }
with setting s1 = {objective: cumulative_regret, feedback: bandit, environment: stochastic_iid, action_space: finite_K, context: none, noise: bounded_01, learner_knows: [], extras: []}.
````

---

## 2. Controlled vocabulary: bandits ontology v0.1

This is substituted for `{{ONTOLOGY}}` in the prompt. In each dimension, `a ⊑ b` means **a is a special case of b**; these per-dimension orders generate the product order on settings ([desiderata.md](desiderata.md) D1). The orders listed are a first pass and each one needs a justification and a validity scope before it is used for inference.

### objective
- `cumulative_regret`
- `simple_regret`
- `bai_fixed_confidence`: best-arm identification, fixed confidence (sample complexity)
- `bai_fixed_budget`: best-arm identification, fixed budget (error probability)
- `pac_epsilon_best`: find an ε-optimal arm with probability ≥ 1−δ
- `top_m_identification`
- `other_pure_exploration`

### feedback
- `full_information` (experts)
- `semi_bandit`
- `bandit`
- `graph_feedback`: side observations given by a feedback graph
- `partial_monitoring`
- `dueling`: relative/preference feedback

Order (more feedback ⊑ less feedback, because an algorithm for less feedback can ignore the extra observations): `full_information ⊑ graph_feedback ⊑ bandit`, `semi_bandit ⊑ bandit` (for combinatorial actions), `bandit ⊑ partial_monitoring`. See the design notes for the definition of ⊑.

### environment
- `stochastic_iid`
- `stochastic_corrupted`: stochastic with an adversarial corruption budget C
- `adversarial_oblivious`
- `adversarial_adaptive`
- `nonstationary_switching`: piecewise stationary, S_T switches
- `nonstationary_drifting`: variation budget V_T
- `markovian`: rested or restless Markov arms

Order: `stochastic_iid ⊑ stochastic_corrupted`, `stochastic_iid ⊑ nonstationary_switching ⊑ adversarial_oblivious ⊑ adversarial_adaptive` (validity depends on the regret notion).
Note: "best of both worlds" is **not** an environment; it is a single algorithm with results in several settings. Record one result per setting.

### action_space
- `finite_K`
- `linear_finite`: finite action set in ℝᵈ, linear reward
- `linear_infinite`: compact/convex action set in ℝᵈ, linear reward
- `generalized_linear`
- `combinatorial`: subsets of base arms, typically with a size bound m
- `convex`: bandit convex optimisation
- `lipschitz_metric`: arms in a metric space, Lipschitz reward
- `kernel_rkhs`: reward in an RKHS / Gaussian-process bandits
- `continuum_other`

Cross-dimension reductions (explicit edges with parameter maps): `finite_K → linear_finite` (d ↦ K, canonical basis), `linear_finite → generalized_linear` (identity link), `linear_infinite → kernel_rkhs` (linear kernel).

### context
- `none`
- `stochastic_contexts`
- `adversarial_contexts`

### noise
- `bounded_01`
- `bernoulli`
- `subgaussian`
- `gaussian_known_variance`
- `exponential_family`
- `heavy_tailed`: bounded (1+ε)-th moment
- `not_applicable`: e.g. adversarial losses

### learner_knows (multi-select)
`T`, `sigma`, `Delta_min`, `S`, `C`, `S_T`, `V_T`, `D`, `gamma_T`, `K`, `d`

### extras (multi-select)
`delayed_feedback`, `batched`, `switching_cost`, `differential_privacy`, `knapsack_constraints`, `safety_constraints`, `multi_player_collision`, `multi_agent_cooperative`, `federated`, `fairness`, `sleeping_arms`, `mortal_arms`, `rotting_or_rising`, `causal`, `strategic_arms`, `budgeted_exploration`, `infinitely_many_arms`, `restless`

### techniques (multi-select)
`optimism`, `thompson_sampling`, `elimination`, `explore_then_commit`, `epsilon_greedy`, `exponential_weights`, `ftrl_or_mirror_descent`, `information_directed_sampling`, `track_and_stop`, `gittins_or_bayes_optimal`, `doubling_trick`, `restarts_or_sliding_window`, `lower_bound_change_of_measure`, `lower_bound_minimax_construction`, `other`

### quantity
`pseudo_regret`, `expected_regret`, `high_probability_regret`, `bayesian_regret`, `simple_regret`, `sample_complexity`, `error_probability`, `dynamic_regret`, `switching_regret`, `other`

---

## 3. Design notes and open questions

**Why LaTeX and not PDF.** Theorem environments, `\label`s and maths are exact in the source. The pipeline should pre-extract `theorem`/`corollary`/`proposition`/`lemma`/`assumption`/`definition` environments plus the setting section, which cuts tokens. It should also resolve `\newcommand` macros, because papers define their own shorthand for regret, gaps and so on.

**Why `cited_results`.** Comparison tables in later papers give an independent second reading of earlier results. Disagreements between a paper's own theorem and how others cite it are a cheap error signal (D5).

**Feedback direction subtlety.** For feedback, "more information" makes the problem easier: an upper bound for `bandit` feedback transfers to `full_information` (an algorithm can ignore extra observations), and a lower bound for `full_information` transfers to `bandit`. So in the inference engine, `full_information ⊑ bandit` in the sense used by D1 ("upper bounds flow from ⊒ to ⊑"). All per-dimension orders are stated in this one sense: **S ⊑ S′ iff any algorithm for S′ can be run on S with at most the same guarantee** (after the parameter map). This means "special case" in the reduction sense, which is not always the intuitive sense: graph feedback is a "special case" of bandit feedback here. Each order in the vocabulary must be checked against this definition before inference is built.

**Open questions**
1. Do we need a bound-comparison DSL beyond SymPy (e.g. exponent vectors in (T, K, d, 1/Δ) plus a polylog flag) to make D2 dominance checks robust?
2. How should we represent results that hold "for T large enough", or that come with problem-dependent constants hidden in the O?
3. Should lemmas be extracted at all in v0? It is probably better to restrict to theorem/corollary/proposition first.
4. One call per paper, or a two-pass design (pass 1: settings and algorithms; pass 2: results given the pass-1 setting ids)? Two passes are probably more accurate; decide in the pilot.
5. Lower-bound algorithm classes (consistent, uniformly good, …) need precise definitions in the vocabulary.
6. The related-work sweep shows the schema needs more result kinds than upper and lower bounds:
   - **reduction / edge results**, e.g. "setting A reduces to B with this parameter map";
   - **separations**;
   - **classification theorems** over a parameterised family (partial monitoring, feedback graphs);
   - **conditional results**, under a conjecture.
   Proposal: add a `kind` field to `results` in v0.2 once the gold set shows how often each occurs ([desiderata.md](desiderata.md) D1, D11).
7. Parameterised settings (independence number α, Bellman–Eluder dimension, …) need a way to declare node parameters in the setting, not only in the bound.
