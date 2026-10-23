# How accurate is the atlas?

Every result in the atlas was extracted from a paper by an LLM (Claude Opus) and almost none is human-verified.
This note collects three independent checks of how often the extractions are right, made without a domain expert
and repeatable with one command each. State on 2026-10-23: 558 papers extracted with ontology v0.5, 2,466 results.

| Check | What it compares | Result |
|---|---|---|
| [Second-model audit](#1-second-model-audit) | 200 random results against the paper text, graded by a different model | **5% major errors** (95% CI 2–9%); the bound itself: 0% (0–2%) |
| [Textbook gold set](#2-textbook-gold-set) | 71 theorems of Lattimore & Szepesvári, *Bandit Algorithms* | **0 contradictions**; 62% of checkable theorems recovered |
| [Citation cross-check](#3-citation-cross-check) | 565 bounds that later papers attribute to corpus papers | **67% agree** with our extraction of the cited paper |

None of these is human review. Together they say the bounds themselves are almost always transcribed correctly,
the settings they are attached to are often imprecise in minor ways, and the atlas is far from complete.

## 1. Second-model audit

`pipeline/audit.py` → [`data/reports/audit.md`](../data/reports/audit.md)

A random sample of 200 extracted results, stratified by side (upper/lower) and by batch (pilot/later), each
graded against the paper by a different model (Claude Fable) that did not do the extraction. The auditor sees the
paper text around the result's own source quote, the setting's definition, and the extracted record, and grades
seven fields as correct, minor error, major error, or cannot tell. 169 of the 200 could be graded; for 31 the
statement was not in the excerpt (the quote could not be located in the source).

| Field | Major-error rate (95% Wilson CI) | Minor errors |
|---|---|---|
| **overall** (any field) | 5% (2–9%) | 49% |
| bound (expression, rate, constants) | 0% (0–2%) | 1% |
| side (upper / lower) | 0% (0–2%) | 0% |
| quantity (regret notion) | 0% (0–2%) | 2% |
| dependence (worst case / instance) | 1% (0–3%) | 3% |
| setting (assumptions) | 3% (1–6%) | 35% |
| conditions | 1% (0–4%) | 15% |
| attribution (theorem number) | 0% (0–2%) | 1% |

- **Minor setting errors** are typical: a noise model recorded more generally than the paper states, a
  knowledge requirement (e.g. the learner must know λ₂) left out, a finite/infinite action-set mix-up. They
  matter for fine-grained transfers between settings, not for reading the bound.
- **Major errors** are mostly mis-scoped settings: a modified protocol (positive externalities, a reserve-price
  grid) recorded as the standard bandit problem, or a lower bound whose algorithm class (consistent *and*
  uniform-sampling strategies) is missing from its conditions. Two of the eight were already caught by the
  conflict check and fixed in [`data/corrections.yaml`](../data/corrections.yaml); the audit grades the raw
  extractions.
- Batch-1 lower bounds look weakest (10% major, 3–26%) and pilot results best (0% in 24), but the strata are
  small.

## 2. Textbook gold set

`pipeline/goldcheck.py` → [`data/reports/goldcheck.md`](../data/reports/goldcheck.md); data:
[`data/ground_truth/ls-book.yaml`](../data/ground_truth/ls-book.yaml)

71 regret and sample-complexity theorems of Lattimore & Szepesvári's *Bandit Algorithms* (chapters 6–37),
transcribed with verbatim quotes and mapped onto the ontology (LLM-assisted; quotes are exact substrings of the
authors' free PDF, so each entry can be checked). For each theorem at setting B, the atlas is searched for an
extracted bound that is valid at B through the specialisation order (an upper bound from B or a more general
setting, a lower bound from B or a special case):

- **recovered: 33 of 53 checkable (62%)**, the atlas has an equal or stronger bound valid at the book's
  setting;
- **contradicted: 0**, no rate-defining atlas bound is incompatible with the book (an upper bound below the
  book's lower bound or the reverse). Two apparent contradictions on the first run were artefacts of the check
  (a free parameter ε < Δ, and game-dependent constants in partial monitoring), now handled;
- not covered: 20 (e.g. the linear lower bounds of chapter 24, partial-monitoring rates), mostly because no
  corpus paper states the result in the book's setting; 18 have no comparable rate (paper-specific symbols).

The textbook is also the reference for the [pilot facts](pilot-facts.md) (each fact records `checked_against`).

## 3. Citation cross-check

`pipeline/crosscheck.py` → [`data/reports/crosscheck.md`](../data/reports/crosscheck.md)

Papers restate earlier results, usually in a comparison table, and the extractor records those as
`cited_results`. 715 cited bounds point at corpus papers; 565 have a comparable rate. Of these, **379 (67%)
agree** with our extraction of the cited paper (272 exactly, 107 up to log factors), 178 differ, and 8 cite a side
(upper/lower) we extracted nothing for.

A disagreement is a lead, not an error: citations paraphrase (UCB1 is cited as "O(√T)" by 12 papers although
the paper states the gap-dependent bound), specialise, or cite another theorem. The strongest leads are the 26
rates cited by two or more papers that our extraction lacks; several are genuine gaps in the extraction (e.g.
Flaxman et al.'s T^{3/4} for bandit convex optimisation, Zoghi et al.'s relative UCB).

## What this does and does not show

- The audit and the cross-check measure transcription: is what we stored what the paper says? Bounds are very
  reliable; settings are the weak point.
- The gold set measures coverage and consistency at the level of rates: the atlas never contradicts the
  textbook, and holds about 60% of its results in the right place.
- None of the three checks the *inference*: whether a bound inherited along the order is valid. That is what the
  conflict check is for (an upper bound below a lower bound in the same cell; 7 conflict cells remain, each
  explained in `plan.md`), and what expert review should target.

Reproduce: `uv run python pipeline/audit.py --n 200`, `pipeline/goldcheck.py`, `pipeline/crosscheck.py`.
