# bandit-browser

A machine-readable atlas of theoretical results, piloted on bandit problems.

Theory papers state results of a regular shape: *in setting S, algorithm X achieves bound f; no algorithm beats g*. This project parses such results from the literature with LLMs and organises them into a graph:

- **Nodes are settings**, defined by assumption vectors from a fixed ontology.
- **Directed edges are specialisations** ("S is a special case of S′"), with parameter maps.
- **Each node holds a table of bounds** (upper and lower), compared per regime as a partial order, with provenance back to the exact theorem.
- **Results propagate along edges**: upper bounds flow to special cases and lower bounds to generalisations. This exposes gaps, unstudied neighbouring settings and redundant results.

Bandits are the test domain; the goal is a domain-agnostic engine for ML, CS and maths theory.

**Status:** Phase 4 (scaling). 1,057 papers (a 59-paper pilot and two breadth batches of about 500) extracted by an LLM with ontology v0.6: about 4,700 results across about 2,060 canonical settings. Results are checked by automated audits and a textbook gold set ([`notes/validation.md`](notes/validation.md)), and a few by their authors, but are not human-verified in general. Roughly half the extracted bounds can be compared across papers; why the rest can't is in [`notes/comparability.md`](notes/comparability.md). Browse at <https://act65.github.io/bandit-browser/>; contributions and corrections: [CONTRIBUTING.md](CONTRIBUTING.md).

## Documents

| File | Contents |
|---|---|
| [motivation.md](motivation.md) | Why this is worth building and why bandits are the pilot |
| [desiderata.md](desiderata.md) | Requirements, including the three core design points |
| [related-work.md](related-work.md) | Existing databases, zoos and extraction systems, and how this differs |
| [schema.md](schema.md) | Draft LLM extraction prompt, output schema and bandits ontology v0.1 |
| [plan.md](plan.md) | Phased plan with go / no-go checks |
| [pipeline/README.md](pipeline/README.md) | Fetch → preprocess → extract → validate |
| [site/README.md](site/README.md) | Static site build and GitHub Pages deploy |
| [ontology/](ontology/) | Machine-readable ontology versions and review notes |
| [notes/](notes/) | Validation, comparability, the bandit convex optimisation ground truth and the pilot facts |
| [data/](data/) | Extractions, ground truth, validation report |

## License

Code: [MIT](LICENSE). Data and documentation: [CC BY 4.0](LICENSE-DATA).
