import pytest
import sys
from importlib import import_module
from parametrization import Parametrization as P
from pathlib import Path
from returns.result import Success, Failure

from _fastrpc.server import resolve_remote_procedures
from _fastrpc.server.exceptions import UnsupportedDefinitionException


FIX_PATH = Path(__file__).parent / "fixtures"


case = lambda fix: P.case(name=fix, fix=fix)


@pytest.fixture()
def resolver():
    def inner(directory, fix):
        try:
            path = FIX_PATH / directory
            sys.path.insert(0, str(path))
            module = import_module(fix)
            if fix in sys.modules:  # avoid module caching
                if "fastrpc" in str(module):
                    del sys.modules[fix]
                    module = import_module(fix)
            return (
                resolve_remote_procedures(path / fix),
                module.EXPECTED,
                module.__doc__,
            )
        finally:
            sys.path.pop(0)

    return inner


@P.autodetect_parameters()
@case("_1")
@case("_2")
@case("_3")
def test_ok(fix, resolver, logger):
    actual, expected, docs = resolver("ok", fix)
    logger.info(docs)
    match actual:
        case Success(mapp):
            assert frozenset(mapp.keys()) == expected
        case Failure(e):
            pytest.fail(f"Expected {expected}, {e} raised")


# SYNCHRONOUS = "synchronous (non-async)"
# OBSCURED = "obscured defintion (ex: __fn)"
# NESTED = "nested function"
# METHOD = "methods"
# UNTYPED_ARGUMENTS = "untyped procedure arguments"
# UNTYPED_RETURN = "untyped procedure return type"
# # _NA = "N/A"
@P.autodetect_parameters()
@case("_1")
@case("_2")
@case("_3")
# @Case("_4") # nested functions
def test_err(fix, resolver, logger):
    actual, expected, docs = resolver("err", fix)
    logger.info(docs)
    match actual:
        case Success(_):
            pytest.fail(f"Expected {expected.__class__} was not raised")
        case Failure(UnsupportedDefinitionException(definition=d)):
            assert d == expected.definition
        case Failure(e):
            assert e.__class__ == expected.__class__
