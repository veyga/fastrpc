"""Untyped return not supported"""

from _fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(
    definition=UnsupportedDefinition.UNTYPED_RETURN
)
