"""Decorated non-async function"""

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
            reason=UnsupportedDefinition.SYNCHRONOUS,
            lineno=5,
            symbol="rp_1",
        ),
    ]
)
