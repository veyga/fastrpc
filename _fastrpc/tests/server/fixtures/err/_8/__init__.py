"""Untyped parameters not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UntypedParameterException,
)

EXPECTED = CodeGenExceptions(
    [
        UntypedParameterException(
            path=Path(__file__).parent / "source.py",
            lineno=7,
            parameter="x",
        ),
        UntypedParameterException(
            path=Path(__file__).parent / "source.py",
            lineno=12,
            parameter="x",
        ),
        UntypedParameterException(
            path=Path(__file__).parent / "source.py",
            lineno=12,
            parameter="y",
        ),
        UntypedParameterException(
            path=Path(__file__).parent / "source.py", lineno=17, parameter="y"
        ),
        UntypedParameterException(
            path=Path(__file__).parent / "source.py",
            lineno=25,
            parameter="z",
        ),
    ]
)
