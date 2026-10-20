# Extraction quality tests: self-consistency and a verification pass

2026-10-19. Automatic proxies only: there is no human gold set yet (desiderata D6). Every LLM call used `claude-opus-5-5[1m]` through `claude -p` with tools disabled.

**Sample** (6 papers, 55k–200k chars of source, K-armed / linear / adversarial / lower-bound-heavy):
`garivier2011klucb`, `zimmert2021tsallisinf`, `abbasi2011oful`, `lattimore2017endofoptimism`, `li2019nearlyminimax`, `garivier2016etc`. Together they have 48 results in `data/extractions/` (v0).

**Spend**: 21 calls in total, about $11.5 equivalent.

| Calls | What | Cost (equivalent) |
|---|---|---|
| 12 | extractions (2 per paper) | $6.4 |
| 6 | verify, run on v0 | $3.8 |
| 3 | verify, run on copies with planted errors | $1.3 |

Raw outputs and scripts were kept out of the repo, in the session scratchpad (`…/scratchpad/exp/`: `runs/`, `verify/`, `inject/`, `scripts/compare.py`, `scripts/numcheck.py`). `data/extractions/` was not touched.

## TL;DR

1. **Bound transcription is stable and accurate. Everything around the bound is where errors live.**
   - Run to run, the side, notation, probability, horizon, comparator, quantity, and the algorithm registry ids agree 98–100%.
   - Expressions agree 84% symbolically, and **95% once declared symbols are allowed to be renamed** (`C_2eps` vs `C2_eps`).
   - The unstable fields are `learner_knows`, `instance_assumptions`, `source.number`, and how a theorem is split into results.
2. **The verifier is a good detector of transcription errors.** It caught **12/12 planted errors**, restored the exact original value for all 12, and raised no false alarms on those files.
3. **On the real v0 extractions it found no substantive bound errors.** It proposed 11 corrections. Judged against the LaTeX: 6 right, 2 debatable, 3 wrong. The 3 wrong ones were low-confidence and are rejected by `--apply` at the default `--min-confidence medium`. It **missed** the convention and interpretation errors that self-consistency surfaced: wrong theorem numbers, `quantity` chosen by the paper's name rather than its definition, gap knowledge missing from `learner_knows`, and the new rule 18.
4. **Theorem numbers are the single most error-prone field.** 8 of 30 labelled results have the wrong `source.number` in v0, and 4 more are wrong in the unlabelled zimmert corollaries. The cause: LaTeX shares counters across theorem/lemma/remark, sometimes inside a `.sty` the model never sees. This should be computed deterministically, not extracted.
5. **Recommendations:**
   - Run `verify.py` over the corpus *after* re-extracting with the current prompt (≈$0.55/paper, ≈$30 total). Treat it as a cheap auto-check (D5 `auto-checked`), not as review.
   - Do **not** adopt 2-of-3 voting.
   - Fix numbering in `preprocess.py`.
   - Make the prompt changes in §4.

## 1. Self-consistency

### Method

- `extract.extract_one` was run twice more per paper (r1, r2) with the *current* prompt (rules 17–18 included).
- r1 vs r2 measures pure sampling variance. Comparisons against v0 also include the prompt change.
- **Matching results.** Results are paired by (`source.label`, `side`) when both have a LaTeX label, else by (normalised `source.number`, `side`). Inside a group, a pair with an equivalent expression is preferred.
  - Matching by number alone fails: the same theorem was numbered 3, 4 and 7 in three runs.
- **Expressions.** Each is parsed with `resolve.parse`. Undefined functions (`sum_subopt`, `kl`) are replaced by fixed deterministic functions, and the two sides are compared numerically at 4 random positive points (rel. tol 1e-6). The second level also allows a bijective renaming of non-canonical (declared) symbols.
- **Settings.** Compared with `resolve.setting_key`: the referenced setting of each matched result, and the set of in-scope keys per paper.

### Numbers

| | r1 vs r2 | r1 vs v0 | r2 vs v0 |
|---|---|---|---|
| results | 48 vs 46 | 48 vs 48 | 46 vs 48 |
| same result count | 4/6 papers | 4/6 | 4/6 |
| matched results (of larger run) | 44 (92%) | 43 (90%) | 42 (88%) |
| expression identical string | 80% | 81% | 81% |
| expression numerically equivalent | 84% | 88% | 81% |
| … modulo renaming declared symbols | **95%** | 95% | 93% |
| notation / probability / horizon / comparator / algorithm_class | 100% | 100% | 100% |
| quantity | 100% | 88% | 88% |
| dependence | 98% | 100% | 100% |
| compute | 98% | 98% | 100% |
| algorithm registry_id (per result) | 98% | 100% | 98% |
| registry-id set Jaccard (per paper) | 18/18 | 18/18 | 18/18 |
| full setting key equal (per matched result) | **45%** | 30% | 36% |
| in-scope setting-key Jaccard (per paper) | 9/22 | 7/26 | 8/24 |

How often each setting dimension agrees, per matched result (r1 vs r2):

- 100%: objective, feedback, environment, action_space, function_class, domain, context, noise, extras.
- Lower: parameters 95%, action_set 93%, learner_knows 91%, **instance_assumptions 61%**.
- Against v0, learner_knows drops to 40%. That is expected, because rule 17 changed it.

Per paper (settings / results / cost):

| paper | v0 | r1 | r2 |
|---|---|---|---|
| garivier2011klucb | 3 / 6 / $0.56 | 2 / 5 / $0.49 | 2 / 5 / $0.49 |
| zimmert2021tsallisinf | 7 / 12 / $1.14 | 7 / 12 / $1.31 | 6 / 11 / $1.26 |
| abbasi2011oful | 3 / 4 / $0.42 | 2 / 4 / $0.41 | 2 / 4 / $0.14 |
| lattimore2017endofoptimism | 1 / 2 / $0.41 | 1 / 3 / $0.42 | 1 / 2 / $0.08 |
| li2019nearlyminimax | 2 / 5 / $0.71 | 2 / 5 / $0.70 | 2 / 5 / $0.16 |
| garivier2016etc | 3 / 19 / $0.66 | 3 / 19 / $0.66 | 3 / 19 / $0.31 |

The cheap second runs are prompt-cache hits: system prompt plus paper, within the cache TTL. A back-to-back repeat extraction costs 25–50% of the first.

### Kinds of disagreement (with examples)

1. **Declared-symbol naming** (accounts for 11 points of the expression gap; harmless).
   - Examples: `C_2eps` / `C2_eps` / `C_2`; `n_exp` / `n` / `n_explore`; `gamma_ll` / `g_pl`; `w_star_i` / `w_a`; `eps_alg` / `eps_c`.
   - Compare with alpha-renaming, or tighten the naming rule (§4.7).
2. **Theorem numbers.** Labels are stable, numbers are not.
   - `abbasi2011oful` `thm:UCBImp` is "Theorem 7" (v0), "Theorem 3" (r1) and "Theorem 4" (r2). LaTeX counter emulation gives Theorem 6, so all three are wrong.
   - `lattimore2017endofoptimism` `thm:upper` is 4 / 5 / 3; the correct number is 10.
   - `zimmert2021tsallisinf`: v0 has Corollaries 1, 2. r1 and r2 have 4, 5, which is correct: `jmlr2e.sty` shares the theorem counter with corollaries, and the `.sty` is not in the flattened source.
   - `li2019nearlyminimax`: all three runs agree on "Theorem 3 / Theorem 4 / Corollary", and all are wrong (10 / 21 / 23).
   - Against counter emulation (`scripts/numcheck.py`, by label), `source.number` is right for 22/30 (v0), 23/31 (r1) and 22/30 (r2).
3. **Granularity: which statements become results.**
   - `garivier2016etc` Theorem 1 has a small-T branch, `T*Delta/2 + Delta` when TΔ² ≤ 4√(2πe). v0 and r1 record it; r2 drops it and records Theorem 2's worst-case bound instead. That is why r2's count still comes out at 19.
   - `garivier2011klucb` Corollary 1 is a Bernoulli specialisation of Theorem 1. Only v0 records it.
   - `lattimore2017endofoptimism` Theorem 1 is a lower bound on confidence widths, not on regret. Only r1 records it.
   - `zimmert2021tsallisinf` has an asymptotic lower bound (Appendix A). r2 omits it.
4. **`instance_assumptions`** (61% agreement). `garivier2016etc` is two arms with gap Δ > 0, and r2 adds `unique_optimal_arm` to all three settings. That is implied by the setting, not stated as an assumption, so the node key changes for no reason.
5. **`learner_knows`.**
   - `zimmert2021tsallisinf` Theorem 3 (asymmetric α-Tsallis-INF): ξᵢ = Δᵢ^{1−2α} needs the gaps.
     - r1 puts `Delta, Delta_min` in `learner_knows`.
     - v0 and r2 put the gaps only in `algorithms[].requires_knowledge_of` and `extra_assumptions`.
     - So the node for that upper bound claims a gap-free learner. **r1 is right, and this is a real v0 error.**
   - `li2019nearlyminimax` adds `S` (‖θ‖ ≤ 1 normalisation) in r1 and r2 but not in v0.
   - `lattimore2017endofoptimism` adds `sigma` / `reward_family` (noise N(0,1)) in some runs.
6. **`quantity`.** For all 5 results, `li2019nearlyminimax` has `expected_regret` in v0 and `pseudo_regret` in r1 and r2. The paper calls it "expected regret", but defines E[Σ maxₓ xᵀθ − x_tᵀθ], which is pseudo-regret. **v0 is wrong.** It chose the label by the paper's name, and the ontology gives no definitions for `quantity` values.
7. **Rule 18 works.** `garivier2011klucb` Theorem 1 / 2 limsup results:
   - v0: `sum_subopt(Delta_i/kl_i)` with regime "normalised by log(n)";
   - r1 and r2: `sum_subopt(Delta_i/kl_i)*log(T)`.
   - This is the intended change, and r1/r2 agree on it.
8. **Rule 17 works but collides with shared settings.** r1 and r2 add T, K, `sigma`, `reward_family` to lower-bound settings. But in `li2019nearlyminimax` and `lattimore2017endofoptimism` the same setting is also used by an upper bound, so the extra knowledge is attached to the upper bound's node too (§4.4).

## 2. Verification pass (`pipeline/verify.py`)

### Design

- One `claude_cli.call_structured` call per paper, with tools disabled.
  - **System prompt:** referee instructions, followed by the full current extraction prompt as "what the extractor was told".
  - **User message:** the manifest metadata, the extraction JSON (without `_run`), then the paper source between untrusted-data markers.
- **Output schema** (pydantic → JSON Schema):
  - `checked[]`: one verdict per setting and per result: `ok | corrected | hallucinated | not_a_guarantee | unverifiable`.
  - `corrections[]`: `{target, old, new, reason, evidence, severity: critical|major|minor, confidence}`.
    - `target` is a dotted path such as `results.r3.bound.expression`. List items are addressed by `id`, or by index for `cited_results`.
    - `old` and `new` are JSON-encoded.
  - `missing_results[]` and `summary`.
- **`apply()`** writes a corrected copy with a `_verify` block: the applied and rejected corrections, flags, model, prompt hash and dates. The original `_run`, including `status`, is kept.
  - A correction is applied only if its `old` matches the stored value, its confidence is at least `--min-confidence` (default `medium`), and the record still passes the pydantic schema and the SymPy parse.
  - Flags (missing or hallucinated results) are recorded, never applied.
- **Never overwrites.** `--out` must differ from `--in`. The default `--out` is `data/extractions_verified/`.

```
uv run python pipeline/verify.py --only abbasi2011oful --out /tmp/x --apply
```

### 2a. Planted-error recall test

Twelve single-field errors were planted in copies of three v0 files (`scripts/inject.py`):

| paper | planted error | caught? | severity / confidence |
|---|---|---|---|
| klucb | Theorem 2 expr: `/kl_i` → `/(2*kl_i)` | yes, exact restore | critical / high |
| klucb | s1 noise `bounded_01` → `subgaussian` | yes | critical / high |
| klucb | Prop 1 probability → `high_probability` | yes | critical / high |
| klucb | Cor 1 setting `s2` → `s1` (Bernoulli → bounded) | yes | major / high |
| etc | worst-case `2.04*sqrt(T)` → `2.04*sqrt(T*log(T))` | yes | critical / high |
| etc | constant 334 → 34 | yes | critical / high |
| etc | horizon `known` → `anytime` | yes | major / high |
| etc | `log(T)/(2*Delta)` → `log(T)/Delta` | yes | critical / high |
| oful | leading constant 4 → 2 | yes | critical / high |
| oful | registry_id `oful` → `lin_ucb` | yes | major / high |
| oful | s2 `linear_infinite` → `linear_finite` | yes | major / medium |
| oful | Thm 14 notation `exact` → `O` | yes | major / high |

- **12/12 caught.** After `--apply`, all three files equal the originals byte for byte (apart from `_verify`).
- No other corrections were raised on these files. In particular, the 3 low-confidence numbering corrections it had proposed for `abbasi2011oful` on the first pass did not come back: the verifier is itself somewhat stochastic at low confidence.

### 2b. Verifier on the real v0 extractions

| paper | corrections | my judgement (read against `corpus/pre/*.tex`) |
|---|---|---|
| garivier2011klucb | 0 | — |
| garivier2016etc | 0 | — |
| abbasi2011oful | 3 × `source.number` (low confidence; rejected by `--apply`) | **wrong** ×3. It anchored on the extraction's own wrong "Theorem 7" and counted from there (→ 14, 15, 18). Counter emulation gives 13, 14, 17. |
| lattimore2017endofoptimism | `r2.source.number` 4 → 10 | **right.** Two of the four remarks sit inside `\iffalse`. The verifier handled that; my first counter script did not. |
| | `s1.learner_knows` + K, d, sigma, reward_family | **right** (rule 17; the upper-bound algorithm also takes 𝒜 and n, and the noise is N(0,1)) |
| li2019nearlyminimax | `r3/r4/r5.source.number` → Theorem 10, Theorem 21, Corollary 23 | **right** ×3 (confirmed by counter emulation) |
| | `s1`, `s2` `learner_knows` + d, S | **debatable** ×2. d is dropped from the key anyway. S is the ‖θ‖ ≤ 1 normalisation, a model constraint rather than knowledge. `s1` is shared with the upper bound r1. |
| zimmert2021tsallisinf | `s7.learner_knows` + T, K, reward_family | **right** (rule 17; only `reward_family` changes the key) |

- **Totals:** 11 corrections. 6 right, 2 debatable, 3 wrong.
- **At `--min-confidence medium`:** 8 applied (6 right, 2 debatable, 0 wrong).
- **Severity:** no critical, 5 major (all `learner_knows`), 6 minor (numbers).
- **Flags:** no hallucinated, missing or `not_a_guarantee` results anywhere.

**Real v0 errors it missed** (found through self-consistency and checked in the source):

- `zimmert2021tsallisinf` Corollaries are numbered 1, 2; they should be 4, 5. The counter is defined in `jmlr2e.sty`, which is not in the flattened source, so this is not detectable from the input.
- All 4 `abbasi2011oful` numbers are wrong (see above).
- `li2019nearlyminimax` `quantity: expected_regret` should be `pseudo_regret`, on 5 results.
- `zimmert2021tsallisinf` `s3.learner_knows` lacks `Delta` / `Delta_min`, although the extraction itself lists them in `a4.requires_knowledge_of`.
- `garivier2011klucb` r1, r3, r5, r6 limsup expressions break the new rule 18 (no `*log(T)`), even though rule 18 was in the instructions the verifier was given.

**Validation-report issues in the sample.** The only ones are `zimmert2021tsallisinf` r10 and r11, "quote not found". These are false alarms: the quote is faithful but drops the `\rev{...}` wrapper. The verifier correctly left them alone. `validate.norm` should strip `\rev{` and similar change-tracking macros.

**Reading.**

- The verifier reliably catches **transcription errors**: constants, terms, flipped qualifiers, wrong setting links, vocabulary misuse. It also catches clear rule violations it is pointed at (rule 17).
- It is weak on **convention errors**: which `quantity` matches a definition, knowledge implied by an algorithm's tuning, newly added rules, numbering.
- It tends to accept what the extractor did when the extractor wrote a plausible note.
- v0 seems to contain few transcription errors: zero found by the verifier, and expression disagreements across runs are all renamings. So most residual error mass is of the kind it misses.

**Cost.** $0.33–1.04 per paper (mean ≈ $0.57), ~25 s, ~2.5k output tokens. That is about 80% of one extraction call: input is the same paper plus the extraction, but output is much shorter.

## 3. Recommendations

**Run verify over the whole corpus? Yes, but after re-extraction, and as an auto-check, not as review.**

- About $30 for 53 papers, and it catches planted transcription errors at 100% with no false positives at ≥ medium confidence.
- It should run *after* the corpus is re-extracted with the current prompt (rules 17–18 change many records anyway).
- Use its output to set D5 `auto-checked` and to rank records for human review: `corrected` and `critical` first.
- Do not auto-apply into `data/extractions/`. Keep `data/extractions_verified/` as a derived layer, or apply only `critical` / `major` with high confidence after a spot check.
- Do not treat it as `human-verified`.
- Before the corpus run, extend its checklist (prompt in `verify.py`) with:
  - "check `quantity` against the paper's *definition*";
  - "every quantity in `algorithms[].requires_knowledge_of` used by an upper bound must be in that setting's `learner_knows`";
  - "check instructions 17 and 18 explicitly";
  - "do not recompute theorem numbers unless the number is printed or referenced in the text".

**Self-consistency / 2-of-3 voting in production? No.**

- The fields where voting could help are the ones where runs disagree: `learner_knows`, `instance_assumptions`, numbers, granularity. There, voting fixes some cases (zimmert corollary numbers, li `quantity`) and breaks others: the only run that got zimmert's gap knowledge right was the minority.
- Expressions and qualifiers are already ≥ 95–100% stable, so a 3× (≈ 1.6× with caching) cost buys little.
- Use a second run instead as a **disagreement detector when building the D6 gold set**. Disagreeing fields are where annotators should look first. Of the 6 v0 errors not caused by the prompt change, 5 showed up as run-to-run disagreements; the li2019 numbers were the exception, where all three runs were consistently wrong. Run the second extraction back-to-back so it hits the prompt cache.

**Deterministic fixes (pipeline, not prompt):**

1. **Theorem numbers** (the biggest single error source).
   - In `preprocess.py`, emulate LaTeX counters: `\newtheorem` from the source *and* from local `.sty`/`.cls` files, shared and `[section]` counters, `\appendix`, skipping `\iffalse…\fi` and starred environments.
   - Annotate each environment in the flattened source, e.g. `% [printed: Theorem 10]` immediately after `\begin{theorem}`, and tell the model to copy it (or overwrite `source.number` from `source.label` after extraction).
   - `scripts/numcheck.py` in the scratchpad is a 50-line prototype; it agrees with the verifier's correct cases.
2. **Upper-bound knowledge.** In `resolve.setting_key` (or a post-pass), union `algorithms[].requires_knowledge_of`, intersected with the `learner_knows` vocabulary, into the node key of each upper bound.
3. **Comparison tooling.** When diffing re-extractions or checking `cited_results`, compare expressions modulo renaming of declared symbols. `scripts/compare.py` has `numeq_renamed`.
4. **Quote matching.** Add change-tracking macros (`\rev`, `\new`, `\change`, `\add`) to `validate.LATEX_NOISE`.

## 4. Proposed prompt changes for schema.md (concrete wording)

Additions to the Rules list:

1. *(numbers)*
   > `source.number` is the number as printed. LaTeX computes it from counters that are often shared between theorems, lemmas, remarks and definitions, and are sometimes defined in a style file you cannot see. If a `% [printed: …]` annotation precedes the environment, copy it. Otherwise copy a number only if the text itself prints it (e.g. "Theorem 3 (Lai & Robbins)"); else write the environment name followed by the label, e.g. `"Theorem (thm:upper)"`, and never count environments yourself.
2. *(case splits)*
   > If a statement gives different bounds in different regimes (e.g. one expression when TΔ² ≥ c and another otherwise), record one result per case, each with its condition in `bound.regime`, including trivial branches such as `T*Delta`.
3. *(instance assumptions)*
   > Add a value to `instance_assumptions` only if the paper states it as an assumption of the result. Do not add consequences of the setting (two arms with Δ > 0 already have a unique optimal arm).
4. *(learner knowledge for upper bounds; amends rule 17)*
   > For a setting used by an upper bound, `learner_knows` must contain every input the algorithm needs from the vocabulary, as listed in its `requires_knowledge_of` (e.g. gaps used to tune a regulariser, the noise level, a norm bound S). If an upper bound and a lower bound of the paper need different `learner_knows`, create two settings (append " (lower bound)" to `name_in_paper`) rather than sharing one.
   - Longer term: move `learner_knows` from the setting to the result, because it is a property of the guarantee, not of the problem.
5. *(quantity)*
   > Choose `quantity` from the paper's definition, not its name. Regret defined through means (Σ μ* − μ_{A_t}, or ⟨θ, x* − x_t⟩, inside an expectation) is `pseudo_regret` even when the paper calls it "expected regret"; `expected_regret` is E[max_a Σ_t X_{a,t} − Σ_t X_{A_t,t}].
   - Also add one-line definitions to the `quantity` vocabulary in `ontology/bandits-0.3.yaml`, so they are rendered into the prompt the way dimension values are.
6. *(specialisations)*
   > Do not record a corollary that only restates an earlier result of the same paper for a special case that the ontology order already covers (e.g. Bernoulli rewards as a case of [0,1] rewards) unless it gives a different expression; mention it in the parent result's `notes`.
   - This is a policy choice. The alternative ("always record") is fine too, but the prompt should pick one, because runs currently disagree.
7. *(declared symbols)*
   > Name a declared symbol after the paper's own symbol, transliterated with underscores (C_2, not C2_eps; n_explore for the paper's exploration length n), and reuse canonical names such as `eps_alg` whenever the meaning matches.

## 5. Full-corpus run after adopting the recommendations (schema 0.4)

Re-extracted all 58 papers, about $38 equivalent. The new run used:
- printed theorem numbers (counter emulation in `preprocess.py`);
- prompt rules for case splits, corollary policy, upper- and lower-bound knowledge, instance assumptions, quantity by definition and symbol naming;
- `conditions` vs `tuning`.

| Metric | Before | After |
|---|---|---|
| Theorem numbers matching counter emulation | ~73% (sample) | **268/270** |
| Validation: clean files | 49/58 | **51/58** |
| `verify.py` corrections | 11 on 6 papers (v0.3 sample) | **4 on 58 papers** (1 major, 3 minor) |
| Flagged missing results | — | 7 |
| Conflicts in `data/reports/conflicts.md` | — | **0** |

The 6 papers with a major correction or a missing-result flag make the first human-review queue: auer2002exp3, baudry2023recipe, bubeck2013bounded, dann2023blackbox, gerchinovitz2016refined, qin2023klms. Verifier reports are in `data/extractions_verified/*.verify.json`. Corrections are never auto-applied to `data/extractions/`.

## 6. Ontology v0.4 extraction (59 papers, including Lai & Robbins)

- Unmapped items: 266 → 180.
- Validation: 49/59 clean. Quote misses are concentrated in the 6 PDF-converted papers; Lai & Robbins is an OCR'd 1985 scan.
- `verify.py`: **38 corrections** (1 critical, 12 major, 25 minor) and 7 missing-result flags.
  - Minor: 18 theorem-number nitpicks.
  - Major or critical, typical ones:
    - quantity by definition (Bubeck et al. 2012: pseudo- vs expected regret);
    - symbol collisions with canonical names (Abeille & Lazaric's γ_T, p);
    - worst-case vs instance-dependent for constructed lower bounds (Lykouris et al.);
    - EXP3 Thm 9.1's average regret. The verifier independently proposes the same ×T fix as `data/corrections.yaml`.
  - The richer v0.4 schema gives more fields to get wrong, hence more corrections than the v0.3-prompt run (4).
- **Human review queue** (major/critical corrections or missing results; 12 papers): abeille2017lints, auer2002exp3, baudry2023recipe, bubeck2012minimax, bubeck2012survey, gerchinovitz2016refined, gupta2019corruption, hamidi2020lints, ito2022variance, lykouris2018corruption, qin2023klms, wei2018moreadaptive.
