"""Decorated non-async function"""

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)
from pathlib import Path

EXPECTED = [
    UnsupportedDefinitionException(
        path=Path(__file__).parent / "source.py",
        definition=UnsupportedDefinition.SYNCHRONOUS,
        lineno=5,
    ),
]
