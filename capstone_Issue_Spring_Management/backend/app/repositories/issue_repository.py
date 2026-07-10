from datetime import datetime
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from app.database.collections import issues_collection


def _to_object_id(identifier: str) -> ObjectId | None:
    try:
        return ObjectId(identifier)
    except (InvalidId, TypeError):
        return None


def _serialize_value(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, list):
        return [_serialize_value(item) for item in value]

    if isinstance(value, dict):
        return {
            key: _serialize_value(item)
            for key, item in value.items()
        }

    return value


def _serialize_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    return _serialize_value(document)


class IssueRepository:
    """
    Issue repository CRUD operations.
    """

    @staticmethod
    def create_issue(issue_document: dict):
        issue_document.setdefault("is_deleted", False)
        return issues_collection.insert_one(issue_document)

    @staticmethod
    def get_all_issues():
        return [
            _serialize_document(issue)
            for issue in issues_collection.find(
                {
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def get_issues_by_project_ids(project_ids: list):
        if not project_ids:
            return []

        return [
            _serialize_document(issue)
            for issue in issues_collection.find(
                {
                    "project_id": {
                        "$in": project_ids
                    },
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def count_issues_by_project(project_id: str):
        return issues_collection.count_documents(
            {
                "project_id": project_id,
                "is_deleted": False
            }
        )

    @staticmethod
    def search_issues(
        project_id: str | None = None,
        status: str | None = None,
        assignee_email: str | None = None,
        search: str | None = None
    ):
        query = {
            "is_deleted": False
        }

        if project_id:
            query["project_id"] = project_id

        if status:
            query["status"] = status

        if assignee_email:
            query["assignee_email"] = assignee_email

        if search:
            query["$or"] = [
                {
                    "title": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "description": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]

        return [
            _serialize_document(issue)
            for issue in issues_collection.find(query)
        ]

    @staticmethod
    def get_issue_by_id(issue_id: str):
        object_id = _to_object_id(issue_id)

        if object_id is None:
            return None

        issue = issues_collection.find_one(
            {
                "_id": object_id,
                "is_deleted": False
            }
        )

        return _serialize_document(issue)

    @staticmethod
    def get_issues_by_project(project_id: str):
        return [
            _serialize_document(issue)
            for issue in issues_collection.find(
                {
                    "project_id": project_id,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def get_issues_by_assignee(email: str):
        return [
            _serialize_document(issue)
            for issue in issues_collection.find(
                {
                    "assignee_email": email,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def get_issues_by_parent_id(parent_id: str):
        return [
            _serialize_document(issue)
            for issue in issues_collection.find(
                {
                    "parent_id": parent_id,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def delete_issue(issue_id: str):
        object_id = _to_object_id(issue_id)

        if object_id is None:
            return None

        return issues_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": {
                    "is_deleted": True
                }
            }
        )

    @staticmethod
    def update_issue(issue_id: str, updated_document: dict):
        object_id = _to_object_id(issue_id)

        if object_id is None:
            return None

        return issues_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )
