"""Explicit None return not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedDefinition,
    UnsupportedException,
)

EXPECTED = CodeGenExceptions(
    [
        UnsupportedException(
            path=Path(__file__).parent / "source.py",
            reason=UnsupportedDefinition.NONE_RETURN,
            lineno=5,
            symbol="rp_1",
        ),
    ]
)
