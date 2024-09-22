import ast
from dataclasses import dataclass, replace
from pathlib import Path
from returns.result import safe
from typing import TypedDict
from _fastrpc.server.decorators import remote_procedure
from .exceptions import (
    DuplicatedNameException,
    UnsupportedDefinitionException,
    UnsupportedDefinition,
)


@dataclass
class RemoteProcedure:
    module: Path
    fn: ast.AsyncFunctionDef


class RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: RemoteProcedure


class RemoteProcedureVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        e = UnsupportedDefinitionException(
                            definition=UnsupportedDefinition.SYNCHRONOUS,
                            path=self.filepath,
                            lineno=node.lineno,
                        )
                        raise e

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        if existing := self.matches.get(node.name):
                            raise DuplicatedNameException(
                                path=self.filepath,
                                lineno=node.lineno,
                                name=node.name,
                                existing=existing.module,
                            )
                        exception = UnsupportedDefinitionException(
                            path=self.filepath,
                            lineno=node.lineno,
                        )
                        if node.name.startswith("__"):
                            raise replace(
                                exception, definition=UnsupportedDefinition.OBSCURED
                            )
                        else:
                            self.matches[node.name] = RemoteProcedure(
                                self.filepath, node
                            )

        # Continue visiting other nodes
        self.generic_visit(node)

    def set_context(self, matches: RemoteProcedureMap, filepath: Path):
        self.matches = matches
        self.filepath = filepath


@safe
def resolve_remote_procedures(src_root: str) -> RemoteProcedureMap:
    if not (path := Path(src_root)).exists():
        raise ValueError(f"src_root ({src_root}) DNE")
    matches: RemoteProcedureMap = {}
    for py_file in path.rglob("*.py"):
        with open(py_file, "r") as file:
            module: ast.Module = ast.parse(file.read(), filename=str(py_file))
            visitor = RemoteProcedureVisitor()
            visitor.set_context(matches, py_file)
            visitor.visit(module)
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
