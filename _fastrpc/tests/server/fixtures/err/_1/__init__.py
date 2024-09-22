"""Decorated non-async function"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = CodeGenExceptions(
    [
        UnsupportedDefinitionException(
            path=Path(__file__).parent / "source.py",
            definition=UnsupportedDefinition.SYNCHRONOUS,
            lineno=5,
        ),
    ]
)
