# Ground truth: Lattimore's *Bandit Convex Optimisation*

This note describes the hand-built reference dataset [`data/ground_truth/bco.yaml`](../data/ground_truth/bco.yaml) and the ontology lessons recorded in [`data/ground_truth/bco-ontology-notes.md`](../data/ground_truth/bco-ontology-notes.md). It summarises the settings, bounds, transfer rules and open problems that the YAML records. Where the YAML is terse, this note says so rather than filling the gap from memory.

## 1. The source and why it is ground truth

**Source.** Tor Lattimore, *Bandit Convex Optimisation*, arXiv:2402.06535, version 5 (12 November 2025). The transcription was made from the arXiv LaTeX source (`cvx.tex`, `all.bib`) and cross-checked against `pdftotext` output of the v5 PDF. Quotes in the YAML are verbatim LaTeX unless marked `pdf_text`. All table, theorem and section numbers below are those of v5.

**Status.** The YAML was produced by an LLM sub-agent on 2026-10-19. Its status is `extracted` with `human_verified: false`. It is therefore *ground truth by construction of the source*, not by independent checking: the book is curated by one expert, but the transcription has not been read line by line by a person.

**Why this book.** Three properties make it a good reference for the atlas:

1. **It already is a table of bounds.** Table 2.1 lists lower bounds and Table 2.2 lists upper bounds, each with a function class, a constraint set or compute cost, and a citation. This is the same shape as the atlas's per-setting bound tables, so the pipeline's output can be compared with it row by row.
2. **It states transfer rules explicitly.** §2.4 explains which lower bounds carry over to which settings and why (improper is easier than constrained, stochastic is easier than adversarial, linear losses are smooth, and so on). These are the edges of the specialisation order, written by the author.
3. **It lists open problems.** Chapter 14 ("Outlook") and several exercises and notes say what is open. A correct graph should show a gap wherever the book says a problem is open, and no gap where the book says a bound is tight.

**Role in the plan.** K-armed and linear bandits remain the primary pilot. Bandit convex optimisation (BCO) is the planned second slice (Phase 4). There the BCO tables test generalisation: can the pipeline reproduce a published table of bounds in a family of settings it was not tuned on?

### Conventions

- **Order.** As in [`schema.md`](../schema.md), $a \sqsubseteq b$ means "$a$ is a special case of $b$" (equivalently, $a$ is easier). Upper bounds flow from $b$ to $a$; lower bounds flow from $a$ to $b$.
- **Horizon.** The book writes $n$ for the number of rounds; this is the atlas's canonical $T$. This note keeps $n$ to match the book.
- **Diameter.** The book writes $D = \mathrm{diam}(K)$. The YAML renames it `D_K`, because canonical `D` means delay.
- **Other symbols.** $d$ is the dimension of $K$; $\alpha$ and $\beta$ are the strong-convexity and smoothness parameters (known constants); $\vartheta$ is the self-concordance parameter of a barrier on $K$; $\varepsilon$ is target accuracy and $\delta$ failure probability.
- **Regret.** The book's regret is $\mathrm{Reg}_n = \sup_{x \in K} \sum_{t=1}^n \big(f_t(X_t) - f_t(x)\big)$, with the supremum inside any expectation. It is not pseudo-regret. Table 2.2 does not say whether a bound holds in expectation or with high probability, so the YAML records such rows with quantity `regret` and leaves the probability unset unless the linked theorem says. Lower bounds are recorded as expected regret (the usual minimax reading; the table does not print this).
- **Simple regret and sample complexity.** In the stochastic setting the learner outputs a final point $\hat X$; simple regret is $f(\hat X) - \inf_{x\in K} f(x)$. Sample complexity is the number of rounds needed until simple regret is at most $\varepsilon$ with high probability.

### Function classes

Definition 1.1 defines properties of a convex function $f$ on $K$. A class is written $\mathcal F_P$ for a set of properties $P$; adding properties gives a smaller class.

| Property | Meaning |
|---|---|
| b (bounded) | $f(x) \in [0,1]$ for all $x \in K$ |
| l (Lipschitz) | $f(x) - f(y) \le \lVert x - y \rVert$ on $K$ |
| sm (smooth) | $f(x) - \tfrac{\beta}{2}\lVert x\rVert^2$ is concave on $K$ |
| sc (strongly convex) | $f(x) - \tfrac{\alpha}{2}\lVert x\rVert^2$ is convex on $K$ |
| lin (linear) | $f(x) = x^\top b + c$ |
| quad (quadratic) | $f(x) = x^\top A x + x^\top b + c$ |

Superscripts on a class mark the setting: $(s)$ for stochastic and $(i)$ for improper. **The two tables use them differently.** In Table 2.1 (lower bounds), $(s)$ means "the bound already holds in the easier stochastic setting" and $(i)$ means "already holds in the easier improper setting", so the bound transfers to harder settings. In Table 2.2 (upper bounds), $(s)$ means "the work covers only the stochastic setting" and $(i)$ means "the algorithm queries outside $K$". A missing $(s)$ in Table 2.2 means adversarial; a missing $(i)$ means constrained. Neither default is written in the book. The ontology notes flag this as a good probe for the gold set, since an extractor is likely to conflate the two meanings.

### Environments and domains

- **Stochastic**: $f_t = f$ for all $t$, observed with conditionally subgaussian noise (Assumption 1.4). The noise is a martingale difference that may depend on the history and the current action; it is not i.i.d.
- **Adversarial**: $f_1, \dots, f_n$ chosen by an adversary. The book allows noise even here, and its tables do not say whether the adversary is oblivious. Many cited adversarial results are noise-free.
- **Constrained**: play in the convex body $K$ (Assumption 1.2: convex, compact, non-empty interior) and compare with the best point of $K$.
- **Improper** (Note 1.iii): query anywhere in $\mathbb R^d$, compare with the best point of $K$. Boundedness and Lipschitzness hold only on $K$; smoothness and strong convexity hold everywhere.
- **Unconstrained** (Note 1.ii): $K = \mathbb R^d$, which is outside Assumption 1.2.

## 2. Settings

The YAML has 19 settings. All use one-point bandit feedback. Each has an assumption vector over function class, environment, domain, dimension and noise, plus a mapping to ontology v0.1 and a list of what v0.1 could not express. They group naturally by function class.

| Group | YAML id | Book notation | Environment | Domain | Extra | Results in YAML |
|---|---|---|---|---|---|---|
| Bounded | `S_b_adv` | $\mathcal F_{b}$ | adversarial | constrained | | U2, U3, U13, U14, U16, U18, U26, X1 |
| | `S_b_sto` | $\mathcal F^{(s)}_{b}$ | stochastic | constrained | | U22, U24, U25, U27, U28, U29, X4 |
| | `S_b_adv_d1` | $\mathcal F_{b,d=1}$ | adversarial | constrained | $d = 1$ | U12, U15 |
| | `S_convex_sto` | $\mathcal F^{(s)}$ | stochastic | constrained | low confidence | U11 |
| Lipschitz | `S_bl_adv` | $\mathcal F_{b,l}$ | adversarial | constrained | | U1 |
| | `S_bl_sto` | $\mathcal F^{(s)}_{b,l}$ | stochastic | constrained | | U9 |
| | `S_l_sto_improper` | $\mathcal F^{(s,i)}_{l}$ | stochastic | improper | | U23 |
| | `S_l_sto_d1` | $\mathcal F^{(s)}_{l,d=1}$ | stochastic | constrained | $d = 1$ | U8 |
| Smooth / strongly convex | `S_bsm_adv` | $\mathcal F_{b,sm}$ | adversarial | constrained | $\beta$ | U6 |
| | `S_bsmsc_adv` | $\mathcal F_{b,sm,sc}$ | adversarial | constrained | $\alpha, \beta$ | U10, U19, U20 |
| | `S_bsmsc_adv_improper` | $\mathcal F^{(i)}_{b,sm,sc}$ | adversarial | improper | $\alpha, \beta$ | U4, U5 |
| | `S_blscsm_sto_improper` | $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | stochastic | improper | $\alpha, \beta$ | L2, L4, L5, L6 |
| | `S_lsmsc_sto_improper` | $\mathcal F^{(s,i)}_{l,sm,sc}$ | stochastic | improper | $\alpha, \beta$ | U17 |
| | `S_smsc_sto_unconstrained` | $\mathcal F_{sm,sc}$, $K = \mathbb R^d$ | stochastic | unconstrained | not in tables | X3 |
| Linear / quadratic | `S_blin_adv` | $\mathcal F_{b,lin}$ | adversarial | constrained | | U7 |
| | `S_blin_sto` | $\mathcal F^{(s)}_{b,lin}$ | stochastic | constrained | | L1, X2 |
| | `S_bquad_adv` | $\mathcal F_{b,quad}$ | adversarial | constrained | | U21 |
| | `S_blquadscsm_sto` | $\mathcal F^{(s)}_{b,l,quad,sc,sm}$ | stochastic | constrained | $\alpha, \beta$ | L3 |
| | `S_quadsmsc_sto_improper` | $\mathcal F^{(s,i)}_{quad,sm,sc}$ | stochastic | improper (also unconstrained) | not in tables | X5 |

Notes on individual settings, as recorded in the YAML:

- `S_blin_adv` and `S_blin_sto` set `smooth` and `quadratic` to true because linearity implies them ($\beta = 0$, $A = 0$). They are not separate assumptions. `S_blin_adv` is the BCO name for the classical adversarial linear bandit on a convex body.
- `S_bquad_adv` sets `smooth` true for the same reason ($\beta = 2\lVert A\rVert$), but $\beta$ does not appear in its bound.
- `S_convex_sto` exists only for the BLN15 row of Table 2.2, whose class is printed $\mathcal F^{(s)}$ without b. Note 2.v describes the same result as being for $\mathcal F_b$. The YAML treats the class as a possible typo for $\mathcal F^{(s)}_b$ and records a conflict.
- `S_smsc_sto_unconstrained` (Note 2.v) and `S_quadsmsc_sto_improper` (§2.4, bullet 6) do not appear in the tables; they come from the text.

**What v0.1 could not say.** In ontology v0.1, all but two of these 19 settings collapse to one tuple (`action_space: convex`), up to environment and noise; the two exceptions differ only in objective. The 29 upper bounds of Table 2.2 would land on two nodes and could not be compared. The ontology notes propose the missing dimensions: a multi-select `function_class` with implications (lin ⇒ quad, lin ⇒ sm with $\beta = 0$, quad ⇒ sm), a `domain` dimension (improper ⊑ constrained, improper ⊑ unconstrained), a node parameter for the constraint set (shape, position, representation), extra noise values, $d = 1$ as a node parameter, two-point feedback, sample-complexity objectives, and result-level fields such as `compute` and `non_constructive`. `function_class` and `domain` were adopted from ontology v0.2 onwards, and v0.5 has an explicit equivalence between `action_space: linear_infinite` and `convex_body` with `function_class: {bounded, linear}`.

## 3. Results

The YAML has 40 results: 6 lower bounds from Table 2.1 (L1–L6), 29 upper bounds from Table 2.2 (U1–U29) and 5 results from the text (X1–X5). Each has a bound with its notation ($O$, $\tilde O$, $\Omega$), a quantity, a dependence (all are worst case), the original citation, the book theorem where the table hyperlinks one, a compute cost, extra assumptions and a confidence. Below, "Table 2.2 r7" means row 7 of Table 2.2.

The tables quote the bounds as the book's tables print them. Lower-order terms and constants that the linked theorem contains are mentioned only when the YAML records them.

### 3.1 Lower bounds

| Id | Setting | Bound | Source | Regime | Conf. |
|---|---|---|---|---|---|
| L1 | $\mathcal F^{(s)}_{b,lin}$ | $\Omega(d\sqrt n)$ | Dani, Hayes & Kakade 2008; Table 2.1(a) r1 | $K = \prod_{k=1}^{d/2} \mathbb S^1$ ($d/2$ unit circles, $d$ even). Not convex; footnote 1 says the bound transfers to $\mathrm{conv}(K)$ for linear losses | high |
| L2 | $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | $\Omega(d\sqrt n)$ | Shamir 2013; Table 2.1(a) r2 | $\alpha = 1/2$, $\beta = 7/2$, $K = B_1$ | high |
| L3 | $\mathcal F^{(s)}_{b,l,quad,sc,sm}$ | $\Omega(d\sqrt n)$ | Shamir 2013; Table 2.1(a) r3 | $\alpha = \beta = 1$, $K = B_1$, constrained | high |
| L4 | $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | $\Omega\big(d\sqrt n / \max(1,\alpha)\big)$ | Akhavan, Chzhen, Pontil & Tsybakov 2024; Table 2.1(a) r4 | $\beta = O(\alpha)$, $K = B_1$ | high |
| L5 | $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | simple regret $\Omega(d/\sqrt n)$ | Shamir 2013; Table 2.1(b) r1 | $\alpha = 1/2$, $\beta = 7/2$, $K = B_1$ | high |
| L6 | $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | simple regret $\Omega\big(d / (\max(1,\alpha)\sqrt n)\big)$ | Akhavan et al. 2024; Table 2.1(b) r2 | $\beta = O(\alpha)$, $K = B_1$ | high |
| X1 | $\mathcal F_{b}$ | $\Omega(d\sqrt n)$ | §2.4, first paragraph | derived from L1 by class inclusion and stochastic ⊑ adversarial; the book states it directly | high |
| X2 | $\mathcal F^{(s)}_{b,lin}$ | simple regret $\Omega(d/\sqrt n)$ | §2.4, bullet 5 (technique of Lattimore & Szepesvári 2020) | $K = [-1,1]^d$; informal claim, no written proof | medium |

All lower bounds are minimax over all algorithms and are proved for specific bodies ($B_1$, a product of circles, the cube). A lower bound on a specific $K$ is a lower bound for the family "all convex bodies", not for every $K$. The quantity (expected regret) is inferred, not printed.

X1 is useful as an inference test: the book states the propagated result explicitly, so the engine should derive exactly this from L1.

### 3.2 Upper bounds: bounded losses, $\mathcal F_b$

| Id | Setting | Bound | Source | Regime / extra assumptions | Compute | Conf. |
|---|---|---|---|---|---|---|
| U2 | $\mathcal F_b$ | $O(d\, n^{5/6})$ | Flaxman, Kalai & McMahan 2005; Table 2.2 r2 | $K$ in isotropic position | $O(d)$, projection | high |
| U3 | $\mathcal F_b$ | $\tilde O(d^{1/2}\vartheta^{1/4} n^{3/4})$ | this book, Thm 6.13; r3 | no noise | $O(d^2)$ | high |
| U13 | $\mathcal F_b$ | $\tilde O(2^{d^4}\sqrt n)$ | Hazan & Li 2016; r13 | | $O(\log(n)^{\mathrm{poly}(d)})$ | high |
| U14 | $\mathcal F_b$ | $\tilde O(d^{10.5}\sqrt n)$ | Bubeck, Lee & Eldan 2017 (key BEL16); r14 | | $\mathrm{poly}(d,n)$ | high |
| U16 | $\mathcal F_b$ | $\tilde O(d^{18}\sqrt n)$ | cited as BEL18; r16 | non-constructive | $\infty$ | low |
| U18 | $\mathcal F_b$ | $\tilde O(d^{2.5}\sqrt n)$ | Lattimore 2020; r18; same bound as Thm 8.21 | non-constructive (Bayesian minimax duality) | $\infty$ | high |
| U26 | $\mathcal F_b$ | $\tilde O(d^{2.5}\sqrt n)$ | Fokkema, van der Hoeven, Lattimore & Mayo 2024; r26; Thm 11.8 | high probability; $B_1 \subset K \subset B_{2d}$ via isotropic positioning | $\mathrm{poly}(d,n)$ | medium |
| U12 | $\mathcal F_{b,d=1}$ | $\tilde O(\sqrt n)$ | Bubeck, Dekel, Koren & Peres 2015; r12 | $d = 1$; non-constructive | $\infty$ | high |
| U15 | $\mathcal F_{b,d=1}$ | $\tilde O(\sqrt n)$ | Bubeck, Lee & Eldan 2017; r15; Thm 8.4 | $d = 1$; no noise | $O(\sqrt n)$ | high |
| U22 | $\mathcal F^{(s)}_b$ | $\tilde O(d^{4.5}\sqrt n)$ | Lattimore & György 2021; r22 | | $O(d^2)$, ellipsoid | high |
| U24 | $\mathcal F^{(s)}_b$ | $\tilde O(d^{1.5}\sqrt n)$ | Fokkema et al. 2024; r24; Thm 10.8 | high probability; $K/d$ in Löwner position (or $K$ symmetric and in John position, or with isotropic polar) | $O(d^2)$ + Löwner positioning | high |
| U25 | $\mathcal F^{(s)}_b$ | $\tilde O(d^{2}\sqrt n)$ | Fokkema et al. 2024; r25; Thm 10.8 | high probability; $K$ in isotropic position | $O(d^2)$ + isotropic positioning | high |
| U27 | $\mathcal F^{(s)}_b$ | sample complexity $\tilde O(d^4/\varepsilon^2)$ | Carpentier 2025; r27; Thm 9.21 | expected number of queries; correct w.p. $\ge 1-\delta$ | $O(d^2)$, centre of gravity | high |
| U28 | $\mathcal F^{(s)}_b$ | sample complexity $\tilde O(d^5/\varepsilon^2)$ | this book, §9.7 (sketch only) | | $O(d^2)$, ellipsoid | medium |
| U29 | $\mathcal F^{(s)}_b$ | sample complexity $\tilde O(d^4/\varepsilon^2)$ | this book, Thm 9.25; r29 | | $O(d^2)$, inscribed ellipsoid | high |
| X4 | $\mathcal F^{(s)}_b$ (assumed) | sample complexity $O(d^{14}/\varepsilon^2)$ | Liang, Narayanan & Rakhlin 2014; Note 2.v | class not stated; assumed from context | | low |
| U11 | $\mathcal F^{(s)}$ (see §2) | sample complexity $\tilde O(d^{7.5}/\varepsilon^2)$ | Belloni, Liang, Narayanan & Rakhlin 2015; r11 | class conflict with Note 2.v | $O(1)$ | low |

The compute column matters for this group. The best bound for adversarial $\mathcal F_b$ was non-constructive ($d^{2.5}$, U18) until U26 matched it in polynomial time; before that the best polynomial-time bound was $d^{10.5}$ (U14). In the stochastic case, $d^{1.5}$ (U24) needs Löwner positioning, which is not known to be computable in polynomial time for general $K$ (Exercise 10.17), and $d^2$ (U25) needs isotropic positioning. The ontology notes argue that "best bound" and "best polynomial-time bound" must be different regimes, which is why the `compute` field exists.

### 3.3 Upper bounds: Lipschitz losses

| Id | Setting | Bound | Source | Regime / extra assumptions | Compute | Conf. |
|---|---|---|---|---|---|---|
| U1 | $\mathcal F_{b,l}$ | $O(d^{1/2} D^{1/2} n^{3/4})$ | Flaxman et al. 2005; r1; Thm 5.6 | $B_1 \subset K$; no noise | $O(d)$, projection | high |
| U9 | $\mathcal F^{(s)}_{b,l}$ | $\tilde O(d^{16}\sqrt n)$ | Agarwal, Foster, Hsu, Kakade & Rakhlin 2013; r9 | | $O(1)$, ellipsoid | high |
| U23 | $\mathcal F^{(s,i)}_{l}$ | $\tilde O(d^{1.5}\sqrt n)$ | Lattimore & György 2023; r23 | $K = B_1$ (stated in §2.2, not in the table) | $O(d^2)$ | high |
| U8 | $\mathcal F^{(s)}_{l,d=1}$ | $\tilde O(\sqrt n)$ | Agarwal et al. 2013; r8; Thm 4.6 (bisection) | $d = 1$; high probability; loss not assumed bounded | $O(1)$ | high |

### 3.4 Upper bounds: smooth and strongly convex losses

| Id | Setting | Bound | Source | Regime / extra assumptions | Compute | Conf. |
|---|---|---|---|---|---|---|
| U6 | $\mathcal F_{b,sm}$ | $\tilde O\big((\vartheta\beta)^{1/3}(Ddn)^{2/3}\big)$ | Saha & Tewari 2011; r6; Thm 6.14 | no noise; the theorem has an extra $3d\sqrt{\vartheta n \log n}$ term | $O(d^2)$ | high |
| U10 | $\mathcal F_{b,sm,sc}$ | $\tilde O\big(d\sqrt{(\vartheta + \beta/\alpha)\,n}\big)$ | Hazan & Levy 2014; r10; Thm 6.16 | no noise; misplaced parenthesis in the book's LaTeX | $O(d^2)$ | high |
| U19 | $\mathcal F_{b,sm,sc}$ | $\tilde O\big(d\sqrt{\beta n/\alpha}\big)$ | Ito 2020; r19 | minimiser "deep inside" $K$ (not quantified) | $\mathrm{poly}(d)$ | high |
| U20 | $\mathcal F_{b,sm,sc}$ | $\tilde O\big(d^{1.5}\sqrt{\beta n/\alpha}\big)$ | Ito 2020; r20 | | $\mathrm{poly}(d)$ | high |
| U4 | $\mathcal F^{(i)}_{b,sm,sc}$ | $\tilde O\big(d\sqrt{\beta n/\alpha}\big)$ | Agarwal, Dekel & Xiao 2010; r4 | erratum: proof only sketched, minor issues (corrected by U5) | $O(d)$ | high |
| U5 | $\mathcal F^{(i)}_{b,sm,sc}$ | $O\big(d\sqrt{\beta n/\alpha}\big)$ | this book, Thm 5.8; r5 | no noise; $0 < \alpha \le \beta$; $f_t \in [0,1]$ on $K + B_r$; lower-order term omitted | $O(d)$ | high |
| U17 | $\mathcal F^{(s,i)}_{l,sm,sc}$ | $O\big(d\sqrt{\beta n/\alpha}\big)$ | Akhavan, Pontil & Tsybakov 2020; r17 | | $O(d)$ | high |
| X3 | $\mathcal F_{sm,sc}$, $K = \mathbb R^d$ | sample complexity $O(d^3/\varepsilon^2)$ | Jamieson, Nowak & Recht 2012; Note 2.v | polynomial dependence on $\alpha, \beta$ hidden | | medium |

### 3.5 Upper bounds: linear and quadratic losses

| Id | Setting | Bound | Source | Regime / extra assumptions | Compute | Conf. |
|---|---|---|---|---|---|---|
| U7 | $\mathcal F_{b,lin}$ | $\tilde O(d\sqrt n)$ | Bubeck, Cesa-Bianchi & Kakade 2012; r7; Thm 7.17 | no noise; exponential weights on a cover | $O(\exp(d))$ | high |
| U21 | $\mathcal F_{b,quad}$ | $\tilde O(d^{16}\sqrt n)$ | Suggala, Ravikumar & Netrapalli 2021; r21 | | $\mathrm{poly}(d)$ | high |
| X5 | $\mathcal F^{(s,i)}_{quad,sm,sc}$ | simple regret $O(d^2/n)$ | §2.4, bullet 6 (no attribution in that sentence) | improper or unconstrained; $\alpha, \beta = \Theta(1)$; book does not say whether b or l is assumed | | medium |

### 3.6 Status per setting

The table below gives, for cumulative regret, the best upper and lower bound available for each setting once the transfer rules of §4 are applied, and the resulting gap in $d$ and $n$ (treating $\alpha$, $\beta$, $\vartheta$ and $D$ as constants). The **Basis** column says where the status comes from:

- **book**: the book states the status (§2.4, Chapter 14, or a result's own note);
- **derived**: this note derived it from the YAML's results and transfer rules; the book does not state it. These rows are what the inference engine should reproduce, and they need checking.

| Setting | Best upper | Best lower | Gap | Basis |
|---|---|---|---|---|
| $\mathcal F_b$ | $\tilde O(d^{2.5}\sqrt n)$ (U18 non-constructive; U26 polynomial time) | $\Omega(d\sqrt n)$ (X1) | $d^{1.5}$ | book (§2.4, Outlook 14.i) |
| $\mathcal F^{(s)}_b$ | $\tilde O(d^{1.5}\sqrt n)$ (U24, Löwner position) | $\Omega(d\sqrt n)$ (L1 by class inclusion) | $d^{0.5}$ | book (Outlook 14.i) |
| $\mathcal F_{b,d=1}$ | $O(\sqrt n \log n)$ (U15; tables print $\tilde O(\sqrt n)$) | $\Omega(\sqrt n)$ (source not cited) | log factor | book (Outlook 14.xii) |
| $\mathcal F_{b,lin}$ | $\tilde O(d\sqrt n)$ (U7, exponential compute) | $\Omega(d\sqrt n)$ (L1, stochastic ⊑ adversarial) | logs | book (§2.4) |
| $\mathcal F^{(s)}_{b,lin}$ | $\tilde O(d\sqrt n)$ (U7, adversarial ⊒ stochastic) | $\Omega(d\sqrt n)$ (L1) | logs | book (§2.4) |
| $\mathcal F^{(s)}_{b,l,quad,sc,sm}$ | $\tilde O\big(d\sqrt{(\vartheta+\beta/\alpha)n}\big)$ (U10 by inclusion) | $\Omega(d\sqrt n)$ (L3) | "nearly" matched | book (§2.4, bullet 6) |
| $\mathcal F^{(s,i)}_{quad,sm,sc}$ | $\Theta(d\sqrt n)$ per the book, citing Akhavan et al. 2020 | see caveat below | tight per book | book (§2.4, bullet 6) |
| $\mathcal F_{b,l}$ | $\tilde O(d^{2.5}\sqrt n)$ (from $\mathcal F_b$); U1 alone gives $n^{3/4}$ | $\Omega(d\sqrt n)$ (L2: improper ⊑ constrained, stochastic ⊑ adversarial, class inclusion) | $d^{1.5}$ | derived |
| $\mathcal F^{(s)}_{b,l}$ | $\tilde O(d^{1.5}\sqrt n)$ (U24 by inclusion, under its positioning assumption); U9 alone gives $d^{16}$ | $\Omega(d\sqrt n)$ (L2, improper ⊑ constrained) | $d^{0.5}$ | derived |
| $\mathcal F^{(s,i)}_{l}$ | $\tilde O(d^{1.5}\sqrt n)$ (U23, $K = B_1$) | $\Omega(d\sqrt n)$ (L2 by class inclusion) | $d^{0.5}$ | derived |
| $\mathcal F^{(s)}_{l,d=1}$ | $\tilde O(\sqrt n)$ (U8) | none recorded | no lower bound | derived |
| $\mathcal F_{b,sm}$ | $\tilde O(d^{2.5}\sqrt n)$ (from $\mathcal F_b$); U6 alone gives $n^{2/3}$ | $\Omega(d\sqrt n)$ (linear ⊑ smooth, Note 6.vi) | $d^{1.5}$ | derived (the lower bound is stated in Note 6.vi) |
| $\mathcal F_{b,sm,sc}$ | $\tilde O\big(d\sqrt{(\vartheta+\beta/\alpha)n}\big)$ (U10) | $\Omega(d\sqrt n)$ (L2, three transfers) | logs and the $\vartheta$ factor | derived |
| $\mathcal F^{(i)}_{b,sm,sc}$ | $O\big(d\sqrt{\beta n/\alpha}\big)$ (U5) | $\Omega(d\sqrt n)$ (L2, stochastic ⊑ adversarial) | none at fixed $\alpha, \beta$ | derived |
| $\mathcal F^{(s,i)}_{b,l,sc,sm}$ | $O\big(d\sqrt{\beta n/\alpha}\big)$ (U17 by inclusion; U5) | $\Omega(d\sqrt n)$ (L2, L4) | none at fixed $\alpha, \beta$ | derived |
| $\mathcal F^{(s,i)}_{l,sm,sc}$ | $O\big(d\sqrt{\beta n/\alpha}\big)$ (U17) | $\Omega(d\sqrt n)$ (L2 by class inclusion) | none at fixed $\alpha, \beta$ | derived |
| $\mathcal F_{b,quad}$ | $\tilde O(d^{2}\sqrt n)$ (U7 via quadratic-as-linear, $d \mapsto d_2$; statistical only); $\tilde O(d^{2.5}\sqrt n)$ from $\mathcal F_b$; U21 $d^{16}$ in polynomial time | $\Omega(d\sqrt n)$ (L1, linear ⊑ quadratic) | $d$ | derived |

Two further observations:

- **Simple regret, improper smooth and strongly convex.** On $\mathcal F^{(s,i)}_{b,l,sc,sm}$ the cumulative upper bound $O(d\sqrt{\beta n/\alpha})$, divided by $n$ (cumulative-to-simple rule), gives simple regret $O(d/\sqrt n)$ at fixed $\alpha,\beta$. This matches L5. Derived, not stated.
- **Sample complexity, stochastic $\mathcal F_b$.** The best table entries are $\tilde O(d^4/\varepsilon^2)$ (U27, U29). The YAML's own example for the rule "high-probability regret to sample complexity" converts U24 into $\tilde O(d^3/\varepsilon^2)$, which is better in $d$. If both are taken at face value, propagation improves on the table (at the cost of Löwner positioning). No sample-complexity lower bound for $\mathcal F^{(s)}_b$ is recorded.

**Caveat on the quadratic improper row.** The book says the $\Omega(d\sqrt n)$ lower bound for quadratic, smooth, strongly convex losses is matched in the unconstrained and improper settings. The only recorded quadratic lower bound, L3, is for the *constrained* setting, and lower bounds transfer from improper to constrained, not the other way. So the recorded results do not support the "tight" claim for the improper quadratic node. Either the Shamir 2013 bound also holds in the improper setting (Table 2.1 does not mark it with $(i)$), or the claim rests on something not in the YAML.

## 4. Transfer rules

The YAML has 19 transfer rules. Each has a kind, the dimension values it connects, which side (upper or lower) transfers in which direction, a parameter map where needed, a validity scope, and a quote from the book.

| Id | Kind | From → to | Transfers | Book reference | Conf. |
|---|---|---|---|---|---|
| `TR_improper_constrained` | easier–harder | improper → constrained | lower forward, upper back | §2.4 bullet 1; Note 1.iii | high |
| `TR_improper_unconstrained` | easier–harder | improper → unconstrained | lower forward, upper back | §2.4 bullet 1; Note 1.iii | high |
| `TR_sto_adv` | inclusion | stochastic → adversarial | lower forward, upper back | §2.4 bullet 4; §1.3 | high |
| `TR_class_inclusion` | inclusion | $\mathcal F_P \to \mathcal F_Q$, $Q \subseteq P$ | lower forward, upper back | §1.3; §2.4 | high |
| `TR_linear_in_smooth` | inclusion | $\mathcal F_{b,lin} \to \mathcal F_{b,sm}$ ($\beta = 0$) | lower | Note 6.vi | high |
| `TR_two_point_feedback` | easier–harder | two-point → one-point feedback | lower forward, upper back | Note 1.vi | medium |
| `TR_simple_to_cumulative` | metric transfer | cumulative ↔ simple regret (stochastic) | upper: divide by $n$; lower: multiply by $n$ | §1.3 eq. (1.4); §2.4 bullet 2 | high |
| `TR_hp_regret_to_sample_complexity` | metric transfer | high-probability regret → sample complexity | upper | Fact 1.6 | high |
| `TR_expected_regret_to_sample_complexity` | metric transfer | expected regret → sample complexity | upper, extra $\log(1/\delta)$ | Prop. 1.7 | high |
| `TR_bayes_adversarial_minimax` | metric transfer | minimax Bayesian ↔ minimax adversarial regret | both (equality) | Thm 8.17 | high |
| `TR_info_ratio_to_exp_by_opt` | metric transfer | information ratio $\Psi^\star$ → exploration-by-optimisation $\Lambda^\star$ | upper ($\Lambda^\star \le 14\Psi^\star$) | Thm 8.22 | medium |
| `TR_gaussian_to_bounded_noise` | log-factor transfer | Gaussian → bounded noise | lower, up to logs | §2.4 bullet 3 (Shamir 2015) | high |
| `TR_gaussian_to_noisefree_adv` | log-factor transfer | stochastic Gaussian → noise-free adversarial, bounded | lower, up to logs | §2.4 bullet 4 (Shamir 2015) | high |
| `TR_nonconvex_hull` | reduction | linear on non-convex $K$ → linear on $\mathrm{conv}(K)$ | lower | Table 2.1 footnote 1 (Shamir 2015) | high |
| `TR_quadratic_as_linear` | reduction | $\mathcal F_{b,quad}$ in dimension $d$ → $\mathcal F_{b,lin}$ in dimension $d_2$ | upper, statistical only | §7.6 | high |
| `TR_submodular_to_bco` | cross-problem reduction | BCO on $[0,1]^d$ → bandit submodular minimisation | upper, additive $\sqrt{2n\log(1/\delta)}$ | §13.2, Prop. 13.9 | high |
| `TR_scaling_invariance` | reduction | $K \to \gamma K$ | both | §3.3, Prop. 3.8 | medium |
| `TR_bounded_to_lipschitz_interior` | reduction | $\mathcal F_b$ on $K$ → Lipschitz on $(1-\varepsilon)K$ | upper, additive $\varepsilon n$ | Cor. 3.12, Prop. 3.13 | medium |
| `TR_lipschitz_extension` | reduction | Lipschitz, constrained → unconstrained | upper (as a tool) | §3.7, Prop. 3.18 | low |

Parameter maps worth stating:

- Quadratic as linear: $d \mapsto d_2 = (d^2 + 3d + 2)/2$ via the degree-2 feature map. The image of $K$ is not convex, so the book uses a cover and discrete exponential weights. The reduction ignores computation.
- Simple from cumulative: $\mathrm{sReg}_n \le \mathrm{Reg}_n / n$ with the average iterate as output (needs convexity).
- High-probability regret to sample complexity: for $\mathrm{Reg}_n \le A n^p$ with $p \in (0,1)$, sample complexity is at most $1 + (A/\varepsilon)^{1/(1-p)}$.
- Submodular minimisation: $K = [0,1]^d$, so $\mathrm{diam}(K) = \sqrt d$ and $\vartheta = \Theta(d)$; the reduction needs the book's action-dependent noise model (randomised rounding creates it).

### What the rules teach about the specialisation order

1. **Not every edge is set inclusion.** Improper ⊑ constrained holds because the learner has more power, not because one environment class contains the other. Improper ⊑ unconstrained holds because the adversary has less power. The ontology therefore needs an "easier–harder" edge kind alongside inclusion.
2. **Edges have validity scopes.** Stochastic ⊑ adversarial is exact only for the book's adversarial model, which allows noise. For the common noise-free adversarial model with bounded losses it holds only up to log factors (Shamir's scaling and truncation argument). These are two edge kinds, and the engine must keep the log-factor loss when it propagates.
3. **Function classes order by reverse inclusion of property sets**, with implications the book does not state as rules: linear ⇒ quadratic, linear ⇒ smooth with $\beta = 0$, quadratic ⇒ smooth with $\beta = 2\lVert A\rVert$. Parameters are monotone: larger $\beta$ or smaller $\alpha$ gives a larger class. Note 6.vi uses linear ⇒ smooth to show that smoothness alone cannot beat $d\sqrt n$.
4. **Metric transfers are one-way and not always tight.** Cumulative regret bounds give simple-regret and sample-complexity bounds, never the reverse. X5 is a witness of non-tightness: for quadratic smooth strongly convex losses in the improper setting, cumulative regret is $\Theta(d\sqrt n)$ but simple regret is $O(d^2/n)$, far below $\Theta(d\sqrt n)/n = \Theta(d/\sqrt n)$. The ontology notes propose storing such witnesses as first-class separations.
5. **Some reductions change parameters or ignore computation.** Quadratic-as-linear maps $d$ to $d_2$ and is statistical only, so it must not carry the `compute` field across. The submodular reduction crosses to a different problem and adds an additive cost.
6. **Lower bounds on specific bodies transfer only to families.** A bound on $B_1$ or the cube is a bound on "all convex bodies", not on every $K$. Transfer along the constraint-set shape must go from specific to general.
7. **Some things must be recorded as non-transfers.** Lower bounds on the information ratio or on $\Lambda^\star$ do not imply regret lower bounds (§8.7). Recording this stops the engine from inferring them.
8. **Non-constructive results come from an equality of minimax values.** Bayesian–adversarial minimax duality (Thm 8.17) gives existence only, which is why U12, U16 and U18 have compute $\infty$.
9. **Some rules are tools, not edges.** Scaling invariance is a sanity check on bound expressions (they must depend on Lipschitz constant times diameter and on $\alpha/\beta$ in an invariant way). Shrinking to $(1-\varepsilon)K$ changes the Lipschitz constant to $1/(\varepsilon r)$, so it is not an edge to $\mathcal F_{b,l}$ without rescaling. The Lipschitz extension cannot always be evaluated.

## 5. Open problems

The YAML records 27 open problems: the 13 items of Chapter 14 (Outlook 14.i–14.xiii), 10 exercises (ids `EX-…`), and 4 from notes and §2.4 (ids `N-…`). Most entries have no `section` field; the id carries the location. The ids of two note-derived problems do not match their recorded location (`N-6.7-highly-smooth-beta` cites Note 6.vi, `N-8.8-thompson-adversarial` cites Note 8.iii). Each has a kind, the settings concerned and, for bound gaps, the known bounds. Statements are paraphrases in the YAML; the quotes are kept there.

### Bound gaps

| Id | Settings | Question | Known bounds |
|---|---|---|---|
| 14.i | $\mathcal F_b$, $\mathcal F^{(s)}_b$ | Minimax regret for bounded convex losses | upper $\tilde O(d^{1.5}\sqrt n)$ (stochastic), $\tilde O(d^{2.5}\sqrt n)$ (adversarial); lower $\Omega(d\sqrt n)$ |
| 14.xii | $\mathcal F_{b,d=1}$ | Are the log factors needed for $d = 1$? | $O(\sqrt n\log n)$ vs $\Omega(\sqrt n)$; lower bound uncited; setting presumed adversarial |
| EX-8.24 | $\mathcal F_b$ | Show $\Lambda^\star = \tilde\Omega(d^2)$ | $\Psi^\star \le C d^4 \log(nd)$; $\Lambda^\star \le 14\Psi^\star$; $\Psi^\star = \tilde\Omega(d^2)$. A complexity measure, not regret |
| N-2.4-simple-linear | $\mathcal F^{(s)}_{b,lin}$ | No written simple-regret lower bound for linear losses | $\Omega(d/\sqrt n)$ informally on $[-1,1]^d$ (X2). A gap in the literature, not a hard problem |
| N-6.7-highly-smooth-beta | approx. $\mathcal F^{(s,i)}_{l,sm,sc}$ | Right dependence on $\beta$ for order-$p$ smooth, strongly convex losses | simple regret $O\big(\tfrac1\alpha (d^2/n)^{(p-1)/p}\big)$ vs $\Omega\big(\tfrac{d}{\alpha} n^{-(p-1)/p}\big)$; they match at $p = 2$ |
| N-8.8-thompson-adversarial | $\mathcal F_{b,d=1}$ | Does Thompson sampling get $\tilde O(\sqrt n)$ Bayesian regret? | $\tilde O(\sqrt n)$ in the stochastic $d = 1$ setting; information ratio unbounded |

### Computational

| Id | Settings | Question |
|---|---|---|
| 14.iii | $\mathcal F_b$, $\mathcal F^{(s)}_b$ | Is $\Omega(d^2)$ memory needed for $\tilde O(\mathrm{poly}(d)\sqrt n)$ regret without smoothness and strong convexity? All known algorithms use $O(d^2)$ |
| EX-9.28 | $\mathcal F^{(s)}_b$ | Polynomial-time inscribed-ellipsoid method with $\tilde O(d^4/\varepsilon^2)$ samples when $K$ is given by a separation oracle |
| EX-10.17 | $\mathcal F^{(s)}_b$ | Polynomial-time positioning with $B_1 \subset K \subset B_{2d}$ and $M(K) = \tilde O(d^{-1/2})$; would make U24 polynomial time |
| EX-10.18 | $\mathcal F^{(s)}_b$ | Polynomial-time positioning so that the polar of $K$ is approximately isotropic |
| EX-10.20 | $\mathcal F^{(s)}_b$ | $\tilde O(d^2)$-time approximation of $(\Sigma^{-1} + uu^\top)^{-1/2}$; currently $O(d^3 + md^2)$ for a polytope with $m$ constraints |
| EX-11.23 | $\mathcal F_b$ | $O(\mathrm{poly}(d, \log n))$ per-round time for adversarial online Newton step; currently $\mathrm{poly}(d,n)$ (U26) |

### Algorithmic

| Id | Settings | Question |
|---|---|---|
| 14.ii | $\mathcal F_b$, $\mathcal F^{(s)}_b$ | A simple, practical algorithm with the $\sqrt n$ rate for $d > 1$ without smoothness and strong convexity |
| 14.v | all | Adapting to an unknown function class; anytime algorithms without a doubling trick |
| 14.vii | $\mathcal F_b$, $\mathcal F^{(s)}_b$ | An optimistic surrogate built from exponential weights instead of a Gaussian |
| 14.ix | $\mathcal F_b$ | Understanding exploration by optimisation (Algorithm 8.3) and its loss estimators |
| N-6.7-adaptive-ftrl | $\mathcal F_b$, $\mathcal F_{b,sm}$ | One algorithm achieving the better of Thm 6.13 and Thm 6.14 by adaptive tuning |

### Analysis

| Id | Settings | Question |
|---|---|---|
| 14.iv | $\mathcal F^{(s)}_b$ | Bounds where the loss range $B$ enters only a lower-order term, not multiplied by the noise scale $\sigma$ |
| EX-4.5 | $\mathcal F^{(s)}_{l,d=1}$ | A slicker proof of Prop. 4.3 (bisection); a proof-technique question |
| EX-6.21 | $\mathcal F^{(s)}_b$ | Apply the §6.6 variance technique to other algorithms |
| EX-10.19 | $\mathcal F^{(s)}_b$ | Regret of online Newton step under Assumption 6.17 |
| EX-10.21 | $\mathcal F^{(s)}_b$ | Does Thm 10.8 hold without the projection onto $K_\varepsilon$? |

### Modelling and conceptual

| Id | Kind | Question |
|---|---|---|
| 14.vi | modelling | Non-convex losses (stationary points), quasi-convexity, Polyak–Łojasiewicz. Classes not closed under addition do not suit the adversarial setting |
| 14.xi | modelling | Heavy-tailed, heteroscedastic or multiplicative noise |
| 14.xiii | modelling | BCO on Riemannian manifolds beyond the known $O(n^{2/3})$ analogue of FTRL |
| 14.viii | conceptual | A black-box reduction from stochastic to adversarial algorithms (restart when the minimum moves). A positive answer would be a new transfer rule, the reverse of `TR_sto_adv` for upper bounds |
| 14.x | conceptual | Unifying stochastic approximation (asymptotics) with minimax finite-time BCO |

Only 14.i, 14.xii and, informally, N-2.4-simple-linear are gaps that the atlas's comparison of bounds can detect on its own. EX-8.24 concerns a complexity measure, and N-6.7-highly-smooth-beta needs a function class (order-$p$ smoothness) outside Definition 1.1. The rest are computational, algorithmic or modelling questions that a bound table cannot express without the `compute` field or new dimensions.

## 6. Known problems in the transcription

These are recorded in the YAML and the ontology notes; they matter for anyone checking the data against the book.

- **U16 citation.** The bib key BEL18 resolves to a paper on Langevin Monte Carlo. §2.2 attributes the first non-constructive $\mathrm{poly}(d)\sqrt n$ adversarial bound to Bubeck & Eldan 2018 ("Exploratory distributions for convex functions"), which is probably what was meant. The bound is recorded as printed, with low confidence.
- **U26 hyperlink.** The table links to Thm 10.8 (stochastic) while the chapter column says Chapter 11; the matching statement is Thm 11.8.
- **U11 class.** Printed $\mathcal F^{(s)}$ with $\tilde O$; Note 2.v says $\mathcal F_b$ with $O$.
- **U14 key.** Key BEL16, but the bibliography entry is the 2017 STOC paper.
- **U10 LaTeX.** A misplaced closing parenthesis inside the square root; the intended bound follows Thm 6.16.
- **U23 notation.** §2.2 writes $O(d^{1.5}\sqrt n)$ for the same result that the table writes as $\tilde O$.
- **14.i** has a stray "§" after the adversarial bound in the source.
- **Symbol clash.** In Thms 10.8 and 11.8, $L$ is a logarithmic factor, not a Lipschitz constant. A naive extractor will map it to the canonical `L`.
