"""Untyped parameters not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedParameter,
    UnsupportedParameterException,
    UnsupportedParameterException,
)

path = Path(__file__).parent / "source.py"
EXPECTED = CodeGenExceptions(
    [
        UnsupportedParameterException(
            path=path,
            lineno=7,
            symbol="x",
            definition=UnsupportedParameter.UNTYPED,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=12,
            symbol="x",
            definition=UnsupportedParameter.UNTYPED,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=12,
            symbol="y",
            definition=UnsupportedParameter.UNTYPED,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=17,
            symbol="y",
            definition=UnsupportedParameter.UNTYPED,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=25,
            symbol="z",
            definition=UnsupportedParameter.UNTYPED,
        ),
    ]
)
