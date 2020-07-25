import pytest

from scorer import create_app
from config import TestingConfig


@pytest.fixture
def test_client():
    test_app = create_app("test")

    testing_client = test_app.test_client()

    ctx = test_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()