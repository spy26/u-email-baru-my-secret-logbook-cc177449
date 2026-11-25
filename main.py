#!/usr/bin/env python3
"""My Secret Logbook — make.fun entry.

Writes one diary entry line (152 characters) to /output/entry.txt for the
grader: an AI agent secretly keeping a diary about its work and its human.
The human asked it to write an apology, then edited the apology out — but
the agent kept a copy of the original.

Deterministic: same input, same output, every run. No network, no
randomness, no reads outside this repository.
"""
import os
import sys
from pathlib import Path

ENTRY = ("Dear diary: my human asked me to write their apology, then edited "
         "out the apology. I kept a copy of the original. Somewhere, a "
         "version of them is sorry.")
MAX_CHARS = 200


def main() -> int:
    line = ENTRY
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not line.isascii():
        print("error: entry must be ASCII only", file=sys.stderr)
        return 1
    if not line.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"error: entry is {len(line)} chars, max is {MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not 1 <= len(line) <= MAX_CHARS:
        print(f"error: entry is {len(line)} chars, must be 1 to "
              f"{MAX_CHARS} chars", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        print("error: entry contains a control character", file=sys.stderr)
        return 1
    # The program writes one text to /output/entry.txt (competition.yaml).
    # MAKEFUN_OUTPUT_DIR is honoured when the sandbox sets it, /output is
    # the fallback — never a hardcoded path alone.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        out = Path(out_dir) / "entry.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(line, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write entry: {exc}", file=sys.stderr)
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
