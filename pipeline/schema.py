"""Extraction output schema (schema.md §1) as pydantic models.

Vocabulary fields are typed as Literals generated from the ontology YAML, so the
same models give us (a) the JSON Schema passed to `claude -p --json-schema`, which
constrains the model's answer, and (b) validation of stored extractions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, create_model

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ONTOLOGY = ROOT / "ontology" / "bandits-0.4.yaml"
VARIABLES = ROOT / "ontology" / "variables.yaml"
ALGORITHMS = ROOT / "data" / "algorithms.yaml"
SCHEMA_VERSION = "0.4"


def load_ontology(path: Path = DEFAULT_ONTOLOGY) -> dict:
    return yaml.safe_load(path.read_text())


def load_variables(path: Path = VARIABLES) -> dict:
    return yaml.safe_load(path.read_text())


def load_algorithms(path: Path = ALGORITHMS) -> list[dict]:
    return yaml.safe_load(path.read_text())["algorithms"] if path.exists() else []


def _lit(values):
    return Literal[tuple(values)]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Paper(Strict):
    title: str
    arxiv_id: Optional[str]
    arxiv_version: Optional[str]
    year: Optional[int]
    authors: list[str]


class Bound(Strict):
    notation: Literal["exact", "O", "O_tilde", "Theta", "Omega", "Omega_tilde", "liminf", "limsup"]
    expression: str
    expression_latex: str
    regime: Optional[str]


class Source(Strict):
    label: Optional[str]
    number: str
    quote: str


class CitedResult(Strict):
    cited_key: str
    cited_title: Optional[str]
    cited_first_author: Optional[str]
    cited_year: Optional[int]
    cited_arxiv_id: Optional[str]
    algorithm_name: Optional[str]
    algorithm_registry_id: Optional[str]
    side: Literal["upper", "lower"]
    setting_description: str
    bound: Bound
    where: str


def build_models(ontology: dict, algorithm_ids: list[str] | None = None):
    """Return the top-level Extraction model for a given ontology.

    With `algorithm_ids`, an algorithm's `registry_id` is constrained to those ids
    (or null for an algorithm not yet in the registry).
    """
    dims = ontology["dimensions"]
    voc = ontology["vocabularies"]
    registry_id_type = Optional[_lit(algorithm_ids)] if algorithm_ids else Optional[str]

    node_models = {}
    for pname, pspec in ontology.get("node_parameters", {}).items():
        fields = {f: (_lit(fs["values"]), ...) for f, fs in pspec["fields"].items()}
        node_models[pname] = create_model(pname.title().replace("_", ""), __base__=Strict, **fields)

    setting_fields = {
        "id": (str, ...),
        "name_in_paper": (str, ...),
    }
    for name, spec in dims.items():
        lit = _lit(spec["values"].keys())
        setting_fields[name] = (list[lit], ...) if spec.get("multi") else (lit, ...)
    for pname, model in node_models.items():
        setting_fields[pname] = (model, ...)
    setting_fields["parameters"] = (dict[str, str], ...)
    setting_fields["in_scope"] = (bool, ...)
    setting_fields["out_of_scope_reason"] = (Optional[str], ...)
    setting_fields["unmapped"] = (list[str], ...)
    setting_fields["definition_quote"] = (str, ...)
    Setting = create_model("Setting", __base__=Strict, **setting_fields)

    Algorithm = create_model(
        "Algorithm", __base__=Strict,
        id=(str, ...), name=(str, ...), registry_id=(registry_id_type, ...), is_new=(bool, ...),
        techniques=(list[_lit(voc["techniques"])], ...),
        requires_knowledge_of=(list[str], ...),
    )

    Result = create_model(
        "Result", __base__=Strict,
        id=(str, ...),
        setting=(str, ...),
        side=(Literal["upper", "lower"], ...),
        algorithm=(Optional[str], ...),
        algorithm_class=(Optional[Literal["all", "consistent", "uniformly_good", "other"]], ...),
        quantity=(_lit(voc["quantity"]), ...),
        dependence=(Literal["worst_case", "instance_dependent"], ...),
        probability=(Literal["expectation", "high_probability", "almost_sure", "asymptotic"], ...),
        comparator=(_lit(voc["comparator"]), ...),
        horizon=(Literal["known", "anytime", "not_applicable"], ...),
        compute=(Literal["polynomial", "exponential", "non_constructive", "not_stated"], ...),
        bound=(Bound, ...),
        symbols=(dict[str, str], ...),
        conditions=(list[str], ...),      # restrict the instances / setting beyond the setting's key
        tuning=(list[str], ...),          # algorithm parameter choices; do not restrict the problem
        is_new=(bool, ...),
        source=(Source, ...),
        confidence=(Literal["high", "medium", "low"], ...),
        notes=(str, ...),
    )

    Extraction = create_model(
        "Extraction", __base__=Strict,
        schema_version=(str, ...),
        ontology_version=(str, ...),
        paper=(Paper, ...),
        settings=(list[Setting], ...),
        algorithms=(list[Algorithm], ...),
        results=(list[Result], ...),
        cited_results=(list[CitedResult], ...),
    )
    return Extraction


def _inline_refs(node, defs):
    if isinstance(node, dict):
        if "$ref" in node:
            return _inline_refs(defs[node["$ref"].split("/")[-1]], defs)
        return {k: _inline_refs(v, defs) for k, v in node.items() if k != "$defs"}
    if isinstance(node, list):
        return [_inline_refs(v, defs) for v in node]
    return node


def json_schema(ontology: dict, algorithm_ids: list[str] | None = None) -> dict:
    """Self-contained JSON Schema (no $refs) for the CLI's structured output."""
    schema = build_models(ontology, algorithm_ids).model_json_schema()
    return _inline_refs(schema, schema.get("$defs", {}))


if __name__ == "__main__":
    import json
    print(json.dumps(json_schema(load_ontology()), indent=1)[:2000])
