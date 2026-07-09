"""
Test cases for Issue Module and workflow.
"""

from app.database.collections import issues_collection
from app.database.collections import projects_collection

ISSUES_URL = "/issues"
PROJECTS_URL = "/projects"


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
        PROJECTS_URL,
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


def create_issue(client, project_id, assignee_email=None):
    payload = {
        "title": "Create issue module",
        "description": "Build issue workflow and tests.",
        "project_id": str(project_id),
        "issue_type": "TASK"
    }

    if assignee_email:
        payload["assignee_email"] = assignee_email

    return client.post(
        ISSUES_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json=payload
    )


def test_create_issue_success(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    assert project is not None

    response = create_issue(client, project["_id"])

    assert response.status_code == 201
    assert response.json()["message"] == "Issue created successfully."
    assert response.json()["issue_id"]


def test_create_issue_invalid_project(client):
    create_admin(client)
    create_member(client)

    response = client.post(
        ISSUES_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "title": "Bad issue",
            "description": "Invalid project id.",
            "project_id": "000000000000000000000000",
            "issue_type": "BUG"
        }
    )

    assert response.status_code == 404


def test_create_issue_assignee_not_member(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    assert project is not None

    client.post(
        "/auth/register",
        json={
            "name": "Other",
            "email": "other@test.com",
            "password": "Password@123",
            "role": "MEMBER"
        }
    )

    response = create_issue(
        client,
        project["_id"],
        assignee_email="other@test.com"
    )

    assert response.status_code == 400


def test_get_issue_by_id(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"])
    issue_id = issue_resp.json()["issue_id"]

    response = client.get(
        f"{ISSUES_URL}/{issue_id}",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Create issue module"


def test_get_project_issues(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    create_issue(client, project["_id"])

    response = client.get(
        f"{ISSUES_URL}/project/{project['_id']}",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_all_issues(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    create_issue(client, project["_id"], assignee_email="member@test.com")

    response = client.get(
        ISSUES_URL,
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_assigned_issues(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    create_issue(client, project["_id"], assignee_email="member@test.com")

    response = client.get(
        f"{ISSUES_URL}/assigned/me",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_update_issue(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"], assignee_email="member@test.com")
    issue_id = issue_resp.json()["issue_id"]

    response = client.patch(
        f"{ISSUES_URL}/{issue_id}",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "title": "Update issue title"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue updated successfully."


def test_update_issue_status_workflow(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"], assignee_email="member@test.com")
    issue_id = issue_resp.json()["issue_id"]

    response = client.patch(
        f"{ISSUES_URL}/{issue_id}/status",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "status": "IN_PROGRESS"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Issue status updated successfully."


def test_invalid_status_transition(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"], assignee_email="member@test.com")
    issue_id = issue_resp.json()["issue_id"]

    response = client.patch(
        f"{ISSUES_URL}/{issue_id}/status",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "status": "DONE"
        }
    )

    assert response.status_code == 400


def test_issue_status_transition_backwards(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"], assignee_email="member@test.com")
    issue_id = issue_resp.json()["issue_id"]

    client.patch(
        f"{ISSUES_URL}/{issue_id}/status",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "status": "IN_PROGRESS"
        }
    )

    response = client.patch(
        f"{ISSUES_URL}/{issue_id}/status",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "status": "TODO"
        }
    )

    assert response.status_code == 200


def test_done_issue_cannot_move_backwards(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    issue_resp = create_issue(client, project["_id"], assignee_email="member@test.com")
    issue_id = issue_resp.json()["issue_id"]

    issues_collection.update_one(
        {
            "_id": issues_collection.find_one({"title": "Create issue module"})["_id"]
        },
        {
            "$set": {
                "status": "DONE"
            }
        }
    )

    response = client.patch(
        f"{ISSUES_URL}/{issue_id}/status",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "status": "TODO"
        }
    )

    assert response.status_code == 400


def test_issue_search_filter_and_pagination(client):
    create_admin(client)
    create_member(client)
    create_sample_project(client)

    project = projects_collection.find_one({"name": "Issue Tracker"})
    create_issue(client, project["_id"], assignee_email="member@test.com")

    response = client.get(
        f"{ISSUES_URL}?search=workflow&status=TODO&assignee=member@test.com&paginated=true&page=1&limit=5",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert len(response.json()["items"]) == 1
