# Why am I getting the following error when throwing an UnsupportedDefinitionException:
#   TypeError: catching classes that do not inherit from BaseException is not allowed

# Here is my source code:

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from textwrap import dedent


class UnsupportedDefinition(StrEnum):
    SYNCHRONOUS = "synchronous (non-async)"
    OBSCURED = "obscured defintion (ex: __fn)"
    NESTED = "nested function"
    METHOD = "methods"
    UNTYPED_ARGUMENTS = "untyped procedure arguments"
    UNTYPED_RETURN = "untyped procedure return type"
    NONE_RETURN = "procedure returning None"
    _NA = "N/A"


@dataclass(init=False)
class CodeGenException(Exception): ...


@dataclass
class CodeGenExceptions(Exception):
    exceptions: list[CodeGenException]


@dataclass
class DuplicatedNameException(CodeGenException):
    path: Path = Path(__file__)
    lineno: int = -1
    name: str = ""
    existing: Path = Path(__file__)

    def __str__(self) -> str:
        message = (
            f"@remote_procedure with name '{self.name}' already assigned."
            f"[see {self.existing}]"
        )
        return dedent(
            f"""
          DuplicatedNameException(
            path={self.path},
            lineno={self.lineno},
            msg={message}
          )
          """
        ).strip()


@dataclass
class UnsupportedDefinitionException(CodeGenException):
    path: Path = Path(__file__)
    lineno: int = -1
    definition: UnsupportedDefinition = UnsupportedDefinition._NA

    def __str__(self) -> str:
        message = (
            "@remote_procedure is decorating an invalid/incomplete definition."
            f"[{self.definition}]"
        )
        return dedent(
            f"""
          UnsupportedDefinitionException(
            path={self.path},
            lineno={self.lineno},
            msg={message}
          )
          """
        ).strip()
