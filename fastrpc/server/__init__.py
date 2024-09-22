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
    fn: ast.FunctionDef


class _RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: _RemoteProcedure


class _RemoteProcedureVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # Check if the function has decorators
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        # check function is async
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


def _resolve_remote_procedures(filepath: Path) -> _RemoteProcedureMap:
    matches: _RemoteProcedureMap = {}
    with open(filepath, "r") as file:
        tree: ast.Module = ast.parse(file.read(), filename=str(filepath))
        visitor = _RemoteProcedureVisitor()
        visitor.set_context(matches, filepath)  # Set the filename for error reporting
        visitor.visit(tree)
    return matches


def create(src_root: str = "src"):
    """
    Walks a directory tree from src_root looking for @remote_procedure
    """
    if not (path := Path(src_root)).exists():
        raise ValueError(f"src_root ({src_root}) DNE")
    for py_file in path.rglob("*.py"):
        # TODO should mypy run on files with endpoints?
        result = _resolve_remote_procedures(py_file)
