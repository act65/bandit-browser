# Extraction schema and prompt (v0.2, bandits ontology v0.2)

This file has three parts:

1. **The prompt**: the system prompt given to the LLM extractor, verbatim (everything inside the `PROMPT` fence).
2. **Controlled vocabulary**: the bandits ontology, maintained in [`ontology/bandits-0.2.yaml`](ontology/bandits-0.2.yaml) and rendered into the prompt by `pipeline/extract.py`.
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
4. **Expressions** must be SymPy-parseable strings using the canonical variables below. If the bound uses a quantity not in the vocabulary, define it in `symbols` with a one-line meaning, and use that symbol. If a canonical symbol is used with a different meaning in the paper (e.g. the paper's L is a log factor), rename it and declare the new name in `symbols`. Use the conventions below for sums over arms.
5. **One result per formal statement and per bound.** If one theorem gives both a gap-dependent and a minimax bound, produce two results with the same `source.label`.
6. **Provenance is mandatory.** Every result gets the LaTeX label (if any), the number as printed (e.g. "Theorem 3.2"), and a verbatim quote of the statement (the LaTeX is fine, truncated to ~600 characters if needed).
7. **Novelty**: set `is_new` to false for results the paper restates from prior work (e.g. "Theorem 1 (Lai & Robbins)"); put those in `cited_results` instead of `results`.
8. **Confidence**: for each result, give `confidence` in {high, medium, low} and a short `notes` field explaining anything you were unsure about.
9. If a field is not stated in the paper, use `null` (or `not_stated` where offered). Do not guess.
10. `function_class` and `domain` apply to continuous action sets (convex bodies, Lipschitz/metric spaces). For finite or linear-finite action sets use `function_class: []` and `domain: not_applicable`.
11. `parameters` on a setting records constraints that define the node, e.g. {"d": "1"} for one-dimensional problems or {"K": "2"} for two-armed bandits; use {} if none.
12. `compute`: whether the algorithm behind an upper bound runs in polynomial time per round, as stated or clearly implied by the paper; `non_constructive` for existence proofs; `not_stated` otherwise and for lower bounds.
13. Output a single JSON object matching the schema below, and nothing else.

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
| L_feat      | bound on the action/feature norm, ‖x‖ ≤ L_feat (if the paper bounds ‖x‖², say so in `symbols`) |
| L_lip       | Lipschitz constant of the loss/reward |
| lam         | regularisation parameter λ (ridge / self-normalised bounds) |
| diam_K      | diameter of the action set K |
| vartheta    | self-concordance parameter of a barrier on K |
| alpha       | strong-convexity parameter |
| beta        | smoothness parameter |
| p           | smoothness order (highly smooth classes) |
| m           | size of a combinatorial action (number of base arms selected) |
| C           | total corruption budget |
| S_T         | number of switches / changes of the environment (non-stationary) |
| V_T         | total variation budget (non-stationary) |
| D           | delay (fixed), or D_total for total delay (not the diameter: use diam_K) |
| B           | budget (knapsacks / constrained) |
| N           | number of agents/players |
| H           | episode length (if an episodic structure appears) |
| gamma_T     | maximum information gain (kernel / GP bandits) |
| KL_i        | KL divergence used in instance-dependent lower bounds for arm i |

Sum over suboptimal arms: write `sum_subopt(<expr in Delta_i, KL_i>)`, e.g. `sum_subopt(log(T)/Delta_i)`.
Sum over all arms: `sum_arms(<expr>)`. Polylog factors kept explicitly: use `log(...)`.

## Output schema (JSON)

{
  "schema_version": "0.2",
  "ontology_version": "bandits-0.2",
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
      "function_class": [<vocab>],      // [] unless continuous action set
      "domain": <vocab>,
      "context": <vocab>,
      "noise": <vocab>,
      "learner_knows": [<vocab>],       // e.g. ["T", "sigma"]
      "extras": [<vocab>],              // e.g. ["delayed_feedback"]
      "parameters": { str: str },       // node-defining constraints, e.g. {"d": "1"}; {} if none
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
      "compute": "polynomial" | "exponential" | "non_constructive" | "not_stated",
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
    "probability": "expectation", "horizon": "anytime", "compute": "polynomial",
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
with setting s1 = {objective: cumulative_regret, feedback: bandit, environment: stochastic_iid, action_space: finite_K, function_class: [], domain: not_applicable, context: none, noise: bounded_01, learner_knows: [], extras: [], parameters: {}}.
````

---

## 2. Controlled vocabulary

The vocabulary lives in [`ontology/bandits-0.2.yaml`](ontology/bandits-0.2.yaml), which is the single source of truth. `pipeline/extract.py` renders it into the prompt in place of `{{ONTOLOGY}}`, and `pipeline/schema.py` turns it into the JSON Schema enums. Version history:

- **v0.1** ([`ontology/bandits-0.1.yaml`](ontology/bandits-0.1.yaml)): dimensions objective, feedback, environment, action_space, context, noise, learner_knows and extras; per-dimension orders; K-armed → linear reduction.
- **v0.2**: added the `function_class` (multi-select) and `domain` (improper ⊑ constrained, improper ⊑ unconstrained) dimensions, so bandit convex optimisation is expressible. Also added node `parameters` and a result-level `compute` field. New values: noise `conditionally_subgaussian` and `noise_free`, feedback `two_point`, environment `adversarial_unspecified`, objective `epsilon_optimal_point`, quantities `regret_unspecified` and `minimax_bayesian_regret`. `L` is split into `L_feat` / `L_lip`, and BCO variables are added. Driven by [`data/ground_truth/bco-ontology-notes.md`](data/ground_truth/bco-ontology-notes.md) and the OFUL test extraction. Deferred to Phase 3: constraint-set geometry and typed edge kinds.

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
