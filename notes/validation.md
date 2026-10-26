# How accurate is the atlas?

Every result in the atlas was extracted from a paper by an LLM (Claude Opus) and almost none is human-verified.
This note collects three independent checks of how often the extractions are right, made without a domain expert
and repeatable with one command each. State on 2026-10-23: 558 papers extracted with ontology v0.5, 2,466 results.

| Check | What it compares | Result |
|---|---|---|
| [Second-model audit](#1-second-model-audit) | 200 random results against the paper text, graded by a different model | **5% major errors** (95% CI 2–8%); the bound itself: 0% (0–2%) |
| [Are the claims in the papers?](#2-are-the-claims-in-the-papers) | every result whose quote is not verbatim (215) | **all 215 present** in their papers; 1 major error |
| [Textbook gold set](#3-textbook-gold-set) | 71 theorems of Lattimore & Szepesvári, *Bandit Algorithms* | **0 contradictions**; 62% of checkable theorems recovered |
| [Citation cross-check](#4-citation-cross-check) | 565 bounds that later papers attribute to corpus papers | **67% agree** with our extraction of the cited paper |

None of these is human review. Together they say the bounds themselves are almost always transcribed correctly,
the settings they are attached to are often imprecise in minor ways, and the atlas is far from complete.

## 1. Second-model audit

`pipeline/audit.py` → [`data/reports/audit.md`](../data/reports/audit.md)

A random sample of 200 extracted results, stratified by side (upper/lower) and by batch (pilot/later), each
graded against the paper by a different model (Claude Fable) that did not do the extraction. The auditor sees the
paper text around the result's own source quote, the setting's definition, and the extracted record, and grades
seven fields as correct, minor error, major error, or cannot tell. 197 of the 200 could be graded. The 3 it could
not grade are all in their papers: two theorems state their bound by reference to another theorem outside the
excerpt, and one is an example whose bound is in the paper's comparison table (checked by hand). A first run
reported 31 "cannot tell": the script had looked for the statement by the start of its quote, which fails for
quotes that begin with "…" or are abridged, and showed the auditor the wrong text. The locator now finds the
statement by its LaTeX label or printed theorem number first; the 31 were re-graded.

| Field | Major-error rate (95% Wilson CI) | Minor errors |
|---|---|---|
| **overall** (any field) | 5% (2–8%) | 48% |
| bound (expression, rate, constants) | 0% (0–2%) | 2% |
| side (upper / lower) | 0% (0–2%) | 0% |
| quantity (regret notion) | 0% (0–2%) | 2% |
| dependence (worst case / instance) | 0.5% (0–3%) | 4% |
| setting (assumptions) | 3% (1–6%) | 37% |
| conditions | 2% (1–4%) | 14% |
| attribution (theorem number) | 0% (0–2%) | 1% |

- **Minor setting errors** are typical: a noise model recorded more generally than the paper states, a
  knowledge requirement (e.g. the learner must know λ₂) left out, a finite/infinite action-set mix-up. They
  matter for fine-grained transfers between settings, not for reading the bound.
- **Major errors** are mostly mis-scoped settings: a modified protocol (positive externalities, a reserve-price
  grid) recorded as the standard bandit problem, or a lower bound whose algorithm class (consistent *and*
  uniform-sampling strategies) is missing from its conditions. Two of the nine were already caught by the
  conflict check and fixed in [`data/corrections.yaml`](../data/corrections.yaml); the audit grades the raw
  extractions.
- Batch-1 lower bounds look weakest (11% major of 35, 5–26%) and pilot results best (0% in 24), but the strata are
  small.

## 2. Are the claims in the papers?

`pipeline/audit.py --population quote_failed` → [`data/reports/audit-quotes.md`](../data/reports/audit-quotes.md)

Every extracted result carries a quote from the paper as evidence. `pipeline/validate.py` checks that the quote
occurs in the source (at least half of its 25-character windows; a quarter for PDF-converted sources): 2,751 of
2,977 quotes pass (92%). The other 8% are abridged (“Suppose … hold”), marked informal, or paraphrase displayed
maths in plain text, and that is exactly where a claim that is not in the paper would hide. So all 215 in-scope
results with such quotes were audited, and the auditor was asked whether the statement is in the paper at all;
whenever it could not find it near the theorem, it was given the whole paper.

- **all 215 statements are present in their papers** (187 found by LaTeX label, 4 by printed theorem number, 5 by a
  verbatim fragment of the quote, 19 only in the whole paper);
- 1 major error (a bound recorded as instance-dependent that is worst-case); the bound itself was wrong in none.

No fabricated result was found, in the random sample or in the population most at risk. The quotes themselves
should become verbatim (next extraction: retry when the validator rejects a quote), so that provenance can be
checked mechanically rather than by a second model.

## 3. Textbook gold set

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

## 4. Citation cross-check

`pipeline/crosscheck.py` → [`data/reports/crosscheck.md`](../data/reports/crosscheck.md)

Papers restate earlier results, usually in a comparison table, and the extractor records those as
`cited_results`. 715 cited bounds point at corpus papers; 565 have a comparable rate. Of these, **379 (67%)
agree** with our extraction of the cited paper (272 exactly, 107 up to log factors), 178 differ, and 8 cite a side
(upper/lower) we extracted nothing for.

A disagreement is a lead, not an error: citations paraphrase (UCB1 is cited as "O(√T)" by 12 papers although
the paper states the gap-dependent bound), specialise, or cite another theorem. The strongest leads are the 26
rates cited by two or more papers that our extraction lacks; several are genuine gaps in the extraction (e.g.
Flaxman et al.'s T^{3/4} for bandit convex optimisation, Zoghi et al.'s relative UCB).

## 5. Inference audit (are inherited bounds valid?)

`pipeline/audit_inference.py` → [`data/reports/audit-inference.md`](../data/reports/audit-inference.md)

200 random inherited bounds that set a verdict (on the best-upper or best-lower front of a tight / gap / conflict
cell), each judged by a second model from the source theorem, both settings and the derivation.

- **Round 1 (2026-10-26): 18% invalid** (13–24%; [round-1 report](../data/reports/audit-inference-round1.md)). Causes,
  all fixed: K-armed embedded into unit-ball / ellipsoid / permutahedron linear settings (an order rule let
  `not_applicable` defer); `top ⊑ unspecified` in node fields; adversarial bounds sent to uncorrupted-reference
  corruption settings; d = K applied to contextual K-armed settings; switching-comparator results pooled with
  static regret; lower bounds in K sent to settings without K; an ETC-only lower bound (correction).
- The same work found an older bug: equal-rate bounds removed each other from the front, leaving 49 cells with no
  best upper bound (tight cells 66 → 77 after the fix).
- **Round 2 (fresh sample, after the fixes): 4% invalid** (2–7%). 4 of the 7 dispute static regret in switching
  settings (valid as stated: Θ(√KT) against the best fixed arm), 2 had an unstated parameter structure read as
  compatible with sparse (fixed since: the K-armed embedding implies dense parameters in a box, and an unstated
  structure in a linear or kernel setting means dense), 1 is a range-adaptivity lower bound (open lead). 33 more are valid but need a
  caveat the derivation does not record (mostly: the lower-bound instances must lie in the target class).

## What this does and does not show

- The audit and the cross-check measure transcription: is what we stored what the paper says? Bounds are very
  reliable; settings are the weak point.
- The gold set measures coverage and consistency at the level of rates: the atlas never contradicts the
  textbook, and holds about 60% of its results in the right place.
- Section 5 checks the *inference*; before it, none did: whether a bound inherited along the order is valid. That is what the
  conflict check is for (an upper bound below a lower bound in the same cell; 7 conflict cells remain, each
  explained in `plan.md`), and what expert review should target.

Reproduce: `uv run python pipeline/audit.py --n 200`, `pipeline/goldcheck.py`, `pipeline/crosscheck.py`.
