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
    _NA = "N/A"


@dataclass
class DuplicatedNameException(Exception):
    path: Path = Path(__file__)
    lineno: int = 0
    conflict: str = "TBD"


@dataclass
class UnsupportedDefinitionException(Exception):
    path: Path = Path(__file__)
    lineno: int = 0
    definition: UnsupportedDefinition = UnsupportedDefinition._NA

    def __str__(self) -> str:
        message = (
            "@remote_procedure is decorating an invalid/incomplete definition."
            f"\t[{self.definition}]"
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
