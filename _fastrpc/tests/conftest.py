import pytest
from pytest import MonkeyPatch
from _fastrpc.utils.log import create_logger, LoggerName


@pytest.fixture(scope="session", autouse=True)
def test_env():
    """
    Temporarily sets ENVIRONMENT=test for a pytest run
    """
    with MonkeyPatch.context() as mp:
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
