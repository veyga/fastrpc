import ast
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


@dataclass
class RemoteProcedure:
    module: Path
    fn: ast.AsyncFunctionDef


class RemoteProcedureMap(TypedDict):
    name: str
    remote_procedure: RemoteProcedure
