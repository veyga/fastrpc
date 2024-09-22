"""Duplicate names"""

from pathlib import Path

from _fastrpc.server.exceptions import DuplicatedNameException

EXPECTED = [
    DuplicatedNameException(
        path=Path(__file__).parent / "sourceA.py",
        lineno=5,
        name="rp_1",
        existing=Path(__file__).parent / "sourceB.py",
    ),
]
