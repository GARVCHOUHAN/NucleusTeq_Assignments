from datetime import datetime
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from app.database.collections import comments_collection


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


class CommentRepository:
    @staticmethod
    def create_comment(comment_document: dict):
        return comments_collection.insert_one(comment_document)

    @staticmethod
    def get_comment_by_id(comment_id: str):
        object_id = _to_object_id(comment_id)

        if object_id is None:
            return None

        comment = comments_collection.find_one(
            {
                "_id": object_id,
                "is_deleted": False
            }
        )

        return _serialize_document(comment)

    @staticmethod
    def get_comments_by_issue(issue_id: str):
        return [
            _serialize_document(comment)
            for comment in comments_collection.find(
                {
                    "issue_id": issue_id,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def update_comment(comment_id: str, updated_document: dict):
        object_id = _to_object_id(comment_id)

        if object_id is None:
            return None

        return comments_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )

    @staticmethod
    def soft_delete_comment(comment_id: str, updated_document: dict):
        object_id = _to_object_id(comment_id)

        if object_id is None:
            return None

        return comments_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )
