"""Methods not yet supported"""

from pathlib import Path

from _fastrpc.server.exceptions import (
    CodeGenExceptions,
    UnsupportedProcedure,
    UnsupportedException,
)

EXPECTED = CodeGenExceptions(
    [
        UnsupportedException(
            path=Path(__file__).parent / "source.py",
            reason=UnsupportedProcedure.METHOD,
            lineno=7,
            symbol="rp_1",
        ),
    ]
)
