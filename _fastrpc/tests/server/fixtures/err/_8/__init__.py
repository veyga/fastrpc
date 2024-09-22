"""Untyped parameters not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedParameter,
    UnsupportedException,
)

path = Path(__file__).parent / "source.py"
EXPECTED = CodeGenExceptions(
    [
        UnsupportedException(
            reason=UnsupportedParameter.UNTYPED,
            path=path,
            lineno=7,
            symbol="x",
        ),
        UnsupportedException(
            reason=UnsupportedParameter.UNTYPED,
            path=path,
            lineno=12,
            symbol="x",
        ),
        UnsupportedException(
            reason=UnsupportedParameter.UNTYPED,
            path=path,
            lineno=12,
            symbol="y",
        ),
        UnsupportedException(
            reason=UnsupportedParameter.UNTYPED,
            path=path,
            lineno=17,
            symbol="y",
        ),
        UnsupportedException(
            reason=UnsupportedParameter.UNTYPED,
            path=path,
            lineno=25,
            symbol="z",
        ),
    ]
)
