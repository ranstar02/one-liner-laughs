#!/usr/bin/env python3
"""One-Liner Laughs — write one original funny line to /output/entry.txt.

The program is fully deterministic: it writes the same fixed line on every
run, with no randomness, no network access and no input beyond the output
directory. It validates the line (one line, 1-200 characters, non-blank),
writes it, then reads the file back and checks the bytes match exactly.
"""

import os
import sys

LINE = "I bought a self-help book; it filed a restraining order."

MAX_CHARS = 200


def validate(line):
    """Raise ValueError if the line breaks the competition gate."""
    if not line:
        raise ValueError("line is empty")
    if not line.strip():
        raise ValueError("line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "line is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )


def main():
    validate(LINE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)

    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError(
            "read-back mismatch: entry.txt holds %d bytes, expected %d"
            % (len(written), len(data))
        )
    # Re-validate the exact bytes that landed on disk, decoded as UTF-8,
    # so a corrupt or truncated write fails loudly instead of passing.
    validate(written.decode("utf-8"))

    print("wrote %d characters to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
