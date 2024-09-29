from fastrpc.server import remote_procedure


@remote_procedure(name_override="myfn22")
async def rp_1() -> str:
    return ""
