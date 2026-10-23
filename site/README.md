# Site

A static browser over the data, backed by a SQLite database that is queried in the browser. `build.py` reads the data files and writes `_site/` (gitignored). Display only: no bound comparison or inference happens here. Inherited bounds come from `data/canonical/inferred.json` (`pipeline/infer.py`) and the analysis from `data/canonical/site_index.json` (`pipeline/site_index.py`).

## Architecture

The site stays static, so GitHub Pages can host it. Most content now lives in one database instead of thousands of HTML files.

- **`_site/data/atlas-<hash>.db.NNN` + `config.json`** (`export_db.py`): one SQLite database, split into 10 MB chunks because GitHub limits files to 100 MB. Chunks are named by a hash of the content, so a browser never mixes chunks from two builds; every page names the version it expects in `<meta name="bb-db">`. It contains:
  - tables `settings`, `papers`, `setting_papers`, `bounds` (own and inherited), `cells` (setting × regime status, rates, best bounds, triage), `triage`, `labels`;
  - FTS5 indexes `settings_fts` and `papers_fts`;
  - `docs`: the gzip-compressed HTML of every setting and paper page.
- **In the browser**: [sql.js-httpvfs](https://github.com/phiresky/sql.js-httpvfs), vendored in `static/vendor/` because a Web Worker must come from the page's own origin, runs SQLite in a worker. It reads the database with HTTP range requests, so a query downloads only the database pages it touches: opening a setting page costs about a dozen 4 KB reads, not the whole file. `static/db.js` wraps it as `bbQuery(sql, params)`.
- **Pages**:
  - `explore.html` (`static/explore.js`): the corpus as queries. Tabs Settings, Papers, Bounds and Gaps, each a query spec (FROM clause, facet columns, text search, sorts, row renderer). Facet counts are computed under all the other filters; results are paged 50 at a time; state lives in the URL hash (`explore.html#tab=gaps&status=poly_gap&q=linear`).
  - `setting.html?s=<id>` and `paper.html?p=<id>` (`static/doc.js`): shells that fetch the page's HTML from `docs`, inject it and fire `bb:doc`. Page scripts start through `window.bbReady`, which runs them on `DOMContentLoaded` on static pages and on `bb:doc` in shells.
  - Static: `index.html`, `graph.html` (layouts precomputed by `layout.py`), and the analysis pages `neighbours.html`, `transfer.html`, `redundant.html`.
- **Links**: pages are still generated with the old relative links (`../settings/<id>.html`). `rewrite_links()` maps them to the database-backed URLs, so the renderers did not change.

Sizes at 559 papers: the database is 33 MB (the site was 175 MB of static HTML before). A setting page transfers about 0.3 MB plus a few database pages. The WebAssembly SQLite (1.2 MB) is cached after the first page.

## Build and preview locally

```bash
uv run python site/build.py              # real data -> _site/
uv run python site/build.py --fixtures   # site/fixtures/ test data
uv run python site/serve.py --port 8000  # then open http://127.0.0.1:8000
```

Use `serve.py`, not `python -m http.server`: the database is read with HTTP range requests, which the standard library server does not support (GitHub Pages does).

Inputs (any may be missing; the build still succeeds):

- `corpus/manifest.yaml`: paper list
- `data/canonical/{settings,results,algorithms}.json`: canonical layer from `pipeline/resolve.py`. Settings with `in_scope: false` are skipped.
- `data/extractions/<paper_id>.json`: raw extractions (format in `schema.md`), used for paper pages and, with no canonical layer (`--fixtures`), for grouping settings
- `data/algorithms.yaml`: algorithm registry (raw mode)
- `data/reports/triage.yaml`: gap-triage verdicts
- `ontology/bandits-<highest version>.yaml` and `ontology/variables.yaml`: dimensions, orders, labels and LaTeX for symbols
- `data/canonical/site_index.json`: the analysis index (bound profiles and JS plot functions, tightness cells, technique-transfer suggestions, unstudied neighbours, redundancy). Without it the analysis pages say "no data" and setting pages have no Rates section.

Reference material (Lattimore's *Bandit Convex Optimisation*, the pilot facts) is written up in [`notes/`](../notes/), not on the site.

## Layout

- `build.py`: the data model and page renderers (setting and paper pages, home, graph, analysis pages, the Explore and shell pages), link rewriting, and the build
- `export_db.py`: the database
- `layout.py`: graph layouts computed at build time (layered hierarchy; networkx spring layout)
- `serve.py`: local preview server with HTTP Range support
- `ontology.py`: readable value labels, defaults and setting names
- `pipeline/order.py` (imported via `sys.path`): the specialisation order `Order.leq`, the single source of truth for directed edges
- `bounds.py`: canonical SymPy bound string → LaTeX. If parsing fails the paper's `expression_latex` is shown instead, muted; the paper's LaTeX is always under a result's *details*.
- `analysis.py`: the analysis layer over `site_index.json` (class `Analysis`: lookups, per-setting status, plot data) and the analysis pages (class `Pages`)
- `static/`:
  - `style.css`, `site.js`: styling (light and dark), KaTeX rendering, filter boxes, compact long bounds;
  - `graph.js`: the settings graph;
  - `plots.js`: rate plot and rate plane on setting pages (hand-rolled SVG);
  - `analysis.js`: facet filters on the analysis pages;
  - `db.js`, `doc.js`, `explore.js`: the database-backed pages;
  - `vendor/sqljs-httpvfs/`: sql.js-httpvfs 0.8.12 (Apache-2.0).
- `fixtures/`: tiny fake dataset (titles marked `[FIXTURE]`), used only with `--fixtures`

External scripts, all pinned: KaTeX 0.16.11 (jsdelivr), Cytoscape.js 3.30.2 and dagre 0.8.5 (cdnjs), cytoscape-dagre 2.5.0 (jsdelivr).

## Analysis

A *cell* is a setting × regime, where regime = quantity family × dependence (`regret|worst_case`, `hp_regret|instance_dependent`, …; bounds in `L_star`, `Q_T` or `Lambda_T` form the `data_dependent` regime, as in `pipeline/compare.py`). Status: tight / log gap / poly gap / no lower / no upper / conflict. Status colours are fixed tokens (`--st-*` in `style.css`) and always come with a text label.

- **Setting pages, "Rates"**: one line per cell (status, per-variable ↑upper/↓lower exponents, triage badge), then:
  - a *rate plot*: every bound in the regime evaluated client-side on the uniform-gap instance against a chosen variable, with sliders for the others; best bounds thick.
  - a *rate plane*: the bounds used in the rate comparison, on ordinal axes listing the rates that occur ("log T", "√T·log T", "T^2/3").
- **Gaps** (Explore tab): every cell, by default only conflicts and polynomial or log gaps, with per-variable rates, the best bound on each side and the triage verdict.
- `neighbours.html` (unstudied neighbours), `transfer.html` (technique-transfer suggestions), `redundant.html` (the redundancy report).

## Neighbours and the graph

Directed edges come from `pipeline/order.py`: S → S′ whenever `Order.leq(S, S′)` holds, so upper bounds flow against the arrow and lower bounds along it. Settings that differ in exactly one unordered dimension are "other neighbours". The graph has an overview of groups (environment × action space) and the full graph, with filters by action space and environment. Clicking a group shows its settings and keeps them highlighted until you click the background. Both layouts are precomputed, so switching layout is instant. `graph.html?focus=<slug>` shows one setting's neighbourhood.

All links are relative, so the site works under `https://act65.github.io/bandit-browser/`.

## Deploy (GitHub Pages)

`.github/workflows/pages.yml` builds and deploys on every push to `main` (or a manual run from the Actions tab). One-time setup: in the GitHub repo go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
