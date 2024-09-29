"""Explicit None return not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedProcedure,
    UnsupportedException,
)

EXPECTED = CodeGenExceptions(
    [
        UnsupportedException(
            path=Path(__file__).parent / "source.py",
            reason=UnsupportedProcedure.RETURN_NONE,
            lineno=5,
            symbol="rp_1",
        ),
    ]
)
