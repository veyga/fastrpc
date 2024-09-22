"""Duplicate names"""

from pathlib import Path

from _fastrpc.server.exceptions import CodeGenExceptions, DuplicatedNameException

parent = Path(__file__).parent

EXPECTED = CodeGenExceptions(
    [
        DuplicatedNameException(
            path=parent / "sourceA.py",
            lineno=5,
            name="rp_1",
            conflicting_module=parent / "sourceB.py",
        ),
    ]
)
