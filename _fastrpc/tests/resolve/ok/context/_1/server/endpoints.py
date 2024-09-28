from fastrpc.server import (
    remote_procedure,
    use_context_handler,
)
from .contexts import token_validator


@remote_procedure(context_handler=token_validator)
async def double_it(x: int) -> int:
    return x * 2


@remote_procedure(context_handler=token_validator)
async def triple_it(x: int) -> int:
    return x * 3


# @remote_procedure()
# async def double_it_no_ctx(x: int) -> int:
#     return x * 2


# requires_valid_token = use_context_handler(token_validator)


# @requires_valid_token()
# async def protected_double_it(x: int) -> int:
#     return x * 2
