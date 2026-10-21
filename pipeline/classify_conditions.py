"""Classify the free-text `conditions` of results (one cached LLM pass).

Classes:
  restatement      repeats the setting (rewards in [0,1], oblivious adversary, ...)
  normalisation    fixes a scale (sigma = 1, ||theta|| <= S, ||x|| <= 1)
  side_condition   constrains problem sizes / asymptotics (K >= 2, T*Delta^2 >= 1, n large)
  instance_restriction  restricts the instances beyond the setting (unique optimal arm,
                   optimal arms span R^d, bounded variance V, ...)
  algorithm_restriction restricts the learners the bound is about (limited memory, B batches,
                   bounded switching, algorithms with O(log T) stochastic regret, ...)
  model_change     the result is for a modified protocol the setting does not express (quantum
                   oracle access, starved feedback, externalities, noiseless rewards)
  unclear          cannot tell (e.g. "Assumption 1" without its content)
compare.py keeps instance_restriction / unclear upper bounds, algorithm_restriction lower
bounds and model_change bounds (either side) out of tightness verdicts. Writes data/condition-classes.yaml; reruns only classify
new strings unless --all is given.

Usage: uv run python pipeline/classify_conditions.py [--all] [--model sonnet]
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_cli  # noqa: E402
import schema  # noqa: E402

ROOT = schema.ROOT
OUT = ROOT / "data" / "condition-classes.yaml"
CLASSES = ["restatement", "normalisation", "side_condition", "instance_restriction", "algorithm_restriction", "model_change", "unclear"]
SYSTEM = ("You classify conditions attached to theoretical bandit results. For each condition string decide "
          "whether it restates the setting, fixes a normalisation/scale, is a side condition on problem sizes or "
          "asymptotics, genuinely restricts the class of problem instances (so the bound is NOT claimed for all "
          "instances of the setting), restricts the class of algorithms the bound is about (limited memory, a fixed "
          "number of batches, bounded switching, 'algorithms with O(log T) regret on stochastic instances'), or is "
          "unclear. Conditions describing the lower-bound construction ('holds for some instances', 'K = 2 in the "
          "construction') are side conditions. A condition that changes the interaction protocol itself (quantum "
          "oracle access, starved or delayed-only feedback, arrivals driven by past rewards, noiseless rewards in a "
          "noisy setting) is model_change. Be conservative: 'unique optimal arm', 'optimal arms span R^d', "
          "'variance bounded by V' are instance restrictions; 'sigma = 1', '||theta|| <= S' are normalisations; "
          "'T >= K', 'n large enough', 'T Delta^2 >= 1' are side conditions.")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["items"], "properties": {"items": {
    "type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["condition", "class"],
                               "properties": {"condition": {"type": "string"}, "class": {"enum": CLASSES}}}}}}


def main() -> None:
    reclassify = "--all" in sys.argv[1:]
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else None
    known = (yaml.safe_load(OUT.read_text()) or {}).get("classes", {}) if OUT.exists() and not reclassify else {}
    conds = sorted({c for r in json.loads((ROOT / "data" / "canonical" / "results.json").read_text())
                    for c in r.get("conditions") or []} - set(known))
    batches = [conds[i:i + 150] for i in range(0, len(conds), 150)]

    def classify(batch: list[str]) -> list[dict]:
        out, _ = claude_cli.call_structured(SYSTEM, json.dumps(batch, ensure_ascii=False), SCHEMA,
                                            model=model, label="classify_conditions", timeout=1200)
        return [it for it in out["items"] if it["condition"] in batch]

    with ThreadPoolExecutor(max_workers=6) as ex:
        for items in ex.map(classify, batches):
            for it in items:
                known[it["condition"]] = it["class"]
    OUT.write_text("# Condition classes (pipeline/classify_conditions.py). Hand edits welcome.\n"
                   + yaml.safe_dump({"classes": dict(sorted(known.items()))}, allow_unicode=True, width=120))
    from collections import Counter
    print(len(conds), "new;", dict(Counter(known.values())))


if __name__ == "__main__":
    main()
