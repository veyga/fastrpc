from dataclasses import dataclass
from typing import Callable, Awaitable


@dataclass(frozen=True)
class Ok[T]:
    value: T


@dataclass(frozen=True)
class Err:
    exception: Exception


type RpcResult[T] = Ok[T] | Err

type RPC[**Ctx, R] = Callable[Ctx, Awaitable[RpcResult[R]]]


def as_rpc_result(coroutine):
    """
    Safely call a coroutine and wrap the result as an RpcResult
    """

    async def wrapper(*args, **kwargs):
        try:
            value = await coroutine(*args, **kwargs)
            return Ok(value=value)
        except Exception as e:
            return Err(exception=e)

    return wrapper


type _ContextApply[Ctx, R] = Callable[[RPC[[Ctx], R]], Awaitable[RpcResult[R]]]


def apply_context[Ctx, R](context: Ctx) -> _ContextApply[Ctx, R]:
    """
    Apply a context object to a remote procedures which require it

    Example:
    WITHOUT:
    doubled_x= await double_it(x=4)(TokenContext(token="invalid"))

    WITH:
    use_token_context = apply_context(TokenContext("valid"))
    doubled_x = await use_token_context(double_it(x=4))
    tripled_x = await use_token_context(triple_it(x=4))

    """

    def apply(rpc: RPC[[Ctx], R]) -> Awaitable[RpcResult[R]]:
        return rpc(context)

    return apply


__all__ = [
    "RPC",
    "Ok",
    "Err",
    "to_rpc_result",
    "apply_context",
]
