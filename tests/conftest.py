"""Shared fixtures: settings and results built by hand on the real ontology (v0.5).

Fixtures are chosen so that a known past bug, or a plausible one, changes the answer
(see the docstring of each test)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import resolve  # noqa: E402
import schema  # noqa: E402

ONT = schema.load_ontology()
CANONICAL = set(schema.load_variables()["variables"])

BASE = dict(objective="cumulative_regret", feedback="bandit", environment="stochastic_iid", action_space="finite_K",
            function_class=[], domain="not_applicable", context="none", noise="bounded_01", learner_knows=[],
            instance_assumptions=[], extras=[])


def key(**kw) -> dict:
    """Canonical key of an extracted setting: the stochastic K-armed bandit with [0, 1] rewards,
    with `kw` overriding dimensions or node parameters (e.g. action_set={"shape": "unit_ball"})."""
    return resolve.setting_key({**BASE, **kw}, ONT)


LINEAR_BALL = dict(action_space="linear_infinite", noise="subgaussian",
                   action_set={"shape": "unit_ball", "time_varying": "fixed"})
LINEAR_FINITE = dict(action_space="linear_finite", noise="subgaussian",
                     action_set={"shape": "finite", "time_varying": "fixed"})


def result(rid: str, sid: str, side: str, expr: str, quantity: str = "pseudo_regret",
           dependence: str = "worst_case", notation: str = "Omega", **kw) -> dict:
    r = {"id": rid, "paper": rid.split(":")[0], "setting_id": sid, "side": side, "quantity": quantity,
         "dependence": dependence, "comparator": "best_fixed_action", "algorithm_class": None, "conditions": [],
         "bound": {"expression": expr, "notation": notation if side == "lower" or notation != "Omega" else "O",
                   "regime": None}}
    r.update(kw)
    return r


@pytest.fixture
def ont():
    return ONT
