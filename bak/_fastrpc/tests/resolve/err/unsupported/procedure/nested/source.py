from fastrpc.server import remote_procedure


def rp_1():

    @remote_procedure
    async def rp_1_inner() -> str:
        return ""
