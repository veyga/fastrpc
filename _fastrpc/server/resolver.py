import ast
from pathlib import Path
from _fastrpc.server.decorators import remote_procedure
from .exceptions import (
    DuplicatedNameException,
    UnsupportedProcedure as UProc,
    UnsupportedParameter as UParam,
    UnsupportedException,
)
from .types import RemoteProcedureMap, RemoteProcedure


class RemoteProcedureResolver(ast.NodeVisitor):
    def err(self, reason, lineno, symbol):
        self.exceptions.append(
            UnsupportedException(
                path=self.filepath,
                reason=reason,
                lineno=lineno,
                symbol=symbol,
            )
        )

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        self.err(UProc.SYNCHRONOUS, node.lineno, node.name)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        if existing := self.matches.get(node.name):
                            self.exceptions.append(
                                DuplicatedNameException(
                                    path=self.filepath,
                                    lineno=node.lineno,
                                    name=node.name,
                                    conflicting_module=existing.module,
                                )
                            )
                            return
                        if node.name.startswith("__"):
                            self.err(UProc.OBSCURED, node.lineno, node.name)
                        if node.returns is None:
                            self.err(UProc.RETURN_NONE, node.lineno, node.name)
                        if (
                            hasattr(node.returns, "value")
                            and node.returns.value is None
                        ):
                            self.err(UProc.RETURN_NONE, node.lineno, node.name)
                        if args := node.args.vararg:
                            self.err(UParam.ARGS, args.lineno, args.arg)
                        if kwargs := node.args.kwarg:
                            self.err(UParam.KWARGS, kwargs.lineno, kwargs.arg)
                        if args := node.args.args:
                            for a in args:
                                if not a.annotation:
                                    self.err(UParam.UNTYPED, a.lineno, a.arg)
                        if not self.exceptions:
                            self.matches[node.name] = RemoteProcedure(
                                self.filepath, node
                            )

        # Continue visiting other nodes
        self.generic_visit(node)

    def set_context(
        self, exceptions: list, matches: RemoteProcedureMap, filepath: Path
    ):
        self.exceptions = exceptions
        self.matches = matches
        self.filepath = filepath
