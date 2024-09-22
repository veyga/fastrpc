"""
Inner functions not yet supported
"""

EXPECTED = frozenset(
    (
        "rp_1__inner",
        "rp_2__inner",
    )
)

from fastrpc.server.decorators import remote_procedure


def rp_1():

    @remote_procedure
    async def inner(): ...
