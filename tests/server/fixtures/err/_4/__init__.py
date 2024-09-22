"""
Nested functions not yet supported
"""

from fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(definition=UnsupportedDefinition.NESTED)
