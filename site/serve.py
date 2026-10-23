"""Local preview server for _site/ with HTTP Range support.

The site reads its SQLite database with range requests (sql.js-httpvfs), which Python's
built-in `http.server` does not implement. GitHub Pages does.

Usage: uv run python site/serve.py [--port 8000] [--dir _site]
"""

from __future__ import annotations

import argparse
import functools
import http.server
import os
import re
from pathlib import Path

RANGE = re.compile(r"bytes=(\d*)-(\d*)$")


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        m = RANGE.match(self.headers.get("Range", "").strip())
        path = self.translate_path(self.path)
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        start, end = m.group(1), m.group(2)
        if start == "":  # suffix range: the last N bytes
            first, last = max(0, size - int(end)), size - 1
        else:
            first, last = int(start), min(int(end) if end else size - 1, size - 1)
        if first >= size or first > last:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None
        f = open(path, "rb")
        f.seek(first)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {first}-{last}/{size}")
        self.send_header("Content-Length", str(last - first + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remaining = last - first + 1
        return f

    def copyfile(self, source, outputfile):
        n = getattr(self, "_remaining", None)
        if n is None:
            return super().copyfile(source, outputfile)
        while n > 0:
            chunk = source.read(min(65536, n))
            if not chunk:
                break
            outputfile.write(chunk)
            n -= len(chunk)
        self._remaining = None

    def end_headers(self):
        if self.headers.get("Range") is None:
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--dir", type=Path, default=Path(__file__).resolve().parent.parent / "_site")
    args = ap.parse_args()
    handler = functools.partial(RangeHandler, directory=str(args.dir))
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as srv:
        print(f"serving {args.dir} on http://127.0.0.1:{args.port}/ (with Range support)")
        srv.serve_forever()


if __name__ == "__main__":
    main()
