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


class UnsupportedProcedure(StrEnum):
    METHOD = "methods"
    NESTED = "nested function"
    OBSCURED = "obscured defintion (ex: __fn)"
    RETURN_NONE = "procedure returning None"
    SYNCHRONOUS = "synchronous (non-async)"
    _NA = "N/A"


class UnsupportedParameter(StrEnum):
    ARGS = "*args defined"
    CUSTOM_TYPE = "type not @remote_procedure_parameter/BaseModel"
    KWARGS = "**kwargs defined"
    KWONLY = "*, defined (keyword only)"
    UNTYPED = "untyped (not annotated)"


@prettyprint
@dataclass
class UnsupportedException(CodeGenException):
    path: Path = Path(__file__)
    reason: UnsupportedProcedure | UnsupportedParameter = UnsupportedProcedure._NA
    lineno: int = -1
    symbol: str = ""
