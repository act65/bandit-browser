"""Download and convert PDFs for non-arXiv papers in corpus/manifest.yaml.

For every manifest entry with `arxiv_id: null` and a `pdf_url`, this downloads the PDF to
corpus/src/<id>/paper.pdf and converts it with `pdftotext -layout` (or pdftotext's reading-order mode when a
two-column layout is detected) into corpus/pre/<id>.tex,
so the LLM extractor can read it like the preprocessed arXiv sources. Both directories are
gitignored (copyright).

PDFs are untrusted data: they are only written to disk and handed to pdftotext as a file
argument (no shell), never opened or executed otherwise.

Some publisher sites (e.g. ScienceDirect) refuse scripted downloads even for open-archive
articles. In that case, download the PDF in a browser, save it as corpus/src/<id>/paper.pdf
and rerun: an existing paper.pdf is reused unless --force is given.

Usage: uv run python pipeline/fetch_pdf.py [--only ID ...] [--force]
"""

from __future__ import annotations

import argparse
import subprocess
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "corpus" / "manifest.yaml"
SRC = ROOT / "corpus" / "src"
PRE = ROOT / "corpus" / "pre"
UA = "bandit-browser/0.1 (research corpus; https://github.com/act65/bandit-browser)"
PDFTOTEXT = "pdftotext"
MAX_BODY_CHARS = 250_000
MAX_PDF_BYTES = 50 * 1024 * 1024
DELAY_S = 2
TWO_COLUMN_GUTTER = 0.7  # fraction of full-width lines blank at one mid-page column
HEADER = "% ===== DOCUMENT BODY (converted from PDF by pdftotext; maths is lossy) ====="


def download(paper_id: str, url: str, force: bool) -> str:
    dest = SRC / paper_id
    pdf = dest / "paper.pdf"
    if pdf.exists() and not force:
        return "cached"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read(MAX_PDF_BYTES + 1)
    if len(raw) > MAX_PDF_BYTES:
        raise ValueError("PDF larger than 50 MB")
    if raw[:5] != b"%PDF-":
        raise ValueError(f"not a PDF (starts with {raw[:16]!r}); "
                         f"download it in a browser to {pdf.relative_to(ROOT)}")
    dest.mkdir(parents=True, exist_ok=True)
    tmp = dest / "paper.pdf.part"
    tmp.write_bytes(raw)
    tmp.replace(pdf)
    return f"downloaded {len(raw)} bytes"


def pdftotext(pdf: Path, layout: bool) -> str:
    cmd = [PDFTOTEXT, *(["-layout"] if layout else []), "-enc", "UTF-8", str(pdf), "-"]
    res = subprocess.run(cmd, capture_output=True, timeout=120, check=True)
    text = res.stdout.decode("utf-8", errors="replace").replace("\f", "\n")  # page breaks
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def two_column(layout_text: str) -> bool:
    """Detect a two-column page layout: a vertical whitespace gutter near the middle.

    With -layout, two-column papers come out with left and right columns interleaved line by
    line, which scrambles theorem statements; pdftotext's default reading-order mode keeps
    each column's prose contiguous, so we fall back to it for such papers.
    """
    lines = [ln for ln in layout_text.splitlines() if ln.strip()]
    if not lines:
        return False
    width = max(map(len, lines))
    long_lines = [ln for ln in lines if len(ln) > 0.75 * width]
    if len(long_lines) < 20:
        return False
    best = max(sum(ln[x:x + 2] == "  " for ln in long_lines) / len(long_lines)
               for x in range(int(0.4 * width), int(0.6 * width)))
    return best > TWO_COLUMN_GUTTER


def convert(paper_id: str) -> dict:
    pdf = SRC / paper_id / "paper.pdf"
    if pdf.read_bytes()[:5] != b"%PDF-":
        raise ValueError(f"{pdf.relative_to(ROOT)} is not a PDF")
    text = pdftotext(pdf, layout=True)
    mode = "-layout"
    if two_column(text):
        text = pdftotext(pdf, layout=False)
        mode = "reading order (two-column layout detected)"
    truncated = len(text) > MAX_BODY_CHARS
    if truncated:
        text = text[:MAX_BODY_CHARS] + "\n% [truncated]"
    out = f"{HEADER}\n% pdftotext mode: {mode}\n{text}\n"
    PRE.mkdir(parents=True, exist_ok=True)
    (PRE / f"{paper_id}.tex").write_text(out, encoding="utf-8")
    return {"chars": len(out), "truncated": truncated, "mode": mode}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="manifest ids to process (default: all eligible)")
    ap.add_argument("--force", action="store_true", help="re-download even if paper.pdf exists")
    args = ap.parse_args()

    papers = yaml.safe_load(MANIFEST.read_text())["papers"]
    todo = [p for p in papers if p.get("arxiv_id") is None and p.get("pdf_url")]
    if args.only:
        todo = [p for p in todo if p["id"] in set(args.only)]
    for i, p in enumerate(todo):
        tag = f"[{i + 1}/{len(todo)}] {p['id']}"
        try:
            status = download(p["id"], p["pdf_url"], args.force)
        except Exception as e:  # keep going; report per paper
            print(f"{tag}: download ERROR {e}", flush=True)
            if (SRC / p["id"] / "paper.pdf").exists():
                status = "cached (download failed)"
            else:
                continue
        try:
            info = convert(p["id"])
            print(f"{tag}: {status}; {info['chars']} chars"
                  f"{' (truncated)' if info['truncated'] else ''}; {info['mode']}", flush=True)
        except Exception as e:
            print(f"{tag}: {status}; convert ERROR {e}", flush=True)
        if status.startswith("downloaded"):
            time.sleep(DELAY_S)


if __name__ == "__main__":
    main()
