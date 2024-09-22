from fastrpc.server.decorators import remote_procedure


@remote_procedure
async def rp_1(*args) -> str:
    print(args)
    return ""


@remote_procedure
async def rp_2(**kwargs) -> str:
    print(kwargs)
    return ""


@remote_procedure
async def rp_3(x: str, *xs, **ys) -> str:
    print(x, xs, ys)
    return ""
