"""Validate extractions (desiderata D5 'auto-checked').

Checks, per file in data/extractions/:
  - schema: pydantic validation against the ontology-derived models;
  - references: result.setting / result.algorithm point at declared ids;
  - expressions: every bound.expression parses with SymPy; symbols outside the
    canonical table must be declared in result.symbols;
  - quotes: every source.quote / definition_quote occurs in the preprocessed
    source (whitespace-normalised; '...' splits a quote into fragments).

Writes data/validation-report.md and prints a summary.
Usage: uv run python pipeline/validate.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import sympy
import yaml
from pydantic import ValidationError
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema  # noqa: E402

ROOT = schema.ROOT
EXT = ROOT / "data" / "extractions"
PRE = ROOT / "corpus" / "pre"
MANIFEST = ROOT / "corpus" / "manifest.yaml"
REPORT = ROOT / "data" / "validation-report.md"

CANONICAL = {"T", "K", "d", "Delta_i", "Delta_min", "Delta_max", "mu_star", "sigma", "delta",
             "epsilon", "S", "L_feat", "L_lip", "m", "C", "S_T", "V_T", "D", "B", "N", "H",
             "gamma_T", "KL_i", "diam_K", "vartheta", "alpha", "beta", "p", "lam",
             "i", "pi", "E"}
FUNCS = {"sum_subopt": sympy.Function("sum_subopt"), "sum_arms": sympy.Function("sum_arms"),
         "log": sympy.log, "sqrt": sympy.sqrt, "exp": sympy.exp, "pi": sympy.pi,
         "Min": sympy.Min, "Max": sympy.Max, "min": sympy.Min, "max": sympy.Max}


LATEX_NOISE = re.compile(r"\\[\[\]()]|\$|~|\\[,;!: ]|\\(?:left|right|big|Big|bigg|Bigg)\b|[{}]")
QUOTE_THRESHOLD = 0.5  # faithful-but-reflowed quotes score 0.55-0.8; invented ones ~0. Fraction of the quote's 25-char windows that must occur in the source


def norm(s: str) -> str:
    """Drop whitespace, maths delimiters, spacing macros and braces before matching."""
    return LATEX_NOISE.sub("", re.sub(r"\s+", "", s))


def quote_score(quote: str, source_norm: str, w: int = 25) -> float:
    """Fraction of the quote's w-char windows (stride w//2) present in the source.

    Exact matching is too strict: models drop delimiters or reflow LaTeX. '...'
    elisions simply contribute windows that are skipped.
    """
    frags = [norm(f) for f in re.split(r"\.\.\.|…|\[\.\.\.\]", quote)]
    wins = [f[i:i + w] for f in frags for i in range(0, max(len(f) - w, 0) + 1, w // 2) if len(f) >= w]
    return sum(x in source_norm for x in wins) / len(wins) if wins else 0.0


def quote_found(quote: str, source_norm: str) -> bool:
    return quote_score(quote, source_norm) >= QUOTE_THRESHOLD


IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
KNOWN_FUNCS = {"log", "sqrt", "exp", "Min", "Max", "min", "max", "LambertW", "sum_subopt", "sum_arms"}


def check_expression(expr: str, declared: set[str]) -> str | None:
    """Parse with every identifier bound explicitly (SymPy's own names such as S, E, N
    would otherwise shadow canonical variables). Unknown names followed by '(' are
    treated as functions; both symbols and functions must be canonical or declared."""
    local = {}
    for m in IDENT_RE.finditer(expr):
        name = m.group(0)
        if name in local or name in KNOWN_FUNCS or name == "pi":
            continue
        is_call = expr[m.end():m.end() + 1] == "("
        local[name] = sympy.Function(name) if is_call else sympy.Symbol(name)
    try:
        parse_expr(expr, local_dict={**FUNCS, "LambertW": sympy.LambertW, **local},
                   transformations=standard_transformations, evaluate=False)
    except Exception as ex:  # SymPy raises many exception types on bad input
        return f"unparseable: {type(ex).__name__}"
    unknown = set(local) - CANONICAL - declared
    return f"undeclared names {sorted(unknown)}" if unknown else None


def validate_file(path: Path, Model, manifest: dict) -> tuple[list[str], dict]:
    issues: list[str] = []
    raw = json.loads(path.read_text())
    run = raw.pop("_run", {})
    stats = Counter()
    try:
        Model.model_validate(raw)
    except ValidationError as e:
        issues += [f"schema: {err['loc']}: {err['msg']}" for err in e.errors()[:10]]

    setting_ids = {s.get("id") for s in raw.get("settings", [])}
    algo_ids = {a.get("id") for a in raw.get("algorithms", [])}
    paper = manifest.get(path.stem, {})
    pre_path = PRE / f"{(paper.get('arxiv_id') or '').replace('/', '_')}.tex"
    source_norm = norm(pre_path.read_text(encoding="utf-8")) if pre_path.exists() else None

    for s in raw.get("settings", []):
        if s.get("unmapped"):
            stats["settings_with_unmapped"] += 1
        if source_norm and not quote_found(s.get("definition_quote", ""), source_norm):
            stats["setting_quote_not_found"] += 1
    for r in raw.get("results", []):
        stats["results"] += 1
        rid = r.get("id")
        if r.get("setting") not in setting_ids:
            issues.append(f"{rid}: unknown setting {r.get('setting')}")
        if r.get("algorithm") and r["algorithm"] not in algo_ids:
            issues.append(f"{rid}: unknown algorithm {r['algorithm']}")
        err = check_expression(r.get("bound", {}).get("expression", ""), set(r.get("symbols", {})))
        if err:
            stats["expr_issues"] += 1
            issues.append(f"{rid}: expression {err}: `{r['bound']['expression']}`")
        if source_norm is not None:
            if quote_found(r.get("source", {}).get("quote", ""), source_norm):
                stats["quotes_ok"] += 1
            else:
                stats["quote_not_found"] += 1
                issues.append(f"{rid}: quote not found in source ({r['source'].get('number')})")
        stats[f"confidence_{r.get('confidence')}"] += 1
    stats["cited_results"] = len(raw.get("cited_results", []))
    stats["cost_usd_equiv"] = run.get("cost_usd_equiv") or 0
    return issues, stats


def main() -> None:
    Model = schema.build_models(schema.load_ontology())
    manifest = {p["id"]: p for p in yaml.safe_load(MANIFEST.read_text())["papers"]}
    files = sorted(EXT.glob("*.json"))
    total = Counter()
    lines = ["# Validation report", "",
             "Generated by `pipeline/validate.py`. Automatic checks only: schema, references, "
             "SymPy parsing, and verbatim quotes.", ""]
    for f in files:
        issues, stats = validate_file(f, Model, manifest)
        total.update(stats)
        total["files"] += 1
        total["files_clean"] += not issues
        lines.append(f"## {f.stem}  ({stats['results']} results, {len(issues)} issues)")
        lines += [f"- {i}" for i in issues] or ["- clean"]
        lines.append("")
    summary = ["## Summary", ""] + [f"- {k}: {round(v, 2) if isinstance(v, float) else v}"
                                    for k, v in sorted(total.items())] + [""]
    REPORT.write_text("\n".join(lines[:4] + summary + lines[4:]))
    print("\n".join(summary))


if __name__ == "__main__":
    main()
