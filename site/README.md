# Site

A minimal static browser over the data. `build.py` reads the data files and writes plain HTML to `_site/` (gitignored). Display only: no bound comparison or inference.

## Build locally

```bash
uv run --with pyyaml python site/build.py              # real data -> _site/
uv run --with pyyaml python site/build.py --fixtures   # site/fixtures/ test data
python3 -m http.server -d _site 8000                   # then open http://localhost:8000
```

Inputs (any may be missing; the build still succeeds):

- `corpus/manifest.yaml`: paper list
- `data/extractions/<paper_id>.json`: one extraction per paper (format in `schema.md`)
- `data/ground_truth/bco.yaml`: hand-curated BCO reference, rendered generically

## Layout

- `build.py`: the whole generator (one file, stdlib + PyYAML)
- `static/style.css`, `static/site.js`: styling, KaTeX rendering of `expression_latex`, filter boxes. KaTeX 0.16.11 is loaded from jsdelivr.
- `fixtures/`: tiny fake dataset (titles marked `[FIXTURE]`), used only with `--fixtures`

Settings are grouped into canonical nodes keyed by objective, feedback, environment, action_space, context, noise and sorted extras. `learner_knows` is not part of the key; it is shown per result. Neighbours are canonical settings that differ in exactly one of those dimensions.

All links are relative, so the site works under `https://act65.github.io/bandit-browser/`.

## Deploy (GitHub Pages)

`.github/workflows/pages.yml` builds and deploys on every push to `main` (or a manual run from the Actions tab). One-time setup: in the GitHub repo go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
