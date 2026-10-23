# Pilot facts: acceptance tests for K-armed and linear bandits

This note describes the 14 known facts in [`data/ground_truth/pilot-facts.yaml`](../data/ground_truth/pilot-facts.yaml), how [`pipeline/acceptance.py`](../pipeline/acceptance.py) checks them against the derived data, and where each one stood in the latest run ([`data/acceptance-report.md`](../data/acceptance-report.md)).

> **Not yet verified.** The facts were written from domain knowledge and the corpus manifest's `why` notes. They have **not** been checked line by line against the papers, and the `user_verified` field is empty for every fact. Facts marked `confidence: medium` in particular need their exact form and regime checked. A PASS below means the pipeline agrees with the fact as written, not that the fact is correct.

## 1. What the facts are for

The atlas extracts bounds from papers with an LLM, places them on settings defined by an ontology, propagates them along the specialisation order, and computes a tightness status per setting and regime. Each step can go wrong silently. The pilot facts are **acceptance tests** for the whole chain: statements about the K-armed and linear slice that any competent bandit theorist would give, and that the graph should rediscover from extracted data alone.

They cover three kinds of claim:

- **tightness status** of a setting in a regime (for example, worst-case regret of stochastic K-armed bandits is $\Theta(\sqrt{KT})$);
- **historical gap closures** (for example, MOSS removing the $\sqrt{\log T}$ factor of UCB1), recorded in a `history` field;
- **structural traps** the engine must handle, recorded in a `tests` field: lower bounds for one algorithm class must not propagate as minimax lower bounds; one algorithm can hold results in two settings (best of both worlds); learner knowledge changes the rate.

The plan (Phase 1) calls for these facts; Phase 3's exit check is that they pass.

### Vocabulary

Each fact has a setting (an assumption vector over the ontology), a regime string, an expected **status**, optional upper and lower bounds with papers, and a confidence.

| Status | Meaning |
|---|---|
| `tight_constants` | upper and lower bounds match up to constant factors |
| `tight_logs` | they match up to logarithmic factors |
| `log_gap` | the best known bounds differ by logarithmic factors |
| `poly_gap` | they differ by a polynomial factor |
| `algorithm_specific` | the lower bound holds for one algorithm class only |
| `impossibility` | an impossibility result (no fact uses this yet) |

| Confidence | Meaning |
|---|---|
| high | textbook fact (Lattimore & Szepesvári 2020) |
| medium | believed correct; exact form or regime to be checked against the paper |

Paper ids refer to [`corpus/manifest.yaml`](../corpus/manifest.yaml).

The YAML defines five base settings by YAML anchors: stochastic K-armed (`stoch_k`, subgaussian noise), adversarial K-armed (`adv_k`, oblivious), stochastic linear with an infinite action set (`stoch_lin_inf`), stochastic linear with finitely many actions (`stoch_lin_fin`), and adversarial linear with finitely many actions (`adv_lin_fin`). All use cumulative regret, bandit feedback and no context. F08 and F14 modify `stoch_k`; F07 refers to two settings at once.

## 2. How a fact is checked

`pipeline/acceptance.py` reads the facts, the canonical settings (`data/canonical/settings.json`) and the comparison table (`data/canonical/comparison.json`, produced by `pipeline/compare.py`). For each fact it does the following.

1. **Decide whether the fact is machine-checkable.** A fact is marked **MANUAL** if its setting is not a single assumption vector (F07), if its status is not one of `tight_constants`, `tight_logs`, `log_gap`, `poly_gap` (F04, F11), or if it carries `check: manual` (F03).
2. **Find matching settings.** A canonical setting matches if it agrees with the fact on five dimensions: objective, feedback, environment, action space and context. Noise is ignored, because papers state different reward models for the same problem. If the fact lists `learner_knows` or `instance_assumptions`, the canonical setting must include them (it may include more).
3. **Pick the regime cell.** The regime string selects a cell of the comparison table. "high probability" selects the high-probability regret family, otherwise expected regret; "instance" or "asymptotic" selects instance-dependent bounds, otherwise worst case.
4. **Choose the best matching cell.** Among matching settings that have bounds in that cell, it takes the one with the best status (tight, then log gap, poly gap, no lower, no upper, conflict), breaking ties by the number of bounds.
5. **Compare.** The cell's status is compared with the expected status. Expected `tight_constants` accepts only `tight`; `tight_logs` and `log_gap` both accept `tight` or `log_gap`; `poly_gap` accepts `poly_gap`. The fact's own bounds, if given in a parseable form, are reduced to growth exponents with `compare.py` and compared, variable by variable, with the cell's best upper and lower rates.

### Rates

`compare.py` reduces every bound to a **profile**: for each variable $v$, the growth $v^a (\log v)^b$, written `a·log^b` (so `0.5·log^1` is $\sqrt v \log v$). $T$ is scanned alone. $K$, $d$, $1/\Delta$ and $1/\varepsilon$ are scanned in the regime "$T$ large", along the path $T = v^4$, with the bound's own $T$-growth subtracted. Instance-dependent bounds are evaluated on an instance with equal gaps. Constants are ignored, so "tight" means tight up to constant factors in the scanned variables.

One consequence shows up in the report: the per-variable status is computed on the raw path exponents, which include the $T$-growth along the path, while the printed rates have it subtracted. So a log gap in $T$ can make the $d$ column read "up 1 / low 1 (log_gap)" (F09).

### Verdicts

| Verdict | Meaning |
|---|---|
| PASS | status accepted and every rate the fact gives agrees |
| PASS_STATUS | status accepted, but the best rates found differ from the fact's (often a weaker upper bound or a different lower bound) |
| PARTIAL | some evidence, but not enough: typically an upper bound and no lower bound (`no_lower`) |
| FAIL | the data contradict the fact: a conflict, or a status *better* than the fact allows |
| MISSING | no matching setting has bounds in the regime |
| MANUAL | not machine-checkable yet |

### Limits of the check

- **Optimistic selection.** The check takes the best of all matching settings. With 100 matching settings (F01), one well-populated node is enough to pass, even if other nodes for the same problem show gaps or conflicts.
- **Superset matching.** A setting with extra learner knowledge or instance assumptions still matches. F02 and F08 pass on nodes where the learner "knows C".
- **Rates only for parseable bounds.** Bounds given in prose (`claim:`) or with variables that are not canonical (such as $N$ in F13 or $C$ in F08) are not compared. Only the status is.
- **Constants are not checked.** `tight_constants` for F02 means the exact Lai–Robbins constant; the check only confirms tightness up to constant factors.
- **`tight_logs` and `log_gap` are not distinguished.** Both accept the same statuses.

## 3. The facts

$R_T$ denotes cumulative regret over $T$ rounds; $\Delta_i$ is the gap of arm $i$; $\mathrm{KL}_i$ is the divergence between arm $i$'s reward distribution and the optimal mean (in the Lai–Robbins sense). Paper ids in the upper column support the upper bound; those in the lower column support the lower bound.

| Id | Setting and regime | Statement | Expected | Upper papers | Lower papers | Conf. |
|---|---|---|---|---|---|---|
| F01 | stochastic K-armed; worst case, pseudo-regret, known $T$ | Minimax regret is $\Theta(\sqrt{KT})$. UCB1's $O(\sqrt{KT\log T})$ was improved by MOSS; the lower bound uses Bernoulli arms, so it applies to the stochastic case | `tight_constants` | audibert2009moss | auer2002exp3 | high |
| F02 | stochastic K-armed; asymptotic, instance-dependent, consistent policies | $\lim_{T\to\infty} \mathbb E[R_T]/\log T = \sum_{i:\Delta_i>0} \Delta_i/\mathrm{KL}_i$ (Lai–Robbins); matched by KL-UCB and Thompson sampling. Exact optimality depends on the reward family | `tight_constants` | cappe2013klucb, kaufmann2012thompson, agrawal2013further | lai1985asymptotically | high |
| F03 | stochastic K-armed; simultaneously worst-case and asymptotically optimal | Some algorithms achieve $O(\sqrt{KT})$ and the Lai–Robbins constant at once. Tests multi-regime results attached to one algorithm | `tight_constants` (manual) | menard2017klucbpp, garivier2018klucbswitch, jin2021mots, jin2022exptsfamily | — | medium |
| F04 | stochastic K-armed; asymptotic, explore-then-commit class | ETC-type strategies lose a factor 2 asymptotically (Gaussian, two arms); Double ETC is asymptotically optimal. A class-restricted lower bound must not propagate as a minimax lower bound | `algorithm_specific` | jin2020detc | garivier2016etc | medium |
| F05 | adversarial K-armed; worst case, pseudo-regret | Minimax regret is $\Theta(\sqrt{KT})$. EXP3's $O(\sqrt{KT\log K})$ was improved by INF; Tsallis-INF is the modern FTRL form | `tight_constants` | audibert2009moss, zimmert2021tsallisinf | auer2002exp3 | high |
| F06 | adversarial K-armed; high probability | $R_T = O\big(\sqrt{KT\log(K/\delta)}\big)$ with probability $1-\delta$. No lower bound given; the note asks what Gerchinovitz & Lattimore 2016 rule out | `tight_logs` | neu2015explore | — (related: gerchinovitz2016refined) | medium |
| F07 | stochastic and adversarial K-armed (one algorithm); best of both worlds | Tsallis-INF gets $O(\sqrt{KT})$ adversarially and $O\big(\sum_{i:\Delta_i>0} \log T/\Delta_i\big)$ stochastically. Earlier SAO and SAPO were suboptimal; Jin et al. 2023 removed the unique-optimal-arm assumption | `tight_constants` | zimmert2021tsallisinf (related: bubeck2012bobw, auer2016nearly, jin2023improved) | — | high |
| F08 | stochastic K-armed with corruption budget $C$; instance-dependent | $\tilde O\big(KC + \sum_{i:\Delta_i>0} \log T/\Delta_i\big)$; an additive $\Omega(C)$-type dependence is necessary. Exact log factors and lower-bound form to check | `log_gap` | gupta2019corruption | lykouris2018corruption, gupta2019corruption | medium |
| F09 | stochastic linear, infinite action set; worst case | $O(d\sqrt T\log T)$ (OFUL) vs $\Omega(d\sqrt T)$. Li, Wang & Zhou 2019 narrowed this for some action sets; the action-set geometry matters for the lower bound | `log_gap` | dani2008stochastic, abbasi2011oful | dani2008stochastic, rusmevichientong2010linear | medium |
| F10 | stochastic linear, $K$ actions; worst case | $\tilde O\big(\sqrt{dT\log K}\big)$ vs $\Omega(\sqrt{dT})$. SupLinUCB is for the contextual version, so the setting mapping needs checking. With $d = K$ the bound is dominated by F01 | `log_gap` | chu2011suplinucb | chu2011suplinucb | medium |
| F11 | stochastic linear, infinite action set; linear Thompson sampling (frequentist) | LinTS has $\tilde O(d^{3/2}\sqrt T)$ regret, and the extra $\sqrt d$ is necessary without posterior inflation. A poly gap in $d$ that is not a gap of the setting | `algorithm_specific` | agrawal2013lints, abeille2017lints | hamidi2020lints | medium |
| F12 | stochastic linear, finite actions; asymptotic, instance-dependent | A Graves–Lai-type lower bound holds; optimism and Thompson sampling are not asymptotically optimal; matched by dedicated algorithms. Asymptotic optimality of UCB does not transfer through K-armed → linear | `tight_constants` | combes2017ossb, hao2020adaptive, kirschner2021ids, tirinzoni2020primaldual | lattimore2017endofoptimism | high |
| F13 | adversarial linear, $N$ actions; worst case | $O\big(\sqrt{dT\log N}\big)$ (Exp2) vs $\Omega(d\sqrt T)$; they match when $\log N \sim d$ (e.g. the hypercube). Exp2 is not efficient; Hazan & Karnin 2016 give an efficient $\tilde O(d\sqrt T)$ | `tight_logs` | bubeck2012minimax (related: hazan2016volumetric) | dani2008stochastic, shamir2015complexity | medium |
| F14 | stochastic K-armed, learner knows $\mu^\star$; known optimal mean and gap lower bound | Regret is bounded, independent of $T$. Learner knowledge must be part of the setting comparison | `tight_constants` | bubeck2013bounded | — | medium |

## 4. Status at ontology v0.5 (2026-10-22)

The latest report gives **6 PASS, 2 PASS_STATUS, 2 PARTIAL, 4 MANUAL**, and no FAIL or MISSING. "Matching settings" counts canonical settings that agree with the fact on the five matched dimensions and have bounds in the fact's regime cell.

| Id | Verdict | What matched or what is missing |
|---|---|---|
| F01 | PASS | Best of 100 matching settings (stochastic K-armed, rewards in $[0,1]$) is tight with $\sqrt{KT}$ on both sides, as expected. |
| F02 | PASS | Best of 96 is tight: upper and lower both $K\,\Delta^{-1}\log T$ on the equal-gap instance. The chosen node also has the learner knowing $C$, and constants are not compared, so the Lai–Robbins constant itself is not checked. |
| F03 | MANUAL | Marked `check: manual`: "simultaneously optimal" is a property of one algorithm across two regimes. |
| F04 | MANUAL | `algorithm_specific` is not machine-checkable yet. |
| F05 | PASS | Best of 11 (adversarial oblivious K-armed) is tight with $\sqrt{KT}$ on both sides. |
| F06 | PASS | Best of 8 has a log gap: upper $\sqrt{KT \log K}$, lower $\sqrt{KT}$. The fact gives no lower bound, so only the upper rate is compared, and it agrees. |
| F07 | MANUAL | The setting is two settings at once (a string, not an assumption vector). |
| F08 | PASS | Best of 9 (corrupted stochastic, learner knows $C$) is *tight* in $\Delta$, $K$ and $T$; tight is accepted for an expected `log_gap`. $C$ is not a scanned variable, so the corruption term is not checked. |
| F09 | PASS_STATUS | Best of 37 has a log gap, as expected, but the best upper bound found is $d\sqrt T\log^{1.5}T$ rather than the fact's $d\sqrt T\log T$. The OFUL rate is not the best upper bound on the matched node. |
| F10 | PASS | Best of 23 has a log gap in $K$: upper $\sqrt{dT\log K}$, lower $\sqrt{dT}$, matching the fact. |
| F11 | MANUAL | `algorithm_specific` is not machine-checkable yet. |
| F12 | PARTIAL | Only 1 matching setting, and it has no lower bound (`no_lower`); the asymptotic lower bound of Lattimore & Szepesvári 2017 is not on a matching node. |
| F13 | PASS_STATUS | Best of 2 has a log gap in $K$ (upper $\sqrt{dT\log K}$, lower $\sqrt{dT}$). The fact's lower bound $d\sqrt T$ is not found on the matched node, and its upper bound is not compared because $N$ is not a canonical variable. |
| F14 | PARTIAL | Best of 8 (learner knows $\Delta$ lower bound, $\mu^\star$, $\sigma$) has an upper bound but no lower bound (`no_lower`). |

**What would move the counts.** The two PARTIAL facts need lower bounds on the matching nodes: the asymptotic linear lower bound for F12 and a lower bound for the known-$\mu^\star$ setting for F14. The two PASS_STATUS facts need the best rates in the data to change: the OFUL bound becoming the best upper bound for F09, and the $\Omega(d\sqrt T)$ lower bound reaching the finite-action adversarial linear node for F13. The four MANUAL facts need new kinds of check: algorithm-class lower bounds (F04, F11), several regimes for one algorithm (F03) and results shared between two settings (F07).
