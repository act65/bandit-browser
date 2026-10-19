# Pipeline

```
corpus/manifest.yaml ──fetch.py──▶ corpus/src/<arxiv_id>/      (LaTeX source; gitignored)
                     ──preprocess.py──▶ corpus/pre/<arxiv_id>.tex  (flattened; gitignored)
                     ──extract.py──▶ data/extractions/<paper_id>.json
                     ──validate.py──▶ data/validation-report.md
site/build.py ──▶ _site/   (static site; deployed by .github/workflows/pages.yml)
```

```bash
uv run python pipeline/fetch.py            # ~3 s per paper (arXiv rate limit)
uv run python pipeline/preprocess.py
CLAUDE_CLI_USAGE_LOG=data/extract.usage.jsonl \
  uv run python pipeline/extract.py --workers 3
uv run python pipeline/validate.py
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

## Sources are not redistributed

The default arXiv licence does not permit redistribution, so `corpus/src` and `corpus/pre` are gitignored. Extractions keep only short verbatim quotes, as provenance.
