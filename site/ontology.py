"""Ontology helpers for the site: dimensions and readable names.

The specialisation order itself lives in pipeline/order.py (single source of truth).

Reads the highest-version ``ontology/bandits-*.yaml`` so new dimensions (e.g. v0.3's
``action_set``) and new order pairs show up without code changes.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

FALLBACK_DIMS = ["objective", "feedback", "environment", "action_space", "function_class", "domain",
                 "context", "noise"]
NOT_KEY = {"learner_knows", "extras"}  # extras is appended separately; learner_knows is per result

# Short human labels for values. Anything missing falls back to "snake_case" -> "snake case".
VALUE_LABEL = {
    "objective": {
        "cumulative_regret": "regret", "simple_regret": "simple regret",
        "bai_fixed_confidence": "best-arm id (fixed confidence)", "bai_fixed_budget": "best-arm id (fixed budget)",
        "pac_epsilon_best": "PAC ε-best arm", "top_m_identification": "top-m identification",
        "other_pure_exploration": "pure exploration", "epsilon_optimal_point": "ε-optimal point",
    },
    "feedback": {
        "full_information": "full information", "two_point": "two-point feedback", "semi_bandit": "semi-bandit",
        "bandit": "bandit feedback", "graph_feedback": "graph feedback", "partial_monitoring": "partial monitoring",
        "dueling": "dueling",
    },
    "environment": {
        "stochastic_iid": "stochastic", "stochastic_corrupted": "corrupted stochastic",
        "adversarial_oblivious": "adversarial (oblivious)", "adversarial_adaptive": "adversarial (adaptive)",
        "adversarial_unspecified": "adversarial", "nonstationary_switching": "switching",
        "nonstationary_drifting": "drifting", "markovian": "Markovian",
    },
    "action_space": {
        "finite_K": "K-armed", "linear_finite": "linear (finite actions)", "linear_infinite": "linear (infinite actions)",
        "generalized_linear": "generalised linear", "combinatorial": "combinatorial", "convex_body": "convex body",
        "lipschitz_metric": "Lipschitz / metric", "kernel_rkhs": "kernel / GP", "continuum_other": "continuum",
    },
    "function_class": {
        "strongly_convex": "strongly convex", "highly_smooth": "highly smooth", "submodular_lovasz": "submodular",
        "quasi_convex": "quasi-convex", "polyak_lojasiewicz": "PL", "lipschitz": "Lipschitz",
    },
    "context": {"stochastic_contexts": "stochastic contexts", "adversarial_contexts": "adversarial contexts"},
    "noise": {
        "bounded_01": "bounded rewards", "bounded_pm1": "rewards in [-1, 1]", "bernoulli": "Bernoulli", "subgaussian": "sub-Gaussian",
        "gaussian_known_variance": "Gaussian", "conditionally_subgaussian": "cond. sub-Gaussian noise",
        "noise_free": "noise-free", "exponential_family": "exponential family", "heavy_tailed": "heavy-tailed",
    },
}
# Values that are the "unremarkable" default for a dimension and so are left out of names.
DEFAULTS = {"objective": {"cumulative_regret"}, "feedback": {"bandit"},
            "action_set.time_varying": {"fixed"}, "action_set.shape": {"unspecified"},
            "action_set.access": {"explicit"}}
EMPTY = {"", "none", "null", "not_applicable", "no-extras"}

DIM_LABEL = {"action_space": "action space", "function_class": "function class", "learner_knows": "learner knows"}

QUANTITY_LABEL = {
    "pseudo_regret": "Pseudo-regret", "expected_regret": "Expected regret",
    "high_probability_regret": "High-probability regret", "bayesian_regret": "Bayesian regret",
    "minimax_bayesian_regret": "Minimax Bayesian regret", "simple_regret": "Simple regret",
    "sample_complexity": "Sample complexity", "error_probability": "Error probability",
    "dynamic_regret": "Dynamic regret", "switching_regret": "Switching regret",
    "regret_unspecified": "Regret (unspecified)", "other": "Other quantity",
}


def dim_label(dim: str) -> str:
    return DIM_LABEL.get(dim, dim.replace("_", " "))


def value_label(dim: str, v) -> str:
    if isinstance(v, (list, tuple)):
        return ", ".join(value_label(dim, x) for x in v) or "none"
    v = str(v)
    if dim in ("function_class", "extras") and "+" in v:
        return ", ".join(value_label(dim, x) for x in v.split("+"))
    return VALUE_LABEL.get(dim, {}).get(v) or v.replace("_", " ")


def is_default(dim: str, v) -> bool:
    if isinstance(v, (list, tuple)):
        return not v
    v = "" if v is None else str(v)
    return v in EMPTY or v in DEFAULTS.get(dim, set())


def _version_key(p: Path):
    m = re.search(r"-(\d+(?:\.\d+)*)\.ya?ml$", p.name)
    return tuple(int(x) for x in m.group(1).split(".")) if m else ()


class Ontology:
    def __init__(self, *dirs: Path):
        files = []
        for d in dirs:
            if d.is_dir():
                files = sorted(d.glob("bandits-*.yaml"), key=_version_key)
                if files:
                    break
        self.path = files[-1] if files else None
        data = {}
        if self.path:
            try:
                data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                data = {}
        self.data: dict = data if isinstance(data, dict) else {}
        self.version = str(data.get("version", "?"))
        self.dimensions: dict = data.get("dimensions") or {}
        self.dims = [d for d in self.dimensions if d not in NOT_KEY] or list(FALLBACK_DIMS)
        self.quantities = list((data.get("vocabularies") or {}).get("quantity") or QUANTITY_LABEL)

    def describe(self, dim: str, value) -> str:
        spec = self.dimensions.get(dim) or {}
        vals = spec.get("values") if isinstance(spec, dict) else None
        return str((vals or {}).get(value) or "") if isinstance(vals, dict) else ""
