from typing import Callable
from returns.future import FutureResultE

type RPC[**A, B] = Callable[A, FutureResultE[B]]


def apply_context[**A, B, Ctx](context: Ctx) -> RPC[[A], B]:
    def apply(rpc) -> FutureResultE[B]:
        return rpc(context)

    return apply


__all__ = [
    "RPC",
    "apply_context",
]
