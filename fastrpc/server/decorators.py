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
    """
    Marker decorator to declare that a function is a remote_procedure
    (Marked functions must have a unique name)
    """
    # Globally unique 'name' allows for moving/renaming functions

    async def factory(*args: _Params.args, **kwargs: _Params.kwargs) -> _R:
        return await function(*args, **kwargs)

    @wraps(function)
    def decorator(*args, **kwargs):
        return factory(*args, **kwargs)

    return decorator
