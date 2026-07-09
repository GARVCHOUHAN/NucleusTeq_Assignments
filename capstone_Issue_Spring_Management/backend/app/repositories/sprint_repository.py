from datetime import date
from datetime import datetime
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId

from app.database.collections import sprints_collection


def _to_object_id(identifier: str) -> ObjectId | None:
    try:
        return ObjectId(identifier)
    except (InvalidId, TypeError):
        return None


def _serialize_value(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, list):
        return [
            _serialize_value(item)
            for item in value
        ]

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


class SprintRepository:
    @staticmethod
    def create_sprint(sprint_document: dict):
        return sprints_collection.insert_one(sprint_document)

    @staticmethod
    def get_sprint_by_id(sprint_id: str):
        object_id = _to_object_id(sprint_id)

        if object_id is None:
            return None

        sprint = sprints_collection.find_one(
            {
                "_id": object_id,
                "is_deleted": False
            }
        )

        return _serialize_document(sprint)

    @staticmethod
    def get_sprints_by_project(project_id: str):
        return [
            _serialize_document(sprint)
            for sprint in sprints_collection.find(
                {
                    "project_id": project_id,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def get_all_sprints():
        return [
            _serialize_document(sprint)
            for sprint in sprints_collection.find(
                {
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def issue_in_sprint(sprint_id: str, issue_id: str):
        object_id = _to_object_id(sprint_id)

        if object_id is None:
            return False

        sprint = sprints_collection.find_one(
            {
                "_id": object_id,
                "issue_ids": issue_id,
                "is_deleted": False
            }
        )

        return sprint is not None

    @staticmethod
    def update_sprint(sprint_id: str, updated_document: dict):
        object_id = _to_object_id(sprint_id)

        if object_id is None:
            return None

        return sprints_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )

    @staticmethod
    def add_issue(sprint_id: str, issue_id: str):
        object_id = _to_object_id(sprint_id)

        if object_id is None:
            return None

        return sprints_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$push": {
                    "issue_ids": issue_id
                }
            }
        )

    @staticmethod
    def remove_issue(sprint_id: str, issue_id: str):
        object_id = _to_object_id(sprint_id)

        if object_id is None:
            return None

        return sprints_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$pull": {
                    "issue_ids": issue_id
                }
            }
        )
