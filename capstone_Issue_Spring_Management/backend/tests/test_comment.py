"""
Test cases for issue comments.
"""

from app.database.collections import projects_collection


PROJECTS_URL = "/projects"
ISSUES_URL = "/issues"


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


def create_other_member(client):
    client.post(
        "/auth/register",
        json={
            "name": "Other",
            "email": "other@test.com",
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
            "name": "Comment Project",
            "description": "Comment project test",
            "project_key": "CP",
            "members": [
                {
                    "email": "member@test.com"
                }
            ]
        }
    )

    return projects_collection.find_one({"name": "Comment Project"})


def create_issue(client, project_id):
    response = client.post(
        ISSUES_URL,
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "title": "Comment issue",
            "description": "Issue for comment tests.",
            "project_id": str(project_id),
            "assignee_email": "member@test.com",
            "issue_type": "TASK"
        }
    )

    return response.json()["issue_id"]


def test_add_edit_delete_comment(client):
    create_admin(client)
    create_member(client)
    project = create_project(client)
    issue_id = create_issue(client, project["_id"])

    create_response = client.post(
        f"{ISSUES_URL}/{issue_id}/comments",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "body": "Initial comment"
        }
    )

    assert create_response.status_code == 201

    comment_id = create_response.json()["comment_id"]

    list_response = client.get(
        f"{ISSUES_URL}/{issue_id}/comments",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/comments/{comment_id}",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "body": "Updated comment"
        }
    )

    assert update_response.status_code == 200

    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers={
            "X-User-Email": "member@test.com"
        }
    )

    assert delete_response.status_code == 200


def test_non_author_cannot_edit_comment(client):
    create_admin(client)
    create_member(client)
    create_other_member(client)
    project = create_project(client)
    issue_id = create_issue(client, project["_id"])

    create_response = client.post(
        f"{ISSUES_URL}/{issue_id}/comments",
        headers={
            "X-User-Email": "member@test.com"
        },
        json={
            "body": "Initial comment"
        }
    )

    comment_id = create_response.json()["comment_id"]

    response = client.put(
        f"/comments/{comment_id}",
        headers={
            "X-User-Email": "other@test.com"
        },
        json={
            "body": "Wrong author"
        }
    )

    assert response.status_code in [401, 403]
