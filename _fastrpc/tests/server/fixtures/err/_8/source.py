from fastrpc.server.decorators import remote_procedure
from typing import Tuple


@remote_procedure
async def rp_1(x) -> str:
    return x


@remote_procedure
async def rp_2(x, y) -> Tuple[str, str]:
    return x, y


@remote_procedure
async def rp_3(x: str, y) -> Tuple[str, str]:
    return x, y
