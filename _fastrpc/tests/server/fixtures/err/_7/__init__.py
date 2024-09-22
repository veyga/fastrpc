"""Untyped args not supported, single arg"""

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = [
    UnsupportedDefinitionException(definition=UnsupportedDefinition.UNTYPED_ARGUMENTS),
    UnsupportedDefinitionException(definition=UnsupportedDefinition.UNTYPED_ARGUMENTS),
    UnsupportedDefinitionException(definition=UnsupportedDefinition.UNTYPED_ARGUMENTS),
]
