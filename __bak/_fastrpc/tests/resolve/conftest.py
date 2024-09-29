import pytest
import sys
from importlib import import_module
from returns.result import Success, Failure
from pathlib import Path

from _fastrpc.tests.conftest import Case
from _fastrpc.server import resolve_remote_procedures
from _fastrpc.server.exceptions import CodeGenExceptions


@pytest.fixture(scope="session")
def _assert_ok():
    def inner(result, expected):
        match result:
            case Success(mapp):
                assert frozenset(mapp.keys()) == expected
            case Failure(e):
                pytest.fail(f"Expected {expected}, {e} raised")
            case x:
                pytest.fail(f"Unhandled case: {x}")

    return inner


@pytest.fixture(scope="session")
def _assert_err():
    def inner(result, expected):
        match result:
            case Success(_):
                pytest.fail(f"Expected {expected.__class__} was not raised")
            case Failure(CodeGenExceptions(exceptions)):
                assert exceptions == expected.exceptions
            case x:
                pytest.fail(f"Unhandled case: {x}")

    return inner


@pytest.fixture(scope="session")
def run_resolve_test(logger, _assert_ok, _assert_err):
    def inner(case_: Case, test_file: Path, fix: str):
        try:
            path = test_file.parent
            sys.path.insert(0, str(path))
            module = import_module(fix.replace("/", "."))
            if fix in sys.modules:  # avoid module caching
                if "fastrpc" in str(module):
                    del sys.modules[fix]
                    module = import_module(fix)
            actual, expected, docs = (
                lambda: resolve_remote_procedures(str(path / fix)),
                module.EXPECTED,
                module.__doc__,
            )
            logger.info(docs)
            result = actual()
            match case_:
                case Case.OK:
                    _assert_ok(result, expected)
                case Case.ERR:
                    _assert_err(result, expected)
                case x:
                    pytest.fail(f"Unhandled Case: {x}")
        finally:
            sys.path.pop(0)

    return inner
