# from .server import TokenContext
from dataclasses import dataclass
from fastrpc import remote_procedure_type
from fastrpc.client import RPC, Ok, Err
from returns.io import IOSuccess, IOFailure
from returns.result import Success, Failure
from returns.future import future_safe, FutureResultE
from .server.contexts import TokenContext as ServerTokenContext, token_validator
from .server.endpoints import (
    double_it as server_double_it,
    triple_it as server_triple_it,
)

TokenContext = ServerTokenContext
# @remote_procedure_type
# class TokenContext:
#     token: str


async def to_rpc_result(future):
    result = await future
    match result:
        case IOSuccess(Success(v)):
            return Ok(v)
        case IOSuccess(Failure(e)) | IOFailure(Success(e)) | IOFailure(Failure(e)):
            return Err(e)
        case e:
            return Err(e)


##### CLIENT CODEGEN
def double_it(*, x: int) -> RPC[[TokenContext], int]:
    def inner(context: TokenContext):
        @future_safe
        async def call_it():
            token_validator(context)
            y = await server_double_it(x)
            return y

        rax = to_rpc_result(call_it())
        return rax

    return inner


def triple_it(*, x: int) -> RPC[[TokenContext], int]:
    def inner(context: TokenContext):
        @future_safe
        async def call_it():
            token_validator(context)
            y = await server_triple_it(x)
            return y

        rax = to_rpc_result(call_it())
        return rax

    return inner


# def double_it_no_ctx(x: int) -> FutureResultE[int]:
#     @future_safe
#     async def call_it():
#         return x * 44

#     return call_it()

__all__ = [
    "TokenContext",
    "double_it",
    "triple_it",
]
