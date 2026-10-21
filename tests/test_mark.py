from __future__ import annotations

import pytest

from shuttle.mark import read_mark


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("---\nmetadata:\n  managed-by: repo-1\n---\n", "repo-1"),
        ("<!-- managed-by: repo.2 -->\n", "repo.2"),
        ("# managed-by: repo_3\n", "repo_3"),
        ('managed-by: "quoted"\n', "quoted"),
        ("nothing here\n", None),
        ("text mentioning managed-by: inline\n", None),
        ("\n" * 50 + "managed-by: too-late\n", None),
    ],
)
def test_read_mark(text: str, expected: str | None) -> None:
    assert read_mark(text) == expected
