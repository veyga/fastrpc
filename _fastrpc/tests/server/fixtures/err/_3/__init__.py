"""Obscured not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = [
    UnsupportedDefinitionException(
        path=Path(__file__).parent / "source.py",
        definition=UnsupportedDefinition.OBSCURED,
        lineno=5,
    ),
]
