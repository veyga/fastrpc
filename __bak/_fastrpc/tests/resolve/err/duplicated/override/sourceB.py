from fastrpc.server import remote_procedure


@remote_procedure(name_override="myfn")
async def myfn() -> str:
    return ""
