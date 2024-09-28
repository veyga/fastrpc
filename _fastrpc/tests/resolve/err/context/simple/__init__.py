""""""

from pathlib import Path

from _fastrpc.server.exceptions import CodeGenExceptions, ContextException

parent = Path(__file__).parent

EXPECTED = CodeGenExceptions(
    [
        ContextException(
            path=parent / "sourceA.py",
            lineno=5,
            name="rp_1",
        ),
    ]
)
