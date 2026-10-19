# bandit-browser

A machine-readable atlas of theoretical results, piloted on bandit problems.

Theory papers state results of a regular shape: *in setting S, algorithm X achieves bound f; no algorithm beats g*. This project parses such results from the literature with LLMs and organises them into a graph:

- **Nodes are settings**, defined by assumption vectors from a fixed ontology.
- **Directed edges are specialisations** ("S is a special case of S′"), with parameter maps.
- **Each node holds a table of bounds** (upper and lower), compared per regime as a partial order, with provenance back to the exact theorem.
- **Results propagate along edges**: upper bounds flow to special cases and lower bounds to generalisations. This exposes gaps, unstudied neighbouring settings and redundant results.

Bandits are the test domain; the goal is a domain-agnostic engine for ML, CS and maths theory.

**Status:** Phase 1 (pilot). 59-paper corpus; 53 papers extracted by an LLM (354 results across 60 canonical settings, not yet human-verified); ground truth from Lattimore's *Bandit Convex Optimisation*. Browse at <https://act65.github.io/bandit-browser/>.

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
| [data/](data/) | Extractions, ground truth, validation report |

## License

Code: [MIT](LICENSE). Data and documentation: [CC BY 4.0](LICENSE-DATA).
