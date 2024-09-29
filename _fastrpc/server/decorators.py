from functools import wraps
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


def remote_procedure(
    function: Callable[_Params, Coroutine[_A, _B, _R]],
) -> Callable[_Params, _R]:
    """Marks a function as a remote_procedure"""

    async def factory(*args: _Params.args, **kwargs: _Params.kwargs) -> _R:
        return await function(*args, **kwargs)

    @wraps(function)
    def decorator(*args, **kwargs):
        return factory(*args, **kwargs)

    return decorator


__all__ = [
    "remote_procedure",
]
