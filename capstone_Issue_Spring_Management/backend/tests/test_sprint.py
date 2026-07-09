"""
Test cases for Sprint Module.
"""

from app.database.collections import issues_collection
from app.database.collections import projects_collection


PROJECTS_URL = "/projects"
ISSUES_URL = "/issues"
SPRINTS_URL = "/sprints"


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


def create_project(client):
    client.post(
        PROJECTS_URL,
        headers={
            "X-User-Email": "admin@test.com"
        },
        json={
            "name": "Sprint Project",
            "description": "Sprint project test",
            "project_key": "SP",
            "members": [
                {
                    "email": "member@test.com"
                }
            ]
        }
    )

    return projects_collection.find_one({"name": "Sprint Project"})


def create_issue(client, project_id, status="TODO"):
    response = client.post(
        ISSUES_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "title": "Sprint issue",
            "description": "Issue for sprint tests.",
            "project_id": str(project_id),
            "assignee_email": "member@test.com",
            "status": status,
            "issue_type": "TASK"
        }
    )

    return response.json()["issue_id"]


def create_sprint(client, project_id):
    return client.post(
        SPRINTS_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "name": "Sprint One",
            "project_id": str(project_id),
            "start_date": "2026-07-01",
            "end_date": "2026-07-14"
        }
    )


def test_create_sprint(client):
    create_admin(client)
    create_member(client)
    project = create_project(client)

    response = create_sprint(client, project["_id"])

    assert response.status_code == 201
    assert response.json()["message"] == "Sprint created successfully."


def test_add_and_remove_issue_from_sprint(client):
    create_admin(client)
    create_member(client)
    project = create_project(client)
    issue_id = create_issue(client, project["_id"])
    sprint_id = create_sprint(client, project["_id"]).json()["sprint_id"]

    add_response = client.post(
        f"{SPRINTS_URL}/{sprint_id}/issues",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "issue_id": issue_id
        }
    )

    assert add_response.status_code == 200

    remove_response = client.delete(
        f"{SPRINTS_URL}/{sprint_id}/issues/{issue_id}",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert remove_response.status_code == 200


def test_prevent_adding_done_issue_to_sprint(client):
    create_admin(client)
    create_member(client)
    project = create_project(client)
    issue_id = create_issue(client, project["_id"])
    issues_collection.update_one(
        {
            "_id": issues_collection.find_one({"title": "Sprint issue"})["_id"]
        },
        {
            "$set": {
                "status": "DONE"
            }
        }
    )
    sprint_id = create_sprint(client, project["_id"]).json()["sprint_id"]

    response = client.post(
        f"{SPRINTS_URL}/{sprint_id}/issues",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "issue_id": issue_id
        }
    )

    assert response.status_code == 400


def test_sprint_lifecycle(client):
    create_admin(client)
    create_member(client)
    project = create_project(client)
    sprint_id = create_sprint(client, project["_id"]).json()["sprint_id"]

    start_response = client.patch(
        f"{SPRINTS_URL}/{sprint_id}/start",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert start_response.status_code == 200

    complete_response = client.patch(
        f"{SPRINTS_URL}/{sprint_id}/complete",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert complete_response.status_code == 200
