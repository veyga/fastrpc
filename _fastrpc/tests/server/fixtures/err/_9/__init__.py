"""args/kwargs parameters not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedParameter,
    UnsupportedParameterException,
    UnsupportedParameterException,
)

path = Path(__file__).parent / "source.py"
EXPECTED = CodeGenExceptions(
    [
        UnsupportedParameterException(
            path=path,
            lineno=5,
            symbol="args",
            definition=UnsupportedParameter.ARGS,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=11,
            symbol="kwargs",
            definition=UnsupportedParameter.KWARGS,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=17,
            symbol="xs",
            definition=UnsupportedParameter.ARGS,
        ),
        UnsupportedParameterException(
            path=path,
            lineno=17,
            symbol="ys",
            definition=UnsupportedParameter.KWARGS,
        ),
    ]
)
