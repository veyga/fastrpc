from fastrpc.server.decorators import remote_procedure


@remote_procedure
async def rp_1(*xs) -> str:
    print(xs)
    return ""


# @remote_procedure
# async def rp_2(**ys) -> str:
#     print(ys)
#     return ""


# @remote_procedure
# async def rp_3(*xs, **ys) -> str:
#     print(xs, ys)
#     return ""
