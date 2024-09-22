from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeGenException(Exception):
    path: Path
    lineno: int
    msg: str


@dataclass
class DuplicatedNameException(CodeGenException):
    def __str__(self):
        return f"DuplicateNameException({self.path}::{self.lineno}\n{self.msg}"


@dataclass
class SynchronousProcedureException(CodeGenException):
    pass


@dataclass
class UntypedDefinitionException(CodeGenException):
    pass
