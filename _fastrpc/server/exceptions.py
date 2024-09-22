# Why am I getting the following error when throwing an UnsupportedDefinitionException:
#   TypeError: catching classes that do not inherit from BaseException is not allowed

# Here is my source code:

from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path
from textwrap import dedent


def prettyprint(cls):
    def __str__(self):
        field_values = "\n".join(
            f"\t{field.name}={getattr(self, field.name)}," for field in fields(self)
        )
        return f"{self.__class__.__name__}(\n{field_values}\n)"

    cls.__str__ = __str__
    return cls


@dataclass(init=False)
class CodeGenException(Exception): ...


@dataclass
class CodeGenExceptions(Exception):
    exceptions: list[CodeGenException]


@prettyprint
@dataclass
class DuplicatedNameException(CodeGenException):
    path: Path = Path(__file__)
    lineno: int = -1
    name: str = ""
    conflicting_module: Path = Path(__file__)


class UnsupportedDefinition(StrEnum):
    SYNCHRONOUS = "synchronous (non-async)"
    OBSCURED = "obscured defintion (ex: __fn)"
    NESTED = "nested function"
    METHOD = "methods"
    NONE_RETURN = "procedure returning None"
    ARGS_LIST = "procedure defining *args"
    KWARGS_LIST = "procedure defining **kargs"
    _NA = "N/A"


@prettyprint
@dataclass
class UnsupportedDefinitionException(CodeGenException):
    path: Path = Path(__file__)
    lineno: int = -1
    definition: UnsupportedDefinition = UnsupportedDefinition._NA


class UnsupportedParameter(StrEnum):
    UNTYPED = "untyped (not annotated)"
    ARGS = "*args"
    KWARGS = "**kwargs"
    _NA = "N/A"


@prettyprint
@dataclass
class UnsupportedParameterException(CodeGenException):
    path: Path = Path(__file__)
    lineno: int = -1
    definition: UnsupportedParameter = UnsupportedParameter._NA
    symbol: str = ""


# @prettyprint
# @dataclass
# class UntypedParameterException(CodeGenException):
#     path: Path = Path(__file__)
#     lineno: int = -1
#     parameter: str = ""

# def __str__(self) -> str:
#     message = "@remote_procedure is decorating an invalid/incomplete definition."
#     return dedent(
#         f"""
#       UntypedParameterException(
#         msg={message}\n
#         path={self.path}\n,
#         lineno={self.lineno}\n,
#         parameter={self.parameter}\n
#       )
#       """
#     ).strip()


# def __str__(self) -> str:
#     message = "@remote_procedure is decorating an invalid/incomplete definition."
#     return dedent(
#         f"""
#       UntypedParameterException(
#         msg={message}\n
#         path={self.path}\n,
#         lineno={self.lineno}\n,
#         parameter={self.parameter}\n
#       )
#       """
#     ).strip()


# def __str__(self) -> str:
#     message = (
#         f"@remote_procedure with name '{self.name}' already assigned."
#         f"[see {self.existing}]"
#     )
#     return dedent(
#         f"""
#       DuplicatedNameException(
#         path={self.path},
#         lineno={self.lineno},
#         msg={message}
#         self
#       )
#       """
#     ).strip()

# def __str__(self) -> str:
#     # message = (
#     #     "@remote_procedure is decorating an invalid/incomplete definition."
#     #     f"[{self.definition}]"
#     # )
#     return dedent(
#         f"""
#       UnsupportedDefinitionException(
#         path={self.path}\n,
#         lineno={self.lineno}\n,
#         definition={self.definition}\n,
#       )
#       """
#     ).strip()
