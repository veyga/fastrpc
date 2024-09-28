from functools import wraps, partial
from typing import (
    Callable,
    Coroutine,
    Optional,
    ParamSpec,
    TypeVar,
)
from .types import ContextHandler

_Params = ParamSpec("_Params")
_A = TypeVar("_A")
_B = TypeVar("_B")
_R = TypeVar("_R", covariant=True)


def remote_procedure(
    *, name_override: Optional[str] = None, context_handler: Optional = None
):
    """
    Marks a function as a remote_procedure
    """

    def inner(
        function: Callable[_Params, Coroutine[_A, _B, _R]],
    ) -> Callable[_Params, _R]:
        # Globally unique 'name' allows for moving/renaming functions

        async def factory(*args: _Params.args, **kwargs: _Params.kwargs) -> _R:
            return await function(*args, **kwargs)

        @wraps(function)
        def decorator(*args, **kwargs):
            return factory(*args, **kwargs)

        return decorator

    return inner


def use_context_handler(context_handler: ContextHandler):
    """
    protected = use_handler(token_validator)

    @protected()
    async def protected_double_it(x: int) -> int:
        return x * 2
    """

    return partial(remote_procedure, context_handler=context_handler)


__all__ = [
    "remote_procedure",
    "use_context_handler",
]
