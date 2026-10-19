# Motivation

## The problem

Theoretical ML (and theoretical CS / maths more broadly) produces results of a very regular shape:

> *In setting S (defined by assumptions A₁, …, Aₙ), algorithm X achieves quantity Q ≤ f(parameters); no algorithm can do better than g(parameters).*

Yet this knowledge is stored as prose and LaTeX scattered over thousands of PDFs. The "state of the art" for a given setting lives in:

- the heads of a few experts,
- hand-curated comparison tables in individual papers ("Table 1: comparison with prior work"), each covering a narrow slice and frozen at publication time,
- surveys and books, which are excellent but expensive to write and go stale.

Consequences:

- **It is hard to know what is known.** Answering "what is the best known regret for delayed linear bandits with adversarial corruption?" means a multi-day literature search, and the answer may be implied by a more general result that never mentions your setting.
- **Gaps are invisible.** Settings with mismatched upper/lower bounds, or with no lower bound at all, are not listed anywhere systematically.
- **Effort is duplicated.** Papers re-prove bounds that already follow from a result in a more general setting, or miss that a neighbouring setting already solved the analogous problem.
- **Newcomers face a steep wall.** The map of the field is implicit.

## The idea

Build a machine-readable **atlas of theoretical results**:

1. **Nodes are settings**, each defined by a vector of assumptions from a fixed ontology.
2. **Directed edges are specialisations** ("S is a special case of S′"), so the settings form a partial order. Its covering relation — settings that differ by exactly one assumption — is the navigable "neighbour" graph.
3. **Each node collects every bound** (upper and lower) proved for that setting, as symbolic expressions with regret type, regime and extra assumptions, with provenance back to the theorem in the source paper.
4. **Results propagate along edges**: an upper bound for a general setting holds for all its special cases; a lower bound for a special case holds for all its generalisations.
5. Papers are parsed at scale (~10³ papers) by LLMs reading arXiv LaTeX source, into a fixed schema, with human verification.

## What it enables (why it is worth the effort)

1. **Gap finding.** Settings where best upper and lower bounds don't match, or where no lower bound exists — an automatically generated, continuously updated open-problems list.
2. **Empty neighbours.** A well-studied setting whose one-assumption-away neighbour is unstudied is a candidate research question.
3. **Technique transfer.** "This technique closed the gap in setting X; the neighbouring setting Y still has a gap" — a concrete suggestion of what to try.
4. **Redundancy detection.** Flag papers whose bounds are already implied (via inheritance) by a more general prior result.

Secondary benefits: a living, queryable survey; a teaching resource; a structured dataset for evaluating AI systems on theory literature; a substrate for answering natural-language questions with citations.

## Why now

- LLMs can read LaTeX theorem statements reliably enough to make extraction at the scale of thousands of papers cheap (order of tens of millions of tokens). The bottleneck has moved from reading to *schema design and verification*.
- arXiv provides LaTeX source, so theorem statements are available as exact maths rather than OCR'd PDF.
- Curated-database precedents (see [related-work.md](related-work.md)) show that the "hierarchy + inference" model works and is valued by communities — but they were built by hand and cover other fields.

## Why bandits as the pilot

The idea is domain-general (online learning, RL theory, stochastic optimisation, statistical learning, complexity theory …). Bandits are a good first test because:

- **Results are crisp.** Regret bounds are explicit functions of a small set of parameters (T, K, d, Δ, …).
- **The setting space is rich but structured.** Feedback × environment × action space × context × extras gives a natural product order.
- **The literature is large but bounded** — a few thousand papers, much of it on arXiv with source.
- **We know the history.** Experts can check whether the system rediscovers known gaps and their closures — a strong validation signal.
- **Known subtleties** (pseudo- vs expected regret, minimax vs instance-dependent, anytime vs known horizon) stress-test the bound representation early.

If the pilot works, the engine (schema core, inference, gap detection, UI) is reused and only the domain ontology changes.
