"""The specialisation order on canonical settings (desiderata D1).

S ⊑ S' ("S is a special case of S'") iff any algorithm for S' runs on S with at most
the same guarantee (after a parameter map). It is the product order over the
ontology's dimensions:
  - scalar dimensions: the reflexive-transitive closure of the ontology's `order`
    pairs, plus `reductions` (cross-value embeddings with parameter maps, e.g.
    K-armed -> linear with d = K);
  - multi-valued dimensions with an `order_rule` (function_class, learner_knows,
    instance_assumptions): more elements = special case (P ⊑ Q iff Q ⊆ P);
    multi-valued dimensions without one (extras) must be equal;
  - an `order_notes` entry may `require` node-field values in the special setting (graph
    feedback ⊑ bandit only for strongly observable graphs); unspecified gives a caveat;
  - node parameters (action_set, corruption, feedback_graph fields): per-field orders and
    value maps; computational-only fields are ignored; `not_applicable` on one side defers
    to the governing dimension; `unspecified` is compatible with a caveat;
  - `parameters`: fixing a parameter is a special case (P ⊑ Q iff Q ⊆ P as items).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

# Generic caveats for edges without a pair-specific note in the ontology.
CAVEATS = {
    "action_space": "reduction: check that the embedding preserves the regret notion and parameter ranges",
}


@dataclass
class Change:
    dim: str
    special: object          # value in the special-case setting
    general: object          # value in the general setting
    kind: str                # "order" | "reduction" | "subset" | "parameter"
    param_map: dict = field(default_factory=dict)  # general-setting symbol -> special-setting expr
    up_map: dict = field(default_factory=dict)     # instantiation for lower bounds moving to the general setting
    justification: list = field(default_factory=list)  # one entry per ontology edge on the path
    caveats: list = field(default_factory=list)
    valid_for_comparator: set | None = None    # None = all comparators
    requires: dict = field(default_factory=dict)  # node field -> values the special setting must have


def _closure(pairs) -> set:
    rel = set(pairs)
    while True:
        new = {(a, d) for a, b in rel for c, d in rel if b == c and a != d} - rel
        if not new:
            return rel
        rel |= new


class Order:
    def __init__(self, ontology: dict):
        self.dims = ontology["dimensions"]
        self.orders: dict[str, set] = {}
        self.reductions: dict[str, dict] = {}  # dim -> {(a, b): composed param map}
        self.implies: dict[tuple, dict] = {}   # (dim, from, to) -> values implied in the special setting
        for d, spec in self.dims.items():
            self.orders[d] = _closure(tuple(p) for p in spec.get("order") or [])
            direct = {(r["from"], r["to"]): dict(r.get("map") or {}) for r in spec.get("reductions") or []}
            for r in spec.get("reductions") or []:
                if r.get("implies"):
                    self.implies[(d, r["from"], r["to"])] = r["implies"]
            self.reductions[d] = self._compose(direct, self.orders[d])
        self.value_maps = {d: spec.get("value_maps") or {} for d, spec in self.dims.items()}
        self.value_maps_up = {d: spec.get("value_maps_up") or {} for d, spec in self.dims.items()}
        self.notes = {d: {tuple(n["pair"]): n for n in spec.get("order_notes") or []}
                      for d, spec in self.dims.items()}
        self.node_fields = {}  # node parameter -> fields that take part in the order
        for name, spec in (ontology.get("node_parameters") or {}).items():
            self.node_fields[name] = [f for f, fs in spec["fields"].items() if not fs.get("computational_only")]
            for f, fspec in spec["fields"].items():
                self.orders[f"{name}.{f}"] = _closure(tuple(p) for p in fspec.get("order") or [])
                self.value_maps[f"{name}.{f}"] = fspec.get("value_maps") or {}

    @staticmethod
    def _compose(direct: dict, order: set) -> dict:
        """Close reductions under composition with each other and with plain order steps."""
        steps = dict(direct)
        steps.update({pair: {} for pair in order})
        closed = dict(direct)
        changed = True
        while changed:
            changed = False
            for (a, b), m1 in list(closed.items()) + [(p, {}) for p in order]:
                for (c, d), m2 in steps.items():
                    if b == c and a != d and (a, d) not in closed and (a, d) not in order:
                        # m2 maps symbols of d's setting into c(=b)'s; m1 maps b's into a's
                        closed[(a, d)] = {**m1, **{k: m1.get(v, v) if isinstance(v, str) else v
                                                   for k, v in m2.items()}}
                        changed = True
        return closed

    def _path_notes(self, dim: str, a, b) -> list[dict]:
        """Ontology notes along a shortest chain of direct order pairs from a to b."""
        direct = self.notes.get(dim, {})
        frontier, prev = [a], {a: None}
        while frontier:
            nxt = []
            for x in frontier:
                for (u, v) in direct:
                    if u == x and v not in prev:
                        prev[v] = (u, v)
                        nxt.append(v)
            frontier = nxt
        if b not in prev:
            return []
        out, x = [], b
        while prev[x] is not None:
            out.append(direct[prev[x]])
            x = prev[x][0]
        return out[::-1]

    def _scalar(self, dim: str, a, b) -> Change | None:
        """Change if a ⊑ b in a scalar dimension (a in the special setting)."""
        if (a, b) in self.orders.get(dim, set()):
            notes = self._path_notes(dim, a, b)
            scopes = [set(n["valid_for_comparator"]) for n in notes if n.get("valid_for_comparator")]
            return Change(dim, a, b, "order",
                          justification=[n["justification"] for n in notes if n.get("justification")],
                          caveats=[n["caveat"] for n in notes if n.get("caveat")],
                          valid_for_comparator=set.intersection(*scopes) if scopes else None,
                          requires={k: v for n in notes for k, v in (n.get("requires") or {}).items()})
        red = self.reductions.get(dim, {})
        if (a, b) in red:
            return Change(dim, a, b, "reduction", red[(a, b)])
        return None

    def leq(self, ka: dict, kb: dict) -> list[Change] | None:
        """If ka ⊑ kb (strictly), the list of changed dimensions; otherwise None."""
        changes: list[Change] = []
        ka = self._with_implied(ka, kb)
        for dim, spec in self.dims.items():
            va, vb = ka.get(dim), kb.get(dim)
            if va == vb:
                continue
            if spec.get("multi"):
                sa, sb = set(va or []), set(vb or [])
                if spec.get("order_rule") and sb < sa:
                    changes.append(Change(dim, sorted(sa), sorted(sb), "subset"))
                    continue
                gen = set(spec.get("generalizing_values") or [])
                if gen and sa - gen == sb - gen and sa & gen < sb & gen:
                    changes.append(Change(dim, sorted(sa), sorted(sb), "subset"))
                    continue
                return None
            ch = self._scalar(dim, va, vb)
            if ch is None:
                return None
            ch.param_map = {**ch.param_map, **self.value_maps.get(dim, {}).get(va, {})}
            ch.up_map = dict(self.value_maps_up.get(dim, {}).get(vb, {}))
            changes.append(ch)
        for name, fields in self.node_fields.items():
            for f in fields:
                va = (ka.get(name) or {}).get(f, "not_applicable")
                vb = (kb.get(name) or {}).get(f, "not_applicable")
                if va == vb:
                    continue
                dim = f"{name}.{f}"
                if (va, vb) in self.orders.get(dim, set()):
                    changes.append(Change(dim, va, vb, "order", dict(self.value_maps.get(dim, {}).get(va, {}))))
                elif "not_applicable" in (va, vb):
                    # irrelevant on one side: the governing dimension (environment for corruption,
                    # feedback for feedback_graph, action_space for action_set) carries the order
                    continue
                elif "unspecified" in (va, vb):
                    # the paper did not say: compatible only if its unstated convention matches
                    changes.append(Change(dim, va, vb, "order",
                                          caveats=[f"{dim} unspecified on one side ({va} vs {vb})"]))
                else:
                    return None
        for ch in list(changes):
            for path, allowed in ch.requires.items():
                # e.g. graph feedback -> bandit only if the learner sees its own loss (strongly observable)
                name, f = path.split(".")
                v = (ka.get(name) or {}).get(f, "not_applicable")
                if v == "unspecified":
                    ch.caveats = ch.caveats + [f"{path} unspecified; the edge needs {' or '.join(allowed)}"]
                elif v != "not_applicable" and v not in allowed:
                    return None
        pa, pb = ka.get("parameters", {}), kb.get("parameters", {})
        if pa != pb:
            if not set(pb.items()) < set(pa.items()):
                return None
            fixed = {k: v for k, v in pa.items() if k not in pb}
            changes.append(Change("parameters", fixed, {}, "parameter", dict(fixed)))
        return changes or None

    def _with_implied(self, ka: dict, kb: dict) -> dict:
        """Add values a reduction implies in the special setting (e.g. K-armed embedded as
        basis vectors satisfies arms_span_Rd) before comparing the remaining dimensions."""
        for (dim, a, b), implied in self.implies.items():
            if ka.get(dim) == a and (a, kb.get(dim)) in self.reductions.get(dim, {}):
                ka = dict(ka)
                for d2, vals in implied.items():
                    ka[d2] = sorted(set(ka.get(d2) or []) | set(vals))
        return ka

    def comparable_pairs(self, keys: dict[str, dict]):
        """Yield (special_id, general_id, changes) for every strictly ordered pair."""
        for a, b in itertools.permutations(keys, 2):
            ch = self.leq(keys[a], keys[b])
            if ch:
                yield a, b, ch
