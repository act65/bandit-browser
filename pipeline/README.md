# Pipeline

```
corpus/manifest.yaml ──fetch.py──▶ corpus/src/<arxiv_id>/      (LaTeX source; gitignored)
                     ──preprocess.py──▶ corpus/pre/<arxiv_id>.tex  (flattened; gitignored)
                     ──extract.py──▶ data/extractions/<paper_id>.json
                     ──validate.py──▶ data/validation-report.md
                     ──resolve.py──▶ data/canonical/  (stable ids: settings S-<hash>, algorithms,
                                                        citations, normalised bounds; report.md)
                     ──infer.py──▶ data/canonical/inferred.json  (inherited bounds + derivations)
site/build.py ──▶ _site/   (static site; deployed by .github/workflows/pages.yml)
```

```bash
uv run python pipeline/fetch.py            # ~3 s per paper (arXiv rate limit)
uv run python pipeline/preprocess.py
CLAUDE_CLI_USAGE_LOG=data/extract.usage.jsonl \
  uv run python pipeline/extract.py --workers 3
uv run python pipeline/validate.py
uv run python pipeline/fetch_pdf.py         # non-arXiv papers: PDF -> text (manifest pdf_url)
uv run python pipeline/derive.py            # resolve -> infer -> compare -> report -> acceptance -> site_index
uv run python pipeline/verify.py            # second-reading verification -> data/extractions_verified/ (never edits extractions)
uv run python pipeline/triage.py            # web search per candidate gap -> data/reports/triage.yaml
uv run python pipeline/review_unmapped.py   # themes of unmapped setting features -> ontology/review-v<version>.md
uv run python pipeline/audit.py --n 200     # second-model audit of random results -> data/reports/audit.md
uv run python pipeline/goldcheck.py         # textbook gold set (ls-book.yaml) vs the atlas -> data/reports/goldcheck.md
uv run python pipeline/crosscheck.py        # our extractions vs how other papers cite them -> data/reports/crosscheck.md
uv run python pipeline/audit_inference.py   # second-model check of inherited bounds that set a verdict -> data/reports/audit-inference.md
uv run python pipeline/open_problems.py     # COLT open problems + web-searched status -> data/reports/open_problems.yaml
uv run python pipeline/link_open_problems.py # place them in the atlas, compare statuses -> data/reports/open_problems_links.yaml
uv run python pipeline/review_algorithms.py # registry vs extraction evidence -> data/reports/algorithm-registry-review.md
uv run python site/build.py && uv run python site/serve.py   # local preview (needs range requests)
uv run pytest tests -q                      # order / inference / comparison tests + checks on the committed data
```

Tests (`tests/`) build settings by hand on the real ontology, at fixtures where a known past bug changes
the answer; each of 16 injected bugs (reversed order rules, unmapped symbols, dropped rate exclusions, ...)
fails at least one test. CI (`.github/workflows/tests.yml`) runs them and re-runs `derive.py`, failing if the
committed derived data differs from what the code produces. Thresholds for the data checks (conflict and
tight cells, acceptance) are in `tests/baseline.yaml`; change them only on purpose.

All commands take `--only ID ...`. `extract.py` skips papers that already have an extraction unless you pass `--force`.

## Extractor backend

`claude_cli.py` calls `claude -p` with:
- `--system-prompt`: the PROMPT block of [schema.md](../schema.md), with the ontology rendered from `ontology/*.yaml`;
- `--json-schema`: generated from the same ontology by `schema.py`, so the model can only emit vocabulary values;
- all tools disabled, because paper text is untrusted.

This uses the Claude subscription rather than API credits. It is adapted from `act65/pol-score-cards`. The test run on OFUL used about 44k input and 6k output tokens, roughly $0.48 at API prices.

Every extraction records `_run` (models, prompt hash, ontology version, token usage). `status` starts as `extracted` and is raised to `human-verified` by review (desiderata D5).

## Canonical notation and ids (D13)

| Registry | File | Used by |
|---|---|---|
| Ontology (dimensions, node parameters, vocabularies) | `ontology/bandits-0.3.yaml` | prompt + JSON Schema enums |
| Variables (definitions, aliases, conversion rules) | `ontology/variables.yaml` | prompt variable table, validator, normaliser |
| Algorithms (ids, aliases, family, introducing paper) | `data/algorithms.yaml` | prompt; `registry_id` is constrained to these ids |
| Papers (ids, arXiv ids, `alt_titles`) | `corpus/manifest.yaml` | citation resolution |

- `seed_algorithms.py` seeded the algorithm registry by LLM clustering of the v0.2 algorithm mentions (148 mentions → 132 algorithms). It is a proposal to review by hand.
- `resolve.py` never edits extractions. It derives `data/canonical/` and a report: declared symbols recurring in 2+ papers are registry proposals; unregistered algorithms get provisional `new:<paper>:<name>` ids; unresolved citations become ranked corpus candidates (`candidates.yaml`), the input to the next snowball round.
- Setting ids hash the full canonical key (all dimensions, `action_set` minus `access`, `parameters`; `learner_knows` minus T, K, d), so they are stable across runs and re-extractions.

## Inference (D1)

`order.py` defines the specialisation order as a product order over the ontology: per-dimension orders, reductions with composed parameter maps, the subset rule for multi-valued dimensions, and fixed `parameters` as special cases. `infer.py` propagates every extracted result one hop over this (transitively closed) order:
- upper bounds go to special cases, with reduction maps and fixed parameters substituted;
- lower bounds go to generalisations, with reduction maps inverted.

Each record carries its derivation and caveats. Inferred results never feed further inference.

## Extraction quality (see data/extraction-tests.md)

- **Run-to-run agreement:**
  - bound expressions agree 95% (allowing renamed symbols);
  - notation, quantity and probability agree 98–100%;
  - full setting keys agree only 45%, driven by `instance_assumptions` and `learner_knows`.
- **Theorem numbers** were wrong 8 of 30 times. `preprocess.py` now replays LaTeX's theorem counters, including `.sty` definitions, shared counters, per-section numbering and `\appendix`, and annotates `% [printed: Theorem 3.2]`; the prompt says to copy it.
- **`verify.py`** caught 12/12 planted copying errors, but misses convention errors (quantity definitions, missing knowledge). Use it to rank records for human review, not as ground truth.
- **Repeat runs** are good disagreement detectors for building the gold set. 2-of-3 voting is not recommended.

## Corrections and condition classes

- `data/corrections.yaml`: manual corrections, applied by `resolve.py` on top of `data/extractions/`, each recording author, reason and review status.
- `data/condition-classes.yaml`: classes for the free-text result `conditions` (`classify_conditions.py`, cached). Upper bounds with an instance restriction (or proved only for small T / on a constructed class), lower bounds for restricted algorithms (memory, batches; consistency assumptions excepted), and results under a `model_change` (quantum oracles, starved feedback, …) stay out of tightness verdicts but remain visible. `--all` reclassifies every string (hand edits are then lost).

## Bound comparison (D2)

`compare.py` reduces every bound (extracted and inferred) to a profile, a growth rate v^a (log v)^b per variable:
- T is scanned alone. K, d, 1/Δ and 1/ε are scanned in the regime "T large" (along T = v⁴), and the bound's own T-profile is subtracted, so √(KT) has K-exponent ½.
- Profiles are fitted numerically: a high-precision, exact 3-point solve at v = 10^500…10^2000, so additive lower-order terms vanish.
- Instance-dependent bounds are evaluated on a uniform-gap instance, and KL-type divergences are taken as ~Δ².
- Data-dependent bounds (L*, Q_T, Λ_T) form their own regime, `data_dependent`.
- Bounds with paper-specific symbols are not profiled; about 64% of bounds are profiled.

Within a regime (quantity family × dependence):
- the best upper bounds form a Pareto front, and so do the best lower bounds;
- each variable gets a status: tight / log gap / poly gap / **conflict** (an upper bound below a lower bound, which usually means an extraction error).

Two transfer rules between quantity families:
- high-probability upper bounds count as expected-regret bounds with δ = 1/T;
- Bayesian lower bounds count as worst-case lower bounds (set in `infer.py`).

`report.py` writes `data/canonical/poset.json` (the covering edges, with justifications) and `data/reports/*.md`: gaps, missing lower bounds, conflicts, unstudied neighbours, already-known results. `acceptance.py` checks the pilot facts and writes `data/acceptance-report.md`.

## Corpus harvesting (Phase 4)

```bash
uv run python pipeline/harvest.py {arxiv,pmlr,neurips,bib,leads,topic,authors,openalex}   # -> corpus/harvest/*.jsonl
uv run python pipeline/dedupe.py      # -> corpus/pool.jsonl (with abstracts, gitignored) + corpus/pool.csv
uv run python pipeline/snowball.py    # citation snowball over the pool (OpenAlex)
```

- Harvesters use a project user-agent and no personal contact details.
- They pace themselves per host (arXiv every 3 s) and back off for minutes on 429s.
- The arXiv harvest resumes from cached pages.
- OpenAlex stages read `OPENALEX_API_KEY`.
- `dedupe.py` links records by arXiv id, DOI or normalised title.

## Site analysis index (Phase 3b)

`site_index.py` writes `data/canonical/site_index.json`, the data behind the site's analysis pages:
- every bound with its profile and a JavaScript plot function: the formula on the uniform-gap instance, with arguments T, K, d, Δ, δ, ε and other symbols at fixed base values (3,310 of 3,771 plottable);
- tightness cells with gap-triage verdicts;
- technique-transfer suggestions: algorithm families achieving a neighbour's best bound but absent here;
- unstudied neighbours, with ill-posed combinations removed;
- redundancy findings.

## Sources are not redistributed

The default arXiv licence does not permit redistribution, so `corpus/src` and `corpus/pre` are gitignored. Extractions keep only short verbatim quotes, as provenance.
