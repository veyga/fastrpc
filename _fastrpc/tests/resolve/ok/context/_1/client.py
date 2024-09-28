from fastrpc.client import RPC, as_rpc_result
from .server.contexts import TokenContext as ServerTokenContext, token_validator
from .server.endpoints import (
    double_it as server_double_it,
)

TokenContext = ServerTokenContext
# @remote_procedure_type
# class TokenContext:
#     token: str


##### CLIENT CODEGEN
def double_it(*, x: int) -> RPC[[TokenContext], int]:
    def inner(context: TokenContext):
        async def call_it():
            token_validator(context)
            return await server_double_it(x)

        return as_rpc_result(call_it)()

    return inner


# def triple_it(*, x: int) -> RPC[[TokenContext], int]:
#     def inner(context: TokenContext):
#         @future_safe
#         async def call_it():
#             token_validator(context)
#             y = await server_triple_it(x)
#             return y

#         rax = to_rpc_result(call_it())
#         return rax

#     return inner


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
