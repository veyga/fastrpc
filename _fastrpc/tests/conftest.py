import pytest
from pytest import MonkeyPatch


@pytest.fixture(scope="session", autouse=True)
def test_env():
    """
    Temporarily sets ENVIRONMENT=test for a pytest run
    """
    with MonkeyPatch.context() as mp:
        mp.setenv("ENVIRONMENT", "test")
        yield
