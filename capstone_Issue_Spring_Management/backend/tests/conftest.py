"""
Common pytest fixtures.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import application
from app.database.collections import users_collection


@pytest.fixture
def client():
    """
    Create FastAPI test client.
    """

    return TestClient(application)


@pytest.fixture(autouse=True)
def clean_database():
    """
    Clean users collection before
    every test.
    """

    users_collection.delete_many({})

    yield

    users_collection.delete_many({})