"""Use the Claude Code CLI (`claude -p`) as the LLM backend.

Adapted from act65/pol-score-cards attribute-extraction/claude_cli.py. Routes
calls through the local `claude` binary, which authenticates with the user's
Claude subscription, so no API key or credits are needed. `--json-schema` makes
the CLI enforce the output schema and return a parsed `structured_output`.

Paper text is untrusted, so every call runs with all tools disabled
(`--tools ""`), no MCP servers, and no session persistence.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import threading
import time

_USAGE_LOCK = threading.Lock()


class QuotaExhausted(RuntimeError):
    """The subscription's usage window is spent; retrying cannot help.

    Signature: an `is_error` envelope with zero API time and zero tokens, which no
    real API error produces.
    """


def _record_usage(env: dict, label: str = "") -> None:
    """Append one usage row to $CLAUDE_CLI_USAGE_LOG, if set."""
    path = os.environ.get("CLAUDE_CLI_USAGE_LOG", "")
    if not path:
        return
    u = env.get("usage") or {}
    row = {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "label": label,
        "input": u.get("input_tokens"),
        "cache_read": u.get("cache_read_input_tokens"),
        "cache_creation": u.get("cache_creation_input_tokens"),
        "output": u.get("output_tokens"),
        "duration_ms": env.get("duration_ms"),
        "cost_usd": env.get("total_cost_usd"),
        "models": list((env.get("modelUsage") or {}).keys()),
    }
    try:
        with _USAGE_LOCK, open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
    except OSError:
        pass  # accounting must never break an extraction run


def _is_quota_error(envelope: dict) -> bool:
    if not envelope.get("is_error"):
        return False
    usage = envelope.get("usage") or {}
    spent = sum(v for k, v in usage.items() if k.endswith("tokens") and isinstance(v, int))
    return envelope.get("duration_api_ms") == 0 and spent == 0


def call_structured(system: str, user: str, schema: dict, model: str | None = None,
                    effort: str | None = None, timeout: int = 900, retries: int = 2,
                    label: str = "", tools: str = "") -> tuple[dict, dict]:
    """Run one structured call; return (structured_output, envelope).

    The system prompt replaces Claude Code's default one, which extraction does not
    need and which would otherwise be sent on every call. The user message goes on
    stdin: a whole paper exceeds Linux's 128 KB limit on a single argv string.
    `tools` is empty (no tools) except for retrieval calls that never see paper text,
    e.g. tools="WebSearch,WebFetch" for gap triage.
    """
    cmd = ["claude", "-p",
           "--system-prompt", system,
           "--json-schema", json.dumps(schema),
           "--output-format", "json",
           "--tools", tools,
           "--strict-mcp-config",
           "--no-session-persistence"]
    if tools:
        # headless mode needs the tools pre-approved as well as made available
        cmd += ["--allowedTools", *tools.split(",")]
    if model:
        cmd += ["--model", model]
    if effort:
        cmd += ["--effort", effort]
    last_err = ""
    for attempt in range(retries + 1):
        proc = None
        try:
            proc = subprocess.run(cmd, input=user, capture_output=True,
                                  text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {timeout}s"
        if proc is not None and proc.stdout.strip():
            try:
                env = json.loads(proc.stdout)
            except json.JSONDecodeError:
                env, last_err = None, "result envelope was not JSON: " + proc.stdout[:300]
            if env is not None:
                _record_usage(env, label)
                if _is_quota_error(env):
                    raise QuotaExhausted("subscription usage window is spent; resume after reset")
                if env.get("is_error"):
                    last_err = str(env.get("result", "cli error"))[:300]
                elif env.get("structured_output") is not None:
                    return env["structured_output"], env
                else:
                    last_err = "no structured_output in envelope"
        elif proc is not None:
            last_err = (proc.stderr or "").strip()[:1200] or f"exit {proc.returncode}"
        if attempt < retries:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"claude --json-schema failed after {retries + 1} attempts: {last_err}")
