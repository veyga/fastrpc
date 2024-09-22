from dataclasses import dataclass, fields
from pathlib import Path


def _prettyprint(cls):
    def __str__(self):
        field_values = ", ".join(
            f"{field.name}={getattr(self, field.name)}" for field in fields(self)
        )
        return f"{self.__class__.__name__}({field_values})"

    cls.__str__ = __str__
    return cls


@dataclass
class CodeGenException(Exception):
    path: Path
    lineno: int
    msg: str


@_prettyprint
@dataclass
class DuplicatedNameException(CodeGenException): ...


@_prettyprint
@dataclass
class SynchronousProcedureException(CodeGenException): ...


@_prettyprint
@dataclass
class UntypedDefinitionException(CodeGenException): ...
