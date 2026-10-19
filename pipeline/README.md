# Pipeline

```
corpus/manifest.yaml ──fetch.py──▶ corpus/src/<arxiv_id>/      (LaTeX source; gitignored)
                     ──preprocess.py──▶ corpus/pre/<arxiv_id>.tex  (flattened; gitignored)
                     ──extract.py──▶ data/extractions/<paper_id>.json
                     ──validate.py──▶ data/validation-report.md
                     ──resolve.py──▶ data/canonical/  (stable ids: settings S-<hash>, algorithms,
                                                        citations, normalised bounds; report.md)
site/build.py ──▶ _site/   (static site; deployed by .github/workflows/pages.yml)
```

```bash
uv run python pipeline/fetch.py            # ~3 s per paper (arXiv rate limit)
uv run python pipeline/preprocess.py
CLAUDE_CLI_USAGE_LOG=data/extract.usage.jsonl \
  uv run python pipeline/extract.py --workers 3
uv run python pipeline/validate.py
uv run python pipeline/resolve.py           # canonicalisation (D13)
uv run python site/build.py && python3 -m http.server -d _site 8000
```

All commands take `--only ID ...`. `extract.py` skips papers that already have an extraction unless you pass `--force`.

## Extractor backend

`claude_cli.py` calls `claude -p` with:
- `--system-prompt`: the PROMPT block of [schema.md](../schema.md), with the ontology rendered from `ontology/*.yaml`;
- `--json-schema`: generated from the same ontology by `schema.py`, so the model can only emit vocabulary values;
- all tools disabled, because paper text is untrusted.

This uses the Claude subscription rather than API credits. It is adapted from `act65/pol-score-cards`. The test run on OFUL used about 44k input and 6k output tokens, roughly $0.48 at API prices.

Every extraction records `_run` (models, prompt hash, ontology version, token usage). `status` starts as `extracted` and is raised to `human-verified` by review (desiderata D5).

## Canonical notation and ids (D13)

| Registry | File | Used by |
|---|---|---|
| Ontology (dimensions, node parameters, vocabularies) | `ontology/bandits-0.3.yaml` | prompt + JSON Schema enums |
| Variables (definitions, aliases, conversion rules) | `ontology/variables.yaml` | prompt variable table, validator, normaliser |
| Algorithms (ids, aliases, family, introducing paper) | `data/algorithms.yaml` | prompt; `registry_id` is constrained to these ids |
| Papers (ids, arXiv ids, `alt_titles`) | `corpus/manifest.yaml` | citation resolution |

- `seed_algorithms.py` seeded the algorithm registry by LLM clustering of the v0.2 algorithm mentions (148 mentions → 132 algorithms). It is a proposal to review by hand.
- `resolve.py` never edits extractions. It derives `data/canonical/` and a report: declared symbols recurring in 2+ papers are registry proposals; unregistered algorithms get provisional `new:<paper>:<name>` ids; unresolved citations become ranked corpus candidates (`candidates.yaml`), the input to the next snowball round.
- Setting ids hash the full canonical key (all dimensions, `action_set` minus `access`, `parameters`; `learner_knows` minus T, K, d), so they are stable across runs and re-extractions.

## Sources are not redistributed

The default arXiv licence does not permit redistribution, so `corpus/src` and `corpus/pre` are gitignored. Extractions keep only short verbatim quotes, as provenance.
