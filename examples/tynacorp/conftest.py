import pytest
from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def test_client() -> TestClient:
    client = TestClient(app)
    setattr(TestClient, "is_ok", lambda _, code: 200 <= code <= 299)
    setattr(TestClient, "is_client_error", lambda _, code: 400 <= code <= 499)
    return client


@pytest.fixture(scope="session", autouse=True)
def test_env():
    """
    Temporarily sets ENVIRONMENT=test for a pytest run
    """
    with MonkeyPatch.context() as mp:
        mp.setenv("ENVIRONMENT", "test")
        yield
