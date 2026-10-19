"""Flatten a paper's LaTeX source into one text file for the extractor.

Output corpus/pre/<arxiv_id>.tex (gitignored) contains:
  1. macro and theorem-environment definitions from the preamble, so the model can
     read paper-specific shorthand;
  2. the document body with comments stripped and \\input/\\include inlined. If the
     body is too long, the appendix is dropped except for its theorem-like
     environments (which hold the formal results);
  3. the bibliography (.bbl), so cited results can be resolved to titles.

Usage: uv run python pipeline/preprocess.py [--only ID ...]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "corpus" / "src"
PRE = ROOT / "corpus" / "pre"
MANIFEST = ROOT / "corpus" / "manifest.yaml"
MAX_BODY_CHARS = 250_000
MAX_BBL_CHARS = 40_000

INPUT_RE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
COMMENT_RE = re.compile(r"(?<!\\)%.*")
MACRO_RE = re.compile(
    r"^\s*\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator\*?|def|newtheorem|"
    r"theoremstyle|newenvironment|let)\b.*$", re.M)
THM_ENVS = ("theorem", "thm", "corollary", "cor", "proposition", "prop", "lemma", "lem",
            "assumption", "definition", "defn", "claim", "conjecture", "fact", "remark")
ENV_RE = re.compile(r"\\begin\{(\w+)\*?\}(?:\[[^\]]*\])?.*?\\end\{\1\*?\}", re.S)


def pre_path(paper: dict) -> Path:
    """Preprocessed source for a manifest entry: keyed by arXiv id, else by manifest id
    (non-arXiv papers are converted from PDF by pipeline/fetch_pdf.py)."""
    key = paper.get("arxiv_id") or paper["id"]
    return PRE / f"{key.replace('/', '_')}.tex"


def strip_comments(text: str) -> str:
    return "\n".join(COMMENT_RE.sub("", line) for line in text.splitlines())


def read_tex(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def flatten(path: Path, root: Path, seen: set[Path] | None = None) -> str:
    """Inline \\input/\\include recursively, staying inside the paper's directory."""
    seen = seen or set()
    if path in seen:
        return ""
    seen.add(path)
    text = strip_comments(read_tex(path))

    def repl(m: re.Match) -> str:
        name = m.group(1).strip()
        for cand in (root / name, root / f"{name}.tex"):
            cand = cand.resolve()
            if cand.is_file() and cand.is_relative_to(root.resolve()):
                return flatten(cand, root, seen)
        return m.group(0)

    return INPUT_RE.sub(repl, text)


def find_main(d: Path) -> Path | None:
    cands = [p for p in d.rglob("*.tex") if "\\documentclass" in read_tex(p)]
    cands.sort(key=lambda p: ("\\begin{document}" not in read_tex(p), len(p.parts)))
    return cands[0] if cands else None


NEWTHM_RE = re.compile(r"\\newtheorem\{(\w+)\}(?:\[(\w+)\])?\{([^}]*)\}(?:\[(\w+)\])?")
NUMBER_EVENTS_RE = re.compile(r"\\section(\*?)\s*\{|\\appendix\b|\\begin\{(\w+)\}")


def theorem_defs(preamble: str, paper_dir: Path) -> dict:
    """env -> (counter, printed name, reset-within) from \newtheorem in the preamble and .sty files."""
    # style files first so the paper's own definitions take precedence
    text = "\n".join(read_tex(s) for s in sorted(paper_dir.rglob("*.sty"))) + "\n" + preamble
    defs = {}
    for env, shared, name, within in NEWTHM_RE.findall(text):
        defs[env] = (shared or env, name, within)
    # an env sharing another's counter inherits that counter's reset-within
    for env, (c, name, within) in list(defs.items()):
        if c != env and c in defs and not within:
            defs[env] = (c, name, defs[c][2])
    return defs


def annotate_numbers(body: str, defs: dict) -> tuple[str, int]:
    r"""Insert "% [printed: Theorem 3.2]" before each numbered theorem-like environment by
    replaying LaTeX's counters, so the extractor copies numbers instead of counting.
    Approximate: \iffalse blocks are skipped; unknown environments are not annotated."""
    body = re.sub(r"\\iffalse\b.*?\\fi\b", "", body, flags=re.S)
    counters, sec, appendix, out, last, n = {}, 0, False, [], 0, 0
    for m in NUMBER_EVENTS_RE.finditer(body):
        tok = m.group(0)
        if tok.startswith("\\appendix"):
            appendix, sec = True, 0
            continue
        if tok.startswith("\\section"):
            if not m.group(1):
                sec += 1
                for c, _, w in defs.values():
                    if w == "section":
                        counters[c] = 0
            continue
        env = m.group(2)
        if env not in defs:
            continue
        c, name, within = defs[env]
        counters[c] = counters.get(c, 0) + 1
        prefix = ((chr(64 + sec) if appendix else str(sec)) + ".") if within == "section" else ""
        out.append(body[last:m.start()])
        out.append(f"% [printed: {name} {prefix}{counters[c]}]\n")
        last, n = m.start(), n + 1
    out.append(body[last:])
    return "".join(out), n


def theorem_envs(text: str) -> list[str]:
    return [m.group(0) for m in ENV_RE.finditer(text) if m.group(1).lower() in THM_ENVS]


def preprocess(arxiv_id: str) -> dict:
    d = SRC / arxiv_id.replace("/", "_")
    if not d.is_dir():
        raise FileNotFoundError(d)
    main = find_main(d)
    if main is None:
        return {"status": "no_tex"}
    full = flatten(main, main.parent)
    pre, _, body = full.partition("\\begin{document}")
    body = body.split("\\end{document}")[0]
    macros = "\n".join(m.group(0).strip() for m in MACRO_RE.finditer(pre))
    body, n_numbered = annotate_numbers(body, theorem_defs(pre, d))

    truncated = False
    if len(body) > MAX_BODY_CHARS and "\\appendix" in body:
        main_part, _, appendix = body.partition("\\appendix")
        envs = "\n\n".join(theorem_envs(appendix))
        body = main_part + "\n\\appendix\n% [appendix omitted except theorem-like environments]\n" + envs
        truncated = True
    if len(body) > MAX_BODY_CHARS:
        body = body[:MAX_BODY_CHARS] + "\n% [truncated]\n"
        truncated = True

    bbl = ""
    bbls = sorted(d.rglob("*.bbl"))
    if bbls:
        bbl = read_tex(bbls[0])[:MAX_BBL_CHARS]

    out = (f"% ===== MACROS AND ENVIRONMENTS (preamble) =====\n{macros}\n\n"
           f"% ===== DOCUMENT BODY =====\n{body.strip()}\n\n"
           f"% ===== BIBLIOGRAPHY =====\n{bbl}\n")
    PRE.mkdir(parents=True, exist_ok=True)
    (PRE / f"{arxiv_id.replace('/', '_')}.tex").write_text(out, encoding="utf-8")
    return {"status": "ok", "chars": len(out), "truncated": truncated, "has_bbl": bool(bbl),
            "n_thm_envs": len(theorem_envs(body)), "n_numbered": n_numbered}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    papers = yaml.safe_load(MANIFEST.read_text())["papers"]
    ids = [p["arxiv_id"] for p in papers if p.get("arxiv_id")]
    if args.only:
        ids = [i for i in ids if i in set(args.only)]
    for arxiv_id in ids:
        try:
            info = preprocess(arxiv_id)
        except FileNotFoundError:
            info = {"status": "not_fetched"}
        print(arxiv_id, info, flush=True)


if __name__ == "__main__":
    main()
