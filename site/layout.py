"""Graph layouts computed at build time, so the browser never runs a layout on the full graph.

hierarchy(nodes, edges)  layered drawing of a DAG (arrows special -> general, drawn bottom-up):
                         longest-path layers, barycentre ordering sweeps to reduce crossings,
                         nodes without any directed edge in a grid beside the hierarchy
force(nodes, edges)      Fruchterman-Reingold (networkx spring_layout), seeded (unused by the site)
similarity(keys)         t-SNE of the settings' ontology features (each value plus its generalisations),
                         seeded; similar settings sit together whether or not an edge links them

Both return {node_id: (x, y)} in screen-like coordinates (y grows downwards), scaled so that
neighbouring nodes are roughly `gap` pixels apart; Cytoscape's `preset` layout uses them as is.
"""

from __future__ import annotations

import collections
import math
import re

import networkx as nx


def hierarchy(nodes: list[str], edges: list[tuple[str, str]], gap: float = 60.0, rank_gap: float = 90.0,
              weight: dict[str, float] | None = None, sweeps: int = 8) -> dict[str, tuple[float, float]]:
    """Layered layout. `edges` are (special, general); general settings sit above special ones."""
    nodes = list(dict.fromkeys(nodes))
    succ, pred = collections.defaultdict(set), collections.defaultdict(set)
    for a, b in edges:
        if a != b:
            succ[a].add(b)
            pred[b].add(a)
    linked = [n for n in nodes if succ[n] or pred[n]]
    loose = [n for n in nodes if not (succ[n] or pred[n])]

    # layer = length of the longest path down to a minimal (most special) node; cycles (should
    # not happen in a partial order, but extraction noise can create equivalent settings) are
    # broken by visiting order
    layer, state = {}, {}

    def depth(n):
        if n in layer:
            return layer[n]
        state[n] = "open"
        d = 0
        for p in pred[n]:
            if state.get(p) != "open":
                d = max(d, depth(p) + 1)
        state[n] = "done"
        layer[n] = d
        return d

    for n in linked:
        depth(n)
    rows = collections.defaultdict(list)
    for n in linked:
        rows[layer[n]].append(n)
    order = {n: i for r in rows.values() for i, n in enumerate(sorted(r))}

    # barycentre sweeps: up (by predecessors) then down (by successors)
    def sweep(rng, nbrs):
        for r in rng:
            row = rows[r]
            bc = {n: (sum(order[m] for m in nbrs[n]) / len(nbrs[n])) if nbrs[n] else order[n] for n in row}
            row.sort(key=lambda n: (bc[n], order[n]))
            for i, n in enumerate(row):
                order[n] = i
    top = max(rows, default=0)
    for _ in range(sweeps):
        sweep(range(1, top + 1), pred)
        sweep(range(top - 1, -1, -1), succ)

    # wide layers wrap onto several sub-rows, so the drawing stays roughly square (a single row of
    # 300 settings made the hierarchy a flat line once fitted to the screen)
    pos = {}
    width = max(8, math.ceil(1.6 * math.sqrt(len(linked) or 1)))
    y = 0.0
    for r in range(top, -1, -1):  # most general layer first (top of the drawing)
        row = rows.get(r, [])
        for start in range(0, len(row), width):
            chunk = row[start:start + width]
            off = (width - len(chunk)) * gap / 2  # centre each sub-row
            for i, n in enumerate(chunk):
                pos[n] = (off + i * gap, y)
            y += gap * 1.1
        y += rank_gap - gap * 1.1
    # loose nodes: a grid to the right, biggest first
    x0 = width * gap + 3 * gap
    cols = max(2, math.ceil(math.sqrt(len(loose) * 0.6)))
    w = weight or {}
    for i, n in enumerate(sorted(loose, key=lambda n: -w.get(n, 0))):
        pos[n] = (x0 + (i % cols) * gap * 1.4, (i // cols) * gap * 1.4)
    return pos


def force(nodes: list[str], edges: list[tuple[str, str]], gap: float = 60.0, seed: int = 0,
          iterations: int = 200) -> dict[str, tuple[float, float]]:
    """Spring layout of the whole graph (components packed by networkx), scaled to ~`gap` spacing."""
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from((a, b) for a, b in edges if a != b)
    if not len(g):
        return {}
    raw = nx.spring_layout(g, seed=seed, iterations=iterations, k=1.6 / math.sqrt(len(g)))
    scale = gap * math.sqrt(len(g)) * 0.9
    return {n: (float(x) * scale, float(-y) * scale) for n, (x, y) in raw.items()}


# ---------------------------------------------------------------- similarity (t-SNE) layout

# Main problem axes weigh more than the detail fields of node parameters (action_set.*, corruption.*, ...)
MAIN_DIMS = {"objective": 1.6, "feedback": 1.6, "environment": 2.0, "action_space": 2.0, "context": 1.0,
             "noise": 0.7, "function_class": 1.0, "domain": 0.7}
SKIP_VALUES = {"", "none", "null", "not_applicable", "unspecified"}


def features(keys: dict[str, dict], orders: dict[str, set] | None = None) -> tuple[list[str], "np.ndarray"]:
    """One row per setting. A value is encoded together with every value above it in the
    specialisation order ("up-set"), so a setting shares features with its generalisations;
    each dimension's weight is spread over its up-set, so long chains don't dominate.
    Free-text fields (learner_knows, parameters, extras, instance_assumptions) add small token weights."""
    import numpy as np
    orders = orders or {}
    ids = list(keys)
    cols: dict[str, int] = {}
    rows = []
    for i in ids:
        feats: dict[str, float] = {}
        for dim, v in keys[i].items():
            if not isinstance(v, str) or v in SKIP_VALUES:
                continue
            if dim in ("learner_knows", "parameters", "extras", "instance_assumptions"):
                toks = [t for t in re.split(r"[;,\s]+", v) if t]
                for t in toks:
                    feats[f"{dim}~{t}"] = feats.get(f"{dim}~{t}", 0) + 0.35 / math.sqrt(len(toks))
                continue
            w = MAIN_DIMS.get(dim, 0.6)
            up = [v] + sorted(b for a, b in orders.get(dim, ()) if a == v)
            for u in up:
                feats[f"{dim}={u}"] = w / math.sqrt(len(up))
        rows.append(feats)
        for k in feats:
            cols.setdefault(k, len(cols))
    x = np.zeros((len(ids), max(1, len(cols))))
    for r, feats in enumerate(rows):
        for k, val in feats.items():
            x[r, cols[k]] = val
    return ids, x


def similarity(keys: dict[str, dict], orders: dict[str, set] | None = None, gap: float = 40.0,
               seed: int = 0) -> dict[str, tuple[float, float]]:
    """t-SNE of the setting features (see `features`), seeded so the drawing is stable between builds.
    Settings with identical features are spread a little so they don't sit on one point."""
    import numpy as np
    from sklearn.manifold import TSNE
    ids, x = features(keys, orders)
    if len(ids) < 4:
        return {n: (i * gap, 0.0) for i, n in enumerate(ids)}
    rng = np.random.default_rng(seed)
    x = x + rng.normal(0, 1e-3, x.shape)
    emb = TSNE(n_components=2, perplexity=min(30, (len(ids) - 1) / 3), init="pca", random_state=seed,
               metric="euclidean").fit_transform(x)
    emb -= emb.mean(0)
    # same overall extent as a grid with `gap` spacing would have, then push apart nodes closer than
    # min_dist (near-identical settings otherwise sit on top of each other)
    emb *= gap * math.sqrt(len(ids)) * 0.8 / max(float(np.ptp(emb, 0).max()), 1e-9)
    return dict(zip(ids, separate(emb, min_dist=gap * 0.4, iterations=120, seed=seed)))


def separate(pts, min_dist: float, iterations: int = 60, seed: int = 0) -> list[tuple[float, float]]:
    """Push apart points closer than min_dist (a few rounds of pairwise nudges)."""
    import numpy as np
    from scipy.spatial import cKDTree
    p = np.array(pts, dtype=float)
    rng = np.random.default_rng(seed)
    for _ in range(iterations):
        pairs = cKDTree(p).query_pairs(min_dist, output_type="ndarray")
        if not len(pairs):
            break
        d = p[pairs[:, 1]] - p[pairs[:, 0]]
        dist = np.linalg.norm(d, axis=1)
        zero = dist < 1e-9
        d[zero] = rng.normal(size=(int(zero.sum()), 2))
        dist[zero] = np.linalg.norm(d[zero], axis=1)
        push = (d / dist[:, None]) * ((min_dist - np.minimum(dist, min_dist)) / 2)[:, None] * 0.5
        np.add.at(p, pairs[:, 0], -push)
        np.add.at(p, pairs[:, 1], push)
    return [(float(a), float(b)) for a, b in p]
