from fastrpc.server.decorators import remote_procedure


def rp_1():

    @remote_procedure
    async def inner(): ...
