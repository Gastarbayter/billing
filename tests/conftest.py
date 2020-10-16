import pytest
from starlette.testclient import TestClient

from billing.app.fastapi import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())
