import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypedDict, Protocol, TypeVar

# from fastrpc.server import remote_procedure_context


@dataclass
class RemoteProcedure:
    module: Path
    name: str
    fn: ast.AsyncFunctionDef


# @remote_procedure_context
class Context(Protocol):
    pass


class ContextHandler[Context](Protocol):
    def __call__(self, context: Context) -> None: ...


""" 
A function which intercepts Context for remote procedures.
Useful for protecting routes, validation, side effects, etc.

Context handlers must accept a single context parameter

EXAMPLE:
class TokenContext(Context):
  token: str

def token_validator(ctx: TokenContext):
  if ctx['token'] != "valid_token":
    raise ValueError("Invalid token")

@remote_procedure(
    context_handler=my_context_handler,
)
def echo(x: str) -> str:
  return x
"""


class RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: RemoteProcedure


# TODO maybe run mypy on stuff instead of trying to manually typecheck

__all__ = [
    "Context",
    "ContextHandler",
]
