"""Nested functions not yet supported"""

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
            reason=UnsupportedDefinition.NESTED,
            lineno=7,
            symbol="rp_1_inner",
        ),
    ]
)
