from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path


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


class UnsupportedParameter(StrEnum):
    UNTYPED = "untyped (not annotated)"
    ARGS = "*args defined"
    KWARGS = "**kwargs defined"


@dataclass
class UnsupportedException(CodeGenException):
    path: Path = Path(__file__)
    reason: UnsupportedDefinition | UnsupportedParameter = UnsupportedDefinition._NA
    lineno: int = -1
    symbol: str = ""
