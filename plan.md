# Plan

Staged so that each phase ends with a **go / no-go check**. We do not scale extraction until the schema and accuracy are proven on a small, hand-checked set ([desiderata.md](desiderata.md) D6).

## Phase 0: Foundations (now)

- [x] Repository and docs: README, motivation, desiderata, related work, schema draft.
- [x] Literature sweep. No existing system does this; ISGCI, π-Base and the Equational Theories Project are the precedents to position against ([related-work.md](related-work.md)).
- [x] License: MIT for code, CC-BY-4.0 for data (as π-Base).
- [ ] Reach out (optional, once there is a demo): Lean Machine Learning / Degenne (closest potential overlap), π-Base (engineering, valued properties).

## Phase 1: Ontology v0 and gold set (pilot slice)

**Scope:** stochastic and adversarial K-armed bandits, plus linear bandits. This is small enough to check by hand, and it contains a known cross-dimension reduction (K-armed → linear) and known gap/closure histories.

- [x] Select about 50 papers in this slice: [`corpus/manifest.yaml`](corpus/manifest.yaml) has 59 papers (53 on arXiv, 6 non-arXiv classics), all with verified ids.
- [x] Extract all 53 arXiv papers with the pipeline (Phase 2 tooling, built early): 166 settings → 60 canonical nodes, 354 results, 282 cited results. 48/53 files pass all automatic checks ([`data/validation-report.md`](data/validation-report.md)). About $34 at API prices, run on the subscription through `claude -p`.
- [ ] The 6 non-arXiv classics (Lai & Robbins, UCB1, EXP3, MOSS/INF, Dani et al., SupLinUCB) are not extracted yet. They hold key lower bounds for the acceptance facts (F01, F05), so add a PDF path or enter them by hand.
- [ ] Gold set: **human-verify** 15–20 of the LLM extractions instead of annotating from scratch (cheaper), and record corrections. Suggested first: OFUL, KL-UCB, Tsallis-INF, Lattimore & Szepesvári 2017, Li et al. 2019, Garivier et al. 2016.
- [x] Ontology v0.2 ([`ontology/bandits-0.2.yaml`](ontology/bandits-0.2.yaml)): function_class and domain dimensions, new noise/feedback/objective/quantity values, node parameters, `compute` field.
- [x] Ontology v0.3 ([`ontology/bandits-0.3.yaml`](ontology/bandits-0.3.yaml)): applies [`ontology/review-v0.2.md`](ontology/review-v0.2.md) (action_set, instance_assumptions, learner knowledge, adversary refinements, comparator, in_scope), plus registries in the prompt. Corpus re-extracted.
- [ ] Fix the per-dimension orders together with their justification and validity scope (D1).
- [x] Write down 5–10 **known facts the system should rediscover** ([`data/ground_truth/pilot-facts.yaml`](data/ground_truth/pilot-facts.yaml), 14 facts, still to be verified by hand) (e.g. which settings are tight up to constants, up to logs, or open; historic gaps and the papers that closed them). These are the Phase 3 acceptance tests.
- [ ] Ready-made ground truth from related work:
  - [x] Lattimore's *Bandit Convex Optimisation* → [`data/ground_truth/bco.yaml`](data/ground_truth/bco.yaml) (19 settings, 40 results, 20 transfer rules, 27 open problems; v5): Tables 2.1 and 2.2 (bounds), §2.4 (transfer rules) and Chapter 14 (open problems).
  - Slivkins' problem-space axes, as a check on the ontology dimensions.
  - COLT open problems in the pilot slice.
  - **Decision:** K-armed and linear bandits stay the primary pilot, because the gold set must be checked by hand and this slice is familiar. Bandit convex optimisation becomes the *second* slice in Phase 4. Its clean ground truth (the BCO tables) then serves as a test of generalisation: can the pipeline reproduce a published table of bounds in a setting family it was not tuned on?

**Exit check:** the schema can express every result in the gold set without abuse of the `unmapped` field.

## Phase 2: Extraction pipeline

- [x] Corpus fetcher: arXiv LaTeX source (plus metadata from Semantic Scholar / OpenAlex), stored per paper with a manifest. Downloaded sources are treated as untrusted data and never executed.
- [x] Pre-processor: flatten `\input`s, expand user macros, pull theorem-like environments, the setting/problem-formulation section, comparison tables and the bibliography.
- [x] Extractor (single pass, `claude -p --json-schema`, all tools disabled).
- [ ] Extractor improvements: compare single-pass and two-pass designs. Add ChatExtract-style follow-up questions for bound expressions, and use self-consistency across repeated runs.
- [x] Validator: JSON schema (pydantic), vocabulary checks, SymPy parse of every expression, and checks that every quote occurs in the source (shingle overlap ≥ 0.5, tolerant of LaTeX reflow). Bound values are the known weak point of extraction (related-work §3), so most checking effort goes there.
- [ ] Evaluation harness against the gold set: per-field precision and recall for settings, bounds (expression equivalence via SymPy) and assumptions.

**Exit check:** accuracy on the gold set reaches the agreed bar (to be set, e.g. ≥ 90% of bounds exactly right and ≥ 95% of settings right), and every error type is understood.

## Phase 3: Graph and inference engine

- [x] **Canonical notation layer (D13)**, prerequisite for comparison (built before the v0.3 re-extraction; `pipeline/resolve.py` → `data/canonical/`):
  - `ontology/variables.yaml`: a symbol registry with precise definitions, aliases and conversion rules (e.g. ‖x‖² ≤ L ⇒ L_feat = √L; σ as std vs sub-Gaussian parameter). It generates the prompt's variable table; declared `symbols` are clustered into registry proposals.
  - `data/algorithms.yaml`: an algorithm registry (canonical id, aliases, introducing paper, techniques), resolved by name normalisation, then LLM adjudication, then human confirmation.
  - Citation resolution: `cited_key` → .bbl title → arXiv/DOI → manifest id. Unmatched cited papers become corpus candidates.
- [ ] **Next:** inherited results on setting pages. The v0.3 key is exact (124 nodes from 175 settings, many with one paper), so each node should show its own results plus those inherited along specialisation edges, with derivation paths. Product-order edges are already computed for the graph view.
- [ ] Build the setting poset: per-dimension orders → product order, plus explicit cross-dimension reductions with parameter maps.
- [ ] Inference: propagate upper bounds down and lower bounds up, translating through parameter maps and storing derivation paths separately from extracted results.
- [ ] Bound comparison (D2): normalise to regime-specific forms (e.g. exponent vectors plus a polylog flag), compute dominance and the Pareto front, and assign a tightness status per setting and regime.
- [ ] Reports: gaps, missing lower bounds, unstudied neighbours, redundant results (D8).
- [ ] Gap triage: run a targeted retrieval search for each candidate gap before labelling it open; mark it open vs blank; log negative searches.

**Exit check:** the acceptance tests from Phase 1 pass, i.e. known gaps and tight results are rediscovered from extracted data alone.

## Phase 4: Scale to the full bandit literature (~1000–3000 papers)

- [ ] Corpus building: snowball through citations from seed surveys and books, plus arXiv category/keyword search, plus COLT/ALT/NeurIPS/ICML/AISTATS proceedings. Dedupe.
- [ ] Extend the ontology module by module (contextual, combinatorial, non-stationary, pure exploration, partial monitoring, …), each with a small gold set.
- [ ] Cross-check with `cited_results` to flag conflicts, and run a human verification queue that prioritises results that drive gap reports.
- [ ] Cost tracking: order of 10⁷–10⁸ tokens in total, so cheap; the real constraint is human review time.

## Phase 5: Browsing and outputs

- [x] Minimal static site ([`site/`](site/)), deployed by GitHub Actions to act65.github.io/bandit-browser.
- [x] Graph view: Hasse diagram of the product order over settings (Cytoscape), redesigned tables with canonical bound rendering (SymPy → LaTeX), neighbourhood panels.
- [ ] Full website: one page per setting with bound tables (filter by regime), the Hasse-diagram neighbourhood view, provenance links and gap badges.
- [ ] Published open-problems list generated from the gap reports, plus a status tracker for COLT open problems (none exists today).
- [ ] Contribution workflow: corrections via PR or an issue template.
- [ ] Later: natural-language query interface answered from the graph, with citations.

## Phase 6: Generalise beyond bandits

- [ ] Split the domain-agnostic core from the bandits ontology module (this should be mostly true by construction, D3).
- [ ] Second domain as a generality test: candidates are online convex optimisation, RL theory (tabular/linear MDPs) or stochastic convex optimisation rates.

## Technical stack (proposal)

- Python with `uv`; pydantic for the schema; SymPy for bounds; networkx for the poset.
- Data: π-Base-style layout. One YAML (or Markdown with YAML frontmatter) file per paper, setting, edge and result in `data/`, with stable IDs, and CI that checks schema validity and consistency (no upper bound below a lower bound on the same setting and regime). Derived artefacts are built by script (D7). arXiv sources are not rehosted (licence); we store extracts and links.
- LLM: Claude via the Anthropic API, with prompt caching for the long fixed prompt and the Batch API for corpus-scale runs.
- Site: a static site generator built from the data directory.

## Open decisions

1. The accuracy bar for Phase 2 to Phase 3.
2. Whether lemmas are extracted in v0 (proposal: no).
3. Representation of "T large enough" and hidden problem-dependent constants.
4. The human verification process: who verifies, and how much is verified before publishing.
5. Project name: "bandit-browser" fits the pilot; the general system may need a broader name later.
