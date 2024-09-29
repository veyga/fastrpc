"""args/kwargs parameters not supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedParameter,
    UnsupportedException,
)

path = Path(__file__).parent / "source.py"
EXPECTED = CodeGenExceptions(
    [
        UnsupportedException(
            reason=UnsupportedParameter.ARGS,
            path=path,
            lineno=5,
            symbol="args",
        ),
        # UnsupportedException(
        #     reason=UnsupportedParameter.KWARGS,
        #     path=path,
        #     lineno=11,
        #     symbol="kwargs",
        # ),
        # UnsupportedException(
        #     reason=UnsupportedParameter.ARGS,
        #     path=path,
        #     lineno=17,
        #     symbol="xs",
        # ),
        # UnsupportedException(
        #     reason=UnsupportedParameter.KWARGS,
        #     path=path,
        #     lineno=17,
        #     symbol="ys",
        # ),
    ]
)
