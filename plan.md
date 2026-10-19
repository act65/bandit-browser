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
- [x] Non-arXiv classics: `pipeline/fetch_pdf.py` (pdftotext, with two-column detection) → 5 of 6 extracted from PDF text (UCB1, EXP3, MOSS, Dani et al., SupLinUCB).
- [ ] Lai & Robbins 1985: all automated legal routes tried and failed. The Elsevier open archive serves a bot check, the Rutgers academic copy's server is retired, and the Internet Archive has no copy. Its main result is in the graph via the Bubeck & Cesa-Bianchi survey's restatement (Thm 2.2), so F02 passes; only first-hand provenance is missing. Needs a manual browser download: Save the PDF by hand to `corpus/src/lai1985asymptotically/paper.pdf`, then run `fetch_pdf.py --only lai1985asymptotically` and extract.
- [ ] Gold set: **human-verify** 15–20 of the LLM extractions instead of annotating from scratch (cheaper), and record corrections. Suggested first: OFUL, KL-UCB, Tsallis-INF, Lattimore & Szepesvári 2017, Li et al. 2019, Garivier et al. 2016.
- [x] Ontology v0.2 ([`ontology/bandits-0.2.yaml`](ontology/bandits-0.2.yaml)): function_class and domain dimensions, new noise/feedback/objective/quantity values, node parameters, `compute` field.
- [x] Ontology v0.3 ([`ontology/bandits-0.3.yaml`](ontology/bandits-0.3.yaml)): applies [`ontology/review-v0.2.md`](ontology/review-v0.2.md) (action_set, instance_assumptions, learner knowledge, adversary refinements, comparator, in_scope), plus registries in the prompt. Corpus re-extracted.
- [x] Per-dimension orders with justification, caveats, comparator scope and value maps (`order_notes`, `value_maps` in the ontology), used by `pipeline/order.py` along the chain of edges.
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
- [x] Extraction tests (`data/extraction-tests.md`): self-consistency on 6 papers × 3 runs, and the `pipeline/verify.py` verification pass (planted-error recall 12/12; on real data 6 right / 2 debatable / 3 wrong corrections, the wrong ones low-confidence).
- [x] Improvements adopted: printed theorem numbers computed in preprocessing; prompt rules 5–6 and 17–20 (case splits, corollary policy, upper/lower-bound knowledge, instance assumptions, quantity by definition, symbol naming); quantity definitions in the ontology; algorithm knowledge merged into upper-bound settings in `resolve.py`.
- [x] Re-extracted the corpus with the improved prompt (schema 0.4, about $38 equivalent): theorem numbers match the counter emulation 268/270 (was about 73%). `verify.py` run over all 58 papers → `data/extractions_verified/` (review queue, never auto-applied to `data/extractions/`). Result: 4 corrections and 7 missing-result flags across 58 papers; the 6 flagged papers are the first human-review queue (`data/extraction-tests.md` §5).
- [ ] Not adopted (for now): two-pass extraction, 2-of-3 voting (it outvoted the one correct run in the tests). Original item: compare single-pass and two-pass designs. Add ChatExtract-style follow-up questions for bound expressions, and use self-consistency across repeated runs.
- [x] Validator: JSON schema (pydantic), vocabulary checks, SymPy parse of every expression, and checks that every quote occurs in the source (shingle overlap ≥ 0.5, tolerant of LaTeX reflow). Bound values are the known weak point of extraction (related-work §3), so most checking effort goes there.
- [ ] Evaluation harness against the gold set: per-field precision and recall for settings, bounds (expression equivalence via SymPy) and assumptions.

**Exit check:** accuracy on the gold set reaches the agreed bar (to be set, e.g. ≥ 90% of bounds exactly right and ≥ 95% of settings right), and every error type is understood.

## Phase 3: Graph and inference engine

- [x] **Canonical notation layer (D13)**, prerequisite for comparison (built before the v0.3 re-extraction; `pipeline/resolve.py` → `data/canonical/`):
  - `ontology/variables.yaml`: a symbol registry with precise definitions, aliases and conversion rules (e.g. ‖x‖² ≤ L ⇒ L_feat = √L; σ as std vs sub-Gaussian parameter). It generates the prompt's variable table; declared `symbols` are clustered into registry proposals.
  - `data/algorithms.yaml`: an algorithm registry (canonical id, aliases, introducing paper, techniques), resolved by name normalisation, then LLM adjudication, then human confirmation.
  - Citation resolution: `cited_key` → .bbl title → arXiv/DOI → manifest id. Unmatched cited papers become corpus candidates.
- [x] Inherited results (D1): `pipeline/order.py` (product order with reduction parameter maps) + `pipeline/infer.py` → `data/canonical/inferred.json` (upper bounds to special cases, lower bounds to generalisations, with derivation paths and caveats); shown on setting pages.
- [x] Build the setting poset (`pipeline/order.py`; covering edges in `data/canonical/poset.json`): per-dimension orders → product order, plus explicit cross-dimension reductions with parameter maps.
- [x] Inference: propagate upper bounds down and lower bounds up, translating through parameter maps and storing derivation paths separately from extracted results.
- [x] Bound comparison (D2) (`pipeline/compare.py`; see pipeline/README.md for the method): normalise to regime-specific forms (e.g. exponent vectors plus a polylog flag), compute dominance and the Pareto front, and assign a tightness status per setting and regime.
- [x] Reports: gaps, missing lower bounds, unstudied neighbours, redundant results, conflicts (D8) → `data/reports/` (`pipeline/report.py`).
- [x] Gap triage (`pipeline/triage.py` → `data/reports/triage.yaml`): one web-search call per candidate gap; verdicts closed / open_known / blank. **First run (17 candidate gaps, 54 searches):** 14 closed by papers outside the corpus (INF/Tsallis-INF, Li et al. 2019, newer corruption-robust bounds, …), 1 known open (stochastic linear on general compact sets: d√T log T vs d√T), 2 blank. Most apparent gaps are coverage holes. Feed the papers cited in `triage.yaml` into the next snowball round. Original item: run a targeted retrieval search for each candidate gap before labelling it open; mark it open vs blank; log negative searches.

**Exit check:** the acceptance tests from Phase 1 pass, i.e. known gaps and tight results are rediscovered from extracted data alone.

- Status (`pipeline/acceptance.py` → `data/acceptance-report.md`): **4 PASS** (F01 Θ(√KT) stochastic; F02 Lai–Robbins tight; F05 Θ(√KT) adversarial; F06 high-probability log gap), **2 PASS_STATUS** (F09 linear log gap via Dani et al.'s bounds; F13), **4 PARTIAL** (missing lower bounds in matching settings), **4 MANUAL** (algorithm-specific facts), **0 FAIL**.

## Phase 3b: Tools for the motivation (requested 2026-10-19)

Everything here builds on one piece of machinery: **D2 bound comparison**. Each bound is reduced to its asymptotic profile, i.e. exponents in (T, K, d, 1/Δ, …) plus a polylog flag, per quantity and regime. With that we can compute dominance, the best upper and best lower bound per setting and regime, and a tightness status.

### d) Plots of bounds (instead of only tables)
- [ ] **Rate plots per setting:** each bound (own and inherited, upper and lower) plotted against one variable (T by default, log-log), with sliders for the others (K, d, Δ, δ).
  - SymPy → JS at build time (`sympy.printing.jscode`), plotted client-side.
  - Instance-dependent sums use a uniform-gap instance: `sum_subopt(f(Delta_i))` → (K−1)·f(Δ).
  - O/Θ/Ω bounds have no constants, so plot their shape with constant 1 and style them differently from exact bounds.
  - Asymptotic (lim inf / lim sup) bounds are drawn as c·log T.
- [ ] **Rate-plane view:** each bound as a point (T-exponent, K- or d-exponent), with upper and lower bounds in different colours. Gaps are visible as the distance between the best upper and best lower point.
- [ ] **Consistency check for free:** an extracted upper bound below an extracted lower bound in the same setting and regime is an extraction error or a genuine conflict (D5). Flag it.

### e) Search and filtering for motivation 1–4
- [ ] **Faceted search** over settings (dimension facets) and results (quantity, regime, algorithm, technique family, paper, year, own/inherited, confidence), client-side from a JSON index. Saved queries such as "adversarial settings with no lower bound".
- [ ] **1. Gap finder:** a per-setting, per-regime tightness status (tight / log gap / poly gap / no lower bound / no upper bound). It feeds a "Gaps" page sorted by importance (number of papers, gap size), a graph colouring by status, and a filter on the settings index. Before a gap is called open it goes through gap triage (open vs blank).
- [ ] **2. Unstudied neighbours:** enumerate keys one order step away from well-studied settings (change one dimension to an adjacent value) that have no extracted results, ranked by how studied the source is. Skip combinations flagged ill-posed (e.g. an adversarial environment with a non-additive function class).
- [ ] **3. Technique transfer:** for a setting with a gap, list algorithm families (registry `family` / techniques) that achieve the best bound in neighbouring settings but don't appear here.
- [ ] **4. Redundancy:** an own result that is dominated by an inherited result from an *earlier* paper is "implied by prior work". List these with the derivation path.

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

## Known weak spots (TODO)

Found while building and reviewing the pilot (2026-10-19). Inference issues are flagged as caveats in `data/canonical/inferred.json` but not yet fixed.

### Inference validity (D1)
- [x] ~~Adversarial → stochastic transfers depend on the regret notion~~: resolved by argument and recorded as an order note (pseudo-regret ≤ expected regret vs the best action in hindsight; Yao's principle for lower bounds), restricted to comparator = best fixed action. Original concern: 375 upper-bound transfers (268 expected regret, 107 high-probability) rely on a single generic caveat. The high-probability ones are the shakiest: a bound against the best arm in hindsight is not directly a high-probability pseudo-regret bound. Fix with per-quantity validity rules on each order edge, part of the D2 work.
- [x] **Lower bounds proved only for a fixed parameter**: excluded from tightness status; on the site they get a 'pinned' badge and sit in a collapsed 'weak transfers' list. Original: (e.g. K = 2) reach general-K settings with a "holds for K = 2 only" caveat. That is valid but weak and easy to misread. Consider showing them separately or hiding them by default.
- [x] **Missing parameter maps:** generalised linear → linear (identity-link value maps `k_mu = c_mu = 1`); graph feedback → bandit (upward value maps: graph lower bounds instantiated at the bandit graph, α(G) = K, with a caveat). Original:
  - graph feedback → bandit: graph quantities such as `vartheta` and `V_pred` stay in bandit settings, where they should become K-armed values (independence number = K);
  - generalised linear → linear: link-function constants (`c_mu`, `k_mu`) should become 1.

  Both are currently caveated as "symbols defined only in the source setting".
- [x] **Instance-dependent lower bounds via reductions** are no longer transferred: per-arm bounds hold only on the embedded instances.
- [x] **Bayesian ↔ frequentist:** a Bayesian lower bound sent to a setting without a prior becomes a worst-case lower bound (sup ≥ average).

### Ontology and setting resolution
- [ ] **Fragmentation:** 175 extracted settings → 124 canonical ones, many with a single paper. Inheritance mitigates this. Revisit whether some key fields (e.g. `learner_knows: sigma`) are too fine-grained.
- [x] **Learner knowledge in lower-bound papers**: rule 17 applied in the schema-0.4 re-extraction (22 of 40 lower-bound settings now record knowledge). Lower bounds usually allow the learner to know everything, but extractions often leave `learner_knows` empty, which blocks valid transfers. Add a prompt rule, or default lower-bound settings to "knows all".
- [x] **Isolated settings: 36 → 15 of 141** after adding orders for `unspecified` values (oblivious ⊑ unspecified ⊑ adaptive; unspecified shape ⊑ arbitrary compact). The remaining 15 are genuinely different problems (expert advice, dueling, games). Original: 36 settings have no specialisation edge, mostly through deliberately unordered values (`unspecified` shapes, `adversarial_unspecified`, expert advice, dueling). Revisit once there are more papers.
- [x] `noise: not_applicable` on stochastic settings was a vocabulary gap (arbitrary model classes, e.g. Garivier et al. 2019): added `general_model_class` and normalised in `resolve.py`.
- [x] `bounded_01 ⊑ bounded_pm1` is exact ([0,1] ⊂ [−1,1]); `bounded_pm1 ⊑ subgaussian` (σ = 1) added.

### Extraction and data quality
- [x] **`extra_assumptions` split** into `conditions` and `tuning` (schema 0.4, re-extracted). Conditions travel with inferred bounds as caveats; transfers that violate a bound's own `regime` (e.g. needs C > R, target has C = 0) are dropped. Original: 71% of results have free-text extra assumptions, mostly tuning ("c = 3") or regime conditions, but some restrict the instance class (e.g. Hao et al.'s "optimal arms span R^d"). Transfers ignore them, which produced 2 of the conflicts. Schema change for the next extraction: split into `conditions` (restrict instances or the setting; must be mapped into the setting or flagged) and `tuning`.
- [x] **Conflict review queue**: 0 conflicts after re-extraction and the methodology fixes. Tsallis-INF r5 was a correct extraction that inference had misused (regime check added); Hao et al. now records its condition; the rest were profiler artefacts (late-crossover asymptotics, tuning parameters tied to Δ). Original: Tsallis-INF r5 (probably a dropped leading term) and Hao et al. r3 (a missing setting assumption).
- [x] **Validation:** 51 of 58 files clean after re-extraction (13 quotes below threshold, 1 expression issue). Original: 6 of 53 files have issues (`data/validation-report.md`), e.g. an `O(...)` inside an exact expression and 11 quotes below the match threshold.
- [x] **Unmapped review** → [`ontology/review-v0.3.md`](ontology/review-v0.3.md): 266 items in 24 themes. 113 items call for ontology changes (largest: scale normalisation of action/parameter norms, 45), 84 are already expressible (extractor guidance), 36 belong in result fields, 20 are out of scope. Next: apply v0.4 together with the next corpus expansion.
- [ ] **The algorithm registry** (`data/algorithms.yaml`, 132 entries) was seeded by an LLM and has not been reviewed.
- [ ] **The pilot facts** (`data/ground_truth/pilot-facts.yaml`) were written from memory and need checking.
- [x] **5 of the 6 non-arXiv classics** extracted from PDF; Lai & Robbins needs a manual PDF save (see Phase 1). Original: (Lai & Robbins, UCB1, EXP3, MOSS/INF, Dani et al., SupLinUCB) are not extracted. They hold the key lower bounds for acceptance facts F01 and F05.
- [ ] **Paper identity:** `alt_titles` is maintained by hand. 49 cited papers outside the corpus are listed in `data/canonical/candidates.yaml` for the next snowball round.

### Site
- [ ] GitHub Pages must be enabled (Settings → Pages → Source: GitHub Actions); a private repo needs a paid plan.
- [x] BCO ground-truth page: settings, results tables, transfer rules and open-problem cards.
- [x] Long bounds: clipped with a 'show full' toggle.

## Open decisions

1. The accuracy bar for Phase 2 to Phase 3.
2. Whether lemmas are extracted in v0 (proposal: no).
3. Representation of "T large enough" and hidden problem-dependent constants.
4. The human verification process: who verifies, and how much is verified before publishing.
5. Project name: "bandit-browser" fits the pilot; the general system may need a broader name later.
