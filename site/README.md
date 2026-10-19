# Site

A static browser over the data. `build.py` reads the data files and writes plain HTML to `_site/` (gitignored). Display only: no bound comparison or inference happens here; inherited bounds are read from `data/canonical/inferred.json` (written by `pipeline/infer.py`) and shown separately from extracted ones.

## Build locally

```bash
uv run python site/build.py              # real data -> _site/
uv run python site/build.py --fixtures   # site/fixtures/ test data
python3 -m http.server -d _site 8000     # then open http://localhost:8000
```

Inputs (any may be missing; the build still succeeds):

- `corpus/manifest.yaml`: paper list
- `data/canonical/{settings,results,algorithms}.json`: canonical layer from `pipeline/resolve.py`. Preferred when present: setting pages are `settings/<S-id>.html`, results use `algorithm_id` names and `bound.expression_normalised`. Settings with `in_scope: false` are skipped.
- `data/extractions/<paper_id>.json`: raw extractions (format in `schema.md`). Used for paper pages, and for grouping settings when there is no canonical layer (e.g. `--fixtures`).
- `data/algorithms.yaml`: algorithm registry (raw mode)
- `data/ground_truth/{bco,pilot-facts}.yaml`
- `ontology/bandits-<highest version>.yaml`: dimensions and their `order` pairs; `ontology/variables.yaml`: LaTeX for symbols

## Layout

- `build.py`: pages and the data model (stdlib + PyYAML)
- `ontology.py`: dimension list, readable value labels and setting names
- `pipeline/order.py` (imported via `sys.path`): the specialisation order `Order.leq`, the single source of truth for directed edges
- `bounds.py`: canonical SymPy bound string -> LaTeX (`sympy.latex` with `sum_subopt`/`sum_arms`, symbol names from `variables.yaml`, notation wrappers O/Õ/Ω/Θ, lim inf/lim sup as ratios to log T). If parsing fails the paper's `expression_latex` is shown instead, muted. The paper's LaTeX is always under a result's *details*.
- `static/style.css`, `static/site.js`: styling (light and dark), KaTeX rendering (with page-level `window.BB_MACROS`, used for the book's macros on the ground-truth page), filter boxes, settings grouping, and compact long bounds (a formula wider than its column is clipped with a fade and a "show full" toggle; re-measured after fonts load, on resize and when a `<details>` opens)
- `static/graph.js`: the settings graph (`graph.html`)
- `fixtures/`: tiny fake dataset (titles marked `[FIXTURE]`), used only with `--fixtures`

External scripts, all pinned: KaTeX 0.16.11 (jsdelivr), Cytoscape.js 3.30.2 and dagre 0.8.5 (cdnjs), cytoscape-dagre 2.5.0 (jsdelivr).

## Ground-truth page

`ground-truth.html` renders `data/ground_truth/bco.yaml`: settings as cards with assumption-vector chips, lower (Table 2.1) and upper (Table 2.2) bounds as result tables (bound from `bound.expression` via `bounds.py` with the book's horizon `n` written as `T`, falling back to `expression_latex`; algorithm, original citation, compute, book theorem, source quote), transfer rules as a list (from → to, kind, side, quotes under *details*) and open problems as cards with known lower/upper bounds.

## Neighbours and the graph

Directed edges come from `pipeline/order.py`: S → S′ whenever `Order.leq(S, S′)` holds (product order over all dimensions, including subset `order_rule`s, action-space `reduction`s and fixed `parameters`), so upper bounds flow against the arrow, lower bounds along it. Settings that differ in exactly one dimension with no order are undirected "other neighbours". Each setting page has collapsed "Inherited upper/lower bounds" sections built from `inferred.json` (deduplicated, sorted by quantity, dependence, then hops along covering edges), each row showing its source setting, changed dimensions, substitutions and caveats; rows whose caveats say "holds for <param> = <value> only" (a bound proved for a pinned value such as K = 2) get a "pinned K = 2" badge and go into a collapsed "Weak transfers" sub-list at the end of the section; they are skipped when `data/canonical` is absent (fixtures). The graph draws the transitive reduction of the directed edges with a dagre layout (or a force layout), colours nodes by action space or environment, and sizes them by number of results. `graph.html?focus=<setting id>` highlights one setting; each setting page links there and lists its more general, more special and other neighbours.

All links are relative, so the site works under `https://act65.github.io/bandit-browser/`.

## Deploy (GitHub Pages)

`.github/workflows/pages.yml` builds and deploys on every push to `main` (or a manual run from the Actions tab). One-time setup: in the GitHub repo go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
