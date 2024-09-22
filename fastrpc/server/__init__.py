import ast
import subprocess
from dataclasses import dataclass
from fastrpc.server.decorators import remote_procedure
from pathlib import Path
from typing import TypedDict
from returns.result import safe, Success, Failure
from .exceptions import CodeGenException, DuplicatedNameException


@dataclass
class _RemoteProcedure:
    module: Path
    fn: ast.AsyncFunctionDef


class _RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: _RemoteProcedure


class _RemoteProcedureVisitor(ast.NodeVisitor):
    def visit_AsyncFunctionDef(self, node):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        # check name is not already taken
                        if existing := self.matches.get(node.name):
                            raise DuplicatedNameException(
                                path=self.filepath,
                                lineno=node.lineno,
                                msg=(
                                    f"The remote_procedure name {node.name}"
                                    f"is already assigned in {existing.module}"
                                ),
                            )
                        else:
                            self.matches[node.name] = _RemoteProcedure(
                                self.filepath, node
                            )

        # Continue visiting other nodes
        self.generic_visit(node)

    def set_context(self, matches, filepath):
        self.matches = matches
        self.filepath = filepath


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
