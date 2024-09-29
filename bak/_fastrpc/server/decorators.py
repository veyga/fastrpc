from functools import wraps, partial
from abc import ABC, abstractmethod
from typing import (
    Callable,
    Coroutine,
    Iterable,
    Optional,
    ParamSpec,
    TypeVar,
    Type,
    final,
)
from .types import ContextHandler

_Params = ParamSpec("_Params")
_A = TypeVar("_A")
_B = TypeVar("_B")
_R = TypeVar("_R", covariant=True)


def remote_procedure(
    *, name_override: Optional[str] = None, context_handler: Optional[Callable] = None
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


type Requires = Optional[Iterable[Type]]


def remote_procedure_class(*, requires: Requires = None):
    def inner(cls: type):
        @final
        class RemoteProcedureClass[T](cls, ABC):
            def __init__(self):
                super(RemoteProcedureClass, self).__init__()

            @abstractmethod
            def ___(self): ...

        return RemoteProcedureClass[cls]

    return inner


def remote_method(*, requires: Optional[Iterable[Type]] = None):
    def inner(fn):
        def wrapper(instance, *args, **kwargs):
            if requires:
                for d in requires:
                    setattr(instance, str(d), d)
            return fn(instance, *args, **kwargs)

        return wrapper

    return inner


tags = ["A1", "A2", "B1"]

__all__ = [
    "remote_procedure",
    "remote_procedure_class",
    "remote_method",
    "use_context_handler",
]
