"""Nested functions not yet supported"""

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(definition=UnsupportedDefinition.NESTED)
