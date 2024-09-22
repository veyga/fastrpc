from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeGenException(Exception):
    path: Path
    lineno: int
    msg: str


@dataclass
class DuplicatedNameException(CodeGenException):
    pass


@dataclass
class SynchronousProcedureException(CodeGenException):
    pass


@dataclass
class UntypedDefinitionException(CodeGenException):
    pass
