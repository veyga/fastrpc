from dataclasses import dataclass
from typing import Callable
from returns.future import FutureResultE


@dataclass
class Ok[T]:
    value: T


@dataclass
class Err[E]:
    exception: E


type RpcResult[T] = Ok[T] | Err[T]
type RPC[**A, B] = Callable[A, RpcResult[B]]


def apply_context[**A, B, Ctx](context: Ctx) -> RPC[[A], B]:
    def apply(rpc) -> RpcResult[B]:
        return rpc(context)

    return apply


__all__ = [
    "RPC",
    "Ok",
    "Err",
    "apply_context",
]
