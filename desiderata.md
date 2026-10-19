# Desiderata

Requirements the system must satisfy. **D1–D3 are the core design points**; the rest are supporting requirements. Each item lists what it means and why.

---

## D1. Settings form a partial order with directed specialisation edges, and results propagate along them

**What.**
- A setting is an assumption vector over the ontology's dimensions (D3).
- Each dimension has its own specialisation order (e.g. `K-armed ⊑ linear`, `stochastic-iid ⊑ stochastic-corrupted`). The setting order is primarily the **product order**: S ⊑ S′ iff S is at least as specialised as S′ in every dimension.
- **Cross-dimension reductions** that the product order misses (e.g. a K-armed bandit *is* a linear bandit with d = K and canonical basis actions) are added as explicit edges.
- Every edge carries a **parameter map** (e.g. `d ↦ K`) so a bound can be translated: √(dT) in linear ⇒ √(KT) in K-armed.
- Every edge carries a **justification** (a citation or short argument) and a **validity scope**: which regret notions it preserves. Some "obvious" inclusions are subtle — e.g. stochastic ⊑ adversarial holds for pseudo-regret but needs care for other regret definitions.
- **Inference rules:**
  - an upper bound on S′ holds on every S ⊑ S′ (translated by the parameter map);
  - a lower bound on S holds on every S′ ⊒ S.
  - Inferred results are stored separately from extracted ones, with the derivation path, and are never confused with directly proved results.
- The **"neighbour" view** (settings differing in one assumption) is the covering relation, i.e. the Hasse diagram, of this order. It is used for navigation and visualisation; the full order is used for inference.
- **Edges are typed**, at least as: set inclusion of environment classes (the semantics in Lattimore & Szepesvári); a reduction with a parameter map; a metric transfer (e.g. simple regret ⇒ cumulative regret); a transfer that holds only up to a log factor. Edges are themselves results, with their own provenance.
- **Store a generating set and compute the closure.** Only directly stated facts are stored; everything else is derived. This follows ETP, ISGCI and CatDat.
- **The following are first-class from day one**, because every precedent had to retrofit them ([related-work.md](related-work.md) §4):
  - **non-inclusions / separations**, i.e. "S is strictly harder than S′", witnessed by a lower bound;
  - **equivalent nodes**: two names in the literature for one setting, merged explicitly;
  - **conditional results**: under a conjecture, or under a variant assumption;
  - **open vs blank**: "known to be open in the literature" is different from "the system cannot deduce it".

**Why.** Inheritance turns a sparse set of extracted results into a dense map of best-known bounds, including results nobody wrote down. It is what makes gap detection meaningful. Symmetric "differs by one assumption" edges cannot do this.

---

## D2. Bounds are compared as a partial order, never forced into a total order

**What.**
- A bound is a **symbolic expression** (SymPy-parseable) over a canonical variable vocabulary (`T, K, d, Delta_min, Delta_i, sigma, delta, …`), plus:
  - **side** — upper / lower;
  - **notation** — `O`, `Õ` (polylog factors hidden), `Θ`, `Ω`, exact (with constants), or asymptotic limit (e.g. `lim inf R_T / log T ≥ …`);
  - **quantity** — pseudo-regret, expected regret, high-probability regret (with δ), Bayesian regret, simple regret, sample complexity, …;
  - **type** — worst-case/minimax vs instance-/gap-dependent;
  - **horizon** — known T vs anytime;
  - **extra assumptions** beyond the node's setting;
  - **algorithm** for upper bounds; the **class of algorithms** for lower bounds (all, consistent, uniformly good, …).
- Comparison is **regime-conditional**: two bounds are comparable only for the same quantity/type and within a stated regime (e.g. "minimax, polylog factors ignored, d ≤ K"). Within a regime we compute dominance; across regimes we show the **Pareto front**.
- Each node reports a **tightness status** per regime: tight (up to constants), tight up to log factors, polynomial gap, no lower bound known, no upper bound known.
- Comparison should be automatable for the common case (monomials/polylogs in a few variables, compared by exponents) and fall back to "incomparable — needs human" otherwise.

**Why.** "Ordered tables" are the headline feature but a naïve ordering is wrong: √(KT), √(dT log T) and Σᵢ log T / Δᵢ are not comparable without fixing a regime. Getting this right is what makes the tables trustworthy.

---

## D3. A fixed, versioned ontology; extraction fills a schema, not free text

**What.**
- Settings are described by a **controlled vocabulary**: a set of dimensions, each with enumerated values and its own specialisation order (see [schema.md](schema.md)).
- The LLM extractor must map each paper to these values. Anything it cannot map goes in an explicit **`unmapped`** field, which is reviewed to drive ontology revisions — new setting types surface instead of being silently forced into the wrong slot.
- The ontology is **versioned**; extractions record the ontology version, and migrations are scripted.
- The **core** (setting = assumption vector, bound representation, inference engine, provenance) is **domain-agnostic**; each domain (bandits, RL theory, convex optimisation, …) supplies its own ontology module.

**Why.** Without a fixed vocabulary, 1000 papers produce 1000 slightly different names for the same setting and the graph is useless. Domain-agnostic core is required because the end goal is ML/CS/maths theory in general; bandits are the pilot.

---

## D4. Provenance for every claim

Every extracted result links to: paper (arXiv id / DOI), version, theorem/corollary label and number, a verbatim quote of the statement, and the extractor run (model, prompt version, date). Every inferred result links to its derivation path, stored as a DAG rather than a flattened citation list. Users must be able to go from any table cell to the exact source sentence in one click.

**Provenance tiers.** Each result records how it is known:
1. extracted by an LLM;
2. human-verified;
3. derived by instantiating a general theorem at this node (e.g. a DEC bound or a unified SGD rate);
4. computed (e.g. PEPit-style);
5. formally verified (Lean / LML).

## D5. Explicit verification status

Each record carries a status: `extracted` → `auto-checked` (schema-valid, expression parses, cross-checked against other papers' comparison tables) → `human-verified`. Disagreements between sources (e.g. paper A's description of paper B's bound vs B's own theorem) are **recorded as conflicts**, not silently resolved. Known errata / flawed proofs can be marked and propagate as warnings to inferred results.

## D6. Measurable extraction quality

A hand-annotated gold set exists before scaling up; extraction precision/recall on settings, bounds and assumptions is reported per release. No scale-up until accuracy clears an agreed bar.

## D7. Open, plain-text, diffable data

The knowledge base lives as plain files (JSON/YAML) in git, so changes are reviewable as diffs and contributions can be made by pull request. Derived artefacts (graph, tables, site) are rebuilt from it deterministically.

## D8. Gap and open-problem reports are first-class outputs

The system produces, per release: settings with non-tight bounds, settings with no lower bound, unstudied neighbours of well-studied settings, and redundant results (implied by prior, more general results).

Gaps are coarsely labelled (e.g. "log-factor gap", "polynomial gap", "no lower bound"). A detected gap is only a **candidate**: before it is reported as open, a targeted retrieval search (Semantic Scholar / OpenAlex / TheoremSearch) checks for a resolving paper outside the corpus. Most apparent gaps will be coverage holes, as the Erdős-problems episode showed. Negative searches are logged.

## D11. Parameterised settings and classification theorems

Nodes can be parameterised families (e.g. "feedback graph with independence number α", "Bellman–Eluder dimension ≤ d", a partial-monitoring game). Some results are **classification theorems** that settle a whole family at once (partial monitoring: trivial / easy / hard / hopeless). Gap detection must then ask "is this node covered by a characterisation?", not only compare two bounds.

## D12. Governance for LLM-extracted content

Every fact is tagged with how it was produced (model, prompt version, human edits). Nothing is published as verified without human review. This matches π-Base's policy that unedited AI output is rejected. Data is CC-BY in an open git repo with no single maintainer or corporate host, because hosting failure is how most precedents died.

## D9. Queryable and browsable

A static website (per-setting pages with bound tables, the Hasse diagram, gap lists) and a programmatic query interface. Later: natural-language queries answered from the graph with citations.

## D10. Incremental and cheap to maintain

New papers can be added without reprocessing the corpus; a periodic job can pick up new arXiv papers. The pipeline is reproducible from a corpus manifest.
