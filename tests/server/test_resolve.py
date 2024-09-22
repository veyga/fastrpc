import os
import pytest
import sys
from fastrpc.server import _resolve_remote_procedures
from importlib import import_module
from parametrization import Parametrization as P
from pathlib import Path
from types import SimpleNamespace as ___


Case = lambda s: P.case(name=s, fix=s)


@pytest.fixture
def add_path():
    def inner(dir, fix):
        # original_sys_path = sys.path.copy()
        print(f"INSERTING PATH {dir}")
        path = Path(__file__).parent / "fixtures" / dir
        sys.path.insert(0, str(path / fix))
        yield
        sys.path.pop(0)

    return inner


@P.autodetect_parameters()
@Case("_1")
def test_ok(fix):
    sys.path.insert(0, str(Path(__file__).parent / "fixtures" / "ok"))
    module = import_module(fix)
    print(module)
    sys.path.pop(0)
