"""Download arXiv LaTeX sources for papers in corpus/manifest.yaml.

Sources land in corpus/src/<arxiv_id>/ (gitignored: the default arXiv licence does
not allow us to redistribute them). Archives are untrusted data; they are only
unpacked, with tarfile's 'data' filter, and never executed.

Usage: uv run python pipeline/fetch.py [--only ID ...]
"""

from __future__ import annotations

import argparse
import gzip
import io
import tarfile
import time
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "corpus" / "manifest.yaml"
SRC = ROOT / "corpus" / "src"
UA = "bandit-browser/0.1 (research corpus; https://github.com/act65/bandit-browser)"
DELAY_S = 3  # arXiv asks for at most one request every 3 seconds


def safe_dir(arxiv_id: str) -> str:
    return arxiv_id.replace("/", "_")


def unpack(raw: bytes, dest: Path) -> str:
    """Unpack an e-print payload; return its kind ('tar', 'tex' or 'pdf')."""
    dest.mkdir(parents=True, exist_ok=True)
    if raw[:4] == b"%PDF":
        (dest / "paper.pdf").write_bytes(raw)
        return "pdf"
    data = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(dest, filter="data")
        return "tar"
    except tarfile.ReadError:
        (dest / "main.tex").write_bytes(data)
        return "tex"


def fetch(arxiv_id: str, force: bool = False) -> str:
    dest = SRC / safe_dir(arxiv_id)
    if dest.exists() and any(dest.iterdir()) and not force:
        return "cached"
    req = urllib.request.Request(f"https://arxiv.org/e-print/{arxiv_id}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return unpack(raw, dest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="arXiv ids to fetch (default: all in manifest)")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    papers = yaml.safe_load(MANIFEST.read_text())["papers"]
    ids = [p["arxiv_id"] for p in papers if p.get("arxiv_id")]
    if args.only:
        ids = [i for i in ids if i in set(args.only)]
    for i, arxiv_id in enumerate(ids):
        try:
            kind = fetch(arxiv_id, args.force)
        except Exception as e:  # keep going; report at the end of the line
            kind = f"ERROR {e}"
        print(f"[{i + 1}/{len(ids)}] {arxiv_id}: {kind}", flush=True)
        if kind != "cached":
            time.sleep(DELAY_S)


if __name__ == "__main__":
    main()
