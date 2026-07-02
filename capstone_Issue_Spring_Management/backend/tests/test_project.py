"""
Test cases for Project Module.
"""

from app.database.collections import projects_collection

PROJECT_URL = "/projects"


def create_admin(client):

    client.post(
        "/auth/register",
        json={
            "name": "Admin",
            "email": "admin@test.com",
            "password": "Password@123",
            "role": "ADMIN"
        }
    )


def create_member(client):

    client.post(
        "/auth/register",
        json={
            "name": "Member",
            "email": "member@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )


def create_sample_project(client):

    return client.post(
        PROJECT_URL,
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "name": "Issue Tracker",
            "description": "Capstone Project",
            "project_key": "IT",
            "members": [
                {
                    "email": "member@test.com"
                }
            ]
        }
    )


def test_create_project_success(client):

    create_admin(client)
    create_member(client)

    response = create_sample_project(client)

    assert response.status_code == 201

    assert response.json()["message"] == \
        "Project created successfully."


def test_duplicate_project_name(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    response = create_sample_project(client)

    assert response.status_code == 409


def test_duplicate_project_key(client):

    create_admin(client)
    create_member(client)

    client.post(
        PROJECT_URL,
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "name": "Project One",
            "description": "First",
            "project_key": "ABC",
            "members": []
        }
    )

    response = client.post(
        PROJECT_URL,
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "name": "Project Two",
            "description": "Second",
            "project_key": "ABC",
            "members": []
        }
    )

    assert response.status_code == 409


def test_member_cannot_create_project(client):

    create_member(client)

    response = client.post(
        PROJECT_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "name": "Member Project",
            "description": "Test",
            "project_key": "MEM",
            "members": []
        }
    )

    assert response.status_code == 403


def test_get_all_projects(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    response = client.get(
        PROJECT_URL,
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_get_project_by_invalid_id(client):

    create_member(client)

    response = client.get(
        f"{PROJECT_URL}/123456",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code in [
        400,
        404,
        422
    ]


def test_delete_project(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    project = projects_collection.find_one(
        {
            "name": "Issue Tracker"
        }
    )

    response = client.delete(
        f"{PROJECT_URL}/{project['_id']}",
        headers={
            "X-User-Email": "admin@test.com"
        }
    )

    assert response.status_code == 200


def test_add_member(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    project = projects_collection.find_one(
        {
            "name": "Issue Tracker"
        }
    )

    client.post(
        "/auth/register",
        json={
            "name": "Garv",
            "email": "garv@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    response = client.post(
        f"{PROJECT_URL}/{project['_id']}/members",
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "email": "garv@test.com"
        }
    )

    assert response.status_code == 200


def test_duplicate_member(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    project = projects_collection.find_one(
        {
            "name": "Issue Tracker"
        }
    )

    response = client.post(
        f"{PROJECT_URL}/{project['_id']}/members",
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "email": "member@test.com"
        }
    )

    assert response.status_code == 409


def test_remove_member(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    project = projects_collection.find_one(
        {
            "name": "Issue Tracker"
        }
    )

    response = client.delete(
        f"{PROJECT_URL}/{project['_id']}/members/member@test.com",
        headers={
            "X-User-Email": "admin@test.com"
        }
    )

    assert response.status_code == 200


def test_get_assigned_projects(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    response = client.get(
        f"{PROJECT_URL}/assigned/me",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200


def test_soft_delete_project(client):

    create_admin(client)
    create_member(client)

    create_sample_project(client)

    project = projects_collection.find_one(
        {
            "name": "Issue Tracker"
        }
    )

    client.delete(
        f"{PROJECT_URL}/{project['_id']}",
        headers={
            "X-User-Email": "admin@test.com"
        }
    )

    deleted_project = projects_collection.find_one(
        {
            "_id": project["_id"]
        }
    )

    assert deleted_project["is_deleted"] is True