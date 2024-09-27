from typing import Tuple

from fastrpc.server import remote_procedure
from fastrpc.server import remote_procedure_parameter
from dataclasses import dataclass


@remote_procedure
async def rp_1(x) -> str:
    return x


@remote_procedure
async def rp_2(x, y) -> Tuple[str, str]:
    return x, y


@remote_procedure
async def rp_3(x: str, y) -> Tuple[str, str]:
    return x, y


# @remote_procedure_interceptor("asdf")


@remote_procedure
async def rp_4(
    x: str,
    y: str,
    z,
) -> Tuple[str, str, str]:
    return x, y, z


# @dataclass
# class Name:
#   first: str
#   last: str

# async def rp_5(name: Name) -> str:
#   return f"{name.first} {name.last}"
