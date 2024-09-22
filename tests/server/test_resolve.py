import pytest
import sys
from enum import StrEnum
from fastrpc.server import _resolve_remote_procedures
from importlib import import_module
from parametrization import Parametrization as P
from pathlib import Path


FIX_PATH = Path(__file__).parent / "fixtures"


class Expected(StrEnum):
    OK = "ok"
    ERR = "err"


Case = lambda ex, fix: P.case(name=f"{ex}{fix}", ex=ex, fix=fix)


@P.autodetect_parameters()
@Case(Expected.OK, "_1")
@Case(Expected.OK, "_2")
@Case(Expected.OK, "_3")
@Case(Expected.ERR, "_1")
@Case(Expected.ERR, "_2")
def test_it(ex, fix):
    path = FIX_PATH / ex.value
    sys.path.insert(0, str(path))
    try:
        module = import_module(fix)
        if fix in sys.modules:  # avoid module caching
            if "fastrpc" in str(module):
                del sys.modules[fix]
                module = import_module(fix)
        expected = module.EXPECTED
        match ex:
            case Expected.OK:
                actual = _resolve_remote_procedures(path / fix)
                assert frozenset(actual.keys()) == expected
            case Expected.ERR:
                # try:
                #   _resolve_remote_procedures(path / fix)
                # except expected as e:
                #   print(f"The exception is\n{e}")
                # else:
                #   pytest.fail(f"Expected {expected} was not raised")
                with pytest.raises(expected):
                    _resolve_remote_procedures(path / fix)
            case x:
                pytest.fail(f"Unknown fixture dir: {x}")
    finally:
        sys.path.pop(0)
