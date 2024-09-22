import ast
from dataclasses import dataclass, replace
from enum import StrEnum
from fastrpc.server.decorators import remote_procedure
from functools import partial
from pathlib import Path
from returns.result import safe, Success, Failure
from textwrap import dedent
from typing import TypedDict
from .exceptions import (
    DuplicatedNameException,
    UnsupportedDefinitionException,
    UnsupportedDefinition,
)


@dataclass
class _RemoteProcedure:
    module: Path
    fn: ast.AsyncFunctionDef


class _RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: _RemoteProcedure


class _RemoteProcedureVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
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

    def visit_AsyncFunctionDef(self, node):
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
                            e = replace(
                                exception, definition=UnsupportedDefinition.OBSCURED
                            )
                            raise e
                        else:
                            self.matches[node.name] = _RemoteProcedure(
                                self.filepath, node
                            )

        # Continue visiting other nodes
        self.generic_visit(node)

    def set_context(self, matches, filepath):
        self.matches = matches
        self.filepath = filepath


@safe
def _resolve_remote_procedures(src_root: Path) -> _RemoteProcedureMap:
    matches: _RemoteProcedureMap = {}
    for py_file in src_root.rglob("*.py"):
        with open(py_file, "r") as file:
            module: ast.Module = ast.parse(file.read(), filename=str(py_file))
            visitor = _RemoteProcedureVisitor()
            visitor.set_context(matches, py_file)
            visitor.visit(module)
    return matches


def create(src_root: str = "src"):
    """
    Walks a directory tree from src_root looking for @remote_procedure
    """
    if not (path := Path(src_root)).exists():
        raise ValueError(f"src_root ({src_root}) DNE")
    matches = _resolve_remote_procedures(path)
    print(matches)
