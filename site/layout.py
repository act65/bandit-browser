"""Graph layouts computed at build time, so the browser never runs a layout on the full graph.

hierarchy(nodes, edges)  layered drawing of a DAG (arrows special -> general, drawn bottom-up):
                         longest-path layers, barycentre ordering sweeps to reduce crossings,
                         nodes without any directed edge in a grid beside the hierarchy
force(nodes, edges)      Fruchterman-Reingold (networkx spring_layout), seeded, so it is stable

Both return {node_id: (x, y)} in screen-like coordinates (y grows downwards), scaled so that
neighbouring nodes are roughly `gap` pixels apart; Cytoscape's `preset` layout uses them as is.
"""

from __future__ import annotations

import collections
import math

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
