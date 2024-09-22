"""
Methods not yet supported
"""

EXPECTED = frozenset(("API___rp_1",))

from fastrpc.server.decorators import remote_procedure


class API:

    @remote_procedure
    async def rp_1(self): ...
