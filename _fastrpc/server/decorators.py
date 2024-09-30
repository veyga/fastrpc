from functools import wraps
from pydantic.dataclasses import dataclass as fastrpc_type
from typing import (
    Callable,
    Coroutine,
    ParamSpec,
    TypeVar,
)

_Params = ParamSpec("_Params")
_A = TypeVar("_A")
_B = TypeVar("_B")
_R = TypeVar("_R", covariant=True)


def fastrpc_procedure(
    function: Callable[_Params, Coroutine[_A, _B, _R]],
) -> Callable[_Params, Coroutine[_A, _B, _R]]:
    """Marks a function as transformable via fastrpc"""

    @wraps(function)
    async def decorator(*args, **kwargs) -> _R:
        return await function(*args, **kwargs)

    return decorator


__all__ = [
    "fastrpc_procedure",
    "fastrpc_type",
]
