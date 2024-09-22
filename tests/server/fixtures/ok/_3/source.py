from fastrpc.server.decorators import remote_procedure


@remote_procedure
async def rp_1(): ...


@remote_procedure
async def rp_2(): ...
