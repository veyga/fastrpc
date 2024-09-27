import pytest
from enum import StrEnum
from _fastrpc.utils.log import create_logger, LoggerName

from parametrization import Parametrization as P

case = lambda fix: P.case(name=fix, fix=fix)


class Case(StrEnum):
    OK = "ok"
    ERR = "err"


@pytest.fixture(scope="session", autouse=True)
def test_env():
    """
    Temporarily sets ENVIRONMENT=test for a pytest run
    """
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("ENVIRONMENT", "test")
        yield


@pytest.fixture(scope="session")
def logger():
    """
    A logger for use in tests
    """
    # log = create_logger(LoggerName.COLORED)
    log = create_logger(LoggerName.SIMPLE)
    return log
