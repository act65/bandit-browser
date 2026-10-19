"""Seed data/algorithms.yaml by clustering the algorithm mentions in existing extractions.

One `claude -p` call: the model groups mentions that denote the same algorithm and
mints canonical ids. The output is a proposal for human review (D13); later
extractions reference these ids, and new algorithms are appended by resolve.py.

Usage: uv run python pipeline/seed_algorithms.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claude_cli  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "algorithms.yaml"

SYSTEM = """You curate a registry of bandit algorithms for a knowledge graph of theoretical results.
You receive every algorithm mention extracted from a corpus of papers (paper id, name as written,
whether the paper introduces it, technique tags). Group mentions that denote the SAME algorithm
(same update rule; trivial renamings, abbreviations and "the algorithm of X et al." count as the same;
genuinely different variants such as KL-UCB vs KL-UCB++ or UCB1 vs UCB-V are DIFFERENT entries).
For each algorithm produce:
- id: short stable snake_case id, e.g. ucb1, kl_ucb, kl_ucb_plus_plus, thompson_sampling_beta, exp3, exp3_ix, tsallis_inf, oful, lin_ts
- name: the canonical display name used in the literature
- aliases: every distinct surface form seen in the mentions (verbatim)
- family: one of optimism, thompson_sampling, elimination, explore_then_commit, exponential_weights,
  ftrl_or_mirror_descent, information_directed_sampling, track_and_stop, minimum_empirical_divergence,
  black_box_reduction, other
- introduced_in: the paper id that introduces it if one of the listed papers does (is_new=true), else null
- mentions: list of {paper, name} for every mention in the group
Every mention must appear in exactly one group. Do not invent algorithms that are not mentioned."""

SCHEMA = {
    "type": "object",
    "properties": {"algorithms": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"}, "name": {"type": "string"},
            "aliases": {"type": "array", "items": {"type": "string"}},
            "family": {"type": "string"},
            "introduced_in": {"type": ["string", "null"]},
            "mentions": {"type": "array", "items": {"type": "object", "properties": {
                "paper": {"type": "string"}, "name": {"type": "string"}},
                "required": ["paper", "name"], "additionalProperties": False}},
        },
        "required": ["id", "name", "aliases", "family", "introduced_in", "mentions"],
        "additionalProperties": False}}},
    "required": ["algorithms"], "additionalProperties": False,
}


def main() -> None:
    mentions = []
    for f in sorted((ROOT / "data" / "extractions").glob("*.json")):
        for a in json.loads(f.read_text())["algorithms"]:
            mentions.append({"paper": f.stem, "name": a["name"], "is_new": a["is_new"],
                             "techniques": a["techniques"]})
    out, _ = claude_cli.call_structured(SYSTEM, json.dumps(mentions, ensure_ascii=False), SCHEMA,
                                        label="seed_algorithms", timeout=1800)
    algos = sorted(out["algorithms"], key=lambda a: a["id"])
    seen = {(m["paper"], m["name"]) for a in algos for m in a["mentions"]}
    missing = [m for m in mentions if (m["paper"], m["name"]) not in seen]
    header = ("# Algorithm registry (D13). Seeded by pipeline/seed_algorithms.py from the v0.2\n"
              "# extractions; review by hand. `id`s are stable: rename via aliases, never reuse.\n")
    OUT.write_text(header + yaml.safe_dump({"algorithms": algos}, sort_keys=False, allow_unicode=True, width=100))
    print(f"{len(mentions)} mentions -> {len(algos)} algorithms; {len(missing)} mentions unassigned")
    for m in missing:
        print("  unassigned:", m["paper"], m["name"])


if __name__ == "__main__":
    main()
