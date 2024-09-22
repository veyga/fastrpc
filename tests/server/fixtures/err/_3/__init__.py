"""
Obscured not supported
"""

from fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(definition=UnsupportedDefinition.OBSCURED)
