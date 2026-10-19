# Related work

Literature sweep done 2026-10-19, using web search plus fetches of the primary pages and PDFs. Items marked **[unverified]** were seen only in secondary sources, or only at the abstract level.

## Verdict on novelty

**No existing system does what we propose.** That is: settings defined by assumptions, a typed specialisation order between settings, upper and lower bounds stored as symbolic expressions with provenance, automatic propagation along the order to find gaps, and LLM extraction at scale. Searches for regret-bound databases, bandit "zoos", learning-theory atlases and rate tables for optimisation or sample complexity found nothing that combines these. That is evidence of absence from a careful search, not a proof.

The idea is not new in *spirit*. The precedents fall into five groups, and each has part of it:

| | Hierarchy of settings | Quantitative results per node | Propagation / inference | Automated extraction | Domain |
|---|---|---|---|---|---|
| **ISGCI** | ✓ (graph classes, inclusions) | 3-valued complexity status plus parameter bounds | ✓ (with derivation notes) | ✗ (curated) | graph theory |
| **π-Base / CatDat** | ✓ (properties and implications) | ✗ (booleans; cardinals planned) | ✓ (forward chaining, generated proofs) | ✗ (PR-curated) | topology, category theory |
| **Complexity Zoology** (Kuperberg) | ✓ | ✗ (inclusion/separation only) | ✓ ("robozoologist") | ✗ | complexity classes |
| **Equational Theories Project** | ✓ (implication graph) | ✗ | ✓ (transitive closure) | partly (automated provers) | universal algebra |
| **Survey and book tables** (e.g. Lattimore's *BCO*) | implicit, in prose | ✓ | by hand | ✗ | bandits, optimisation |
| **Papers with Code / AxCell / SciLead** | ✗ (flat task keys) | ✓ (empirical numbers) | ✗ | ✓ | empirical ML |
| **TheoremKB / TheoremSearch / TheoremGraph** | ✗ | ✗ (statement text only) | dependency edges | ✓ | all of maths |
| **ORKG** | ✗ | ✓ (generic comparison tables) | ✗ | partly (LLM-assisted) | all of science |
| **This project** | ✓ | ✓ (symbolic bounds, partial order) | ✓ | ✓ | ML theory → general |

The new contribution is the combination. Specifically: (i) **quantitative, regime-dependent values** on nodes instead of booleans or complexity classes; (ii) **LLM extraction** instead of hand curation; (iii) applying this to **ML theory**, where nothing of the kind exists.

---

## 1. Curated hierarchies with inference (closest in spirit)

### ISGCI: Information System on Graph Classes and their Inclusions
<https://www.graphclasses.org/>
- **Scale (2026-10-19):** 1,694 graph classes, 242,192 inclusions, 28,930 complexity results, 51,968 bounds. Maintained by H.N. de Ridder since 2001 and active, with v4 in development.
- **Inference:** inclusions are deduced automatically. Complexity results propagate along them: NP-hardness goes up to superclasses, polynomial-time solvability goes down to subclasses. Results also transfer across problems (via reductions) and across parameters.
- **Provenance:** every fact carries a provenance note ("[by definition]", "[trivial]", a citation, or a derivation such as "NP-complete on split").
- **Limitations:**
  - It cannot answer "not a subclass", because non-inclusions are not stored.
  - It has duplicate classes (e.g. Perfect = Berge).
  - "Unknown" means "unknown to ISGCI", not "open in the literature".
  - Submission is by email, curation is by a single team, and the raw data is not openly downloadable.
- **Relevance:** this is our design, applied to graph theory, and the precedent to position against. The difference is that our node values are symbolic bounds, not a three-valued status, and that we extract with LLMs.

### π-Base (and the π-Base family)
<https://topology.pi-base.org/>, data at <https://github.com/pi-base/data>; Clontz, "Database-Driven Mathematical Inquiry", [arXiv:2404.05778](https://arxiv.org/abs/2404.05778).
- **Data:** 224 spaces, 247 properties, 935 theorems of the form "AND(properties) ⇒ property", and 2,139 asserted traits. Everything else is deduced, including through contrapositives.
- **Engineering:**
  - One Markdown-plus-YAML file per entity, with stable IDs.
  - CC-BY data and MIT code.
  - PR-based review, and CI that rejects contradictions.
  - "Don't add what can be deduced."
  - Proofs are generated for deduced facts.
  - A "find counterexamples" search: property combinations with neither an example nor a proof are candidate open problems.
- **AI policy:** "Submissions that are the unedited output of an AI tool will be closed without review."
- **Direction:** Clontz's 2026 slides plan **cardinal-valued properties** and conditional assumptions (e.g. "assume CH"). π-Base is hitting the "need ordered values, not booleans" wall, which our project needs from day one.
- **Siblings:**
  - **CatDat** (<https://catdat.app>, category theory): 861 implications generate 92% of its 28k property facts automatically, roughly 12× leverage. It has a "Missing data" page.
  - Also pi-base-topos, DaRT (ring theory) and the Adjectives Project (schemes).

### Complexity Zoology (Kuperberg) and the Complexity Zoo (Aaronson)
- **Complexity Zoology** (<https://math.ucdavis.edu/~greg/zoology/intro.html>): a "robozoologist" that infers inclusions and separations, relative to oracles, from the Zoo.
  - **Scale:** 394 classes, 43,653 inclusions, 92,210 separations.
  - **Open vs blank:** it explicitly distinguishes **open** cases (240, known to the community as open) from **blank** cases (18,739, where the system simply doesn't know).
  - **Citation explosion:** it notes that following every inference made the citation data blow up, which is an argument for storing provenance as a derivation DAG.
  - Looks unmaintained.
  - R. J. Sanders' thesis (UC Davis 2019) describes a related inference system for complexity classes **[unverified in detail]**.
- **Complexity Zoo** (<https://complexityzoo.net>): a MediaWiki with 400+ classes. It is free text, not machine-readable, and has had to move host repeatedly. The site was unreachable on 2026-10-19 **[unverified status]**.

### Equational Theories Project (Tao et al.)
<https://teorth.github.io/equational_theories/>, [arXiv:2512.07087](https://arxiv.org/abs/2512.07087)
- Settled all 22,028,942 implications between 4,694 magma laws, crowdsourced and with automated provers. Everything was formalised in Lean by April 2025.
- Only 10,657 positive and 586,925 negative implications are stored explicitly; the rest are **derived by transitivity and duality closure**.
- **Lessons:**
  - Store a minimal generating set and compute the closure.
  - Treat refutations (counterexamples / separations) as first-class objects.
  - Keep a live dashboard of what is resolved.

### Other hierarchy and problem databases

| Resource | Notes and lesson |
|---|---|
| Graph Parameter Hierarchy (Sorge & Weller, 2019, [PDF](https://manyu.pro/assets/parameter-hierarchy.pdf)) | Hand-drawn diagram with a lemma on every edge. Edges are theorems with provenance. Static PDF, inactive; the linked "Graph Parameter Project" site is dead. |
| Crescenzi–Kann compendium of NP optimisation problems ([link](https://www.csc.kth.se/~viggo/problemlist/compendium.html)) | Approximability upper and lower bounds per problem, with references. The best CS precedent for "upper and lower bound per problem". **Last updated 2000**, and died when its editors stopped. |
| Quantum Algorithm Zoo ([link](https://quantumalgorithmzoo.org/)) | Prose entry per problem with a coarse speedup label. Active, single maintainer. Useful idea: coarse gap badges such as "log-factor gap" vs "polynomial gap". |
| Algorithms with Predictions (ALPS, [link](https://algorithms-with-predictions.github.io/)) | 454 YAML-per-paper entries, maintained by community PRs. Shows a small theory community will maintain YAML in git, but it stops at labels and records no bounds. |
| Algorithm-Wiki (Sherry & Thompson, *Proc. IEEE* 2021) | Worst-case time complexity for algorithm families, compiled by hand from ~1,110 papers. No hierarchy or inference. |
| Erdős Problems ([site](https://www.erdosproblems.com/), [data](https://github.com/teorth/erdosproblems)) | YAML with a schema, validated by CI, with machine-readable status. Flooded with AI-found results, so provenance tags for "AI-produced / human-verified" are needed. |
| Formal Conjectures (DeepMind, [repo](https://github.com/google-deepmind/formal-conjectures)) | Open conjectures stated in Lean. The main failure mode is misformalisation, which is the analogue of our extraction errors. |
| OEIS, LMFDB, mathlib, Groupprops, Open Problem Garden | Long-lived curation (OEIS editorial review); typeclass hierarchies as machine-checked "special case" relations (mathlib). Cautionary cases: Groupprops went dormant with its maintainer; Open Problem Garden is overrun with spam. |
| MathBases ([ICMS 2026](https://icms-conference.org/2026/papers/paper60/main.pdf)) | Index of 130+ maths databases. We should register there. |
| Fine-grained complexity | **No database exists.** The web of conditional reductions (SETH, 3SUM, APSP) has the same shape as our graph. Another candidate domain, and a reminder to model conditional lower bounds as first-class. |

---

## 2. ML-theory-specific prior art

### Books and surveys with tables (hand-made slices of our graph)
- **Lattimore, *Bandit Convex Optimisation*** ([arXiv:2402.06535](https://arxiv.org/abs/2402.06535), v5 2025). **The single most relevant document.**
  - Function classes are named by assumption subscripts (ℱ_{b,l,sc,sm}).
  - Tables 2.1 and 2.2 tabulate lower and upper bounds.
  - §2.4 spells out *transfer rules in prose*: improper is easier than constrained, adversarial is harder than stochastic, and simple-regret bounds imply cumulative-regret bounds.
  - Chapter 14 lists open problems (e.g. Ω(d√n) vs Õ(d^{1.5}√n)).
  - Note 1.vii: "the number of settings and possible assumptions is enormous."
  - **Use as a ground-truth test set.**
- **Lattimore & Szepesvári, *Bandit Algorithms*** (CUP 2020). Table 4.1 defines environment classes *as sets of distributions*, so "special case" becomes literal set inclusion. This gives our edges a clean semantics.
- **Slivkins, *Introduction to Multi-Armed Bandits*** ([arXiv:1904.07272](https://arxiv.org/abs/1904.07272)). Its "multi-dimensional problem space" (feedback, reward model, contexts, priors, structure, constraints) is a ready-made set of ontology dimensions.
- **Bubeck, *Convex Optimization: Algorithms and Complexity*** ([arXiv:1405.4980](https://arxiv.org/abs/1405.4980)), Table 1.1: oracle complexity by function class.
- **Burtini, Loeppky & Lawrence** ([arXiv:1510.00757](https://arxiv.org/abs/1510.00757)): a taxonomy of MAB variants plus a "Known Regret Bounds" table. Typical weaknesses: flat setting labels, no lower bounds, no structure.
- **Steier, "PAC Guarantees for RL"** ([arXiv:2603.01309](https://arxiv.org/abs/2603.01309), 2026): rate lookup tables indexed by Coverage–Structure–Objective coordinates. A static PDF, but a recent sign of demand for coordinates on the space of settings **[checked only at the abstract level]**.
- Comparison tables in individual papers (e.g. Audibert, Bubeck & Lugosi on combinatorial bandits, [arXiv:1204.4710](https://arxiv.org/abs/1204.4710)) are raw material for ingestion and cross-checking.

### Hand-drawn inclusion diagrams in RL theory
These papers draw our specialisation edges by hand, each one frozen inside its own paper:
- Bilinear Classes (Du et al., ICML 2021): a containment matrix between frameworks.
- Bellman–Eluder dimension (Jin, Liu & Miryoosefi, NeurIPS 2021): an inclusion diagram of families of RL problems.
- GEC (Zhong et al., [arXiv:2211.01962](https://arxiv.org/abs/2211.01962)).
- Foster & Rakhlin's lecture notes ([arXiv:2312.16730](https://arxiv.org/abs/2312.16730)): a landscape of settings along three axes.

**Lesson:** settings are often *parameterised by complexity measures* (e.g. "BE-dimension ≤ d"), and containment claims are theorems that need their own provenance.

### Unifying theories and complete classifications
- **Decision–Estimation Coefficient** (Foster, Kakade, Qian & Rakhlin, [arXiv:2112.13487](https://arxiv.org/abs/2112.13487)): one general theorem gives a lower bound, and a nearly matching upper bound, *for any* interactive decision problem. Bounds can come from **instantiating a general theorem at a node**, not only from a paper about that node.
- **Partial monitoring classification** (Bartók, Pál & Szepesvári 2010; Bartók et al., *Math. OR* 2014; Lattimore & Szepesvári, [arXiv:1805.09247](https://arxiv.org/abs/1805.09247)): every finite game is trivial (0), easy (Θ̃(√T)), hard (Θ(T^{2/3})) or hopeless (Θ(T)). This is a **classification theorem that settles a whole parameterised family**.
- **Feedback graphs** (Alon, Cesa-Bianchi, Dekel & Koren, [arXiv:1502.07617](https://arxiv.org/abs/1502.07617)): a characterisation by observability, with known remaining log-factor gaps. Good test cases for gap detection.

### Open-problem sources
- **COLT Open Problems** (yearly, in PMLR). **Nobody keeps a status index of them.** They make a natural evaluation set for gap detection, and a status tracker would be a contribution in itself.
- `WhenWen/dl-open-problems` (GitHub, created 2026-10): an evidence-tracked catalogue of open problems with logs of searches that found nothing. Not a graph, but a curation workflow worth copying.
- **VALG** ([arXiv:2608.13060](https://arxiv.org/abs/2608.13060), 2026): an agent that attacks COLT 2026 open problems. It is a natural *consumer* of our graph **[checked only at the abstract level]**.

### Formal verification
- **Lean Machine Learning library** (<https://github.com/LeanMachineLearning/LML>): formalised bandit framework, regret bounds for ETC, UCB and Thompson sampling, and the start of lower-bound machinery.
- **Rémy Degenne** is formalising individual COLT 2026 bandit papers in Lean.
- **Relevance:** a Lean-checked result could be the highest provenance tier, and specialisation edges could eventually be machine-checked implications between hypotheses. This group is also the most likely to build something overlapping, so **worth contacting**.

### Ontologies of ML
**OntoDM, ML-Schema, MEX** and **ITO** (Intelligence Task Ontology, Blagec et al., *Scientific Data* 2022) all model *empirical* tasks, experiments and benchmarks. ITO is structurally the closest: a task hierarchy plus benchmark results. **No ontology of learning-theory assumptions exists**, so we have to design one. We can reuse PROV-O for provenance and link out to ITO and ML-Schema identifiers.

### Optimisation
- **PEPit** (Goujaud et al., *Math. Prog. Comp.* 2024): computes tight worst-case rates for first-order methods via SDP. This suggests a provenance type for bounds that are "computed" rather than cited.
- Unified-analysis papers (e.g. Gorbunov, Hanzely & Richtárik, "A Unified Theory of SGD", AISTATS 2020): one theorem gives rates for many special cases. This fits our downward propagation directly.
- No maintained database of rates was found.

### Paper lists
Awesome-bandit lists and course sites (rltheory.github.io, rltheorybook.github.io) are lists of papers or teaching material, with no bounds or structure. Most are abandoned.

---

## 3. Automated extraction from scientific papers

### Leaderboards built from empirical results
- **Papers with Code** (Meta) was **shut down without notice in July 2025**. Only a frozen JSON dump remains (`paperswithcode/paperswithcode-data`), and the leaderboards were not carried over. **Lesson:** keep open data and governance independent of any single host.
- **AxCell** (Kardas et al., EMNLP 2020), **TDMS-IE** (Hou et al., ACL 2019), **SciREX** (Jain et al., ACL 2020), **SciLead** (Şahinuç et al., EMNLP 2024), **LEGOBench** (2024) and **League** (2025).
  - The consistent finding across a decade of work: **identifying the setting (task, dataset, metric) is the easier part, and extracting the exact result value is the hard part.**
  - TDMS-IE: macro-F1 56.6 for (task, dataset, metric) triples, dropping sharply once scores are included.
  - SciLead: LLMs get the triples right but struggle with the values.
  - **For us, the bound expression is the "value", so most of our validation effort should go there.**

### ORKG: Open Research Knowledge Graph (TIB Hannover)
- **Scale:** >10k papers and >1k comparisons as of 2023.
- **LLM extraction:** has been explored (Nechakhin et al., [arXiv:2405.02105](https://arxiv.org/abs/2405.02105); ORKG ASK, [arXiv:2412.04977](https://arxiv.org/abs/2412.04977)). LLMs work as *recommenders* of structure and need fine-tuning or careful prompting.
- **Limits:** no "special case" semantics, no inference, and open-ended per-field templates that hurt consistency. That supports our fixed schema (D3).
- **Use for us:** a possible interop or hosting target.

### Theorem and statement extraction from arXiv
- **TheoremKB** (Mishra et al., SDP@ACL 2024; theoremkb.org):
  - Trained on all 1.7M arXiv papers available up to 2020, with labels generated by recompiling the LaTeX with an instrumented package.
  - Classifies PDF paragraphs as text, theorem or proof with about 84% accuracy.
  - Linking the same result across papers is weak (38% at best).
  - Its motivating query ("which variants of vertex cover are polynomial?") is exactly our use case, but it never got as far as structured settings or bounds.
- **TheoremSearch** ([arXiv:2602.05216](https://arxiv.org/abs/2602.05216), 2026): 9.2M theorem statements with an API and an MCP server. Usable for retrieval and cross-checking.
- **TheoremGraph** ([arXiv:2606.25363](https://arxiv.org/abs/2606.25363), 2026): 11.7M statements and 18.3M candidate dependency edges. **Every edge is tagged with the extractor that produced it, and users filter by confidence.** A provenance design worth copying.
- **NaturalProofs** (Welleck et al., NeurIPS 2021), **MathGloss** ([arXiv:2311.12649](https://arxiv.org/abs/2311.12649)), definition extraction (Jiang & Senellart 2023; SciDef 2026), **ARQMath** (formula retrieval), **zbMATH Open** (metadata and formula search), **MaRDI** (a Wikibase knowledge graph for maths, which is a realistic hosting option) and **sTeX/SMGloM** (theory graphs with inheritance that rely on authors annotating their own papers, with little uptake).
- **unarXive 2022** (Saier et al.): 1.9M arXiv papers already parsed from LaTeX. A pre-processed alternative.

### LLM-era extraction, surveys and discovery
- **AOE benchmark** ([arXiv:2507.16271](https://arxiv.org/abs/2507.16271)): building structured tables from long documents. The best LLM reaches **28% cell-F1**, and outputs are well formatted but wrong. Validate *content*, not just the schema.
- **ChatExtract** (Polak & Morgan, *Nat. Commun.* 2024): uncertainty-inducing follow-up questions push GPT-4 to about 90% precision and recall. A cheap self-verification step to reuse.
- **ArxivDIGESTables** (Newman et al., EMNLP 2024): 2,228 review tables from arXiv, split into generating a schema and filling values. We avoid the schema-generation half by fixing the schema.
- **AutoSurvey** (Wang et al., NeurIPS 2024): prose surveys with about 80% citation precision and recall. Not structured or queryable.
- **PaperQA2 / ContraCrow** (FutureHouse 2024): finds contradictions between papers, with about 70% confirmed by experts. Our symbolic comparison of bounds (an upper bound below a lower bound on the same setting) should be more reliable.
- **SciMON** (ACL 2024), GAPMAP, LimitGen: "gap finding" from free text is weak, which argues for structural gap detection.
- **The Erdős problems and GPT-5 episode** (Oct 2025, [arXiv:2511.16072](https://arxiv.org/abs/2511.16072)): problems listed as open turned out to have published solutions. **Many apparent gaps are coverage holes in the corpus.** Run a retrieval step targeted at each candidate gap before calling it open.
- **Reliability of LLM extraction:**
  - Gartlehner et al. (2023): Claude 2 reached about 96% accuracy on simple fields from RCTs, but complex conditional fields score much lower.
  - Elicit's independent evaluation (*Res. Synth. Methods* 2025): repeat runs agreed on extracted values 90% of the time but on supporting quotes only 46%.
  - So expect non-determinism: use self-consistency and store the evidence quote for every field.

### Data access
- arXiv LaTeX source is available per paper (`arxiv.org/src/<id>`) or in bulk from S3 (requester pays).
- The default arXiv licence does not allow redistribution: **extract and link back, don't rehost sources.**
- Semantic Scholar (>200M papers, citation intents) and OpenAlex (CC0) provide metadata and the citation graph.

---

## 4. Lessons adopted

These feed into [desiderata.md](desiderata.md) and [plan.md](plan.md):

1. **Store generating facts and compute the closure** (ETP, ISGCI, CatDat). Show derivations as a DAG, as ISGCI's notes and π-Base's generated proofs do; this avoids Zoology's citation explosion.
2. **Model these as first-class from the start**, because every precedent hit them later:
   - non-inclusions and separations (ISGCI);
   - equivalent or duplicate nodes;
   - conditional results (under a hypothesis or a variant assumption);
   - **open vs blank** (Zoology).
3. **Ordered values, not booleans** (where π-Base is heading now).
4. **Edges are typed and carry provenance:**
   - set inclusion;
   - reductions with parameter maps;
   - transfers between metrics (simple → cumulative regret), from Lattimore *BCO* §2.4;
   - transfers that lose a log factor.
5. **Parameterised nodes and classification theorems** that settle a whole family (partial monitoring, feedback graphs, DEC).
6. **Provenance tiers:** extracted → human-verified → derived from a general theorem → computed (PEPit-style) → formally verified (Lean / LML).
7. **Bound values are the weak point of extraction.** Check them symbolically, run self-verification follow-ups, run several times for self-consistency, and store an evidence quote for every field.
8. **A gap is only a candidate open problem until a targeted retrieval search fails to find a resolving paper** (the Erdős episode).
9. **Ground-truth evaluation sets:** Lattimore *BCO* Tables 2.1–2.2 and Chapter 14; COLT open problems.
10. **Sustainability:** an open git repo of data with a CC-BY licence, PR review, CI consistency checks, and no single maintainer or corporate host. The failures are Papers with Code, Crescenzi–Kann, Groupprops, Open Problem Garden and the Complexity Zoo's hosting.
11. **AI governance:** tag every fact with how it was extracted, and gate writes behind human review (π-Base's policy, the misformalisation risk in Formal Conjectures).
12. **People to talk to:**
    - the Lean Machine Learning community (Degenne) about overlap and collaboration;
    - π-Base (Clontz, Dabbs) about engineering and their move to valued properties;
    - possibly the ISGCI maintainers.
