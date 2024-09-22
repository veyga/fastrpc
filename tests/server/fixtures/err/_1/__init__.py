"""
Decorated non-async function
"""

from fastrpc.server.exceptions import (
    UnsupportedDefinition,
    UnsupportedDefinitionException,
)

EXPECTED = UnsupportedDefinitionException(definition=UnsupportedDefinition.SYNCHRONOUS)
