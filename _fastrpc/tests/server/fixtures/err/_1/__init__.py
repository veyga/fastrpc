"""Decorated non-async function"""

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(definition=UnsupportedDefinition.SYNCHRONOUS)
