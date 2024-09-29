import ast
from pathlib import Path
from returns.result import safe
from .exceptions import (
    CodeGenExceptions,
)
from .types import RemoteProcedureMap
from .resolver import RemoteProcedureResolver


@safe
def resolve_remote_procedures(src_root: str) -> RemoteProcedureMap:
    if not (path := Path(src_root)).exists():
        raise ValueError(f"src_root ({src_root}) DNE")
    matches: RemoteProcedureMap = {}
    exceptions = []
    for py_file in path.rglob("*.py"):
        with open(py_file, "r") as file:
            module: ast.Module = ast.parse(file.read(), filename=str(py_file))
            visitor = RemoteProcedureResolver()
            visitor.set_context(exceptions, matches, py_file)
            visitor.visit(module)
    if exceptions:
        raise CodeGenExceptions(exceptions)
    return matches


def create(src_root: str = "src"):
    """
    Walks a directory tree from src_root looking for @remote_procedure
    """
    result = resolve_remote_procedures(src_root)
    print(result)


__all__ = [
    "create",
]
