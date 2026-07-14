from datetime import datetime
from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from app.database.collections import projects_collection

def _to_object_id(project_id: str) -> ObjectId | None:
    try:
        return ObjectId(project_id)
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


class ProjectRepository:
    @staticmethod
    def create_project(project_document: dict):
        return projects_collection.insert_one(project_document)

    @staticmethod
    def get_project_by_name(project_name: str):
        return projects_collection.find_one({"name": project_name,"is_deleted": False})

    @staticmethod
    def get_project_by_key(project_key: str):
        return projects_collection.find_one({"project_key": project_key,"is_deleted": False})

    @staticmethod
    def get_project_by_id(project_id: str):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return None

        project = projects_collection.find_one({"_id": object_id,"is_deleted": False})

        return _serialize_document(project)

    @staticmethod
    def get_all_projects():
        return [
            _serialize_document(project)
            for project in projects_collection.find({"is_deleted": False})
        ]

    @staticmethod
    def get_projects_by_member(email: str):
        return [
            _serialize_document(project)
            for project in projects_collection.find(
                {
                    "members.email": email,
                    "is_deleted": False
                }
            )
        ]

    @staticmethod
    def update_project(project_id: str,updated_document: dict):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return None

        return projects_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )

    @staticmethod
    def soft_delete_project(project_id: str):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return None

        return projects_collection.update_one(
            {
                "_id": object_id
            },
            {"$set": {"is_deleted": True}}
        )

    @staticmethod
    def add_member(project_id: str,member_document: dict):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return None

        return projects_collection.update_one(
            {"_id": object_id,"is_deleted": False},
            {"$push": {"members": member_document}}
        )

    @staticmethod
    def remove_member(
        project_id: str,
        email: str
    ):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return None

        return projects_collection.update_one(
            {
                "_id": object_id,
                "is_deleted": False
            },
            {"$pull": {"members": {"email": email}}}
        )

    @staticmethod
    def member_exists(project_id: str,email: str):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return False

        project = projects_collection.find_one(
            {
                "_id": object_id,
                "members.email": email,
                "is_deleted": False
            }
        )

        return project is not None

    @staticmethod
    def project_exists(project_id: str):
        object_id = _to_object_id(project_id)

        if object_id is None:
            return False

        project = projects_collection.find_one(
            {
                "_id": object_id,
                "is_deleted": False
            }
        )

        return project is not None
