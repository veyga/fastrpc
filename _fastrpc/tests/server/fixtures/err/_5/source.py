from fastrpc.server.decorators import remote_procedure


class API:

    @remote_procedure
    async def rp_1(self): ...
