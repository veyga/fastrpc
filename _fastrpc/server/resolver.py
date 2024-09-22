import ast
from pathlib import Path
from _fastrpc.server.decorators import remote_procedure
from .exceptions import (
    DuplicatedNameException,
    UnsupportedDefinitionException,
    UnsupportedDefinition,
    UnsupportedParameterException,
    UnsupportedParameter,
)
from .types import RemoteProcedureMap, RemoteProcedure


class RemoteProcedureResolver(ast.NodeVisitor):
    def err_def(self, node, definition):
        self.exceptions.append(
            UnsupportedDefinitionException(
                path=self.filepath,
                lineno=node.lineno,
                definition=definition,
            )
        )

    def err_param(self, definition, lineno, symbol):
        self.exceptions.append(
            UnsupportedParameterException(
                path=self.filepath,
                lineno=lineno,
                definition=definition,
                symbol=symbol,
            )
        )

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for decorator in node.decorator_list:
            match decorator:
                case ast.Name():
                    if decorator.id == remote_procedure.__name__:
                        self.err_def(node, UnsupportedDefinition.SYNCHRONOUS)

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
                            self.err_def(node, UnsupportedDefinition.OBSCURED)
                        if node.returns is None:
                            self.err_def(node, UnsupportedDefinition.NONE_RETURN)
                        if (
                            hasattr(node.returns, "value")
                            and node.returns.value is None
                        ):
                            self.err_def(node, UnsupportedDefinition.NONE_RETURN)
                        if args := node.args.vararg:
                            self.err_param(
                                UnsupportedParameter.ARGS,
                                lineno=args.lineno,
                                symbol=args.arg,
                            )
                        if kwargs := node.args.kwarg:
                            self.err_param(
                                UnsupportedParameter.KWARGS,
                                lineno=kwargs.lineno,
                                symbol=kwargs.arg,
                            )
                        if args := node.args.args:
                            for arg in args:
                                if not arg.annotation:
                                    self.err_param(
                                        UnsupportedParameter.UNTYPED,
                                        lineno=arg.lineno,
                                        symbol=arg.arg,
                                    )
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
