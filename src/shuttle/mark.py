"""The origin mark: how generated files are recognized as belonging to a repository."""

from __future__ import annotations

import re

MARK_KEY = "managed-by"
_SCAN_LINES = 40
_MARK = re.compile(rf"^\s*(?:#\s*|<!--\s*)?{MARK_KEY}:\s*[\"']?([A-Za-z0-9][A-Za-z0-9._-]*)")


def read_mark(text: str) -> str | None:
    """Return the repository name in the mark found in the first lines, if any."""
    for line in text.splitlines()[:_SCAN_LINES]:
        match = _MARK.match(line)
        if match:
            return match.group(1)
    return None
