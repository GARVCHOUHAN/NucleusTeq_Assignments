from fastapi.testclient import TestClient

from app.main import application

client = TestClient(
    application
)


def test_health_api():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {

        "status": "Running",

        "message": "Issue & Sprint Management System API"

    }