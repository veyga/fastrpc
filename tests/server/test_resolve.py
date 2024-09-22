import pytest
import sys
from enum import StrEnum
from fastrpc.server import _resolve_remote_procedures
from fastrpc.server.exceptions import UnsupportedDefinitionException
from importlib import import_module
from parametrization import Parametrization as P
from pathlib import Path
from returns.result import Success, Failure


FIX_PATH = Path(__file__).parent / "fixtures"


Case = lambda fix: P.case(name=fix, fix=fix)


@P.autodetect_parameters()
@Case("_1")
@Case("_2")
@Case("_3")
def test_ok(fix):
    path = FIX_PATH / "ok"
    sys.path.insert(0, str(path))
    try:
        module = import_module(fix)
        if fix in sys.modules:  # avoid module caching
            if "fastrpc" in str(module):
                del sys.modules[fix]
                module = import_module(fix)

        match _resolve_remote_procedures(path / fix):
            case Success(mapp):
                assert frozenset(mapp.keys()) == module.EXPECTED
            case Failure(e):
                pytest.fail(f"Expected {module.EXPECTED}, {e} raised")

    finally:
        sys.path.pop(0)


@P.autodetect_parameters()
@Case("_1")
@Case("_2")
@Case("_3")
# @Case(Expected.ERR, "_4")
def test_err(fix):
    path = FIX_PATH / "err"
    sys.path.insert(0, str(path))
    try:
        module = import_module(fix)
        if fix in sys.modules:  # avoid module caching
            if "fastrpc" in str(module):
                del sys.modules[fix]
                module = import_module(fix)

        expected = module.EXPECTED
        actual = _resolve_remote_procedures(path / fix)
        match actual:
            case Success(_):
                pytest.fail(f"Expected {expected.__class__} was not raised")
            case Failure(UnsupportedDefinitionException(definition=d)):
                assert d == expected.definition
            case Failure(e):
                assert e.__class__ == expected.__class__

    finally:
        sys.path.pop(0)
