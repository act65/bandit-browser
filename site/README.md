# Site

A static browser over the data. `build.py` reads the data files and writes plain HTML to `_site/` (gitignored). Display only: no bound comparison or inference.

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
- `ontology.py`: dimension list, readable value labels and setting names, transitive `order` closure
- `bounds.py`: canonical SymPy bound string -> LaTeX (`sympy.latex` with `sum_subopt`/`sum_arms`, symbol names from `variables.yaml`, notation wrappers O/Õ/Ω/Θ, lim inf/lim sup as ratios to log T). If parsing fails the paper's `expression_latex` is shown instead, muted. The paper's LaTeX is always under a result's *details*.
- `static/style.css`, `static/site.js`: styling (light and dark), KaTeX rendering, filter boxes, settings grouping
- `static/graph.js`: the settings graph (`graph.html`)
- `fixtures/`: tiny fake dataset (titles marked `[FIXTURE]`), used only with `--fixtures`

External scripts, all pinned: KaTeX 0.16.11 (jsdelivr), Cytoscape.js 3.30.2 and dagre 0.8.5 (cdnjs), cytoscape-dagre 2.5.0 (jsdelivr).

## Neighbours and the graph

Two settings are neighbours when their assumption vectors differ in exactly one dimension (`action_set` fields count as separate dimensions). If the ontology orders the two values (transitively, through `order`, a multi-valued dimension's subset `order_rule`, or an action-space `reduction`), the edge is directed from the special case to the general one: upper bounds flow against the arrow, lower bounds along it. Otherwise it is an undirected "other neighbour". The graph draws the transitive reduction of the directed edges with a dagre layout (or a force layout), colours nodes by action space or environment, and sizes them by number of results. `graph.html?focus=<setting id>` highlights one setting; each setting page links there and lists its more general, more special and other neighbours.

All links are relative, so the site works under `https://act65.github.io/bandit-browser/`.

## Deploy (GitHub Pages)

`.github/workflows/pages.yml` builds and deploys on every push to `main` (or a manual run from the Actions tab). One-time setup: in the GitHub repo go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
