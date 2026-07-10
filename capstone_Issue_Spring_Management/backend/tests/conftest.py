"""
Common pytest fixtures.
"""

import pytest
from fastapi.testclient import TestClient

from app.database.collections import projects_collection
from app.database.collections import users_collection
from app.database.collections import issues_collection
from app.database.collections import sprints_collection
from app.database.collections import comments_collection
from app.main import application


@pytest.fixture
def client():
    """
    Create FastAPI test client.
    """

    return TestClient(application)


@pytest.fixture(autouse=True)
def clean_database():
    """
    Clean collections before every test.
    """

    users_collection.delete_many({})
    projects_collection.delete_many({})
    issues_collection.delete_many({})
    sprints_collection.delete_many({})
    comments_collection.delete_many({})

    yield

    users_collection.delete_many({})
    projects_collection.delete_many({})
    issues_collection.delete_many({})
    sprints_collection.delete_many({})
    comments_collection.delete_many({})
