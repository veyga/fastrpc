from fastrpc.server import remote_procedure


@remote_procedure()
async def rp_1() -> str:
    return ""
